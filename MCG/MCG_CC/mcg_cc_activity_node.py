#   FILE:           mcg_cc_activity_node.py
#
#   DESCRIPTION:
#       This module contains definition of ActivityNode class, which represents node on
#       activity diagram, i.e. interaction together with its input and output data.
#
#   COPYRIGHT:      Copyright (C) 2021-2023 Kamil Deć github.com/deckamil
#   DATE:           25 DEC 2023
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


# Description:
# This class represents node on activity diagram, i.e. interaction together with its input and output data.
class ActivityNode(object):

    # Indexes of interface element list
    DATA_NAME_INDEX = 0
    PIN_NAME_INDEX = 1

    # Node types
    UNKNOWN = 10
    DATA = 20
    ACTION = 30
    OPERATION = 40
    CONDITION = 50

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        self.input_data_list = []
        self.interaction = "UNKNOWN"
        self.uid = "UNKNOWN"
        self.type = ActivityNode.UNKNOWN
        self.dependency_list = []
        self.output_data_list = []

    # Description:
    # This method returns string representation of ActivityNode class.
    def __str__(self):

        if self.type == ActivityNode.OPERATION:

            # append input data
            line = "$INPUTS$: "
            for input_data in self.input_data_list:
                line = line + input_data[ActivityNode.DATA_NAME_INDEX] + \
                       "->" + input_data[ActivityNode.PIN_NAME_INDEX] + " "

            # append interaction and uid
            line = line + "$OPERATION$: " + self.interaction + " " + self.uid + " "

            # append output data
            line = line + "$OUTPUTS$: "
            for output_data in self.output_data_list:
                line = line + output_data[ActivityNode.PIN_NAME_INDEX] + \
                       "->" + output_data[ActivityNode.DATA_NAME_INDEX] + " "

            # remove spare whitespace
            line = line[0:len(line) - 1]

        elif self.type == ActivityNode.ACTION:

            # append input data
            line = "$INPUTS$: "
            for input_data in self.input_data_list:
                line = line + input_data[ActivityNode.DATA_NAME_INDEX] + " "

            # append interaction and uid
            line = line + "$ACTION$: " + self.interaction + " " + self.uid + " "

            # append output data
            line = line + "$OUTPUT$: " + self.output_data_list[0][ActivityNode.DATA_NAME_INDEX]

        elif self.type == ActivityNode.DATA:

            # append input data
            line = "$INPUT$: " + self.input_data_list[0][ActivityNode.DATA_NAME_INDEX] + " "

            # append interaction
            line = line + "$ASSIGNMENT$: "

            # append output data
            line = line + "$OUTPUT$: " + self.output_data_list[0][ActivityNode.DATA_NAME_INDEX]

        elif self.type == ActivityNode.CONDITION:

            # append interaction and uid
            line = "$CONDITION$: " + self.interaction + " " + self.uid + " "

            # append output data
            line = line + "$OUTPUTS$: "
            for output_data in self.output_data_list:
                line = line + output_data[ActivityNode.DATA_NAME_INDEX] + " "

            # remove spare whitespace
            line = line[0:len(line) - 1]

        else:

            line = "$UNKNOWN$"

        # return string representation
        return line
