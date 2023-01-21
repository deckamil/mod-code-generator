#   FILE:           mcg_cc_module_sorter.py
#
#   DESCRIPTION:
#       This module contains definition of ModuleSorter class, which is responsible
#       for finding and sorting of module nodes.
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


from mcg_cc_file_reader import FileReader
from mcg_cc_logger import Logger
from mcg_cc_node import Node


# Description:
# This class allows to find and sort module nodes.
class ModuleSorter(object):

    # indexes of sorter list
    SORTED_NODE_LIST_INDEX = 0

    # Description:
    # This is class constructor.
    def __init__(self, file_reader_list):

        # initialize object data
        self.connection_list = file_reader_list[FileReader.CONNECTION_LIST_INDEX]
        self.local_interface_list = file_reader_list[FileReader.LOCAL_INTERFACE_LIST_INDEX]
        self.node_list = []
        self.dependency_list = []
        self.sorted_node_list = []

    # Description:
    # This method sorts connections with same interaction in one place within connection list.
    def sort_connections(self):

        # record info
        Logger.save_in_log_file("Sorter", "Sorting module connections", True)

        # this index tells where to put connection (defines new position of connection)
        index = 0

        # repeat for each interaction recorded on interaction list
        # sort connections of given interaction in one place within connection list
        # first, connections with inputs to interaction are sorted (interaction is connection target),
        # then, connection with output from interaction is placed after them (interaction is connection source)
        for i in range(0, len(self.interaction_list)):
            # go through all connections for each interaction on interaction list
            for connection in self.connection_list:
                # if interaction is connection target
                if connection.connection_target == self.interaction_list[i]:
                    # remove connection from current position on the list
                    self.connection_list.remove(connection)
                    # insert connection under new position defined by index
                    self.connection_list.insert(index, connection)
                    # increment index to put next connection right after this connection
                    index = index + 1
            # go through all connections for each interaction on interaction list
            for connection in self.connection_list:
                # if interaction is connection source
                if connection.connection_source == self.interaction_list[i]:
                    # remove connection from current position on the list
                    self.connection_list.remove(connection)
                    # insert connection under new position defined by index
                    self.connection_list.insert(index, connection)
                    # increment index to put next connection right after this connection
                    index = index + 1

        # place connections with no target (connection target is $EMPTY$") at the end of connection list
        for i in range(index, len(self.connection_list)):
            # if data does not have any target
            if self.connection_list[index].connection_target == "$EMPTY$":
                # copy connection from given index
                connection = self.connection_list[index]
                # remove connection
                self.connection_list.remove(connection)
                # insert connection at the end of list
                self.connection_list.insert(len(self.connection_list), connection)
                # decrement index for next iteration, as inserted connection pushes by one position
                # from right to left other connections, e.g. [...,...,...,A,B,C] -> [...,...,...,B,C,A];
                # A was placed at the end and now B is under previous position of A,
                # so at next iteration the same index need to be checked to examine B
                index = index - 1
            index = index + 1

        # record info
        for connection in self.connection_list:
            Logger.save_in_log_file("Sorter", "Have sorted " + str(connection) + " connection", False)

    # Description:
    # This method gathers details of connections from activity diagram and base on them create nodes, where each
    # node describes inputs and output from one unique interaction.
    def find_nodes(self):

        # record info
        Logger.save_in_log_file("Sorter", "Looking for module nodes", False)

        # find node details for each interaction
        for interaction in self.interaction_list:
            # new node instance
            node = Node()
            # set node interaction
            node.node_interaction = interaction

            # go through all connections for each interaction on interaction list
            for connection in self.connection_list:

                # if interaction is connection target, then connection source is note input
                if connection.connection_target == interaction:
                    # get node input
                    node_input = connection.connection_source
                    # append node input
                    node.node_input_list.append(node_input)

                # if interaction is connection source, then connection target is node output
                elif connection.connection_source == interaction:
                    # get node output
                    node_output = connection.connection_target
                    # set node output
                    node.node_output = node_output

            # append node to node list
            self.node_list.append(node)

        # find node details for connections with data assignment, i.e. without interaction or $EMPTY$ marker
        for connection in self.connection_list:

            # interaction marker show whether interaction was found or not within connection
            interaction_found = False

            # check if connection contains interaction
            for interaction in self.interaction_list:
                # if interaction is found within connection
                if (connection.connection_source == interaction) or (connection.connection_target == interaction):
                    # change interaction marker
                    interaction_found = True
                    # exit loop
                    break

            # if any interaction was not found within connection and connection does not contain "$EMPTY$" target
            if (not interaction_found) and (connection.connection_target != "$EMPTY$"):
                # new node instance
                node = Node()
                # get node input
                node_input = connection.connection_source
                # get node output
                node_output = connection.connection_target
                # append node input
                node.node_input_list.append(node_input)
                # set node interaction
                node.node_interaction = "ASSIGNMENT"
                # set node output
                node.node_output = node_output
                # append node to node list
                self.node_list.append(node)

        # record info
        for node in self.node_list:
            Logger.save_in_log_file("Sorter", "Have found " + str(node) + " node", False)

    # Description:
    # This method finds dependencies of each node, i.e. list of local data elements, which are inputs to node
    # interaction and are required to compute node output.
    def find_dependencies(self):

        # record info
        Logger.save_in_log_file("Sorter", "Looking for dependencies between module nodes", False)

        # each node will have dedicated sublist under dependency list
        # the sublist starts with node itself under position 0 and local data elements, which are inputs to that
        # node are appended under further positions of the sublist;
        # as result, length of sublist express number of local data elements needed to compute node output;
        # in special case, if some node does not need any local data element (e.g. only input interface elements
        # are required to compute the node output) the length of sublist is equal to 1

        # find dependencies of each nodes
        for node in self.node_list:
            # dependency sublist with node at list beginning
            dependency = [node]
            # go through all local data elements for each node
            for local_data in self.local_data_list:
                # get name of local data element
                local_data_name = local_data[FileReader.INTERFACE_ELEMENT_NAME_INDEX]
                # go through all node inputs
                for node_input in node.node_input_list:
                    # if local data element is input to node
                    if local_data_name == node_input:
                        # append name of local data element to dependency sublist
                        dependency.append(local_data_name)

            # append dependency to dependency list
            self.dependency_list.append(dependency)

        # record info
        for dependency in self.dependency_list:
            Logger.save_in_log_file("Sorter", "Have found dependency on " + str(dependency[1:len(dependency)]) + " in "
                                    + str(dependency[0]) + " node", False)

    # Description:
    # This method sorts nodes basing on their dependencies from sublist under dependency list.
    def sort_nodes(self):

        # record info
        Logger.save_in_log_file("Sorter", "Sorting module nodes", False)

        # sort nodes basing on their dependencies
        # first append nodes without dependencies to sorted node list, i.e. look for each sublist on dependency
        # list with length equal to 1, which means that given sublist contains node that does not consume any
        # local data elements (or consume local data elements outputted by node, which was already appended to
        # sorted node list at previous cycle);
        # then remove local data element outputted by above node from each sublist under dependency list, which
        # will lead to situation where some of sublist will have new length equal to 1;
        # next repeat the cycle until all nodes are sorted

        # number of nodes to sort, i.e. length of dependency list
        dependency_list_length = len(self.dependency_list)
        # repeat until all nodes are sorted
        while dependency_list_length > 0:
            # go thorough each dependency sublist
            for i in range(0, len(self.dependency_list)):
                # if given node under dependency sublist does not have any further dependencies
                if len(self.dependency_list[i]) == 1:
                    # get dependency sublist
                    dependency = self.dependency_list[i]
                    # append node to sorted node list
                    self.sorted_node_list.append(dependency[0])
                    # remove dependency sublist from dependency list
                    self.dependency_list.remove(dependency)
                    # find node output
                    node_output = dependency[0].node_output
                    # recalculate number of nodes to sort, i.e. length of dependency list
                    dependency_list_length = len(self.dependency_list)

                    # refresh each dependency sublist
                    for j in range(0, len(self.dependency_list)):
                        # if given node under dependency sublist DOES HAVE further dependencies
                        if len(self.dependency_list[j]) > 1:
                            # get dependency sublist
                            dependency = self.dependency_list[j]
                            # set initial index
                            index = 1
                            # chek local data elements under dependency sublist
                            for k in range(index, len(dependency)):
                                # if given node consumes local data elements, which comes from node, which
                                # was appended above to sorted node list
                                if node_output == dependency[index]:
                                    # remove local data element from dependency sublist
                                    dependency.remove(dependency[index])
                                    # decrement index for next iteration, as one dependence was removed
                                    # therefore all next dependencies in dependency sublist were pushed by
                                    # one position towards beginning of the sublist, e.g. [...,A,B,C] -> [...,B,C];
                                    # A was removed and now B is under previous position of A so at next
                                    # iteration the same index need to be checked to examine B;
                                    index = index - 1
                                index = index + 1

                    # exit "for i in range" loop
                    break

        # record info
        for sorted_node in self.sorted_node_list:
            Logger.save_in_log_file("Sorter", "Have sorted " + str(sorted_node) + " node", False)

    # Description:
    # This method moves first input signal, recognized by $FIRST$ marker, at beginning of node input list
    # and removes $FIRST$ marker.
    def sort_first_input_signals(self):

        # record info
        Logger.save_in_log_file("Sorter", "Sorting first input signal in nodes", False)

        # for each node check if it contains first input signal
        for node in self.node_list:

            # go through all node inputs of node
            for node_input in node.node_input_list:

                # if given node input contains $FIRST$ marker
                if "$FIRST$" in node_input:

                    # find marker position
                    first_position = node_input.find("$FIRST$")
                    # get first input signal
                    first_input_signal = node_input[first_position + Supporter.FIRST_INPUT_SIGNAL_OFFSET:
                                                    len(node_input)]
                    # remove node input from the list
                    node.node_input_list.remove(node_input)
                    # append first input signal at beginning of node input list
                    node.node_input_list = [first_input_signal] + node.node_input_list

        # record info
        for node in self.node_list:
            Logger.save_in_log_file("Sorter", "Have sorted " + str(node) + " node", False)

    # Description:
    # This method is responsible for finding and sorting of module nodes.
    def sort_module(self):

        # sort connections of same action into one place on connections list
        # self.sort_connections()
        TBD = ""

        # find nodes base on connections and interactions
        # self.find_nodes()

        # sort first input signals within nodes
        # self.sort_first_input_signals()

        # find dependencies between nodes
        # self.find_dependencies()

        # sort nodes basing on their dependencies
        # self.sort_nodes()

        # append collected data to component sorter list
        # component_sorter_list = []
        # component_sorter_list.insert(Sorter.SORTED_NODE_LIST_INDEX, self.sorted_node_list)

        # return component sorter list
        # return component_sorter_list
