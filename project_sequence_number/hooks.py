def post_init_hook(env):
    # Default project display name pattern
    pattern = "{r.sequence_number}{' ' if r.sequence_number != r.name else ''}{r.name if r.sequence_number != r.name else ''}"
    env["ir.model"].search([("model", "=", "project.project")]).display_name_expression = pattern
