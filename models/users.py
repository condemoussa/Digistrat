# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta


# utilisateur
class RUsers(models.Model):
    _inherit = "res.users"
    _description = "Utilisateur"

    matricule=fields.Char("Matricule")
    prenom=fields.Char("Prénom")
    dat_naissance=fields.Date("Date de naissance")
    sex=fields.Selection([
        ('m',"M"),
        ('f',"F")
    ],default='m' ,string="Sexe")
    grade=fields.Char("Grade")
    direction_id = fields.Many2one("atm.direction","Direction :")
    profil = fields.Selection([
        ('admin_digistrat', "Admin Digistrat"),
        ('auditeur', "Auditeur Digistrat"),
        ('agent_deesp', "Equipe projet Digistrat"),
        ('contributeur', "Contributeur Digistrat")
    ], string="Profil")








