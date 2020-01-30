from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
from odoo.addons import decimal_precision as dp
import pdb

class MrpWorkorderEX(models.Model):
    _inherit = 'mrp.workorder'

    @api.depends('mfg_checklist')
    def checklist_progress(self):
        """:return the value for the check list progress"""
        for rec in self:
            total_len = self.env['mfg.checklist'].search_count([])
            check_list_len = len(rec.mfg_checklist)
            if total_len != 0:
                rec.checklist_progress = (check_list_len*100) / total_len

    mfg_checklist = fields.Many2many('mfg.checklist', string='Check List')

    checklist_progress = fields.Float(compute=checklist_progress, string='Progress', store=True, recompute=True,
                                      default=0.0)
    max_rate = fields.Integer(string='Maximum rate', default=100)

    mrp_checklist_id = fields.One2many('mrp.workorder.checklist','op_workorder_id', string='Checklist')
    #remarks_id = fields.One2many('mrp.remarks','op_workorder_id', string='Remarks')

    test_field = fields.Char('Config Checkbox', default='Nothing', readonly=True, store=True)

    @api.multi
    def button_start_extend(self):
        #pdb.set_trace()
        timeline = self.env['mrp.workcenter.productivity']

        check_list = self.env['mrp.workorder.checklist']

        if self.duration < self.duration_expected:
            loss_id = self.env['mrp.workcenter.productivity.loss'].search([('loss_type','=','productive')], limit=1)
            if not len(loss_id):
                raise UserError(_("You need to define at least one productivity loss in the category 'Productivity'. Create one from the Manufacturing app, menu: Configuration / Productivity Losses."))
        else:
            loss_id = self.env['mrp.workcenter.productivity.loss'].search([('loss_type','=','performance')], limit=1)
            if not len(loss_id):
                raise UserError(_("You need to define at least one productivity loss in the category 'Performance'. Create one from the Manufacturing app, menu: Configuration / Productivity Losses."))
        for workorder in self:
            if workorder.production_id.state != 'progress':
                workorder.production_id.write({
                    'state': 'progress',
                    'date_start': datetime.now(),
                })
            timeline.create({
                'workorder_id': workorder.id,
                'workcenter_id': workorder.workcenter_id.id,
                'description': _('Time Tracking: ')+self.env.user.name,
                'loss_id': loss_id[0].id,
                'date_start': datetime.now(),
                'user_id': self.env.user.id
            })

        # if self.workcenter_id and self.id:
        #     #pdb.set_trace()
        #     a = self.workcenter_id[0].id or self.workcenter_id
        #     b = self.id and self.id
        #     self._cr.execute("""SELECT * FROM insert_workorder_check_list_1(%s,%s)""", (b, a))
        #     self._cr.fetchall()

        #pdb.set_trace()
        self._cr.execute("""SELECT * FROM insert_workorder_check_list_test(%s,%s)""", (self.id, self.workcenter_id[0].id))

        return self.write({'state': 'progress',
                    'date_start': datetime.now(),
        })

    @api.multi
    def button_finish_extended(self):
        self._cr.execute("""
                UPDATE mrp_workorder
                SET test_field = (SELECT module_mrp_wo_checklist 
                FROM res_config_settings WHERE id = (SELECT max(id)
                FROM res_config_settings WHERE module_mrp_wo_checklist is not null))
            """)

        if self.test_field == 'true':
            
            self._cr.execute("""SELECT count (id) 
                FROM mrp_workorder_checklist woc 
                WHERE op_workorder_id = %s AND (yes !='f' or no !='f' or na !='f')""" % (self.id))
            a = self._cr.fetchall()

            self._cr.execute("""SELECT count (id) 
                FROM mrp_workorder_checklist woc 
                WHERE op_workorder_id = %s """ % (self.id))
            b = self._cr.fetchall()

            if a != b:
                raise UserError(_("Please check all the Checklists are filled...!"))
            
            elif a == b:

                self.ensure_one()
                self.end_all()
                return self.write({'state': 'done', 'date_finished': fields.Datetime.now()})



    @api.multi
    def check_all_checklists(self):
        self._cr.execute("""
                UPDATE mrp_workorder
                SET test_field = (SELECT module_mrp_wo_checklist 
                FROM res_config_settings WHERE id = (SELECT max(id)
                FROM res_config_settings WHERE module_mrp_wo_checklist is not null))
            """)

        if self.test_field == 'true':

            self._cr.execute("""SELECT count (id) 
                FROM mrp_workorder_checklist woc 
                WHERE op_workorder_id = %s AND (yes !='f' or no !='f' or na !='f')""" % (self.id))

            a = self._cr.fetchall()

            self._cr.execute("""SELECT count (id) 
                FROM mrp_workorder_checklist woc 
                WHERE op_workorder_id = %s """ % (self.id))

            b = self._cr.fetchall()

            if a != b:
                raise UserError(_("Please check all the Checklists are filled...!"))
            
            elif a == b:
                self.ensure_one()
                if self.qty_producing <= 0:
                    raise UserError(_('Please set the quantity you are currently producing. It should be different from zero.'))

                if (self.production_id.product_id.tracking != 'none') and not self.final_lot_id and self.move_raw_ids:
                    raise UserError(_('You should provide a lot/serial number for the final product'))

                # Update quantities done on each raw material line
                # For each untracked component without any 'temporary' move lines,
                # (the new workorder tablet view allows registering consumed quantities for untracked components)
                # we assume that only the theoretical quantity was used
                for move in self.move_raw_ids:
                    if move.has_tracking == 'none' and (move.state not in ('done', 'cancel')) and move.bom_line_id\
                                and move.unit_factor and not move.move_line_ids.filtered(lambda ml: not ml.done_wo):
                        rounding = move.product_uom.rounding
                        if self.product_id.tracking != 'none':
                            qty_to_add = float_round(self.qty_producing * move.unit_factor, precision_rounding=rounding)
                            move._generate_consumed_move_line(qty_to_add, self.final_lot_id)
                        else:
                            move.quantity_done += float_round(self.qty_producing * move.unit_factor, precision_rounding=rounding)

                # Transfer quantities from temporary to final move lots or make them final
                for move_line in self.active_move_line_ids:
                    # Check if move_line already exists
                    if move_line.qty_done <= 0:  # rounding...
                        move_line.sudo().unlink()
                        continue
                    if move_line.product_id.tracking != 'none' and not move_line.lot_id:
                        raise UserError(_('You should provide a lot/serial number for a component'))
                    # Search other move_line where it could be added:
                    lots = self.move_line_ids.filtered(lambda x: (x.lot_id.id == move_line.lot_id.id) and (not x.lot_produced_id) and (not x.done_move) and (x.product_id == move_line.product_id))
                    if lots:
                        lots[0].qty_done += move_line.qty_done
                        lots[0].lot_produced_id = self.final_lot_id.id
                        move_line.sudo().unlink()
                    else:
                        move_line.lot_produced_id = self.final_lot_id.id
                        move_line.done_wo = True

                # One a piece is produced, you can launch the next work order
                if self.next_work_order_id.state == 'pending':
                    self.next_work_order_id.state = 'ready'

                self.move_line_ids.filtered(
                    lambda move_line: not move_line.done_move and not move_line.lot_produced_id and move_line.qty_done > 0
                ).write({
                    'lot_produced_id': self.final_lot_id.id,
                    'lot_produced_qty': self.qty_producing
                })

                # If last work order, then post lots used
                # TODO: should be same as checking if for every workorder something has been done?
                if not self.next_work_order_id:
                    production_move = self.production_id.move_finished_ids.filtered(lambda x: (x.product_id.id == self.production_id.product_id.id) and (x.state not in ('done', 'cancel')))
                    if production_move.has_tracking != 'none':
                        move_line = production_move.move_line_ids.filtered(lambda x: x.lot_id.id == self.final_lot_id.id)
                        if move_line:
                            move_line.product_uom_qty += self.qty_producing
                        else:
                            move_line.create({'move_id': production_move.id,
                                         'product_id': production_move.product_id.id,
                                         'lot_id': self.final_lot_id.id,
                                         'product_uom_qty': self.qty_producing,
                                         'product_uom_id': production_move.product_uom.id,
                                         'qty_done': self.qty_producing,
                                         'workorder_id': self.id,
                                         'location_id': production_move.location_id.id, 
                                         'location_dest_id': production_move.location_dest_id.id,
                                         })
                    else:
                        production_move.quantity_done += self.qty_producing

                if not self.next_work_order_id:
                    for by_product_move in self.production_id.move_finished_ids.filtered(lambda x: (x.product_id.id != self.production_id.product_id.id) and (x.state not in ('done', 'cancel'))):
                        if by_product_move.has_tracking == 'none':
                            by_product_move.quantity_done += self.qty_producing * by_product_move.unit_factor

                # Update workorder quantity produced
                self.qty_produced += self.qty_producing

                if self.final_lot_id:
                    self.final_lot_id.use_next_on_work_order_id = self.next_work_order_id
                    self.final_lot_id = False

                # Set a qty producing
                rounding = self.production_id.product_uom_id.rounding
                if float_compare(self.qty_produced, self.production_id.product_qty, precision_rounding=rounding) >= 0:
                    self.qty_producing = 0
                elif self.production_id.product_id.tracking == 'serial':
                    self._assign_default_final_lot_id()
                    self.qty_producing = 1.0
                    self._generate_lot_ids()
                else:
                    self.qty_producing = float_round(self.production_id.product_qty - self.qty_produced, precision_rounding=rounding)
                    self._generate_lot_ids()

                if self.next_work_order_id and self.production_id.product_id.tracking != 'none':
                    self.next_work_order_id._assign_default_final_lot_id()

                if float_compare(self.qty_produced, self.production_id.product_qty, precision_rounding=rounding) >= 0:
                    self.button_finish()
                #return True
        else:
            self.ensure_one()
            if self.qty_producing <= 0:
                raise UserError(_('Please set the quantity you are currently producing. It should be different from zero.'))

            if (self.production_id.product_id.tracking != 'none') and not self.final_lot_id and self.move_raw_ids:
                raise UserError(_('You should provide a lot/serial number for the final product'))

            # Update quantities done on each raw material line
            # For each untracked component without any 'temporary' move lines,
            # (the new workorder tablet view allows registering consumed quantities for untracked components)
            # we assume that only the theoretical quantity was used
            for move in self.move_raw_ids:
                if move.has_tracking == 'none' and (move.state not in ('done', 'cancel')) and move.bom_line_id\
                            and move.unit_factor and not move.move_line_ids.filtered(lambda ml: not ml.done_wo):
                    rounding = move.product_uom.rounding
                    if self.product_id.tracking != 'none':
                        qty_to_add = float_round(self.qty_producing * move.unit_factor, precision_rounding=rounding)
                        move._generate_consumed_move_line(qty_to_add, self.final_lot_id)
                    else:
                        move.quantity_done += float_round(self.qty_producing * move.unit_factor, precision_rounding=rounding)

            # Transfer quantities from temporary to final move lots or make them final
            for move_line in self.active_move_line_ids:
                # Check if move_line already exists
                if move_line.qty_done <= 0:  # rounding...
                    move_line.sudo().unlink()
                    continue
                if move_line.product_id.tracking != 'none' and not move_line.lot_id:
                    raise UserError(_('You should provide a lot/serial number for a component'))
                # Search other move_line where it could be added:
                lots = self.move_line_ids.filtered(lambda x: (x.lot_id.id == move_line.lot_id.id) and (not x.lot_produced_id) and (not x.done_move) and (x.product_id == move_line.product_id))
                if lots:
                    lots[0].qty_done += move_line.qty_done
                    lots[0].lot_produced_id = self.final_lot_id.id
                    move_line.sudo().unlink()
                else:
                    move_line.lot_produced_id = self.final_lot_id.id
                    move_line.done_wo = True

            # One a piece is produced, you can launch the next work order
            if self.next_work_order_id.state == 'pending':
                self.next_work_order_id.state = 'ready'

            self.move_line_ids.filtered(
                lambda move_line: not move_line.done_move and not move_line.lot_produced_id and move_line.qty_done > 0
            ).write({
                'lot_produced_id': self.final_lot_id.id,
                'lot_produced_qty': self.qty_producing
            })

            # If last work order, then post lots used
            # TODO: should be same as checking if for every workorder something has been done?
            if not self.next_work_order_id:
                production_move = self.production_id.move_finished_ids.filtered(lambda x: (x.product_id.id == self.production_id.product_id.id) and (x.state not in ('done', 'cancel')))
                if production_move.has_tracking != 'none':
                    move_line = production_move.move_line_ids.filtered(lambda x: x.lot_id.id == self.final_lot_id.id)
                    if move_line:
                        move_line.product_uom_qty += self.qty_producing
                    else:
                        move_line.create({'move_id': production_move.id,
                                     'product_id': production_move.product_id.id,
                                     'lot_id': self.final_lot_id.id,
                                     'product_uom_qty': self.qty_producing,
                                     'product_uom_id': production_move.product_uom.id,
                                     'qty_done': self.qty_producing,
                                     'workorder_id': self.id,
                                     'location_id': production_move.location_id.id, 
                                     'location_dest_id': production_move.location_dest_id.id,
                                     })
                else:
                    production_move.quantity_done += self.qty_producing

            if not self.next_work_order_id:
                for by_product_move in self.production_id.move_finished_ids.filtered(lambda x: (x.product_id.id != self.production_id.product_id.id) and (x.state not in ('done', 'cancel'))):
                    if by_product_move.has_tracking == 'none':
                        by_product_move.quantity_done += self.qty_producing * by_product_move.unit_factor

            # Update workorder quantity produced
            self.qty_produced += self.qty_producing

            if self.final_lot_id:
                self.final_lot_id.use_next_on_work_order_id = self.next_work_order_id
                self.final_lot_id = False

            # Set a qty producing
            rounding = self.production_id.product_uom_id.rounding
            if float_compare(self.qty_produced, self.production_id.product_qty, precision_rounding=rounding) >= 0:
                self.qty_producing = 0
            elif self.production_id.product_id.tracking == 'serial':
                self._assign_default_final_lot_id()
                self.qty_producing = 1.0
                self._generate_lot_ids()
            else:
                self.qty_producing = float_round(self.production_id.product_qty - self.qty_produced, precision_rounding=rounding)
                self._generate_lot_ids()

            if self.next_work_order_id and self.production_id.product_id.tracking != 'none':
                self.next_work_order_id._assign_default_final_lot_id()

            if float_compare(self.qty_produced, self.production_id.product_qty, precision_rounding=rounding) >= 0:
                self.button_finish()
            return True


