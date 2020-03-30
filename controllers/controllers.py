# -*- coding: utf-8 -*-
from odoo import http

# class PetKlinik(http.Controller):
#     @http.route('/pet_klinik/pet_klinik/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pet_klinik/pet_klinik/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pet_klinik.listing', {
#             'root': '/pet_klinik/pet_klinik',
#             'objects': http.request.env['pet_klinik.pet_klinik'].search([]),
#         })

#     @http.route('/pet_klinik/pet_klinik/objects/<model("pet_klinik.pet_klinik"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pet_klinik.object', {
#             'object': obj
#         })