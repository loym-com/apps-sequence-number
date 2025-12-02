from odoo import api, fields, models


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", "sequence.number.mixin", "expression.value.mixin"]
    _sequence_field = "sequence_code" # Same as in OCA project_sequence
    _ir_sequence_code = "project.sequence"
    _sql_constraints = [
        (
            "unique_sequence",
            "UNIQUE(sequence_code)",
            "sequence_code must be unique!",
        ),
    ]

    sequence_code = fields.Char(
        string="No.",
        copy=False,
        readonly=True,
    )

    name = fields.Char(
        # We actually require it with the SQL constraint, but it is disabled
        # here to let users create/write projects without name, and let this module
        # add a default name if needed
        required=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        new_records = super().create(vals_list)
        new_records._sync_related_records()
        return new_records

    def write(self, vals):
        super().write(vals)
        self._sync_related_records(vals)
        return True

    def copy(self, default):
        new_records = super().copy(default)
        new_records._sync_related_records()
        return new_records

    def _sync_related_records(self, vals=None):
        for project in self:

            # --- analytic account ---
            if project.account_id:
                if not vals or "sequence_code" in vals:
                    project.account_id.code = project.sequence_code
                if not vals or "name" in vals:
                    project.account_id.name = project.name
