#   FILE:           mcg_cc_component_reader.py
#
#   DESCRIPTION:
#       This module is responsible for reading of component content, i.e.
#       activity diagram and interface details from .exml files.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           27 AUG 2021
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


import random
from os import listdir
import mcg_cc_error_handler
import mcg_cc_supporter
from mcg_cc_parameters import MCG_CC_TEST_RUN
from mcg_cc_parameters import EXML_FILE_NAME_LENGTH
from mcg_cc_parameters import ACTION_UID_OFFSET

action_types_with_first_input_signal = "SUB - "
allowed_action_types = "ADD - SUB - "


# Function:
# check_component_correctness()
#
# Description:
# This function checks correctness of component data.
#
# Returns:
# This function does not return anything.
def check_component_correctness(signal_list, action_list, node_list):
    # check is some signal has more than one source
    for signal in signal_list:
        keyword = "target " + str(signal)
        keyword_occurrence = 0

        # go through all nodes for each signal on signal_list
        for node in node_list:

            # if keyword within the node
            if keyword in node:
                # increment keyword counter
                keyword_occurrence = keyword_occurrence + 1

        # if keyword has more than one occurrence
        if keyword_occurrence > 1:
            # record error
            mcg_cc_error_handler.record_error(1, signal, "none")

    # check if some actions are not recognized
    for action in action_list:
        # get action type
        action_type = action[0:len(action) + ACTION_UID_OFFSET]
        # if action type is not allowed
        if action_type not in allowed_action_types:
            # record error
            mcg_cc_error_handler.record_error(51, action, "none")


# Function:
# read_signal_targets()
#
# Description:
# This function looks for signals and their targets.
#
# Returns:
# This function returns list of nodes and signals.
def read_signal_targets(file_content, node_list, signal_list):
    # search for signals in file content
    for i in range(0, len(file_content)):

        # if given line contains definition of signal name
        if ("<ID name=" in file_content[i]) and ("Standard.Attribute" in file_content[i]):
            # get line
            line = file_content[i]
            # get line number
            line_number = i + 1
            # get signal name
            signal_name = mcg_cc_supporter.get_name(line, line_number)
            # append signal name to list of signals
            signal_list.append(signal_name)

            # signal does not have any target
            signal_has_targets = False

            # search for targets
            for j in range(i, len(file_content)):

                # if line contains <COMP that means the signal has some targets
                if "<COMP" in file_content[j]:
                    # signal has some target
                    signal_has_targets = True

                # if line contains </DEPENDENCIES> then signal does not have any target
                if ("</DEPENDENCIES>" in file_content[j]) and (not signal_has_targets):
                    # append node to list of nodes
                    node_list.append(str(signal_name) + " target empty")
                    # exit "for j in range" loop
                    break

                # if line contain <LINK relation="Target"> that means target for given signal
                if ("<LINK relation=" in file_content[j]) and ("Target" in file_content[j]):
                    # if action is target of given signal
                    if ("<ID name=" in file_content[j + 2]) and ("Standard.OpaqueAction" in file_content[j + 2]):
                        # get line
                        line = file_content[j + 2]
                        # get line number
                        line_number = j + 3
                        # get target action type
                        target_action_type = mcg_cc_supporter.get_name(line, line_number)
                        # get target action uid
                        target_action_uid = mcg_cc_supporter.get_uid(line, line_number)
                        # get target action
                        target_action = str(target_action_type) + " " + str(target_action_uid)

                        # first input signal is not needed
                        first_input_signal_needed = False

                        # if this type of action requires first input signal
                        if target_action_type in action_types_with_first_input_signal:

                            # find first input signal in file content
                            first_input_signal = mcg_cc_supporter.find_first_input_signal(target_action,
                                                                                          target_action_uid,
                                                                                          file_content)

                            # if first input signal is same as current node signal
                            if signal_name in first_input_signal:
                                # first input signal is needed
                                first_input_signal_needed = True

                        # append node to list of nodes
                        if first_input_signal_needed:
                            node_list.append("*FIRST* " + str(signal_name) + " *FIRST* target " + str(target_action))
                        else:
                            node_list.append(str(signal_name) + " target " + str(target_action))

                    # if signal is target of given signal
                    if ("<ID name=" in file_content[j + 2]) and ("Standard.InstanceNode" in file_content[j + 2]):
                        # get line
                        line = file_content[j + 2]
                        # get line number
                        line_number = j + 3
                        # get target signal uid
                        target_signal_uid = mcg_cc_supporter.get_uid(line, line_number)
                        # find target signal
                        target_signal_list = mcg_cc_supporter.find_target_element(target_signal_uid,
                                                                                  "Standard.Attribute",
                                                                                  file_content)
                        # if target signal was not found
                        if "NOT_FOUND" in target_signal_list[0]:
                            # record error
                            mcg_cc_error_handler.record_error(20, target_signal_uid, signal_name)
                        # append node to list of nodes
                        node_list.append(str(signal_name) + " target " + str(target_signal_list[1]))

                # if line contains </COMP> that means end of targets for given signal
                if "</COMP>" in file_content[j]:
                    # exit "for j in range" loop
                    break

    # remove duplicates from signal_list
    signal_list = list(set(signal_list))

    return node_list, signal_list


