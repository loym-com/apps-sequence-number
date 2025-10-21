# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

import psycopg2

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class UniqueCodeMixin(models.AbstractModel):
    _name = "sequence.number.mixin"
    _inherit = "expression.value.mixin"
    _description = "Sequence No Mixin"
    _sql_constraints = [
        (
            "unique_sequence_number",
            "UNIQUE(sequence_number)",
            "sequence_number must be unique!",
        ),
    ]

    sequence_code = fields.Char(
        string="Sequence Code",
        copy=False,
        store=True,
        help="Configure in model settings."
    )

    sequence_number = fields.Char(
        string="No.",
        copy=False,
        index=True,
        store=True,
        help="Configure in model settings."
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Set sequence_number and name, if sequence_number is not set."""
        vals_list_ok = [vals for vals in vals_list if "sequence_number" in vals]
        vals_list_todo = [vals for vals in vals_list if "sequence_number" not in vals]
        # Create first, so we can use the record "id" etc. in the expression
        records_ok = super().create(vals_list_ok)
        records_todo = super().create(vals_list_todo)
        records_todo.set_sequence_code_sequence_number_and_name()
        return records_ok | records_todo

    def write(self, vals):
        vals = self._ondelete_sequence_number_delete_also_sequence_code(vals)
        super().write(vals)
        self._set_name_if_empty()

    def set_sequence_code_sequence_number_and_name(self):
        self._set_sequence_code()
        self._set_sequence_number()
        self._set_name_if_empty()

    def _ondelete_sequence_number_delete_also_sequence_code(self, vals):
        if "sequence_number" in vals and not vals.get("sequence_number"):
            vals["sequence_code"] = ""
        return vals

    def _set_sequence_code(self):
        """Set sequence_code based on the ir.model's number_sequence_option and number_sequence_id or number_sequence_field_id."""
        records = self.filtered(lambda r: not r.sequence_code)
        number_sequence_option = self.get_ir_model().number_sequence_option
        if not number_sequence_option:
            return
        elif number_sequence_option == "sequence":
            sequence = self.get_ir_model(prefetch_fields=False).number_sequence_id
            if not sequence:
                return
            for record in records:
                record.sequence_code = sequence.next_by_id()
        elif number_sequence_option == "field":
            choice_field = self.get_ir_model(prefetch_fields=False).number_sequence_field_id
            if not choice_field:
                return
            for record in records:
                choice_value = getattr(record, choice_field.name)
                if choice_field.ttype == "many2one":
                    choice_value = choice_value.id
                choice_value = str(choice_value)
                #################################################################
                code = f"{choice_field.model}.{choice_field.name}.{choice_value}"
                #################################################################
                sequence_code = self.env["ir.sequence"].next_by_code(code)
                if sequence_code:
                    setattr(record, "sequence_code", sequence_code)
                else:
                    raise UserError(
                        "No sequence found for code:\n"
                        f"{code}\n\n"
                        "Please create a sequence for this code.\n\n"
                        f"Or go to Settings - Technical - Database Structure - Models - {choice_field.model}.\n"
                        "CHOOSE SEQUENCE BY:\n"
                        "- Remember the current setting.\n"
                        "- Set the field to blank and save.\n"
                        "- Set the field to the remembered value and save.\n"
                        "Then go to Sequences and configure the new sequence(s)."
                    )

    def _set_sequence_number(self):
        for record in self:
            record.sequence_number = record.get_value_from_source("ir.model", "number_expression")

    def _set_name_if_empty(self):
        """Set name = sequence_number if removing name or no existing name

        Checking if the record has a name may affect the performance..."""

        # Relevant for uninstalling the module
        context = self.env.context
        if "prefetch_fields" in context and not context.get("prefetch_fields"):
            return

        if "name" not in self._fields:
            return

        for record in self:
            if record.sequence_number and not record.name:
                record.name = record.sequence_number
