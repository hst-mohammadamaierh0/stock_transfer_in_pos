/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { registry } from "@web/core/registry";

export class PosScrapOrdersScreen extends Component {
    static template = "PosScrapOrdersScreen";

    setup() {
        this.orm = useService("orm");
        this.pos = usePos();
        this.state = useState({ scraps: [] });

        this.loadScrapOrders();
    }

    
    // Convert UTC → Local Time
    
    convertUTCtoLocal(utcDate) {
        if (!utcDate) return "";
        try {
            const localDate = new Date(utcDate + " UTC");
            return localDate.toLocaleString(); 
        } catch (error) {
            return utcDate;
        }
    }

    async loadScrapOrders() {
        const scraps = await this.orm.call(
            "pos.config",
            "get_pos_scrap_orders",
            [],
            {}
        );

       
        scraps.forEach(s => {
            s.date_done_local = this.convertUTCtoLocal(s.date_done);
        });

        this.state.scraps = scraps;
    }

    back() {
        this.pos.showScreen("ProductScreen");
    }

    openBackend(scrap) {
        window.location = `/web#id=${scrap.id}&model=stock.scrap&view_type=form`;
    }
}


registry.category("pos_screens").add("PosScrapOrdersScreen", PosScrapOrdersScreen);
