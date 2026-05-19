# SPDX-FileCopyrightText: 2026 IonQ, Inc.
# SPDX-License-Identifier: Apache-2.0
# @generated

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qctrl_qaoa_job_input_problem_type import check_qctrl_qaoa_job_input_problem_type
from ..models.qctrl_qaoa_job_input_problem_type import QctrlQaoaJobInputProblemType
from typing import cast

if TYPE_CHECKING:
  from ..models.qctrl_qaoa_job_input_problem import QctrlQaoaJobInputProblem





T = TypeVar("T", bound="QctrlQaoaJobInput")



@_attrs_define
class QctrlQaoaJobInput:
    """
        Attributes:
            problem_type (QctrlQaoaJobInputProblemType):
            problem (QctrlQaoaJobInputProblem): A NetworkX adjacency_graph object Example: {'directed': False, 'multigraph':
                False, 'graph': [], 'nodes': [{'id': 0}, {'id': 1}, {'id': 2}], 'adjacency': [[{'id': 1}, {'id': 2}], [{'id':
                0}, {'id': 2}], [{'id': 0}, {'id': 1}]]}.
     """

    problem_type: QctrlQaoaJobInputProblemType
    problem: QctrlQaoaJobInputProblem
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.qctrl_qaoa_job_input_problem import QctrlQaoaJobInputProblem
        problem_type: str = self.problem_type

        problem = self.problem.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "problem_type": problem_type,
            "problem": problem,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.qctrl_qaoa_job_input_problem import QctrlQaoaJobInputProblem
        d = dict(src_dict)
        problem_type = check_qctrl_qaoa_job_input_problem_type(d.pop("problem_type"))




        problem = QctrlQaoaJobInputProblem.from_dict(d.pop("problem"))




        qctrl_qaoa_job_input = cls(
            problem_type=problem_type,
            problem=problem,
        )


        qctrl_qaoa_job_input.additional_properties = d
        return qctrl_qaoa_job_input

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
