# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# indicateur d'impact

class IndicateurImpact(models.Model):
    _name="indicateur.impact"
    _description = "indicateur d'impact"
    _rec_name = "libelle"

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(IndicateurImpact, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un  indicateur impact"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'un indicateur impact suivant : {self.libelle}"
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res


    libelle=fields.Char("Libelle d'indicateur :")
    anne_base=fields.Char("Année de Base :" , size=4)
    valeur_base=fields.Char("Valeur Base :")
    impact_id=fields.Many2one("atm.impact" ,"Impact :")
    direction_id = fields.Many2one("atm.direction", string="Direction :")