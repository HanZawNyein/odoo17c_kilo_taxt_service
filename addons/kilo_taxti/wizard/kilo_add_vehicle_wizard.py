from odoo import api, fields, models


class KiloAddVehicleWizard(models.TransientModel):
    _name = 'kilo.add.vehicle.wizard'
    _description = 'KiloAddDriverWizard'

    vehicle_id = fields.Many2one('fleet.vehicle')
    driver_id = fields.Many2one('res.partner', related="vehicle_id.driver_id")

    def action_add_vehicle(self):
        context = self.env.context
        active_model = context.get('active_model')
        active_id = context.get('active_id')
        kilo_booking_id = self.env[active_model].browse(active_id)
        kilo_booking_id.vehicle_id = self.vehicle_id
        kilo_booking_id.state = "accept"
