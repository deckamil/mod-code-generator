#   FILE:           mcg_cc_supporter.py
#
#   DESCRIPTION:
#       This module provides additional, supporting functions, which are used
#       by Mod Code Generator (MCG) Converter Component (CC) to read details of
#       .exml file or merged nodes.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           19 SEP 2021
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


import mcg_cc_error_handler
from mcg_cc_parameters import TARGET_OFFSET
from mcg_cc_parameters import NAME_START_OFFSET
from mcg_cc_parameters import NAME_END_OFFSET
from mcg_cc_parameters import UID_START_OFFSET
from mcg_cc_parameters import UID_END_OFFSET
from mcg_cc_parameters import FIRST_INPUT_SIGNAL_OFFSET
from mcg_cc_parameters import MCG_CC_TEST_RUN
from mcg_cc_parameters import action_type_list
from mcg_cc_parameters import action_type_req_first_input_signal_list


# Function:
# get_name()
#
# Description:
# This function looks for <name> element within line of .exml file, which defines action type,
# signal name, signal type, interface type, model element name (name of model component or
# package), depending on the context where <name> element occurs within the .exml file, an
# example of .exml file line:
# <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
#
# Returns:
# This function returns <name> element.
def get_name(line, line_number):

    # find position of name within the line
    name_position = line.find("name")
    # find position of mc within the line
    mc_position = line.find("mc")

    # check if <name> and <mc> position is found
    if (name_position == -1) or (mc_position == -1):
        # record error
        mcg_cc_error_handler.record_error(271, line_number, "none")
        # set error name
        name = "NAME_NOT_FOUND"
    else:
        # get name
        name = line[name_position + NAME_START_OFFSET:mc_position + NAME_END_OFFSET]

    # return name
    return name


# Function:
# get_uid()
#
# Description:
# This function looks for <uid> element within line of .exml file, which defines action uid
# or signal uid, an example of .exml file line:
# <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
#
# Returns:
# This function returns <uid>.
def get_uid(line, line_number):

    # find position of uid within the line
    uid_position = line.find("uid")

    # check if <uid> position is found
    if uid_position == -1:
        # record error
        mcg_cc_error_handler.record_error(272, line_number, "none")
        # set error uid
        uid = "UID_NOT_FOUND"
    else:
        # get uid
        uid = line[uid_position + UID_START_OFFSET:len(line) + UID_END_OFFSET]

    # return uid
    return uid


# Function:
# find_model_element()
#
# Description:
# This function looks model element name and model element type (i.e. information whether file content
# contains data of model component or model package) within content of .exml file, an example of .exml file line:
# <PID name="DataSeparator" mc="Standard.Component" uid="a291290d-4d60-4daa-b606-1eda25d2ecda"/>
#
# Returns:
# This function returns model element name and model element type.
def find_model_element(file_content):
    # local data
    model_element_name = ""
    model_element_type = ""

    # search for model element name and type in file content
    for i in range(0, len(file_content)):

        # if given line contains definition of activity diagram
        if ("Standard.Activity" in file_content[i]) and ("Standard.Component" in file_content[i+1]):
            # get line
            line = file_content[i+1]
            # get line number
            line_number = i + 2
            # get model element name
            model_element_name = get_name(line, line_number)
            # set model element type
            model_element_type = "Standard.Component"
            # exit "for i in range" loop
            break
        elif ("Standard.Activity" in file_content[i]) and ("Standard.Package" in file_content[i+1]):
            # get line
            line = file_content[i+1]
            # get line number
            line_number = i + 2
            # get model element name
            model_element_name = get_name(line, line_number)
            # set model element type
            model_element_type = "Standard.Package"
            # exit "for i in range" loop
            break
        else:
            # set empty model element name and type
            model_element_name = ""
            model_element_type = ""

    # if model element name or type is not found
    if (model_element_name == "") or (model_element_type == ""):
        # record error
        mcg_cc_error_handler.record_error(270, "none", "none")
        # set model element name
        model_element_name = "MODEL_ELEMENT_NAME_NOT_FOUND"
        # set model element type
        model_element_type = "MODEL_ELEMENT_TYPE_NOT_FOUND"

    # return element name and type
    return model_element_name, model_element_type


