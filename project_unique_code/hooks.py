def post_init_hook(env):
    # Default project display name pattern
    pattern = "{r.unique_code}{' ' if r.unique_code != r.name else ''}{r.name if r.unique_code != r.name else ''}"
    env["ir.model"].search([("model", "=", "project.project")]).display_name_expression = pattern
