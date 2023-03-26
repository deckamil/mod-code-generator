#   FILE:           mcg_cc_file_checker.py
#
#   DESCRIPTION:
#       This module contains definition of FileChecker class, which is
#       responsible for checking of model module content from .exml file.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           7 DEC 2022
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
from mcg_cc_supporter import Supporter
from mcg_cc_logger import Logger
from mcg_cc_connection import Connection


# Description:
# This class allows to check model module content from .exml files.
class FileChecker(object):

    # list of actions types
    action_type_list = ["ADD", "SUB", "MUL", "DIV"]

    # list of non-commutative actions types (where inputs order does matter)
    non_commutative_action_type_list = ["SUB", "DIV"]

    # list of data types
    data_type_list = ["INT8", "INT16", "INT32", "INT64",
                      "UINT8", "UINT16", "UINT32", "UINT64",
                      "FLOAT32", "FLOAT64"]

    # Description:
    # This is class constructor.
    def __init__(self, file_reader_list):

        # initialize object data
        self.connection_list = file_reader_list[FileReader.CONNECTION_LIST_INDEX]
        self.input_interface_list = file_reader_list[FileReader.INPUT_INTERFACE_LIST_INDEX]
        self.output_interface_list = file_reader_list[FileReader.OUTPUT_INTERFACE_LIST_INDEX]
        self.local_interface_list = file_reader_list[FileReader.LOCAL_INTERFACE_LIST_INDEX]

    # Description:
    # This method checks any signal-related errors and issues.
    def check_signal_errors(self):

        # *******************************************************************
        # check if any signal on data list has more than one input connection
        for signal_name in self.data_list:
            # input counter shows how many inputs (sources) are connected to given signal
            input_counter = 0

            # go through all connections for each signal
            for connection in self.connection_list:
                # if connection target is same as signal name, then it means that
                # signal has input connection (source)
                if connection.connection_target == signal_name:
                    # increment input counter
                    input_counter = input_counter + 1

            # if signal has more than one input connection
            if input_counter > 1:
                # record error
                ErrorHandler.record_error(ErrorHandler.SIG_ERR_MORE_INPUTS, signal_name, "none")

    # Description:
    # This method checks any action-related errors and issues.
    def check_action_errors(self):

        # ******************************************************
        # check if any action type is not valid
        for interaction in self.interaction_list:
            # get action type
            action_type = interaction[0:len(interaction) + Supporter.UID_OFFSET]

            # check if action type is valid
            action_type_found = ComponentReader.check_if_action_type(action_type)

            # if action type is not valid
            if not action_type_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.ACT_ERR_ACT_NOT_ALLOWED, interaction, "none")

    # Description:
    # This method checks any interface-related errors and issues.
    def check_interface_errors(self):

        # ************************************************************************
        # check if any signal used on diagram does not come from interface element
        for signal_name in self.data_list:
            # signal marker shows whether signal was found or not within interface element
            signal_found = False

            # if signal has not been found, search in input interface
            if not signal_found:
                # go through all input interface elements
                for interface_element in self.input_interface_list:

                    # get interface element name
                    interface_element_name = interface_element[ComponentReader.INTERFACE_ELEMENT_NAME_INDEX]

                    # if diagram signal is identified as interface element
                    if signal_name == interface_element_name:
                        # change signal marker
                        signal_found = True
                        # break "for interface_element in" loop
                        break

            # if signal has not been found, search in output interface
            if not signal_found:
                # go through all output interface elements
                for interface_element in self.output_interface_list:

                    # get interface element name
                    interface_element_name = interface_element[ComponentReader.INTERFACE_ELEMENT_NAME_INDEX]

                    # if diagram signal is identified as interface element
                    if signal_name == interface_element_name:
                        # change signal marker
                        signal_found = True
                        # break "for interface_element in" loop
                        break

            # if signal has not been found, search in local data interface
            if not signal_found:
                # go through all local data interface elements
                for interface_element in self.local_data_list:

                    # get interface element name
                    interface_element_name = interface_element[ComponentReader.INTERFACE_ELEMENT_NAME_INDEX]

                    # if diagram signal is identified as interface element
                    if signal_name == interface_element_name:
                        # change signal marker
                        signal_found = True
                        # break "for interface_element in" loop
                        break

            # if diagram signal is not found in interface element
            if not signal_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_SIG_NOT_IN_INT, signal_name, "none")

        # *****************************************************************************
        # check if any input interface signal type in not valid
        for interface_element in self.input_interface_list:
            # get interface element name
            interface_element_name = interface_element[ComponentReader.INTERFACE_ELEMENT_NAME_INDEX]
            # get interface element type
            interface_element_type = interface_element[ComponentReader.INTERFACE_ELEMENT_TYPE_INDEX]

            # check if interface element type is valid
            interface_element_type_found = ComponentReader.check_if_interface_element_type(interface_element_type,
                                                                                           "signal")

            # if interface element type is not valid
            if not interface_element_type_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_INC_INP_INT_TYPE_IN_COM, interface_element_name,
                                          interface_element_type)

        # *****************************************************************************
        # check if any output interface signal type in not valid
        for interface_element in self.output_interface_list:
            # get interface element name
            interface_element_name = interface_element[ComponentReader.INTERFACE_ELEMENT_NAME_INDEX]
            # get interface element type
            interface_element_type = interface_element[ComponentReader.INTERFACE_ELEMENT_TYPE_INDEX]

            # check if interface element type is valid
            interface_element_type_found = ComponentReader.check_if_interface_element_type(interface_element_type,
                                                                                           "signal")

            # if interface element type is not valid
            if not interface_element_type_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_INC_OUT_INT_TYPE_IN_COM, interface_element_name,
                                          interface_element_type)

        # *****************************************************************************
        # check if any local data signal type in not valid
        for interface_element in self.local_data_list:
            # get interface element name
            interface_element_name = interface_element[ComponentReader.INTERFACE_ELEMENT_NAME_INDEX]
            # get interface element type
            interface_element_type = interface_element[ComponentReader.INTERFACE_ELEMENT_TYPE_INDEX]

            # check if interface element type is valid
            interface_element_type_found = ComponentReader.check_if_interface_element_type(interface_element_type,
                                                                                           "signal")

            # if interface element type is not valid
            if not interface_element_type_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_INC_LOC_DAT_TYPE_IN_COM, interface_element_name,
                                          interface_element_type)

        # *****************************************************************************
        # check if any input interface signal is connected as output (target) of other element
        for interface_element in self.input_interface_list:
            # get interface element name
            interface_element_name = interface_element[ComponentReader.INTERFACE_ELEMENT_NAME_INDEX]

            # go through all connections for each interface element
            for connection in self.connection_list:
                # if connection target is same as interface element name, then it means that
                # input interface element is connected as output (target) of another element
                if connection.connection_target == interface_element_name:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.INT_ERR_INP_INT_SIG_IS_TAR_IN_COM,
                                              interface_element_name,
                                              connection.connection_source)

        # *****************************************************************************
        # check if any output interface signal is connected as input (source) of other element
        for interface_element in self.output_interface_list:
            # get interface element name
            interface_element_name = interface_element[ComponentReader.INTERFACE_ELEMENT_NAME_INDEX]

            # go through all connections for each interface element
            for connection in self.connection_list:
                # if connection source is same as interface element name, then it means that
                # output interface element is connected as input (source) of another element
                if (connection.connection_source == interface_element_name) and \
                        (connection.connection_target != "$EMPTY$"):
                    # record error
                    ErrorHandler.record_error(ErrorHandler.INT_ERR_OUT_INT_SIG_IS_SRC_IN_COM,
                                              interface_element_name,
                                              connection.connection_target)

    # Description:
    # This method checks if reference contains valid action type.
    @staticmethod
    def check_if_action_type(ref_action_type):
        # action type marker shows whether valid acton type was found or not within reference
        action_type_found = False

        # for all allowed action types
        for action_type in ComponentReader.action_type_list:
            # if action type is the same as in reference
            if action_type == ref_action_type:
                # change action type marker
                action_type_found = True
                # exit loop
                break

        # return action type marker
        return action_type_found

    # Description:
    # This method checks if reference contains valid action type, which requires in addition first input signal marker.
    @staticmethod
    def check_if_action_type_with_first_input_signal(ref_action_type_with_first_input_signal):
        # action type marker shows whether valid action type, which requires in addition first input signal marker,
        # was found or not within reference
        action_type_with_first_input_signal_found = False

        # for all allowed action types, which require in addition first input signal marker
        for action_type_with_first_input_signal in ComponentReader.action_type_with_first_input_signal_list:
            # if action type is the same as in reference
            if action_type_with_first_input_signal == ref_action_type_with_first_input_signal:
                # change action type marker
                action_type_with_first_input_signal_found = True
                # exit loop
                break

        # return action type marker
        return action_type_with_first_input_signal_found

    # Description:
    # This method is responsible for checking of module details.
    def check_files(self):

        # record info
        Logger.save_in_log_file("FileChecker", "Checking module details from set of .exml files", True)

