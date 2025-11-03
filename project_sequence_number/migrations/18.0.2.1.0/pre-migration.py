def migrate(cr, version):
    cr.execute("""
UPDATE project_project
SET sequence_sequence = sequence_code;

UPDATE project_project
SET sequence_code = sequence_number;

UPDATE project_task
SET code = sequence_number;

    """)
