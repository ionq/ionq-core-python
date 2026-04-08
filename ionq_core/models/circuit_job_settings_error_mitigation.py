from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.circuit_job_settings_error_mitigation_debiasing_type_0 import CircuitJobSettingsErrorMitigationDebiasingType0





T = TypeVar("T", bound="CircuitJobSettingsErrorMitigation")



@_attrs_define
class CircuitJobSettingsErrorMitigation:
    """ 
        Attributes:
            debiasing (bool | CircuitJobSettingsErrorMitigationDebiasingType0 | Unset):
     """

    debiasing: bool | CircuitJobSettingsErrorMitigationDebiasingType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.circuit_job_settings_error_mitigation_debiasing_type_0 import CircuitJobSettingsErrorMitigationDebiasingType0
        debiasing: bool | dict[str, Any] | Unset
        if isinstance(self.debiasing, Unset):
            debiasing = UNSET
        elif isinstance(self.debiasing, CircuitJobSettingsErrorMitigationDebiasingType0):
            debiasing = self.debiasing.to_dict()
        else:
            debiasing = self.debiasing


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if debiasing is not UNSET:
            field_dict["debiasing"] = debiasing

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.circuit_job_settings_error_mitigation_debiasing_type_0 import CircuitJobSettingsErrorMitigationDebiasingType0
        d = dict(src_dict)
        def _parse_debiasing(data: object) -> bool | CircuitJobSettingsErrorMitigationDebiasingType0 | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                debiasing_type_0 = CircuitJobSettingsErrorMitigationDebiasingType0.from_dict(data)



                return debiasing_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(bool | CircuitJobSettingsErrorMitigationDebiasingType0 | Unset, data)

        debiasing = _parse_debiasing(d.pop("debiasing", UNSET))


        circuit_job_settings_error_mitigation = cls(
            debiasing=debiasing,
        )


        circuit_job_settings_error_mitigation.additional_properties = d
        return circuit_job_settings_error_mitigation

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
