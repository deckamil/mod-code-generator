#   FILE:           mcg_cc_main.py
#
#   DESCRIPTION:
#       This is main module of Mod Code Generator (MCG) Converter Component (CC)
#       and is responsible for conversion of component and package content from
#       .exml file into configuration file, which will be used by Mod Code Generator
#       (MCG) Code Generator Component (CGC) to generate C code for the model.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           6 OCT 2021
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


from sys import argv
import mcg_cc_error_handler
from mcg_cc_parameters import MCG_CC_TEST_RUN
from mcg_cc_parameters import TARGET_OFFSET
from mcg_cc_parameters import NUMBER_OF_MCG_CC_CMD_LINE_ARGS
from mcg_cc_file_finder import FileFinder
from mcg_cc_component_reader import ComponentReader
from mcg_cc_package_reader import PackageReader
from mcg_cc_component_sorter import ComponentSorter
from mcg_cc_package_sorter import PackageSorter
from mcg_cc_component_converter import ComponentConverter


# Function:
# convert_call()
#
# Description:
# This function is responsible for conversion of sorted node with component call into converted node in format
# required by configuration file.
#
# Returns:
# This function returns configuration file.
def convert_call(configuration_file, sorted_node):

    # find output structure position within sorted node
    output_structure_position = sorted_node.rfind("target")
    # find output structure name within sorted node
    output_structure_name = sorted_node[output_structure_position + TARGET_OFFSET:len(sorted_node)]
    # append output structure name to conversion line
    conversion_line = str("CAL ") + str(output_structure_name) + str(" = ")

    # find component position within sorted node
    component_position = sorted_node.rfind("target", 0, output_structure_position)
    # find component name within sorted node
    component_name = sorted_node[component_position + TARGET_OFFSET:output_structure_position-1]
    # append component name to conversion line
    conversion_line = conversion_line + str(component_name) + str("(")

    # append conversion line to configuration file
    configuration_file.append(conversion_line)

    # return configuration file
    return configuration_file


# Function:
# convert_package()
#
# Description:
# This function is responsible for conversion of package content into configuration file.
#
# Returns:
# This function does not return anything.
def convert_package(sorted_node_list, input_interface_list, output_interface_list, local_data_list,
                    activity_source, model_element_name, interaction_list):

    # configuration file
    configuration_file = []

    # package conversion
    print("**************************** PACKAGE CONVERSION ****************************")
    print()

    # print package details
    print("Package Source:      " + str(activity_source))
    print("Package Name:        " + str(model_element_name))

    # append start marker of new package section to configuration file
    configuration_file.append(str("PACKAGE START"))

    # append file name to configuration file
    configuration_file.append(str("PACKAGE SOURCE ") + str(activity_source))

    # append package name to configuration file
    configuration_file.append(str("PACKAGE NAME ") + str(model_element_name))

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
    configuration_file.append(str("LOCAL DATA START"))

    # append local data details to configuration file
    for local_data in local_data_list:
        # get structure name
        structure_name = local_data[0]
        # get structure type
        structure_type = local_data[1]
        # get configuration file line
        configuration_file_line = "type " + str(structure_type) + " name " + str(structure_name)
        # append configuration file line to configuration file
        configuration_file.append(configuration_file_line)

    # append end marker of local parameters section to configuration file
    configuration_file.append(str("LOCAL DATA END"))

    # append start marker of function body section to configuration file
    configuration_file.append(str("BODY START"))

    print("*** CONVERT NODES ***")

    # repeat for all nodes from sorted node list
    for sorted_node in sorted_node_list:

        # if sorted node contains interaction
        for interaction in interaction_list:
            keyword = "target " + str(interaction) + " target"
            # if keyword for given interaction is found
            if keyword in sorted_node:
                # convert call
                configuration_file = convert_call(configuration_file, sorted_node)

    print("*** NODES CONVERTED ***")
    print()

    # append end marker of function body section to configuration file
    configuration_file.append(str("BODY END"))

    # append end marker of new package section to configuration file
    configuration_file.append(str("PACKAGE END"))

    # display additional details after package conversion for test run
    if MCG_CC_TEST_RUN:

        print("Configuration File:")
        for line in configuration_file:
            print("          " + str(line))
        print()

    # end of package conversion
    print("************************* END OF PACKAGE CONVERSION ************************")
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
def process_components():

    # files marker shows whether desired component files were found or not
    files_found = True

    # repeat until all components are converted into configuration file
    while files_found:

        # find component files
        file_finder_list = FileFinder.find_files("Standard.Component")
        # get files marker
        files_found = file_finder_list[FileFinder.FILES_FOUND_INDEX]

        # if component files were found
        if files_found:

            # check errors
            mcg_cc_error_handler.check_errors(file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                              file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                              "Standard.Component")

            # initialize component reader
            component_reader = ComponentReader(file_finder_list)
            # read component content
            component_reader_list = component_reader.read_component()

            # check errors
            mcg_cc_error_handler.check_errors(file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                              file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                              "Standard.Component")

            # initialize component sorter
            component_sorter = ComponentSorter(component_reader_list)
            # sort component content
            component_sorter_list = component_sorter.sort_component()

            # check errors
            mcg_cc_error_handler.check_errors(file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                              file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                              "Standard.Component")

            # initialize component converter
            component_converter = ComponentConverter(component_reader_list, component_sorter_list)
            # convert component content
            component_converter.convert_component()


