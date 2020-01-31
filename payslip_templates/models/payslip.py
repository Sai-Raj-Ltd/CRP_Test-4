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
from odoo import models, fields, api


class PayslipTemplates(models.Model):
    _inherit = ["hr.payslip"]

    payslip_logo = fields.Binary(
        "Payslip Logo",
        attachment=True,
        help="This field holds the image used as logo for the payslip, if non is uploaded, the default company logo will be used",
        default=lambda self: self.env.user.company_id.payslip_logo)
    template_id = fields.Many2one(
        'ir.ui.view',
        'Payslip Template',
        domain="[('type', '=', 'qweb'), ('key', 'like', 'payslip_templates.PAYSLIP\_%\_document' )]",
        default=lambda self: self.env.user.company_id.ptemplate_id)
    detailed_template_id = fields.Many2one(
        'ir.ui.view',
        'Detailed Payslip Template',
        domain="[('type', '=', 'qweb'), ('key', 'like', 'payslip_templates.PAYSLIP\_%\_detailed' )]",
        default=lambda self: self.env.user.company_id.pdetailed_template_id)
    odd = fields.Char(
        'Odd parity Color',
        size=7,
        required=True,
        help="The background color for Odd lines in the payslip",
        default=lambda self: self.env.user.company_id.podd)
    even = fields.Char(
        'Even parity Color',
        size=7,
        required=True,
        help="The background color for Even lines in the payslip",
        default=lambda self: self.env.user.company_id.peven)
    theme_color = fields.Char(
        'Theme Color',
        size=7,
        required=True,
        help="The Main Theme color of the payslip",
        default=lambda self: self.env.user.company_id.ptheme_color)
    theme_txt_color = fields.Char(
        'Theme Text Color',
        size=7,
        required=True,
        help="The Text color of the areas with theme color",
        default=lambda self: self.env.user.company_id.ptheme_txt_color)
    text_color = fields.Char(
        'Text Color',
        size=7,
        required=True,
        help="The Text color of the payslip",
        default=lambda self: self.env.user.company_id.ptext_color)
    name_color = fields.Char(
        'Company Name Color',
        size=7,
        required=True,
        help="The Text color of the Company Name",
        default=lambda self: self.env.user.company_id.pname_color)
    cust_color = fields.Char(
        'Employee Name Color',
        size=7,
        required=True,
        help="The Text color of the Employee Name",
        default=lambda self: self.env.user.company_id.pcust_color)
    header_font = fields.Selection(
        [
            (x,
             str(x)) for x in range(
                1,
                51)],
        string="Header Font-Size(px):",
        required=True,
        default=lambda self: self.env.user.company_id.pheader_font)
    body_font = fields.Selection(
        [
            (x,
             str(x)) for x in range(
                1,
                51)],
        string="Body Font-Size(px):",
        required=True,
        default=lambda self: self.env.user.company_id.pbody_font)
    footer_font = fields.Selection(
        [
            (x,
             str(x)) for x in range(
                1,
                51)],
        string="Footer Font-Size(px):",
        required=True,
        default=lambda self: self.env.user.company_id.pfooter_font)
    font_family = fields.Char(
        'Font Family:',
        required=True,
        default=lambda self: self.env.user.company_id.pfont_family)
