# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    def _compute_number_field_exists(self):
        for record in self:
            field = self.env["ir.model.fields"].search(
                [
                    ("model_id", "=", record.id),
                    ("name", "=", "sequence_number"),
                ],
            )
            record.number_field_exists = bool(field)

    number_field_exists = fields.Boolean(
        string="No. field exists",
        compute="_compute_number_field_exists",
        help="When a model does not have a sequence_number field, hide the settings.",
    )
    number_expression = fields.Char(
        string="No. Expression",
        help=(
            "Example: 'Y{create_date:%y}-{parent_id.id:>03}'\n"
            "Computed with safe_eval."
        ),
    )
    number_sequence_option = fields.Selection(
        [
            ("sequence", "Use one sequence"),
            ("field", "Choose sequence by a field"),
        ],
        string="No. Sequence Option",
    )
    number_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="No. Sequence",
    )
    number_sequence_field_id = fields.Many2one(
        string="No. Sequence Field",
        comodel_name="ir.model.fields",
        domain="[('id', 'in', field_id), ('ttype', 'in', ['boolean', 'selection', 'many2one'])]",
        help="If this field is empty, "
            "all records will get a sequence code from the same sequence.\n"
            "If this field is set, "
            "a record will get a sequence code depending on the value of this field.\n"
            "Available field types are 'selection' or 'boolean'.\n"
            "A 'boolean' field has two options: True or False.\n"
            "A 'selection' field has a list of options.\n"
            "A sequence is created for each option.\n\n"
            "NB: If another Odoo app is installed later and that app adds an option,"
            "then do this to create a sequence for the new option:\n"
            "1. Set this field to empty, and save.\n"
            "2. Set this field again, and save."
    )

    @api.constrains("number_sequence_field_id")
    def set_sequences(self):
        self.ensure_one()
        Sequence = self.env["ir.sequence"]
        if self.number_sequence_field_id:
            field = self.number_sequence_field_id
            if field.ttype == "boolean":
                values = ["True", "False"]
            elif field.ttype == "many2one":
                values = self.env[field.relation].search([]).mapped("id")
                values = [str(value) for value in values]
            elif field.ttype == "selection":
                values = field.selection_ids.mapped("value")
            else:
                raise ValidationError(f"Unsupported field type {field.ttype}")

            for value in values:
                ###########################################
                code = f"{self.model}.{field.name}.{value}"
                ###########################################
                sequence = Sequence.search([("code", "=", code)])
                if not sequence:
                    if field.ttype == "many2one":
                        name = self.env[field.relation].browse(int(value)).display_name
                    else:
                        name = code
                    Sequence.create(
                        {
                            "name": name,
                            "code": code,
                            "prefix": f"{value}-",
                            "padding": 5,
                        }
                    )

    @api.constrains("number_expression")
    def raise_error_if_invalid_field_paths(self):
        return self.env[self.model].raise_error_if_invalid_field_paths_from_source(
            "ir.model", "number_expression"
        )

    def action_goto_sequences(self):
        """Return an action showing sequences relevant for this model and field."""
        self.ensure_one()

        # Base search domain for ir.sequence
        domain = []

        # Example: if _name == 'res.partner' and number_sequence_field_id.name == 'is_company'
        # show sequences with code starting with 'res.partner.is_company'
        if self.model and self.number_sequence_field_id:
            #######################################################
            prefix = f"{self.model}.{self.number_sequence_field_id.name}."
            #######################################################
            domain = [("code", "like", prefix + "%")]
        else:
            raise UserError(_("Save and try again to see the sequences."))

        return {
            "type": "ir.actions.act_window",
            "name": _("Sequences"),
            "res_model": "ir.sequence",
            "view_mode": "list,form",
            "domain": domain,
        }
