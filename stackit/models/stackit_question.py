from odoo import models, fields, api

class Question(models.Model):
    _name = 'stackit.question'

    question = fields.Text(string='Question', required=True)
    tags = fields.Many2many('stackit.tag', string='Tags')
    up = fields.Integer(string='Upvotes', default=0)
    down = fields.Integer(string='Downvotes', default=0)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)
    answers = fields.One2many('stackit.answer', 'question_id', string='Answers')

    def action_upvote(self):
        self.ensure_one()
        self.up += 1
        self.message_post(body=f"Upvoted by {self.env.user.name}")

    def action_downvote(self):
        self.ensure_one()
        self.down += 1
        self.message_post(body=f"Downvoted by {self.env.user.name}")