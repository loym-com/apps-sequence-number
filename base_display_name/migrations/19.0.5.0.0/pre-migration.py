def migrate(cr, version):
        # if version < "19.0.5.0.0":
        cr.execute("""
            ALTER TABLE ir_model
            ADD COLUMN IF NOT EXISTS display_name_expression varchar;

            UPDATE ir_model
            SET
                display_name_expression = display_name_pattern;
        """)
