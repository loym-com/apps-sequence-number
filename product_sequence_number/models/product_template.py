from odoo import api, fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "sequence.number.mixin", "expression.value.mixin"]
    _sequence_field = "sequence_number"
    _ir_sequence_code = "product.template"
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
