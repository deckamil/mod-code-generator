#   FILE:           mcg_cgc_config_checker.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigChecker class, which is
#       responsible for verification of the configuration file data.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           20 MAR 2022
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

        # when file index is out of range
        if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_HEADER_EOF, ConfigChecker.file_index + 1, "")
            # complete process
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

        # when line is empty
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1

        # when config start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "MCG CGC CONFIG START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.FIND_DATE_OR_NEW_MODULE

        # or when line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_HEADER_UN_LINE, ConfigChecker.file_index+1, "")
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.FIND_DATE_OR_NEW_MODULE

    # Description:
    # This method looks for date or new module section in the configuration file.
    @staticmethod
    def find_date_or_new_module():

        # when file index is out of range
        if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_DATA_OR_MOD_START_EOF, ConfigChecker.file_index + 1, "")
            # complete process
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

        # when line is empty
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1

        # when date marker is found
        elif "MCG CGC CONFIG DATE " in ConfigChecker.config_file[ConfigChecker.file_index]:
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.FIND_NEW_MODULE

        # when component start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT

        # when package start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE

        # or when line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_DATA_OR_MOD_START_UN_LINE, ConfigChecker.file_index+1, "")
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.FIND_NEW_MODULE

    # Description:
    # This method looks for new module section in the configuration file.
    @staticmethod
    def find_new_module():

        # when file index is out of range
        if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_MOD_START_EOF, ConfigChecker.file_index + 1, "")
            # complete process
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

        # when line is empty
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1

        # when component start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT

        # when package start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE

        # or when line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_MOD_START_UN_LINE, ConfigChecker.file_index+1, "")
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_NEW_MODULE

    # Description:
    # This method skips current part of the configuration file and looks for new module section.
    @staticmethod
    def skip_and_find_new_module():

        # when file index is out of range
        if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_MOD_START_EOF, ConfigChecker.file_index + 1, "")
            # complete process
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

        # when line is empty
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1

        # when component start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT

        # when package start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE

        # or when line contains unexpected data
        else:
            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1

    # Description:
    # This method checks correctness of component section in the configuration file.
    @staticmethod
    def check_component():

        # internal method state
        check_component_state = ""

        # method states
        CHECK_COMPONENT_SOURCE = 101
        CHECK_COMPONENT_NAME = 102
        CHECK_COMPONENT_INPUT_INTERFACE_START = 103
        CHECK_COMPONENT_INPUT_INTERFACE = 104
        CHECK_COMPONENT_OUTPUT_INTERFACE_START = 105
        CHECK_COMPONENT_OUTPUT_INTERFACE = 106
        CHECK_COMPONENT_LOCAL_DATA_START = 107
        CHECK_COMPONENT_LOCAL_DATA = 108
        CHECK_COMPONENT_BODY_START = 109
        CHECK_COMPONENT_BODY = 110
        CHECK_COMPONENT_END = 111
        COMPONENT_CHECK_COMPLETED = 112

        # set entry state
        check_component_state = CHECK_COMPONENT_SOURCE

        # continue checking until verification of the configuration file is completed
        while check_component_state != COMPONENT_CHECK_COMPLETED:

            # when file index is out of range
            if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_EOF, ConfigChecker.file_index + 1, "")
                # complete component check
                check_component_state = COMPONENT_CHECK_COMPLETED
                # complete process
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

            # when line is empty
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # check component source
            elif check_component_state == CHECK_COMPONENT_SOURCE:

                # when component source marker is found
                if "COMPONENT SOURCE " in ConfigChecker.config_file[ConfigChecker.file_index]:
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_NAME

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_SRC_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_NAME

            # check component name
            elif check_component_state == CHECK_COMPONENT_NAME:

                # when component name marker is found
                if "COMPONENT NAME " in ConfigChecker.config_file[ConfigChecker.file_index]:
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_INPUT_INTERFACE_START

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_NAM_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_INPUT_INTERFACE_START

            # check component input interface start
            elif check_component_state == CHECK_COMPONENT_INPUT_INTERFACE_START:

                # when component input interface start marker is found
                if ConfigChecker.config_file[ConfigChecker.file_index] == "INPUT INTERFACE START":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_INPUT_INTERFACE

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_IN_ST_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_INPUT_INTERFACE

            # check component input interface
            elif check_component_state == CHECK_COMPONENT_INPUT_INTERFACE:

                # when type and name in input interface is found
                if ("type " in ConfigChecker.config_file[ConfigChecker.file_index]) and \
                        (" name " in ConfigChecker.config_file[ConfigChecker.file_index]):
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

                # when component input interface end marker is found
                elif ConfigChecker.config_file[ConfigChecker.file_index] == "INPUT INTERFACE END":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_OUTPUT_INTERFACE_START

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_IN_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_OUTPUT_INTERFACE_START

            # check component output interface start
            elif check_component_state == CHECK_COMPONENT_OUTPUT_INTERFACE_START:

                # when component output interface start marker is found
                if ConfigChecker.config_file[ConfigChecker.file_index] == "OUTPUT INTERFACE START":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_OUTPUT_INTERFACE

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_OUT_ST_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_OUTPUT_INTERFACE

            # check component output interface
            elif check_component_state == CHECK_COMPONENT_OUTPUT_INTERFACE:

                # when type and name in output interface is found
                if ("type " in ConfigChecker.config_file[ConfigChecker.file_index]) and \
                        (" name " in ConfigChecker.config_file[ConfigChecker.file_index]):
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

                # when component output interface end marker is found
                elif ConfigChecker.config_file[ConfigChecker.file_index] == "OUTPUT INTERFACE END":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_LOCAL_DATA_START

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_OUT_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_LOCAL_DATA_START

            # check component local data start
            elif check_component_state == CHECK_COMPONENT_LOCAL_DATA_START:

                # when component local data start marker is found
                if ConfigChecker.config_file[ConfigChecker.file_index] == "LOCAL DATA START":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_LOCAL_DATA

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_LOC_ST_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_LOCAL_DATA

            # check component local data
            elif check_component_state == CHECK_COMPONENT_LOCAL_DATA:

                # when type and name in local data is found
                if ("type " in ConfigChecker.config_file[ConfigChecker.file_index]) and \
                        (" name " in ConfigChecker.config_file[ConfigChecker.file_index]):
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

                # when component local data end marker is found
                elif ConfigChecker.config_file[ConfigChecker.file_index] == "LOCAL DATA END":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_BODY_START

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_LOC_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_BODY_START

            # check component body start
            elif check_component_state == CHECK_COMPONENT_BODY_START:

                # when component body start marker is found
                if ConfigChecker.config_file[ConfigChecker.file_index] == "BODY START":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_BODY

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_BOD_ST_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_BODY

            # check component body
            elif check_component_state == CHECK_COMPONENT_BODY:

                # when comment is found
                if "COM " in ConfigChecker.config_file[ConfigChecker.file_index]:
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

                # when instruction is found
                if "INS" in ConfigChecker.config_file[ConfigChecker.file_index]:
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

                # when component body end marker is found
                elif ConfigChecker.config_file[ConfigChecker.file_index] == "BODY END":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_END

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_BOD_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    check_component_state = CHECK_COMPONENT_END

            # check component end
            elif check_component_state == CHECK_COMPONENT_END:

                # when component end marker is found
                if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT END":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # complete component check
                    check_component_state = COMPONENT_CHECK_COMPLETED
                    # find new module
                    ConfigChecker.checker_state = ConfigChecker.FIND_NEW_MODULE

                # or when line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_END_UN_LINE, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # complete component check
                    check_component_state = COMPONENT_CHECK_COMPLETED
                    # find new module
                    ConfigChecker.checker_state = ConfigChecker.FIND_NEW_MODULE

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
