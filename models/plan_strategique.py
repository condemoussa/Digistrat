# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

class PlanStrategique(models.Model):
    _name="plan.strategique"
    _description = "Plan strategique"
    _rec_name = "libelle"


    @api.constrains("dat_debut","dat_fin")
    def _check_date_range(self):
        for line in self:
            if line.dat_debut and line.dat_fin:
                if line.dat_debut > line.dat_fin:
                    raise models.ValidationError("la date de début ne peut pas etre postérieure a la date de fin")

    def demarrer(self):
        self.write({'state': 'encour'})

    def cloture(self):
        self.write({'state': 'cloture'})

    def remettre_initialisation(self):
        self.write({'state': 'brouillon'})

    def annuler(self):
        self.write({'state': 'cancel'})


    libelle=fields.Char("Nom du Plan :")
    periode=fields.Char("Période :")
    dat_debut=fields.Date("Date de debut :")
    dat_fin=fields.Date("Date de fin :")
    state = fields.Selection([
        ('brouillon', "Initialisé"),
        ('encour', "en cours"),
        ('cloture', "cloturé"),
        ('cancel', "Annuler")
    ], default="brouillon", string="brouillon :")
    pdf_files = fields.One2many('atm.pdf', 'plan_strategique_id', string='PDF Files :')

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        user=self.env.user
        for line in self :
            if line.state == "cloture" and  user.profil != "admin_digistrat" and user.profil !="agent_deesp" :
                raise models.UserError("Desolé vous ne pouvez plus modifier cet enregistrement.")
        res=super(PlanStrategique, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un plan strategique"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'un plan strategique suivant : {self.libelle} "
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()
        return res



