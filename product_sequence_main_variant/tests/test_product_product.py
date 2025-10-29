from odoo.tests.common import TransactionCase


class TestProductProduct(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_product_model = cls.env["ir.model"].search([("model", "=", "product.product")])
        cls.product_product_model.sequence_expression = "P{r.id:0>5}"

    def test_product_product_creation(self):
        product_1 = self.env["product.product"].create({"name": "product 1"})
        id = str(product_1.id).zfill(5)
        self.assertEqual(
            product_1.sequence_number,
            f"P{id}",
            "Product No. does not match the id with 5 digits",
        )