# Function:
# find_first_input_signal()
#
# Description:
# This function looks for first input signal, recognized by *FIRST* marker, of given target action within
# content of .exml file. In case of some type of actions the order of input signals, which take part in action
# calculation can influence on action results. In such case it is important to distinguish first input
# signal of given action, therefore this function is responsible for finding of such signal in .exml file,
# an example of .exml file line:
# <ATT name="Content"><![CDATA[*FIRST* locAddRes *FIRST*]]></ATT>
#
# Returns:
# This function returns first input signal name of given action.
def find_first_input_signal(target_action, target_action_uid, file_content):
    # local data
    first_input_signal = ""

    # search for above actions in file content
    for i in range(0, len(file_content)):

        # if given line contains definition of action
        if ("<OBJECT>" in file_content[i]) and ("<ID name=" in file_content[i + 1]) and (
                "Standard.OpaqueAction" in file_content[i + 1]) and (
                target_action_uid in file_content[i + 1]):

            # search for first input signal to above action
            for j in range(i, len(file_content)):

                # if given line contains details about first input signal
                if ("<ATT name=" in file_content[j]) and ("*FIRST*" in file_content[j]):
                    # get line
                    line = file_content[j]
                    # find start marker of first input signal
                    first_input_start = line.find("*FIRST*")
                    # find end marker of first input signal
                    first_input_end = line.rfind("*FIRST*")
                    # check if *FIRST* marker is found
                    if (first_input_start == -1) or (first_input_end == -1) or (first_input_start == first_input_end):
                        # set empty first input signal
                        first_input_signal = ""
                    else:
                        # get first input signal
                        first_input_signal = line[first_input_start + FIRST_INPUT_SIGNAL_OFFSET:first_input_end - 1]

    # if signal is not found
    if first_input_signal == "":
        # record error
        mcg_cc_error_handler.record_error(22, target_action, "none")
        # set error signal
        first_input_signal = "FIRST_INPUT_SIGNAL_NOT_FOUND"

    # return first input signal
    return first_input_signal


# Function:
# find_target_element()
#
# Description:
# This function looks for name of target element, basing on target element type and its uid, within
# content of .exml file, an example of .exml file line:
# <ID name="input3" mc="Standard.Attribute" uid="338540aa-439c-4dc7-8414-a275ba3c08e1"/>
#
# Returns:
# This function returns list of target elements.
def find_target_element(target_element_uid, target_element_type, file_content):
    # local data
    target_element_name = ""
    target_element_list = []

    # search for uid in file content
    for i in range(0, len(file_content)):

        # if uid within the line
        if ("<OBJECT>" in file_content[i]) and ("<ID name=" in file_content[i + 1]) and\
                (target_element_uid in file_content[i + 1]):

            # search for target element definition
            for j in range(i + 1, len(file_content)):

                # if given line contains definition of target element
                if ("<ID name=" in file_content[j]) and (target_element_type in file_content[j]):
                    # get line
                    line = file_content[j]
                    # get line number
                    line_number = j + 1
                    # get target element name
                    target_element_name = get_name(line, line_number)
                    # append "found" marker to list of target elements
                    target_element_list.append("FOUND")
                    # append target element name to list of target elements
                    target_element_list.append(target_element_name)
                    # exit "for j in range" loop
                    break

                # if line contains </OBJECT> that means end of object definition
                if "</OBJECT>" in file_content[j]:
                    # exit "for j in range" loop
                    break

            # exit "for i in range" loop
            break

    # if target element name is not found
    if target_element_name == "":
        # set target element name
        target_element_name = "TARGET_ELEMENT_NOT_FOUND"
        # append "not found" marker to list of target elements
        target_element_list.append("NOT_FOUND")
        # append target element name to list of target elements
        target_element_list.append(target_element_name)

    # return list of target elements
    return target_element_list


