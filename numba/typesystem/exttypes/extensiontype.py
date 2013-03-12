# -*- coding: utf-8 -*-

"""
Extension type types.
"""

from numba.minivect import minitypes

from numba.traits import traits, Delegate
from numba.typesystem import NumbaType

@traits
class ExtensionType(NumbaType, minitypes.ObjectType):
    """
    Extension type Numba type.

    Available to users through MyExtensionType.exttype (or
    numba.typeof(MyExtensionType).
    """

    is_extension = True
    is_final = False

    methoddict = Delegate('vtab_type')
    methodnames = Delegate('vtab_type')
    add_method = Delegate('vtab_type')

    attributedict = Delegate('attribute_table')
    attributes = Delegate('attribute_table')

    def __init__(self, py_class, **kwds):
        super(ExtensionType, self).__init__(**kwds)
        assert isinstance(py_class, type), ("Must be a new-style class "
                                            "(inherit from 'object')")
        self.name = py_class.__name__
        self.py_class = py_class

        self.symtab = {}  # attr_name -> attr_type

        self.compute_offsets(py_class)

        self.attribute_table = None
        self.vtab_type = None

        self.parent_attr_struct = None
        self.parent_vtab_type = None
        self.parent_type = getattr(py_class, "__numba_ext_type", None)

    def compute_offsets(self, py_class):
        from numba.exttypes import extension_types

        self.vtab_offset = extension_types.compute_vtab_offset(py_class)
        self.attr_offset = extension_types.compute_attrs_offset(py_class)

    def set_attributes(self, attribute_list):
        """
        Create the symbol table and attribute struct from a list of
        (varname, attribute_type)
        """
        import numba.symtab

        self.attribute_table = numba.struct(attribute_list)
        self.symtab.update([(name, numba.symtab.Variable(type))
                               for name, type in attribute_list])

# ______________________________________________________________________
# @jit

class JitExtensionType(ExtensionType):
    "Type for @jit extension types"

    is_jit_extension = True

    def __repr__(self):
        return "<JitExtension %s>" % self.name

    def __str__(self):
        if self.attribute_table:
            return "<JitExtension %s(%s)>" % (
                self.name, self.attribute_table.attributedict)
        return repr(self)

# ______________________________________________________________________
# @autojit

class AutojitExtensionType(ExtensionType):
    "Type for @autojit extension types"

    is_autojit_extension = True

    def __repr__(self):
        return "<AutojitExtension %s>" % self.name

    def __str__(self):
        if self.attribute_table:
            return "<AutojitExtension %s(%s)>" % (
                self.name, self.attribute_table.attributedict)
        return repr(self)
