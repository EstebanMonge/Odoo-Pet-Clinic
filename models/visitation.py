from odoo import fields, models, api, _
from datetime import time


class Visitation(models.Model):
    _name = 'pet_clinic.visitation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'visitation_id'
    _defaults = {
        'date_end': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
    }

    # Appointment
    appointment = fields.Many2one(
        'pet_clinic.appointment', string='Appointment ID', required=True)
    appointment_pet_rec_name = fields.Char(
        related='appointment.pet_rec_name', string='Pet')
    appointment_pet_owner = fields.Char(
        related='appointment.pet_owner', string='Owner')
    appointment_doctor_name = fields.Char(
        related='appointment.doctor_name', string='Doctor')

    visitation_id = fields.Char(string='ID', required=True, copy=False, readonly=True,
                                index=True, default=lambda self: _('New'))
    date_start = fields.Datetime(
        string='Date Start', store=True)
    date_end = fields.Datetime(
        string='Date End')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_process', 'In Process'),
        ('done', 'done'),
        ('canceled', 'canceled'),
    ], string='Status', default='draft')
    description = fields.Text(string='Description')

    @api.model
    def create(self, vals):
        if vals.get('visitation_id', _('New')) == _('New'):
            vals['visitation_id'] = self.env['ir.sequence'].next_by_code(
                'pet_visitation.seq') or _('New')
        result = super(Visitation, self).create(vals)
        return result

    def action_check(self):
        for rec in self:
            rec.state = 'in_process'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        for rec in self.appointment:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'canceled'