# Function:
# find_interface_signals()
#
# Description:
# This function looks for name and type of interface signals for given component or package, within
# content of .exml file, an example of .exml file line:
# <ID name="loc_add_result" mc="Standard.Attribute" uid="47398f97-728c-4e18-aa19-d36a5c099ba7"/>
# <ID name="INT16" mc="Standard.DataType" uid="e7213c05-8c48-4585-8bc5-cc8690ffd6be"/>
#
# Returns:
# This function returns list of interface signals.
def find_interface_signals(interface_type, interface_source, model_element_name, model_element_type, file_content):
    # local data
    interface_found = False
    interface_signal = []
    interface_signal_list = []

    # search for interface details in file content
    for i in range(0, len(file_content)):

        # if given line contains definition of input interface
        if (interface_type in file_content[i]) and ("Standard.Interface" in file_content[i]) and (
                model_element_name in file_content[i + 1]) and (model_element_type in file_content[i + 1]):

            # if interface is found
            if not interface_found:
                # change interface found marker
                interface_found = True
                # append "found" marker to list of interface signals
                interface_signal_list.append("FOUND")

            # print details of interface file
            print("Interface Source:    " + str(interface_source))
            print("Interface Type:      " + str(interface_type))

            # record list of interface signals
            print("*** RECORD INTERFACE ***")

            # search for input interface signals
            for j in range(0, len(file_content)):
                # if given line contains definition of signal name
                if ("<ID name=" in file_content[j]) and ("Standard.Attribute" in file_content[j]):
                    # get line
                    line = file_content[j]
                    # get line number
                    line_number = j + 1
                    # get signal name
                    signal_name = get_name(line, line_number)
                    # append signal name to signal
                    interface_signal.append(signal_name)
                # if given line contain definition of signal type
                if ("<ID name=" in file_content[j]) and ("Standard.DataType" in file_content[j]):
                    # get line
                    line = file_content[j]
                    # get line number
                    line_number = j + 1
                    # get signal type
                    signal_type = get_name(line, line_number)
                    # append signal type to signal
                    interface_signal.append(signal_type)
                    # append interface signal to interface list
                    interface_signal_list.append(interface_signal)
                    # clear interface signal
                    interface_signal = []

            # list of interface signals recorded
            print("*** INTERFACE RECORDED ***")
            print()

            # exit "for i in range" loop
            break

    # if interface is not found
    if not interface_found:
        # append "not found" marker to list of interface signals
        interface_signal_list.append("NOT_FOUND")

    # return list of interface signals
    return interface_signal_list


# Function:
# find_output_signal()
#
# Description:
# This function looks for output signal name within merged node, i.e. output signal from given action,
# an example of merged node:
# eng_gain1 target eng_gain2 target ADD a084fca5-1c0a-4dfd-881b-21c3f83284e7 target eng_gain_total
#
# Returns:
# This function returns output signal name.
def find_output_signal(merged_node):
    # find position of output signal from merged node
    target_last_position = merged_node.rfind("target")
    # get output signal from appended node
    output_signal = merged_node[target_last_position + TARGET_OFFSET:len(merged_node)]

    # return output signal
    return output_signal


# Function:
# check_if_reference_contains_action_type()
#
# Description:
# This function checks if reference contains any action type.
#
# Returns:
# This function returns action found marker.
def check_if_reference_contains_action_type(reference):
    # action marker shows whether reference contains action type
    action_type_found = False

    # for all allowed type of actions
    for action_type in action_type_list:
        # if action type is found within reference
        if action_type in reference:
            # change action marker
            action_type_found = True
            # exit loop
            break

    # return action marker
    return action_type_found


# Function:
# check_if_reference_contains_action_type_req_first_input_signal()
#
# Description:
# This function checks if reference contains any action type requiring first input signal.
#
# Returns:
# This function returns action found marker.
def check_if_reference_contains_action_type_req_first_input_signal(reference):
    # action marker shows whether reference contains action type requiring first input signal
    action_type_req_first_input_signal_found = False

    # for all allowed type of actions requiring first input signal
    for action_type_req_first_input_signal in action_type_req_first_input_signal_list:
        # if action type requiring first input signal is found within reference
        if action_type_req_first_input_signal in reference:
            # change action marker
            action_type_req_first_input_signal_found = True
            # exit loop
            break

    # return action marker
    return action_type_req_first_input_signal_found


