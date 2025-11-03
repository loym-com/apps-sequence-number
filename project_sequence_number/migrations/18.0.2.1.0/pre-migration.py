def migrate(cr, version):
    if version < "18.0.2.0.1":
        cr.execute("""
            ALTER TABLE project_project
            ADD COLUMN IF NOT EXISTS sequence_sequence varchar,
            ADD COLUMN IF NOT EXISTS sequence_code varchar;

            ALTER TABLE project_task
            ADD COLUMN IF NOT EXISTS code varchar;

            UPDATE project_project
            SET sequence_sequence = sequence_code,
                sequence_code = sequence_number;

            UPDATE project_task
            SET code = sequence_number;
        """)
