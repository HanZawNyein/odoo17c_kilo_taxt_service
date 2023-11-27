from odoo import api, fields, models


class KiloBooking(models.Model):
    _name = 'kilo.booking'
    _description = 'KiloBooking'
    _rec_name = "partner_id"

    partner_id = fields.Many2one('res.partner')
    start_kilo = fields.Float()
    end_kilo = fields.Float()
