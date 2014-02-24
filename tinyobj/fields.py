"""**tinyobj** implements a number of fields to do validation, etc."""
from . import _compat


class Field(object):
    """base for other fields"""
    def __init__(self):
        self.default = None

    def initialize(self, value=()):
        """\
        initialize returns a cleaned value or the default, raising ValueErrors
        as necessary.
        """
        if value == ():
            try:
                return self.default()
            except TypeError:
                return self.default
        else:
            return self.clean(value)

    def clean(self, value):
        """clean a value, returning the cleaned value"""
        raise NotImplementedError


class NumberField(Field):
    """accept and validate numbers

    takes a type to convert values to, can be (EG) ``float``, ``int``,
    ``long``, or ``complex``.
    """
    def __init__(self, t=float, allow_negative=True, allow_positive=True):
        self.t = t
        self.default = t()
        self.allow_negative = allow_negative
        self.allow_positive = allow_positive

    def clean(self, value):
        """clean a value, converting and performing bounds checking"""
        if not isinstance(value, self.t):
            value = self.t(value)

        if not self.allow_negative and value < 0:
            raise ValueError('value was negative')

        if not self.allow_positive and value > 0:
            raise ValueError('values was positive')

        return value


class BoolField(Field):
    """accept and validate boolean values

    note that this field will just call ``bool`` on values, this may not be
    your desired behavior so you might want to implement a subclass that parses
    truthy/falsey values in a way specific to your application
    """
    def __init__(self, default=False):
        self.clean = bool
        self.default = bool(default)


class TextField(Field):
    """accept and validate text.

    Uses the Python implementation's appropriate unicode value (IE ``unicode``
    on 2.x and ``str`` on 3.x)
    """
    def __init__(self):
        self.default = _compat.text_type
        self.clean = _compat.text_type


class NoValidationField(Field):
    """\
    doesn't validate at all, but returns the value passed (defaulting to None)
    """
    def initialize(self, value=None):
        return value
