# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

import psycopg2

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

# from odoo.addons.base_display_name.tools import get_value, is_none, set_value
from odoo.addons.expression_value.expression_value import ExpressionValue


class UniqueCodeMixin(models.AbstractModel):
    _name = "unique.code.mixin"
    _description = "Unique Code Mixin"
    _inherit = "display.name.mixin"
    _sql_constraints = [
        (
            "unique_unique_code",
            "UNIQUE(unique_code)",
            "unique_code must be unique!",
        ),
    ]

    sequence_code = fields.Char(
        string="Sequence No.",
        copy=False,
        store=True,
        help="Configure in model settings."
    )

    unique_code = fields.Char(
        string="No.",
        copy=False,
        index=True,
        store=True,
        help="Configure in model settings."
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Set unique_code and name, if unique_code is not set."""
        vals_list_ok = [vals for vals in vals_list if "unique_code" in vals]
        vals_list_todo = [vals for vals in vals_list if "unique_code" not in vals]
        # Create first, so we can use the record "id" etc. in the pattern
        records_ok = super().create(vals_list_ok)
        records_todo = super().create(vals_list_todo)
        records_todo.set_sequence_code_unique_code_and_name()
        return records_ok | records_todo

    def write(self, vals):
        super().write(vals)
        self._set_name_if_empty()

    def set_sequence_code_unique_code_and_name(self):
        self._set_sequence_code()
        self._set_unique_code()
        self._set_name_if_empty()

    def _set_sequence_code(self):
        """Set sequence_code based on the ir.model's sequence_option and sequence_id or sequence_field_id."""
        records = self.filtered(lambda r: not r.sequence_code)
        sequence_option = self._get_ir_model().sequence_option
        if not sequence_option:
            return
        elif sequence_option == "one":
            sequence = self._get_ir_model(prefetch_fields=False).sequence_id
            if not sequence:
                return
            for record in records:
                record.sequence_code = sequence.next_by_id()
        elif sequence_option == "field":
            choice_field = self._get_ir_model(prefetch_fields=False).sequence_field_id
            if not choice_field:
                return
            for record in records:
                choice_value = getattr(record, choice_field)
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

    def _set_unique_code(self):
        for record in self:
            expr_val = ExpressionValue(
                source="ir.model",
                source_model=record._name,
                source_lookup="unique_code_expression",
                record=record,
            )
            record.unique_code = expr_val.value

    def _set_name_if_empty(self):
        """Set name = unique_code if removing name or no existing name

        Checking if the record has a name may affect the performance..."""

        # Relevant for uninstalling the module
        context = self.env.context
        if "prefetch_fields" in context and not context.get("prefetch_fields"):
            return

        if "name" not in self._fields:
            return
        
        if self.unique_code and not self.name:
            self.name = self.unique_code
