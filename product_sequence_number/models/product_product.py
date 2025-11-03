from odoo import api, fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "sequence.number.mixin", "expression.value.mixin"]
    _sequence_field = "sequence_number"
    _ir_sequence_code = "product.product"
    _sql_constraints = [
        (
            "unique_sequence",
            "UNIQUE(sequence_number)",
            "sequence_number must be unique!",
        ),
    ]

    sequence_number = fields.Char(
        string="No.",
        copy=False,
        readonly=True,
    )
