#   FILE:           mcg_cc_file_checker.py
#
#   DESCRIPTION:
#       This module contains definition of FileChecker class, which is
#       responsible for checking of model module content from .exml file.
#
#   COPYRIGHT:      Copyright (C) 2021-2023 Kamil Deć github.com/deckamil
#   DATE:           13 JUN 2023
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


from mcg_cc_file_reader import FileReader
from mcg_cc_error_handler import ErrorHandler
from mcg_cc_logger import Logger
from mcg_cc_connection import Connection


# Description:
# This class allows to check model module content from .exml files.
class FileChecker(object):

    # list of actions types
    action_3letter_type_list = ["ADD", "SUB", "MUL", "DIV", "AND", "NOT"]

    action_2letter_type_list = ["OR"]

    # list of interface element types
    interface_element_type_list = ["INT8", "INT16", "INT32", "INT64",
                                   "UINT8", "UINT16", "UINT32", "UINT64",
                                   "FLOAT32", "FLOAT64",
                                   "BOOL"]

    # Description:
    # This is class constructor.
    def __init__(self, file_reader_list):

        # initialize object data
        self.connection_list = file_reader_list[FileReader.CONNECTION_LIST_INDEX]
        self.input_interface_list = file_reader_list[FileReader.INPUT_INTERFACE_LIST_INDEX]
        self.output_interface_list = file_reader_list[FileReader.OUTPUT_INTERFACE_LIST_INDEX]
        self.local_interface_list = file_reader_list[FileReader.LOCAL_INTERFACE_LIST_INDEX]

    # Description:
    # This method checks any connection-related errors and issues.
    def check_connection_errors(self):

        # record info
        Logger.save_in_log_file("FileChecker", "Looking for connection errors in .exml file", False)

        # check action types in connections
        for connection in self.connection_list:
            # if action is connection source
            if connection.source_type == Connection.ACTION:

                # check if action type is valid
                action_type_valid = FileChecker.check_action_type(connection.source_name)

                # if action type is not valid
                if not action_type_valid:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CON_ERR_INVALID_ACTION_TYPE, connection, "none")

            # if action is connection target
            if connection.target_type == Connection.ACTION:
                # check if action type is valid
                action_type_valid = FileChecker.check_action_type(connection.target_name)

                # if action type is not valid
                if not action_type_valid:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.CON_ERR_INVALID_ACTION_TYPE, connection, "none")

    # Description:
    # This method checks if action type is valid.
    @staticmethod
    def check_action_type(action_type_ref):
        # result flag
        action_type_valid = False

        # check 3-letter action types
        if len(action_type_ref) > 2:

            # for all possible action types
            for action_type in FileChecker.action_3letter_type_list:
                # if action type is the same as in reference
                if action_type == action_type_ref[0:3]:
                    # set flag
                    action_type_valid = True
                    # exit loop
                    break

        # check 2-letter action types
        elif len(action_type_ref) < 3:

            # for all possible action types
            for action_type in FileChecker.action_2letter_type_list:
                # if action type is the same as in reference
                if action_type == action_type_ref[0:2]:
                    # set flag
                    action_type_valid = True
                    # exit loop
                    break

        # return flag
        return action_type_valid

    # Description:
    # This method checks any interface-related errors and issues.
    def check_interface_errors(self):

        # record info
        Logger.save_in_log_file("FileChecker", "Looking for interface errors in .exml file", False)

        # check interface element types in input interface
        for interface_element in self.input_interface_list:
            # get interface element type
            interface_element_type = interface_element[FileReader.INTERFACE_ELEMENT_TYPE_INDEX]
            # check interface element type
            interface_element_type_valid = FileChecker.check_interface_element_type(interface_element_type)

            # if data type not valid
            if not interface_element_type_valid:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_INVALID_INTERFACE_ELEMENT_TYPE, interface_element, "none")

        # check interface element types in output interface
        for interface_element in self.output_interface_list:
            # get interface element type
            interface_element_type = interface_element[FileReader.INTERFACE_ELEMENT_TYPE_INDEX]
            # check interface element type
            interface_element_type_valid = FileChecker.check_interface_element_type(interface_element_type)

            # if data type not valid
            if not interface_element_type_valid:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_INVALID_INTERFACE_ELEMENT_TYPE, interface_element, "none")

        # check interface element types in local interface
        for interface_element in self.local_interface_list:
            # get interface element type
            interface_element_type = interface_element[FileReader.INTERFACE_ELEMENT_TYPE_INDEX]
            # check interface element type
            interface_element_type_valid = FileChecker.check_interface_element_type(interface_element_type)

            # if data type not valid
            if not interface_element_type_valid:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_INVALID_INTERFACE_ELEMENT_TYPE, interface_element, "none")

    # Description:
    # This method checks if interface element type is valid.
    @staticmethod
    def check_interface_element_type(interface_element_type_ref):
        # result flag
        interface_element_type_valid = False

        # for all possible interface element types
        for interface_element_type in FileChecker.interface_element_type_list:
            # if interface element type is the same as in reference
            if interface_element_type == interface_element_type_ref:
                # set flag
                interface_element_type_valid = True
                # exit loop
                break

        # return flag
        return interface_element_type_valid

    # Description:
    # This method is responsible for checking of module details.
    def check_files(self):

        # record info
        Logger.save_in_log_file("FileChecker", "Checking module details from set of .exml files", True)

        # search for connection errors
        self.check_connection_errors()

        # search for interface errors
        self.check_interface_errors()


