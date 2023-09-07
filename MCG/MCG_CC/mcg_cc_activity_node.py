#   FILE:           mcg_cc_activity_node.py
#
#   DESCRIPTION:
#       This module contains definition of ActivityNode class, which represents node on
#       activity diagram, i.e. interaction together with its input and output data.
#
#   COPYRIGHT:      Copyright (C) 2021-2023 Kamil Deć github.com/deckamil
#   DATE:           7 SEP 2023
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

    # indexes of interface element list
    DATA_NAME_INDEX = 0
    PIN_NAME_INDEX = 1

    # interaction types
    UNKNOWN = 10
    DATA = 30
    ACTION = 40
    OPERATION = 50

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        self.input_data_list = []
        self.name = "N/A"
        self.uid = "N/A"
        self.type = ActivityNode.UNKNOWN
        self.output_data_list = []

    # Description:
    # This method returns string representation of ActivityNode class.
    def __str__(self):
        # append input marker
        line = "$INPUTS$: "

        # if node is operation type
        if self.type == ActivityNode.OPERATION:

            # append input data
            for input_data in self.input_data_list:
                line = line + input_data[ActivityNode.DATA_NAME_INDEX] + \
                       "->" + input_data[ActivityNode.PIN_NAME_INDEX] + " "

            # append interaction name and uid
            line = line + "$INTERACTION$: " + self.name + "() " + self.uid + " "

            # append output marker and data
            line = line + "$OUTPUT$: "

            # append output data
            for output_data in self.output_data_list:
                line = line + output_data[ActivityNode.PIN_NAME_INDEX] + \
                       "->" + output_data[ActivityNode.DATA_NAME_INDEX] + " "

            # remove spare whitespace
            line = line[0:len(line)-1]

        # if node is action type
        elif self.type == ActivityNode.ACTION:

            # append input data
            for input_data in self.input_data_list:
                line = line + input_data[ActivityNode.DATA_NAME_INDEX] + " "

            # append interaction name and uid
            line = line + "$INTERACTION$: " + self.name + " " + self.uid + " "

            # get output data
            output_data = self.output_data_list[0]

            # append output marker and data
            line = line + "$OUTPUT$: " + output_data[ActivityNode.DATA_NAME_INDEX]

        # if there is no interaction, but only connection between two data points
        else:

            # append input data
            for input_data in self.input_data_list:
                line = line + input_data[ActivityNode.DATA_NAME_INDEX] + " "

            # append interaction name
            line = line + "$INTERACTION$: ASSIGNMENT "

            # get output data
            output_data = self.output_data_list[0]

            # append output marker and data
            line = line + "$OUTPUT$: " + output_data[ActivityNode.DATA_NAME_INDEX]

        # return string representation
        return line
