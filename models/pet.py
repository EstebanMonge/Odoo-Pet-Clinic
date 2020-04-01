# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Pet(models.Model):
    _name = 'pet_klinik.pet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'rec_name'

    pet_id = fields.Char(string='ID', required=True, copy=False, readonly=True,
                         index=True, default=lambda self: _('New'))
    name = fields.Char(string='nama', required=True)
    gender = fields.Selection([
        ('jantan', 'Jantan'),
        ('betina', 'Betina'),
    ], default='jantan', string="Gender", required=True)
    age = fields.Char(string='Umur', required=True)
    image = fields.Binary(string='Foto')
    type = fields.Many2one('pet_klinik.pet.pet_type',
                           string='Jenis', required=True)
    type_name = fields.Char(related='type.name',
                            string='Jenis')
    breed = fields.Many2one('pet_klinik.pet.breed', domain="[('type','=',type)]",
                            string='Ras', required=True)
    breed_name = fields.Char(related='breed.name',
                             string='Ras')
    owner = fields.Many2one('pet_klinik.client')
    owner_name = fields.Char(related='owner.name',
                             string='Owner')
    owner_name = fields.Char(related='owner.name',
                             string='Owner')
    rec_name = fields.Char(string='Recname',
                           compute='_compute_fields_rec_name')

    @api.depends('name', 'type_name', 'breed_name')
    def _compute_fields_rec_name(self):
        for pet in self:
            pet.rec_name = '{} - {} {}'.format(pet.name,
                                               pet.type_name, pet.breed_name)

    @api.model
    def create(self, vals):
        if vals.get('pet_id', _('New')) == _('New'):
            vals['pet_id'] = self.env['ir.sequence'].next_by_code(
                'pet.seq') or _('New')
        result = super(Pet, self).create(vals)
        return result


class PetType(models.Model):
    _name = 'pet_klinik.pet.pet_type'
    name = fields.Char(string='Nama', required=True)


class PetBreed(models.Model):
    _name = 'pet_klinik.pet.breed'
    name = fields.Char(string='Nama', required=True)
    type = fields.Many2one('pet_klinik.pet.pet_type',
                           string='Jenis', required=True)
