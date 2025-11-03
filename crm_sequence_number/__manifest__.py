# Copyright (C) 2025 Loym
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


{
    "name": "Lead/Opportunity No.",
    "version": "18.0.2.0.0",
    "author": "FIQ, Loym",
    "website": "https://www.loym.com",
    "license": "LGPL-3",
    "category": "",
    "depends": [
        "base_display_name",
        "base_mixin_sequence_number",
        "crm",
    ],
    "data": [
        "data/ir_actions_server_data.xml",
        "data/ir_sequence.xml",
        "views/crm_lead_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "pre_uninstall_hook",
}
