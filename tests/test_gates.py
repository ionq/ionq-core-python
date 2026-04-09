import math

from ionq_core._gates import gpi_matrix, gpi2_matrix, ms_matrix, zz_matrix


def _approx(a, b, tol=1e-12):
    """Check two nested tuples of complex numbers are close."""
    for row_a, row_b in zip(a, b):
        for va, vb in zip(row_a, row_b):
            assert abs(va - vb) < tol, f"{va} != {vb}"


def _matmul(a, b):
    """Multiply two square matrices (nested tuples)."""
    n = len(a)
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n))
        for i in range(n)
    )


def _dagger(m):
    """Conjugate transpose."""
    n = len(m)
    return tuple(tuple(m[j][i].conjugate() for j in range(n)) for i in range(n))


def _identity(n):
    return tuple(tuple(1 + 0j if i == j else 0 + 0j for j in range(n)) for i in range(n))


def _assert_unitary(m):
    n = len(m)
    _approx(_matmul(m, _dagger(m)), _identity(n))


class TestGPI:
    def test_phi0_is_pauli_x(self):
        m = gpi_matrix(0)
        _approx(m, ((0, 1), (1, 0)))

    def test_phi025_is_pauli_y(self):
        m = gpi_matrix(0.25)
        _approx(m, ((0, -1j), (1j, 0)))

    def test_involution(self):
        for phi in [0, 0.1, 0.25, 0.5, 0.73]:
            m = gpi_matrix(phi)
            _approx(_matmul(m, m), _identity(2))

    def test_unitary(self):
        for phi in [0, 0.1, 0.25, 0.5, 0.73]:
            _assert_unitary(gpi_matrix(phi))


class TestGPI2:
    def test_phi0_entries(self):
        m = gpi2_matrix(0)
        s = 1 / math.sqrt(2)
        _approx(m, ((s, -1j * s), (-1j * s, s)))

    def test_unitary(self):
        for phi in [0, 0.1, 0.25, 0.5, 0.73]:
            _assert_unitary(gpi2_matrix(phi))


class TestMS:
    def test_default_angle_equals_025(self):
        m1 = ms_matrix(0.1, 0.2)
        m2 = ms_matrix(0.1, 0.2, 0.25)
        _approx(m1, m2)

    def test_unitary(self):
        for phi0, phi1, angle in [(0, 0, 0.25), (0.1, 0.2, 0.25), (0.3, 0.7, 0.1)]:
            _assert_unitary(ms_matrix(phi0, phi1, angle))


class TestZZ:
    def test_zero_is_identity(self):
        _approx(zz_matrix(0), _identity(4))

    def test_diagonal(self):
        m = zz_matrix(0.3)
        n = len(m)
        for i in range(n):
            for j in range(n):
                if i != j:
                    assert abs(m[i][j]) < 1e-15

    def test_unitary(self):
        for angle in [0, 0.1, 0.25, 0.5, 1.0]:
            _assert_unitary(zz_matrix(angle))
