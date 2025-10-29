from odoo import api, fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "sequence.number.mixin", "display.name.mixin"]
    _sequence_field = "sequence_number"

    sequence_number = fields.Char(
        string="No.",
        copy=False,
        readonly=True,
    )
