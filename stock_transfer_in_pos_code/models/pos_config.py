# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.fields import Command


class PosConfig(models.Model):
    _inherit = 'pos.config'

   
    # SETTINGS FIELDS
   
    stock_transfer = fields.Boolean(
        string="Enable Stock Transfer",
        help="Enable if you want to transfer stock from PoS session"
    )

    scrap_conditional = fields.Boolean(
        string="Enable Conditional Scrap",
        help=(
            "If checked: scrap orders without available stock stay in draft.\n"
            "If unchecked (strict): scrap requires available stock to validate."
        )
    )


    # STOCK TRANSFER LIST FOR POS UI
  
    @api.model
    def get_stock_transfer_list(self):
        main = {}
        main['picking_type'] = self.env['stock.picking.type'].search_read(
            [('company_id', '=', self.env.user.company_id.id)],
            ['display_name', 'code']
        )
        main['location'] = self.env['stock.location'].search_read([], ['display_name'])
        main['wh_stock'] = self.env['stock.warehouse'].search(
            [('company_id', '=', self.env.user.company_id.id)]
        ).lot_stock_id.id
        return main

   
    # CREATE TRANSFER
   
    @api.model
    def create_transfer(self, pick_id, source_id, dest_id, state, line):
        transfer = self.env['stock.picking'].create({
            'picking_type_id': int(pick_id),
            'location_id': int(source_id),
            'location_dest_id': int(dest_id),
            'move_ids': [
                Command.create({
                    'product_id': line['pro_id'][rec],
                    'product_uom_qty': line['qty'][rec],
                    'location_id': int(source_id),
                    'location_dest_id': int(dest_id),
                    'name': "Product",
                }) for rec in range(len(line['pro_id']))
            ],
        })
        transfer.write({'state': state})
        return {
            'id': transfer.id,
            'name': transfer.name
        }

   
    # CREATE SCRAP
    
    @api.model
    def create_scrap_from_pos(self, product_lines, reason):
        """Create scrap orders from POS with strict/conditional mode behavior."""

        
        config_id = self.env.context.get("pos_config_id")
        if not config_id:
            return {
                "ids": [],
                "warnings": ["POS config missing from context"],
                "name": False,
                "mode": "strict",
            }

        pos_config = self.env['pos.config'].browse(config_id)

      
        mode = 'conditional' if pos_config.scrap_conditional else 'strict'

        scrap_ids = []
        warning_products = []

       
        try:
            stock_location = self.env.ref("stock.stock_location_stock")
        except Exception:
            stock_location = self.env['stock.location'].search(
                [('usage', '=', 'internal')], limit=1)

      
        session = self.env['pos.session'].search(
            [('config_id', '=', pos_config.id), ('state', '=', 'opened')],
            limit=1)

        if session:
            pos_origin = f"POS Scrap ({session.name}) - {self.env.user.name}"
        else:
            pos_origin = f"POS Scrap - {self.env.user.name}"

        
        for line in product_lines:
            product = self.env['product.product'].browse(line['product_id'])
            qty = abs(line['qty'])

            if not product:
                continue

            available_qty = product.with_context(
                location=stock_location.id).qty_available

           
            origin_value = (
                f"{pos_origin} | Reason: {reason}"
                if reason else pos_origin
            )

            scrap = self.env["stock.scrap"].create({
                "product_id": product.id,
                "scrap_qty": qty,
                "origin": origin_value,
                "location_id": stock_location.id,
            })

            # STRICT MODE
            if mode == 'strict':
                if available_qty >= qty:
                    scrap.action_validate()
                else:
                    warning_products.append(product.display_name)
                    scrap.unlink()
                    continue

            # CONDITIONAL MODE
            else:  
                if available_qty >= qty:
                    scrap.action_validate()
                

            scrap_ids.append(scrap.id)

        return {
            "ids": scrap_ids,
            "warnings": warning_products,
            "name": scrap_ids and f"SCRAP/{scrap_ids[0]}" or False,
            "mode": mode,
        }

   
    @api.model
    def get_pos_scrap_orders(self):
        """Return scrap orders created from POS for POS Scrap Orders Screen."""

        scraps = self.env["stock.scrap"].search(
            [("origin", "ilike", "POS Scrap")]
        )

        return scraps.read([
            "name",
            "product_id",
            "scrap_qty",
            "date_done",
            "state",
            "location_id",
        ])
