# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Appointment(models.Model):
    _name = 'pet_klinik.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'appointment_id'

    appointment_id = fields.Char(string='ID', required=True, copy=False, readonly=True,
                                 index=True, default=lambda self: _('New'))
    pet = fields.Many2one('pet_klinik.pet', string='Binatang Peliharan')

    @api.model
    def create(self, vals):
        if vals.get('appointment_id', _('New')) == _('New'):
            vals['appointment_id'] = self.env['ir.sequence'].next_by_code(
                'pet_appointment.seq') or _('New')
        result = super(Appointment, self).create(vals)
        return result
