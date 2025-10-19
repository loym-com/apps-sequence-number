from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # product.product

    @api.depends("company_id")
    def _compute_product_product_model(self):
        for record in self:
            record.product_product_model = self.env.ref("product.model_product_product")

    product_product_model = fields.Many2one(
        "ir.model", string="Product Variant Model", compute="_compute_product_product_model", store=True
    )
    product_product_number_expression = fields.Char(
        related="product_product_model.number_expression",
        readonly=False,
        string="Product Variant No.",
    )
    product_product_number_sequence_option = fields.Selection(
        related="product_product_model.number_sequence_option",
        readonly=False,
        string="Product Variant Option",
    )
    product_product_number_sequence_id = fields.Many2one(
        related="product_product_model.number_sequence_id",
        readonly=False,
        string="Product Variant Sequence",
    )
    product_product_number_sequence_field_id = fields.Many2one(
        related="product_product_model.number_sequence_field_id",
        readonly=False,
        string="Product Variant Field",
    )

    def product_product_action_goto_sequences(self):
        return self.env.ref("product.model_product_product").action_goto_sequences()
    
    # product.template

    @api.depends("company_id")
    def _compute_product_template_model(self):
        for record in self:
            record.product_template_model = self.env.ref("product.model_product_template")

    product_template_model = fields.Many2one(
        "ir.model", string="Lead Model", compute="_compute_product_template_model", store=True
    )
    product_template_number_expression = fields.Char(
        related="product_template_model.number_expression",
        readonly=False,
        string="Lead No.",
    )
    product_template_number_sequence_option = fields.Selection(
        related="product_template_model.number_sequence_option",
        readonly=False,
        string="Lead Option",
    )
    product_template_number_sequence_id = fields.Many2one(
        related="product_template_model.number_sequence_id",
        readonly=False,
        string="Lead Sequence",
    )
    product_template_number_sequence_field_id = fields.Many2one(
        related="product_template_model.number_sequence_field_id",
        readonly=False,
        string="Lead Field",
    )

    def product_template_action_goto_sequences(self):
        return self.env.ref("product.model_product_template").action_goto_sequences()
    
    # product.template special setting

    product_template_sequence_number_from_main_variant = fields.Boolean(
        string="Get Product Template No. from Main Variant",
        config_parameter="product_sequence_number.product_template_sequence_number_from_main_variant"
    )
