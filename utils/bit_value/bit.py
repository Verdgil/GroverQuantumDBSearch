from __future__ import annotations


class Bit:
    def __init__(self, value: int):
        assert value in (0, 1)
        self.value = value

    def __eq__(self, other: Bit):
        return self.value == other.value

    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)
