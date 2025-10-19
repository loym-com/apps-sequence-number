# Copyright 2025 Loym
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Contact No.",
    "summary": "",
    "author": "Loym",
    "data": [
        "data/ir_actions_server_data.xml",
        "views/ir_model_views.xml",
        "views/res_partner_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "depends": [
        "expression_value_mixin",
        "base_setup",
        "mail", # problem that the field "sequence_number" exists everywhere
    ],
    "license": "LGPL-3",
    "post_init_hook": "post_init_hook",
    "version": "18.0.5.0.1",
    "website": "https://www.loym.com",
}
