from odoo import api, fields, models


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = ["crm.lead", "sequence.number.mixin", "expression.value.mixin"]
    _sequence_field = "sequence_number"
    _ir_sequence_code = "crm.lead"

    _unique_sequence = models.Constraint(
        "UNIQUE(sequence_number, company_id)",
        "sequence_number must be unique per company!",
    )

    sequence_number = fields.Char(
        string="No.",
        copy=False,
        readonly=True,
    )
