import logging
import re

from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class ComputeValueFromExpression(object):
    """
    The purpose of this class is to compute a value,
    based on a user-defined python expression
    stored in "ir.config_parameter" or "ir.model".

    source: "ir.config_parameter" or "ir.model"
    source_model: name of model (if source is "ir.model")
    source_lookup: name of ir.config_parameter key or ir.model field

    record:
        To get the expression: Any odoo record (to et the environment)
        To compute the value: The odoo record that will use the value

    expression:
        String to compute a value with safe_eval.
        The record is passed to safe_eval as "r".
        Template examples:
            "{r.id:0>5}"            # 00001
            "{r.date:%Y-%m-%d}"     # 2025-12-31
            "{r.parent_id.name}"
            "{'active' if r.active else 'archived'}"
            "{r.first_name} {r.last_name}"
    """
    source = str()
    source_model = str()
    source_lookup = str()
    record = object()
    field = str()
    expression = str()

    field_paths = tuple()
    all_paths_are_valid = bool()
    value = str()

    def __init__(
            self,
            source: str | None = None,
            source_model: str | None = None,
            source_lookup: str | None = None,
            record: object | None = None,
            field: str | None = None,
            expression: str | None = None,
        ):
        self.source = source
        self.source_model = source_model
        self.source_lookup = source_lookup
        self.record = record
        self.field = field
        self.expression = expression

        if self.source:
            if self.source not in ["ir.model", "ir.config_parameter"]:
                raise ValueError(f"Invalid source: {self.source}")
            if self.source == "ir.model" and not self.source_model:
                raise ValueError("`model` is required when source='ir.model'.")
            if self.source == "ir.config_parameter" and self.source_model:
                raise ValueError("`model` must be empty when source='ir.config_parameter'.")

        if self.source and self.source_lookup and self.record and not self.expression:
            self.expression = self.get_expression()

        if self.expression:
            self.field_paths = self.get_field_paths()

        if self.record and self.field_paths:
            self.all_paths_are_valid = self.get_all_paths_are_valid()

        if self.expression and self.record:
            self.value = self.get_value()

        if self.record and self.field and self.value:
            self.update_record_field()

    def get_ir_model(self, prefetch_fields=True):
        if not self.record:
            raise ValueError("Missing self.record")
        IrModel = self.record.env["ir.model"].sudo()
        IrModel = IrModel.with_context(prefetch_fields=prefetch_fields)
        # To install apps without errors:
        # - Order by a field which always exists.
        return IrModel.search([("model", "=", self.record._name)], order="id")

    def get_expression(self):
        """
        Return: A user-defined string with a python expression.
        """
        # To install apps without errors:
        # - Do not prefetch fields.
        if self.source == "ir.model":
            ir_model = self.get_ir_model(prefetch_fields=False)
            return getattr(ir_model, self.source_lookup) or ""
        elif self.source == "ir.config_parameter":
            param = self.record.env["ir.config_parameter"].sudo().get_param(self.source_lookup)
            return param or ""

    def get_field_paths(self):
        """
        Use regular expression to get all field paths beginning with "r."
        return: tuple of field paths, without the "r."

        Example:
            expression: "{r.parent_id.name}/{r.name}"
            field_paths: set("parent_id.name", "name")
        """
        # 1️⃣ Match everything inside braces {}
        pattern = r"\{([^{}]+)\}"  # matches { … } contents
        placeholders = re.findall(pattern, self.expression)
        
        # 2️⃣ For each placeholder, find r.field.paths without r.
        r_path_pattern = r"r\.([a-zA-Z_][a-zA-Z0-9_\.]*)"
        field_paths = set()
        for placeholder in placeholders:
            found = re.findall(r_path_pattern, placeholder)
            field_paths.update(found)
        
        return field_paths

    def get_all_paths_are_valid(self):

        def get_value_and_type(field_path):
            """
            record: 0-1 records
            field_path may use dot notation, e.g. related_id.field"
            return: (value, value_type)
            """
            fields = field_path.split(".")
            if fields and fields[0] == "r":
                fields = fields[1:]
            model = self.record
            value = self.record
            for field in fields:
                if field in model._fields:
                    value_type = model._fields.get(field).type
                    value = getattr(value, field)
                    model = value
                else:
                    return (None, None)
            return (value, value_type)

        tuples = [
            get_value_and_type(field_path)
            for field_path in self.field_paths
        ]
        if (None, None) in tuples:
            return False
        else:
            return True

    def get_value(self):
        try:
            return safe_eval(f"f{repr(self.expression)}", {"r": self.record})
        except Exception as e:
            _logger.warning("Error evaluating expression %r for %s(%d): %s", self.expression, self.record._name, self.record.id, e)

    def update_record_field(self):

        # # Skip if value exists in stored field
        # if record._fields[field].store and getattr(record, field):
        #     return

        # Set value
        if self.value:
            setattr(self.record, self.field, self.value)
