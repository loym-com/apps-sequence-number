Install a module where unique_code is implemented for a model.
(This module has implemented unique_code for Contacts.)

Activate debug mode.

Open the model (Contacts), and in the debug menu, go to Model (res.partner).

Or go to *Settings \> Technical \> Database Structure \> Models* and open the model.

There are three sequence options:

0. Do not use a sequence.

1. Use one sequence.
    - Create a sequence.

2. Choose sequence by a field.
    - Select a field. Possible field types: selection, boolean, many2one.
    - Save. A sequence will be auto-created for each possible field value.
    - Click the button with the list icon, to customize the sequences.

"No. Expression" defines how to generate "No." - by default "{sequence_code}".

https://www.geeksforgeeks.org/formatted-string-literals-f-strings-python/
