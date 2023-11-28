from odoo import api, fields, models, _


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
        ('confirm', 'Confirm'),
        ('accept', 'Accept'),
        ('arrived', 'Arrived')
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

    def action_accept(self):
        return {
            'name': _('Add Vehicle'),
            'view_mode': 'form',
            # 'domain': [('lost_reason_id', 'in', self.ids)],
            'res_model': 'kilo.add.vehicle.wizard',
            'type': 'ir.actions.act_window',
            "target":"new"
            # 'context': {'create': False, 'active_test': False},
        }

    def action_arrived(self):
        return {
            'name': _('Add End Kilo'),
            'view_mode': 'form',
            'res_model': 'kilo.arrived.wizard',
            'type': 'ir.actions.act_window',
            "target": "new"
        }
