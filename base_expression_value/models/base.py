from odoo import models


class Base(models.AbstractModel):
    _inherit = "base"

    def get_ir_model(self, prefetch_fields=True):
        if not self:
            raise ValueError("Missing self")
        IrModel = self.env["ir.model"].sudo()
        IrModel = IrModel.with_context(prefetch_fields=prefetch_fields)
        # To install apps without errors:
        # - Order by a field which always exists.
        return IrModel.search([("model", "=", self._name)], order="id")
