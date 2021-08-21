#   FILE:           mcg_cc_component_reader.py
#
#   DESCRIPTION:
#       This module is responsible for reading of component content, i.e.
#       activity diagram and interface details from .exml files.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           21 AUG 2021
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

actions_with_first_input_signals = "SUB - "


# Function:
# check_signals_correctness()
#
# Description:
# This function checks correctness of signals from signal list.
#
# Returns:
# This function does not return anything.
def check_signals_correctness(signal_list, node_list):
    # check is some signal has more tha one source
    for s in signal_list:
        keyword = "target " + str(s)
        keyword_occurrence = 0

        # go through all nodes for each signal on signal_list
        for n in node_list:

            # if keyword within the node
            if keyword in n:
                # increment keyword counter
                keyword_occurrence = keyword_occurrence + 1

        # if keyword has more than one occurrence
        if keyword_occurrence > 1:
            # record error
            mcg_cc_error_handler.record_error(1, s, "none")


# Function:
# check_actions_correctness()
#
# Description:
# This function checks correctness of actions from action list.
#
# Returns:
# This function does not return anything.
def check_actions_correctness(action_list, node_list):
    # check if some actions are not recognized
    for a in action_list:
        if ("ADD" not in a) and ("SUB" not in a):
            # record error
            mcg_cc_error_handler.record_error(51, a, "none")


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
                        # get action name
                        action_name = mcg_cc_supporter.get_name(line, line_number)
                        # get action uid
                        action_uid = mcg_cc_supporter.get_uid(line, line_number)
                        # get target action
                        target_action = str(action_name) + " " + str(action_uid)

                        # first input signal is not needed
                        first_input_signal_needed = False

                        # if it is SUB action then find first input signal in SUB arithmetic operation
                        if action_name in actions_with_first_input_signals:

                            # find first input signal in file content
                            first_input_signal = mcg_cc_supporter.find_first_input_signal(target_action,
                                                                                          action_uid, file_content)

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
                        # get signal uid
                        signal_uid = mcg_cc_supporter.get_uid(line, line_number)
                        # find target signal
                        target_signal_list = mcg_cc_supporter.find_target_element(signal_uid, "Standard.Attribute",
                                                                                  file_content)
                        # if target signal was not found
                        if "NOT_FOUND" in target_signal_list[0]:
                            # record error
                            mcg_cc_error_handler.record_error(20, signal_uid, signal_name)
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
            # get action name
            action_name = mcg_cc_supporter.get_name(line, line_number)
            # get action uid
            action_uid = mcg_cc_supporter.get_uid(line, line_number)
            # get action
            action = str(action_name) + " " + str(action_uid)
            # append action to list of signals
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
                        # get signal uid
                        signal_uid = mcg_cc_supporter.get_uid(line, line_number)
                        # find target signal
                        target_signal_list = mcg_cc_supporter.find_target_element(signal_uid, "Standard.Attribute",
                                                                                  file_content)
                        # if target signal was not found
                        if "NOT_FOUND" in target_signal_list[0]:
                            # record error
                            mcg_cc_error_handler.record_error(21, signal_uid, action)
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
def read_interfaces(path, component_name):
    # empty placeholders
    input_interface_list = []
    output_interface_list = []
    local_parameter_list = []
    signal = []

    # interface markers show whether interface was found of not
    input_interface_found = False
    output_interface_found = False
    local_parameters_found = False

    # find position of standard activity within the path
    standard_activity_position = path.find("\\Standard.Activity")
    # get interface directory path
    interface_dir_path = path[0:standard_activity_position] + str("\\Standard.Interface")

    # get list of interfaces
    interface_list = listdir(interface_dir_path)

    # create list of paths to interfaces
    interface_path_list = []
    for il in interface_list:
        interface_path_list.append(interface_dir_path + str("\\") + str(il))

    # read interface details
    for ipl in interface_path_list:

        # open file and read content, then close file
        file = open(ipl, "r")
        file_content = file.readlines()
        file_content = [x.strip() for x in file_content]
        file.close()

        # search for interface details in file content
        for i in range(0, len(file_content)):

            # if given line contains definition of input interface
            if ("Input Interface" in file_content[i]) and ("Standard.Interface" in file_content[i]) and (
                    component_name in file_content[i + 1]) and ("Standard.Component" in file_content[i + 1]):

                # input interface is found
                input_interface_found = True

                # print details of input interface file
                interface_source = ipl[len(ipl) - EXML_FILE_NAME_LENGTH:len(ipl)]
                print("Interface Source:    " + str(interface_source))
                print("Interface Type:      Input Interface")

                # record list of input interface signals
                print("*** RECORD INPUT INTERFACE ***")

                # search for input interface signals
                for line in file_content:
                    # if given line contains definition of signal name
                    if ("<ID name=" in line) and ("Standard.Attribute" in line):
                        # get signal name
                        signal_name = mcg_cc_supporter.get_name(line, "unknown")
                        # append signal name to signal
                        signal.append(signal_name)
                    # if given line contain definition of signal type
                    if ("<ID name=" in line) and ("Standard.DataType" in line):
                        # get signal type
                        signal_type = mcg_cc_supporter.get_name(line, "unknown")
                        # append signal type to signal
                        signal.append(signal_type)
                        # append signal to input interface list
                        input_interface_list.append(signal)
                        # clear signal placeholder
                        signal = []

                # list of input interface signals recorded
                print("*** INPUT INTERFACE RECORDED ***")
                print()

                # exit "for i in range" loop
                break

            # else if given line contains definition of output interface
            elif ("Output Interface" in file_content[i]) and ("Standard.Interface" in file_content[i]) and (
                    component_name in file_content[i + 1]) and ("Standard.Component" in file_content[i + 1]):

                # output interface is found
                output_interface_found = True

                # print details of output interface file
                interface_source = ipl[len(ipl) - EXML_FILE_NAME_LENGTH:len(ipl)]
                print("Interface Source:    " + str(interface_source))
                print("Interface Type:      Output Interface")

                # record list of output interface signals
                print("*** RECORD OUTPUT INTERFACE ***")

                # search for output interface signals
                for line in file_content:
                    # if given line contains definition of signal name
                    if ("<ID name=" in line) and ("Standard.Attribute" in line):
                        # get signal name
                        signal_name = mcg_cc_supporter.get_name(line, "unknown")
                        # append signal name to signal
                        signal.append(signal_name)
                    # if given line contain definition of signal type
                    if ("<ID name=" in line) and ("Standard.DataType" in line):
                        # get signal type
                        signal_type = mcg_cc_supporter.get_name(line, "unknown")
                        # append signal type to signal
                        signal.append(signal_type)
                        # append signal to output interface list
                        output_interface_list.append(signal)
                        # clear signal placeholder
                        signal = []

                # list of output interface signals recorded
                print("*** OUTPUT INTERFACE RECORDED ***")
                print()

                # exit "for i in range" loop
                break

            # else if given line contains definition of local parameters
            elif ("Local Parameters" in file_content[i]) and ("Standard.Interface" in file_content[i]) and (
                    component_name in file_content[i + 1]) and ("Standard.Component" in file_content[i + 1]):

                # local parameters are found
                local_parameters_found = True

                # print details of local parameters file
                interface_source = ipl[len(ipl) - EXML_FILE_NAME_LENGTH:len(ipl)]
                print("Interface Source:    " + str(interface_source))
                print("Interface Type:      Local Parameters")

                # record list of local signals
                print("*** RECORD LOCAL PARAMETERS ***")

                # search for local signals
                for line in file_content:
                    # if given line contains definition of signal name
                    if ("<ID name=" in line) and ("Standard.Attribute" in line):
                        # get signal name
                        signal_name = mcg_cc_supporter.get_name(line, "unknown")
                        # append signal name to signal
                        signal.append(signal_name)
                    # if given line contain definition of signal type
                    if ("<ID name=" in line) and ("Standard.DataType" in line):
                        # get signal type
                        signal_type = mcg_cc_supporter.get_name(line, "unknown")
                        # append signal type to signal
                        signal.append(signal_type)
                        # append signal to local parameters list
                        local_parameter_list.append(signal)
                        # clear signal placeholder
                        signal = []

                # list of local signals recorded
                print("*** LOCAL PARAMETERS RECORDED ***")
                print()

                # exit "for i in range" loop
                break

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
# This function returns list of nodes, actions, signals, input interfaces,
# output interfaces, local parameters, component source and component name.
def read_component(path):
    # empty lists
    node_list = []
    signal_list = []
    action_list = []
    input_interface_list = []
    output_interface_list = []
    local_parameter_list = []

    # activity diagram path
    activity_diagram_path = path

    # open file and read content, then close file
    file = open(activity_diagram_path, "r")
    file_content = file.readlines()
    file_content = [x.strip() for x in file_content]
    file.close()

    # find model element source, i.e. name of exml file
    model_element_source = activity_diagram_path[
                           len(activity_diagram_path) - EXML_FILE_NAME_LENGTH:len(activity_diagram_path)]

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
        input_interface_list, output_interface_list, local_parameter_list = read_interfaces(path, model_element_name)

        # check signals correctness
        check_signals_correctness(signal_list, node_list)

        # check actions correctness
        check_actions_correctness(action_list, node_list)

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
            for n in node_list:
                print("          " + str(n))
            print("Actions:")
            for a in action_list:
                print("          " + str(a))
            print("Signals:")
            for s in signal_list:
                print("          " + str(s))
            print("Input Interface:")
            for ii in input_interface_list:
                print("          " + str(ii))
            print("Output Interface:")
            for oi in output_interface_list:
                print("          " + str(oi))
            print("Local Parameters:")
            for lp in local_parameter_list:
                print("          " + str(lp))
            print()

        # end of component reading
        print("************************* END OF COMPONENT READING *************************")
        print()

    # return collected data
    return node_list, action_list, signal_list, input_interface_list, output_interface_list, local_parameter_list, \
        model_element_source, model_element_name