# Function:
# process_packages()
#
# Description:
# This function is responsible for processing of package content from .exml file
# into configuration file.
#
# Returns:
# This function does not return anything.
def process_packages():

    # files marker shows whether desired package files were found or not
    files_found = True

    # repeat until all packages are converted into configuration file
    while files_found:

        # find package files
        file_finder_list = FileFinder.find_files("Standard.Package")
        # get files marker
        files_found = file_finder_list[FileFinder.FILES_FOUND_INDEX]

        # if package files were found
        if files_found:

            # check errors
            mcg_cc_error_handler.check_errors(file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                              file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                              "Standard.Package")

            # initialize package reader
            package_reader = PackageReader(file_finder_list)
            # read package content
            package_reader_list = package_reader.read_package()

            # check errors
            mcg_cc_error_handler.check_errors(file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                              file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                              "Standard.Package")

            # initialize package sorter
            package_sorter = PackageSorter(package_reader_list)
            # sort package content
            package_sorter_list = package_sorter.sort_package()

            # check errors
            mcg_cc_error_handler.check_errors(file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX],
                                              file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX],
                                              "Standard.Package")

            # convert package content
            convert_package(package_sorter_list[PackageSorter.SORTED_NODE_LIST_INDEX],
                            package_reader_list[PackageReader.INPUT_INTERFACE_LIST_INDEX],
                            package_reader_list[PackageReader.OUTPUT_INTERFACE_LIST_INDEX],
                            package_reader_list[PackageReader.LOCAL_DATA_LIST_INDEX],
                            package_reader_list[PackageReader.ACTIVITY_SOURCE_INDEX],
                            package_reader_list[PackageReader.MODEL_ELEMENT_NAME_INDEX],
                            package_reader_list[PackageReader.INTERACTION_LIST_INDEX])


# Function:
# convert_model()
#
# Description:
# This is main function of this module and is responsible for conversion of .exml file
# into configuration file.
#
# Returns:
# This function does not return anything.
def convert_model():

    # process components content from .exml files into configuration file
    process_components()

    # process packages content from .exml files into configuration file
    process_packages()


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

    # get model directory path from cmd line argument
    model_dir_path = str(argv[1])

    # set path to model directory
    FileFinder.set_paths(model_dir_path)

    # convert model
    convert_model()

# else display info and exit
else:
    print("Incorrect number of command line arguments, MCG CC process cancelled.")
