#   FILE:           mcg_cc_activity_layer.py
#
#   DESCRIPTION:
#       TThis module contains definition of classes, which collect data and artefacts
#       from different layers of activity diagram.
#
#   COPYRIGHT:      Copyright (C) 2021-2024 Kamil Deć github.com/deckamil
#   DATE:           3 FEB 2024
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
# This class collects data and artefacts that belongs directly to layer of activity diagram.
class ActivityDiagramLayer(object):

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        self.connection_list = []
        self.interaction_uid_list = []
        self.node_list = []
        self.sorted_node_list = []

    # Description:
    # This method returns string representation of the class.
    def __str__(self):
        line = "$DIAGRAM$"
        return line


# Description:
# This class collects data and artefacts that belongs to layer of condition element on activity diagram.
class ActivityConditionLayer(object):

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        self.name = "UNKNOWN"
        self.uid = "UNKNOWN"
        self.clause_layer_list = []

    # Description:
    # This method returns string representation of the class.
    def __str__(self):
        line = "$CONDITION$: " + self.name + " " + self.uid
        return line


# Description:
# This class collects data and artefacts that belongs to layer of clause element on activity diagram.
class ActivityClauseLayer(object):

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        self.decision = "UNKNOWN"
        self.uid = "UNKNOWN"
        self.start_index = 0
        self.end_index = 0
        self.connection_list = []
        self.interaction_uid_list = []
        self.node_list = []
        self.sorted_node_list = []

    # Description:
    # This method returns string representation of the class.
    def __str__(self):
        line = "$CLAUSE$: " + self.decision + " " + self.uid
        return line
