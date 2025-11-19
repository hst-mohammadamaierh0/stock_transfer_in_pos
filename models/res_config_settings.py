# -*- coding: utf-8 -*-
###############################################################################
#    Cybrosys Technologies Pvt. Ltd.
###############################################################################

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Add POS stock transfer + scrap checkbox behavior"""
    _inherit = 'res.config.settings'

    is_stock_transfer = fields.Boolean(
        related="pos_config_id.stock_transfer",
        string="Enable Stock Transfer",
        help="Enable if you want to transfer stock from PoS session",
        readonly=False
    )

    # conditional scrap
    scrap_conditional = fields.Boolean(
        related="pos_config_id.scrap_conditional",
        string="Enable Conditional Scrap",
        help="If checked: scrap stays draft when no stock. If unchecked: strict validation applies.",
        readonly=False
    )
