#   FILE:           mcg_cc_supporter.py
#
#   DESCRIPTION:
#       This module provides additional, supporting functions, which are used
#       by Mod Code Generator (MCG) Converter Component (CC) to read details of
#       .exml file or merged nodes.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           13 AUG 2021
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
def get_name(line):

    # find position of name within the line
    name_position = line.find("name")
    # find position of mc within the line
    mc_position = line.find("mc")

    # check if <name> and <mc> position is found
    if (name_position == -1) or (mc_position == -1):
        # record error
        mcg_cc_error_handler.record_error(102, "none")
        # set error name
        name = "ERROR_NAME"
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
def get_uid(line):

    # find position of uid within the line
    uid_position = line.find("uid")

    # check if <uid> position is found
    if uid_position == -1:
        # record error
        mcg_cc_error_handler.record_error(103, "none")
        # set error uid
        uid = "ERROR_UID"
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
    # empty model element name and type placeholders
    model_element_name = ""
    model_element_type = ""

    # search for model element name and type in file content
    for i in range(0, len(file_content)):

        # if given line contains definition of activity diagram
        if ("Standard.Activity" in file_content[i]) and ("Standard.Component" in file_content[i+1]):
            # get line
            line = file_content[i+1]
            # get model element name
            model_element_name = get_name(line)
            # set model element type
            model_element_type = "Standard.Component"
            # exit "for i in range" loop
            break
        elif ("Standard.Activity" in file_content[i]) and ("Standard.Package" in file_content[i+1]):
            # get line
            line = file_content[i+1]
            # get model element name
            model_element_name = get_name(line)
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
        mcg_cc_error_handler.record_error(101, "none")
        # set error model element name and type
        model_element_name = "ERROR_MODEL_ELEMENT_NAME"
        model_element_type = "ERROR_MODEL_ELEMENT_TYPE"

    # return element type and name
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
def find_first_input_signal(action_uid, file_content):
    # empty placeholder
    first_input_signal = ""

    # search for above actions in file content
    for k in range(0, len(file_content)):

        # if given line contains definition of action
        if ("<OBJECT>" in file_content[k]) and ("<ID name=" in file_content[k + 1]) and (
                "Standard.OpaqueAction" in file_content[k + 1]) and (
                action_uid in file_content[k + 1]):

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
        mcg_cc_error_handler.record_error(31, action_uid)
        # set error signal
        first_input_signal = "ERROR_SIGNAL"

    # return first input signal
    return first_input_signal


# Function:
# find_target_signal()
#
# Description:
# This function looks for target signal of given action or another signal, basing on signal uid, within
# line of .exml file, an example of .exml file line:
# <ID name="" mc="Standard.InstanceNode" uid="91282ffc-e076-41c7-99e6-9aed64f5a02d"/>
#
# Returns:
# This function returns target signal name of given action or another signal.
def find_target_signal(signal_uid, file_content):
    # empty placeholder
    target_signal = ""

    # search for uid in file content
    for i in range(0, len(file_content)):

        # if uid within the line
        if ("<OBJECT>" in file_content[i]) and ("<ID name=" in file_content[i + 1]) and\
                (signal_uid in file_content[i + 1]):

            # search for signal definition
            for j in range(i + 1, len(file_content)):

                # if given line contains definition of signal name
                if ("<ID name=" in file_content[j]) and ("Standard.Attribute" in file_content[j]):
                    # get copy of line
                    line = file_content[j]
                    # get target signal
                    target_signal = get_name(line)
                    # exit "for j in range" loop
                    break

            # exit "for i in range" loop
            break

    # if signal is not found
    if target_signal == "":
        # record error
        mcg_cc_error_handler.record_error(30, signal_uid)
        # set error signal
        target_signal = "ERROR_SIGNAL"

    # return signal
    return target_signal


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
