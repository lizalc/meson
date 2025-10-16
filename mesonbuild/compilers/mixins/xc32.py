# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

"""Provides mixins for the Microchip XC32 compiler family."""

import typing as T

from ... import mesonlib
from ...linkers.linkers import Xc32DynamicLinker
from ...options import OptionKey

if T.TYPE_CHECKING:
    from ...environment import Environment
    from ..compilers import Compiler
else:
    # This is a bit clever, for mypy we pretend that these mixins descend from
    # Compiler, so we get all of the methods and attributes defined for us, but
    # for runtime we make them descend from object (which all classes normally
    # do). This gives up DRYer type checking, with no runtime impact
    Compiler = object


class Xc32Compiler(Compiler):

    """Microchip XC32 compiler. GCC based with some options disabled."""

    id = 'xc32-gcc'

    def __init__(self) -> None:
        print(self.base_options)
        if not self.is_cross:
            raise mesonlib.EnvironmentException("XC32 supports only cross-compilation.")
        # Check whether 'xc32-ld' is available in path
        if not isinstance(self.linker, Xc32DynamicLinker):
            raise mesonlib.EnvironmentException(f'Unsupported Linker {self.linker.exelist}, must be xc32-ld')
        if not mesonlib.version_compare(self.version, '==' + self.linker.version):
            raise mesonlib.EnvironmentException('xc32-ld version does not match with compiler version')
        self.base_options = {OptionKey(o) for o in ['b_asneeded', 'b_colorout', 'b_lto', 'b_ndebug', 'b_pch']}
        # Assembly
        self.can_compile_suffixes.add('s')
        self.can_compile_suffixes.add('sx')
        print(self.base_options)

    def get_pic_args(self) -> T.List[str]:
        return []

    def get_pie_args(self) -> T.List[str]:
        return []

    def openmp_flags(self, env: Environment) -> T.List[str]:
        return []

    def get_profile_generate_args(self) -> T.List[str]:
        return []

    def get_profile_use_args(self) -> T.List[str]:
        return []

    def sanitizer_compile_args(self, value: T.List[str]) -> T.List[str]:
        return []

    def sanitizer_link_args(self, value: T.List[str]) -> T.List[str]:
        return []

    def get_prelink_args(self, prelink_name: str, obj_list: T.List[str]) -> T.Tuple[T.List[str], T.List[str]]:
        return Compiler.get_prelink_args(self, prelink_name, obj_list)

    def get_prelink_append_compile_args(self) -> bool:
        return Compiler.get_prelink_append_compile_args(self)

    @classmethod
    def use_linker_args(cls, linker: str, version: str) -> T.List[str]:
        return []

    def get_coverage_args(self) -> T.List[str]:
        return []
