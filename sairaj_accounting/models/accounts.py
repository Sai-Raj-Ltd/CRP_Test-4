# -*- coding: utf-8 -*-

from odoo import models, fields, api



class AccountInvoice(models.Model):
	_inherit = "account.invoice"
















class accountpayments(models.Model):
	_inherit = 'account.payment'


	online_payment_method = fields.Selection([('mpesa','M-Pesa'),('visa_card','Visa Card')],string="Online Payment Method")
	payment_refernce = fields.Char(string = "Payment Reference")
	

