# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta


#  hypthose indicateur effet
class HypotheseIndicateurProduit(models.Model):
    _name="hipothese.indicateur.produit"
    _description = "hypothese des indicateur produit"
    _rec_name = "valeur"


    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(HypotheseIndicateurProduit, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'une hipothese indicateur produit"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'une hipothese indicateur produit suivant : {self.valeur}"

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
    ind_prod_id = fields.Many2one("indicateur.produit", " Indicateur produit")