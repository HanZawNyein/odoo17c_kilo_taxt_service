from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    kilo_per_mmk = fields.Monetary()
    kilo_service_fees = fields.Monetary()


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    start_kilo = fields.Float(config_parameter="start_kilo")
    currency_id = fields.Many2one('res.currency', related="company_id.currency_id")
    kilo_per_mmk = fields.Monetary(related="company_id.kilo_per_mmk", readonly=False)
    kilo_service_fees = fields.Monetary(related="company_id.kilo_service_fees", readonly=False)
    #  100
    # 200

    # def set_values(self):
    #     super(ResConfigSettings,self).set_values()
    #     self.env['ir.config_parameter'].set_param('kilo_per_mmk',self.kilo_per_mmk)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        start_kilo = ICPSudo.get_param('start_kilo')
        res.update(start_kilo=float(start_kilo))
        return res
