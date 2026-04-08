from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.hamiltonian_energy_input_data_type import check_hamiltonian_energy_input_data_type
from ..models.hamiltonian_energy_input_data_type import HamiltonianEnergyInputDataType
from typing import cast

if TYPE_CHECKING:
  from ..models.hamiltonian_energy_data import HamiltonianEnergyData





T = TypeVar("T", bound="HamiltonianEnergyInputData")



@_attrs_define
class HamiltonianEnergyInputData:
    """ 
        Attributes:
            type_ (HamiltonianEnergyInputDataType):
            data (HamiltonianEnergyData):
     """

    type_: HamiltonianEnergyInputDataType
    data: HamiltonianEnergyData
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.hamiltonian_energy_data import HamiltonianEnergyData
        type_: str = self.type_

        data = self.data.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.hamiltonian_energy_data import HamiltonianEnergyData
        d = dict(src_dict)
        type_ = check_hamiltonian_energy_input_data_type(d.pop("type"))




        data = HamiltonianEnergyData.from_dict(d.pop("data"))




        hamiltonian_energy_input_data = cls(
            type_=type_,
            data=data,
        )


        hamiltonian_energy_input_data.additional_properties = d
        return hamiltonian_energy_input_data

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
