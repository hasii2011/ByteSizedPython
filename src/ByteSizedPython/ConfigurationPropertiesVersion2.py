
from logging import Logger
from logging import getLogger
from logging import basicConfig
from logging import INFO

from codeallybasic.ConfigurationProperties import ConfigurationNameValue
from codeallybasic.ConfigurationProperties import PropertyName
from codeallybasic.ConfigurationProperties import Section
from codeallybasic.ConfigurationProperties import ConfigurationProperties
from codeallybasic.ConfigurationProperties import SectionName
from codeallybasic.ConfigurationProperties import Sections
from codeallybasic.ConfigurationProperties import configurationGetter
from codeallybasic.ConfigurationProperties import configurationSetter

from codeallybasic.SingletonV3 import SingletonV3

from ByteSizedPython.ImpostorEnumByName import ImpostorEnumByName
from ByteSizedPython.PhoneyEnumByValue import PhoneyEnumByValue

LOGGER_NAME:    str = 'Tutorial'

BASE_FILE_NAME: str = 'config.ini'
MODULE_NAME:    str = 'version2properties'


DEFAULT_PHONEY_ENUM_BY_VALUE:  PhoneyEnumByValue   = PhoneyEnumByValue.FakeBrenda
DEFAULT_IMPOSTOR_ENUM_BY_NAME: ImpostorEnumByName = ImpostorEnumByName.High


SECTION_GENERAL: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('debug'),              defaultValue='False'),
        ConfigurationNameValue(name=PropertyName('logLevel'),           defaultValue='Info'),
        ConfigurationNameValue(name=PropertyName('phoneyEnumByValue'),  defaultValue=DEFAULT_PHONEY_ENUM_BY_VALUE.value),
        ConfigurationNameValue(name=PropertyName('impostorEnumByName'), defaultValue=DEFAULT_IMPOSTOR_ENUM_BY_NAME.name),
    ]
)

SECTION_DATABASE: Section = Section(
    [
        ConfigurationNameValue(name=PropertyName('dbName'), defaultValue='example_db'),
        ConfigurationNameValue(name=PropertyName('dbHost'), defaultValue='localhost'),
        ConfigurationNameValue(name=PropertyName('dbPort'), defaultValue='5432'),
    ]
)


CONFIGURATION_SECTIONS: Sections = Sections(
    {
        SectionName('General'):  SECTION_GENERAL,
        SectionName('Database'): SECTION_DATABASE,
    }
)


class ConfigurationPropertiesVersion2(ConfigurationProperties, metaclass=SingletonV3):

    def __init__(self):
        self.logger: Logger = getLogger(LOGGER_NAME)

        super().__init__(baseFileName=BASE_FILE_NAME, moduleName=MODULE_NAME, sections=CONFIGURATION_SECTIONS)

        self._configParser.optionxform = self._toStr    # type: ignore

        self._loadConfiguration()

    @property
    @configurationGetter(sectionName='General')
    def debug(self) -> str:
        return ''

    @debug.setter
    @configurationSetter(sectionName='General')
    def debug(self, newValue: str):
        pass

    @property
    @configurationGetter(sectionName='General')
    def logLevel(self) -> str:
        return ''

    @logLevel.setter
    @configurationSetter(sectionName='General')
    def logLevel(self, newValue: str):
        pass

    @property
    @configurationGetter(sectionName='General', deserializeFunction=PhoneyEnumByValue.deSerialize)
    def phoneyEnumByValue(self) -> PhoneyEnumByValue:
        return PhoneyEnumByValue.NotSet      # Never executed

    @phoneyEnumByValue.setter
    @configurationSetter(sectionName='General', isEnum=True)
    def phoneyEnumByValue(self, newValue: PhoneyEnumByValue):
        pass

    @property
    @configurationGetter(sectionName='General')
    def impostorEnumByName(self) -> ImpostorEnumByName:
        return ImpostorEnumByName.NotSet      # Never executed

    @impostorEnumByName.setter
    @configurationSetter(sectionName='General', enumUseName=True)
    def impostorEnumByName(self, newValue: ImpostorEnumByName):
        pass

    @property
    @configurationGetter(sectionName='Database')
    def dbName(self) -> str:
        return ''

    @dbName.setter
    @configurationSetter(sectionName='Database')
    def dbName(self, newValue: str):
        pass

    @property
    @configurationGetter(sectionName='Database')
    def dbHost(self) -> str:
        return ''

    @dbHost.setter
    @configurationSetter(sectionName='Database')
    def dbHost(self, newValue: str):
        pass

    @property
    @configurationGetter(sectionName='Database', deserializeFunction=int)
    def dbPort(self) -> int:
        return -1

    @dbPort.setter
    @configurationSetter(sectionName='Database',)
    def dbPort(self, newValue: int):
        pass

    def _toStr(self, optionString: str) -> str:
        """
        Override base method

        Args:
            optionString:

        Returns: The option string unchanged
        """
        return optionString


if __name__ == '__main__':
    basicConfig(level=INFO)

    config: ConfigurationPropertiesVersion2 = ConfigurationPropertiesVersion2()

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
