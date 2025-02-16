# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta


class AtmPdf(models.Model):
    _name = 'atm.pdf'
    _rec_name = "name"

    name = fields.Char(string='Name')
    pdf_file = fields.Binary(string='Fichier Pdf ')
    plan_strategique_id = fields.Many2one('plan.strategique', string='Plan strategique')