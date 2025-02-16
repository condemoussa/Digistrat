# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# les axes

class AtmTableaubord(models.Model):
    _name="atm.tableaubord"
    _description = "Tableau de bord"
    _rec_name = "axe"

    def clear_existing_data(self):
        existing_records = self.search([])
        existing_records.unlink()

    def insert_data_from_query(self):
        self.clear_existing_data()
        query = """
                       INSERT INTO atm_tableaubord (produit,action,effet,axe,period_real,period_real_fin)
                       SELECT pro.libelle , act.libelle,ef.libelle,ax.libelle ,act.dat_debut, act.dat_fin
                       FROM atm_action act
                       JOIN atm_produit pro ON act.produit_id = pro.id
                       JOIN atm_effet ef ON  pro.effet_id = ef.id
                       JOIN atm_axe ax ON  ef.axe_id = ax.id
                      
                   """
        self.env.cr.execute(query)



    axe=fields.Char("Axe")
    effet = fields.Char("Effet")
    produit = fields.Char("Produit")
    action = fields.Char("Action")
    responsable = fields.Char("Responsable")
    partenaire = fields.Char("Partenaire")
    period_real=fields.Char("Période debut")
    period_real_fin = fields.Char("Période fin")
