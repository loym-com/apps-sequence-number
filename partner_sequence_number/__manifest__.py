# Copyright 2025 Loym
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contact No.",
    "summary": "",
    "author": "FIQ, Loym",
    "data": [
        "data/ir_actions_server_data.xml",
        "data/ir_sequence.xml",
        "views/res_partner_views.xml",
    ],
    "depends": [
        "base_mixin_display_name",
        "base_mixin_sequence_number",
        # "base_setup",
    ],
    "license": "AGPL-3",
    "version": "18.0.2.0.0",
    "website": "https://www.loym.com",
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "pre_uninstall_hook",
}
