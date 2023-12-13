from odoo import api, fields, models


class KiloBooking(models.Model):
    _inherit = 'kilo.booking'

    def action_confirm(self):
        res = super(KiloBooking, self).action_confirm()
        message = self.read(fields=['partner_id', 'date', 'start_kilo'])[0]
        self.env['bus.bus']._sendone('kilo_taxi_services', 'kilo.booking/action_confirm', message)
        return res
