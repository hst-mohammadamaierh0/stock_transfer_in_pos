/** @odoo-module */

import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { _t } from "@web/core/l10n/translation";
import { ScrapReasonPopup } from "./scrap_reason_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

/* SCRAP BUTTON */
export class ScrapButton extends Component {
    static template = "ScrapButton";

    setup() {
        this.pos = usePos();
        this.orm = useService("orm");
    }

    async onClick() {
        let order = this.pos.get_order();

        if (!order || order.orderlines.length === 0) {
            this.pos.popup.add(ErrorPopup, {
                title: _t("No products"),
                body: _t("Please select at least one product"),
            });
            return;
        }

        this.pos.popup.add(ScrapReasonPopup, {
            title: _t("Scrap Reason"),
        });
    }
}

ProductScreen.addControlButton({
    component: ScrapButton,
    condition: () => true,
});

/* SCRAP ORDERS SCREEN BUTTON */
export class ScrapOrdersButton extends Component {
    static template = "ScrapOrdersButton";

    setup() {
        this.pos = usePos();
    }

    onClick() {
        this.pos.showScreen("PosScrapOrdersScreen");
    }
}

ProductScreen.addControlButton({
    component: ScrapOrdersButton,
    condition: () => true,
});