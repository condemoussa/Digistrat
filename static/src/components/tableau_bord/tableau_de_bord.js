/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillUpdateProps,useState,onWillStart,onMounted } = owl;

export class Tableau_de_bord_digistrat extends Component {
    setup() {
        this.orm = useService("orm");

          // Déclarez une variable pour stocker le total des axes
        this.state = useState({
                              totalAxe: 0,
                              totalEffet:0,
                              totalProduit:0,
                              totalAction:0,
                              totalAtteint:0,
                              totalNonAtteint:0,
                               data: [],
                               });

        // Récupérez le total des axes au démarrage du composant

        onWillStart(async () => {

                                  const totalAxe = await this.orm.searchCount("atm.axe", []);
                                  const totalEffet = await this.orm.searchCount("atm.effet", []);
                                  const totalAction = await this.orm.searchCount("atm.action", []);
                                  const produit = await this.orm.searchCount("atm.produit", []);
                                  const atteint = await this.orm.searchCount("saisir.indicateur.impact", [['status', '=', 'atteint']]);
                                // Compter les indicateurs avec le statut 'non atteint'
                                   const NonAtteint = await this.orm.searchCount("saisir.indicateur.impact", [['status', '=', 'no_atteint']]);
                                    this.state.totalAxe = totalAxe;
                                    this.state.totalEffet = totalEffet;
                                    this.state.totalAction = totalAction;
                                    this.state.totalAtteint = atteint;
                                    this.state.totalNonAtteint = NonAtteint;
                                    this.state.data = [
                                            { name: 'Atteint', value: atteint },
                                            { name: 'Non Atteint', value: NonAtteint },
                                    ];
              });


    }
}

// Associez le template au composant
Tableau_de_bord_digistrat.template = "Tableau_de_bord_digistrat";

// Enregistrez le composant dans le registre
registry.category("actions").add("tableau_de_bord_digistrat", Tableau_de_bord_digistrat);