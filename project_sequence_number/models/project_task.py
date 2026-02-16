from odoo import models, fields

PROJECT_TASK_WRITABLE_FIELDS = {
    "code",
}


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = ["project.task", "sequence.number.mixin", "expression.value.mixin"]
    _sequence_field = "code" # Same as in OCA project_task_code
    _ir_sequence_code = "project.task"
    _sql_constraints = [
        (
            "unique_code_per_company",
            "UNIQUE(code, company_id)",
            "code must be unique per company!",
        ),
    ]

    @property
    def SELF_WRITABLE_FIELDS(self):
        return super().SELF_WRITABLE_FIELDS | PROJECT_TASK_WRITABLE_FIELDS

    company_code = fields.Char(
        related="company_id.code",
        string="Company Code",
        store=True,
        readonly=True,
    )
    code = fields.Char(
        string="Task No.",
        # required=True,
        # default="/",
        copy=False,
    )
