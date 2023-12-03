from odoo import api, fields, models


class KiloArrivedWizard(models.TransientModel):
    _name = 'kilo.arrived.wizard'
    _description = 'KiloArrivedWizard'

    end_kilo = fields.Float()

    def action_add_end_kilo(self):
        context = self.env.context
        active_model = context.get('active_model')
        active_id = context.get('active_id')
        kilo_booking_id = self.env[active_model].browse(active_id)

        kilo_booking_id.end_kilo = self.end_kilo
        kilo_booking_id._on_change_end_kilo()
        kilo_booking_id._create_invoice()
