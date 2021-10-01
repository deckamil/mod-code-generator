#   FILE:           mcg_cc_reader.py
#
#   DESCRIPTION:
#       This module contains definition of Reader class, which is responsible
#       for reading of .exml file content.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           1 OCT 2021
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


import mcg_cc_error_handler
from mcg_cc_parameters import NAME_START_OFFSET
from mcg_cc_parameters import NAME_END_OFFSET
from mcg_cc_parameters import UID_START_OFFSET
from mcg_cc_parameters import UID_END_OFFSET


# Class:
# Reader()
#
# Description:
# This is base class responsible for reading of .exml file content.
class Reader(object):

    # Method:
    # get_name()
    #
    # Description:
    # This method looks for <name> element within line of .exml file, an example of .exml file line:
    # <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
    #
    # Returns:
    # This method returns <name> element.
    @staticmethod
    def get_name(line, line_number):

        # find position of name within the line
        name_position = line.find("name")
        # find position of mc within the line
        mc_position = line.find("mc")

        # check if <name> and <mc> position is found
        if (name_position == -1) or (mc_position == -1):
            # record error
            mcg_cc_error_handler.record_error(271, line_number, "none")
            # set error name
            name = "NAME_NOT_FOUND"
        else:
            # get name
            name = line[name_position + NAME_START_OFFSET:mc_position + NAME_END_OFFSET]

        # return name
        return name

    # Method:
    # get_uid()
    #
    # Description:
    # This method looks for <uid> element within line of .exml file, an example of .exml file line:
    # <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
    #
    # Returns:
    # This method returns <uid> element.
    @staticmethod
    def get_uid(line, line_number):

        # find position of uid within the line
        uid_position = line.find("uid")

        # check if <uid> position is found
        if uid_position == -1:
            # record error
            mcg_cc_error_handler.record_error(272, line_number, "none")
            # set error uid
            uid = "UID_NOT_FOUND"
        else:
            # get uid
            uid = line[uid_position + UID_START_OFFSET:len(line) + UID_END_OFFSET]

        # return uid
        return uid
