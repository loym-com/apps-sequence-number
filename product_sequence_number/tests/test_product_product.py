from odoo.tests.common import TransactionCase


class TestProductProduct(TransactionCase):

    def test_product_product_creation(self):
        product_1 = self.env["product.product"].create({"name": "product 1"})
        id = str(product_1.id).zfill(5)
        self.assertEqual(
            product_1.sequence_number, "1",
        )
