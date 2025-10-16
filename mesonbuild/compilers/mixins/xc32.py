# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from mesonbuild.environment import Environment

"""Provides mixins for the Microchip XC32 compiler family."""

import typing as T

from ... import mesonlib
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

    def __init__(self) -> None:
        if not self.is_cross:
            raise mesonlib.EnvironmentException("XC32 supports only cross-compilation.")

        self.base_options.difference_update({
            OptionKey(o) for o in ['b_pgo', 'b_coverage', 'b_staticpic', 'b_pie',
                                   'b_sanitize']})

    def get_instruction_set_args(self, instruction_set: str) -> T.List[str] | None:
        return None

    def thread_flags(self, env: Environment) -> T.List[str]:
        return []

    def openmp_flags(self, env: Environment) -> T.List[str]:
        raise mesonlib.EnvironmentException(f'{self.id} does not support OpenMP flags.')

    def get_pic_args(self) -> T.List[str]:
        raise mesonlib.EnvironmentException(f'{self.id} does not support position-independent code')

    def get_pie_args(self) -> T.List[str]:
        raise mesonlib.EnvironmentException(f'{self.id} does not support position-independent executable')

    def get_profile_generate_args(self) -> T.List[str]:
        raise mesonlib.EnvironmentException(f'{self.id} does not support get_profile_generate_args')

    def get_profile_use_args(self) -> T.List[str]:
        raise mesonlib.EnvironmentException(f'{self.id} does not support get_profile_use_args')

    def sanitizer_compile_args(self, value: T.List[str]) -> T.List[str]:
        return []

    @classmethod
    def use_linker_args(cls, linker: str, version: str) -> T.List[str]:
        return []

    def get_coverage_args(self) -> T.List[str]:
        return []

    def get_largefile_args(self) -> T.List[str]:
        return []

    def get_prelink_args(self, prelink_name: str, obj_list: T.List[str]) -> T.Tuple[T.List[str], T.List[str]]:
        raise mesonlib.EnvironmentException(f"{self.id} does not know how to do prelinking.")

    def get_prelink_append_compile_args(self) -> bool:
        return False
