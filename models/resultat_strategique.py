# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# les resultat Strategique

class ResultatStrategique(models.Model):
    _name="resultat.strategique"
    _description = "Les Resultat Strategique"
    _rec_name = "libelle"


    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(ResultatStrategique, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un Resultat Strategique"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour du Resultat Strategique suivante : {self.libelle} "


                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res


    libelle=fields.Char("Libellé du resultat :")
    axe_id=fields.Many2one("atm.axe" ,"Axe :")