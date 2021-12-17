#   FILE:           mcg_cc_node.py
#
#   DESCRIPTION:
#       This module contains definition of Node class, which allows to hold together
#       all details of unique interactions form activity diagram, i.e. node inputs,
#       node interaction and node output.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           17 DEC 2021
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


# Class:
# Node()
#
# Description:
# This is base class responsible for storing details of unique interaction from activity diagram.
class Node(object):

    # Method:
    # __init__()
    #
    # Description:
    # This is class constructor.
    #
    # Returns:
    # This method does not return anything.
    def __init__(self):
        # initialize object data
        self.node_input_list = []
        self.node_interaction = ""
        self.node_output = ""

    # Method:
    # __str__()
    #
    # Description:
    # This is string representation of object data.
    #
    # Returns:
    # This method return string representation of object data.
    def __str__(self):
        # append input marker
        line = str("$INPUTS$: ")

        # append input data to line
        for node_input in self.node_input_list:
            line = line + str(node_input) + str(" ")

        # append interaction marker and data
        line = line + str("$INTERACTION$: ") + str(self.node_interaction) + str(" ")

        # append output marker and data
        line = line + str("$OUTPUT$: ") + str(self.node_output)

        # return string representation
        return line
