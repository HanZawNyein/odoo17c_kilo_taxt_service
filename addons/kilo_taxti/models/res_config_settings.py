from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    start_kilo = fields.Float(config_parameter="start_kilo")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        start_kilo = ICPSudo.get_param('start_kilo')
        res.update(start_kilo=float(start_kilo))
        return res