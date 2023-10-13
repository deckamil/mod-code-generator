#   FILE:           mcg_cc_activity_clause.py
#
#   DESCRIPTION:
#       This module contains definition of ActivityClause class, which represents clause
#       of conditional element on activity diagram.
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
# This class represents clause of conditional element on activity diagram.
class ActivityClause(object):

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        self.start_index = 0
        self.end_index = 0
        self.decision = "UNKNOWN"
        self.uid = "UNKNOWN"
        self.connection_list = []

    # Description:
    # This method returns string representation of ActivityClause class.
    def __str__(self):

        # append clause decision and uid
        line = "$CLAUSE$: " + self.decision + " " + self.uid

        # return string representation
        return line
