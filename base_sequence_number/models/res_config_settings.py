from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.depends("company_id")
    def _compute_res_partner_model(self):
        for record in self:
            record.res_partner_model = self.env["ir.model"].sudo().search([("model", "=", "res.partner")], limit=1)

    res_partner_model = fields.Many2one(
        "ir.model", string="Contact Model", compute="_compute_res_partner_model", store=True
    )
    res_partner_number_expression = fields.Char(
        related="res_partner_model.number_expression",
        readonly=False,
        string="Contact No.",
    )
    res_partner_number_sequence_option = fields.Selection(
        related="res_partner_model.number_sequence_option",
        readonly=False,
        string="Contact Option",
    )
    res_partner_number_sequence_id = fields.Many2one(
        related="res_partner_model.number_sequence_id",
        readonly=False,
        string="Contact Sequence",
    )
    res_partner_number_sequence_field_id = fields.Many2one(
        related="res_partner_model.number_sequence_field_id",
        readonly=False,
        string="Contact Field",
    )

    def res_partner_action_goto_sequences(self):
        return self.env.ref("base.model_res_partner").action_goto_sequences()
