# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta
# partenaire
class AtmPartenaire(models.Model):
    _name = "atm.partenaire"
    _rec_name = "nom"
    _description = "Partenaire"
    _rec_name="nom"

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(AtmPartenaire, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un partenaire"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour du partenaire suivant : {self.nom}"
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    code=fields.Char("Code :")
    nom=fields.Char("Nom :")
    # indicateur_produit_ids=fields.Many2many("indicateur.produit","partenaire_produit_rel","partenaire_id","produit_id","Indicateur Produit")
    # indicateur_effet_ids = fields.Many2many("indicateur.effet", "partenaire_effet_rel", "partenaire_id",
    #                                           "effet_id", "Indicateur Effet")
    # atm_action_ids = fields.Many2many("atm.action", "partenaire_action_rel", "partenaire_id",
    #                                           "action_id", "Action")