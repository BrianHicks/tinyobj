"""
Tests for `tinyobj` module.
"""
import pytest

from tinyobj import fields
from tinyobj import _compat

class TestField(object):
    def test_initialize(self):
        ins = fields.Field()
        ins.default = "TEST"

        assert ins.initialize() == ins.default

    def test_initialize_func(self):
        ins = fields.Field()
        ins.default = lambda: "TEST"

        assert ins.initialize() == ins.default()

    def test_clean_not_implemented(self):
        ins = fields.Field()

        with pytest.raises(NotImplementedError):
            ins.clean(None)


class TestNumberField(object):
    def test_clean_converts(self):
        ins = fields.NumberField()

        assert ins.clean(0) == ins.t(0)

    def test_clean_checks_negative(self):
        ins = fields.NumberField(allow_negative=False)

        with pytest.raises(ValueError):
            ins.clean(-1)

    def test_clean_checks_positive(self):
        ins = fields.NumberField(allow_positive=False)

        with pytest.raises(ValueError):
            ins.clean(1)


class TestBoolField(object):
    def test_default(self):
        ins = fields.BoolField()

        assert ins.initialize() == bool()

    def test_clean(self):
        ins = fields.BoolField()

        assert ins.clean("test") == bool("test")


class TestTextField(object):
    def test_default(self):
        ins = fields.TextField()

        assert ins.initialize() == _compat.text_type()

    def test_clean(self):
        ins = fields.TextField()

        assert ins.clean("asdf") == _compat.text_type("asdf")


@pytest.mark.parametrize("value", [
    -1, 0, 1, 1.0,            # numeric
    True, False,              # boolean
    "a",                      # string
    [], {}, set(),            # container
    type("a", tuple(), {})(), # class instances
])
def test_no_validation(value):
    ins = fields.NoValidationField()

    assert ins.initialize(value) == value
