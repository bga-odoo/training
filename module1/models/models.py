# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class openacademy(models.Model):
    _name = 'openacademy'
    _description = "Models for academies"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    full_description = fields.Text()
    session_ids = fields.One2many('session','academy_id',string="Sessions")
    tag_ids = fields.Many2many('tag', string='Tags', help="Tags for academies")

class course(models.Model):
    _name = 'course'
    _description = "Model for courses"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        (
            'unique_name_for_course', 'UNIQUE (name)',
            'Name of the course must be unique',
        )
    ]

    description = fields.Text(string="description")
    session_ids = fields.One2many('session','course_id',string="Sessions")
    tag_ids = fields.Many2many('tag', string='Tags', help="Tags for courses")
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible")

class session(models.Model):
    _name = 'session'
    _description = "Models for sessions"

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    seats = fields.Integer(string="Number of seats")

    @api.onchange('seats')
    def _onchange_seats(self):
        if self.seats < 0:
            return{
                'warning':{
                    'title' : "Number of seats is negative",
                    'message' : "Number of seats is negative",
                }
            }

    duration = fields.Float(digits=(6, 2), help="Duration in days")
    course_id = fields.Many2one('course', string="Course")
    academy_id = fields.Many2one('openacademy', string="Academy")
    instructor_id = fields.Many2one('res.partner', string="Instructor")

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_attendee(self):
        if self.instructor_id and self.attendee_ids and self.instructor_id in self.attendee_ids:
            raise ValidationError("The instructor is part of the attendees")

    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(string="Taken seats percentage", compute="_taken_seats")

    @api.depends('seats','attendee_ids')
    def _taken_seats(self):
        for record in self:
            if record.seats:
                record['taken_seats'] = 100 * len(record.attendee_ids) / record.seats
            else:
                record['taken_seats'] = 0

    @api.onchange('seats','attendee_ids')
    def _onchange_taken_seats(self):
        if self.seats != 0 and len(self.attendee_ids) / self.seats > 1:
            return {
                'warning': {
                    'title' : "Number of seats exceeded",
                    'message' : "Number of seats exceeded",
                }
            }

    active = fields.Boolean(string="Active", default=True)
    start_date = fields.Date(default=fields.Date.today)
    
class tag(models.Model):
    _name = 'tag'
    _description = "Tags for courses and academies"

    name = fields.Char(sring="Tag")