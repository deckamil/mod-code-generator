#   FILE:           mcg_cc_component_converter.py
#
#   DESCRIPTION:
#       This module contains definition of ComponentConverter class, which is child
#       class of Converter class and is responsible for conversion of component content
#       into configuration file.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           10 OCT 2021
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


# Class:
# ComponentConverter()
#
# Description:
# This is child class responsible for converting of component content into configuration file.
class ComponentConverter(Converter):

    # Method:
    # convert_action()
    #
    # Description:
    # This method is responsible for conversion of sorted node with action into configuration file.
    #
    # Returns:
    # This method does not return anything.
    def convert_action(self, sorted_node, action_type, math_symbol):

        # find target last position within sorted node
        target_last_position = sorted_node.rfind("target")
        # find action uid within sorted node
        action_uid = sorted_node[target_last_position + Supporter.ACTION_UID_OFFSET:target_last_position - 1]
        # find output signal name within sorted node
        output_signal_name = sorted_node[target_last_position + Supporter.TARGET_OFFSET:len(sorted_node)]
        # append action uid to configuration file
        self.configuration_file.append(str("COM Action ") + str(action_type) + str(" ") + str(action_uid))
        # append output signal name to conversion line
        conversion_line = str("INS ") + str(output_signal_name) + str(" = ")

        # count number of keyword "target"
        # number of "target" occurrences is required to calculate how many input signals are
        # consumed by node with action, i.e. basing on the format and content of sorted node
        # with action, the number of input signals is equal to (target_number - 1)
        target_number = sorted_node.count("target")

        # search input signals within sorted node starting from this position
        start_index = 0

        # search for all input signal names within sorted node and put them into conversion line
        for i in range(0, target_number - 1):
            target_position = sorted_node.find("target", start_index)
            # find input signal name within sorted node
            input_signal_name = sorted_node[start_index:target_position - 1]
            # append input signal name to conversion line
            conversion_line = conversion_line + str(input_signal_name)
            # if sorted node processing is not completed
            if i < target_number - 2:
                # append math symbol to conversion line
                conversion_line = conversion_line + str(" ") + str(math_symbol) + str(" ")

            # update start_index to point where to search for next input signal name within sorted node
            start_index = target_position + Supporter.TARGET_OFFSET

        # append conversion line to configuration file
        self.configuration_file.append(conversion_line)

    # Method:
    # convert_signal_assignment()
    #
    # Description:
    # This method is responsible for conversion of sorted node with signal assignment into configuration file.
    #
    # Returns:
    # This method does not return anything.
    def convert_signal_assignment(self, sorted_node):

        # find target last position within sorted node
        target_last_position = sorted_node.rfind("target")
        # find output signal name within sorted node
        output_signal_name = sorted_node[target_last_position + Supporter.TARGET_OFFSET:len(sorted_node)]
        # find input signal name within sorted node
        input_signal_name = sorted_node[0:target_last_position - 1]

        # append input and output signal to conversion line
        conversion_line = str("INS ") + str(output_signal_name) + str(" = ") + str(input_signal_name)

        # append conversion line to configuration file
        self.configuration_file.append(conversion_line)

    # Method:
    # convert_component()
    #
    # Description:
    # This method is responsible for converting of component content into configuration file.
    #
    # Returns:
    # This method does not return anything.
    def convert_component(self):

        # component conversion
        print("*************************** COMPONENT CONVERSION ***************************")
        print()

        # print component details
        print("Component Source:    " + str(self.activity_source))
        print("Component Name:      " + str(self.model_element_name))

        # append start marker of new component section to configuration file
        self.configuration_file.append(str("COMPONENT START"))

        # append file name to configuration file
        self.configuration_file.append(str("COMPONENT SOURCE ") + str(self.activity_source))

        # append component name to configuration file
        self.configuration_file.append(str("COMPONENT NAME ") + str(self.model_element_name))

        # convert interface details to configuration file
        self.convert_interfaces()

        # append start marker of function body section to configuration file
        self.configuration_file.append(str("BODY START"))

        print("*** CONVERT NODES ***")

        # repeat for all nodes from sorted node list
        for sorted_node in self.sorted_node_list:

            # if sorted node contains ADD action
            if " ADD " in sorted_node:
                # convert ADD action
                self.convert_action(sorted_node, "ADD", "+")

            # if sorted node contains SUB action
            if " SUB " in sorted_node:
                # convert ADD action
                self.convert_action(sorted_node, "SUB", "-")

            # if sorted node contains signal target signal
            action_type_found = Supporter.check_if_reference_contains_action_type(sorted_node)

            # if sorted node does not contain any action
            if (not action_type_found) and ("target empty" not in sorted_node):
                # convert signal target signal
                self.convert_signal_assignment(sorted_node)

        print("*** NODES CONVERTED ***")
        print()

        # append end marker of function body section to configuration file
        self.configuration_file.append(str("BODY END"))

        # append end marker of new component section to configuration file
        self.configuration_file.append(str("COMPONENT END"))

        # display additional details after component conversion for test run
        if Supporter.MCG_CC_TEST_RUN:

            print("Configuration File:")
            for line in self.configuration_file:
                print("          " + str(line))
            print()

        # end of component conversion
        print("************************ END OF COMPONENT CONVERSION ***********************")
        print()