# Function:
# count_dependencies()
#
# Description:
# This function counts dependencies between merged nodes, i.e. number of local data elements outputted by merged nodes,
# which are required to compute another merged node. The number of dependencies is expressed by length of sublist
# created for each merged node under list of dependencies.
#
# Returns:
# This function returns list of dependencies.
def count_dependencies(merged_node_list, local_data_list):

    # count dependencies between nodes
    # each merged node (with exception for target empty node) has its own sublist under list of dependencies
    # the sublist starts with merged node under index 0 and local data elements required to compute the merged node
    # are appended under further indexes of the sublist;
    # as result, length of sublist express number of local data elements needed to compute the merged node;
    # in special case, if merged node does not need any local data element (i.e. only input interface elements are
    # required to compute the merged node) the length of sublist is equal to 1
    dependency_list = []
    for i in range(0, len(merged_node_list)):
        # dependency sublist
        dependency = []
        if "target empty" not in merged_node_list[i]:
            # copy merged node from given index
            merged_node = merged_node_list[i]
            # append merged node to dependency sublist
            dependency.append(merged_node)
            # find output element within merged node
            output_element = find_output_signal(merged_node)
            # go through all local data elements for each merged node on list of merged nodes
            for local_data in local_data_list:
                # get name of local data element
                local_data_name = local_data[0]
                # if local data element is input to merged node
                if (local_data_name in merged_node) and (local_data_name not in output_element):
                    # append name of local data element to dependency sublist
                    dependency.append(local_data_name)

        # if dependency sublist is not empty
        if len(dependency) > 0:
            # append dependency sublist to list of dependencies
            dependency_list.append(dependency)

    # display additional details after component sorting for test run
    if MCG_CC_TEST_RUN:

        print("Dependencies:")
        for dependency in dependency_list:
            print("          " + str(dependency))
        print()

    return dependency_list


# Function:
# sort_nodes()
#
# Description:
# This function sort nodes basing on their dependencies from sublist under list of dependencies.
#
# Returns:
# This function returns list of sorted nodes.
def sort_nodes(merged_node_list, dependency_list):

    # list of sorted nodes
    sorted_node_list = []

    # sort nodes basing on their dependencies
    # first append merged nodes without dependencies to list of sorted nodes, i.e. those merged nodes which sublist
    # length is equal to 1, which means that given merged node does not consume any local data elements (or consume
    # local data elements outputted by merged node, which was already appended to list of sorted nodes);
    # then remove local data element outputted by above merged node from each sublist under list of dependencies, which
    # will lead to situation where some of sublist will have new length equal to 1;
    # next repeat the cycle until all merged nodes are sorted

    # number of merged nodes to sort, i.e. length of list of dependencies
    dependency_list_length = len(dependency_list)
    # repeat until all merged nodes are sorted
    while dependency_list_length > 0:
        # go thorough each dependency sublist
        for i in range(0, len(dependency_list)):
            # if given merged node under dependency sublist does not have any further dependencies
            if len(dependency_list[i]) == 1:
                # get dependency sublist
                dependency = dependency_list[i]
                # append merged node to list of sorted nodes
                sorted_node_list.append(dependency[0])
                # remove dependency sublist from list of dependencies
                dependency_list.remove(dependency)
                # find output element within merged node
                output_element = find_output_signal(dependency[0])
                # recalculate number of merged nodes to sort, i.e. length of list of dependencies
                dependency_list_length = len(dependency_list)

                # refresh each dependency sublist
                for j in range(0, len(dependency_list)):
                    # if given merged node under dependency sublist does have further dependencies
                    if len(dependency_list[j]) > 1:
                        # get dependency sublist
                        dependency = dependency_list[j]
                        # set initial index
                        index = 1
                        # chek local data elements under dependency sublist
                        for k in range(index, len(dependency)):
                            # if given merged node consumes local data elements, which comes from merged node, which
                            # was appended above to list of sorted nodes
                            if output_element in dependency[index]:
                                # remove local data element from dependency sublist
                                dependency.remove(dependency[index])
                                # decrement index for next iteration, as one dependence was removed
                                # therefore all next dependencies in ref was pushed by one position
                                # towards beginning of ref, e.g. [...,A,B,C] -> [...,B,C];
                                # A was removed and now B is under previous position of A so at next
                                # iteration the same index need to be checked to examine B;
                                index = index - 1
                            index = index + 1

                # exit "for i in range" loop
                break

    # append merged nodes with empty target (last element from list of merged nodes)
    sorted_node_list.append(merged_node_list[len(merged_node_list)-1])

    # display additional details after component sorting for test run
    if MCG_CC_TEST_RUN:

        print("Sorted Nodes:")
        for sorted_node in sorted_node_list:
            print("          " + str(sorted_node))
        print()

    # return sorted list of nodes
    return sorted_node_list
