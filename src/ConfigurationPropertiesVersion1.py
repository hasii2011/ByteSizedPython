
from typing import Dict

from logging import Logger
from logging import getLogger
from logging import basicConfig
from logging import INFO

from configparser import ConfigParser

from pathlib import Path

from codeallybasic.SingletonV3 import SingletonV3

LOGGER_NAME:      str = 'Tutorial'
CONFIG_FILE_NAME: str = '/tmp/config.ini'
SECTION_GENERAL:  str = 'General'
SECTION_DATABASE: str = 'Database'

GENERAL_PREFERENCES: Dict[str, str] = {
    'debug':    'False',
    'logLevel': 'Info'
}

DATABASE_PREFERENCES: Dict[str, str] = {
    'dbName': 'example_db',
    'dbHost': 'localhost',
    'dbPort': '5432'
}


class ConfigurationPropertiesVersion1(metaclass=SingletonV3):
    """
    Basic implementation of a configuration class backed by Python
    configuration parser and .ini file
    """
    def __init__(self):
        self.logger: Logger = getLogger(LOGGER_NAME)

        self._configParser:   ConfigParser = ConfigParser()
        self._configFileName: Path         = Path(CONFIG_FILE_NAME)
        self._configParser.optionxform     = self._toStr    # type: ignore

        self._loadConfiguration()

    @property
    def debug(self) -> bool:
        return self._configParser.getboolean(SECTION_GENERAL, 'debug')

    @debug.setter
    def debug(self, newValue: bool):
        self._configParser.set(SECTION_GENERAL, 'debug', str(newValue))
        self._saveConfiguration()

    @property
    def logLevel(self) -> str:
        return self._configParser.get(SECTION_GENERAL, 'logLevel')

    @logLevel.setter
    def logLevel(self, newValue: str):
        self._configParser.set(SECTION_GENERAL, 'logLevel', newValue)
        self._saveConfiguration()

    @property
    def dbName(self) -> str:
        return self._configParser.get(SECTION_DATABASE, 'dbName')

    @dbName.setter
    def dbName(self, newValue: str):
        self._configParser.set(SECTION_DATABASE, 'dbName', newValue)
        self._saveConfiguration()

    @property
    def dbHost(self) -> str:
        return self._configParser.get(SECTION_DATABASE, 'dbHost')

    @dbHost.setter
    def dbHost(self, newValue: str):
        self._configParser.set(SECTION_DATABASE, 'dbHost', newValue)
        self._saveConfiguration()

    @property
    def dbPort(self) -> int:
        return self._configParser.getint(SECTION_DATABASE, 'dbPort')

    @dbPort.setter
    def dbPort(self, newValue: int):
        self._configParser.set(SECTION_DATABASE, 'dbPort', str(newValue))
        self._saveConfiguration()

    def _loadConfiguration(self):
        """
        Load preferences from configuration file.  May load
        no preferences if the configuration file did not exist and
        was created empty
        """
        self._ensureConfigurationFileExists()
        self._configParser.read(CONFIG_FILE_NAME)
        self._createMissingSections()
        self._createMissingKeys()

        self._saveConfiguration()

    # noinspection PyUnusedLocal
    def _ensureConfigurationFileExists(self):
        """
        Creates an empty file if does not exist.  This usually occurs
        at application start up on a new installation. We ignore the
        exception if the file exists
        """
        try:
            with self._configFileName.open(mode="x", encoding="utf-8") as configFD:
                pass
        except FileExistsError as fe:
            self.logger.info(f'Configuration file existed')

    def _createMissingSections(self):
        """
        Create missing sections.  Add additional calls for
        each defined section
        """
        self._createMissingSection(SECTION_GENERAL)
        self._createMissingSection(SECTION_DATABASE)

    def _createMissingSection(self, sectionName: str):
        """
        Only gets created if it is missing
        Args:
            sectionName: The potential section to create
        """

        hasSection: bool = self._configParser.has_section(sectionName)
        self.logger.info(f'hasSection: {hasSection} - {sectionName}')
        if hasSection is False:
            self._configParser.add_section(sectionName)

    def _createMissingKeys(self):
        """
        Create missing keys and there values.  Add additional calls for
        each defined section.

        """
        for keyName, keyValue in GENERAL_PREFERENCES.items():
            self._createMissingKey(sectionName=SECTION_GENERAL, keyName=keyName, defaultValue=keyValue)
        for keyName, keyValue in DATABASE_PREFERENCES.items():
            self._createMissingKey(sectionName=SECTION_DATABASE, keyName=keyName, defaultValue=keyValue)

    def _createMissingKey(self, sectionName: str, keyName: str, defaultValue: str):
        """
        Only gets created if it is missing.  The configuration file is updated
        immediately for each missing key and its value

        Args:
            sectionName:   The section name where the key resides
            keyName:       The key name
            defaultValue:  Its value
        """
        if self._configParser.has_option(sectionName, keyName) is False:
            self._configParser.set(sectionName, keyName, defaultValue)
            self._saveConfiguration()

    def _saveConfiguration(self):
        """
        Save configuration data to the configuration file
        """
        with open(CONFIG_FILE_NAME, "w") as fd:
            # noinspection PyTypeChecker
            self._configParser.write(fd)

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

    config: ConfigurationPropertiesVersion1 = ConfigurationPropertiesVersion1()

    logger: Logger = getLogger(LOGGER_NAME)

    logger.info(f'{config.debug=}')
    logger.info(f'{config.logLevel=}')
    #
    logger.info('Change the values and show them')
    #
    config.debug = True
    logger.info(f'{config.debug=}')
    config.logLevel = 'Warning'
    logger.info(f'{config.logLevel=}')
    #
    logger.info('**** DataBase Section ****')
    logger.info(f'{config.dbName=}')
    logger.info(f'{config.dbHost=}')
    logger.info(f'{config.dbPort=}')
    #
    logger.info('Change db values and print them')
    config.dbName = 'ozzeeDb'
    config.dbHost = 'ozzeeHost'
    config.dbPort = 6666

    logger.info(f'{config.dbName=}')
    logger.info(f'{config.dbHost=}')
    logger.info(f'{config.dbPort=}')
