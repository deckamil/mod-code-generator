#   FILE:           mcg_cgc_config_checker.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigChecker class, which is
#       responsible for verification of the configuration file data.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           19 MAR 2022
#
#   LICENSE:
#       This file is part of Mod Code Generator (MCG).
#
#       MCG is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       MCG is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#       GNU General Public License for more details.
#
#       Under Section 7 of GPL version 3, you are granted additional
#       permissions described in the MCG Output Exception, version 1, which
#       copy you should have received along with this program.
#
#       You should have received a copy of the GNU General Public License
#       along with this program. If not, see <https://www.gnu.org/licenses/>.


from mcg_cgc_error_handler import ErrorHandler


# Description:
# This class is responsible for verification of the configuration file.
class ConfigChecker(object):

    # initialize class data
    config_file_path = ""
    config_file = []
    file_index = 0
    number_of_config_file_lines = 0
    checker_state = ""

    # checker states
    FIND_HEADER = 0
    FIND_DATE_OR_NEW_MODULE = 1
    FIND_NEW_MODULE = 2
    SKIP_AND_FIND_NEW_MODULE = 3
    CHECK_COMPONENT = 100
    CHECK_PACKAGE = 200
    CHECK_FOOTER = 300
    CHECK_COMPLETED = 400

    # indexes of config checker list
    CONFIG_FILE_VALIDITY_INDEX = 0
    CONFIG_FILE_INDEX = 1

    # Description:
    # This method sets path to the configuration file.
    @staticmethod
    def set_config_file_path(config_file_path):

        # set config file path
        ConfigChecker.config_file_path = config_file_path

    # Description:
    # This method reads content of the configuration file.
    @staticmethod
    def read_config_file():

        # open file and read content, then close file
        config_file_disk = open(ConfigChecker.config_file_path, "r")
        config_file = config_file_disk.readlines()
        config_file = [line.strip() for line in config_file]
        config_file_disk.close()

        # set config file
        ConfigChecker.config_file = config_file
        # set number of config file lines
        ConfigChecker.number_of_config_file_lines = len(config_file)

    # Description:
    # This is main method of the class, which checks if content of configuration file is correct.
    @staticmethod
    def check_config_file():

        # set entry state
        ConfigChecker.checker_state = ConfigChecker.FIND_HEADER

        # continue checking until verification of the configuration file is completed
        while ConfigChecker.checker_state != ConfigChecker.CHECK_COMPLETED:

            # find header
            if ConfigChecker.checker_state == ConfigChecker.FIND_HEADER:
                ConfigChecker.find_header()

            # find date or new module
            elif ConfigChecker.checker_state == ConfigChecker.FIND_DATE_OR_NEW_MODULE:
                ConfigChecker.find_date_or_new_module()

            # find new module
            elif ConfigChecker.checker_state == ConfigChecker.FIND_NEW_MODULE:
                ConfigChecker.find_new_module()

            # skip current part and find new module
            elif ConfigChecker.checker_state == ConfigChecker.SKIP_AND_FIND_NEW_MODULE:
                ConfigChecker.skip_and_find_new_module()

            # check component
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT:
                ConfigChecker.check_component()

            # check package
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE:
                ConfigChecker.check_package()

            # check footer
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_FOOTER:
                ConfigChecker.find_footer()

    # Description:
    # This method looks for config start in the configuration file.
    @staticmethod
    def find_header():

        # if file index is out of range
        if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_HEADER_EOF, ConfigChecker.file_index + 1, "none")
            # complete process
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

        # else if line is empty
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1

        # else if config start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "MCG CGC CONFIG START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.FIND_DATE_OR_NEW_MODULE

        # else when line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_HEADER_UN_LINE, ConfigChecker.file_index+1, "none")
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.FIND_DATE_OR_NEW_MODULE

    # Description:
    # This method looks for date or new module section in the configuration file.
    @staticmethod
    def find_date_or_new_module():

        # if file index is out of range
        if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_DATA_OR_MOD_EOF, ConfigChecker.file_index + 1, "none")
            # complete process
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

        # else if line is empty
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1

        # else if date marker is found
        elif "MCG CGC CONFIG DATE " in ConfigChecker.config_file[ConfigChecker.file_index]:
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.FIND_NEW_MODULE

        # else if component start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT START":
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT

        # else if package start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE START":
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE

        # else when line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_DATA_OR_MOD_UN_LINE, ConfigChecker.file_index+1, "none")
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.FIND_NEW_MODULE

    # Description:
    # This method looks for new module section in the configuration file.
    @staticmethod
    def find_new_module():

        # if file index is out of range
        if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_MOD_EOF, ConfigChecker.file_index + 1, "none")
            # complete process
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

        # else if line is empty
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1

        # else if component start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT START":
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT

        # else if package start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE START":
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE

        # else when line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_MOD_UN_LINE, ConfigChecker.file_index+1, "none")
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_NEW_MODULE

    # Description:
    # This method skips current part of the configuration file and looks for new module section.
    @staticmethod
    def skip_and_find_new_module():

        # if file index is out of range
        if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_MOD_EOF, ConfigChecker.file_index + 1, "none")
            # complete process
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

        # else if line is empty
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1

        # else if component start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT START":
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT

        # else if package start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE START":
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE

        # else when line contains unexpected data
        else:
            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1

    # Description:
    # This method checks correctness of component section in the configuration file.
    @staticmethod
    def check_component():
        ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

    # Description:
    # This method checks correctness of package section in the configuration file.
    @staticmethod
    def check_package():
        ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

    # Description:
    # This method looks for config end in the configuration file.
    @staticmethod
    def find_footer():
        ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED
