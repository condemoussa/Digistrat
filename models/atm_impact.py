# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

#les impact

class AtmImpact(models.Model):
    _name="atm.impact"
    _description = "Les Impacts"
    _rec_name = "libelle"


    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(AtmImpact, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un impact"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour de l'impact suivant : {self.libelle} "
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res


    libelle=fields.Char("Libellé de l'impact :")
    # axe_id=fields.Many2one("atm.axe" ,"Axe :")
    plan_strategique_id = fields.Many2one("plan.strategique", "Plan strategique :")
