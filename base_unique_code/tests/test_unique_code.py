import logging

from odoo.tests.common import TransactionCase

_logger = logging.getLogger(__name__)


class TestUniqueCode(TransactionCase):

    @classmethod
    def _get_field(cls, model_id, field_name):
        return cls.env["ir.model.fields"].search(
            [("model_id", "=", model_id), ("name", "=", field_name)]
        ).ensure_one()

    def setUp(self):
        super().setUp()
        # Sequence must be reset to 1, otherwise the tests will fail
        sequence = self.env["ir.sequence"].create(
            [
                {
                    "name": "Test Partner Sequence",
                    "prefix": "partner-",
                    "padding": 5,
                    "number_increment": 1,
                }
            ]
        )
        self.model = self.env.ref("base.model_res_partner")
        self.model.unique_code_expression = "{__sequence__}"
        self.model.sequence_id = sequence.id

    def test_0_sequence(self):
        self.model.unique_code_expression = ""
        record = self.env[self.model.model].create({"name": "Test Partner"})
        self.assertEqual(record.unique_code, False)
        self.assertEqual(record.name, "Test Partner")

    def test_1_secuence(self):
        record = self.env[self.model.model].create({"name": "Test Partner"})
        self.assertEqual(record.unique_code, "partner-00001")
        record.unique_code = ""
        self.assertEqual(record.unique_code, "")
        record.set_sequence_code_unique_code_and_name()
        self.assertEqual(record.unique_code, "partner-00002")

    def test_no_change_of_existing_sequence_code(self):
        record = self.env[self.model.model].create({"name": "Test Partner"})
        self.assertEqual(record.unique_code, "partner-00001")
        record.set_sequence_code_unique_code_and_name()
        self.assertEqual(record.unique_code, "partner-00001")

    def test_no_name_get_next_sequence_code(self):
        # Contact name is mandatory except when type == "other"
        record = self.env[self.model.model].create({"type": "other"})
        self.assertEqual(record.name, "partner-00001")

    # From sequence_choice

    def test_1_count_sequences(self):
        Sequence = self.env["ir.sequence"]
        model = self.env.ref("base.model_res_lang")
        seq_count1 = Sequence.search_count([])
        model.unique_code_expression = "{__sequence__}"
        model.sequence_field_id = self._get_field(model.id, "direction").id
        seq_count2 = Sequence.search_count([])
        self.assertEqual(seq_count1 + 2, seq_count2, "Add 2 directions: ltr and rtl")

    def test_choice_boolean(self):
        model = self.env.ref("base.model_res_groups")
        model.unique_code_expression = "{__sequence__}"
        model.sequence_field_id = self._get_field(model.id, "share").id
        record = self.env[model.model].create(
            {"name": "Test Group", "share": False}
        )
        self.assertEqual(record.unique_code, "False-00001")
        record.unique_code = ""
        self.assertEqual(record.unique_code, "")
        record.set_sequence_code_unique_code_and_name()
        self.assertEqual(record.unique_code, "False-00002")

    def test_choice_many2one(self):
        model = self.env.ref("base.model_res_partner")
        model.sequence_field_id = self._get_field(model.id, "title").id
        title = self.env.ref("base.res_partner_title_madam")
        record = self.env[model.model].create(
            {"name": "Test Contact", "title": title.id}
        )
        self.assertEqual(record.ref, f"{title.id}-00001")
        record.ref = ""
        self.assertEqual(record.ref, "")
        record.set_sequence_code_unique_code_and_name()
        self.assertEqual(record.ref, f"{title.id}-00002")

    def test_choice_selection(self):
        model = self.env.ref("base.model_res_lang")
        model.unique_code_expression = "{__sequence__}"
        model.sequence_field_id = self._get_field(model.id, "direction").id
        record = self.env[model.model].create(
            {"name": "Test Language", "direction": "ltr", "code": "test"}
        )
        self.assertEqual(record.unique_code, "ltr-00001")
        record.unique_code = ""
        self.assertEqual(record.unique_code, "")
        record.set_sequence_code_unique_code_and_name()
        self.assertEqual(record.unique_code, "ltr-00002")


