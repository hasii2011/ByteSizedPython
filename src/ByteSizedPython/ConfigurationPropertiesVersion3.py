
from logging import INFO
from logging import Logger
from logging import basicConfig
from logging import getLogger

from codeallybasic.DynamicConfiguration import DynamicConfiguration
from codeallybasic.DynamicConfiguration import KeyName
from codeallybasic.DynamicConfiguration import SectionName
from codeallybasic.DynamicConfiguration import Sections
from codeallybasic.DynamicConfiguration import ValueDescription
from codeallybasic.DynamicConfiguration import ValueDescriptions
from codeallybasic.SecureConversions import SecureConversions

from codeallybasic.SingletonV3 import SingletonV3

from ByteSizedPython.ImpostorEnumByName import ImpostorEnumByName
from ByteSizedPython.PhoneyEnumByValue import PhoneyEnumByValue

LOGGER_NAME:    str = 'Tutorial'

BASE_FILE_NAME: str = 'config.ini'
MODULE_NAME:    str = 'version3properties'


DEFAULT_PHONEY_ENUM_BY_VALUE:  PhoneyEnumByValue  = PhoneyEnumByValue.FakeBrenda
DEFAULT_IMPOSTOR_ENUM_BY_NAME: ImpostorEnumByName = ImpostorEnumByName.High


GENERAL_PROPERTIES: ValueDescriptions = ValueDescriptions(
    {
        KeyName('debug'):    ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('logLevel'): ValueDescription(defaultValue='Info'),
        KeyName('phoneyEnumByValue'):  ValueDescription(defaultValue=DEFAULT_PHONEY_ENUM_BY_VALUE.value,  enumUseValue=True),
        KeyName('impostorEnumByName'): ValueDescription(defaultValue=DEFAULT_IMPOSTOR_ENUM_BY_NAME.name,  enumUseName=True),
    }
)

DATABASE_PROPERTIES: ValueDescriptions = ValueDescriptions(
    {
        KeyName('dbName'): ValueDescription(defaultValue='dbName'),
        KeyName('dbHost'): ValueDescription(defaultValue='localhost'),
        KeyName('dbPort'): ValueDescription(defaultValue='5342', deserializer=SecureConversions.secureInteger),
    }
)

CONFIGURATION_SECTIONS: Sections = Sections(
    {
        SectionName('General'):  GENERAL_PROPERTIES,
        SectionName('Database'): DATABASE_PROPERTIES,
    }
)


class ConfigurationPropertiesVersion3(DynamicConfiguration, metaclass=SingletonV3):
    def __init__(self):

        self._logger: Logger = getLogger(LOGGER_NAME)

        super().__init__(baseFileName=BASE_FILE_NAME, moduleName=MODULE_NAME, sections=CONFIGURATION_SECTIONS)


if __name__ == '__main__':
    basicConfig(level=INFO)

    config: ConfigurationPropertiesVersion3 = ConfigurationPropertiesVersion3()

    logger: Logger = getLogger(LOGGER_NAME)

    logger.info(f'{config.debug=}')
    logger.info(f'{config.logLevel=}')
    logger.info(f'{config.phoneyEnumByValue=}')
    logger.info(f'{config.impostorEnumByName=}')
    logger.info('Database Properties Follow')
    logger.info(f'{config.dbName=}')
    logger.info(f'{config.dbHost=}')
    logger.info(f'{config.dbPort=}')
    logger.info('Mutate Enumeration Properties')
    config.phoneyEnumByValue = PhoneyEnumByValue.TheWanderer
    logger.info(f'{config.phoneyEnumByValue=}')
    config.impostorEnumByName = ImpostorEnumByName.Low
    logger.info(f'{config.impostorEnumByName=}')
