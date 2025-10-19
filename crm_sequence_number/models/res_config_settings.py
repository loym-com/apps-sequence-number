from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.depends("company_id")
    def _compute_crm_lead_model(self):
        for record in self:
            record.crm_lead_model = self.env["ir.model"].sudo().search([("model", "=", "crm.lead")], limit=1)

    crm_lead_model = fields.Many2one(
        "ir.model", string="Lead Model", compute="_compute_crm_lead_model", store=True
    )
    crm_lead_number_expression = fields.Char(
        related="crm_lead_model.number_expression",
        readonly=False,
        string="Lead No.",
    )
    crm_lead_number_sequence_option = fields.Selection(
        related="crm_lead_model.number_sequence_option",
        readonly=False,
        string="Lead Option",
    )
    crm_lead_number_sequence_id = fields.Many2one(
        related="crm_lead_model.number_sequence_id",
        readonly=False,
        string="Lead Sequence",
    )
    crm_lead_number_sequence_field_id = fields.Many2one(
        related="crm_lead_model.number_sequence_field_id",
        readonly=False,
        string="Lead Field",
    )

    def crm_lead_action_goto_sequences(self):
        return self.env.ref("crm.model_crm_lead").action_goto_sequences()
