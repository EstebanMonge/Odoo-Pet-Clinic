from odoo import models, fields, api, _
from datetime import time


class Service(models.Model):
    _name = 'pet_clinic.service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'service_id'
    _defaults = {
        'date_start': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'date_end': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    service_id = fields.Char(string='ID', required=True, copy=False, readonly=True,
                             index=True, default=lambda self: _('New'))
    date_start = fields.Datetime(
        string='Date Start', required=True)
    date_end = fields.Datetime(
        string='Date End', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_process', 'In Process'),
        ('done', 'done'),
        ('canceled', 'canceled'),
    ], string='Status', default='draft')
    description = fields.Text(string='Description')

    # Item
    service_name = fields.Many2one(
        'pet_clinic.item', string='Service', required=True, domain="[('item_type', '=', 'service')]")

    # Appointment
    appointment = fields.Many2one(
        'pet_clinic.appointment', string='Appointment ID')
    appointment_pet_name = fields.Char(
        related='appointment.pet_name', string='Pet')
    appointment_pet_owner = fields.Char(
        related='appointment.pet_owner', string='Owner')
    appointment_doctor_name = fields.Char(
        related='appointment.doctor_name', string='Doctor')

    @api.model
    def create(self, vals):
        if vals.get('service_id', _('New')) == _('New'):
            vals['service_id'] = self.env['ir.sequence'].next_by_code(
                'pet_service.seq') or _('New')
        result = super(Service, self).create(vals)
        return result

    def action_check(self):
        for rec in self:
            rec.state = 'in_process'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'canceled'
