import math


def fyd(fy: float, gamma_s: float = 1.15) -> float:
    """Calculate the design yield strength for reinforcement steel.

    ACI 318-19, Chapter 20.

    Args:
        fy (float): The specified yield strength of reinforcement in psi.
        gamma_s (float): The strength reduction factor (default is 1.15).

    Returns:
        float: The design yield strength in psi.

    Raises:
        ValueError: If fy is less than or equal to 0.
        ValueError: If gamma_s is less than 1.
    """
    if fy <= 0:
        raise ValueError(f'fy must be greater than 0, got {fy}')
    if gamma_s < 1:
        raise ValueError(
            f'gamma_s must be greater than or equal to 1, got {gamma_s}'
        )
    return fy / gamma_s


def fud(fu: float, gamma_s: float = 1.15) -> float:
    """Calculate the design ultimate tensile strength for reinforcement steel.

    ACI 318-19, Chapter 20.

    Args:
        fu (float): The specified ultimate tensile strength in psi.
        gamma_s (float): The strength reduction factor (default is 1.15).

    Returns:
        float: The design ultimate tensile strength in psi.

    Raises:
        ValueError: If fu is less than or equal to 0.
        ValueError: If gamma_s is less than 1.
    """
    if fu <= 0:
        raise ValueError(f'fu must be greater than 0, got {fu}')
    if gamma_s < 1:
        raise ValueError(
            f'gamma_s must be greater than or equal to 1, got {gamma_s}'
        )
    return fu / gamma_s
