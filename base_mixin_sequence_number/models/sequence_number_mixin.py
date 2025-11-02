# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

import psycopg2

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class SequenceNumberMixin(models.AbstractModel):
    _name = "sequence.number.mixin"
    _description = "Sequence No. Mixin"

    # Required settings by the model inheriting the mixin
    _sequence_field = "sequence_number"
    _ir_sequence_code = None

    # _sql_constraints = (_sequence_field and company_id) or (_sequence_field)
    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()

        # ignore base abstract model
        if not hasattr(cls, "_sequence_field"):
            return

        field = cls._sequence_field

        # At this point the fields registry is not yet fully built,
        # so we can't check cls._fields directly here.
        # Instead, we patch constraints in post_init.
        def _patch_constraints():
            _fields = cls._fields  # fields now exist
            if "company_id" in _fields:
                constraint_name = f"unique_{field}_company"
                sql = f"UNIQUE({field}, company_id)"
                message = f"{field} must be unique within the same company!"
            else:
                constraint_name = f"unique_{field}"
                sql = f"UNIQUE({field})"
                message = f"{field} must be unique!"

            cls._sql_constraints = [
                (constraint_name, sql, message)
            ]

        # defer until fields loaded
        cls._patch_constraints = staticmethod(_patch_constraints)

    def _register_hook(cls):
        """Called when the model is fully defined."""
        if hasattr(cls, "_patch_constraints"):
            cls._patch_constraints()
        return super()._register_hook()

    @api.model_create_multi
    def create(self, vals_list):
        """Set sequence_number and name, if sequence_number is not set."""
        vals_list_ok = [vals for vals in vals_list if self._sequence_field in vals]
        vals_list_todo = [vals for vals in vals_list if self._sequence_field not in vals]
        # Create first, so we can use the record "id" etc. in the expression
        records_ok = super().create(vals_list_ok)
        records_todo = super().create(vals_list_todo)
        records_todo.set_sequence_field_and_name()
        return records_ok | records_todo

    def write(self, vals):
        super().write(vals)
        self._set_name_if_empty()

    def set_sequence_field_and_name(self):
        self._set_sequence_field()
        self._set_name_if_empty()

    def _set_sequence_field(self):
        records = self.filtered(lambda r: not r[r._sequence_field])
        for rec in records:
            rec[self._sequence_field] = self.env['ir.sequence'].next_by_code(self._ir_sequence_code)

    def _set_name_if_empty(self):
        """Set name = sequence_number if removing name or no existing name

        Checking if the record has a name may affect the performance..."""

        # Relevant for uninstalling the module
        context = self.env.context
        if "prefetch_fields" in context and not context.get("prefetch_fields"):
            return

        if "name" not in self._fields:
            return

        for rec in self:
            if rec[rec._sequence_field] and not rec.name:
                rec.name = rec[rec._sequence_field]

    # DEPRECATED
    sequence_code = fields.Char(
        string="Sequence Code",
        copy=False,
        store=True,
    )
    sequence_number = fields.Char(
        string="No.",
        copy=False,
    )
