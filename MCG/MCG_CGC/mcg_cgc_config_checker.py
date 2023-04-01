#   FILE:           mcg_cgc_config_checker.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigChecker class, which is
#       responsible for verification of the configuration file data.
#
#   COPYRIGHT:      Copyright (C) 2022-2023 Kamil Deć github.com/deckamil
#   DATE:           1 APR 2023
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
from mcg_cgc_logger import Logger


# Description:
# This class is responsible for verification of the configuration file.
class ConfigChecker(object):

    # class data
    config_file_path = ""
    config_file = []
    file_index = 0
    module_name_list = []
    operation_name_list = []
    number_of_config_file_lines = 0
    number_of_subsection_errors = 0
    NUMBER_OF_REPETITIONS_BEFORE_SKIPPING = 5

    # expected data/marker positions or properties of configuration file
    BASE_POSITION = 0
    MODULE_SOURCE_MARKER_POSITION_IN_CFG = BASE_POSITION
    MODULE_NAME_MARKER_POSITION_IN_CFG = BASE_POSITION
    COMPONENT_NAME_POSITION_IN_CFG = 15
    PACKAGE_NAME_POSITION_IN_CFG = 13
    INTERFACE_TYPE_MARKER_POSITION_IN_CFG = BASE_POSITION
    INTERFACE_NAME_MARKER_POSITION_IN_CFG = BASE_POSITION
    BODY_DEFINITION_MARKER_POSITION_IN_CFG = BASE_POSITION
    MIN_COMPONENT_NAME_LINE_LENGTH_IN_CFG = COMPONENT_NAME_POSITION_IN_CFG + 1
    MIN_PACKAGE_NAME_LINE_LENGTH_IN_CFG = PACKAGE_NAME_POSITION_IN_CFG + 1

    # verification state
    checker_state = ""

    # possible checker states
    CHECK_HEADER = 100
    FIND_NEW_MODULE = 200
    CHECK_MODULE_NAME = 301
    CHECK_OPERATION_NAME = 302
    CHECK_INPUT_INTERFACE_START = 303
    CHECK_INPUT_INTERFACE = 304
    CHECK_OUTPUT_INTERFACE_START = 305
    CHECK_OUTPUT_INTERFACE = 306
    CHECK_LOCAL_INTERFACE_START = 307
    CHECK_LOCAL_INTERFACE = 308
    CHECK_MODULE_BODY_START = 309
    CHECK_MODULE_BODY = 310
    CHECK_MODULE_END = 311
    SKIP_TO_NEXT_SECTION = 400
    CHECK_FOOTER = 500
    END_CHECKING = 600

    # Description:
    # This method sets path to the configuration file.
    @staticmethod
    def set_config_file_path(config_file_path):

        # set config file path
        ConfigChecker.config_file_path = config_file_path

    # Description:
    # This method loads content of the configuration file from hard disk.
    @staticmethod
    def load_config_file():

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Loading of the configuration file",
                                True)

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
    # This method checks content of the configuration file.
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

            # check module name
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_MODULE_NAME:
                ConfigChecker.check_module_name()

            # check operation name
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_OPERATION_NAME:
                ConfigChecker.check_operation_name()

            # check interface
            elif (ConfigChecker.checker_state == ConfigChecker.CHECK_INPUT_INTERFACE_START or
                  ConfigChecker.checker_state == ConfigChecker.CHECK_INPUT_INTERFACE or
                  ConfigChecker.checker_state == ConfigChecker.CHECK_OUTPUT_INTERFACE_START or
                  ConfigChecker.checker_state == ConfigChecker.CHECK_OUTPUT_INTERFACE or
                  ConfigChecker.checker_state == ConfigChecker.CHECK_LOCAL_INTERFACE_START or
                  ConfigChecker.checker_state == ConfigChecker.CHECK_LOCAL_INTERFACE):
                ConfigChecker.check_interface()

            # check module body
            elif (ConfigChecker.checker_state == ConfigChecker.CHECK_MODULE_BODY_START or
                  ConfigChecker.checker_state == ConfigChecker.CHECK_MODULE_BODY):
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                ConfigChecker.skip_to_next_section()

            # check module end
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_MODULE_END:
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                ConfigChecker.skip_to_next_section()

            # skip current part of module section and find next one
            elif ConfigChecker.checker_state == ConfigChecker.SKIP_TO_NEXT_SECTION:
                ConfigChecker.skip_to_next_section()

            # check footer
            elif ConfigChecker.checker_state == ConfigChecker.CHECK_FOOTER:
                ConfigChecker.check_footer()

    # Description:
    # This method returns content of the configuration file.
    @staticmethod
    def get_config_file():

        # return config file
        return ConfigChecker.config_file

    # Description:
    # This method checks correctness of header in the configuration file.
    @staticmethod
    def check_header():

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Checking header of the configuration file at line "
                                + str(ConfigChecker.file_index + 1),
                                False)

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

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Looking for next section of the configuration file",
                                False)

        # clear counter of subsection errors
        ConfigChecker.number_of_subsection_errors = 0

        # when module start marker is found
        if ConfigChecker.config_file[ConfigChecker.file_index] == "$MODULE START$":
            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Have found new module section in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # start module verification
            ConfigChecker.checker_state = ConfigChecker.CHECK_MODULE_NAME

        # when config end marker is found
        elif "MCG CGC CONFIG END" in ConfigChecker.config_file[ConfigChecker.file_index]:
            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Have found footer of the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)
            # start footer verification
            ConfigChecker.checker_state = ConfigChecker.CHECK_FOOTER

        # or when line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_START_OR_FOOTER, ConfigChecker.file_index+1, "")
            # skip part of the configuration file and find next section
            ConfigChecker.checker_state = ConfigChecker.SKIP_TO_NEXT_SECTION

    # Description:
    # This method checks correctness of module name section in the configuration file.
    @staticmethod
    def check_module_name():

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Checking module name in the configuration file at line "
                                + str(ConfigChecker.file_index + 1),
                                False)

        # if module name start and end marker if found and module name is not empty
        if (ConfigChecker.config_file[ConfigChecker.file_index] == "$MODULE NAME START$" and
                len(ConfigChecker.config_file[ConfigChecker.file_index+1]) > 1 and
                ConfigChecker.config_file[ConfigChecker.file_index+2] == "$MODULE NAME END$"):
            # get module name
            module_name = ConfigChecker.config_file[ConfigChecker.file_index+1]
            # check if module name was already defined in the configuration file
            ConfigChecker.check_if_same_module_name(module_name)
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 3
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_OPERATION_NAME

        # or if line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_MODULE_NAME, ConfigChecker.file_index + 1, "")
            # skip part of the configuration file and find next module section
            ConfigChecker.checker_state = ConfigChecker.SKIP_TO_NEXT_SECTION

    # Description:
    # This method checks correctness of operation name section in the configuration file.
    @staticmethod
    def check_operation_name():

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Checking operation name in the configuration file at line "
                                + str(ConfigChecker.file_index + 1),
                                False)

        # if operation name start and end marker if found and operation name is not empty
        if (ConfigChecker.config_file[ConfigChecker.file_index] == "$OPERATION NAME START$" and
                len(ConfigChecker.config_file[ConfigChecker.file_index+1]) > 1 and
                ConfigChecker.config_file[ConfigChecker.file_index+2] == "$OPERATION NAME END$"):
            # get operation name
            operation_name = ConfigChecker.config_file[ConfigChecker.file_index+1]
            # check if operation name was already defined in the configuration file
            ConfigChecker.check_if_same_operation_name(operation_name)
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 3
            # move to next state
            ConfigChecker.checker_state = ConfigChecker.CHECK_INPUT_INTERFACE_START

        # or if line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_OPERATION_NAME, ConfigChecker.file_index + 1, "")
            # skip part of the configuration file and find next module section
            ConfigChecker.checker_state = ConfigChecker.SKIP_TO_NEXT_SECTION

    # Description:
    # This method checks correctness of input, output or local interface section in the configuration file.
    @staticmethod
    def check_interface():

        # method setup depending on checker state
        if ConfigChecker.checker_state == ConfigChecker.CHECK_INPUT_INTERFACE_START:
            marker = "$INPUT "
            info = "input"
            error_code = ErrorHandler.CHK_ERR_FAULTY_INPUT_INTERFACE
            next_state = ConfigChecker.CHECK_INPUT_INTERFACE

        elif ConfigChecker.checker_state == ConfigChecker.CHECK_INPUT_INTERFACE:
            marker = "$INPUT "
            info = "input"
            error_code = ErrorHandler.CHK_ERR_FAULTY_INPUT_INTERFACE
            next_state = ConfigChecker.CHECK_OUTPUT_INTERFACE_START

        elif ConfigChecker.checker_state == ConfigChecker.CHECK_OUTPUT_INTERFACE_START:
            marker = "$OUTPUT "
            info = "output"
            error_code = ErrorHandler.CHK_ERR_FAULTY_OUTPUT_INTERFACE
            next_state = ConfigChecker.CHECK_OUTPUT_INTERFACE

        elif ConfigChecker.checker_state == ConfigChecker.CHECK_OUTPUT_INTERFACE:
            marker = "$OUTPUT "
            info = "output"
            error_code = ErrorHandler.CHK_ERR_FAULTY_OUTPUT_INTERFACE
            next_state = ConfigChecker.CHECK_LOCAL_INTERFACE_START

        elif ConfigChecker.checker_state == ConfigChecker.CHECK_LOCAL_INTERFACE_START:
            marker = "$LOCAL "
            info = "local"
            error_code = ErrorHandler.CHK_ERR_FAULTY_LOCAL_INTERFACE
            next_state = ConfigChecker.CHECK_LOCAL_INTERFACE

        else:
            marker = "$LOCAL "
            info = "local"
            error_code = ErrorHandler.CHK_ERR_FAULTY_LOCAL_INTERFACE
            next_state = ConfigChecker.CHECK_MODULE_BODY_START

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Checking " + info + " interface in the configuration file at line "
                                + str(ConfigChecker.file_index + 1),
                                False)

        # for interface start check
        if (ConfigChecker.checker_state == ConfigChecker.CHECK_INPUT_INTERFACE_START or
                ConfigChecker.checker_state == ConfigChecker.CHECK_OUTPUT_INTERFACE_START or
                ConfigChecker.checker_state == ConfigChecker.CHECK_LOCAL_INTERFACE_START):

            # if interface start marker is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == str(marker + "INTERFACE START$"):
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = next_state

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(error_code, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_TO_NEXT_SECTION

        # otherwise for interface check
        else:

            # if type and name in input interface is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("type ") ==
                ConfigChecker.INTERFACE_TYPE_MARKER_POSITION_IN_CFG) and \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find(" name ") >
                     ConfigChecker.INTERFACE_NAME_MARKER_POSITION_IN_CFG):
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # or if interface end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == str(marker + "INTERFACE END$"):
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # clear counter of subsection errors
                ConfigChecker.number_of_subsection_errors = 0
                # move to next state
                ConfigChecker.checker_state = next_state

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(error_code, ConfigChecker.file_index + 1, "")
                # increment number of subsection errors
                ConfigChecker.number_of_subsection_errors = ConfigChecker.number_of_subsection_errors + 1
                # if number of subsection errors is greater than skipping threshold
                if ConfigChecker.number_of_subsection_errors >= ConfigChecker.NUMBER_OF_REPETITIONS_BEFORE_SKIPPING:
                    # skip part of the configuration file and find next module section
                    ConfigChecker.checker_state = ConfigChecker.SKIP_TO_NEXT_SECTION
                else:
                    # increment file index and repeat same state
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

    # Description:
    # This method looks for next valid module section to continue verification of the configuration file,
    # after error was detected in module section.
    @staticmethod
    def skip_to_next_section():

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Skipping current section of the configuration file and looking for next one",
                                False)

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

            # when module name is found
            elif ConfigChecker.config_file[temporary_file_index] == "$MODULE NAME START$":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_MODULE_NAME

            # when operation name is found
            elif ConfigChecker.config_file[temporary_file_index] == "$OPERATION NAME START$":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_OPERATION_NAME

            # when input interface is found
            elif ConfigChecker.config_file[temporary_file_index] == "$INPUT INTERFACE START$":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_INPUT_INTERFACE_START

            # when output interface is found
            elif ConfigChecker.config_file[temporary_file_index] == "$OUTPUT INTERFACE START$":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_OUTPUT_INTERFACE_START

            # when local interface is found
            elif ConfigChecker.config_file[temporary_file_index] == "$LOCAL INTERFACE START$":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_LOCAL_INTERFACE_START

            # when module body is found
            elif ConfigChecker.config_file[temporary_file_index] == "$MODULE BODY START$":
                # move to expected state
                ConfigChecker.checker_state = ConfigChecker.CHECK_MODULE_BODY_START

            # when config end marker is found
            elif "MCG CGC CONFIG END" in ConfigChecker.config_file[temporary_file_index]:
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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component source in the configuration file at line "
                                    + str(ConfigChecker.file_index + 1),
                                    False)

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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component name in the configuration file at line "
                                    + str(ConfigChecker.file_index + 1),
                                    False)

            # if component name is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("COMPONENT NAME ") ==
                ConfigChecker.MODULE_NAME_MARKER_POSITION_IN_CFG) and \
                    (len(ConfigChecker.config_file[ConfigChecker.file_index]) >=
                     ConfigChecker.MIN_COMPONENT_NAME_LINE_LENGTH_IN_CFG):
                # get configuration file line
                line = ConfigChecker.config_file[ConfigChecker.file_index]
                # get module name
                module_name = line[ConfigChecker.COMPONENT_NAME_POSITION_IN_CFG:len(line)]
                # check if same module name was already declared in the configuration file
                ConfigChecker.check_if_same_module_name(module_name)
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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component input interface in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component input interface in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component output interface in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component output interface in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component local data in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component local data in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component body in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component body in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

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

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking component end in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

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

        # for package source check
        if ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_SOURCE:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package source in the configuration file at line "
                                    + str(ConfigChecker.file_index + 1),
                                    False)

            # if package source is found
            if ConfigChecker.config_file[ConfigChecker.file_index].find("PACKAGE SOURCE") == \
                    ConfigChecker.MODULE_SOURCE_MARKER_POSITION_IN_CFG:
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_NAME

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_SOURCE, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for package name check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_NAME:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package name in the configuration file at line "
                                    + str(ConfigChecker.file_index + 1),
                                    False)

            # if package name is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("PACKAGE NAME ") ==
                ConfigChecker.MODULE_NAME_MARKER_POSITION_IN_CFG) and \
                    (len(ConfigChecker.config_file[ConfigChecker.file_index]) >=
                     ConfigChecker.MIN_PACKAGE_NAME_LINE_LENGTH_IN_CFG):
                # get configuration file line
                line = ConfigChecker.config_file[ConfigChecker.file_index]
                # get module name
                module_name = line[ConfigChecker.PACKAGE_NAME_POSITION_IN_CFG:len(line)]
                # check if same module name was already declared in the configuration file
                ConfigChecker.check_if_same_module_name(module_name)
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_INPUT_INTERFACE_START

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_NAME, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for package input interface start check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_INPUT_INTERFACE_START:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package input interface in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

            # if package input interface start is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE INPUT INTERFACE START":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_INPUT_INTERFACE

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_INPUT_INTERFACE, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for package input interface check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_INPUT_INTERFACE:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package input interface in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

            # if type and name in input interface is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("type ") ==
                ConfigChecker.INTERFACE_TYPE_MARKER_POSITION_IN_CFG) and \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find(" name ") >
                     ConfigChecker.INTERFACE_NAME_MARKER_POSITION_IN_CFG):
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # of if package input interface end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE INPUT INTERFACE END":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # clear counter of subsection errors
                ConfigChecker.number_of_subsection_errors = 0
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_OUTPUT_INTERFACE_START

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

        # for package output interface start check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_OUTPUT_INTERFACE_START:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package output interface in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

            # if package output interface start is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE OUTPUT INTERFACE START":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_OUTPUT_INTERFACE

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_OUTPUT_INTERFACE, ConfigChecker.file_index + 1,
                                          "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for package output interface check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_OUTPUT_INTERFACE:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package output interface in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

            # if type and name in output interface is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("type ") ==
                ConfigChecker.INTERFACE_TYPE_MARKER_POSITION_IN_CFG) and \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find(" name ") >
                     ConfigChecker.INTERFACE_NAME_MARKER_POSITION_IN_CFG):
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # or if package output interface end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE OUTPUT INTERFACE END":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # clear counter of subsection errors
                ConfigChecker.number_of_subsection_errors = 0
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_LOCAL_DATA_START

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_OUTPUT_INTERFACE, ConfigChecker.file_index + 1,
                                          "")
                # increment number of subsection errors
                ConfigChecker.number_of_subsection_errors = ConfigChecker.number_of_subsection_errors + 1
                # if number of subsection errors is greater than skipping threshold
                if ConfigChecker.number_of_subsection_errors >= ConfigChecker.NUMBER_OF_REPETITIONS_BEFORE_SKIPPING:
                    # skip part of the configuration file and find next module section
                    ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION
                else:
                    # increment file index and repeat same state
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

        # for package local data start check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_LOCAL_DATA_START:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package local data in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

            # if package local data start is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE LOCAL DATA START":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_LOCAL_DATA

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_LOCAL_INTERFACE, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for package local data check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_LOCAL_DATA:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package local data in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

            # if type and name in local data is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("type ") ==
                ConfigChecker.INTERFACE_TYPE_MARKER_POSITION_IN_CFG) and \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find(" name ") >
                     ConfigChecker.INTERFACE_NAME_MARKER_POSITION_IN_CFG):
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # or if package local data end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE LOCAL DATA END":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # clear counter of subsection errors
                ConfigChecker.number_of_subsection_errors = 0
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_BODY_START

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

        # for package body start check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_BODY_START:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package body in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

            # if package body start is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE BODY START":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_BODY

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_BODY, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.checker_state = ConfigChecker.SKIP_AND_FIND_MODULE_SECTION

        # for package body check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_BODY:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package body in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

            # if instruction or comment is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("INV ") ==
                ConfigChecker.BODY_DEFINITION_MARKER_POSITION_IN_CFG) or \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find("ASI ") ==
                     ConfigChecker.BODY_DEFINITION_MARKER_POSITION_IN_CFG) or \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find("COM ") ==
                     ConfigChecker.BODY_DEFINITION_MARKER_POSITION_IN_CFG):
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # or if package body end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE BODY END":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # clear counter of subsection errors
                ConfigChecker.number_of_subsection_errors = 0
                # move to next state
                ConfigChecker.checker_state = ConfigChecker.CHECK_PACKAGE_END

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

        # for package end check
        elif ConfigChecker.checker_state == ConfigChecker.CHECK_PACKAGE_END:

            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Checking package end in the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)

            # if package end is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "PACKAGE END":
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
    # This method checks correctness of footer in the configuration file.
    @staticmethod
    def check_footer():

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Checking footer of the configuration file at line "
                                + str(ConfigChecker.file_index + 1),
                                False)

        # increment file index once config file end marker was found
        ConfigChecker.file_index = ConfigChecker.file_index + 1

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

    # Description:
    # This method checks if given module name was already defined in the configuration file.
    @staticmethod
    def check_if_same_module_name(module_name):

        # for all names from module name list
        for name in ConfigChecker.module_name_list:
            # check if name is same as given module name
            if name == module_name:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_SAME_MODULE_NAME, module_name, "")
                print("yes1")
                # exit 'for name in' loop
                break

        # append name to list of module names
        ConfigChecker.module_name_list.append(module_name)

        # remove duplicates from module name list
        ConfigChecker.module_name_list = list(set(ConfigChecker.module_name_list))

    # Description:
    # This method checks if given operation name was already defined in the configuration file.
    @staticmethod
    def check_if_same_operation_name(operation_name):

        # for all names from operation name list
        for name in ConfigChecker.operation_name_list:
            # check if name is same as given operation name
            if name == operation_name:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_SAME_OPERATION_NAME, operation_name, "")
                print("yes2")
                # exit 'for name in' loop
                break

        # append name to list of operation names
        ConfigChecker.operation_name_list.append(operation_name)

        # remove duplicates from operation name list
        ConfigChecker.operation_name_list = list(set(ConfigChecker.operation_name_list))
