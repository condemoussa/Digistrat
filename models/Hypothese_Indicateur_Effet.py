# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

#  hypthose indicateur effet
class HypotheseIndicateurEffet(models.Model):
    _name="hipothese.indicateur.effet"
    _description = "risque des indicateur effet"
    _rec_name = "valeur"

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(HypotheseIndicateurEffet, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'une hipothese indicateur effet"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'une hipothese indicateur effet suivant : {self.valeur}"
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    valeur= fields.Char("Valeur")
    ind_efft_id = fields.Many2one("indicateur.effet", "Indicateur Effet")