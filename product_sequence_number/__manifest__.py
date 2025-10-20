# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product No.",
    "summary": " ",
    "version": "18.0.1.0.0",
    "author": "FIQ, Cetmix, Loym",
    "website": "https://www.loym.com",
    "license": "AGPL-3",
    "category": "Product",
    "depends": [
        "base_mixin_sequence_number",
        "product",
    ],
    "data": [
        "data/ir_actions_server_data.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "post_init_hook": "post_init_hook",
}
