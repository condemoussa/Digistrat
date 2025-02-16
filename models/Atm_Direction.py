# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# direction
class AtmDirection(models.Model):
    _name = "atm.direction"
    _rec_name = "nom"
    _description = "Direction"

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(AtmDirection, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'une direction"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour sur la direction suivante : {self.nom} "

                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    @api.constrains('code')
    def _check_unique_record(self):
        for record in self:
            # Recherche d'autres enregistrements avec les mêmes valeurs pour les champs
            val_code = self.env['atm.direction'].search(
                [('code', '=', record.code), ('id', '!=', record.id)])

            if val_code:
                raise ValidationError("Ce code existe déjà !")


    code=fields.Char("Code :")
    nom=fields.Char("Nom :" , required=True)
    # user_id=fields.Many2one("res.users","Utilisateur")
    # indicateur_effet_ids = fields.Many2many("indicateur.effet", "direction_effet_rel", "direction_id",
    #                                   "effet_id", "Indicateur Effet")
    # indicateur_produit_ids = fields.Many2many("indicateur.produit", "direction_produit_rel", "direction_id",
    #                                  "produit_id", "Indicateur Produit")
    # action_ids = fields.Many2many("atm.action", "direction_action_rel", "direction_id",
    #                                           "action_id", "Action")
    # users_ids = fields.Many2many("res.users", "direction_users_rel", "direction_id",
    #                               "user_id", "Utilisateur")