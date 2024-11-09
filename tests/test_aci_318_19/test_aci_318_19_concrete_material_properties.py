"""Tests for the concrete material properties of ACI 318-19."""

import math

import pytest

from structuralcodes.codes.aci318_19 import _concrete_material_properties


@pytest.mark.parametrize(
    'f_c, w_c, expected',
    [
        (4000, 145, 3644147.43),  # Normal-weight concrete (default weight)
        (5000, 145, 4074280.69),  # Normal-weight concrete with higher strength
        (
            4000,
            120,
            2743568.48,
        ),  # Lightweight concrete with f'c = 4000 psi, w_c = 120 lb/ft³
        (
            5000,
            120,
            3067402.81,
        ),  # Lightweight concrete with f'c = 5000 psi, w_c = 120 lb/ft³
    ],
)
def test_Ec(f_c, w_c, expected):
    assert math.isclose(
        _concrete_material_properties.Ec(f_c, w_c), expected, rel_tol=1e-2
    )


@pytest.mark.parametrize(
    'f_c, lambda_, expected',
    [
        (4000, 1.0, 474.34),  # Normal-weight concrete
        (5000, 1.0, 530.33),  # Normal-weight concrete with higher strength
        (4000, 0.8, 379.47),  # Lightweight concrete with lambda = 0.8
        (5000, 0.8, 424.26),  # Lightweight concrete with lambda = 0.8
    ],
)
def test_f_r(f_c, lambda_, expected):
    assert math.isclose(
        _concrete_material_properties.f_r(f_c, lambda_), expected, rel_tol=1e-2
    )