# Function:
# read_action_targets()
#
# Description:
# This function looks for actions and their targets.
#
# Returns:
# This function returns list of nodes and actions.
def read_action_targets(file_content, node_list, action_list):
    # search for actions in file content
    for i in range(0, len(file_content)):

        # if given line contains definition of action
        if ("<OBJECT>" in file_content[i]) and ("<ID name=" in file_content[i + 1]) and (
                "Standard.OpaqueAction" in file_content[i + 1]):
            # get line
            line = file_content[i + 1]
            # get line number
            line_number = i + 2
            # get action type
            action_type = mcg_cc_supporter.get_name(line, line_number)
            # get action uid
            action_uid = mcg_cc_supporter.get_uid(line, line_number)
            # get action
            action = str(action_type) + " " + str(action_uid)
            # append action to list of actions
            action_list.append(action)

            # action does not have any target
            action_has_targets = False

            # search for targets
            for j in range(i, len(file_content)):

                # if line contains <COMP that means the action has some targets
                if "<COMP" in file_content[j]:
                    # action has some target
                    action_has_targets = True

                # if line contains </DEPENDENCIES> then action does not have any target
                if ("</DEPENDENCIES>" in file_content[j]) and (not action_has_targets):
                    # record error
                    mcg_cc_error_handler.record_error(70, action, "none")
                    # exit "for j in range" loop
                    break

                # if line contain <LINK relation="Target"> that means target for given action
                if ("<LINK relation=" in file_content[j]) and ("Target" in file_content[j]):
                    # if action is target of given action
                    if ("<ID name=" in file_content[j + 2]) and ("Standard.OpaqueAction" in file_content[j + 2]):
                        # record error
                        mcg_cc_error_handler.record_error(80, action, "none")

                    # if signal is target of given action
                    if ("<ID name=" in file_content[j + 2]) and ("Standard.InstanceNode" in file_content[j + 2]):
                        # get line
                        line = file_content[j + 2]
                        # get line number
                        line_number = j + 3
                        # get target signal uid
                        target_signal_uid = mcg_cc_supporter.get_uid(line, line_number)
                        # find target signal
                        target_signal_list = mcg_cc_supporter.find_target_element(target_signal_uid,
                                                                                  "Standard.Attribute",
                                                                                  file_content)
                        # if target signal was not found
                        if "NOT_FOUND" in target_signal_list[0]:
                            # record error
                            mcg_cc_error_handler.record_error(21, target_signal_uid, action)
                        # append node to list of nodes
                        node_list.append(str(action) + " target " + str(target_signal_list[1]))

                # if line contains </COMP> that means end of targets for given signal
                if "</COMP>" in file_content[j]:
                    # exit "for j in range" loop
                    break

    return node_list, action_list


