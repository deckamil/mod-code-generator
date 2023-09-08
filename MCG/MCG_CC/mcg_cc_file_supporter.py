#   FILE:           mcg_cc_file_supporter.py
#
#   DESCRIPTION:
#       This module contains definition of FileSupporter class, which provides additional
#       supporting methods and parameters reused by other classes.
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
# This class provides additional methods and parameters reused by other classes.
class FileSupporter(object):

    # This parameter defines start offset of name element after "name" marker in line of .exml file, i.e.
    # number of characters after occurrence of "name" marker, where beginning of name element occurs, an example:
    # <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
    NAME_START_OFFSET = 6

    # This parameter defines end offset of name element before "mc" marker in line of .exml file, i.e.
    # number of characters before occurrence of "mc" marker, where end of name element occurs, an example:
    # <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
    NAME_END_OFFSET = -2

    # This parameter defines start offset of uid element after "uid" marker in line of .exml file, i.e.
    # number of characters after occurrence of "uid" marker, where beginning of uid element occurs, an example:
    # <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
    UID_START_OFFSET = 5

    # This parameter defines end offset of uid element before end of .exml file line, i.e.
    # number of characters before occurrence of .exml file line end, where end of uid element occurs, an example:
    # <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
    UID_END_OFFSET = -3

    # Description:
    # This method looks for <name> element within line of .exml file, an example of .exml file line:
    # <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
    @staticmethod
    def get_name(line):

        # find position of name within the line
        name_position = line.find("name")
        # find position of mc within the line
        mc_position = line.find("mc")

        # get name
        name = line[name_position + FileSupporter.NAME_START_OFFSET:mc_position + FileSupporter.NAME_END_OFFSET]

        # return name
        return name

    # Description:
    # This method looks for <uid> element within line of .exml file, an example of .exml file line:
    # <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
    @staticmethod
    def get_uid(line):

        # find position of uid within the line
        uid_position = line.find("uid")

        # get uid
        uid = line[uid_position + FileSupporter.UID_START_OFFSET:len(line) + FileSupporter.UID_END_OFFSET]

        # return uid
        return uid
