from odoo import api, fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "sequence.number.mixin", "expression.value.mixin"]
    _sequence_field = "sequence_number"
    _ir_sequence_code = "product.product"

    # _unique_sequence = models.Constraint(
    #     "UNIQUE(sequence_number, company_id)",
    #     "sequence_number must be unique per company!",
    # )
    # unable to add constraint 'product_product_unique_sequence_number_per_company' as UNIQUE(sequence_number, company_id)

    sequence_number = fields.Char(
        string="No.",
        copy=False,
        readonly=True,
    )
