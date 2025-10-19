from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # project.project

    @api.depends("company_id")
    def _compute_project_project_model(self):
        for record in self:
            record.project_project_model = self.env.ref("project.model_project_project")

    project_project_model = fields.Many2one(
        "ir.model", string="Project Model", compute="_compute_project_project_model", store=True
    )
    project_project_number_expression = fields.Char(
        related="project_project_model.number_expression",
        readonly=False,
        string="Project No.",
    )
    project_project_number_sequence_option = fields.Selection(
        related="project_project_model.number_sequence_option",
        readonly=False,
        string="Project Option",
    )
    project_project_number_sequence_id = fields.Many2one(
        related="project_project_model.number_sequence_id",
        readonly=False,
        string="Project Sequence",
    )
    project_project_number_sequence_field_id = fields.Many2one(
        related="project_project_model.number_sequence_field_id",
        readonly=False,
        string="Project Field",
    )

    def project_project_action_goto_sequences(self):
        return self.env.ref("project.model_project_project").action_goto_sequences()
    
    # project.task

    @api.depends("company_id")
    def _compute_project_task_model(self):
        for record in self:
            record.project_task_model = self.env.ref("project.model_project_task")

    project_task_model = fields.Many2one(
        "ir.model", string="Task Model", compute="_compute_project_task_model", store=True
    )
    project_task_number_expression = fields.Char(
        related="project_task_model.number_expression",
        readonly=False,
        string="Task No.",
    )
    project_task_number_sequence_option = fields.Selection(
        related="project_task_model.number_sequence_option",
        readonly=False,
        string="Task Option",
    )
    project_task_number_sequence_id = fields.Many2one(
        related="project_task_model.number_sequence_id",
        readonly=False,
        string="Task Sequence",
    )
    project_task_number_sequence_field_id = fields.Many2one(
        related="project_task_model.number_sequence_field_id",
        readonly=False,
        string="Task Field",
    )

    def project_task_action_goto_sequences(self):
        return self.env.ref("project.model_project_task").action_goto_sequences()
