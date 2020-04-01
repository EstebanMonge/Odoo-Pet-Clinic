# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Doctor(models.Model):
    _name = 'pet_klinik.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'rec_name'

    doctor_id = fields.Char(string='ID', required=True, copy=False, readonly=True,
                            index=True, default=lambda self: _('New'))
    name = fields.Char(string='Nama', required=True)
    gender = fields.Selection([
        ('laki-laki', 'Laki-laki'),
        ('perempuan', 'Perempuan'),
    ], default='laki-laki', string="Gender", required=True)
    age = fields.Integer(string='Umur', required=True)
    image = fields.Binary(string='Foto')
    phone = fields.Char(string='No Telepon', required=True)
    email = fields.Char(string='Email')
    address = fields.Text(string='Alamat')
    speciality = fields.Many2one(
        'pet_klinik.doctor.speciality', string='Spesialis',  required=True)
    speciality_name = fields.Char(related='speciality.name',
                                  string='Spesialis')
    rec_name = fields.Char(string='Recname',
                           compute='_compute_fields_rec_name')

    @api.depends('name', 'speciality_name')
    def _compute_fields_rec_name(self):
        for doctor in self:
            doctor.rec_name = '{} spesialis {}'.format(doctor.name,
                                                       doctor.speciality_name)

    @api.model
    def create(self, vals):
        if vals.get('doctor_id', _('New')) == _('New'):
            vals['doctor_id'] = self.env['ir.sequence'].next_by_code(
                'doctor.seq') or _('New')
        result = super(Doctor, self).create(vals)
        return result


class DoctorSpeciality(models.Model):
    _name = 'pet_klinik.doctor.speciality'

    name = fields.Char(string='Nama', required=True)
