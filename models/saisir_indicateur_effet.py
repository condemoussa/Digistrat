# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# saisir indicateur effet
class SaisirIndicateurEffet(models.Model):
    _name="saisir.indicateur.effet"
    _description = "saisir des indicateur effet"
    _rec_name = "cible"

    @api.constrains('ind_efft_id', 'annee','direction_id' )
    def _check_unique_record(self):
        for record in self:
            # Recherche d'autres enregistrements avec les mêmes valeurs pour les champs
            val_anne = self.env['saisir.indicateur.effet'].search(
                [('annee', '=', record.annee), ('id', '!=', record.id),('ind_efft_id', '=', record.ind_efft_id.id),('direction_id', '=', record.direction_id.id)])
            # val_direction = self.env['saisir.indicateur.effet'].search(
            #     [('direction_id', '=', record.direction_id.id), ('id', '!=', record.id)])
            # val_effet = self.env['saisir.indicateur.effet'].search(
            #     [('ind_efft_id', '=', record.ind_efft_id.id), ('id', '!=', record.id)])

            # if val_anne and val_direction and val_seffet :
            #     raise ValidationError("il existe deja des données saisies sur cet enregistrement !")
            if val_anne:
                raise ValidationError("il existe deja des données saisies sur cet enregistrement !")

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(SaisirIndicateurEffet, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'une saisie des indicateurs effet"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'une saisie des indicateurs effet suivante : {self.annee} "

                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    # @api.model
    # def _get_default_domain(self):
    #     current_user_direction=self.env.user.direction_id
    #     return [('id','=',current_user_direction.id)]

    annee= fields.Char('Année :')
    cible = fields.Char("Cible :")
    realise = fields.Char("Réalise :")
    comment = fields.Text("Commentaire :")
    ind_efft_id = fields.Many2one("indicateur.effet", "Indicateur Effet :")
    direction_id = fields.Many2one("atm.direction", string="Direction :" ,related="ind_efft_id.direction_id",store=True,
    readonly=True)
    status=fields.Selection([
        ('atteint','Atteint'),
        ('no_atteint', 'Non atteint'),
    ],string="Statut :")
