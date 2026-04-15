"""Pure-Python unitary matrices for IonQ native gates.

Phase parameters (phi, phi0, phi1) are in turns (fractions of 2*pi).
Interaction parameters (angle) are in units of pi (0.25 = pi/4 radians).
Matrices are returned as nested tuples of complex numbers.
"""

from __future__ import annotations

import cmath
import math

Matrix2x2 = tuple[tuple[complex, complex], tuple[complex, complex]]
Matrix4x4 = tuple[
    tuple[complex, complex, complex, complex],
    tuple[complex, complex, complex, complex],
    tuple[complex, complex, complex, complex],
    tuple[complex, complex, complex, complex],
]

_2PI = 2 * math.pi


def gpi_matrix(phi: float) -> Matrix2x2:
    """Single-qubit GPI gate: [[0, e^{-i*2pi*phi}], [e^{i*2pi*phi}, 0]]."""
    e = cmath.exp(1j * _2PI * phi)
    return ((0, 1 / e), (e, 0))


def gpi2_matrix(phi: float) -> Matrix2x2:
    """Single-qubit GPI2 gate (pi/2 rotation about axis in XY plane)."""
    e = cmath.exp(1j * _2PI * phi)
    s = 1 / math.sqrt(2)
    return ((s, -1j * s / e), (-1j * s * e, s))


def ms_matrix(phi0: float, phi1: float, angle: float = 0.25) -> Matrix4x4:
    """Two-qubit Molmer-Sorensen gate with frame rotation phases and interaction angle."""
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
    """Two-qubit ZZ gate: diag(e^{-i*pi*a}, e^{i*pi*a}, e^{i*pi*a}, e^{-i*pi*a})."""
    em = cmath.exp(-1j * math.pi * angle)
    ep = cmath.exp(1j * math.pi * angle)
    return (
        (em, 0, 0, 0),
        (0, ep, 0, 0),
        (0, 0, ep, 0),
        (0, 0, 0, em),
    )
