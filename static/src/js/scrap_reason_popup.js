/** @odoo-module **/

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { useRef } from "@odoo/owl";
import { ScrapSuccessPopup } from "./scrap_success_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

export class ScrapReasonPopup extends AbstractAwaitablePopup {
    static template = "ScrapReasonPopup";

    setup() {
        super.setup();
        this.pos = usePos();
        this.orm = useService("orm");
        this.popup = useService("popup");

        this.reasonRef = useRef("reason");
    }

    async applyScrap() {
        let order = this.pos.get_order();
        let reason = this.reasonRef.el.value;

        let lines = order.get_orderlines().map((l) => ({
            product_id: l.product.id,
            qty: l.quantity,
        }));

        
        let result = await this.orm.call(
            "pos.config",
            "create_scrap_from_pos",
            [lines, reason],
            { context: { pos_config_id: this.pos.config.id } }
        );

        
        if (result.warnings && result.warnings.length > 0) {
            await this.popup.add(ErrorPopup, {
                title: "Scrap Failed (Strict Mode)",
                body: `Insufficient stock for: ${result.warnings.join(", ")}`,
            });
        }

        
        if (!result.ids || result.ids.length === 0) {
            await this.popup.add(ErrorPopup, {
                title: "No Scrap Created",
                body: "No products matched your scrap conditions.",
            });
            return;
        }

        
        await this.popup.add(ScrapSuccessPopup, {
            title: "Scrap Created",
            body:
                result.mode === "strict"
                    ? `Scrap Order Created & Validated: ${result.name}`
                    : `Scrap Order Created (${result.name}) — Validated only if stock was available.`,
        });

       
        order.orderlines.forEach((line) => line.set_quantity(0));

        this.cancel();
    }
}
