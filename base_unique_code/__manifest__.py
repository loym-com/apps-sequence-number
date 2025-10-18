# Copyright 2025 Loym
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Base Unique Code",
    "summary": "Each record may have a unique code",
    "author": "Loym",
    "data": [
        "data/ir_actions_server_data.xml",
        "views/ir_model_views.xml",
        "views/res_partner_views.xml",
    ],
    "depends": [
        "base_setup",
        "compute_value_from_expression",
        "mail", # problem that the field "unique_code" exists everywhere
    ],
    "license": "LGPL-3",
    "pre_init_hook": "pre_init_hook",
    "version": "18.0.5.0.1",
    "website": "https://www.loym.com",
}
