from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	module_mrp_wo_checklist = fields.Boolean("Mandatory Checklist")

	@api.model
	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		res.update(
			module_mrp_wo_checklist=self.env['ir.config_parameter'].sudo().get_param('module_mrp_wo_checklist')
		)
		return res

	@api.multi
	def set_values(self):
		super(ResConfigSettings, self).set_values()
		self.env['ir.config_parameter'].sudo().set_param('module_mrp_wo_checklist', self.module_mrp_wo_checklist)

	@api.multi
	@api.onchange('module_mrp_wo_checklist')
	def check_module_mrp_wo_checklist(self):

		if self.module_mrp_wo_checklist == True:
			self._cr.execute("""
				UPDATE mrp_workorder
				SET test_field = (SELECT module_mrp_wo_checklist 
				FROM res_config_settings WHERE id = (SELECT max(id)
				FROM res_config_settings WHERE module_mrp_wo_checklist is not null))
			""")

		elif self.module_mrp_wo_checklist == False:
			self._cr.execute("""
				UPDATE mrp_workorder
				SET test_field = (SELECT module_mrp_wo_checklist 
				FROM res_config_settings WHERE id = (SELECT max(id)
				FROM res_config_settings WHERE module_mrp_wo_checklist is not null))
			""")

		else:
			self._cr.execute("""
				UPDATE mrp_workorder
				SET test_field = (SELECT module_mrp_wo_checklist 
				FROM res_config_settings WHERE id = (SELECT max(id)
				FROM res_config_settings WHERE module_mrp_wo_checklist is not null))
			""")