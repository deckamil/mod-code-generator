#   FILE:           mcg_cc_converter.py
#
#   DESCRIPTION:
#       This is main module of Mod Code Generator (MCG) Converter Component (CC)
#       and is responsible for conversion of component and package content from
#       .exml file into configuration file, which will be used by Mod Code Generator
#       (MCG) Code Generator Component (CGC) to generate C code for the model.
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


from os import listdir
from sys import argv
import mcg_cc_error_handler
import mcg_cc_component_reader
import mcg_cc_component_sorter
import mcg_cc_package_reader
import mcg_cc_package_sorter
import mcg_cc_supporter
from mcg_cc_parameters import MCG_CC_TEST_RUN
from mcg_cc_parameters import TARGET_OFFSET
from mcg_cc_parameters import ACTION_UID_OFFSET
from mcg_cc_parameters import NUMBER_OF_MCG_CC_CMD_LINE_ARGS


# Function:
# convert_add()
#
# Description:
# This function is responsible for conversion of sorted node with ADD action into converted node in format
# required by configuration file.
#
# Returns:
# This function returns configuration file.
def convert_add(configuration_file, sorted_node):

    # find position of output signal within sorted node
    target_last_position = sorted_node.rfind("target")
    # get action uid
    action_uid = sorted_node[target_last_position + ACTION_UID_OFFSET:target_last_position - 1]
    # append action uid to configuration file
    configuration_file.append(str("COM Action ADD ") + str(action_uid))
    # find output signal within sorted node
    output_signal = mcg_cc_supporter.find_output_signal(sorted_node)
    # append output signal to conversion line
    conversion_line = str("INS ") + str(output_signal) + str(" = ")

    # count number of keyword "target"
    # number of "target" occurrences is required to calculate how many input signals are
    # consumed by node with ADD action, i.e. basing on the format and content of sorted node
    # with ADD action, the number of input signals is equal to (target_number - 1)
    target_number = sorted_node.count("target")

    # search input signals within sorted node starting from this position
    start_index = 0

    # search for all input signals within sorted node and put them into conversion line
    for i in range(0, target_number - 1):
        target_position = sorted_node.find("target", start_index)
        # get input signal from node
        input_signal = sorted_node[start_index:target_position - 1]
        # append input signal to conversion line
        conversion_line = conversion_line + str(input_signal)
        # if node processing is not completed
        if i < target_number - 2:
            # append "+" sign to conversion line
            conversion_line = conversion_line + str(" + ")

        # update start_index to point where to search for next input signal within sorted node
        start_index = target_position + TARGET_OFFSET

    # append conversion line to configuration file
    configuration_file.append(conversion_line)

    # return configuration file
    return configuration_file


# Function:
# convert_sub()
#
# Description:
# This function is responsible for conversion of sorted node with SUB action into converted node in format
# required by configuration file.
#
# Returns:
# This function returns configuration file.
def convert_sub(configuration_file, sorted_node):

    # find position of output signal within sorted node
    target_last_position = sorted_node.rfind("target")
    # get action uid
    action_uid = sorted_node[target_last_position + ACTION_UID_OFFSET:target_last_position - 1]
    # append action uid to configuration file
    configuration_file.append(str("COM Action SUB ") + str(action_uid))
    # find output signal within sorted node
    output_signal = mcg_cc_supporter.find_output_signal(sorted_node)
    # append output signal to conversion line
    conversion_line = str("INS ") + str(output_signal) + str(" = ")

    # count number of keyword "target"
    # number of "target" occurrences is required to calculate how many input signals are
    # consumed by node with SUB action, i.e. basing on the format and content of sorted node
    # with SUB action, the number of input signals is equal to (target_number - 1)
    target_number = sorted_node.count("target")

    # search input signals within sorted node starting from this position
    start_index = 0

    # search for all input signals within sorted node and put them into conversion line
    for i in range(0, target_number - 1):
        target_position = sorted_node.find("target", start_index)
        # get input signal from node
        input_signal = sorted_node[start_index:target_position - 1]
        # append input signal to conversion line
        conversion_line = conversion_line + str(input_signal)
        # if node processing is not completed
        if i < target_number - 2:
            # append "-" sign to conversion line
            conversion_line = conversion_line + str(" - ")

        # update start_index to point where to search for next input signal within sorted node
        start_index = target_position + TARGET_OFFSET

    # append conversion line to configuration file
    configuration_file.append(conversion_line)

    # return configuration file
    return configuration_file


