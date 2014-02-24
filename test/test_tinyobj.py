"""
Tests for `tinyobj` module.
"""
import pytest

from tinyobj import tinyobj, fields

class TestFieldParserMetaclass(object):
    def test_moves(self):
        attrs = {
            'test': 1,
            'name': fields.Field()
        }
        obj = tinyobj.FieldParserMetaclass('test', (object,), attrs)

        assert hasattr(obj, '_fields')
        assert 'name' in obj._fields


class TestTinyObj(object):
    @classmethod
    def setup_class(cls):
        cls.user = type(
            'User',
            (tinyobj.TinyObj,),
            {
                'name': fields.TextField(),
                'password': fields.TextField(),
                'active': fields.BoolField(),
            }
        )
        cls.name = 'test'
        cls.password = 'pass'
        cls.active = True
        cls.record = {
            'name': cls.name,
            'password': cls.password,
            'active': cls.active,
        }

    def test_doc_arg(self):
        obj = self.user(self.record)

        assert obj.name == self.name
        assert obj.password == self.password
        assert obj.active == self.active

    def test_doc_kwargs(self):
        obj = self.user(**self.record)

        assert obj.name == self.name
        assert obj.password == self.password
        assert obj.active == self.active

    def test_to_dict(self):
        obj = self.user(self.record)

        assert obj.to_dict() == self.record
