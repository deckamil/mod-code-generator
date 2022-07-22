#   FILE:           mcg_cc_package_converter.py
#
#   DESCRIPTION:
#       This module contains definition of PackageConverter class, which is
#       responsible for conversion of package content into configuration file
#       format.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           22 JUL 2022
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
#       Under Section 7 of GPL version 3, you are granted additional
#       permissions described in the MCG Output Exception, version 1, which
#       copy you should have received along with this program.
#
#       You should have received a copy of the GNU General Public License
#       along with this program. If not, see <https://www.gnu.org/licenses/>.


from mcg_cc_converter import Converter
from mcg_cc_supporter import Supporter
from mcg_cc_logger import Logger


# Description:
# This class allows to convert package content into configuration file format.
class PackageConverter(Converter):

    # Description:
    # This method is responsible for conversion of component interaction into configuration file.
    def convert_component_interaction(self, sorted_node):

        # find component name
        component_name = sorted_node.node_interaction[0:len(sorted_node.node_interaction) + Supporter.UID_OFFSET]
        # append interaction comment to configuration file
        self.configuration_file.append(str("COM Component Interaction ") + str(sorted_node.node_interaction))
        # append beginning of component interaction to conversion line
        conversion_line = str("INV ") + str(sorted_node.node_output) + str(" = ") + str(component_name) + str(" (")

        # search for all input structure names within sorted node and put them into conversion line
        for i in range(0, len(sorted_node.node_input_list)):
            # find input structure name within sorted node
            node_input = sorted_node.node_input_list[i]
            # append input structure name to conversion line
            conversion_line = conversion_line + str(node_input)
            # if sorted node processing is not completed
            if i < len(sorted_node.node_input_list) - 1:
                # append separator symbol to conversion line
                conversion_line = conversion_line + str(", ")

        # close component interaction
        conversion_line = conversion_line + str(")")

        # append conversion line to configuration file
        self.configuration_file.append(conversion_line)

        # record info
        Logger.save_in_log_file("Converter", "Have converted to " + str(conversion_line) + " line", False)

    # Description:
    # This method is responsible for conversion of structure assignment into configuration file.
    def convert_structure_assignment(self, sorted_node):

        # append Output Interface structure to conversion line
        conversion_line = str("ASI Output Interface = (")

        # search for all input structure names within sorted node and put them into conversion line
        for i in range(0, len(sorted_node.node_input_list)):
            # find input structure name within sorted node
            node_input = sorted_node.node_input_list[i]
            # append input structure name to conversion line
            conversion_line = conversion_line + str(node_input)
            # if sorted node processing is not completed
            if i < len(sorted_node.node_input_list) - 1:
                # append separator symbol to conversion line
                conversion_line = conversion_line + str(", ")

        # close structure assignment
        conversion_line = conversion_line + str(")")

        # append conversion line to configuration file
        self.configuration_file.append(conversion_line)

        # record info
        Logger.save_in_log_file("Converter", "Have converted to " + str(conversion_line) + " line", False)

    # Description:
    # This method is responsible for converting of package content into configuration file.
    def convert_package(self):

        # record info
        Logger.save_in_log_file("Converter", "Converting module source and name into configuration file", True)

        # append start marker of new package section to configuration file
        self.configuration_file.append(str("PACKAGE START"))

        # append file name to configuration file
        self.configuration_file.append(str("PACKAGE SOURCE ") + str(self.activity_source))

        # append package name to configuration file
        self.configuration_file.append(str("PACKAGE NAME ") + str(self.model_element_name))

        # record info
        Logger.save_in_log_file("Converter", "Have converted to "
                                + str(self.configuration_file[len(self.configuration_file) - 2]) + " line", False)
        Logger.save_in_log_file("Converter", "Have converted to "
                                + str(self.configuration_file[len(self.configuration_file) - 1]) + " line", False)

        # convert interface details to configuration file
        self.convert_interfaces("PACKAGE")

        # record info
        Logger.save_in_log_file("Converter", "Converting module body into configuration file", False)

        # append start marker of function body section to configuration file
        self.configuration_file.append(str("PACKAGE BODY START"))

        # repeat for all nodes from sorted node list
        for sorted_node in self.sorted_node_list:

            # if sorted node does not contain ASSIGNMENT interaction
            if sorted_node.node_interaction != "ASSIGNMENT":
                # convert component interaction
                self.convert_component_interaction(sorted_node)
            else:
                # convert structure assignment
                self.convert_structure_assignment(sorted_node)

        # append end marker of function body section to configuration file
        self.configuration_file.append(str("PACKAGE BODY END"))

        # append end marker of new package section to configuration file
        self.configuration_file.append(str("PACKAGE END"))

        # record info
        Logger.save_in_log_file("Converter", "Saving conversion results into configuration file", False)

        # save configuration file
        self.save_in_configuration_file()
