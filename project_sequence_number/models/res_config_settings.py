from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    project_project_display_name_expression = fields.Char(
        related="ir_model_project_project.display_name_expression",
        readonly=False,
        string="Project Display Name Pattern",
    )
    project_project_number_expression = fields.Char(
        related="ir_model_project_project.number_expression",
        readonly=False,
        string="Project Sequence No Pattern",
    )
    project_project_number_sequence_id = fields.Many2one(
        related="ir_model_project_project.number_sequence_id",
        readonly=False,
        string="Project Sequence",
    )
    project_task_display_name_expression = fields.Char(
        related="ir_model_project_task.display_name_expression",
        readonly=False,
        string="Task Display Name Pattern",
    )
    project_task_number_expression = fields.Char(
        related="ir_model_project_task.number_expression",
        readonly=False,
        string="Task Sequence No Pattern",
    )
    project_task_number_sequence_id = fields.Many2one(
        related="ir_model_project_task.number_sequence_id",
        readonly=False,
        string="Task Sequence",
    )

    ir_model_project_project = fields.Many2one(
        "ir.model", string="Project Model", compute="_compute_ir_model_project_project", store=True
    )
    ir_model_project_task = fields.Many2one(
        "ir.model", string="Task Model", compute="_compute_ir_model_project_task", store=True
    )

    @api.depends("company_id")
    def _compute_ir_model_project_project(self):
        for record in self:
            record.ir_model_project_project = self.env["ir.model"].search([("model", "=", "project.project")], limit=1)

    @api.depends("company_id")
    def _compute_ir_model_project_task(self):
        for record in self:
            record.ir_model_project_task = self.env["ir.model"].search([("model", "=", "project.task")], limit=1)
