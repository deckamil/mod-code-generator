#   FILE:           mcg_cc_component_reader.py
#
#   DESCRIPTION:
#       This module contains definition of ComponentReader class, which is child
#       class of FileReader class and is responsible for reading of component content,
#       i.e. activity diagram and interface details from .exml files.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           26 JAN 2022
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


# Class:
# ComponentReader()
#
# Description:
# This is child class responsible for reading of component .exml file content.
class ComponentReader(FileReader):

    # This list defines all valid action types.
    action_type_list = ["ADD", "SUB"]

    # This list defines all valid action types, which requires in addition first input signal marker.
    action_type_with_first_input_signal_list = ["SUB"]

    # Function:
    # check_correctness()
    #
    # Description:
    # This function checks correctness of component content.
    #
    # Returns:
    # This function does not return anything.
    def check_correctness(self):

        # check correctness
        Logger.save_in_log_file("*** check correctness")

        # check signal-related errors
        self.check_signal_errors()

        # check action-related errors
        self.check_action_errors()

        # check interface-related errors
        self.check_interface_errors()

    # Function:
    # check_signal_errors()
    #
    # Description:
    # This function checks any signal-related errors and issues.
    #
    # Returns:
    # This function does not return anything.
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

    # Function:
    # check_action_errors()
    #
    # Description:
    # This function checks any action-related errors and issues.
    #
    # Returns:
    # This function does not return anything.
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

    # Function:
    # check_interface_errors()
    #
    # Description:
    # This function checks any interface-related errors and issues.
    #
    # Returns:
    # This function does not return anything.
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

    # Method:
    # check_if_action_type()
    #
    # Description:
    # This method checks if reference contains valid action type.
    #
    # Returns:
    # This method returns action marker.
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

    # Method:
    # check_if_action_type_with_first_input_signal()
    #
    # Description:
    # This method checks if reference contains valid action type, which requires in addition first input signal marker.
    #
    # Returns:
    # This method returns action marker.
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

    # Function:
    # find_first_input_signal_name()
    #
    # Description:
    # This function looks for first input signal, recognized by $FIRST$ marker, of given target action.
    #
    # Returns:
    # This function returns first input signal name.
    def find_first_input_signal_name(self, target_action, target_action_uid):
        # local data
        first_input_signal_name = ""

        # search for above actions in file content
        for i in range(0, len(self.activity_file)):

            # if given line contains definition of action
            if ("<OBJECT>" in self.activity_file[i]) and ("<ID name=" in self.activity_file[i + 1]) and \
                    ("Standard.OpaqueAction" in self.activity_file[i + 1]) and \
                    (target_action_uid in self.activity_file[i + 1]):

                # search for first input signal of above action
                for j in range(i, len(self.activity_file)):

                    # if given line contains details about first input signal
                    if ("<ATT name=" in self.activity_file[j]) and ("$FIRST$" in self.activity_file[j]):
                        # get line
                        line = self.activity_file[j]
                        # find start marker of first input signal
                        first_input_start = line.find("$FIRST$")
                        # find end marker of first input signal
                        first_input_end = line.rfind("$FIRST$")
                        # check if $FIRST$ marker is found
                        if (first_input_start == -1) or (first_input_end == -1) or \
                                (first_input_start == first_input_end):
                            # set empty first input signal name
                            first_input_signal_name = ""
                        else:
                            # get first input signal name
                            first_input_signal_name = line[first_input_start + Supporter.FIRST_INPUT_SIGNAL_OFFSET:
                                                           first_input_end - 1]

        # if signal is not found
        if first_input_signal_name == "":
            # record error
            ErrorHandler.record_error(ErrorHandler.ACT_ERR_NO_FIRST_INPUT, target_action, "none")
            # set error signal
            first_input_signal_name = "FIRST_INPUT_SIGNAL_NOT_FOUND"

        # return first input signal name
        return first_input_signal_name

    # Function:
    # read_data_targets()
    #
    # Description:
    # This function looks data targets, i.e. component signals and their targets from activity diagram.
    #
    # Returns:
    # This function does not return anything.
    def read_data_targets(self):

        # read data targets
        Logger.save_in_log_file("*** read data targets")

        # search for signals in activity file
        for i in range(0, len(self.activity_file)):

            # if given line contains definition of signal name
            if ("<ID name=" in self.activity_file[i]) and ("Standard.Attribute" in self.activity_file[i]):
                # get line
                line = self.activity_file[i]
                # get line number
                line_number = i + 1
                # get signal name
                signal_name = ComponentReader.get_name(line, line_number)
                # append signal name to data list
                self.data_list.append(signal_name)

                # signal marker shows whether signal target has been found or not
                signal_has_targets = False

                # search for targets
                for j in range(i, len(self.activity_file)):

                    # new connection instance
                    connection = Connection()

                    # if line contains <COMP that means the signal has some targets
                    if "<COMP" in self.activity_file[j]:
                        # change signal marker
                        signal_has_targets = True

                    # if line contains </DEPENDENCIES> then signal does not have any target
                    if ("</DEPENDENCIES>" in self.activity_file[j]) and (not signal_has_targets):
                        # set connection source
                        connection.connection_source = signal_name
                        # set connection $EMPTY$ target
                        connection.connection_target = "$EMPTY$"
                        # append connection to connection list
                        self.connection_list.append(connection)
                        # exit "for j in range" loop
                        break

                    # if line contain <LINK relation="Target"> that means target for given signal
                    if ("<LINK relation=" in self.activity_file[j]) and ("Target" in self.activity_file[j]):
                        # if action is target of given signal
                        if ("<ID name=" in self.activity_file[j + 2]) and \
                                ("Standard.OpaqueAction" in self.activity_file[j + 2]):
                            # get line
                            line = self.activity_file[j + 2]
                            # get line number
                            line_number = j + 3
                            # get target action type
                            target_action_type = ComponentReader.get_name(line, line_number)
                            # get target action uid
                            target_action_uid = ComponentReader.get_uid(line, line_number)
                            # get target action
                            target_action = str(target_action_type) + " " + str(target_action_uid)

                            # first input signal is not needed
                            first_input_signal_needed = False

                            # check if target action requires first input signal
                            action_type_with_first_input_signal_found = ComponentReader. \
                                check_if_action_type_with_first_input_signal(target_action_type)

                            # if this type of action requires first input signal
                            if action_type_with_first_input_signal_found:

                                # find first input signal name in file content
                                first_input_signal_name = self.find_first_input_signal_name(target_action,
                                                                                            target_action_uid)

                                # if first input signal name is same as current signal
                                if signal_name == first_input_signal_name:
                                    # first input signal is needed
                                    first_input_signal_needed = True

                            # set connection source with or without $FIRST$ input signal marker
                            if first_input_signal_needed:
                                connection.connection_source = "$FIRST$ " + signal_name
                            else:
                                connection.connection_source = signal_name

                            # set connection target
                            connection.connection_target = target_action
                            # append connection to connection list
                            self.connection_list.append(connection)

                        # if signal is target of given signal
                        if ("<ID name=" in self.activity_file[j + 2]) and \
                                ("Standard.InstanceNode" in self.activity_file[j + 2]):
                            # get line
                            line = self.activity_file[j + 2]
                            # get line number
                            line_number = j + 3
                            # get target signal uid
                            target_signal_uid = ComponentReader.get_uid(line, line_number)
                            # find target signal name
                            target_signal_list = self.find_target_element_name(target_signal_uid, "Standard.Attribute")

                            # get target signal marker
                            target_signal_found = target_signal_list[ComponentReader.TARGET_ELEMENT_FOUND_INDEX]
                            # get target signal name
                            target_signal_name = target_signal_list[ComponentReader.TARGET_ELEMENT_NAME_INDEX]

                            # if target signal was not found
                            if not target_signal_found:
                                # record error
                                ErrorHandler.record_error(ErrorHandler.SIG_ERR_NO_SIG_UID_TARGET,
                                                          target_signal_uid,
                                                          signal_name)

                            # set connection source
                            connection.connection_source = signal_name
                            # set connection target
                            connection.connection_target = target_signal_name
                            # append connection to connection list
                            self.connection_list.append(connection)

                    # if line contains </COMP> that means end of targets for given signal
                    if "</COMP>" in self.activity_file[j]:
                        # exit "for j in range" loop
                        break

        # remove duplicates from data list
        self.data_list = list(set(self.data_list))

    # Function:
    # read_interaction_targets()
    #
    # Description:
    # This function looks interaction targets, i.e. component actions and their targets from activity diagram.
    #
    # Returns:
    # This function does not return anything.
    def read_interaction_targets(self):

        # read interaction targets
        Logger.save_in_log_file("*** read interaction targets")

        # search for actions in activity file
        for i in range(0, len(self.activity_file)):

            # if given line contains definition of action
            if ("<OBJECT>" in self.activity_file[i]) and ("<ID name=" in self.activity_file[i + 1]) and \
                    ("Standard.OpaqueAction" in self.activity_file[i + 1]):
                # get line
                line = self.activity_file[i + 1]
                # get line number
                line_number = i + 2
                # get action type
                action_type = ComponentReader.get_name(line, line_number)
                # get action uid
                action_uid = ComponentReader.get_uid(line, line_number)
                # get action
                action = str(action_type) + " " + str(action_uid)
                # append action to interaction list
                self.interaction_list.append(action)

                # action marker shows whether action target has been found or not
                action_has_targets = False

                # search for targets
                for j in range(i, len(self.activity_file)):

                    # new connection instance
                    connection = Connection()

                    # if line contains <COMP that means the action has some targets
                    if "<COMP" in self.activity_file[j]:
                        # change action marker
                        action_has_targets = True

                    # if line contains </DEPENDENCIES> then action does not have any target
                    if ("</DEPENDENCIES>" in self.activity_file[j]) and (not action_has_targets):
                        # record error
                        ErrorHandler.record_error(ErrorHandler.ACT_ERR_NO_TARGET, action, "none")
                        # exit "for j in range" loop
                        break

                    # if line contain <LINK relation="Target"> that means target for given action
                    if ("<LINK relation=" in self.activity_file[j]) and ("Target" in self.activity_file[j]):
                        # if action is target of given action
                        if ("<ID name=" in self.activity_file[j + 2]) and \
                                ("Standard.OpaqueAction" in self.activity_file[j + 2]):
                            # record error
                            ErrorHandler.record_error(ErrorHandler.ACT_ERR_ACT_IS_TARGET, action, "none")

                        # if signal is target of given action
                        if ("<ID name=" in self.activity_file[j + 2]) and \
                                ("Standard.InstanceNode" in self.activity_file[j + 2]):
                            # get line
                            line = self.activity_file[j + 2]
                            # get line number
                            line_number = j + 3
                            # get target signal uid
                            target_signal_uid = ComponentReader.get_uid(line, line_number)
                            # find target signal name
                            target_signal_list = self.find_target_element_name(target_signal_uid, "Standard.Attribute")

                            # get target signal marker
                            target_signal_found = target_signal_list[ComponentReader.TARGET_ELEMENT_FOUND_INDEX]
                            # get target signal name
                            target_signal_name = target_signal_list[ComponentReader.TARGET_ELEMENT_NAME_INDEX]

                            # if target signal was not found
                            if not target_signal_found:
                                # record error
                                ErrorHandler.record_error(ErrorHandler.ACT_ERR_NO_SIG_UID_TARGET,
                                                          target_signal_uid,
                                                          action)

                            # set connection source
                            connection.connection_source = action
                            # set connection target
                            connection.connection_target = target_signal_name
                            # append connection to connection list
                            self.connection_list.append(connection)

                    # if line contains </COMP> that means end of targets for given signal
                    if "</COMP>" in self.activity_file[j]:
                        # exit "for j in range" loop
                        break

        # remove duplicates from interaction list
        self.interaction_list = list(set(self.interaction_list))

    # Method:
    # read_component()
    #
    # Description:
    # This method is responsible for reading of component details.
    #
    # Returns:
    # This method returns component reader list, which describes component content and its activity.
    def read_component(self):

        # component reader
        Logger.save_in_log_file(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> COMPONENT READER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

        # search for signals target within activity file
        self.read_data_targets()

        # search for action targets within activity file
        self.read_interaction_targets()

        # search for interface elements
        self.read_interface_elements()

        # check component correctness
        self.check_correctness()

        # process completed
        Logger.save_in_log_file("PROCESS COMPLETED")

        # display additional details after component reading
        Logger.save_in_log_file("")
        Logger.save_in_log_file("Connections:")
        for connection in self.connection_list:
            Logger.save_in_log_file("          " + str(connection))
        Logger.save_in_log_file("Actions:")
        for interaction in self.interaction_list:
            Logger.save_in_log_file("          " + str(interaction))
        Logger.save_in_log_file("Signals:")
        for data in self.data_list:
            Logger.save_in_log_file("          " + str(data))
        Logger.save_in_log_file("Input Interface:")
        for input_interface in self.input_interface_list:
            Logger.save_in_log_file("          " + str(input_interface))
        Logger.save_in_log_file("Output Interface:")
        for output_interface in self.output_interface_list:
            Logger.save_in_log_file("          " + str(output_interface))
        Logger.save_in_log_file("Local Data:")
        for local_data in self.local_data_list:
            Logger.save_in_log_file("          " + str(local_data))

        # end of component reader
        Logger.save_in_log_file("\n>>>>>>>>>>>>>>>>>>>>>>>>>> END OF COMPONENT READER <<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # append collected data to component reader list
        component_reader_list = []
        component_reader_list.insert(ComponentReader.MODEL_ELEMENT_NAME_INDEX, self.model_element_name)
        component_reader_list.insert(ComponentReader.ACTIVITY_SOURCE_INDEX, self.activity_source)
        component_reader_list.insert(ComponentReader.CONNECTION_LIST_INDEX, self.connection_list)
        component_reader_list.insert(ComponentReader.INTERACTION_LIST_INDEX, self.interaction_list)
        component_reader_list.insert(ComponentReader.INPUT_INTERFACE_LIST_INDEX, self.input_interface_list)
        component_reader_list.insert(ComponentReader.OUTPUT_INTERFACE_LIST_INDEX, self.output_interface_list)
        component_reader_list.insert(ComponentReader.LOCAL_DATA_LIST_INDEX, self.local_data_list)

        # return component reader list
        return component_reader_list
