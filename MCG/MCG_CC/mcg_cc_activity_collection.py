#   FILE:           mcg_cc_activity_collection.py
#
#   DESCRIPTION:
#       TThis module contains definition of ActivityBasicCollection class
#       and its child classes, which represent collections of related elements
#       on activity diagram.
#
#   COPYRIGHT:      Copyright (C) 2021-2023 Kamil Deć github.com/deckamil
#   DATE:           6 DEC 2023
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
# This class represents basic collection type of related elements on activity diagram.
class ActivityBasicCollection(object):

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        self.collection_list = []

    # Description:
    # This method returns string representation of the class.
    def __str__(self):
        line = "$UNKNOWN BASIC COLLECTION$"
        return line


# Description:
# This class represents collection of diagram elements, that do not belong to any other specific collection type.
# The collection list is used to store list of connection that do not belong to any other collection type.
class ActivityDiagramCollection(ActivityBasicCollection):

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        super().__init__()
        self.interaction_uid_list = []

    # Description:
    # This method returns string representation of the class.
    def __str__(self):
        line = "$DIAGRAM COLLECTION$"
        return line


# Description:
# This class represents collection of condition elements on activity diagram.
# The collection list is used to store list of clauses that belong to condition element.
class ActivityConditionCollection(ActivityBasicCollection):

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        super().__init__()
        self.name = "UNKNOWN"
        self.uid = "UNKNOWN"

    # Description:
    # This method returns string representation of the class.
    def __str__(self):
        line = "$CONDITION COLLECTION$: " + self.name + " " + self.uid
        return line


# Description:
# This class represents collection of clause elements on activity diagram.
# The collection list is used to store list of connections that belong to clause.
class ActivityClauseCollection(ActivityConditionCollection):

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        super().__init__()
        self.start_index = 0
        self.end_index = 0
        self.decision = "UNKNOWN"
        self.interaction_uid_list = []

    # Description:
    # This method returns string representation of the class.
    def __str__(self):
        line = "$CLAUSE COLLECTION$: " + self.decision + " " + self.uid
        return line
