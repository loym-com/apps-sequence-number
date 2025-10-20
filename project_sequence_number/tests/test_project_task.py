# Copyright 2016 Tecnativa <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.tests.common as common


class TestProjectTask(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_model = cls.env["project.task"]
        cls.ir_sequence_model = cls.env["ir.sequence"]
        cls.task_sequence = cls.env["ir.sequence"].create(
            {
                "name": "Task code",
                "code": "project.task",
                "padding": 4,
                "prefix": "T",
                "company_id": False,
            }
        )
        cls.ir_model = cls.env["ir.model"].search([("model", "=", "project.task")])
        # cls.ir_model.display_name_expression = "[{r.sequence_number}] {name}"
        # cls.ir_model.number_expression = "{r.sequence_code}"
        cls.ir_model.number_sequence_option = "sequence"
        cls.ir_model.number_sequence_id = cls.task_sequence.id

    def setUp(self):
        super().setUp()
        self.task_sequence._get_current_sequence().number_next = 1

    def test_old_task_sequence_number_assign(self):
        tasks = self.task_model.search([])
        for task in tasks:
            self.assertNotEqual(task.sequence_number, "/")

    def test_new_task_sequence_number_assign(self):
        number_next = self.task_sequence.number_next_actual
        sequence_number = self.task_sequence.get_next_char(number_next)
        task = self.task_model.create(
            {
                "name": "Testing task sequence_number",
            }
        )
        self.assertNotEqual(task.sequence_number, "/")
        self.assertEqual(task.sequence_number, sequence_number)

    def test_name_get(self):
        number_next = self.task_sequence.number_next_actual
        sequence_number = self.task_sequence.get_next_char(number_next)
        task = self.task_model.create(
            {
                "name": "Task Testing Get Name",
            }
        )
        result = task.display_name
        self.assertEqual(result, f"[{task.sequence_number}] Task Testing Get Name")

    def test_name_search(self):
        task = self.env["project.task"].create(
            {"name": "Such Much Task", "sequence_number": "TEST-123"}
        )

        result = task.name_search("TEST-123")
        self.assertIn(
            task.id,
            map(lambda x: x[0], result),
            f"Task with sequence_number {task.sequence_number} should be in the results",
        )

        result = task.name_search("TEST")
        self.assertIn(
            task.id,
            map(lambda x: x[0], result),
            f"Task with sequence_number {task.sequence_number} should be in the results",
        )

        result = task.name_search("much")
        self.assertIn(
            task.id,
            map(lambda x: x[0], result),
            f"Task with sequence_number {task.sequence_number} should be in the results",
        )

        result = task.name_search("20232")
        self.assertNotIn(
            task.id,
            map(lambda x: x[0], result),
            f"Task with sequence_number {task.sequence_number} shouldn't be in the results",
        )
