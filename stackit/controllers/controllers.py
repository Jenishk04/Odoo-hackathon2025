# -*- coding: utf-8 -*-
# from odoo import http


# class Stackit(http.Controller):
#     @http.route('/stackit/stackit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stackit/stackit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stackit.listing', {
#             'root': '/stackit/stackit',
#             'objects': http.request.env['stackit.stackit'].search([]),
#         })

#     @http.route('/stackit/stackit/objects/<model("stackit.stackit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stackit.object', {
#             'object': obj
#         })

