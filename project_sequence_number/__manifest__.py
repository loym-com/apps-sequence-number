# Copyright 2025 Loym
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project/Task No.",
    "summary": "",
    "author": "FIQ, Loym",
    "data": [
        "data/ir_actions_server_data.xml",
        "data/ir_sequence.xml",
        "views/project_project_views.xml",
        "views/project_task_views.xml",
    ],
    "depends": [
        "base_display_name",
        "base_mixin_sequence_number",
        "project",
    ],
    "excludes": [""],
    "license": "AGPL-3",
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "pre_uninstall_hook",
    "version": "19.0.5.0.2",
    "website": "https://www.loym.com",
}