# Function:
# convert_signal_target_signal()
#
# Description:
# This function is responsible for conversion of sorted node with signal target signal into converted node in format
# required by configuration file.
#
# Returns:
# This function returns configuration file.
def convert_signal_target_signal(configuration_file, sorted_node):

    # find position of output signal within sorted node
    target_position = sorted_node.find("target")

    # find output signal within sorted node
    output_signal = mcg_cc_supporter.find_output_signal(sorted_node)

    # find input signal within sorted node
    input_signal = sorted_node[0:target_position-1]

    # append input and output signal to conversion line
    conversion_line = str("INS ") + str(output_signal) + str(" = ") + str(input_signal)

    # append conversion line to configuration file
    configuration_file.append(conversion_line)

    # return configuration file
    return configuration_file


# Function:
# convert_component()
#
# Description:
# This function is responsible for conversion of component content into configuration file.
#
# Returns:
# This function does not return anything.
def convert_component(sorted_node_list, input_interface_list, output_interface_list, local_parameter_list,
                      component_source, component_name):

    # configuration file
    configuration_file = []

    # component conversion
    print("*************************** COMPONENT CONVERSION ***************************")
    print()

    # print component details
    print("Component Source:    " + str(component_source))
    print("Component Name:      " + str(component_name))

    # append start marker of new module section to configuration file
    configuration_file.append(str("MODULE START"))

    # append file name to configuration file
    configuration_file.append(str("COMPONENT SOURCE ") + str(component_source))

    # append diagram name to configuration file
    configuration_file.append(str("COMPONENT NAME ") + str(component_name))

    # append start marker of input interface section to configuration file
    configuration_file.append(str("INPUT INTERFACE START"))

    # append input interface details to configuration file
    for input_interface in input_interface_list:
        # get signal name
        signal_name = input_interface[0]
        # get signal type
        signal_type = input_interface[1]
        # get configuration file line
        configuration_file_line = "type " + str(signal_type) + " name " + str(signal_name)
        # append configuration file line to configuration file
        configuration_file.append(configuration_file_line)

    # append end marker of input interface section to configuration file
    configuration_file.append(str("INPUT INTERFACE END"))

    # append start marker of output interface section to configuration file
    configuration_file.append(str("OUTPUT INTERFACE START"))

    # append output interface details to configuration file
    for output_interface in output_interface_list:
        # get signal name
        signal_name = output_interface[0]
        # get signal type
        signal_type = output_interface[1]
        # get configuration file line
        configuration_file_line = "type " + str(signal_type) + " name " + str(signal_name)
        # append configuration file line to configuration file
        configuration_file.append(configuration_file_line)

    # append end marker of output interface section to configuration file
    configuration_file.append(str("OUTPUT INTERFACE END"))

    # append start marker of local parameters section to configuration file
    configuration_file.append(str("LOCAL PARAMETERS START"))

    # append local parameters details to configuration file
    for local_parameter in local_parameter_list:
        # get signal name
        signal_name = local_parameter[0]
        # get signal type
        signal_type = local_parameter[1]
        # get configuration file line
        configuration_file_line = "type " + str(signal_type) + " name " + str(signal_name)
        # append configuration file line to configuration file
        configuration_file.append(configuration_file_line)

    # append end marker of local parameters section to configuration file
    configuration_file.append(str("LOCAL PARAMETERS END"))

    # append start marker of function body section to configuration file
    configuration_file.append(str("BODY START"))

    print("*** CONVERT NODES ***")

    # repeat for all nodes from sorted list of nodes
    for sorted_node in sorted_node_list:

        # if sorted node contains ADD action
        if " ADD " in sorted_node:
            # convert ADD action
            configuration_file = convert_add(configuration_file, sorted_node)

        # if sorted node contains SUB action
        if " SUB " in sorted_node:
            # convert ADD action
            configuration_file = convert_sub(configuration_file, sorted_node)

        # if sorted node contains signal target signal
        action_type_found = mcg_cc_supporter.check_if_reference_contains_action_type(sorted_node)

        # if sorted node does not contain any action
        if (not action_type_found) and ("target empty" not in sorted_node):
            # convert signal target signal
            configuration_file = convert_signal_target_signal(configuration_file, sorted_node)

    print("*** NODES CONVERTED ***")
    print()

    # append end marker of function body section to configuration file
    configuration_file.append(str("BODY END"))

    # append end marker of new module section to configuration file
    configuration_file.append(str("MODULE END"))

    # display additional details after component conversion for test run
    if MCG_CC_TEST_RUN:

        print("Configuration File:")
        for line in configuration_file:
            print("          " + str(line))
        print()

    # end of component conversion
    print("************************ END OF COMPONENT CONVERSION ***********************")
    print()


