# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta
# saisir indicateur impact
class SaisirIndicateurImpact(models.Model):
    _name="saisir.indicateur.impact"
    _description = "saisir des indicateur impact"
    _rec_name = "cible"

    @api.constrains('ind_inp_id', 'annee',)
    def _check_unique_record(self):
        for record in self:
            # Recherche d'autres enregistrements avec les mêmes valeurs pour les champs

            val_indicateur = self.env['saisir.indicateur.impact'].search(
                [('annee', '=', record.annee), ('id', '!=', record.id),('ind_inp_id', '=', record.ind_inp_id.id)])
            # val_annee = self.env['saisir.indicateur.impact'].search(
            #     [('annee', '=', record.annee), ('id', '!=', record.id)])


            if val_indicateur :
                raise ValidationError("il existe deja des données saisies sur cet enregistrement !")


    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        test=vals["realise"]
        res = super(SaisirIndicateurImpact, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'une saisie des indicateurs impact"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'une saisie des indicateurs impact suivante : {self.annee} "
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res


    annee= fields.Char('Année :' ,size=4)
    cible = fields.Char("Cible :")
    realise = fields.Char("Réalise :")
    comment = fields.Text("Commentaire :")
    ind_inp_id = fields.Many2one("indicateur.impact", "Indicateur impact :")
    status = fields.Selection([
        ('atteint', 'Atteint'),
        ('no_atteint', 'Non atteint'),
    ], string="Statut :")
    direction_id = fields.Many2one("atm.direction", string="Direction :" ,related="ind_inp_id.direction_id" ,store=True,
    readonly=True)