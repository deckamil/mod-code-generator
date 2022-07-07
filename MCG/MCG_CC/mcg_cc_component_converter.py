#   FILE:           mcg_cc_component_converter.py
#
#   DESCRIPTION:
#       This module contains definition of ComponentConverter class, which is
#       responsible for conversion of component content into configuration file
#       format.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           7 JUL 2022
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
from mcg_cc_logger import Logger


# Description:
# This class allows to convert component content into configuration file format.
class ComponentConverter(Converter):

    # Description:
    # This method is responsible for conversion of action interaction into configuration file.
    def convert_action_interaction(self, sorted_node, math_symbol):

        # append interaction comment to configuration file
        self.configuration_file.append(str("COM Action Interaction ") + str(sorted_node.node_interaction))
        # append beginning of action interaction to conversion line
        conversion_line = str("INS ") + str(sorted_node.node_output) + str(" = ")

        # search for all input signal names within sorted node and put them into conversion line
        for i in range(0, len(sorted_node.node_input_list)):
            # find input signal name within sorted node
            node_input = sorted_node.node_input_list[i]
            # append input signal name to conversion line
            conversion_line = conversion_line + str(node_input)
            # if sorted node processing is not completed
            if i < len(sorted_node.node_input_list) - 1:
                # append math symbol to conversion line
                conversion_line = conversion_line + str(" ") + str(math_symbol) + str(" ")

        # append conversion line to configuration file
        self.configuration_file.append(conversion_line)

    # Description:
    # This method is responsible for conversion of signal assignment into configuration file.
    def convert_signal_assignment(self, sorted_node):

        # find output signal name within sorted node
        node_output = sorted_node.node_output
        # find input signal name within sorted node
        node_input = sorted_node.node_input_list[0]

        # append input and output signal to conversion line
        conversion_line = str("INS ") + str(node_output) + str(" = ") + str(node_input)

        # append conversion line to configuration file
        self.configuration_file.append(conversion_line)

    # Description:
    # This method is responsible for converting of component content into configuration file.
    def convert_component(self):

        # component converter
        Logger.save_in_log_file(">>>>>>>>>>>>>>>>>>>>>>>>>>>> COMPONENT CONVERTER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

        # convert header
        Logger.save_in_log_file("*** convert header")

        # append start marker of new component section to configuration file
        self.configuration_file.append(str("COMPONENT START"))

        # append file name to configuration file
        self.configuration_file.append(str("COMPONENT SOURCE ") + str(self.activity_source))

        # append component name to configuration file
        self.configuration_file.append(str("COMPONENT NAME ") + str(self.model_element_name))

        # convert interface details to configuration file
        self.convert_interfaces(str("COMPONENT"))

        # convert body
        Logger.save_in_log_file("*** convert body")

        # append start marker of function body section to configuration file
        self.configuration_file.append(str("COMPONENT BODY START"))

        # repeat for all nodes from sorted node list
        for sorted_node in self.sorted_node_list:

            # if sorted node contains ADD action
            if "ADD " in sorted_node.node_interaction:
                # convert ADD action
                self.convert_action_interaction(sorted_node, "+")

            # if sorted node contains SUB action
            if "SUB " in sorted_node.node_interaction:
                # convert SUB action
                self.convert_action_interaction(sorted_node, "-")

            # if sorted node contains MUL action
            if "MUL " in sorted_node.node_interaction:
                # convert MUL action
                self.convert_action_interaction(sorted_node, "*")

            # if sorted node contains DIV action
            if "DIV " in sorted_node.node_interaction:
                # convert DIV action
                self.convert_action_interaction(sorted_node, "/")

            # if sorted node contains ASSIGNMENT action
            if "ASSIGNMENT" in sorted_node.node_interaction:
                # convert ASSIGNMENT action
                self.convert_signal_assignment(sorted_node)

        # append end marker of function body section to configuration file
        self.configuration_file.append(str("COMPONENT BODY END"))

        # append end marker of new component section to configuration file
        self.configuration_file.append(str("COMPONENT END"))

        # save configuration file
        self.save_in_configuration_file()

        # process completed
        Logger.save_in_log_file("PROCESS COMPLETED")

        # display additional details after component conversion
        Logger.save_in_log_file("")
        Logger.save_in_log_file("Configuration File:")
        for line in self.configuration_file:
            Logger.save_in_log_file("          " + str(line))

        # end of component converter
        Logger.save_in_log_file("\n>>>>>>>>>>>>>>>>>>>>>>>> END OF COMPONENT CONVERTER <<<<<<<<<<<<<<<<<<<<<<<<<<<")
