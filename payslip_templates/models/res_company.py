# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://opensource.org/licenses/LGPL-3.0).
#
# This software and associated files (the "Software") may only be used (executed,
# modified, executed after modifications) if you have purchased a valid license
# from the authors, typically via Odoo Apps, or if you have received a written
# agreement from the authors of the Software (see the COPYRIGHT section below).
#
# You may develop Odoo modules that use the Software as a library (typically
# by depending on it, importing it and using its resources), but without copying
# any source code or material from the Software. You may distribute those
# modules under the license of your choice, provided that this license is
# compatible with the terms of the Odoo Proprietary License (For example:
# LGPL, MIT, or proprietary licenses similar to this one).
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the Software
# or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
#########COPYRIGHT#####
# © 2016 Bernard K Too<bernard.too@optima.co.ke>
from openerp import models, fields, api


class DefaultPayslipSettings(models.Model):
    _inherit = ["res.company"]

    @api.model
    def _default_ps_template(self):
        def_tpl = self.env['ir.ui.view'].search(
            [
                ('key',
                 'like',
                 'payslip_templates.PAYSLIP\_%\_document'),
                ('type',
                 '=',
                 'qweb')],
            order='id desc',
            limit=1)
        return def_tpl or self.env.ref('hr_payroll.report_payslip')

    @api.model
    def _default_dps_template(self):
        def_tpl = self.env['ir.ui.view'].search(
            [
                ('key',
                 'like',
                 'payslip_templates.PAYSLIP\_%\_detailed'),
                ('type',
                 '=',
                 'qweb')],
            order='id desc',
            limit=1)
        return def_tpl or self.env.ref('hr_payroll.report_payslipdetails')

    ptemplate_id = fields.Many2one(
        'ir.ui.view',
        'Payslip Template',
        default=_default_ps_template,
        domain="[('type', '=', 'qweb'), ('key', 'like', 'payslip_templates.PAYSLIP\_%\_document' )]",
        required=False)
    pdetailed_template_id = fields.Many2one(
        'ir.ui.view',
        'Detailed Payslip Template',
        default=_default_dps_template,
        domain="[('type', '=', 'qweb'), ('key', 'like', 'payslip_templates.PAYSLIP\_%\_detailed' )]",
        required=False)
    payslip_logo = fields.Binary(
        string='Payslip Logo',
        attachment=True,
        help="Default Logo for Payslips")
    podd = fields.Char(
        'Odd parity Color',
        size=7,
        default='#DDDDDD',
        help="The background color for Odd lines in the payslip",
        required=True)
    peven = fields.Char(
        'Even parity Color',
        size=7,
        default='#EEEEEE',
        help="The background color for Even lines in the payslip",
        required=True)
    ptheme_color = fields.Char(
        'Theme Color',
        size=7,
        default='#545454',
        help="The Main Theme color of the payslip",
        required=True)
    ptheme_txt_color = fields.Char(
        'Theme Text Color',
        size=7,
        default='#FFFFFF',
        help="The font color of the areas with the theme color",
        required=True)
    ptext_color = fields.Char(
        'Text Color',
        size=7,
        default='#545454',
        help="The Text color of the payslip",
        required=True)
    pname_color = fields.Char(
        'Company Name Color',
        size=7,
        default='#9ABE00',
        help="The Text color of the Company Name",
        required=True)
    pcust_color = fields.Char(
        'Employee Name Color',
        size=7,
        default='#9ABE00',
        help="The Text color of the Employee Name",
        required=True)
    pheader_font = fields.Selection([(x, str(x)) for x in range(
        1, 51)], default=10, string="Header Font-Size(px):", required=True)
    pbody_font = fields.Selection([(x, str(x)) for x in range(
        1, 51)], default=10, string="Body Font-Size(px):", required=True)
    pfooter_font = fields.Selection([(x, str(x)) for x in range(
        1, 51)], default=10, string="Footer Font-Size(px):", required=True)
    pfont_family = fields.Char(
        'Font Family:',
        default='san-serif',
        help="If no font is set, 'Times New Roman' will be used")
