# Model to track votes to prevent multiple votes per user
from odoo import models, fields

class StackItVote(models.Model):
    _name = 'stackit.vote'
    _description = 'StackIt Vote'

    user_id = fields.Many2one('res.users', string='User', required=True)
    question_id = fields.Many2one('stackit.question', string='Question')
    answer_id = fields.Many2one('stackit.answer', string='Answer')
    vote_type = fields.Selection([('up', 'Upvote'), ('down', 'Downvote')], required=True)
    _sql_constraints = [
        ('unique_vote', 'unique(user_id, question_id, answer_id, vote_type)', 'You can only vote once per item per type!')
    ]