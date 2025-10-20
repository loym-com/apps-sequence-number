def pre_init_hook(arg):
    cr = getattr(arg, "cr", None) or arg
    try:
        cr.execute("""
            ALTER TABLE ir_model
            ADD COLUMN display_name_expression VARCHAR DEFAULT '';
        """)
    except Exception:
        pass
