def post_init_hook(env):
    lead_model = env["ir.model"].search([("model", "=", "crm.lead")])
    lead_sequence = env.ref("crm_sequence_number.lead_sequence")
    lead_model.write(
        {
            "use_display_name_expression": True,
            "display_name_expression": "{r.sequence_number + ' - ' if r.sequence_number and r.sequence_number != r.name else ''}{r.name}",
            "number_expression": "{r.sequence_code}",
            "number_sequence_option": "sequence",
            "number_sequence_id": lead_sequence,
        }
    )

def pre_uninstall_hook(env):
    lead_model = env["ir.model"].search([("model", "=", "crm.lead")])
    lead_model.write(
        {
            "use_display_name_expression": False,
            "display_name_expression": "",
            "number_expression": "",
            "number_sequence_option": "",
            "number_sequence_id": False,
        }
    )
