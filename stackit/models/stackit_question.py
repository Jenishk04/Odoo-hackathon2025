from odoo import models, fields, api

class Question(models.Model):
    _name = 'stackit.question'

    title = fields.Text(string='Title', required=True)
    tags = fields.Many2many('stackit.tag', string='Tags')
    description = fields.Html(string='Description')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)
    answers = fields.One2many('stackit.answer', 'question_id', string='Answers')
