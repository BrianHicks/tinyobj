========
Usage
========

Say you have a dictionary that looks sort of like this::

    {
        'username': 'rabbit',
        'password': 'some-hash',
        'active': True
    }

you'd define a schema like so::

	from tinyobj import TinyObj, fields

    class User(TinyObj):
        username = fields.TextField()
        password = fields.TextField()
        active = fields.BoolField()

and then initialize it::

    user = User(username='rabbit', password='some-hash', active=True)

    # or

    user = User(doc_from_db)

    assert user.username == 'rabbit'
    assert user.password == 'some-hash'
    assert user.active == True

You can get a dictionary of fields back (for saving) with ``to_dict``::

    assert user.to_dict() == doc_from_db
