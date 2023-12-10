/** @odoo-module **/

import {registry} from "@web/core/registry";

import {Component, useState,onWillStart} from "@odoo/owl";

class ConfirmationClientAction extends Component {
    setup() {
        this.states = useState({
            "confirmationList": []
        })
        this.MODEL = "kilo.booking"
        this.orm = this.env.services.orm;
        onWillStart(async ()=>{
            await this.getAllConfirmation()
        })
    }

    async getAllConfirmation() {
        this.states.confirmationList = await this.orm.searchRead(this.MODEL, [['state','=','confirm']], ['partner_id','date','start_kilo'])
    }
}

ConfirmationClientAction.template = "kali_confirmation.Confirmation";

// remember the tag name we put in the first step
registry.category("actions").add("kali_confirmation.ConfirmationClientAction", ConfirmationClientAction);