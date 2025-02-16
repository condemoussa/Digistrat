# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# saisir action
class SaisirAction(models.Model):
    _name="saisir.action"
    _description = "saisir des action"
    _rec_name = "action_id"

    @api.model
    def create(self, vals):
        res = super(SaisirAction, self).create(vals)
        if res:
            record = self.env["saisir.synthese.action"].create({
                "annee": res['annee'],
                "comment": res['comment'],
                "state": res['state'],
                "action_id": res.action_id.id,
                "direction_id": res.direction_id.id,
                "saisir_action_id": res.id
            })
        return res

    def unlink(self):
        for line in self.filtered('id'):

            data_saisir_action = self.env["saisir.synthese.action"].search(
                [('saisir_action_id', '=', line.id)])
            data_saisir_action.unlink()

        super(SaisirAction, self).unlink()
        return True

    def demarrer(self):
        self.write({'state': 'encour'})

    def realiser(self):
        self.write({'state': 'realiser'})
    def non_realiser(self):
        self.write({'state': 'no_realiser'})

    def remettre_initialisation(self):
        self.write({'state': 'brouillon'})

    def annuler(self):
        self.write({'state': 'cancel'})


    @api.constrains('action_id', 'annee','direction_id' )
    def _check_unique_record(self):
        for record in self:
            # Recherche d'autres enregistrements avec les mêmes valeurs pour les champs
            val_anne = self.env['saisir.action'].search(
                [('annee', '=', record.annee), ('id', '!=', record.id),('direction_id', '=', record.direction_id.id),('action_id', '=', record.action_id.id)])
            # val_direction = self.env['saisir.action'].search(
            #     [('direction_id', '=', record.direction_id.id), ('id', '!=', record.id)])
            # val_effet = self.env['saisir.action'].search(
            #     [('action_id', '=', record.action_id.id), ('id', '!=', record.id)])

            if val_anne :
                raise ValidationError("il existe deja des données saisies sur cet enregistrement !")

    # @api.model
    # def _get_default_domain(self):
    #     current_user_direction = self.env.user.direction_id
    #     return [('id', '=', current_user_direction.id)]

    annee= fields.Char('Année')
    comment = fields.Text("Commentaire")
    state = fields.Selection([
        ('brouillon', "Initialisé"),
        ('encours', "En cours"),
        ('realiser', "Réalisé"),
        ('no_realiser', " Non réalisé"),
        ('cancel', "Annuler")
    ], default="brouillon", string="brouillon")
    action_id = fields.Many2one("atm.action", "Action" ,required=True)
    direction_id = fields.Many2one("atm.direction", string="Direction")
    # domain = _get_default_domain

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        user = self.env.user
        for line in self:
            if line.state == "realiser" and user.profil != "admin_digistrat" and user.profil != "agent_deesp":
                raise models.UserError("Desolé vous ne pouvez plus modifier cet enregistrement Merci !!!.")
        res= super(SaisirAction, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'une saisie d'action"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'une saisie d'action suivante : {self.annee} "
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()
        return res