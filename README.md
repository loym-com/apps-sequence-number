Sequences
=========

`base_mixin_expression_value` has `expression.value.mixin` used by `base_display_name`.

`base_display_name` is a base module to compute `display_name` with a python expression.

`base_mixin_sequence_number` is a base module to compute `sequence_number` with a python expression.

A record number may contain:

- Sequence
    - Option: Choose sequence based on the value of a field.
    - Install `sequence_python` for more options on the sequence.
- Values of the record or related records
- Anything that python can evaluate

Implementations:

- `crm_sequence_number`: Lead/Opportunity
- `partner_sequence_number`: Contact
- `product_sequence_number`: Product, Product Variant
- `project_sequence_number`: Project, Task

There are many OCA sequence modules on a supported version (16-18):

1. account_analytic_sequence
2. account_journal_general_sequence
3. account_move_name_sequence
4. account_number_sequence_option
5. base_partner_sequence
6. base_sequence_default
7. base_number_sequence_option
8. hr_expense_advance_clearing_sequence
9. hr_expense_sequence
10. hr_expense_number_sequence_option
11. l10n_th_base_sequence
12. maintenance_equipment_sequence
13. maintenance_request_sequence
14. mrp_workorder_sequence
15. product_default_code_res_company_code
16. product_internal_reference_generator
17. product_lot_sequence
18. product_sequence
19. project_task_code
20. purchase_order_line_sequence
21. repair_type_sequence
22. sale_order_line_sequence
23. sale_quotation_number
24. sale_stock_line_sequence
25. sequence_check_digit
26. sequence_python
27. sequence_reset_period
28. stock_picking_line_sequence

On migrating to 19.0, please consider to rename to `MODULE_sequence_number` and depend on `base_sequence_number`.

[Here I have opened an issue to discuss these things](https://github.com/OCA/server-ux/issues/1058).

