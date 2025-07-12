# -*- coding: utf-8 -*-
# from odoo import http
from odoo import http
from odoo.http import request


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

# Controller for StackIt Home Page (Question List)
class StackItController(http.Controller):
    @http.route('/stackit', auth='public', website=True)
    def stackit_home(self, page=1, search='', filter='newest', **kw):
        page = int(page) if str(page).isdigit() else 1
        page_size = 10
        domain = []
        order = 'create_date desc'
        if search:
            domain += ['|', ('title', 'ilike', search), ('description', 'ilike', search)]
        if filter == 'unanswered':
            domain += [('answers', '=', False)]
        Question = request.env['stackit.question'].sudo()
        total = Question.search_count(domain)
        page_count = (total + page_size - 1) // page_size
        questions = Question.search(domain, order=order, offset=(page-1)*page_size, limit=page_size)
        return request.render('stackit.stackit_homepage', {
            'questions': questions,
            'page': page,
            'page_count': page_count,
            'search': search,
            'filter': filter,
        })



    @http.route('/stackit/question/<int:question_id>', auth='public', website=True)
    def stackit_question_detail(self, question_id, **kw):
        question = request.env['stackit.question'].sudo().browse(question_id)
        if not question.exists():
            return request.not_found()
        user = request.env.user if request.env.user and request.env.user.id else None
        return request.render('stackit.stackit_question_detail', {
            'question': question,
            'user': user,
        })


    @http.route(['/stackit/question/upvote/<int:question_id>', '/stackit/question/downvote/<int:question_id>'], type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def stackit_question_vote(self, question_id, **kw):
        vote_type = 'up' if 'upvote' in request.httprequest.path else 'down'
        question = request.env['stackit.question'].sudo().browse(question_id)
        user = request.env.user
        if not question.exists() or not user:
            return request.redirect('/web/login')
        vote_obj = request.env['stackit.vote'].sudo()
        existing_vote = vote_obj.search([
            ('user_id', '=', user.id),
            ('question_id', '=', question.id),
            ('answer_id', '=', False),
            ('vote_type', '=', vote_type)
        ])
        if not existing_vote:
            vote_obj.create({
                'user_id': user.id,
                'question_id': question.id,
                'vote_type': vote_type
            })
            if vote_type == 'up':
                question.sudo().up += 1
            else:
                question.sudo().down += 1
        return request.redirect('/stackit/question/%d' % question.id)

    @http.route(['/stackit/answer/upvote/<int:answer_id>', '/stackit/answer/downvote/<int:answer_id>'], type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def stackit_answer_vote(self, answer_id, **kw):
        vote_type = 'up' if 'upvote' in request.httprequest.path else 'down'
        answer = request.env['stackit.answer'].sudo().browse(answer_id)
        user = request.env.user
        if not answer.exists() or not user:
            return request.redirect('/web/login')
        vote_obj = request.env['stackit.vote'].sudo()
        existing_vote = vote_obj.search([
            ('user_id', '=', user.id),
            ('answer_id', '=', answer.id),
            ('question_id', '=', False),
            ('vote_type', '=', vote_type)
        ])
        if not existing_vote:
            vote_obj.create({
                'user_id': user.id,
                'answer_id': answer.id,
                'vote_type': vote_type
            })
            if vote_type == 'up':
                answer.sudo().up += 1
            else:
                answer.sudo().down += 1
        return request.redirect('/stackit/question/%d' % answer.question_id.id)

    @http.route('/stackit/ask', auth='user', website=True, methods=['GET', 'POST'], csrf=False)
    def stackit_ask_question(self, **post):
        if request.httprequest.method == 'POST':
            title = post.get('title')
            description = post.get('description')
            tags = post.get('tags')
            tag_ids = []
            if tags:
                tag_names = [t.strip() for t in tags.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag = request.env['stackit.tag'].sudo().search([('name', '=', tag_name)], limit=1)
                    if not tag:
                        tag = request.env['stackit.tag'].sudo().create({'name': tag_name})
                    tag_ids.append(tag.id)
            question = request.env['stackit.question'].sudo().create({
                'title': title,
                'description': description,
                'tags': [(6, 0, tag_ids)],
                'user_id': request.env.user.id,
            })
            return request.redirect('/stackit/question/%d' % question.id)
        return request.render('stackit.stackit_ask_question', {})



    @http.route('/stackit/question/<int:question_id>/answer', auth='user', website=True, methods=['POST'], csrf=False)
    def stackit_submit_answer(self, question_id, **post):
        answer_text = post.get('answer')
        question = request.env['stackit.question'].sudo().browse(question_id)
        if question.exists() and answer_text:
            request.env['stackit.answer'].sudo().create({
                'question_id': question.id,
                'answer': answer_text,
                'user_id': request.env.user.id,
            })
        return request.redirect('/stackit/question/%d' % question.id)

