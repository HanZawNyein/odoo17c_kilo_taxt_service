/** @odoo-module **/

import {registry} from "@web/core/registry";

import {Component, useState, onWillStart} from "@odoo/owl";

class ConfirmationClientAction extends Component {
    setup() {
        this.states = useState({
            "confirmationList": []
        })
        this.MODEL = "kilo.booking"
        this.orm = this.env.services.orm;
        this.busService = this.env.services.bus_service;
        this.busChannel = "kilo_taxi_services";


        onWillStart(async () => {
            await this.getAllConfirmation();
            this.busService.addChannel(this.busChannel);
            this.busService.subscribe('kilo.booking/action_confirm', (data) => {
                this.addConfirmOrder(data);
            });
            this.busService.subscribe('kilo.booking/accept', (data) => {
                // console.log(data);
                this.removeAcceptOrder(data);
            });
            // this.busService.addEventListener('notification', (data) => {
            //     console.log(data)
            // });
        })
    }

    removeAcceptOrder(data) {
        this.states.confirmationList = this.states.confirmationList.filter((x) => x.id !== data.id)
    }

    addConfirmOrder(data) {
        this.states.confirmationList.push(data)
        // {'id':this.states.confirmationList.length,"partner_id"}
    }

    async getAllConfirmation() {
        this.states.confirmationList = await this.orm.searchRead(this.MODEL, [['state', '=', 'confirm']], ['partner_id', 'date', 'start_kilo'])
    }
}

ConfirmationClientAction.template = "kali_confirmation.Confirmation";

// remember the tag name we put in the first step
registry.category("actions").add("kali_confirmation.ConfirmationClientAction", ConfirmationClientAction);