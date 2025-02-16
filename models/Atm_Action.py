# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# produit
class AtmAction(models.Model):
    _name = "atm.action"
    _rec_name = "libelle"
    _description = "les actions"

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(AtmAction, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'une action"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour de l'action suivante : {self.libelle} "

                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    libelle=fields.Char("Action :",required=True)
    dat_debut=fields.Char("Période Debut :")
    dat_fin=fields.Char("période  Fin :")
    produit_id=fields.Many2one("atm.produit", string="Produit :")
    partenaire_ids = fields.Many2many("atm.partenaire", string="Partenaire :")
    direction_ids = fields.Many2many("atm.direction", string="Direction :")
    total_action = fields.Integer("Total Action", compute="_compute_count_action", store=True)

    @api.depends('libelle')
    def _compute_count_action(self):
        for record in self:
            count = self.env['atm.action'].search([])
            record.total_action = len(count)