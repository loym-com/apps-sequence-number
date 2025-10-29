from odoo import api, fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "sequence.number.mixin", "display.name.mixin"]
    _sequence_field = "sequence_number"

    sequence_number = fields.Char(
        string="No.",
        copy=False,
        readonly=True,
    )
