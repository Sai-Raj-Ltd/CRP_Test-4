# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sairaj_inventory(models.Model):
    _inherit = 'stock.inventory'

    state = fields.Selection(string='Status', selection=[('draft', 'Draft'),('cancel', 'Cancelled'),('cancel', 'Cancelled'),('confirm', 'In Progress'),('approval', 'To Approve'),('done', 'Validated')],copy=False, index=True, readonly=True,default='draft')

    def action_for_approval(self):
        self.state='approval'


