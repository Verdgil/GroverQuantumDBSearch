import string
import random
from typing import Optional, Dict

import numpy as np
from qiskit.quantum_info import Operator

from utils.bit_value.bit_value import BitValue


class DB:
    """
    Простой класс симулирующий БД
    """
    _dict = {}

    @staticmethod
    def get_random_string(length: int = 16) -> str:
        """
        :param length: длинна случайной строки
        :return: Случайная строка длинной length
        """
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    def append(self, obj: BitValue) -> None:
        """
        Добавляет в базу данных

        :param obj: Что добавить
        :return:
        """
        self._dict[self.get_random_string()] = obj

    def get_by_id(self, id_: int) -> Optional[BitValue]:
        """
        Возвразает объект по его номеру

        :param id_: номер в бд
        :return:
        """
        return self._dict.get(id_, None)

    def find_one_cl(self, value: BitValue) -> Optional[Dict[str, BitValue]]:
        """
        Ищет в базе данных

        :param value: значение искомого параметра
        :return: Объект
        """
        for key in self._dict:
            if self._dict[key] == value:
                return {key: self._dict[value]}
        return None

    @staticmethod
    def quantum_oracle(value: BitValue) -> Operator:
        """
        Квантовый оракл, фактически генерируется единичная матрица нужного размера,
        и значение соответсвующее нужному ставится в -1

        :param value: Значение
        :return: Оператор говорящий нужный элемент
        """

        op = np.identity(2**len(value))
        index = value.number_from_bits()
        op[index, index] = -1
        return Operator(op)

