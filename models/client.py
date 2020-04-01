# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Client(models.Model):
    _name = 'pet_klinik.client'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    client_id = fields.Char(string='ID', required=True, copy=False, readonly=True,
                            index=True, default=lambda self: _('New'))
    name = fields.Char(string="Nama", required=True)
    gender = fields.Selection([
        ('laki-laki', 'Laki-laki'),
        ('perempuan', 'Perempuan'),
    ], default='laki-laki', string="Gender", required=True)
    age = fields.Integer(string='Umur', required=True)
    image = fields.Binary(string='Foto', attachment=True)
    phone = fields.Char(string='No Telepon', required=True)
    email = fields.Char(string='Email')
    address = fields.Text(string='Alamat')

    pet = fields.One2many('pet_klinik.pet', 'owner',
                          string="Hewan Peliharaan")
    pet_count = fields.Integer(compute='compute_pet_count')

    appointment = fields.Many2many('pet_klinik.appointment', 'client',
                                   string="Appointment")
    appointment_count = fields.Integer(compute='compute_appointment_count')

    @api.model
    def create(self, vals):
        if vals.get('client_id', _('New')) == _('New'):
            vals['client_id'] = self.env['ir.sequence'].next_by_code(
                'client.seq') or _('New')
        result = super(Client, self).create(vals)
        return result

    # Button Pet Handle
    @api.multi
    def open_client_pet(self):
        return {
            'name': _('Pets'),
            'domain': [('owner', '=', self.id)],
            'view_type': 'form',
            'res_model': 'pet_klinik.pet',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
    # Button Pet Count

    def compute_pet_count(self):
        for record in self:
            record.pet_count = self.env['pet_klinik.pet'].search_count(
                [('owner', '=', self.id)])

    # Button Appointment Handle
    @api.multi
    def open_client_appointment(self):
        return {
            'name': _('Appointments'),
            'domain': [('client', '=', self.id)],
            'view_type': 'form',
            'res_model': 'pet_klinik.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    # Button Appointment Count

    def compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['pet_klinik.appointment'].search_count(
                [('client', '=', self.id)])
