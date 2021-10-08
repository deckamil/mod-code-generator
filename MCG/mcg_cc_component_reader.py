#   FILE:           mcg_cc_component_reader.py
#
#   DESCRIPTION:
#       This module contains definition of ComponentReader class, which is child
#       class of FileReader class and is responsible for reading of component content,
#       i.e. activity diagram and interface details from .exml files.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           8 OCT 2021
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
#       You should have received a copy of the GNU General Public License
#       along with this program. If not, see <https://www.gnu.org/licenses/>.


import mcg_cc_supporter
import mcg_cc_error_handler
from mcg_cc_file_reader import FileReader
from mcg_cc_parameters import FIRST_INPUT_SIGNAL_OFFSET
from mcg_cc_parameters import MCG_CC_TEST_RUN
from mcg_cc_parameters import ACTION_UID_OFFSET


# Class:
# ComponentReader()
#
# Description:
# This is child class responsible for reading of component .exml file content.
class ComponentReader(FileReader):

    # Function:
    # check_correctness()
    #
    # Description:
    # This function checks correctness of component content.
    #
    # Returns:
    # This function does not return anything.
    def check_correctness(self):

        # check is any signal on data list has more than one source
        for data in self.data_list:
            keyword = "target " + str(data)
            keyword_occurrence = 0

            # go through all nodes for each signal
            for node in self.node_list:

                # if keyword within the node
                if keyword in node:
                    # increment keyword counter
                    keyword_occurrence = keyword_occurrence + 1

            # if keyword has more than one occurrence
            if keyword_occurrence > 1:
                # record error
                mcg_cc_error_handler.record_error(1, data, "none")

        # check if any action on interaction list is not allowed
        for interaction in self.interaction_list:
            # get action type
            action_type = interaction[0:len(interaction) + ACTION_UID_OFFSET]

            # check if action type is allowed
            action_type_found = mcg_cc_supporter.check_if_reference_contains_action_type(action_type)

            # if action type is not allowed
            if not action_type_found:
                # record error
                mcg_cc_error_handler.record_error(51, interaction, "none")

    # Function:
    # find_first_input_signal_name()
    #
    # Description:
    # This function looks for first input signal, recognized by *FIRST* marker, of given target action.
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
                    if ("<ATT name=" in self.activity_file[j]) and ("*FIRST*" in self.activity_file[j]):
                        # get line
                        line = self.activity_file[j]
                        # find start marker of first input signal
                        first_input_start = line.find("*FIRST*")
                        # find end marker of first input signal
                        first_input_end = line.rfind("*FIRST*")
                        # check if *FIRST* marker is found
                        if (first_input_start == -1) or (first_input_end == -1) or \
                                (first_input_start == first_input_end):
                            # set empty first input signal name
                            first_input_signal_name = ""
                        else:
                            # get first input signal name
                            first_input_signal_name = line[first_input_start + FIRST_INPUT_SIGNAL_OFFSET:
                                                           first_input_end - 1]

        # if signal is not found
        if first_input_signal_name == "":
            # record error
            mcg_cc_error_handler.record_error(22, target_action, "none")
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

                    # if line contains <COMP that means the signal has some targets
                    if "<COMP" in self.activity_file[j]:
                        # change signal marker
                        signal_has_targets = True

                    # if line contains </DEPENDENCIES> then signal does not have any target
                    if ("</DEPENDENCIES>" in self.activity_file[j]) and (not signal_has_targets):
                        # append node to node list
                        self.node_list.append(str(signal_name) + " target empty")
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
                            action_type_req_first_input_signal_found = mcg_cc_supporter. \
                                check_if_reference_contains_action_type_req_first_input_signal(target_action_type)

                            # if this type of action requires first input signal
                            if action_type_req_first_input_signal_found:

                                # find first input signal name in file content
                                first_input_signal_name = self.find_first_input_signal_name(target_action,
                                                                                            target_action_uid)

                                # if first input signal name is same as current signal
                                if signal_name in first_input_signal_name:
                                    # first input signal is needed
                                    first_input_signal_needed = True

                            # append node to node list
                            if first_input_signal_needed:
                                self.node_list.append("*FIRST* " + str(signal_name) + " *FIRST* target " +
                                                      str(target_action))
                            else:
                                self.node_list.append(str(signal_name) + " target " + str(target_action))

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
                                mcg_cc_error_handler.record_error(20, target_signal_uid, signal_name)
                            # append node to node list
                            self.node_list.append(str(signal_name) + " target " + str(target_signal_name))

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

                    # if line contains <COMP that means the action has some targets
                    if "<COMP" in self.activity_file[j]:
                        # change action marker
                        action_has_targets = True

                    # if line contains </DEPENDENCIES> then action does not have any target
                    if ("</DEPENDENCIES>" in self.activity_file[j]) and (not action_has_targets):
                        # record error
                        mcg_cc_error_handler.record_error(70, action, "none")
                        # exit "for j in range" loop
                        break

                    # if line contain <LINK relation="Target"> that means target for given action
                    if ("<LINK relation=" in self.activity_file[j]) and ("Target" in self.activity_file[j]):
                        # if action is target of given action
                        if ("<ID name=" in self.activity_file[j + 2]) and \
                                ("Standard.OpaqueAction" in self.activity_file[j + 2]):
                            # record error
                            mcg_cc_error_handler.record_error(80, action, "none")

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
                                mcg_cc_error_handler.record_error(21, target_signal_uid, action)
                            # append node to node list
                            self.node_list.append(str(action) + " target " + str(target_signal_name))

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

        # component reading
        print("***************************** COMPONENT READING ****************************")
        print()

        # print component details
        print("Component Source:    " + str(self.activity_source))
        print("Component Name:      " + str(self.model_element_name))

        # record node list
        print("*** RECORD NODES ***")

        # search for signals target within activity file
        self.read_data_targets()

        # search for action targets within activity file
        self.read_interaction_targets()

        # node list recorded
        print("*** NODES RECORDED ***")
        print()

        # search for interface signals
        self.read_interface_signals()

        # check component correctness
        self.check_correctness()

        # display additional details after component reading for test run
        if MCG_CC_TEST_RUN:

            # print component details
            print("Nodes:")
            for node in self.node_list:
                print("          " + str(node))
            print("Actions:")
            for interaction in self.interaction_list:
                print("          " + str(interaction))
            print("Signals:")
            for data in self.data_list:
                print("          " + str(data))
            print("Input Interface:")
            for input_interface in self.input_interface_list:
                print("          " + str(input_interface))
            print("Output Interface:")
            for output_interface in self.output_interface_list:
                print("          " + str(output_interface))
            print("Local Data:")
            for local_data in self.local_data_list:
                print("          " + str(local_data))
            print()

        # end of component reading
        print("************************* END OF COMPONENT READING *************************")
        print()

        # append collected data to component reader list
        component_reader_list = []
        component_reader_list.insert(ComponentReader.MODEL_ELEMENT_NAME_INDEX, self.model_element_name)
        component_reader_list.insert(ComponentReader.ACTIVITY_SOURCE_INDEX, self.activity_source)
        component_reader_list.insert(ComponentReader.NODE_LIST_INDEX, self.node_list)
        component_reader_list.insert(ComponentReader.INTERACTION_LIST_INDEX, self.interaction_list)
        component_reader_list.insert(ComponentReader.INPUT_INTERFACE_LIST_INDEX, self.input_interface_list)
        component_reader_list.insert(ComponentReader.OUTPUT_INTERFACE_LIST_INDEX, self.output_interface_list)
        component_reader_list.insert(ComponentReader.LOCAL_DATA_LIST_INDEX, self.local_data_list)

        # return component reader list
        return component_reader_list
