# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime


class Appointment(models.Model):
    _name = 'pet_klinik.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'appointment_id'

    appointment_id = fields.Char(string='ID', required=True, copy=False, readonly=True,
                                 index=True, default=lambda self: _('New'))
    pet = fields.Many2one(
        'pet_klinik.pet', string='Binatang Peliharan', required=True)
    pet_id = fields.Char(related='pet.pet_id', string='ID Binatang Peliharaan')
    pet_owner = fields.Char(related='pet.owner_name', string='Owner')
    date_start = fields.Datetime(
        string='Tanggal Mulai', required=True, default=datetime.now())
    date_end = fields.Datetime(string='Tanggal Berakhir')
    doctor = fields.Many2one(
        'pet_klinik.doctor', string='Dokter', required=True)
    doctor_name = fields.Char(related='doctor.name', string='Dokter')
    state = fields.Selection([
        ('rancangan', 'Rancangan'),
        ('sedang_diperiksa', 'Sedang Diperiksa'),
        ('selesai', 'Selesai'),
        ('dibatalkan', 'Dibatalkan'),
    ], string='Status', default='rancangan')

    @api.model
    def create(self, vals):
        if vals.get('appointment_id', _('New')) == _('New'):
            vals['appointment_id'] = self.env['ir.sequence'].next_by_code(
                'pet_appointment.seq') or _('New')
        result = super(Appointment, self).create(vals)
        return result

    def action_check(self):
        for rec in self:
            rec.state = 'sedang_diperiksa'

    def action_done(self):
        for rec in self:
            rec.state = 'selesai'

    def action_cancel(self):
        for rec in self:
            rec.state = 'dibatalkan'
