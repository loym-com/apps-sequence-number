def post_init_hook(env):
    lead_model = env["ir.model"].search([("model", "=", "crm.lead")])
    lead_model.write(
        {
            "use_display_name_expression": True,
            "display_name_expression": "{r.sequence_number + ' - ' if r.sequence_number and r.sequence_number != r.name else ''}{r.name}",
        }
    )

def pre_uninstall_hook(env):
    lead_model = env["ir.model"].search([("model", "=", "crm.lead")])
    lead_model.write(
        {
            "use_display_name_expression": False,
            "display_name_expression": "",
        }
    )
