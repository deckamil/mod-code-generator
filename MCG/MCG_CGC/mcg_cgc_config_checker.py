#   FILE:           mcg_cgc_config_checker.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigChecker class, which is
#       responsible for verification of the configuration file data.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           26 MAR 2022
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

    # verification state
    checker_state = ""
    check_component_state = ""
    check_package_state = ""

    # possible checker states
    CHECK_HEADER = 0
    FIND_NEW_MODULE = 2
    CHECK_COMPONENT = 100
    SKIP_AND_FIND_COMPONENT_SECTION = 500
    CHECK_PACKAGE = 200
    SKIP_AND_FIND_PACKAGE_SECTION = 600
    CHECK_FOOTER = 300
    CHECK_COMPLETED = 400

    # possible component verification states
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

    # possible package verification states
    CHECK_PACKAGE_SOURCE = 201
    CHECK_PACKAGE_NAME = 202
    CHECK_PACKAGE_INPUT_INTERFACE_START = 203
    CHECK_PACKAGE_INPUT_INTERFACE = 204
    CHECK_PACKAGE_OUTPUT_INTERFACE_START = 205
    CHECK_PACKAGE_OUTPUT_INTERFACE = 206
    CHECK_PACKAGE_LOCAL_DATA_START = 207
    CHECK_PACKAGE_LOCAL_DATA = 208
    CHECK_PACKAGE_BODY_START = 209
    CHECK_PACKAGE_BODY = 210
    CHECK_PACKAGE_END = 211
    PACKAGE_CHECK_COMPLETED = 212

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
        ConfigChecker.checker_state = ConfigChecker.CHECK_HEADER

        # continue checking until verification of the configuration file is completed
        while ConfigChecker.checker_state != ConfigChecker.CHECK_COMPLETED:

            # when file index is out of range
            if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_EOF, ConfigChecker.file_index + 1, "")
                # end configuration check
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

            # when line is empty
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # check header
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_HEADER:
                ConfigChecker.check_header()

            # find new module
            elif ConfigChecker.checker_state == ConfigChecker.FIND_NEW_MODULE:
                ConfigChecker.find_new_module()

            # check component
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT:
                ConfigChecker.check_component()

            # skip current part of module section and find next one
            elif ConfigChecker.checker_state == ConfigChecker.SKIP_AND_FIND_COMPONENT_SECTION:
                ConfigChecker.skip_and_find_module_section()

            # check package
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE:
                ConfigChecker.check_package()

            # check footer
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_FOOTER:
                ConfigChecker.find_footer()

    # Description:
    # This method checks correctness of header in the configuration file.
    @staticmethod
    def check_header():

        # when config start marker is NOT found
        if "MCG CGC CONFIG START" not in ConfigChecker.config_file[ConfigChecker.file_index]:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_HEADER, ConfigChecker.file_index + 1, "")

        # increment file index
        ConfigChecker.file_index = ConfigChecker.file_index + 1
        # find beginning of module section
        ConfigChecker.checker_state = ConfigChecker.FIND_NEW_MODULE

    # Description:
    # This method looks for new module section in the configuration file.
    @staticmethod
    def find_new_module():

        # when component start marker is found
        if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to check component state
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
            # move to recognized internal state
            ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_SOURCE

        # when package start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to check package state
            ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE
            # move to recognized internal state
            ConfigChecker.check_component_state = ConfigChecker.CHECK_PACKAGE_SOURCE

        # or when line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_MOD_ST_UN, ConfigChecker.file_index+1, "")
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_COMPONENT_SECTION

    # Description:
    # This method checks correctness of component section in the configuration file.
    @staticmethod
    def check_component():

        # continue checking until verification of the component section is completed
        while ConfigChecker.check_component_state != ConfigChecker.COMPONENT_CHECK_COMPLETED:

            # when file index is out of range
            if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_EOF, ConfigChecker.file_index + 1, "")
                # finish configuration check
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED
                # finish component check
                ConfigChecker.check_component_state = ConfigChecker.COMPONENT_CHECK_COMPLETED

            # when line is empty
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # for component source state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_SOURCE:

                # if component source is found
                if "COMPONENT SOURCE" in ConfigChecker.config_file[ConfigChecker.file_index]:
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_NAME

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_SRC_UN, ConfigChecker.file_index + 1, "")
                    # move to skip and find component section state
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_COMPONENT_SECTION
                    # finish component check
                    ConfigChecker.check_component_state = ConfigChecker.COMPONENT_CHECK_COMPLETED

            # for component name state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_NAME:

                # if component name is found
                if "COMPONENT NAME " in ConfigChecker.config_file[ConfigChecker.file_index]:
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE_START

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_NAM_UN, ConfigChecker.file_index + 1, "")
                    # move to skip and find component section state
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_COMPONENT_SECTION
                    # finish component check
                    ConfigChecker.check_component_state = ConfigChecker.COMPONENT_CHECK_COMPLETED

            # for component input interface start state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE_START:

                # if component input interface start is found
                if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT INPUT INTERFACE START":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_IN_ST_UN, ConfigChecker.file_index + 1, "")
                    # move to skip and find component section state
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_COMPONENT_SECTION
                    # finish component check
                    ConfigChecker.check_component_state = ConfigChecker.COMPONENT_CHECK_COMPLETED

            # for component input interface state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE:

                # if type and name in input interface is found
                if ("type " in ConfigChecker.config_file[ConfigChecker.file_index]) and \
                        (" name " in ConfigChecker.config_file[ConfigChecker.file_index]):
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

                # of if component input interface end is found
                elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT INPUT INTERFACE END":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE_START

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_IN_UN, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE_START

            # for component output interface start state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE_START:

                # if component output interface start is found
                if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT OUTPUT INTERFACE START":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_OUT_ST_UN, ConfigChecker.file_index + 1, "")
                    # move to skip and find component section state
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_COMPONENT_SECTION
                    # finish component check
                    ConfigChecker.check_component_state = ConfigChecker.COMPONENT_CHECK_COMPLETED

            # for component output interface state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE:

                # if type and name in output interface is found
                if ("type " in ConfigChecker.config_file[ConfigChecker.file_index]) and \
                        (" name " in ConfigChecker.config_file[ConfigChecker.file_index]):
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

                # or if component output interface end is found
                elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT OUTPUT INTERFACE END":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_LOCAL_DATA_START

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_OUT_UN, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_LOCAL_DATA_START

            # for component local data start state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_LOCAL_DATA_START:

                # if component local data start is found
                if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT LOCAL DATA START":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_LOCAL_DATA

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_LOC_ST_UN, ConfigChecker.file_index + 1, "")
                    # move to skip and find component section state
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_COMPONENT_SECTION
                    # finish component check
                    ConfigChecker.check_component_state = ConfigChecker.COMPONENT_CHECK_COMPLETED

            # for component local data state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_LOCAL_DATA:

                # if type and name in local data is found
                if ("type " in ConfigChecker.config_file[ConfigChecker.file_index]) and \
                        (" name " in ConfigChecker.config_file[ConfigChecker.file_index]):
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

                # or if component local data end is found
                elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT LOCAL DATA END":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_BODY_START

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_LOC_UN, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_BODY_START

            # for component body start state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_BODY_START:

                # if component body start is found
                if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT BODY START":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_BODY

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_BOD_ST_UN, ConfigChecker.file_index + 1, "")
                    # move to skip and find component section state
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_COMPONENT_SECTION
                    # finish component check
                    ConfigChecker.check_component_state = ConfigChecker.COMPONENT_CHECK_COMPLETED

            # for component body state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_BODY:

                # if comment is found
                if "COM " in ConfigChecker.config_file[ConfigChecker.file_index]:
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

                # or if instruction is found
                elif "INS" in ConfigChecker.config_file[ConfigChecker.file_index]:
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

                # or if component body end is found
                elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT BODY END":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_END

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_BOD_UN, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to next state
                    ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_END

            # for component end state check
            elif ConfigChecker.check_component_state == ConfigChecker.CHECK_COMPONENT_END:

                # if component end is found
                if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT END":
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to find new module state
                    ConfigChecker.checker_state = ConfigChecker.FIND_NEW_MODULE
                    # finish component check
                    ConfigChecker.check_component_state = ConfigChecker.COMPONENT_CHECK_COMPLETED

                # or if line contains unexpected data
                else:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CHK_ERR_COM_END_UN, ConfigChecker.file_index + 1, "")
                    # increment file index
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                    # move to find new module state
                    ConfigChecker.checker_state = ConfigChecker.FIND_NEW_MODULE
                    # finish component check
                    ConfigChecker.check_component_state = ConfigChecker.COMPONENT_CHECK_COMPLETED

    # Description:
    # This method looks for next valid module section to continue verification of the configuration file,
    # after error was detected in module section.
    @staticmethod
    def skip_and_find_module_section():

        # get copy of file index
        temporary_file_index = ConfigChecker.file_index
        # start searching for next valid module section
        continue_searching = True

        # continue searching until some section of the configuration file is recognized
        while continue_searching:

            # assume that some section will be found for current file index
            continue_searching = False

            # when temporary file index is out of range
            if temporary_file_index >= ConfigChecker.number_of_config_file_lines:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_EOF, temporary_file_index + 1, "")
                # finish configuration check
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPLETED

            # when component source if found
            elif "COMPONENT SOURCE" in ConfigChecker.config_file[temporary_file_index]:
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_SOURCE

            # when component name is found
            elif "COMPONENT NAME " in ConfigChecker.config_file[temporary_file_index]:
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_NAME

            # when input interface start is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT INPUT INTERFACE START":
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE_START

            # when input interface end is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT INPUT INTERFACE END":
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE

            # when output interface start is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT OUTPUT INTERFACE START":
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE_START

            # when output interface end is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT OUTPUT INTERFACE END":
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE

            # when local data start is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT LOCAL DATA START":
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_LOCAL_DATA_START

            # when local data end is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT LOCAL DATA END":
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_LOCAL_DATA

            # when body start is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT BODY START":
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_BODY_START

            # when body end is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT BODY END":
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_BODY

            # when component end is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT END":
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT
                # move to recognized internal state
                ConfigChecker.check_component_state = ConfigChecker.CHECK_COMPONENT_END

            # when package start is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE START":
                # increment file index
                temporary_file_index = temporary_file_index + 1
                # move to check component state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE
                # move to recognized internal state
                ConfigChecker.check_package_state = ConfigChecker.CHECK_PACKAGE_SOURCE

            # if any configuration section was not recognized
            else:
                # increment temporary file index
                temporary_file_index = temporary_file_index + 1
                # repeat searching for next file index
                continue_searching = True

        # record error
        ErrorHandler.record_error(ErrorHandler.CHK_ERR_SKIPPED, ConfigChecker.file_index + 1, temporary_file_index + 1)
        # set file index after searching is finished
        ConfigChecker.file_index = temporary_file_index

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
