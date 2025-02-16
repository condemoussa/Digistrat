# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# saisir indicateur
class SaisirIndicateurResultatStrategique(models.Model):
    _name="saisir.indicateur.resultat.strategique"
    _description = "saisir des indicateur resultat strategique"
    _rec_name = "cible"

    @api.constrains('ind_inp_id', 'annee', )
    def _check_unique_record(self):
        for record in self:
            # Recherche d'autres enregistrements avec les mêmes valeurs pour les champs
            val_indicateur = self.env['saisir.indicateur.resultat.strategique'].search(
                [('annee', '=', record.annee), ('id', '!=', record.id),('ind_result_id', '=', record.ind_result_id.id)])
            # val_annee = self.env['saisir.indicateur.impact'].search(
            #     [('annee', '=', record.annee), ('id', '!=', record.id)])

            if val_indicateur:
                raise ValidationError("il existe deja des données saisies sur cet enregistrement !")

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(SaisirIndicateurResultatStrategique, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'une saisie des indicateurs resultat strategique"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'une saisie des indicateurs resultat strategique suivante : {self.annee} "
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    annee= fields.Char('Année :')
    cible = fields.Char("Cible :")
    realise = fields.Char("Réalise :")
    comment = fields.Text("Comment :")
    status = fields.Selection([
        ('atteint', 'Atteint'),
        ('no_atteint', 'Non atteint'),
    ], string="Statut :")
    ind_result_id= fields.Many2one("indicateur.resultat.strategique", "Indicateur Resultat Strategique :")
    direction_id = fields.Many2one("atm.direction", string="Direction :",related="ind_result_id.direction_id",store=True,
    readonly=True,)