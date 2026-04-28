# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from typing import Literal, cast

GetCompiledFileLang = Literal['native', 'qasm3']

GET_COMPILED_FILE_LANG_VALUES: set[GetCompiledFileLang] = { 'native', 'qasm3',  }

def check_get_compiled_file_lang(value: str) -> GetCompiledFileLang:
    if value in GET_COMPILED_FILE_LANG_VALUES:
        return cast(GetCompiledFileLang, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_COMPILED_FILE_LANG_VALUES!r}")
