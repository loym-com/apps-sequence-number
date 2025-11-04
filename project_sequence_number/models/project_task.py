from odoo import models, fields

PROJECT_TASK_WRITABLE_FIELDS = {
    "sequence_number",
}


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = ["project.task", "sequence.number.mixin", "expression.value.mixin"]
    _sequence_field = "code" # Same as in OCA project_task_code
    _ir_sequence_code = "project.task"

    _unique_sequence = models.Constraint(
        'UNIQUE(code)',
        'code must be unique!'
    )

    @property
    def SELF_WRITABLE_FIELDS(self):
        return super().SELF_WRITABLE_FIELDS | PROJECT_TASK_WRITABLE_FIELDS

    code = fields.Char(
        string="No.",
        # required=True,
        # default="/",
        readonly=True,
        copy=False,
    )
