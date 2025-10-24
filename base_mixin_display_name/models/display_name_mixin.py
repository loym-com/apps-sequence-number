import logging

from odoo import api, models
from odoo.osv import expression
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class DisplayNameMixin(models.AbstractModel):
    _name = "display.name.mixin"
    _description = "display.name.mixin"
    _inherit = "expression.value.mixin"

    # display_name

    @api.model
    def _search_display_name(self, operator, value):
        search_fnames = self.get_field_paths_from_source("ir.model", "display_name_expression")
        if not search_fnames:
            return super()._search_display_name(operator, value)

        # Copied from ORM models.py
        if operator.endswith('like') and not value and '=' not in operator:
            # optimize out the default criterion of ``like ''`` that matches everything
            # return all when operator is positive
            return expression.FALSE_DOMAIN if operator in expression.NEGATIVE_TERM_OPERATORS else expression.TRUE_DOMAIN
        aggregator = expression.AND if operator in expression.NEGATIVE_TERM_OPERATORS else expression.OR
        return aggregator([[(field_name, operator, value)] for field_name in search_fnames])
    
    @api.depends(lambda self: self.get_field_paths_from_source("ir.model", "display_name_expression"))
    def _compute_display_name(self):
        super()._compute_display_name()
        expression = self.get_expression_from_source("ir.model", "display_name_expression")
        if expression:
            # TODO: Find out if safe_eval slows down the performance
            self.display_name = self.get_value_from_expression(expression)
