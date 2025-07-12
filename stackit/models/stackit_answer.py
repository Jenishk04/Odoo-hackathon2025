from odoo import models, fields, api

class Answer(models.Model):
    _name = 'stackit.answer'

    question_id = fields.Many2one('stackit.question', string='Question', required=True, ondelete='cascade')
    answer = fields.Text(string='Answer', required=True)
    up = fields.Integer(string='Upvotes', default=0)
    down = fields.Integer(string='Downvotes', default=0)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)

    def action_upvote(self):
        self.ensure_one()
        self.up += 1
        self.message_post(body=f"Upvoted by {self.env.user.name}")

    def action_downvote(self):
        self.ensure_one()
        self.down += 1
        self.message_post(body=f"Downvoted by {self.env.user.name}")