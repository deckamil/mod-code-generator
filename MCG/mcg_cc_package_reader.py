#   FILE:           mcg_cc_package_reader.py
#
#   DESCRIPTION:
#       This module is responsible for reading of package content, i.e.
#       activity diagram and interface details from .exml files.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           20 AUG 2021
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


# Function:
# read_interface_targets()
#
# Description:
# This function looks for interfaces and their targets.
#
# Returns:
# This function returns list of nodes and interfaces.
def read_interface_targets(file_content, node_list, interface_list):
    # search for interfaces in file content
    for i in range(0, len(file_content)):

        # if given line contains definition of interface type
        if ("<ID name=" in file_content[i]) and ("Standard.Interface" in file_content[i]):
            # get line
            line = file_content[i]
            # get line number
            line_number = i + 1
            # get interface type
            interface_type = mcg_cc_supporter.get_name(line, line_number)
            # append interface type to list of interfaces
            interface_list.append(interface_type)

            # interface does not have any target
            interface_has_targets = False

            # search for targets
            for j in range(i, len(file_content)):

                # if line contains <COMP that means the interface has some targets
                if "<COMP" in file_content[j]:
                    # interface has some target
                    interface_has_targets = True

                # if line contains </DEPENDENCIES> then interface does not have any target
                if ("</DEPENDENCIES>" in file_content[j]) and (not interface_has_targets):
                    # append node to list of nodes
                    node_list.append(str(interface_type) + " target empty")
                    # exit "for j in range" loop
                    break

                # if line contain <LINK relation="Target"> that means target for given interface
                if ("<LINK relation=" in file_content[j]) and ("Target" in file_content[j]):
                    # if component is target of given interface
                    if ("<ID name=" in file_content[j + 2]) and ("Standard.InstanceNode" in file_content[j + 2]):
                        # get line
                        line = file_content[j + 2]
                        # get line number
                        line_number = j + 3
                        # get component uid
                        component_uid = mcg_cc_supporter.get_uid(line, line_number)
                        # find target component
                        target_component_list = mcg_cc_supporter.find_target_element(component_uid,
                                                                                     "Standard.Component",
                                                                                     file_content)
                        # if target component was not found
                        if "NOT_FOUND" in target_component_list[0]:
                            # record error
                            mcg_cc_error_handler.record_error(172, component_uid, interface_type)
                        # append node to list of nodes
                        node_list.append(str(interface_type) + " target " + str(target_component_list[1]))

                # if line contains </COMP> that means end of targets for given interface
                if "</COMP>" in file_content[j]:
                    # exit "for j in range" loop
                    break

    return node_list, interface_list


# Function:
# read_component_targets()
#
# Description:
# This function looks for components and their targets.
#
# Returns:
# This function returns list of nodes and components.
def read_component_targets(file_content, node_list, component_list):
    # search for components in file content
    for i in range(0, len(file_content)):

        # if given line contains definition of component name
        if ("<ID name=" in file_content[i]) and ("Standard.Component" in file_content[i]):
            # get line
            line = file_content[i]
            # get line number
            line_number = i + 1
            # get interface type
            component_name = mcg_cc_supporter.get_name(line, line_number)
            # append component name to list of components
            component_list.append(component_name)

            # component does not have any target
            component_has_targets = False

            # search for targets
            for j in range(i, len(file_content)):

                # if line contains <COMP that means the interface has some targets
                if "<COMP" in file_content[j]:
                    # interface has some target
                    interface_has_targets = True

                # if line contains </DEPENDENCIES> then component does not have any target
                if ("</DEPENDENCIES>" in file_content[j]) and (not component_has_targets):
                    # record error
                    mcg_cc_error_handler.record_error(170, component_name, "none")
                    # exit "for j in range" loop
                    break

                # if line contain <LINK relation="Target"> that means target for given interface
                if ("<LINK relation=" in file_content[j]) and ("Target" in file_content[j]):
                    # if line contains uid of target element
                    if ("<ID name=" in file_content[j + 2]) and ("Standard.InstanceNode" in file_content[j + 2]):
                        # get line
                        line = file_content[j + 2]
                        # get line number
                        line_number = j + 3
                        # get target uid
                        target_uid = mcg_cc_supporter.get_uid(line, line_number)
                        # find target component
                        target_component_list = mcg_cc_supporter.find_target_element(target_uid,
                                                                                     "Standard.Component",
                                                                                     file_content)
                        # find target interface
                        target_interface_list = mcg_cc_supporter.find_target_element(target_uid,
                                                                                     "Standard.Interface",
                                                                                     file_content)
                        # if target element was not found
                        if ("NOT_FOUND" in target_component_list[0]) and ("NOT_FOUND" in target_interface_list[0]):
                            # record error
                            mcg_cc_error_handler.record_error(171, target_uid, component_name)
                        # select target element for node
                        if "NOT_FOUND" in target_component_list[0]:
                            target_element = target_interface_list[1]
                        else:
                            target_element = target_component_list[1]
                        # append node to list of nodes
                        node_list.append(str(component_name) + " target " + str(target_element))

                # if line contains </COMP> that means end of targets for given interface
                if "</COMP>" in file_content[j]:
                    # exit "for j in range" loop
                    break

    return node_list, component_list


