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
        sequence = cls.env["ir.sequence"].create(
            [
                {
                    "name": "Test Partner Sequence",
                    "prefix": "partner-",
                    "padding": 5,
                    "number_increment": 1,
                }
            ]
        )
        cls.model = cls.env.ref("base.model_res_partner")
        cls.model.number_sequence_id = sequence.id

    def test_00_sequence(self):
        self.model.number_sequence_option = False
        record = self.env[self.model.model].create({"name": "Test Partner"})
        self.assertFalse(record.sequence_number)
        self.assertEqual(record.name, "Test Partner")

    def test_01_secuence_with_reset(self):
        self.model.number_sequence_option = "sequence"
        record = self.env[self.model.model].create({"name": "Test Partner"})
        self.assertEqual(record.sequence_number, "partner-00001")
        record.sequence_number = ""
        self.assertFalse(record.sequence_number)
        self.assertFalse(record.sequence_code)
        record.set_sequence_code_sequence_number_and_name()
        self.assertEqual(record.sequence_number, "partner-00002")

    def test_02_field_boolean_with_sequence_count(self):
        Sequence = self.env["ir.sequence"]
        seq_count1 = Sequence.search_count([])
        self.model.number_sequence_option = "field"
        self.model.number_sequence_field_id = self._get_field(self.model.id, "active").id
        record = self.env[self.model.model].create({"name": "Test Partner"})
        self.assertEqual(record.sequence_number, "True-00001")
        seq_count2 = Sequence.search_count([])
        self.assertEqual(seq_count2, seq_count1 + 2, "Active sequences: True and False")

    def test_03_field_many2one(self):
        self.model.number_sequence_option = "field"
        self.model.number_sequence_field_id = self._get_field(self.model.id, "company_id").id
        company = self.env.ref("base.main_company")
        record = self.env[self.model.model].create({"name": "Test Partner", "company_id": company.id})
        self.assertEqual(record.sequence_number, f"{company.id}-00001")

    def test_04_field_selection(self):
        self.model.number_sequence_option = "field"
        self.model.number_sequence_field_id = self._get_field(self.model.id, "company_type").id
        record = self.env[self.model.model].create({"name": "Test Partner", "company_type": "person"})
        self.assertEqual(record.sequence_number, "person-00001")

    def test_05_sequence_number_also_in_name_if_empty(self):
        self.model.number_sequence_option = "sequence"
        # Contact name is mandatory except when type == "other"
        record = self.env[self.model.model].create({"type": "other"})
        self.assertEqual(record.name, "partner-00003")

    def test_06_no_change_of_existing_sequence_number(self):
        self.model.number_sequence_option = "sequence"
        record = self.env[self.model.model].create({"name": "Test Partner"})
        self.assertEqual(record.sequence_number, "partner-00004")
        record.set_sequence_code_sequence_number_and_name()
        self.assertEqual(record.sequence_number, "partner-00004")
