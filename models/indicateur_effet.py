# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# saisir Effet
class IndicateurEffet(models.Model):
    _name="indicateur.effet"
    _description = "indicateur effet"
    _rec_name = "libelle"

    def write(self, vals):
        user_admin = self.env["res.users"].search([("profil", "=", "admin_digistrat")])
        res = super(IndicateurEffet, self).write(vals)
        if res:
            for line in user_admin:
                subject = "DIGISTRAT : Modification d'un  indicateur effet"
                body = f"Bonjour {line.name},\n\n l'utilisateur {self.env.user.name} a effectué une mise à jour d'un indicateur effet suivant : {self.libelle}"
                self.env['mail.mail'].create({
                    'subject': subject,
                    'body_html': body,
                    'email_from': 'mconde@iwc-ci.com',
                    'email_to': line.login,
                    #'email_cc': 'condemoussa05@gmail.com',
                    'state': 'outgoing'
                }).send()

        return res

    #code=fields.Char("Code")
    libelle=fields.Char("Nom de l'indicateur :" , required=True)
    an_base=fields.Char("Année de base :")
    val_base=fields.Char("Valeur de base :")
    effet_id= fields.Many2one("atm.effet", "Effet :")
    partenaire_ids = fields.Many2many("atm.partenaire",string="Partenaire :")
    direction_id = fields.Many2one("atm.direction", string="Direction :")
    risque_ids=fields.One2many("risque.indicateur.effet","ind_efft_id" ,"Risque")
    hypothese_ids = fields.One2many("hipothese.indicateur.effet", "ind_efft_id", "Hypothèse")