"""This module provides functions to calculate the shear strength
based on ACI 318-19.
"""

import math

# 22.5 One Way Shear Strength

def calc_shear_strength(
    f_c: float,
    bw: float,
    d: float,
    Nu: float = 0.0,
    Ag: float = None,
    Av_min: float = None,
    lambda_concrete: float = 1.0,
    phi: float = None,
) -> dict:
    """Calculate the nominal one-way shear strength (Vn), based on ACI 318-19.

    Args:
        f_c (float): Concrete compressive strength in psi.
        bw (float): Width of the section in inches.
        d (float): Effective depth of the section in inches.
        Nu (float): Axial load, compression is positive (default is 0).
        Ag (float): Gross area of the section in square inches (required if
            Nu provided).
        Av_min (float): Minimum shear reinforcement area, in² (optional).
        lambda_concrete (float): Modification factor for lightweight concrete.
        phi (float): Optional strength reduction factor, calculated if not
            provided.

    Returns:
        dict: Dictionary with shear strength values:
              {'Vc': ..., 'Vn': ..., 'phi': ..., 'lambda_s': ...}
    """
    # Check inputs
    if Nu != 0 and Ag is None:
        raise ValueError('Ag must be provided if Nu is not zero.')

    # Size effect factor (λs)
    lambda_s = min(math.sqrt(2 / (1 + d / 10)), 1.0)

    # Calculate Vc based on Table 22.5.5.1 (nonprestressed case)
    if Av_min is not None and Av_min >= 0:  # For sections with min shear reinf
        # Choose between Vc calculation methods (a or b)
        Vc_a = 2 * lambda_concrete * math.sqrt(f_c) * bw * d
        Vc_b = (8 * lambda_concrete * (Av_min / (bw * d)) ** (1 / 3) *
                math.sqrt(f_c) * bw * d)
        Vc = max(Vc_a, Vc_b)
    else:  # For sections without min shear reinforcement
        rho_w = Av_min / (bw * d) if Av_min else 0
        Vc = (8 * lambda_s * lambda_concrete * (rho_w) ** (1 / 3) *
              math.sqrt(f_c) * bw * d)

    # Adjust for axial load effect
    Nu_term = min(Nu / (6 * Ag), 0.05 * f_c) if Nu and Ag else 0
    Vc += Nu_term * bw * d

    # Limit Vc per ACI 22.5.5.1.1
    Vc_max = 5 * lambda_concrete * math.sqrt(f_c) * bw * d
    Vc = min(Vc, Vc_max)

    # Calculate phi if not provided
    if phi is None:
        # Placeholder for logic based on Table 21.2.1 (default for shear: 0.75)
        phi = 0.75  # This could be dynamically calculated based on inputs

    # Calculate nominal shear strength Vn
    Vn = phi * Vc  # Vs could be added if reinforcement is present

    return {
        'Vc': Vc,
        'Vn': Vn,
        'phi': phi,
        'lambda_s': lambda_s,
    }
