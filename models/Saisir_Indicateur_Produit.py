# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# saisir indicateur produit
class SaisirIndicateurProduit(models.Model):
    _name="saisir.indicateur.produit"
    _description = "saisir des indicateur produit"
    _rec_name = "cible"

    @api.model
    def create(self, vals):
        user = self.env.user
        group_users = user.has_group('Digistrat.group_agent_deesp')

        if group_users != True:
            raise models.UserError("Désolé, vous ne pouvez pas créer de saisir d'indicateur produit. Veuillez voir l'administrateur !")

        res = super(SaisirIndicateurProduit, self).create(vals)
        if res:
            record = self.env["saisir.synthese.indicateur.produit"].create({
                "annee": res['annee'],
                "cible": res['cible'],
                "realise": res['realise'],
                "comment": res['comment'],
                "ind_prod_id": res.ind_prod_id.id,
                "direction_id": res.direction_id.id,
                "status": res['status'],
                "saisir_ind_produi_id": res.id
            })
        return res

    def unlink(self):
        for line in self.filtered('id'):
            data_saisir = self.env["saisir.synthese.indicateur.produit"].search([('saisir_ind_produi_id','=',line.id)])
            data_saisir.unlink()
        super(SaisirIndicateurProduit, self).unlink()
        return True

    @api.constrains('ind_prod_id', 'annee','direction_id' )
    def _check_unique_record(self):
        for record in self:
            # Recherche d'autres enregistrements avec les mêmes valeurs pour les champs
            val_anne = self.env['saisir.indicateur.produit'].search(
                [('annee', '=', record.annee), ('id', '!=', record.id),('direction_id', '=', record.direction_id.id),('ind_prod_id', '=', record.ind_prod_id.id)])
            # val_direction = self.env['saisir.indicateur.produit'].search(
            #     [('direction_id', '=', record.direction_id.id), ('id', '!=', record.id)])
            # val_effet = self.env['saisir.indicateur.produit'].search(
            #     [('ind_prod_id', '=', record.ind_prod_id.id), ('id', '!=', record.id)])

            if val_anne :
                raise ValidationError("il existe deja des données saisies sur cet enregistrement !")

    @api.model
    def _get_default_domain(self):
        current_user_direction = self.env.user.direction_id
        return [('id', '=', current_user_direction.id)]

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(SaisirIndicateurProduit, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'une saisie des indicateurs produit"
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

    annee= fields.Char('Année :')
    cible = fields.Char("Cible :")
    realise = fields.Char("Réalise :")
    comment = fields.Text("Comment :")
    ind_prod_id= fields.Many2one("indicateur.produit", " Indicateur produit :")
    direction_id=fields.Many2one("atm.direction",string="Direction :")
    status = fields.Selection([
        ('atteint', 'Atteint'),
        ('no_atteint', 'Non atteint'),
    ], string="Statut :")