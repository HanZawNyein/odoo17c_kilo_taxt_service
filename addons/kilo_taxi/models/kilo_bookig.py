from odoo import api, fields, models, _


class KiloBooking(models.Model):
    _name = 'kilo.booking'
    _description = 'KiloBooking'
    _rec_name = "partner_id"

    partner_id = fields.Many2one('res.partner')
    start_kilo = fields.Float(copy=False)
    end_kilo = fields.Float(copy=False)
    total_kilo = fields.Float(copy=False)

    vehicle_id = fields.Many2one('fleet.vehicle', copy=False)
    driver_id = fields.Many2one('res.partner', related="vehicle_id.driver_id", copy=False)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('accept', 'Accept'),
        ('arrived', 'Arrived'),
        ('cancel', 'Cancel'),
    ], default="draft")

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related="company_id.currency_id")
    amount = fields.Monetary(copy=False)  # currency_field="company_currency_id")
    service_fees = fields.Monetary(copy=False)  # currency_field="company_currency_id")
    date = fields.Datetime(default=lambda self: fields.Datetime.now())
    move_id = fields.Many2one('account.move', copy=False)

    @api.onchange('end_kilo')
    def _on_change_end_kilo(self):
        if self.end_kilo:
            self.total_kilo = self.start_kilo + self.end_kilo
            self.amount = self.total_kilo * self.company_id.kilo_per_mmk

    def action_rest_to_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = "confirm"
        ICPSudo = self.env['ir.config_parameter'].sudo()
        start_kilo = ICPSudo.get_param('start_kilo')
        self.start_kilo = start_kilo
        self.service_fees = self.company_id.kilo_service_fees

    def action_accept(self):
        return {
            'name': _('Add Vehicle'),
            'view_mode': 'form',
            # 'domain': [('lost_reason_id', 'in', self.ids)],
            'res_model': 'kilo.add.vehicle.wizard',
            'type': 'ir.actions.act_window',
            "target": "new"
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

    def action_cancel(self):
        self.state = "cancel"

    def _create_invoice(self):
        self.state = "arrived"
        domain = [('product_tmpl_id', '=', self.company_id.kilo_service_product.id)]
        product_id = self.env['product.product'].search(domain=domain, limit=1)
        vals = {
            "partner_id": self.driver_id.id,
            "move_type": "out_invoice",
            "invoice_date": self.date.date(),
            "currency_id": self.currency_id.id,
            "invoice_line_ids": [
                (0, 0, {"product_id": product_id.id, "price_unit": self.service_fees}),
            ]
        }
        self.move_id = self.env['account.move'].create(vals)
        self.move_id.action_post()
        ...
