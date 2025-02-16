# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'DIGISTRAT',
    'version': '1.0',
    'category': 'P',
    'description': """
This adds uselfull methods for payslips structures 
==================================================================
    """,
    'depends': ['base_setup','web','mail',],
    'data': [
           "security/ir.model.access.csv",
           "security/security_digistra.xml",
           'views/plan_strategique.xml',
           'views/atm_axe.xml',
           'views/indicateur_impact.xml',
           'views/indicateur_resultat_strategique.xml',
           'views/saisirIndicateurImpact.xml',
           'views/saisirIndicateurresultatstrategique.xml',
           'views/atm_effet.xml',
            'views/risque_Indicateur_effet.xml',
            'views/indicateur_effet.xml',
            'views/saisir_indicateur_effet.xml',
            'views/risque_Indicateur_effet.xml',
            'views/Hypothese_Indicateur_Effet.xml',
            'views/Atm_Produit.xml',
            'views/Hypothese_Indicateur_Produit.xml',
            'views/Indicateur_Produit.xml',
            'views/Saisir_Indicateur_Produit.xml',
            'views/Risque_Indicateur_Produit.xml',
            'views/Atm_Action.xml',
            'views/atm_impact.xml',
            'views/donne_synthese_indicateur_action.xml',
            'views/donne_synthese_indicateur_produit.xml',
            'views/resultat_strategique.xml',
            'views/Atm_Profil.xml',
            'views/Atm_Direction.xml',
            'views/Atm_Partenaire.xml',
            'views/atm_pdf.xml',
            'views/saisir_action.xml',
            "views/tableau_bord.xml",
            "views/menu_general.xml",
             #"views/requete_tableau_bord.xml",
             "views/users.xml"
    ],
    'assets': {
        'web.assets_backend': [
            "/Digistrat/static/src/css/custom.css",

        ]
    },
    'installable': True,
    'license': 'LGPL-3',
}
