from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from utils.bit_value.bit import Bit


class AbstractBitValue(ABC):
    _arr: List[Bit]

    @abstractmethod
    def __init__(self, arr: List[Bit]) -> None:
        ...

    @abstractmethod
    def __eq__(self, other: AbstractBitValue) -> bool:
        ...

    def number_from_bits(self) -> int:
        res = 0
        for ind, bit in enumerate(self._arr[::-1]):
            res += int(bit)*2**ind
        return res

    def __len__(self):
        return len(self._arr)
