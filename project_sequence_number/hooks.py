def post_init_hook(env):
    project_model = env["ir.model"].search([("model", "=", "project.project")])
    project_sequence = env.ref("project_sequence_number.project_sequence")
    project_model.write(
        {
            "use_display_name_expression": True,
            "display_name_expression": "{r.sequence_number + ' - ' if r.sequence_number and r.sequence_number != r.name else ''}{r.name}",
            "number_expression": "{r.sequence_code}",
            "number_sequence_option": "sequence",
            "number_sequence_id": project_sequence,
        }
    )
    task_model = env["ir.model"].search([("model", "=", "project.task")])
    task_sequence = env.ref("project_sequence_number.task_sequence")
    task_model.write(
        {
            "use_display_name_expression": True,
            "display_name_expression": "[{r.sequence_number}] {r.name}",
            "display_name_expression": "{'[' + r.sequence_number + '] ' if r.sequence_number and r.sequence_number != r.name else ''}{r.name}",
            "number_expression": "{r.sequence_code}",
            "number_sequence_option": "sequence",
            "number_sequence_id": task_sequence,
        }
    )


def pre_uninstall_hook(env):
    project_model = env["ir.model"].search([("model", "=", "project.project")])
    project_model.write(
        {
            "use_display_name_expression": False,
            "display_name_expression": "",
            "number_expression": "",
            "number_sequence_option": "",
            "number_sequence_id": False,
        }
    )
    task_model = env["ir.model"].search([("model", "=", "project.task")])
    task_model.write(
        {
            "use_display_name_expression": False,
            "display_name_expression": "",
            "number_expression": "",
            "number_sequence_option": "",
            "number_sequence_id": False,
        }
    )
