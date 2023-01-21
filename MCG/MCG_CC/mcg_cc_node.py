#   FILE:           mcg_cc_node.py
#
#   DESCRIPTION:
#       This module contains definition of Node class, which represents node on
#       activity diagram, i.e. interaction together with its input and output data.
#
#   COPYRIGHT:      Copyright (C) 2021-2023 Kamil Deć github.com/deckamil
#   DATE:           21 JAN 2023
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
class Node(object):

    # Interaction types
    UNKNOWN = 10
    ACTION = 40
    OPERATION = 50

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        self.input_list = []
        self.interaction_name = "N/A"
        self.interaction_uid = "N/A"
        self.interaction_type = Node.UNKNOWN
        self.output = "N/A"

    # Description:
    # This method returns string representation of Node class.
    def __str__(self):
        # append input marker
        line = "$INPUTS$: "

        # append input data
        for node_input in self.input_list:
            line = line + node_input + " "

        # if operation is interaction
        if self.interaction_type == Node.OPERATION:
            line = line + "$INTERACTION$: " + self.interaction_name + "() " + self.interaction_uid + " "
        # if action is interaction
        elif self.interaction_type == Node.ACTION:
            line = line + "$INTERACTION$: " + self.interaction_name + " " + self.interaction_uid + " "

        # append output marker and data
        line = line + "$OUTPUT$: " + self.output

        # return string representation
        return line
