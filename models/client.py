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
    pet = fields.One2many('pet_klinik.pet', 'owner',
                          string="Hewan Peliharaan")
    phone = fields.Char(string='No Telepon', required=True)
    email = fields.Char(string='Email')
    address = fields.Text(string='Alamat')

    @api.model
    def create(self, vals):
        if vals.get('client_id', _('New')) == _('New'):
            vals['client_id'] = self.env['ir.sequence'].next_by_code(
                'client.seq') or _('New')
        result = super(Client, self).create(vals)
        return result

    @api.onchange('pet')
    def pet_onchange(self):
        return {'domain': {'pet': [('owner', '=', False)]}}
