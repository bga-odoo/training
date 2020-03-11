# -*- coding: utf-8 -*-

from odoo import models, fields, api

class openacademy(models.Model):
    _name = 'openacademy'
    _description = "Models for academies"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    full_description = fields.Text()

class course(models.Model):
    _name = 'course'
    _description = "Model for courses"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="description")

class session(models.Model):
    _name = 'session'
    _description = "Models for sessions"

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")