from odoo import fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "sequence.number.mixin", "display.name.mixin"]
    _sequence_field = "sequence_number"
    _ir_sequence_code = "res.partner"
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
