
from enum import Enum


class PhoneyEnumByValue(Enum):
    TheWanderer = 'The Wanderer'
    Mentiroso   = 'Mentiroso'
    FakeBrenda  = 'Faker Extraordinaire'
    NotSet      = 'Not Set'

    @classmethod
    def deSerialize(cls, value: str) -> 'PhoneyEnumByValue':

        match value:
            case PhoneyEnumByValue.TheWanderer.value:
                phoneyEnum: PhoneyEnumByValue = PhoneyEnumByValue.TheWanderer
            case PhoneyEnumByValue.Mentiroso.value:
                phoneyEnum = PhoneyEnumByValue.Mentiroso
            case PhoneyEnumByValue.FakeBrenda.value:
                phoneyEnum = PhoneyEnumByValue.FakeBrenda
            case _:
                raise Exception('Unknown PhoneyEnumByValue')

        return phoneyEnum
