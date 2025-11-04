def migrate(cr, version):
        # if version < "19.0.5.0.0":
        cr.execute("""
            ALTER TABLE project_project
            ADD COLUMN IF NOT EXISTS sequence_sequence varchar,
            ADD COLUMN IF NOT EXISTS sequence_code varchar;
                   
            UPDATE project_project
            SET sequence_sequence = sequence_code,
                   sequence_code = unique_code
            WHERE unique_code IS NOT NULL;


            ALTER TABLE project_task
            ADD COLUMN IF NOT EXISTS code varchar;

            UPDATE project_task
            SET code = unique_code
            WHERE unique_code IS NOT NULL;

                   
            ALTER TABLE res_partner
            ADD COLUMN IF NOT EXISTS sequence_number varchar;
                   
            UPDATE res_partner
            SET sequence_number = unique_code
            WHERE unique_code IS NOT NULL;


            ALTER TABLE crm_lead
            ADD COLUMN IF NOT EXISTS sequence_number varchar;

            UPDATE crm_lead
            SET sequence_number = unique_code
            WHERE unique_code IS NOT NULL;


            ALTER TABLE product_template
            ADD COLUMN IF NOT EXISTS sequence_number varchar;

            UPDATE product_template
            SET sequence_number = unique_code
            WHERE unique_code IS NOT NULL;


            ALTER TABLE product_product
            ADD COLUMN IF NOT EXISTS sequence_number varchar;

            UPDATE product_product
            SET sequence_number = unique_code
            WHERE unique_code IS NOT NULL;

        """)
