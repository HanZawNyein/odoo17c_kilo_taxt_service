from odoo import api, fields, models


class KiloBooking(models.Model):
    _name = 'kilo.booking'
    _description = 'KiloBooking'
    _rec_name = "partner_id"

    partner_id = fields.Many2one('res.partner')
    start_kilo = fields.Float()
    end_kilo = fields.Float()
    total_kilo = fields.Float()

    vehicle_id = fields.Many2one('fleet.vehicle')
    driver_id = fields.Many2one('res.partner', related="vehicle_id.driver_id")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm')
    ], default="draft")

    @api.onchange('end_kilo')
    def _on_change_end_kilo(self):
        if self.end_kilo:
            self.total_kilo = self.start_kilo + self.end_kilo

    def action_rest_to_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = "confirm"
        ICPSudo = self.env['ir.config_parameter'].sudo()
        start_kilo = ICPSudo.get_param('start_kilo')
        self.start_kilo = start_kilo