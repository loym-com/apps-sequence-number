def post_init_hook(env):
    project_model = env["ir.model"].search([("model", "=", "project.project")])
    project_model.write(
        {
            "use_display_name_expression": True,
            "display_name_expression": "{r.sequence_code + ' - ' if r.sequence_code and r.sequence_code != r.name else ''}{r.name}",
        }
    )
    task_model = env["ir.model"].search([("model", "=", "project.task")])
    task_model.write(
        {
            "use_display_name_expression": True,
            "display_name_expression": "{'[' + r.code + '] ' if r.code and r.code != r.name else ''}{r.name}",
        }
    )


def pre_uninstall_hook(env):
    project_model = env["ir.model"].search([("model", "=", "project.project")])
    project_model.write(
        {
            "use_display_name_expression": False,
            "display_name_expression": "",
        }
    )
    task_model = env["ir.model"].search([("model", "=", "project.task")])
    task_model.write(
        {
            "use_display_name_expression": False,
            "display_name_expression": "",
        }
    )
