from odoo import api, fields, models


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = ["crm.lead", "sequence.number.mixin", "display.name.mixin"]
    _sequence_field = "sequence_number"

    sequence_number = fields.Char(
        string="No.",
        copy=False,
        readonly=True,
    )
