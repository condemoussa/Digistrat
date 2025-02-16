# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# indicateur produit
class IndicateurProduit(models.Model):
    _name="indicateur.produit"
    _description = "indicateur produit"
    _rec_name = "libelle"

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(IndicateurProduit, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un  indicateur produit"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'un indicateur produit suivant : {self.libelle}"
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    #@api.constrains('anne_base', )
    # def _check_unique_record(self):
    #     for record in self:
    #         # Recherche d'autres enregistrements avec les mêmes valeurs pour les champs
    #         val_indicateur = self.env['indicateur.produit'].search(
    #             [('anne_base', '=', record.anne_base), ('id', '!=', record.id)])
    #         # val_annee = self.env['saisir.indicateur.impact'].search(
    #         #     [('annee', '=', record.annee), ('id', '!=', record.id)])
    #
    #         if val_indicateur:
    #             raise ValidationError("il existe deja des données saisies sur cet enregistrement !")

    libelle = fields.Char("Nom de l'indicateur :" , required=True)
    anne_base = fields.Char("Année de Base :" ,size=4)
    valeur_base = fields.Char("Valeur Base :")
    produit_id = fields.Many2one("atm.produit", "Produit :")
    partenaire_ids = fields.Many2many("atm.partenaire", string="Partenaire :")
    direction_ids = fields.Many2many("atm.direction", string="Direction :")
    risque_ids = fields.One2many("risque.indicateur.produit", "ind_prod_id", "Risque :")
    hypothese_ids = fields.One2many("hipothese.indicateur.produit", "ind_prod_id", "Hypothèse :")