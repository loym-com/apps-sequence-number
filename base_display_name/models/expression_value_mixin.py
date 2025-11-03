import logging

from odoo import api, models
from odoo.osv import expression
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class ExpressionValueMixin(models.AbstractModel):
    _inherit = "expression.value.mixin"

    @api.model
    def _search_display_name(self, operator, value):
        # self._rec_names_search is readonly, so we need to work with search_fnames.
        search_fnames = self.get_valid_field_paths_from_source("ir.model", "display_name_expression")
        if not search_fnames:
            return super()._search_display_name(operator, value)

        # Copied from ORM models.py
        if operator.endswith('like') and not value and '=' not in operator:
            # optimize out the default criterion of ``like ''`` that matches everything
            # return all when operator is positive
            return expression.FALSE_DOMAIN if operator in expression.NEGATIVE_TERM_OPERATORS else expression.TRUE_DOMAIN
        aggregator = expression.AND if operator in expression.NEGATIVE_TERM_OPERATORS else expression.OR
        return aggregator([[(field_name, operator, value)] for field_name in search_fnames])

    @api.depends(lambda self: self.get_valid_field_paths_from_source("ir.model", "display_name_expression"))
    def _compute_display_name(self):
        """
        If display_name is stored, restart Odoo after changing display_name_expression.
        """
        expression = self.get_expression_from_source("ir.model", "display_name_expression")
        if expression:
            for rec in self:
                rec.display_name = rec.get_value_from_expression(expression)
        else:
            return super()._compute_display_name()
