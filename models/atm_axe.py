# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# les axes

class AtmAxe(models.Model):
    _name="atm.axe"
    _description = "Les Axes"
    _rec_name = "libelle"

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res=super(AtmAxe, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un axe"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour de l'axe suivant : {self.libelle}"
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()


        return res




    libelle=fields.Char("Nom de l'axe :")
    pla_strat_id=fields.Many2one("plan.strategique" ,"Plan Strategique :",required=True)
    total_axe=fields.Integer("Total Axe",compute="_compute_count_axe" ,store=True)




    @api.depends('libelle')
    def _compute_count_axe(self):
        for record in self:
            count = self.env['atm.axe'].search([])
            record.total_axe =len(count)











   





