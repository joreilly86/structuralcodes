import math

# Chapter 19 - Concrete: Design and Durability Requirements

# 19.2.2 - Modulus of Elasticity

def Ec(f_c: float, w_c: float = 145) -> float:
    """Calculate the modulus of elasticity (E_c) for concrete.

    ACI 318-19, Section 19.2.2.1:
    Specifies the modulus of elasticity calculation based on the unit weight
    and specified compressive strength of concrete.

    Equations:
    E_c = w_c^1.5 * 33 * sqrt(f'c) for lightweight concrete, psi (19.2.2.1a)
    E_c = 57000 * sqrt(f'c) for normal-weight concrete, psi (19.2.2.1b)

    Args:
        f_c (float): Specified compressive strength of concrete in psi.
        w_c (float): Unit weight of concrete in lb/ft³ (default is 145 for
            normal-weight concrete).

    Returns:
        float: Modulus of elasticity in psi.

    Note:
        From Section 19.2.1.1
        Typical minimum specified compressive strengths (f'c) for various
        applications per ACI 318-19:

        - General: 2500 psi
        - Foundations (SDC A, B, or C): 2500 psi
        - Foundations for Residential/Utility (SDC D, E, or F): 2500 psi
        - Foundations (Other uses, SDC D, E, or F): 3000 psi
        - Special Moment Frames, Structural Walls (Grade 60 or 80
          reinforcement): 3000 psi
        - Special Structural Walls (Grade 100 reinforcement): 5000 psi
        - Precast Non-prestressed Driven Piles, Drilled Shafts: 4000 psi
        - Precast Prestressed Driven Piles: 5000 psi

        These values are provided as a reference. The user is expected to input
        the appropriate f'c value.
    """
    if 90 <= w_c <= 160:
        # For varying unit weights of concrete
        return 33 * (w_c**1.5) * math.sqrt(f_c)
    # For normal-weight concrete as a fallback
    return 57000 * math.sqrt(f_c)

# 19.2.3 - Modulus of Rupture

def f_r(f_c: float, lambda_: float = 1.0) -> float:
    """Calculate the modulus of rupture (f_r) for concrete.

    ACI 318-19, Section 19.2.3:
    Specifies the modulus of rupture calculation based on the specified
    compressive strength of concrete and a modification factor for
    lightweight concrete.

    Equation:
        f_r = lambda * 7.5 * sqrt(f'c) (19.2.3.1)

    Args:
        f_c (float): Specified compressive strength of concrete in psi.
        lambda_ (float): Modification factor for lightweight concrete. Default
            is 1.0 for normal-weight concrete. Typical values range from 0.75
            to 0.85 for lightweight concrete.

    Returns:
        float: Modulus of rupture in psi.
    """
    return lambda_ * 7.5 * math.sqrt(f_c)

# 19.3.1 - Exposure Categories and Classes 

def exposure_class_requirements(exposure_class: str) -> dict | None:
    """Return the requirements for a given exposure class."""
    requirements = {
        'XC1': {'min_cement_content': 300, 'max_w_c_ratio': 0.65},
        'XC2': {'min_cement_content': 320, 'max_w_c_ratio': 0.60},
        # Add other exposure classes as needed
    }
    return requirements.get(exposure_class.upper(), None)

    # Example usage
    # print(get_exposure_class_requirements('F1'))

