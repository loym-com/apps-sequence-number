def post_init_hook(arg):
    cr = getattr(arg, "cr", None) or arg
    cr.execute("""
        UPDATE ir_model
        SET number_expression = '{r.sequence_code}'
        WHERE model in ('product.product', 'product.template')
            AND (number_expression IS NULL OR number_expression = '');
    """)
