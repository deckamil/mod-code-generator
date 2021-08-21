#   FILE:           mcg_cc_supporter.py
#
#   DESCRIPTION:
#       This module provides additional, supporting functions, which are used
#       by Mod Code Generator (MCG) Converter Component (CC) to read details of
#       .exml file or merged nodes.
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


import mcg_cc_error_handler
from mcg_cc_parameters import TARGET_OFFSET
from mcg_cc_parameters import NAME_START_OFFSET
from mcg_cc_parameters import NAME_END_OFFSET
from mcg_cc_parameters import UID_START_OFFSET
from mcg_cc_parameters import UID_END_OFFSET
from mcg_cc_parameters import FIRST_INPUT_SIGNAL_OFFSET


# Function:
# get_name()
#
# Description:
# This function looks for <name> element within line of .exml file, which define name of action,
# signal, signal type, interface type or model element (name of model component or package), an
# example of .exml file line:
# <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
#
# Returns:
# This function returns name of action, signal, signal type or model element.
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
# This function looks for <uid> element within line of .exml file, which define uid of action
# or signal, an example of .exml file line:
# <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
#
# Returns:
# This function returns uid of action or signal.
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
# This function looks for <name> and <mc> elements within line of .exml file, which define
# model element name and model element type (i.e. information whether file content contains
# data of model component or model package), an example of .exml file line:
# <PID name="DataSeparator" mc="Standard.Component" uid="a291290d-4d60-4daa-b606-1eda25d2ecda"/>
#
# Returns:
# This function returns model element name and model element type.
def find_model_element(file_content):
    # empty placeholders
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
# This function looks for first input signal, recognized by *FIRST* marker, of given action uid within
# line of .exml file. In case of some type of actions the order of input signals, which take part in action
# calculation can influence on action results. In such case it is important to distinguish first input
# signal of given action, therefore this function is responsible for finding of such signal in .exml file,
# an example of .exml file line:
# <ATT name="Content"><![CDATA[*FIRST* locAddRes *FIRST*]]></ATT>
#
# Returns:
# This function returns first input signal name of given action.
def find_first_input_signal(target_action, target_action_uid, file_content):
    # empty placeholder
    first_input_signal = ""

    # search for above actions in file content
    for k in range(0, len(file_content)):

        # if given line contains definition of action
        if ("<OBJECT>" in file_content[k]) and ("<ID name=" in file_content[k + 1]) and (
                "Standard.OpaqueAction" in file_content[k + 1]) and (
                target_action_uid in file_content[k + 1]):

            # search for first input signal to above action
            for l in range(k, len(file_content)):

                # if given line contains details about first input signal
                if ("<ATT name=" in file_content[l]) and ("*FIRST*" in file_content[l]):
                    # get line
                    line = file_content[l]
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
# line of .exml file, an example of .exml file line:
# <ID name="input3" mc="Standard.Attribute" uid="338540aa-439c-4dc7-8414-a275ba3c08e1"/>
#
# Returns:
# This function returns list of target elements.
def find_target_element(target_element_uid, target_element_type, file_content):
    # empty placeholders
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
                    # append "found" info to list of target elements
                    target_element_list.append("FOUND")
                    # append target element name to list of target elements
                    target_element_list.append(target_element_name)
                    # exit "for j in range" loop
                    break

            # exit "for i in range" loop
            break

    # if target element name is not found
    if target_element_name == "":
        # set target element name
        target_element_name = "TARGET_ELEMENT_NOT_FOUND"
        # append "not found" info to list of target elements
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
# line of .exml file, an example of .exml file line:
# <ID name="loc_add_result" mc="Standard.Attribute" uid="47398f97-728c-4e18-aa19-d36a5c099ba7"/>
# <ID name="INT16" mc="Standard.DataType" uid="e7213c05-8c48-4585-8bc5-cc8690ffd6be"/>
#
# Returns:
# This function returns list of interface signals.
def find_interface_signals(interface_type, interface_source, model_element_name, model_element_type, file_content):
    # locals
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
                # append "found" info to list of interface signals
                interface_signal_list.append("FOUND")

            # print details of interface file
            print("Interface Source:    " + str(interface_source))
            print("Interface Type:      " + str(interface_type))

            # record list of interface signals
            print("*** RECORD INTERFACE ***")

            # search for input interface signals
            for line in file_content:
                # if given line contains definition of signal name
                if ("<ID name=" in line) and ("Standard.Attribute" in line):
                    # get signal name
                    signal_name = get_name(line, "unknown")
                    # append signal name to signal
                    interface_signal.append(signal_name)
                # if given line contain definition of signal type
                if ("<ID name=" in line) and ("Standard.DataType" in line):
                    # get signal type
                    signal_type = get_name(line, "unknown")
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
        # append "not found" info to list of interface signals
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
