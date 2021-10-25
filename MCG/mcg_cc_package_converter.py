#   FILE:           mcg_cc_package_converter.py
#
#   DESCRIPTION:
#       This module contains definition of PackageConverter class, which is child
#       class of Converter class and is responsible for conversion of package content
#       into configuration file.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           25 OCT 2021
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


from mcg_cc_converter import Converter
from mcg_cc_supporter import Supporter
from mcg_cc_logger import Logger


# Class:
# PackageConverter()
#
# Description:
# This is child class responsible for converting of package content into configuration file.
class PackageConverter(Converter):

    # Method:
    # convert_component_invocation()
    #
    # Description:
    # This method is responsible for conversion of sorted node with component invocation into configuration file.
    #
    # Returns:
    # This method does not return anything.
    def convert_component_invocation(self, sorted_node):

        # find output structure position within sorted node
        output_structure_position = sorted_node.rfind("target")
        # find output structure name within sorted node
        output_structure_name = sorted_node[output_structure_position + Supporter.TARGET_OFFSET:len(sorted_node)]
        # append output structure name to conversion line
        conversion_line = str("INV ") + str(output_structure_name) + str(" = ")

        # find component position within sorted node
        component_position = sorted_node.rfind("target", 0, output_structure_position)
        # find component name within sorted node
        component_name = sorted_node[component_position + Supporter.TARGET_OFFSET:output_structure_position - 1]
        # append component name to conversion line
        conversion_line = conversion_line + str(component_name) + str(" (")

        # count number of keyword "target"
        # number of "target" occurrences is required to calculate how many input structures are
        # consumed by node with component, i.e. basing on the format and content of sorted node
        # with component, the number of input structures is equal to (target_number - 1)
        target_number = sorted_node.count("target")

        # search input structures within sorted node starting from this position
        start_index = 0

        # search for all input structure names within sorted node and put them into conversion line
        for i in range(0, target_number - 1):
            target_position = sorted_node.find("target", start_index)
            # find input structure name within sorted node
            input_structure_name = sorted_node[start_index:target_position - 1]
            # append input structure name to conversion line
            conversion_line = conversion_line + str(input_structure_name)
            # if sorted node processing is not completed
            if i < target_number - 2:
                # append comma symbol to conversion line
                conversion_line = conversion_line + str(", ")

            # update start_index to point where to search for next input structure name within sorted node
            start_index = target_position + Supporter.TARGET_OFFSET

        # close component invocation
        conversion_line = conversion_line + str(")")

        # append conversion line to configuration file
        self.configuration_file.append(conversion_line)

    # Method:
    # convert_output_assignment()
    #
    # Description:
    # This method is responsible for conversion of sorted node with output structures assignment
    # into configuration file
    #
    # Returns:
    # This method does not return anything.
    def convert_output_assignment(self, sorted_node):

        # append Output Interface structure to conversion line
        conversion_line = str("ASI Output Interface = (")

        # count number of keyword "target"
        # number of "target" occurrences is required to calculate how many output structures are
        # consumed by node with assignment to Output Interface, i.e. basing on the format and content
        # of sorted node with assignment to Output Interface, the number of output structures is equal
        # to target_number
        target_number = sorted_node.count("target")

        # search output structures within sorted node starting from this position
        start_index = 0

        # search for all output structure names within sorted node and put them into conversion line
        for i in range(0, target_number):
            target_position = sorted_node.find("target", start_index)
            # find output structure name within sorted node
            output_structure_name = sorted_node[start_index:target_position - 1]
            # append output structure name to conversion line
            conversion_line = conversion_line + str(output_structure_name)
            # if sorted node processing is not completed
            if i < target_number - 1:
                # append pass symbol to conversion line
                conversion_line = conversion_line + str(", ")

            # update start_index to point where to search for next output structure name within sorted node
            start_index = target_position + Supporter.TARGET_OFFSET

        # close output structure assignment
        conversion_line = conversion_line + str(")")

        # append conversion line to configuration file
        self.configuration_file.append(conversion_line)

    # Method:
    # convert_package()
    #
    # Description:
    # This method is responsible for converting of package content into configuration file.
    #
    # Returns:
    # This method does not return anything.
    def convert_package(self):

        # package converter
        Logger.record_in_log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> PACKAGE CONVERTER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

        # convert header
        Logger.record_in_log("*** convert header")

        # append start marker of new package section to configuration file
        self.configuration_file.append(str("PACKAGE START"))

        # append file name to configuration file
        self.configuration_file.append(str("PACKAGE SOURCE ") + str(self.activity_source))

        # append package name to configuration file
        self.configuration_file.append(str("PACKAGE NAME ") + str(self.model_element_name))

        # convert interface details to configuration file
        self.convert_interfaces()

        # convert body
        Logger.record_in_log("*** convert body")

        # append start marker of function body section to configuration file
        self.configuration_file.append(str("BODY START"))

        # repeat for all nodes from sorted node list
        for sorted_node in self.sorted_node_list:

            # component invocation marker shows whether component invocation was found or not
            component_invocation_found = False

            # if sorted node contains component invocation
            for interaction in self.interaction_list:
                keyword = "target " + str(interaction) + " target"
                # if keyword for given interaction is found
                if keyword in sorted_node:
                    # convert component invocation
                    self.convert_component_invocation(sorted_node)
                    # change component invocation marker
                    component_invocation_found = True

            # if component invocation has not been found and sorted node does not have empty target
            if (not component_invocation_found) and ("target empty" not in sorted_node):
                # convert output assignment
                self.convert_output_assignment(sorted_node)

        # append end marker of function body section to configuration file
        self.configuration_file.append(str("BODY END"))

        # append end marker of new package section to configuration file
        self.configuration_file.append(str("PACKAGE END"))

        # save configuration file
        self.save_configuration_file()

        # process completed
        Logger.record_in_log("PROCESS COMPLETED")

        # display additional details after package conversion
        if Supporter.PRINT_EXTRA_INFO:

            # print package details
            Logger.record_in_log("")
            Logger.record_in_log("Configuration File:")
            for line in self.configuration_file:
                Logger.record_in_log("          " + str(line))

        # end of package converter
        Logger.record_in_log("\n>>>>>>>>>>>>>>>>>>>>>>>>> END OF PACKAGE CONVERTER <<<<<<<<<<<<<<<<<<<<<<<<<<<<")
