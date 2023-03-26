#   FILE:           mcg_cc_supporter.py
#
#   DESCRIPTION:
#       This module contains definition of Supporter class, which provides additional
#       supporting methods and parameters reused by other classes.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           29 NOV 2022
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


from mcg_cc_error_handler import ErrorHandler


# Description:
# This class provides additional methods and parameters reused by other classes.
class Supporter(object):

    # This parameter defines offset of signal or structure name after "$TARGET$" marker in merged node,
    # i.e. number of characters after occurrence of "$TARGET$" marker, where beginning of signal or
    # structure name occurs, an example:
    # eng_gain1 $TARGET$ eng_gain2 $TARGET$ ADD a084fca5-1c0a-4dfd-881b-21c3f83284e7 $TARGET$ eng_gain_total
    TARGET_OFFSET = 9

    # This parameter defines offset of signal name after "$FIRST$" marker in merged node or line of .exml file,
    # i.e. number of characters after occurrence of "$FIRST$" marker, where beginning of signal name occurs, an example:
    # $FIRST$ some_signal
    FIRST_INPUT_SIGNAL_OFFSET = 8

    # This parameter defines offset of action or component uid before end of action or component definition,
    # i.e. number of characters before occurrence of action or component definition end, where beginning of action
    # or component uid occurs, plus one additional character to accommodate space between action type or component
    # name and uid, an example:
    # ADD fd5be3ed-0d38-42d0-ab56-d1058657eee8
    UID_OFFSET = -37

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
        name = line[name_position + Supporter.NAME_START_OFFSET:mc_position + Supporter.NAME_END_OFFSET]

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
        uid = line[uid_position + Supporter.UID_START_OFFSET:len(line) + Supporter.UID_END_OFFSET]

        # return uid
        return uid
