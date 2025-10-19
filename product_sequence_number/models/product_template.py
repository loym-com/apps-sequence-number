# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "sequence.number.mixin"]

    sequence_number = fields.Char(
        string="Product Number",
        compute="_compute_sequence_number",
        store=True,
    )
    main_variant_id = fields.Many2one(
        comodel_name="product.product",
        string="Main Variant",
        # group="stock.group_stock_manager",
        help="The main variant of the product template. "
             "This is used to determine the unique code for the product template. "
             "Only STOCK MANAGER can change this value.",
    )

    @api.depends(
        "product_variant_ids.sequence_number",
        "product_variant_ids.active",
        "main_variant_id",
    )
    def _compute_sequence_number(self):
        """Get active product variant sequence_number."""
        param_name = 'product_sequence_number.product_template_sequence_number_from_variant'
        param = self.env['ir.config_parameter'].sudo().get_param(param_name)
        if param:
            for template in self:
                if template.main_variant_id:
                    template.sequence_number = template.main_variant_id.sequence_number
