import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestResPartner(TransactionCase):

    @classmethod
    def _get_field(cls, model_id, field_name):
        return cls.env["ir.model.fields"].search(
            [("model_id", "=", model_id), ("name", "=", field_name)]
        ).ensure_one()

    @classmethod
    def setUpClass(cls):
        """
        setUp is used instead of seUpClass,
        because the sequence must be reset to 1,
        otherwie the tests will fail.
        """
        super().setUpClass()
        cls.sequence = cls.env['ir.sequence'].search(
            [('code', '=', "res.partner"), '|', ('company_id', '=', cls.env.company.id), ('company_id', '=', False)],
            order='company_id desc',  # company-specific first, then global
            limit=1
        )
        cls.sequence.write(
            {
                "prefix": "partner-",
                "padding": 5,
                "number_next_actual": 1,
            }
        )

    def test_01_secuence_with_reset(self):
        record = self.env["res.partner"].create({"name": "Test Partner"})
        self.assertEqual(record.sequence_number, "partner-00001")
        record.sequence_number = ""
        self.assertFalse(record.sequence_number)
        record.set_sequence_field_and_name()
        self.assertEqual(record.sequence_number, "partner-00002")

    def test_05_sequence_number_also_in_name_if_empty(self):
        # Contact name is mandatory except when type == "other"
        record = self.env["res.partner"].create({"type": "other"})
        self.assertEqual(record.name, "partner-00003")

    def test_06_no_change_of_existing_sequence_number(self):
        record = self.env["res.partner"].create({"name": "Test Partner"})
        self.assertEqual(record.sequence_number, "partner-00004")
        record.set_sequence_field_and_name()
        self.assertEqual(record.sequence_number, "partner-00004")
