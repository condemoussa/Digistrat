# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# saisir Effet
class AtmEffet(models.Model):
    _name="atm.effet"
    _description = "Effets"
    _rec_name = "libelle"
    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(AtmEffet, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un effet"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour de l'effet suivant : {self.libelle} "
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    libelle=fields.Char("Nom de l'Effet :")
    axe_id= fields.Many2one("atm.axe", "Axe :")
    total_effet = fields.Integer("Total Effet", compute="_compute_count_effet", store=True)

    @api.depends('libelle')
    def _compute_count_effet(self):
        for record in self:
            count = self.env['atm.effet'].search([])
            record.total_effet = len(count)