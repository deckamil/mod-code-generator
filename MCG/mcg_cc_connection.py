#   FILE:           mcg_cc_connection.py
#
#   DESCRIPTION:
#       This module contains definition of Connection class, which represents connection
#       between two model elements from activity diagram.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           21 JAN 2022
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
# Connection()
#
# Description:
# This is base class responsible for storing details of connection between two model elements from activity diagram.
class Connection(object):

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
        self.connection_source = ""
        self.connection_target = ""

    # Method:
    # __str__()
    #
    # Description:
    # This is string representation of object data.
    #
    # Returns:
    # This method return string representation of object data.
    def __str__(self):
        # append source marker and data
        line = "$SOURCE$: " + self.connection_source + " "

        # append target marker and data
        line = line + "$TARGET$: " + self.connection_target

        # return string representation
        return line