# Function:
# process_components()
#
# Description:
# This function is responsible for processing of component content from .exml file
# into configuration file.
#
# Returns:
# This function does not return anything.
def process_components(model_dir_path):
    # get activity directory path
    activity_dir_path = model_dir_path + str("\\Standard.Activity")

    # get list of activity sources, i.e. names of exml files
    activity_source_list = listdir(activity_dir_path)

    # read and sort activity details
    for activity_source in activity_source_list:
        # get activity file path
        activity_file_path = activity_dir_path + str("\\") + str(activity_source)

        # read component content
        node_list, action_list, input_interface_list, output_interface_list, local_parameter_list, \
            model_element_source, model_element_name, \
            model_element_type = mcg_cc_component_reader.read_component(activity_file_path)

        # check errors
        if "Standard.Package" not in model_element_type:
            mcg_cc_error_handler.check_errors(model_element_source, model_element_name, model_element_type)

        # if node list is not empty, then sort nodes
        if len(node_list) > 0:

            # sort component content
            sorted_node_list = mcg_cc_component_sorter.sort_component(node_list, action_list,
                                                                      local_parameter_list, model_element_source,
                                                                      model_element_name)

            # check errors
            if "Standard.Package" not in model_element_type:
                mcg_cc_error_handler.check_errors(model_element_source, model_element_name, model_element_type)

            # if sorted list of nodes is not empty, then convert nodes
            if len(sorted_node_list) > 0:

                # convert component content
                convert_component(sorted_node_list, input_interface_list, output_interface_list, local_parameter_list,
                                  model_element_source, model_element_name)


# Function:
# process_packages()
#
# Description:
# This function is responsible for processing of package content from .exml file
# into configuration file.
#
# Returns:
# This function does not return anything.
def process_packages(model_dir_path):
    # get activity directory path
    activity_dir_path = model_dir_path + str("\\Standard.Activity")

    # get list of activity sources, i.e. names of exml files
    activity_source_list = listdir(activity_dir_path)

    # read and sort activity details
    for activity_source in activity_source_list:
        # get activity file path
        activity_file_path = activity_dir_path + str("\\") + str(activity_source)

        # read package content
        node_list, structure_list, component_list, input_interface_list, output_interface_list, local_data_list, \
            model_element_source, model_element_name, \
            model_element_type = mcg_cc_package_reader.read_package(activity_file_path)

        # check errors
        if "Standard.Component" not in model_element_type:
            mcg_cc_error_handler.check_errors(model_element_source, model_element_name, model_element_type)

        # if node list is not empty, then sort nodes
        if len(node_list) > 0:
            # sort package content
            sorted_node_list = mcg_cc_package_sorter.sort_package(node_list, component_list, local_data_list,
                                                                  model_element_source, model_element_name)


# Function:
# convert_model()
#
# Description:
# This is main function of this module and is responsible for conversion of .exml file
# into configuration file.
#
# Returns:
# This function does not return anything.
def convert_model(model_dir_path):

    # process components content from .exml files into configuration file
    process_components(model_dir_path)

    # process packages content from .exml files into configuration file
    process_packages(model_dir_path)


# Mod Code Generator (MCG) Converter Component (CC) entrance

# display short notice
print()
print("Mod Code Generator (MCG)")
print("Copyright (C) 2021 Kamil Deć github.com/deckamil")
print("This is Converter Component (CC) of Mod Code Generator (MCG)")
print()
print("License GPLv3+: GNU GPL version 3 or later.")
print("This is free software; see the source for copying conditions. There is NO")
print("warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.")
print()

# check if number of command line arguments is correct
if len(argv) - 1 == NUMBER_OF_MCG_CC_CMD_LINE_ARGS:

    # set model directory path to cmd line argument
    model_dir_path = str(argv[1])

    # convert model
    convert_model(model_dir_path)

# else display info and exit
else:
    print("Incorrect number of command line arguments, MCG CC process cancelled.")
