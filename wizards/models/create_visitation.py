# -*- coding: utf-8 -*-

from odoo import models, fields


class CreateVisitation(models.TransientModel):
    _name = 'create.visitation'
    _description = 'Create visitation Wizard'

    appointment = fields.Many2one(
        'pet_clinic.appointment', string="Appointment", required=True)
    appointment_date = fields.Datetime(
        related='appointment.date', string='Date')
    _defaults = {
        'date': appointment_date
    }
    doctor = fields.Many2one(
        'pet_clinic.doctor', required=True)
    date = fields.Datetime(string='Date', required=True)

    def action_confirm(self):
        for rec in self.appointment:
            rec.state = 'confirmed'

    def create_visitation(self):
        vals = {
            'appointment': self.appointment.id,
            'date': self.date,
            'doctor': self.doctor
        }
        self.action_confirm()
        self.appointment.message_post(
            body="new visitation Created", subject="visitation Creation")
        # creating visitations from the code
        new_visitation = self.env['pet_clinic.visitation'].create(vals)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'pet_clinic.visitation',
                'res_id': new_visitation.id,
                'context': context
                }
