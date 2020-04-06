# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import time


class Appointment(models.Model):
    _name = 'pet_clinic.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'appointment_id'
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    appointment_id = fields.Char(string='ID', required=True, copy=False, readonly=True,
                                 index=True, default=lambda self: _('New'))
    date = fields.Datetime(
        string='Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_process', 'In Process'),
        ('done', 'done'),
        ('canceled', 'canceled'),
    ], string='Status', default='draft')
    description = fields.Text(string='Description')

    # Pet
    pet = fields.Many2one(
        'pet_clinic.pet', required=True)
    pet_rec_name = fields.Char(related='pet.rec_name', string='Pet Recname')
    pet_id = fields.Char(related='pet.pet_id', string='Pet')
    pet_name = fields.Char(related='pet.name', string='Pet')
    pet_owner_id = fields.Integer(
        related='pet.owner_id')
    pet_owner = fields.Char(related='pet.owner_name', string='Owner')

    # Doctor
    doctor = fields.Many2one(
        'pet_clinic.doctor', required=True)
    doctor_name = fields.Char(related='doctor.name', string='Doctor')

    appointment_sequence = fields.Many2one(
        'pet_clinic.appointment.sequence')
    apid = fields.Integer(related='appointment_sequence.id')

    @api.model
    def create(self, vals):
        if vals.get('appointment_id', _('New')) == _('New'):
            vals['appointment_id'] = self.env['ir.sequence'].next_by_code(
                'pet_appointment.seq') or _('New')
        result = super(Appointment, self).create(vals)
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


class AppointmenSequence(models.Model):
    _name = 'pet_clinic.appointment.sequence'

    appointment_date = fields.Datetime()
    number = fields.Integer(default=1, store=True)
