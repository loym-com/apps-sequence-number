# Copyright (C) 2023 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase, tagged


class TestProductUniqueCode(TransactionCase):
    """Tests for creating product with and without product sequence_number"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_product = cls.env["product.product"]
        cls.product_template = cls.env["product.template"]
        cls.ir_model = cls.env["ir.model"].search([("model", "=", "product.product")])
        cls.ir_model_variant.number_expression = "P{id:0>5}"

    def test_product_product_creation(self):
        """Tests creating a new product and validating its unique Product Number.

        This test does the following:

        - Gets the next sequence number for unique Product Numbers.
        - Creates a new product.
        - Validates that the new product's sequence_number matches
          the expected next sequence number.

        Args:
            self (obj): The test class instance
        """

        product_1 = self.product_product.create({"name": "product 1"})
        id = str(product_1.id).zfill(5)  # Correct usage of zfill

        self.assertEqual(
            product_1.sequence_number,
            f"P{id}",
            "Product Number should match next sequence number",
        )

    def test_product_template(self):
        """Tests the product template's unique code sync with variants.

        This test does the following:

        - Creates a new product template
        - Checks the initial variant's code matches the template
        - Creates a second variant
        - Checks the template code does not change
        - Archives the initial variant
        - Checks the template code updates to match the active variant
        """

        self.env["ir.config_parameter"].sudo().set_param(
            "product_sequence_number.product_template_sequence_number_from_main_variant", "True"
        )

        # Create a product template
        template = self.product_template.create({"name": "Test Template"})
        # Check the related product
        related_product = template.product_variant_ids[0]
        self.assertTrue(related_product)
        # Check the related product's sequence_number
        #  is the same as the template's sequence_number
        self.assertEqual(
            template.sequence_number,
            related_product.sequence_number,
            "code should be the same",
        )
        # Create another related product.product.
        related_product_1 = self.product_product.create(
            {
                "name": "Test Product 1",
                "product_tmpl_id": template.id,
            }
        )
        self.assertTrue(related_product_1)
        # Check if the  template's sequence_number has not changed
        self.assertEqual(
            template.sequence_number,
            related_product.sequence_number,
            "code should not change",
        )
        # Archive the first related product.product.
        related_product.active = False
        # Check if the  template's sequence_number has changed
        self.assertEqual(
            template.sequence_number,
            related_product_1.sequence_number,
            "code should be equal to code of next active product.product",
        )
