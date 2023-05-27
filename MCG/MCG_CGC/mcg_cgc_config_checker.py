#   FILE:           mcg_cgc_config_checker.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigChecker class, which is
#       responsible for verification of the configuration file data.
#
#   COPYRIGHT:      Copyright (C) 2022-2023 Kamil Deć github.com/deckamil
#   DATE:           27 MAY 2023
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
    BASE_MARKER_POSITION = 0

    # main verification state
    main_checker_state = ""

    # possible checker states
    MAIN_CHECK_HEADER = 100
    MAIN_FIND_NEW_MODULE = 200
    MAIN_CHECK_MODULE_NAME = 301
    MAIN_CHECK_OPERATION_NAME = 302
    MAIN_CHECK_INPUT_INTERFACE_START = 303
    MAIN_CHECK_INPUT_INTERFACE = 304
    MAIN_CHECK_OUTPUT_INTERFACE_START = 305
    MAIN_CHECK_OUTPUT_INTERFACE = 306
    MAIN_CHECK_LOCAL_INTERFACE_START = 307
    MAIN_CHECK_LOCAL_INTERFACE = 308
    MAIN_CHECK_MODULE_BODY_START = 309
    MAIN_CHECK_MODULE_BODY = 310
    MAIN_CHECK_MODULE_END = 311
    MAIN_SKIP_TO_NEXT_SECTION = 400
    MAIN_CHECK_FOOTER = 500
    MAIN_END_CHECKING = 600

    # body verification state
    body_checker_state = ""

    # possible body operation checker states
    BODY_NO_CHECK = 1500
    BODY_CHECK_INPUT_INTERFACE = 1600
    BODY_CHECK_OUTPUT_INTERFACE = 1700

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
        ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_HEADER
        ConfigChecker.body_checker_state = ConfigChecker.BODY_NO_CHECK

        # continue checking until verification of the configuration file is completed
        while ConfigChecker.main_checker_state != ConfigChecker.MAIN_END_CHECKING:

            # when file index is out of range
            if ConfigChecker.file_index >= ConfigChecker.number_of_config_file_lines:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_EOF, ConfigChecker.file_index + 1, "")
                # end configuration check
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_END_CHECKING

            # when line is empty
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "":
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # check header
            elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_HEADER:
                ConfigChecker.check_header()

            # find new module
            elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_FIND_NEW_MODULE:
                ConfigChecker.find_new_module()

            # check module name
            elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_MODULE_NAME:
                ConfigChecker.check_module_name()

            # check operation name
            elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_OPERATION_NAME:
                ConfigChecker.check_operation_name()

            # check interface
            elif (ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_INPUT_INTERFACE_START or
                  ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_INPUT_INTERFACE or
                  ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_OUTPUT_INTERFACE_START or
                  ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_OUTPUT_INTERFACE or
                  ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_LOCAL_INTERFACE_START or
                  ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_LOCAL_INTERFACE):
                ConfigChecker.check_interface()

            # check module body
            elif (ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_MODULE_BODY_START or
                  ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_MODULE_BODY):
                ConfigChecker.check_module_body()

            # check module end
            elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_MODULE_END:
                ConfigChecker.check_module_end()

            # check footer
            elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_FOOTER:
                ConfigChecker.check_footer()

            # skip current part of module section and find next one
            elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_SKIP_TO_NEXT_SECTION:
                ConfigChecker.skip_to_next_section()

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
        ConfigChecker.main_checker_state = ConfigChecker.MAIN_FIND_NEW_MODULE

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
            ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_MODULE_NAME

        # when config end marker is found
        elif "MCG CGC CONFIG END" in ConfigChecker.config_file[ConfigChecker.file_index]:
            # record info
            Logger.save_in_log_file("ConfigChecker",
                                    "Have found footer of the configuration file at line " +
                                    str(ConfigChecker.file_index + 1),
                                    False)
            # start footer verification
            ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_FOOTER

        # or when line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_START_OR_FOOTER, ConfigChecker.file_index+1, "")
            # skip part of the configuration file and find next section
            ConfigChecker.main_checker_state = ConfigChecker.MAIN_SKIP_TO_NEXT_SECTION

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
            ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_OPERATION_NAME

        # or if line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_MODULE_NAME, ConfigChecker.file_index + 1, "")
            # skip part of the configuration file and find next module section
            ConfigChecker.main_checker_state = ConfigChecker.MAIN_SKIP_TO_NEXT_SECTION

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
            ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_INPUT_INTERFACE_START

        # or if line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_OPERATION_NAME, ConfigChecker.file_index + 1, "")
            # skip part of the configuration file and find next module section
            ConfigChecker.main_checker_state = ConfigChecker.MAIN_SKIP_TO_NEXT_SECTION

    # Description:
    # This method checks correctness of input, output or local interface section in the configuration file.
    @staticmethod
    def check_interface():

        # method setup depending on checker state
        if ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_INPUT_INTERFACE_START:
            marker = "$INPUT "
            info = "input"
            error_code = ErrorHandler.CHK_ERR_FAULTY_INPUT_INTERFACE
            next_state = ConfigChecker.MAIN_CHECK_INPUT_INTERFACE

        elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_INPUT_INTERFACE:
            marker = "$INPUT "
            info = "input"
            error_code = ErrorHandler.CHK_ERR_FAULTY_INPUT_INTERFACE
            next_state = ConfigChecker.MAIN_CHECK_OUTPUT_INTERFACE_START

        elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_OUTPUT_INTERFACE_START:
            marker = "$OUTPUT "
            info = "output"
            error_code = ErrorHandler.CHK_ERR_FAULTY_OUTPUT_INTERFACE
            next_state = ConfigChecker.MAIN_CHECK_OUTPUT_INTERFACE

        elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_OUTPUT_INTERFACE:
            marker = "$OUTPUT "
            info = "output"
            error_code = ErrorHandler.CHK_ERR_FAULTY_OUTPUT_INTERFACE
            next_state = ConfigChecker.MAIN_CHECK_LOCAL_INTERFACE_START

        elif ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_LOCAL_INTERFACE_START:
            marker = "$LOCAL "
            info = "local"
            error_code = ErrorHandler.CHK_ERR_FAULTY_LOCAL_INTERFACE
            next_state = ConfigChecker.MAIN_CHECK_LOCAL_INTERFACE

        else:
            marker = "$LOCAL "
            info = "local"
            error_code = ErrorHandler.CHK_ERR_FAULTY_LOCAL_INTERFACE
            next_state = ConfigChecker.MAIN_CHECK_MODULE_BODY_START

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Checking " + info + " interface in the configuration file at line "
                                + str(ConfigChecker.file_index + 1),
                                False)

        # for interface start check
        if (ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_INPUT_INTERFACE_START or
                ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_OUTPUT_INTERFACE_START or
                ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_LOCAL_INTERFACE_START):

            # if interface start marker is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == str(marker + "INTERFACE START$"):
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.main_checker_state = next_state

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(error_code, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_SKIP_TO_NEXT_SECTION

        # otherwise for interface check
        else:

            # if type and name in input interface is found
            if (ConfigChecker.config_file[ConfigChecker.file_index].find("type ") ==
                ConfigChecker.BASE_MARKER_POSITION) and \
                    (ConfigChecker.config_file[ConfigChecker.file_index].find(" name ") >
                     ConfigChecker.BASE_MARKER_POSITION):
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # or if interface end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == str(marker + "INTERFACE END$"):
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # clear counter of subsection errors
                ConfigChecker.number_of_subsection_errors = 0
                # move to next state
                ConfigChecker.main_checker_state = next_state

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(error_code, ConfigChecker.file_index + 1, "")
                # increment number of subsection errors
                ConfigChecker.number_of_subsection_errors = ConfigChecker.number_of_subsection_errors + 1
                # if number of subsection errors is greater than skipping threshold
                if ConfigChecker.number_of_subsection_errors >= ConfigChecker.NUMBER_OF_REPETITIONS_BEFORE_SKIPPING:
                    # skip part of the configuration file and find next module section
                    ConfigChecker.main_checker_state = ConfigChecker.MAIN_SKIP_TO_NEXT_SECTION
                else:
                    # increment file index and repeat same state
                    ConfigChecker.file_index = ConfigChecker.file_index + 1

    # Description:
    # This method checks correctness of module body section in the configuration file.
    @staticmethod
    def check_module_body():

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Checking module body in the configuration file at line "
                                + str(ConfigChecker.file_index + 1),
                                False)

        # for module body start check
        if ConfigChecker.main_checker_state == ConfigChecker.MAIN_CHECK_MODULE_BODY_START:

            # if interface start marker is found
            if ConfigChecker.config_file[ConfigChecker.file_index] == "$MODULE BODY START$":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_MODULE_BODY

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_BODY, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_SKIP_TO_NEXT_SECTION

        # otherwise for module body check
        else:

            # if instruction marker is found
            if ConfigChecker.config_file[ConfigChecker.file_index].find("$INS ") == \
                    ConfigChecker.BASE_MARKER_POSITION:
                # increment file index and repeat same state process
                ConfigChecker.file_index = ConfigChecker.file_index + 1

            # or if operation marker is found:
            elif ConfigChecker.config_file[ConfigChecker.file_index].find("$OPE ") == \
                    ConfigChecker.BASE_MARKER_POSITION:
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next sub-state
                ConfigChecker.body_checker_state = ConfigChecker.BODY_CHECK_INPUT_INTERFACE

            # or if body operation input interface check state is entered
            elif ConfigChecker.body_checker_state == ConfigChecker.BODY_CHECK_INPUT_INTERFACE:

                # if input interface marker is found
                if ConfigChecker.config_file[ConfigChecker.file_index].find("$INP ") == \
                        ConfigChecker.BASE_MARKER_POSITION:
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                else:
                    # move to next sub-state
                    ConfigChecker.body_checker_state = ConfigChecker.BODY_CHECK_OUTPUT_INTERFACE

            # or if body operation output interface check state is entered
            elif ConfigChecker.body_checker_state == ConfigChecker.BODY_CHECK_OUTPUT_INTERFACE:

                # if output interface marker is found
                if ConfigChecker.config_file[ConfigChecker.file_index].find("$OUT ") == \
                        ConfigChecker.BASE_MARKER_POSITION:
                    # increment file index and repeat same state process
                    ConfigChecker.file_index = ConfigChecker.file_index + 1
                else:
                    # no further body operation check
                    ConfigChecker.body_checker_state = ConfigChecker.BODY_NO_CHECK

            # or if module body end is found
            elif ConfigChecker.config_file[ConfigChecker.file_index] == "$MODULE BODY END$":
                # increment file index
                ConfigChecker.file_index = ConfigChecker.file_index + 1
                # move to next state
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_MODULE_END

            # or if line contains unexpected data
            else:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_BODY, ConfigChecker.file_index + 1, "")
                # skip part of the configuration file and find next module section
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_SKIP_TO_NEXT_SECTION

    # Description:
    # This method checks correctness of module end section in the configuration file.
    @staticmethod
    def check_module_end():

        # record info
        Logger.save_in_log_file("ConfigChecker",
                                "Checking module end in the configuration file at line "
                                + str(ConfigChecker.file_index + 1),
                                False)

        # if module end marker if found
        if ConfigChecker.config_file[ConfigChecker.file_index] == "$MODULE END$":
            # increment file index
            ConfigChecker.file_index = ConfigChecker.file_index + 1
            # move to next state
            ConfigChecker.main_checker_state = ConfigChecker.MAIN_FIND_NEW_MODULE

        # or if line contains unexpected data
        else:
            # record error
            ErrorHandler.record_error(ErrorHandler.CHK_ERR_FAULTY_END, ConfigChecker.file_index + 1, "")
            # skip part of the configuration file and find next module section
            ConfigChecker.main_checker_state = ConfigChecker.MAIN_SKIP_TO_NEXT_SECTION

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
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_END_CHECKING

            # when line is NOT empty
            elif ConfigChecker.config_file[ConfigChecker.file_index] != "":
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_DATA_AFTER_FOOTER, ConfigChecker.file_index + 1, "")

            # increment file index and repeat same state process
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
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_END_CHECKING

            # when module name is found
            elif ConfigChecker.config_file[temporary_file_index] == "$MODULE NAME START$":
                # move to expected state
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_MODULE_NAME

            # when operation name is found
            elif ConfigChecker.config_file[temporary_file_index] == "$OPERATION NAME START$":
                # move to expected state
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_OPERATION_NAME

            # when input interface is found
            elif ConfigChecker.config_file[temporary_file_index] == "$INPUT INTERFACE START$":
                # move to expected state
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_INPUT_INTERFACE_START

            # when output interface is found
            elif ConfigChecker.config_file[temporary_file_index] == "$OUTPUT INTERFACE START$":
                # move to expected state
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_OUTPUT_INTERFACE_START

            # when local interface is found
            elif ConfigChecker.config_file[temporary_file_index] == "$LOCAL INTERFACE START$":
                # move to expected state
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_LOCAL_INTERFACE_START

            # when module body is found
            elif ConfigChecker.config_file[temporary_file_index] == "$MODULE BODY START$":
                # move to expected state
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_MODULE_BODY_START

            # when config end marker is found
            elif "MCG CGC CONFIG END" in ConfigChecker.config_file[temporary_file_index]:
                # move to expected state
                ConfigChecker.main_checker_state = ConfigChecker.MAIN_CHECK_FOOTER

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
    # This method checks if given module name was already defined in the configuration file.
    @staticmethod
    def check_if_same_module_name(module_name):

        # for all names from module name list
        for name in ConfigChecker.module_name_list:
            # check if name is same as given module name
            if name == module_name:
                # record error
                ErrorHandler.record_error(ErrorHandler.CHK_ERR_SAME_MODULE_NAME, module_name, "")
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
                # exit 'for name in' loop
                break

        # append name to list of operation names
        ConfigChecker.operation_name_list.append(operation_name)

        # remove duplicates from operation name list
        ConfigChecker.operation_name_list = list(set(ConfigChecker.operation_name_list))
