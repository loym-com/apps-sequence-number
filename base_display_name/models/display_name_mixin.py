import logging
import psycopg2
import re

from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class DisplayNameMixin(models.AbstractModel):
    _name = "display.name.mixin"
    _description = "display.name.mixin"

    # display_name

    @api.model
    def _search_display_name(self, operator, value):
        search_fnames = self._get_display_field_paths("display_name_pattern", source="ir.model")
        if not search_fnames:
            return super()._search_display_name(operator, value)

        # Copied from ORM models.py
        if operator.endswith('like') and not value and '=' not in operator:
            # optimize out the default criterion of ``like ''`` that matches everything
            # return all when operator is positive
            return expression.FALSE_DOMAIN if operator in expression.NEGATIVE_TERM_OPERATORS else expression.TRUE_DOMAIN
        aggregator = expression.AND if operator in expression.NEGATIVE_TERM_OPERATORS else expression.OR
        return aggregator([[(field_name, operator, value)] for field_name in search_fnames])
    
    @api.depends(lambda self: self._get_display_field_paths("display_name_pattern", source="ir.model"))
    def _compute_display_name(self):
        super()._compute_display_name()
        self._set_field_from_pattern_name("display_name", "display_name_pattern", "ir.model")






