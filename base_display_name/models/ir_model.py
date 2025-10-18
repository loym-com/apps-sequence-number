# -*- coding: utf-8 -*-

import logging
import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.addons.expression_value.expression_value import ExpressionValue

_logger = logging.getLogger(__name__)


class IrModel(models.Model):
    _inherit = "ir.model"

    display_name_expression = fields.Char(
        string="Name Pattern",
        help=(
            "Example: '{parent_id.display_code}/{display_code} - {name}'\n"
            "Use python string format syntax.\n\n"
            "Conditions for displaying a record like the pattern:\n"
            "1. The field values are non-false (boolean field may be False)."
            "2. The name has a different value than the other fields.\n"
            "3. No other module will _compute_display_name()."
        ),
    )

    @api.constrains("display_name_expression")
    def _check_display_name_field_paths(self):
        for model in self:
            expr_value = ExpressionValue(
                source="ir.model",
                source_model=model._name,
                source_lookup="display_name_expression",
                record=model,
            )
            if not expr_value.all_paths_are_valid:
                raise ValidationError(
                    f"_check_display_name_field_paths: "
                    f"At least one field is not valid: {expr_value.field_paths}"
                )