# Function:
# read_interfaces()
#
# Description:
# This function looks for interfaces of component, i.e. input interface list,
# output interface list and local parameters list.
#
# Returns:
# This function returns list of input interfaces, output interfaces and local
# parameters.
def read_interfaces(activity_file_path, model_element_name):
    # interface lists
    input_interface_list = []
    output_interface_list = []
    local_parameter_list = []

    # interface markers show whether interface was found of not
    input_interface_found = False
    output_interface_found = False
    local_parameters_found = False

    # find position of standard activity within the path
    standard_activity_position = activity_file_path.find("\\Standard.Activity")
    # get interface directory path
    interface_dir_path = activity_file_path[0:standard_activity_position] + str("\\Standard.Interface")
    # get list of interface sources, i.e. names of exml files
    interface_source_list = listdir(interface_dir_path)

    # read interface details
    for interface_source in interface_source_list:
        # get interface file path
        interface_file_path = interface_dir_path + str("\\") + str(interface_source)

        # open file and read content, then close file
        file = open(interface_file_path, "r")
        file_content = file.readlines()
        file_content = [line.strip() for line in file_content]
        file.close()

        # if input interface element has not been found yet
        if not input_interface_found:
            # find input interface
            input_interface_list = mcg_cc_supporter.find_interface_signals("Input Interface", interface_source,
                                                                           model_element_name, "Standard.Component",
                                                                           file_content)

            # if input interface element was found:
            if "NOT_FOUND" not in input_interface_list[0]:
                # change input interface marker
                input_interface_found = True
                # remove "found" info from list of input interface
                input_interface_list.remove(input_interface_list[0])

        # if output interface element has not been found yet
        if not output_interface_found:
            # find output interface
            output_interface_list = mcg_cc_supporter.find_interface_signals("Output Interface", interface_source,
                                                                            model_element_name, "Standard.Component",
                                                                            file_content)

            # if output interface element was found:
            if "NOT_FOUND" not in output_interface_list[0]:
                # change output interface marker
                output_interface_found = True
                # remove "found" info from list of output interface
                output_interface_list.remove(output_interface_list[0])

        # if local parameters element has not been found yet
        if not local_parameters_found:
            # find local parameters
            local_parameter_list = mcg_cc_supporter.find_interface_signals("Local Parameters", interface_source,
                                                                           model_element_name, "Standard.Component",
                                                                           file_content)

            # if local parameters element was found:
            if "NOT_FOUND" not in local_parameter_list[0]:
                # change local parameters marker
                local_parameters_found = True
                # remove "found" info from list of local parameters
                local_parameter_list.remove(local_parameter_list[0])

    # if input interface element was not found
    if not input_interface_found:
        # record error
        mcg_cc_error_handler.record_error(120, "none", "none")

    # if output interface element was not found
    if not output_interface_found:
        # record error
        mcg_cc_error_handler.record_error(121, "none", "none")

    # if local parameters element was not found
    if not local_parameters_found:
        # record error
        mcg_cc_error_handler.record_error(122, "none", "none")

    return input_interface_list, output_interface_list, local_parameter_list


# Function:
# read_component()
#
# Description:
# This is main function of this module and is responsible for reading of component
# details from .exml files.
#
# Returns:
# This function returns lists with component details.
def read_component(activity_file_path):
    # component lists
    node_list = []
    signal_list = []
    action_list = []
    input_interface_list = []
    output_interface_list = []
    local_parameter_list = []

    # open file and read content, then close file
    file = open(activity_file_path, "r")
    file_content = file.readlines()
    file_content = [line.strip() for line in file_content]
    file.close()

    # find model element source, i.e. name of exml file
    model_element_source = activity_file_path[len(activity_file_path) - EXML_FILE_NAME_LENGTH:len(activity_file_path)]

    # search for model element name and type in file content, i.e. find out if file content contains component data
    model_element_name, model_element_type = mcg_cc_supporter.find_model_element(file_content)

    # if file content contains component data
    if "Standard.Component" in model_element_type:

        # component reading
        print("***************************** COMPONENT READING ****************************")
        print()

        # print component details
        print("Component Source:    " + str(model_element_source))
        print("Component Name:      " + str(model_element_name))

        # record list of nodes
        print("*** RECORD NODES ***")

        # search for signals targets within diagram content
        node_list, signal_list = read_signal_targets(file_content, node_list, signal_list)

        # search for action targets within diagram content
        node_list, action_list = read_action_targets(file_content, node_list, action_list)

        # list of nodes recorded
        print("*** NODES RECORDED ***")
        print()

        # open and read interface file
        input_interface_list, output_interface_list, local_parameter_list = read_interfaces(activity_file_path,
                                                                                            model_element_name)

        # check component correctness
        check_component_correctness(signal_list, action_list, node_list)

        # display additional details after component reading for test run
        if MCG_CC_TEST_RUN:

            # shuffle lists
            random.shuffle(node_list)
            random.shuffle(action_list)
            random.shuffle(signal_list)
            random.shuffle(input_interface_list)
            random.shuffle(output_interface_list)
            random.shuffle(local_parameter_list)

            # print component details
            print("Nodes:")
            for node in node_list:
                print("          " + str(node))
            print("Actions:")
            for action in action_list:
                print("          " + str(action))
            print("Signals:")
            for signal in signal_list:
                print("          " + str(signal))
            print("Input Interface:")
            for input_interface in input_interface_list:
                print("          " + str(input_interface))
            print("Output Interface:")
            for output_interface in output_interface_list:
                print("          " + str(output_interface))
            print("Local Parameters:")
            for local_parameter in local_parameter_list:
                print("          " + str(local_parameter))
            print()

        # end of component reading
        print("************************* END OF COMPONENT READING *************************")
        print()

    # return collected data
    return node_list, action_list, signal_list, input_interface_list, output_interface_list, local_parameter_list, \
        model_element_source, model_element_name, model_element_type
