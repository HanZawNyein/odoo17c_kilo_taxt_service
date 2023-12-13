from odoo import api, fields, models


class KiloAddVehicleWizard(models.TransientModel):
    _inherit = 'kilo.add.vehicle.wizard'

    def action_add_vehicle(self):
        res = super(KiloAddVehicleWizard, self).action_add_vehicle()

        context = self.env.context
        active_model = context.get('active_model')
        active_id = context.get('active_id')
        kilo_booking_id = self.env[active_model].browse(active_id)
        message = kilo_booking_id.read(fields=['partner_id', 'date', 'start_kilo'])[0]
        self.env['bus.bus']._sendone('kilo_taxi_services', 'kilo.booking/accept', message)

        return res
