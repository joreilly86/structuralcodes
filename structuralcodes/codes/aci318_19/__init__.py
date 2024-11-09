"""ACI 318-19 - Building Code Requirements
for Structural Concrete and Commentary.
"""
# URL: https://www.concrete.org/store/productdetail.aspx?ItemID=318U19&Language=English&Units=US_Units

import typing as t

from ._concrete_material_properties import Ec

# Define the public API with placeholders (update these as you build the module)
__all__ = [
    'example_concrete_function',
    'example_shear_function',
]

__title__: str = 'ACI 318-19'
__year__: str = '2019'
__materials__: t.Tuple[str] = ('concrete', 'reinforcement')
