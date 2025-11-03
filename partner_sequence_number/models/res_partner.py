from odoo import api, fields, models


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

    # @api.depends("name")
    # def _compute_display_name(self):
    #     """
    #     If display_name is stored, restart Odoo after changing display_name_expression.
    #     """
    #     expression = self.get_expression_from_source("ir.model", "display_name_expression")

    #     if expression:
    #         fallback_records = self.browse([])  # empty recordset
    #         for rec in self:
    #             display_name = rec.get_value_from_expression(expression)
    #             if display_name:
    #                 rec.display_name = display_name
    #             else:
    #                 fallback_records |= rec  # collect records for super

    #         if fallback_records:
    #             super(type(self), fallback_records)._compute_display_name()
    #     else:
    #         super()._compute_display_name()

    # @api.depends("name")
    # def _compute_display_name(self):
    #     expression = self.get_expression_from_source("ir.model", "display_name_expression")

    #     if not expression:
    #         # fallback: call super on the whole recordset
    #         return super()._compute_display_name()

    #     # records that can be computed via expression
    #     expr_records = self.browse([])
    #     fallback_records = self.browse([])

    #     for rec in self:
    #         display_name = rec.get_value_from_expression(expression)
    #         if display_name:
    #             rec.display_name = display_name
    #             expr_records |= rec
    #         else:
    #             fallback_records |= rec

    #     # call super ONLY on fallback_records
    #     if fallback_records:
    #         # use the base class explicitly, not self.__class__
    #         super(type(self), fallback_records)._compute_display_name()


