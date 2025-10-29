from odoo.tests.common import TransactionCase


class TestProductTemplate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_product_model = cls.env["ir.model"].search([("model", "=", "product.product")])
        cls.product_product_model.sequence_expression = "P{r.id:0>5}"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_product_model = cls.env["ir.model"].search([("model", "=", "product.product")])

    def test_product_template_param_false(self):
        template = self.env["product.template"].create({"name": "Test Template"})
        self.assertFalse(template.sequence_number)
    
    def test_product_template_param_true(self):
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
            "product_main_variant.product_template_sequence_number_from_main_variant", "True"
        )

        # Create a product template
        template = self.env["product.template"].create({"name": "Test Template"})
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
        related_product_1 = self.env["product.product"].create(
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
