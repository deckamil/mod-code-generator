#   FILE:           mcg_cgc_config_checker.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigChecker class, which is
#       responsible for verification of the configuration file data.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           22 APR 2022
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

    # class data
    config_file_path = ""
    config_file = []
    file_index = 0
    module_name_list = []
    number_of_config_file_lines = 0
    number_of_subsection_errors = 0
    NUMBER_OF_REPETITIONS_BEFORE_SKIPPING = 5

    # expected data/marker positions or properties of configuration file
    BASE_POSITION = 0
    MODULE_SOURCE_MARKER_POSITION_IN_CFG = BASE_POSITION
    MODULE_NAME_MARKER_POSITION_IN_CFG = BASE_POSITION
    MODULE_NAME_POSITION_IN_CFG = 15
    INTERFACE_TYPE_MARKER_POSITION_IN_CFG = BASE_POSITION
    INTERFACE_NAME_MARKER_POSITION_IN_CFG = BASE_POSITION
    BODY_DEFINITION_MARKER_POSITION_IN_CFG = BASE_POSITION
    MIN_MODULE_NAME_LINE_LENGTH_IN_CFG = MODULE_NAME_POSITION_IN_CFG + 1

    # verification state
    checker_state = ""

    # possible checker states
    CHECK_HEADER = 10
    FIND_NEW_MODULE = 20
    SKIP_AND_FIND_MODULE_SECTION = 30
    CHECK_FOOTER = 40
    END_CHECKING = 50

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
    # This is main method of the class, which checks if content of the configuration file is correct.
    @staticmethod
    def check_config_file():

        # set entry state
        ConfigChecker.checker_state = ConfigChecker.CHECK_HEADER

        # continue checking until verification of the configuration file is completed
        while ConfigChecker.checker_state != ConfigChecker.END_CHECKING:

            # when file index is out of range
            if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_EOF, ConfigChecker.file_index + 1, "")
                # end configuration check
                ConfigChecker.checker_state = ConfigChecker.END_CHECKING

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

            # skip current part of module section and find next one
            elif ConfigChecker.checker_state == ConfigChecker.SKIP_AND_FIND_MODULE_SECTION:
                ConfigChecker.skip_and_find_module_section()

            # check component
            elif (ConfigChecker.checker_state >= ConfigChecker.CHECK_COMPONENT_SOURCE) and \
                    (ConfigChecker.checker_state <= ConfigChecker.CHECK_COMPONENT_END):
                ConfigChecker.check_component()

            # check package
            elif (ConfigChecker.checker_state >= ConfigChecker.CHECK_PACKAGE_SOURCE) and \
                    (ConfigChecker.checker_state <= ConfigChecker.CHECK_PACKAGE_END):
                ConfigChecker.check_package()

            # check footer
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_FOOTER:
                ConfigChecker.check_footer()

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

        # clear counter of subsection errors
        ConfigChecker.number_of_subsection_errors = 0

        # when component start marker is found
        if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # start component verification
            ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_SOURCE

        # when package start marker is found
        elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE START":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # start package verification
            ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_SOURCE

        # when config end marker is found
        elif "MCG CGC CONFIG END" in ConfigChecker.config_file[ConfigChecker.file_index]:
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # start footer verification
            ConfigChecker.checker_state = ConfigChecker.CHECK_FOOTER

        # or when line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_START_OR_FOOTER, ConfigChecker.file_index+1, "")
            # skip part of the configuration file and find next module section
            ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

    # Description:
    # This method looks for next valid module section to continue verification of the configuration file,
    # after error was detected in module section.
    @staticmethod
    def skip_and_find_module_section():

        # clear counter of subsection errors
        ConfigChecker.number_of_subsection_errors = 0

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
                # end configuration check
                ConfigChecker.checker_state = ConfigChecker.END_CHECKING

            # when component start is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT START":
                # increment file index
                temporary_file_index = temporary_file_index + 1
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_SOURCE

            # when component source if found
            elif ConfigChecker.config_file[temporary_file_index].find("COMPONENT SOURCE") == \
                    ConfigChecker.MODULE_SOURCE_MARKER_POSITION_IN_CFG:
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_SOURCE

            # when component name is found
            elif (ConfigChecker.config_file[ConfigChecker.file_index].find("COMPONENT NAME ") ==
                  ConfigChecker.MODULE_NAME_MARKER_POSITION_IN_CFG) and \
                    (len(ConfigChecker.config_file[ConfigChecker.file_index]) >=
                     ConfigChecker.MIN_MODULE_NAME_LINE_LENGTH_IN_CFG):
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_NAME

            # when component input interface start is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT INPUT INTERFACE START":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE_START

            # when component input interface end is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT INPUT INTERFACE END":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE

            # when component output interface start is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT OUTPUT INTERFACE START":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE_START

            # when component output interface end is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT OUTPUT INTERFACE END":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE

            # when component local data start is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT LOCAL DATA START":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_LOCAL_DATA_START

            # when component local data end is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT LOCAL DATA END":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_LOCAL_DATA

            # when component body start is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT BODY START":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_BODY_START

            # when component body end is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT BODY END":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_BODY

            # when component end is found
            elif ConfigChecker.config_file[temporary_file_index] == "COMPONENT END":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_END

            # when package start is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE START":
                # increment file index
                temporary_file_index = temporary_file_index + 1
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_SOURCE

            # when package source if found
            elif ConfigChecker.config_file[temporary_file_index].find("PACKAGE SOURCE") == \
                    ConfigChecker.MODULE_SOURCE_MARKER_POSITION_IN_CFG:
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_SOURCE

            # when package name is found
            elif (ConfigChecker.config_file[ConfigChecker.file_index].find("PACKAGE NAME ") ==
                  ConfigChecker.MODULE_NAME_MARKER_POSITION_IN_CFG) and \
                    (len(ConfigChecker.config_file[ConfigChecker.file_index]) >=
                     ConfigChecker.MIN_MODULE_NAME_LINE_LENGTH_IN_CFG):
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_NAME

            # when package input interface start is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE INPUT INTERFACE START":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_INPUT_INTERFACE_START

            # when package input interface end is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE INPUT INTERFACE END":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_INPUT_INTERFACE

            # when package output interface start is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE OUTPUT INTERFACE START":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_OUTPUT_INTERFACE_START

            # when package output interface end is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE OUTPUT INTERFACE END":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_OUTPUT_INTERFACE

            # when package local data start is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE LOCAL DATA START":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_LOCAL_DATA_START

            # when package local data end is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE LOCAL DATA END":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_LOCAL_DATA

            # when package body start is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE BODY START":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_BODY_START

            # when package body end is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE BODY END":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_BODY

            # when package end is found
            elif ConfigChecker.config_file[temporary_file_index] == "PACKAGE END":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_END

            # when config end marker is found
            elif "MCG CGC CONFIG END" in ConfigChecker.config_file[ConfigChecker.file_index]:
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_FOOTER

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
    # This method checks correctness of component section in the configuration file.
    @staticmethod
    def check_component():

        # for component source check
        if ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_SOURCE:

            # if component source is found
            if ConfigChecker.config_file[ConfigChecker.file_index].find("COMPONENT SOURCE") == \
                    ConfigChecker.MODULE_SOURCE_MARKER_POSITION_IN_CFG:
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_NAME

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_SOURCE, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for component name check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_NAME:

            # if component name is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("COMPONENT NAME ") ==
                ConfigChecker.MODULE_NAME_MARKER_POSITION_IN_CFG) and \
                    (len(ConfigChecker.config_file[ConfigChecker.file_index]) >=
                     ConfigChecker.MIN_MODULE_NAME_LINE_LENGTH_IN_CFG):
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE_START

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_NAME, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for component input interface start check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE_START:

            # if component input interface start is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT INPUT INTERFACE START":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_INPUT_INTERFACE, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for component input interface check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_INPUT_INTERFACE:

            # if type and name in input interface is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("type ") ==
                ConfigChecker.INTERFACE_TYPE_MARKER_POSITION_IN_CFG) and \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find(" name ") >
                     ConfigChecker.INTERFACE_NAME_MARKER_POSITION_IN_CFG):
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # of if component input interface end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT INPUT INTERFACE END":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # clear counter of subsection errors
                ConfigChecker.number_of_subsection_errors = 0
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE_START

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_INPUT_INTERFACE, ConfigChecker.file_index + 1, "")
                # increment number of subsection errors
                ConfigChecker.number_of_subsection_errors = ConfigChecker.number_of_subsection_errors + 1
                # if number of subsection errors is greater than skipping threshold
                if ConfigChecker.number_of_subsection_errors >= ConfigChecker.NUMBER_OF_REPETITIONS_BEFORE_SKIPPING:
                    # skip part of the configuration file and find next module section
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION
                else:
                    # increment file index and repeat same state
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

        # for component output interface start check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE_START:

            # if component output interface start is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT OUTPUT INTERFACE START":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_OUTPUT_INTERFACE, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for component output interface check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_OUTPUT_INTERFACE:

            # if type and name in output interface is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("type ") ==
                ConfigChecker.INTERFACE_TYPE_MARKER_POSITION_IN_CFG) and \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find(" name ") >
                     ConfigChecker.INTERFACE_NAME_MARKER_POSITION_IN_CFG):
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # or if component output interface end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT OUTPUT INTERFACE END":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # clear counter of subsection errors
                ConfigChecker.number_of_subsection_errors = 0
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_LOCAL_DATA_START

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_OUTPUT_INTERFACE, ConfigChecker.file_index + 1, "")
                # increment number of subsection errors
                ConfigChecker.number_of_subsection_errors = ConfigChecker.number_of_subsection_errors + 1
                # if number of subsection errors is greater than skipping threshold
                if ConfigChecker.number_of_subsection_errors >= ConfigChecker.NUMBER_OF_REPETITIONS_BEFORE_SKIPPING:
                    # skip part of the configuration file and find next module section
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION
                else:
                    # increment file index and repeat same state
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

        # for component local data start check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_LOCAL_DATA_START:

            # if component local data start is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT LOCAL DATA START":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_LOCAL_DATA

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_LOCAL_INTERFACE, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for component local data check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_LOCAL_DATA:

            # if type and name in local data is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("type ") ==
                ConfigChecker.INTERFACE_TYPE_MARKER_POSITION_IN_CFG) and \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find(" name ") >
                     ConfigChecker.INTERFACE_NAME_MARKER_POSITION_IN_CFG):
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # or if component local data end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT LOCAL DATA END":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # clear counter of subsection errors
                ConfigChecker.number_of_subsection_errors = 0
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_BODY_START

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_LOCAL_INTERFACE, ConfigChecker.file_index + 1, "")
                # increment number of subsection errors
                ConfigChecker.number_of_subsection_errors = ConfigChecker.number_of_subsection_errors + 1
                # if number of subsection errors is greater than skipping threshold
                if ConfigChecker.number_of_subsection_errors >= ConfigChecker.NUMBER_OF_REPETITIONS_BEFORE_SKIPPING:
                    # skip part of the configuration file and find next module section
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION
                else:
                    # increment file index and repeat same state
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

        # for component body start check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_BODY_START:

            # if component body start is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT BODY START":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_BODY

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_BODY, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for component body check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_BODY:

            # if instruction or comment is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("INS ") ==
                ConfigChecker.BODY_DEFINITION_MARKER_POSITION_IN_CFG) or \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find("COM ") ==
                     ConfigChecker.BODY_DEFINITION_MARKER_POSITION_IN_CFG):
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # or if component body end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT BODY END":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # clear counter of subsection errors
                ConfigChecker.number_of_subsection_errors = 0
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_COMPONENT_END

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_BODY, ConfigChecker.file_index + 1, "")
                # increment number of subsection errors
                ConfigChecker.number_of_subsection_errors = ConfigChecker.number_of_subsection_errors + 1
                # if number of subsection errors is greater than skipping threshold
                if ConfigChecker.number_of_subsection_errors >= ConfigChecker.NUMBER_OF_REPETITIONS_BEFORE_SKIPPING:
                    # skip part of the configuration file and find next module section
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION
                else:
                    # increment file index and repeat same state
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

        # for component end check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_COMPONENT_END:

            # if component end is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "COMPONENT END":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # find beginning of next module section
                ConfigChecker.checker_state = ConfigChecker.FIND_NEW_MODULE

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_END, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

    # Description:
    # This method checks correctness of package section in the configuration file.
    @staticmethod
    def check_package():
        ConfigChecker.checker_state = ConfigChecker.END_CHECKING

    # Description:
    # This method checks correctness of footer in the configuration file.
    @staticmethod
    def check_footer():

        # start searching for end of configuration file
        continue_searching = True

        # continue searching until EOF is found
        while continue_searching:

            # when file index is out of range
            if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
                # stop searching
                continue_searching = False
                # end configuration check
                ConfigChecker.checker_state = ConfigChecker.END_CHECKING

            # when line is NOT empty
            elif ConfigChecker.config_file[ConfigChecker.file_index] != "":
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_DATA_AFTER_FOOTER, ConfigChecker.file_index + 1, "")

            # increment file index and repeat same state process
            ConfigChecker.file_index = ConfigChecker.file_index + 1
