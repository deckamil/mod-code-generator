#   FILE:           mcg_cc_activity_connection.py
#
#   DESCRIPTION:
#       This module contains definition of ActivityConnection class, which represents connection
#       between two model elements on activity diagram.
#
#   COPYRIGHT:      Copyright (C) 2021-2023 Kamil Deć github.com/deckamil
#   DATE:           13 OCT 2023
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
# This class represents connection between two model elements on activity diagram.
class ActivityConnection(object):

    # Connections types
    UNKNOWN = 10
    PARAMETER = 20
    LOCAL = 30
    ACTION = 40
    OPERATION = 50

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        self.index = 0
        self.source_pin = "UNKNOWN"
        self.source_name = "UNKNOWN"
        self.source_uid = "UNKNOWN"
        self.source_type = ActivityConnection.UNKNOWN
        self.target_pin = "UNKNOWN"
        self.target_name = "UNKNOWN"
        self.target_uid = "UNKNOWN"
        self.target_type = ActivityConnection.UNKNOWN

    # Description:
    # This method returns string representation of ActivityConnection class.
    def __str__(self):

        # source
        line = "$SOURCE$: "

        # if operation is source
        if self.source_type == ActivityConnection.OPERATION:
            line = line + self.source_pin + " " + self.source_name + "() " + self.source_uid + " "
        # if action is source
        elif self.source_type == ActivityConnection.ACTION:
            line = line + self.source_name + " " + self.source_uid + " "
        # if local data or other parameter is source
        else:
            line = line + self.source_name + " "

        # target
        line = line + "$TARGET$: "

        # if operation is target
        if self.target_type == ActivityConnection.OPERATION:
            line = line + self.target_pin + " " + self.target_name + "() " + self.target_uid
        # if action is target
        elif self.target_type == ActivityConnection.ACTION:
            line = line + self.target_name + " " + self.target_uid
        # if local data or other parameter is target
        else:
            line = line + self.target_name

        # return string representation
        return line
