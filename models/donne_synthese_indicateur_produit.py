# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# saisir indicateur produit
class SaisirSynthesIndicateurProduit(models.Model):
    _name="saisir.synthese.indicateur.produit"
    _description = "saisir synthèse des indicateurs produit"
    _rec_name = "cible"

    def unlink(self):
        for line in self:
            res = super().unlink()
        return res

    @api.constrains('ind_prod_id', 'annee','direction_id' )
    def _check_unique_record(self):
        for record in self:
            # Recherche d'autres enregistrements avec les mêmes valeurs pour les champs
            val_anne = self.env['saisir.synthese.indicateur.produit'].search(
                [('annee', '=', record.annee), ('id', '!=', record.id),('direction_id', '=', record.direction_id.id),('ind_prod_id', '=', record.ind_prod_id.id)])
            if val_anne :
                raise ValidationError("il existe deja des données saisies sur cet enregistrement !")

    @api.model
    def _get_default_domain(self):
        current_user_direction = self.env.user.direction_id
        return [('id', '=', current_user_direction.id)]

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(SaisirSynthesIndicateurProduit, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'une saisie de synthèse des indicateurs produit"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'une saisie des indicateurs produit suivante : {self.annee} "
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    annee= fields.Char('Année')
    cible = fields.Char("Cible")
    realise = fields.Char("Réalise")
    comment = fields.Text("Comment")
    ind_prod_id= fields.Many2one("indicateur.produit", " Indicateur produit")
    direction_id=fields.Many2one("atm.direction",string="Direction :")
    status = fields.Selection([
        ('atteint', 'Atteint'),
        ('no_atteint', 'Non atteint'),
    ], string="Statut")
    saisir_ind_produi_id=fields.Many2one("saisir.indicateur.produit")