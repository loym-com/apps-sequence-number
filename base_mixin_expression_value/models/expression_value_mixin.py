import logging
import re

from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class ExpressionValueMixin(models.AbstractModel):
    _name = "expression.value.mixin"
    _description = "expression.value.mixin"

    def get_ir_model(self, prefetch_fields=True):
        IrModel = self.env["ir.model"].sudo()
        IrModel = IrModel.with_context(prefetch_fields=prefetch_fields)
        # To install apps without errors:
        # - Order by a field which always exists.
        return IrModel.search([("model", "=", self._name)], order="id")
    
    def get_value_from_source(self, source, lookup):
        expression = self.get_expression_from_source(source, lookup)
        return self.get_value_from_expression(expression)
    
    def get_field_paths_from_source(self, source, lookup):
        expression = self.get_expression_from_source(source, lookup)
        return self.get_field_paths_from_expression(expression)
    
    def raise_error_if_invalid_field_paths_from_source(self, source, lookup):
        expression = self.get_expression_from_source(source, lookup)
        field_paths = self.get_field_paths_from_expression(expression)
        self.raise_error_if_invalid_field_paths(field_paths)

    def get_expression_from_source(self, source, source_lookup):
        """
        Return: A user-defined string with a python expression.
        """
        # To install apps without errors:
        # - Do not prefetch fields.
        if source == "ir.model":
            ir_model = self.get_ir_model(prefetch_fields=False)
            return getattr(ir_model, source_lookup) or ""
        elif source == "ir.config_parameter":
            param = self.env["ir.config_parameter"].sudo().get_param(source_lookup)
            return param or ""

    def get_value_from_expression(self, expression):
        for record in self:
            try:
                value = safe_eval(f"f{repr(expression)}", {"r": record})
                if value in ("False"):
                    return None
                return value
            except Exception as e:
                _logger.warning("Error evaluating expression %r for %s(%d): %s", expression, record._name, record.id, e)

    @api.model
    def get_field_paths_from_expression(self, expression):
        """
        Use regular expression to get all field paths beginning with "r."
        return: tuple of field paths, without the "r."

        Example:
            expression: "{r.parent_id.name}/{r.name}"
            field_paths: set("parent_id.name", "name")
        """
        # 1️⃣ Match everything inside braces {}
        pattern = r"\{([^{}]+)\}"  # matches { … } contents
        placeholders = re.findall(pattern, expression)
        
        # 2️⃣ For each placeholder, find r.field.paths without r.
        r_path_pattern = r"r\.([a-zA-Z_][a-zA-Z0-9_\.]*)"
        field_paths = set()
        for placeholder in placeholders:
            found = re.findall(r_path_pattern, placeholder)
            field_paths.update(found)
        
        return field_paths

    @api.model
    def check_if_all_field_paths_are_valid(self, field_paths):
        """
        Return True if all paths exist on the model, False otherwise.
        """
        model = self.env[self._name]
        for path in field_paths:
            if not self._is_field_path_valid(model, path.split('.')):
                return False
        return True

    @api.model
    def get_valid_field_paths(self, field_paths):
        """
        Return only valid field paths from the input list.
        """
        model = self.env[self._name]
        valid_paths = [
            path for path in field_paths
            if self._is_field_path_valid(model, path.split('.'))
        ]
        return valid_paths

    def raise_error_if_invalid_field_paths(self, field_paths):
        valid = self.check_if_all_field_paths_are_valid(field_paths)
        if not valid:
            raise ValidationError(
                f"Not all field_paths are valid: {field_paths}"
            )

    @api.model
    def _is_field_path_valid(self, model, path_parts):
        """
        Recursive helper to check if a dotted field path exists on a model.
        """
        if not path_parts:
            return True
        field_name = path_parts[0]
        field = model._fields.get(field_name)
        if not field:
            return False
        # Follow relational fields
        if field.type in ('many2one', 'one2many', 'many2many'):
            rel_model = self.env[field.comodel_name]
            return self._is_field_path_valid(rel_model, path_parts[1:])
        elif len(path_parts) > 1:
            # Non-relational field cannot have further parts
            return False
        return True
