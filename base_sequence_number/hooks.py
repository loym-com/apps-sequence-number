import logging

_logger = logging.getLogger(__name__)

def post_init_hook(arg):
    cr = getattr(arg, "cr", None) or arg
    cr.execute("""
        UPDATE ir_model
        SET number_expression = '{sequence_code}'
        WHERE model = 'res.partner'
          AND (number_expression IS NULL OR number_expression = '');
    """)

    _logger.info("Post-init hook completed: number_expression is {sequence_code} for contacts.")
