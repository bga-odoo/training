# -*- coding: utf-8 -*-

from odoo import models, fields, api

class openacademy(models.Model):
    name = 'openacademy'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()