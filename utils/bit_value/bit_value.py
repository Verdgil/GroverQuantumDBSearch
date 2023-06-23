from __future__ import annotations

from typing import List

from utils.bit_value.bit import Bit
from utils.bit_value.interface import AbstractBitValue


class BitValue(AbstractBitValue):
    def __init__(self, arr: List[Bit] | List[int]) -> None:
        self._arr = []
        for bit in arr:
            if isinstance(bit, Bit):
                self._arr.append(bit)
            elif isinstance(bit, int):
                self._arr.append(Bit(bit))

    def __eq__(self, other: BitValue) -> bool:
        if len(self._arr) != other._arr:
            return False

        for index, bit in enumerate(self._arr):
            if other._arr[index] != bit:
                return False

        return True
