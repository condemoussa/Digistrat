# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

#produit
class AtmProduit(models.Model):
    _name="atm.produit"
    _description = "Produit"
    _rec_name = "libelle"

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(AtmProduit, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un produit"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'un produit suivant : {self.libelle}"
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    libelle= fields.Char("Nom du Produit :")
    effet_id = fields.Many2one("atm.effet", "Effets : ")
    total_produit = fields.Integer("Total Produit", compute="_compute_count_produit", store=True)


    @api.depends('libelle')
    def _compute_count_produit(self):
        for record in self:
            count = self.env['atm.produit'].search([])
            record.total_produit =len(count)