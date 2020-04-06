from odoo import fields, models, api, _
from datetime import time


class Visitation(models.Model):
    _name = 'pet_clinic.visitation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'visitation_id'
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
    }

    visitation_id = fields.Char(string='ID', required=True, copy=False, readonly=True,
                                index=True, default=lambda self: _('New'))
    date = fields.Datetime(string='Date Start', required=True)
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

    def action_cancel(self):
        for rec in self:
            rec.state = 'canceled'
