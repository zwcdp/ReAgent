#!/usr/bin/env python3

from typing import Dict, List, Type

from reagent.core.dataclasses import dataclass, field
from reagent.models.base import ModelBase
from reagent.models.dueling_quantile_dqn import DuelingQuantileDQN
from reagent.net_builder.quantile_dqn_net_builder import QRDQNNetBuilder
from reagent.parameters import NormalizationParameters, param_hash


@dataclass
class DuelingQuantile(QRDQNNetBuilder):
    __hash__ = param_hash

    sizes: List[int] = field(default_factory=lambda: [256, 128])
    activations: List[str] = field(default_factory=lambda: ["relu", "relu"])
    num_atoms: int = 51

    def __post_init_post_parse__(self):
        super().__init__()
        assert len(self.sizes) == len(self.activations), (
            f"Must have the same numbers of sizes and activations; got: "
            f"{self.sizes}, {self.activations}"
        )

    def build_q_network(
        self,
        state_normalization_parameters: Dict[int, NormalizationParameters],
        output_dim: int,
    ) -> ModelBase:
        state_dim = self._get_input_dim(state_normalization_parameters)
        return DuelingQuantileDQN(
            layers=[state_dim] + self.sizes + [output_dim],
            activations=self.activations + ["linear"],
            num_atoms=self.num_atoms,
        )
