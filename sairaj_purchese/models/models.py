# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class sairaj_purchese(models.Model):
    _inherit= 'res.partner'

    vendor_type = fields.Selection([('Local','Local'),('Non Local','Non Local')],copy=False, index=True, default='Local',track_visibility='onchange')

class PurchaseOrderExtended(models.Model):
    _inherit = "purchase.order"

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    partner_id_extended = fields.Many2many('res.partner', string='Vendor', required=True, states=READONLY_STATES, change_default=True, track_visibility='always', help="You can find a vendor by its Name, TIN, Email or Internal Reference.")

    @api.onchange('partner_id_extended')
    def partner_id_extended_change(self):
        # import pdb
        # pdb.set_trace()
        for i in self:
            if len( i.partner_id_extended) == 1:
                    i.partner_id=i.partner_id_extended

    @api.multi
    def action_rfq_send(self):
        # import pdb
        # pdb.set_trace()
        '''
        This function opens a window to compose an email, with the edi purchase template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            if self.env.context.get('send_rfq', False):
                template_id = ir_model_data.get_object_reference('sairaj_purchese', 'email_template_edi_purchase_extended')[1]
            else:
                template_id = ir_model_data.get_object_reference('purchase', 'email_template_edi_purchase_done')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'purchase.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            'mark_rfq_as_sent': True,
        })
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def get_emails_list(self):
        # import pdb
        # pdb.set_trace()
        email_ids = ''
        for partner in self.partner_id_extended:
            email_ids = email_ids + ',' + str(partner.email)
        return email_ids

        # user_group = self.env.ref("res.group_res_user")
        # email_list = [usr.partner_id.email for usr in user_group.users if usr.partner_id.email]
        # return ",".join(email_list)