class MrpWorkorderChecklist(models.Model):
    _name = 'mrp.workorder.checklist'

    workcenter_id = fields.Many2one('mrp.workcenter', compute='_change_workcenter_status', store=True)

    @api.depends('op_workorder_id')
    def _change_workcenter_status(self):
        for op in self:
            if op.op_workorder_id:
                for get in op:
                    get.workcenter_id = get.checklist_ids.workcenter_id
                    get.description = get.checklist_ids.description


    op_workorder_id = fields.Many2one('mrp.workorder', string='Workorder')
    checklist_ids = fields.Many2one('mrp.checklist',string='Inspection Checklists',)
    yes = fields.Boolean(string='Yes')
    no = fields.Boolean(string='No')
    na = fields.Boolean(string='N/A')
    comments = fields.Char('Comments') 
    description = fields.Char(string='Description', compute='_change_workcenter_status', store=True)


    @api.onchange('yes')
    def _change_boolean_status_yes(self):
        if self.yes:
            self.yes = False
            self.no = False
            self.na = False
            self.yes = True

    @api.onchange('no')
    def _change_boolean_status_no(self):
        if self.no:
            self.no = False
            self.yes=False
            self.na=False
            self.no = True

    @api.onchange('na')
    def _change_boolean_status_na(self):
        if self.na:
            self.na = False
            self.no=False
            self.yes=False
            self.na = True




