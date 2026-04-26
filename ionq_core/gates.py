# Copyright 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0

"""Pure-Python unitary matrices for IonQ native trapped-ion gates.

All functions return nested tuples of complex numbers (no NumPy dependency).

**Parameter conventions:**

- Phase parameters (``phi``, ``phi0``, ``phi1``) are in **turns** -
  fractions of 2*pi. So ``phi=0.25`` means pi/2 radians.
- Interaction parameters (``angle``) are in **units of pi**. So
  ``angle=0.25`` means pi/4 radians.

**Type aliases:**

- `Matrix2x2` - ``tuple[tuple[complex, complex], tuple[complex, complex]]``
- `Matrix4x4` - 4x4 nested tuple of complex numbers

Example:
    ```python
    from ionq_core import gpi_matrix, gpi2_matrix, ms_matrix, zz_matrix

    gpi_matrix(0)  # Pauli X gate
    gpi2_matrix(0.25)  # pi/2 rotation about Y axis
    ms_matrix(0, 0)  # maximally-entangling MS gate
    zz_matrix(0.1)  # ZZ interaction
    ```
"""

import cmath
import math

Matrix2x2 = tuple[tuple[complex, complex], tuple[complex, complex]]
"""Type alias for a 2x2 unitary matrix (single-qubit gate)."""

Matrix4x4 = tuple[
    tuple[complex, complex, complex, complex],
    tuple[complex, complex, complex, complex],
    tuple[complex, complex, complex, complex],
    tuple[complex, complex, complex, complex],
]
"""Type alias for a 4x4 unitary matrix (two-qubit gate)."""

_2PI = 2 * math.pi


def gpi_matrix(phi: float) -> Matrix2x2:
    r"""Single-qubit GPI gate.

    Matrix form: ``[[0, e^{-i*2*pi*phi}], [e^{i*2*pi*phi}, 0]]``

    At ``phi=0`` this is the Pauli X gate.

    Args:
        phi: Phase angle in turns (fractions of 2*pi).

    Returns:
        A `Matrix2x2` unitary matrix.

    Examples:
        ```python
        >>> gpi_matrix(0)       # Pauli X
        ((0, (1+0j)), ((1+0j), 0))
        ```
    """
    e = cmath.exp(1j * _2PI * phi)
    return ((0, 1 / e), (e, 0))


def gpi2_matrix(phi: float) -> Matrix2x2:
    """Single-qubit GPI2 gate (pi/2 rotation about an axis in the XY plane).

    Args:
        phi: Phase angle in turns (fractions of 2*pi) defining the
            rotation axis in the XY plane.

    Returns:
        A `Matrix2x2` unitary matrix.
    """
    e = cmath.exp(1j * _2PI * phi)
    s = 1 / math.sqrt(2)
    return ((s, -1j * s / e), (-1j * s * e, s))


def ms_matrix(phi0: float, phi1: float, angle: float = 0.25) -> Matrix4x4:
    """Two-qubit Molmer-Sorensen (MS) gate.

    The default ``angle=0.25`` produces a maximally-entangling gate.

    Args:
        phi0: Frame rotation phase for qubit 0 in turns.
        phi1: Frame rotation phase for qubit 1 in turns.
        angle: Interaction angle in units of pi. Defaults to 0.25
            (i.e. pi/4 radians).

    Returns:
        A `Matrix4x4` unitary matrix.

    Examples:
        ```python
        >>> ms_matrix(0, 0)         # maximally-entangling MS gate
        >>> ms_matrix(0, 0, 0.125)  # partial entanglement
        ```
    """
    a = math.pi * angle
    ca, sa = math.cos(a), math.sin(a)
    ep = cmath.exp(1j * _2PI * (phi0 + phi1))
    em = cmath.exp(1j * _2PI * (phi0 - phi1))
    return (
        (ca, 0, 0, -1j * sa / ep),
        (0, ca, -1j * sa / em, 0),
        (0, -1j * sa * em, ca, 0),
        (-1j * sa * ep, 0, 0, ca),
    )


def zz_matrix(angle: float) -> Matrix4x4:
    """Two-qubit ZZ interaction gate.

    Diagonal matrix: ``diag(e^{-i*pi*a}, e^{i*pi*a}, e^{i*pi*a}, e^{-i*pi*a})``

    At ``angle=0`` this is the identity gate.

    Args:
        angle: Interaction angle in units of pi.

    Returns:
        A `Matrix4x4` unitary matrix.
    """
    em = cmath.exp(-1j * math.pi * angle)
    ep = cmath.exp(1j * math.pi * angle)
    return (
        (em, 0, 0, 0),
        (0, ep, 0, 0),
        (0, 0, ep, 0),
        (0, 0, 0, em),
    )
