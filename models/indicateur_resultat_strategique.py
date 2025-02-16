# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# indicateur de resultat strategique

class IndicateurResultatStrategique(models.Model):
    _name="indicateur.resultat.strategique"
    _description = "indicateur resultat strategique"
    _rec_name = "libelle"

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(IndicateurResultatStrategique, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un indicateur resultat strategique"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'un indicateur resultat strategique suivant : {self.libelle}"
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res


    libelle = fields.Char("Libelle :")
    anne_base = fields.Char("Année de Base :" ,size=4)
    valeur_base = fields.Char("Valeur Base :")
    impact_id = fields.Many2one("resultat.strategique", "Résultat stratégique :")
    direction_id = fields.Many2one("atm.direction", string="Direction :")