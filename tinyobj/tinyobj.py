"""tinyobj main"""
from .fields import Field


class FieldParserMetaclass(type):
    """\
    FieldParserMetaclass moves instances of ``Field`` to the ``_fields``
    attribute on the class, preparing for actual values to be set in their
    place.
    """
    def __init__(self, name, parents, attrs):
        fields = {}
        for name, value in attrs.items():
            if isinstance(value, Field):
                fields[name] = value

        self._fields = fields


class TinyObj(object):
    """\
    TinyObj is the main superclass for objects which want to tie into the
    getters/setters/deserialization/serialization mechanism. Subclass TinyObj
    and provide a number of ``Field``s, like so::

        class User(TinyObj):
            username = UnicodeField()
            password = UnicodeField()
            active = BoolField(default=True)

            def __unicode__(self):
                return self.username

    Then just use the fields like Python objects (because they are.)::

        u = User(username='test', password='plaintext')
        assert u.username == 'test'
        assert u.password == 'plaintext'
        assert u.active == False
    """
    __metaclass__ = FieldParserMetaclass

    def __init__(self, *doc, **attrs):
        """\
        The expected usage pattern is to either pass a single dict or a number
        of attributes. You can do both, the attributes will take precedence.
        """
        source = {}
        for item in doc:
            source.update(item)
        source.update(attrs)

        for key in set(source.keys()) | set(self._fields.keys()):
            if key not in self._fields:
                value = source[key]
            elif key not in source:
                value = self._fields[key].initialize()
            else:
                value = self._fields[key].initialize(source[key])

            self.__dict__[key] = value

    def __repr__(self):
        if hasattr(self, '__unicode__'):
            return u'<{}: {}>'.format(self.__class__.__name__, unicode(self))
        else:
            return u'<{}>'.format(self.__class__.__name__)

    def to_dict(self):
        """return a dict of this object's fields"""
        return self.__dict__
