========
Fields
========

Fields are the validation/cleaning mechanic of **tinyobj**. Each is responsible
for receiving a value (from the database, for example), cleaning it, and
returning the cleaned value. A reference to the original value is not kept at
this time, so reserializing the data for your specific use case is left as an
exercise to the reader.

The base object is ``Field``, of which ``TinyObj`` will detect subclasses to
use as fields:

.. autoclass:: tinyobj.fields.Field
   :members:

----------
Subclasses
----------

.. automodule:: tinyobj.fields
   :members: NumberField, BoolField, TextField, NoValidationField, DefaultField
