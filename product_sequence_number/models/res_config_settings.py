from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_template_display_name_expression = fields.Char(
        related="ir_model_product_template.display_name_expression",
        readonly=False,
        string="Template Display Name Pattern",
    )
    product_template_number_expression = fields.Char(
        related="ir_model_product_template.number_expression",
        readonly=False,
        string="Template Sequence No Pattern",
    )
    product_template_number_sequence_id = fields.Many2one(
        related="ir_model_product_template.number_sequence_id",
        readonly=False,
        string="Template Sequence",
    )
    product_template_sequence_number_from_variant = fields.Boolean(
        string="Get Sequence No from Variant",
        config_parameter="product_sequence_number.product_template_sequence_number_from_variant"
    )

    product_product_display_name_expression = fields.Char(
        related="ir_model_product_product.display_name_expression",
        readonly=False,
        string="Variant Display Name Pattern",
    )
    product_product_number_expression = fields.Char(
        related="ir_model_product_product.number_expression",
        readonly=False,
        string="Variant Sequence No Pattern",
    )
    product_product_number_sequence_id = fields.Many2one(
        related="ir_model_product_product.number_sequence_id",
        readonly=False,
        string="Variant Sequence",
    )

    ir_model_product_template = fields.Many2one(
        "ir.model", string="Template Model", compute="_compute_ir_model_product_template", store=True
    )
    ir_model_product_product = fields.Many2one(
        "ir.model", string="Variant Model", compute="_compute_ir_model_product_product", store=True
    )

    @api.depends("company_id")
    def _compute_ir_model_product_template(self):
        for record in self:
            record.ir_model_product_template = self.env["ir.model"].search([("model", "=", "product.template")], limit=1)

    @api.depends("company_id")
    def _compute_ir_model_product_product(self):
        for record in self:
            record.ir_model_product_product = self.env["ir.model"].search([("model", "=", "product.product")], limit=1)
