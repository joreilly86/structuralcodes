"""Concrete class for ACI 318-19, capturing core material properties.

This class represents concrete material properties following the ACI 318-19
standards. Variables and property names are chosen to match terminology in
ACI 318-19 where possible. Units are assumed as psi for strength, lb/ft³ for
density, and strains are unitless.

Attributes:
    fc (float): Specified compressive strength of concrete (f'c), in psi.
        (See ACI 318-19 Chapter 19).
    fct (float): Tensile strength of concrete, computed or user-defined, in
        psi. (Refer to ACI 318-19, Section 19.2).
    Ec (float): Modulus of elasticity, representing the stiffness of concrete,
        in psi. (See ACI 318-19, Eq. 19.2.2.1).
    eps_cu (float): Ultimate strain capacity in compression, often specified
        in ACI 318-19 and used in concrete failure criteria (typically around
        0.003).
    density (float): Density of concrete, with a default of 150 lb/ft³.

Methods:
    __elastic__: Returns arguments to construct an elastic constitutive model.

    Experimental (The following methods are not yet implemented):
    __bilinearcompression__: Returns arguments for a bi-linear compression
        model to represent concrete in compression.
    __parabolarectangle__: Returns parameters for a parabola-rectangle model,
        a common approximation for nonlinear concrete behavior.
    __sargin__: Returns parameters for Sargin's model, providing a
        sophisticated stress-strain response used in advanced analyses.

Note:
This class is specific to ACI 318-19 and may need adjustments for other codes.

Example:
    >>> concrete = ConcreteAci31819(fc=4000)
    >>> print(concrete.Ec)  # Outputs modulus of elasticity based on ACI 318-19

"""

import typing as t

from structuralcodes.codes import aci318_19  # ACI-specific functions

from ._concrete import Concrete


class ConcreteACI318_19(Concrete):  # noqa: N801
    """Concrete implementation for ACI 318-19."""

    # computed attributes
    _fc: float = None
    _fct: t.Optional[float] = None
    _Ec: t.Optional[float] = None
    _eps_cu: t.Optional[float] = None

    def __init__(
        self,
        fc: float,
        name: t.Optional[str] = None,
        density: float = 150,
        **kwargs,
    ) -> None:
        """Initialize a new instance of Concrete for ACI 318-19.

        Args:
            fc (float): Specified compressive strength (f'c) in psi.
            name (str, optional): Descriptive name for concrete.
            density (float, optional): Density in lb/ft³ (default is 150).
        """
        del kwargs
        if name is None:
            name = f'C{round(fc):d}_ACI318'
        super().__init__(fck=fc, name=name, density=density, existing=False)

    @property
    def Ec(self) -> float:
        """Returns the modulus of elasticity, Ec, in psi."""
        if self._Ec is None:
            self._Ec = aci318_19.Ec(self._fc)
        return self._Ec

    @Ec.setter
    def Ec(self, value: float):
        """Set a user-defined value for Ec."""
        self._Ec = abs(value)

    @property
    def fct(self) -> float:
        """Returns the tensile strength, fct, in psi."""
        if self._fct is None:
            self._fct = aci318_19.fct(self._fc)
        return self._fct

    @fct.setter
    def fct(self, value: float):
        """Set a user-defined value for fct."""
        self._fct = abs(value)

    @property
    def eps_cu(self) -> float:
        """Return the ultimate compressive strain, unitless."""
        self._eps_cu = self._eps_cu or aci318_19.eps_cu(self._fc)
        return self._eps_cu

    @eps_cu.setter
    def eps_cu(self, value: float):
        """Set a user-defined value for ultimate compressive strain."""
        self._eps_cu = value

    def __elastic__(self) -> dict:
        """Return kwargs for creating an elastic constitutive law."""
        return {'E': self.Ec}

    def __bilinearcompression__(self) -> dict:
        """Return kwargs for creating a bi-linear compression model."""
        return {
            'fc': self._fc,
            'eps_c': 0.002,  # Typical ACI value for strain at peak strength
            'eps_cu': self.eps_cu,
        }

    def __parabolarectangle__(self) -> dict:
        """Return parameters for a parabola-rectangle model."""
        return {
            'fc': self._fc,
            'eps_0': 0.002,  # strain at max strength
            'eps_u': self.eps_cu,
            'n': 2.0,  # Generic ACI-compatible parabola exponent
        }

def __sargin__(self) -> dict:
    """Return parameters for Sargin model.

    ACI 318-19 doesn’t prescribe k for Sargin’s model specifically, but k=1.5
    remains a reasonable and widely accepted choice for general applications
    in practice. These output parameters allow another function or class to:
    - Calculate the stress in the concrete at a given strain.
    - Generate the full stress-strain curve from initial loading to failure,
    including the post-peak region.
    Refer to Sargin, M. (1971). "Stress-strain relationship for concrete and
    analysis of structural concrete sections." Solid Mechanics Division,
    University of Waterloo, Ontario, Canada.
    """
    return {
        'fc': self._fc,
        'eps_c1': 0.002,
        'eps_cu1': self.eps_cu,
        'k': 1.5,  # Approximate value; ACI does not specify directly
    }
