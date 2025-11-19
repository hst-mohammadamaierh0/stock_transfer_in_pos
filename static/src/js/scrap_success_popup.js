/** @odoo-module **/
console.warn("ScrapSuccessPopup JS FILE LOADED");

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { registry } from "@web/core/registry";

export class ScrapSuccessPopup extends AbstractAwaitablePopup {
    static template = "ScrapSuccessPopup";

    async confirm() {
        this.cancel();
    }
}


registry.category("pos_popups").add("ScrapSuccessPopup", ScrapSuccessPopup);
