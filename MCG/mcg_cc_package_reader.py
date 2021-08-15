#   FILE:           mcg_cc_package_reader.py
#
#   DESCRIPTION:
#       This module is responsible for reading of package content, i.e.
#       activity diagram and interface details from .exml files.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           15 AUG 2021
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
            # get copy of line
            line = file_content[i]
            # get interface type
            interface_type = mcg_cc_supporter.get_name(line)
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

                # if line contains </DEPENDENCIES> and interface does not have any target
                if ("</DEPENDENCIES>" in file_content[j]) and (not interface_has_targets):
                    # append node to list of nodes
                    node_list.append(str(interface_type) + " target empty")
                    # exit "for j in range" loop
                    break

                # if line contain <LINK relation="Target"> that means target for given interface
                if ("<LINK relation=" in file_content[j]) and ("Target" in file_content[j]):
                    # if component is target of given action
                    if ("<ID name=" in file_content[j + 2]) and ("Standard.InstanceNode" in file_content[j + 2]):
                        # get line
                        line = file_content[j + 2]
                        # get component uid
                        component_uid = mcg_cc_supporter.get_uid(line)
                        # find target component
                        target_component = mcg_cc_supporter.find_target_component(component_uid, file_content)
                        # append node to list of nodes
                        node_list.append(str(interface_type) + " target " + str(target_component))

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
def read_component_targets():
    tmpvar = ""
    # TBC


# Function:
# read_interfaces()
#
# Description:
# This function looks for interfaces of package, i.e. input interface list and
# output interface list.
#
# Returns:
# This function returns list of input interfaces and output interfaces.
def read_interfaces():
    tmpvar = ""
    # TBC


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
    package_source = ""
    package_name = ""

    # activity diagram path
    activity_diagram_path = path

    # open file and read content, then close file
    file = open(activity_diagram_path, "r")
    file_content = file.readlines()
    file_content = [x.strip() for x in file_content]
    file.close()

    # search for model element name and type in file content, i.e. find out if file content contains component data
    model_element_name, model_element_type = mcg_cc_supporter.find_model_element(file_content)

    # if file content contains package data
    if "Standard.Package" in model_element_type:

        # find package source, i.e. name of exml file
        package_source = activity_diagram_path[
                           len(activity_diagram_path) - EXML_FILE_NAME_LENGTH:len(activity_diagram_path)]

        # package name is same as model element name
        package_name = model_element_name

        # package reading
        print("****************************** PACKAGE READING *****************************")
        print()

        # print component details
        print("Package Source:      " + str(package_source))
        print("Package Name:        " + str(package_name))

        # record list of nodes
        print("*** RECORD NODES ***")

        # search for interface targets within diagram content
        node_list, interface_list = read_interface_targets(file_content, node_list, interface_list)

        # search for component targets within diagram content
        # node_list, component_list = read_component_targets(file_content, node_list, component_list)

        # list of nodes recorded
        print("*** NODES RECORDED ***")
        print()

        # open and read interface file
        # input_interface_list, output_interface_list = read_interfaces(path, package_name)

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

    # return collected data
    return node_list, interface_list, component_list, input_interface_list, output_interface_list, \
        package_source, package_name