class MFGChecklist(models.Model):
    _name = 'mfg.checklist'
    _description = 'Checklist for the Work center'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')


class MrpRoutingWorkorder(models.Model):
    _inherit = 'mrp.routing.workcenter'

    checklist_id = fields.One2many('mrp.checklist','op_id', string='Checklist')
    remarks_id = fields.One2many('mrp.remarks','op_id', string='Remarks')


class MRPChecklist(models.Model):
    _name = 'mrp.checklist'
    _description = 'Checklist for the Work center'

    op_id = fields.Many2one('mrp.routing.workcenter', string='Checklist')
    name = fields.Many2one('mfg.checklist', string='Name', required=True)
    description = fields.Char(string='Description')
    workcenter_id = fields.Many2one('mrp.workcenter', compute='_change_workcenter_status', store=True)
    routing_id = fields.Many2one('mrp.routing', compute='_change_workcenter_status', store=True)


    @api.depends('name')
    def _change_workcenter_status(self):
        for op in self:
            if op.name:
                for get in op:
                    get.workcenter_id = get.op_id.workcenter_id
                    get.routing_id = get.op_id.routing_id


class MRPRemarks(models.Model):
    _name = 'mrp.remarks'
    _description = 'Checklist for the Work center'


    op_id = fields.Many2one('mrp.routing.workcenter', string='Remarks')
    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')