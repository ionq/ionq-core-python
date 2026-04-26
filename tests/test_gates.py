import math

import pytest

from ionq_core.gates import gpi2_matrix, gpi_matrix, ms_matrix, zz_matrix

_PHIS = [0, 0.1, 0.25, 0.5, 0.73]


def _approx(a, b, tol=1e-12):
    for row_a, row_b in zip(a, b, strict=True):
        for va, vb in zip(row_a, row_b, strict=True):
            assert abs(va - vb) < tol, f"{va} != {vb}"


def _matmul(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)) for i in range(n))


def _dagger(m):
    n = len(m)
    return tuple(tuple(m[j][i].conjugate() for j in range(n)) for i in range(n))


def _eye(n):
    return tuple(tuple(1 + 0j if i == j else 0 + 0j for j in range(n)) for i in range(n))


def _assert_unitary(m):
    _approx(_matmul(m, _dagger(m)), _eye(len(m)))


class TestGPI:
    def test_phi0_is_pauli_x(self):
        _approx(gpi_matrix(0), ((0, 1), (1, 0)))

    def test_phi025_is_pauli_y(self):
        _approx(gpi_matrix(0.25), ((0, -1j), (1j, 0)))

    @pytest.mark.parametrize("phi", _PHIS)
    def test_involution(self, phi):
        _approx(_matmul(gpi_matrix(phi), gpi_matrix(phi)), _eye(2))

    @pytest.mark.parametrize("phi", _PHIS)
    def test_unitary(self, phi):
        _assert_unitary(gpi_matrix(phi))


class TestGPI2:
    def test_phi0_entries(self):
        s = 1 / math.sqrt(2)
        _approx(gpi2_matrix(0), ((s, -1j * s), (-1j * s, s)))

    @pytest.mark.parametrize("phi", _PHIS)
    def test_unitary(self, phi):
        _assert_unitary(gpi2_matrix(phi))


class TestMS:
    def test_default_angle_equals_025(self):
        _approx(ms_matrix(0.1, 0.2), ms_matrix(0.1, 0.2, 0.25))

    @pytest.mark.parametrize(
        ("phi0", "phi1", "angle"),
        [(0, 0, 0.25), (0.1, 0.2, 0.25), (0.3, 0.7, 0.1)],
    )
    def test_unitary(self, phi0, phi1, angle):
        _assert_unitary(ms_matrix(phi0, phi1, angle))


class TestZZ:
    def test_zero_is_identity(self):
        _approx(zz_matrix(0), _eye(4))

    def test_diagonal(self):
        m = zz_matrix(0.3)
        for i in range(len(m)):
            for j in range(len(m)):
                if i != j:
                    assert abs(m[i][j]) < 1e-15

    @pytest.mark.parametrize("angle", [0, 0.1, 0.25, 0.5, 1.0])
    def test_unitary(self, angle):
        _assert_unitary(zz_matrix(angle))
