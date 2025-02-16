# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime, timedelta
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

# profil
class AtmProfil(models.Model):
    _name = "atm.profil"
    _description = "Profil"

    libelle=fields.Char("Libelle")