# Function:
# read_interfaces()
#
# Description:
# This function looks for interfaces of package, i.e. input interface list and
# output interface list.
#
# Returns:
# This function returns list of input interfaces and output interfaces.
def read_interfaces(path, package_name):
    # empty placeholders
    input_interface_list = []
    output_interface_list = []
    signal = []

    # interface markers show whether interface was found of not
    input_interface_found = False
    output_interface_found = False

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
                    package_name in file_content[i + 1]) and ("Standard.Package" in file_content[i + 1]):

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
                    package_name in file_content[i + 1]) and ("Standard.Package" in file_content[i + 1]):

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

    # if input interface element was not found
    if not input_interface_found:
        # record error
        mcg_cc_error_handler.record_error(123, "none", "none")

    # if output interface element was not found
    if not output_interface_found:
        # record error
        mcg_cc_error_handler.record_error(124, "none", "none")

    return input_interface_list, output_interface_list


# Function:
# read_package()
#
# Description:
# This is main function of this module and is responsible for reading of package
# details from .exml files.
#
# Returns:
# This function returns list of nodes, interfaces, components, input interfaces,
# output interfaces, package source and package name.
def read_package(path):
    # empty placeholders
    node_list = []
    interface_list = []
    component_list = []
    input_interface_list = []
    output_interface_list = []

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

    # search for model element name and type in file content, i.e. find out if file content contains package data
    model_element_list = mcg_cc_supporter.find_model_element(file_content)

    # extract data from model element list
    model_element_found = model_element_list[0]
    model_element_name = model_element_list[1]
    model_element_type = model_element_list[2]

    # if file content contains package data
    if ("NOT_FOUND" not in model_element_found) and ("Standard.Package" in model_element_type):

        # package reading
        print("****************************** PACKAGE READING *****************************")
        print()

        # print component details
        print("Package Source:      " + str(model_element_source))
        print("Package Name:        " + str(model_element_name))

        # record list of nodes
        print("*** RECORD NODES ***")

        # search for interface targets within diagram content
        node_list, interface_list = read_interface_targets(file_content, node_list, interface_list)

        # search for component targets within diagram content
        node_list, component_list = read_component_targets(file_content, node_list, component_list)

        # list of nodes recorded
        print("*** NODES RECORDED ***")
        print()

        # open and read interface file
        input_interface_list, output_interface_list = read_interfaces(path, model_element_name)

        # display additional details after component reading for test run
        if MCG_CC_TEST_RUN:

            # shuffle lists
            random.shuffle(node_list)
            random.shuffle(interface_list)
            random.shuffle(component_list)
            random.shuffle(input_interface_list)
            random.shuffle(output_interface_list)

            # print component details
            print("Nodes:")
            for n in node_list:
                print("          " + str(n))
            print("Interfaces:")
            for i in interface_list:
                print("          " + str(i))
            print("Components:")
            for c in component_list:
                print("          " + str(c))
            print("Input Interface:")
            for ii in input_interface_list:
                print("          " + str(ii))
            print("Output Interface:")
            for oi in output_interface_list:
                print("          " + str(oi))
            print()

        # end of component reading
        print("************************** END OF PACKAGE READING **************************")
        print()

    # else if neither component nor package data was found in file content
    elif "NOT_FOUND" in model_element_found:
        # record error
        mcg_cc_error_handler.record_error(270, "none", "none", model_element_source)

    # return collected data
    return node_list, interface_list, component_list, input_interface_list, output_interface_list, \
        model_element_source, model_element_name
