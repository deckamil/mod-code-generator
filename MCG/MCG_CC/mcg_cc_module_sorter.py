#   FILE:           mcg_cc_module_sorter.py
#
#   DESCRIPTION:
#       This module contains definition of ModuleSorter class, which is responsible
#       for finding and sorting of module nodes.
#
#   COPYRIGHT:      Copyright (C) 2021-2023 Kamil Deć github.com/deckamil
#   DATE:           25 DEC 2023
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


from mcg_cc_activity_connection import ActivityConnection
from mcg_cc_activity_node import ActivityNode
from mcg_cc_file_reader import FileReader
from mcg_cc_logger import Logger


# Description:
# This class allows to find and sort module nodes.
class ModuleSorter(object):

    # indexes of sorter list
    SORTED_NODE_LIST_INDEX = 0

    # list of action interaction that require to distinguish main data input
    input_sensitive_action_list = ["SUB", "DIV", "BLS", "BRS", "GT", "LT", "GE", "LE"]

    # Description:
    # This is class constructor.
    def __init__(self, file_reader_list):

        # initialize object data
        self.diagram_collection = file_reader_list[FileReader.DIAGRAM_COLLECTION_INDEX]
        self.condition_collection_list = file_reader_list[FileReader.CONDITION_COLLECTION_LIST_INDEX]
        self.local_interface_list = file_reader_list[FileReader.LOCAL_INTERFACE_LIST_INDEX]
        self.sorted_node_list = []

    # Description:
    # This method looks for list of activity interactions.
    def find_interactions(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for diagram interactions", False)

        # search for node interactions under diagram collection
        self.find_interactions_from_collection(self.diagram_collection)

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for clause interactions", False)

        # search for node interactions under clause collection
        for condition_collection in self.condition_collection_list:
            Logger.save_in_log_file("ModuleSorter", "Looking under " + str(condition_collection) + " element", False)
            for clause_collection in condition_collection.collection_list:
                Logger.save_in_log_file("ModuleSorter", "Looking under " + str(clause_collection) + " element", False)
                self.find_interactions_from_collection(clause_collection)

    # Description:
    # This method looks for interactions from given collection.
    @staticmethod
    def find_interactions_from_collection(collection):

        # search for node interaction
        for connection in collection.collection_list:

            # if action or operation is connection source
            if connection.source_type == ActivityConnection.ACTION or \
                    connection.source_type == ActivityConnection.OPERATION:

                # if new integration is found in connection
                if connection.source_uid not in collection.interaction_uid_list:
                    # append interaction uid to interaction uid list
                    collection.interaction_uid_list.append(connection.source_uid)

            # if action or operation is connection target
            if connection.target_type == ActivityConnection.ACTION or \
                    connection.target_type == ActivityConnection.OPERATION:

                # if new integration is found in connection
                if connection.target_uid not in collection.interaction_uid_list:
                    # append interaction uid to interaction uid list
                    collection.interaction_uid_list.append(connection.target_uid)

        # record info
        for interaction_uid in collection.interaction_uid_list:
            Logger.save_in_log_file("ModuleSorter", "Have found " + str(interaction_uid) + " interaction uid", False)

    # Description:
    # This method looks for list of activity nodes.
    def find_nodes(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for diagram nodes", False)

        # search for nodes under diagram collection
        self.find_nodes_from_collection(self.diagram_collection)

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for clause nodes", False)

        # search for nodes under clause collection
        for condition_collection in self.condition_collection_list:
            Logger.save_in_log_file("ModuleSorter", "Looking under " + str(condition_collection) + " element", False)
            for clause_collection in condition_collection.collection_list:
                Logger.save_in_log_file("ModuleSorter", "Looking under " + str(clause_collection) + " element", False)
                self.find_nodes_from_collection(clause_collection)

    # Description:
    # This method looks for nodes from given collection.
    @staticmethod
    def find_nodes_from_collection(collection):

        # search for nodes with interaction, i.e. nodes that represent either action or operation
        for interaction_uid in collection.interaction_uid_list:

            # new node instance
            node = ActivityNode()

            # check source and target uid of each connection
            for connection in collection.collection_list:

                # if interaction is connection target then
                # connection source is node input data
                if interaction_uid == connection.target_uid:
                    # get input data and pin name
                    input_data_name = connection.source_name
                    input_pin_name = connection.target_pin
                    # set input link and append it to node input data list
                    input_link = [input_data_name, input_pin_name]
                    node.input_data_list.append(input_link)
                    # set node name and uid
                    node.name = connection.target_name
                    node.uid = connection.target_uid

                    # if action is connection target
                    if connection.target_type == ActivityConnection.ACTION:
                        # set node type
                        node.type = ActivityNode.ACTION
                    # if operation is connection target
                    elif connection.target_type == ActivityConnection.OPERATION:
                        # set node type
                        node.type = ActivityNode.OPERATION

                # if interaction is connection source then
                # connection target is node output data
                if interaction_uid == connection.source_uid:
                    # get output data and pin name
                    output_data_name = connection.target_name
                    output_pin_name = connection.source_pin
                    # set output link and append it to node output data list
                    output_link = [output_data_name, output_pin_name]
                    node.output_data_list.append(output_link)

            # append node to node list
            collection.node_list.append(node)

        # search for nodes without interaction, i.e. nodes that represent connection between two data points
        for connection in collection.collection_list:

            # if connection is between two data points
            if (connection.source_type == ActivityConnection.LOCAL or
                connection.source_type == ActivityConnection.PARAMETER) and \
                    (connection.target_type == ActivityConnection.LOCAL or
                     connection.target_type == ActivityConnection.PARAMETER):
                # new node instance
                node = ActivityNode()

                # get input data and pin name
                input_data_name = connection.source_name
                input_pin_name = connection.target_pin
                # set input link and append it to node input data list
                input_link = [input_data_name, input_pin_name]
                node.input_data_list.append(input_link)
                # set node type
                node.type = ActivityNode.DATA
                # get output data and pin name
                output_data_name = connection.target_name
                output_pin_name = connection.source_pin
                # set output link and append it to node output data list
                output_link = [output_data_name, output_pin_name]
                node.output_data_list.append(output_link)

                # append node to node list
                collection.node_list.append(node)

        # record info
        for node in collection.node_list:
            Logger.save_in_log_file("ModuleSorter", "Have found " + str(node) + " node", False)

    # Description:
    # This method looks for dependencies between nodes, i.e. list of local data elements, which are inputs to node
    # interaction and are required to compute node output.
    def find_dependencies(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for dependencies between diagram nodes", False)

        # search for node dependencies under diagram collection
        self.find_dependencies_from_collection(self.diagram_collection)

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for dependencies between clause nodes", False)

        # search for node dependencies under clause collection
        for condition_collection in self.condition_collection_list:
            Logger.save_in_log_file("ModuleSorter", "Looking under " + str(condition_collection) + " element", False)
            for clause_collection in condition_collection.collection_list:
                Logger.save_in_log_file("ModuleSorter", "Looking under " + str(clause_collection) + " element", False)
                self.find_dependencies_from_collection(clause_collection)

    # Description:
    # This method looks for dependencies from given collection.
    def find_dependencies_from_collection(self, collection):

        # search for node dependencies
        for node in collection.node_list:
            # go through all local data elements for each node
            for local_interface in self.local_interface_list:
                # get local data name
                local_data_name = local_interface[FileReader.DATA_ELEMENT_NAME_INDEX]
                # go through all input links
                for input_link in node.input_data_list:
                    # if local data element is input to node
                    if local_data_name == input_link[ActivityNode.DATA_NAME_INDEX]:
                        # append name of local data element to dependency list
                        node.dependency_list.append(local_data_name)
                        # record info
                        Logger.save_in_log_file("ModuleSorter", "Have found dependency on " +
                                                str(node.dependency_list) + " in " +
                                                str(node) + " node", False)

    # Description:
    # This method sorts clauses of each condition element.
    def sort_clauses(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Sorting clauses of each condition element", False)

        # for each condition collection
        for condition_collection in self.condition_collection_list:
            # record info
            Logger.save_in_log_file("ModuleSorter", "Sorting under " + str(condition_collection) + " element", False)
            # set initial clause level number
            clause_level_number = 0
            # flag to distinguish if given clause level is found
            clause_level_found = True

            # repeat while clause level for given number is found
            while clause_level_found:
                # increment clause level number
                clause_level_number = clause_level_number + 1
                # get string format
                clause_level_str = "[" + str(clause_level_number) + "] "
                # assume that given clause level is not found
                clause_level_found = False

                # for each clause collection
                for clause_collection in list(condition_collection.collection_list):
                    # if matching clause level is found in clause decision
                    if clause_collection.decision.find(clause_level_str) != -1:
                        # remove clause from collection list
                        condition_collection.collection_list.remove(clause_collection)
                        # insert clause at position defined by clause level number
                        condition_collection.collection_list.insert(clause_level_number-1, clause_collection)
                        # set clause flag state
                        clause_level_found = True

            # record info
            for clause_collection in condition_collection.collection_list:
                Logger.save_in_log_file("ModuleSorter", "Have sorted " + str(clause_collection) + " element", False)

    # Description:
    # This method defines and adds nodes that represent condition elements to diagram node list.
    def add_condition_nodes(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Adding condition nodes", False)

        # for each condition collection
        for condition_collection in self.condition_collection_list:
            # record info
            Logger.save_in_log_file("ModuleSorter", "Adding node for " + str(condition_collection) + " element", False)

            # new node instance
            node = ActivityNode()

            # set node name, uid and type
            node.name = condition_collection.name
            node.uid = condition_collection.uid
            node.type = ActivityNode.CONDITION

            # list to collect condition output data
            condition_target_list = []

            # for each clause collection
            for clause_collection in condition_collection.collection_list:
                # record info
                Logger.save_in_log_file("ModuleSorter", "Checking " + str(clause_collection) + " element for"
                                        "input and output data", False)

                # for each node in clause
                for clause_node in clause_collection.node_list:
                    # go through all output links
                    for output_link in clause_node.output_data_list:
                        # and add each data name to condition target list
                        condition_target_list.append(output_link[ActivityNode.DATA_NAME_INDEX])

            # remove duplicates from target list
            condition_target_list = list(dict.fromkeys(condition_target_list))

            # add output links from condition target list
            for condition_target in condition_target_list:
                # set output data and pin name
                output_data_name = condition_target
                output_pin_name = "NOT APPLICABLE"
                # set output link and append it to node output data list
                output_link = [output_data_name, output_pin_name]
                node.output_data_list.append(output_link)

            # record info
            Logger.save_in_log_file("ModuleSorter", "Have added " + str(node) + " node", False)

            # append node to diagram node list
            self.diagram_collection.node_list.append(node)

    # Description:
    # This method sorts nodes basing on their dependencies from sublist under dependency list.
    def sort_nodes(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Sorting module nodes basing on their dependencies", False)

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
                    # get output data list
                    output_data_list = dependency[0].output_data_list
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
                                for output_link in output_data_list:
                                    if output_link[ActivityNode.DATA_NAME_INDEX] == dependency[index]:
                                        # remove local data element from dependency sublist
                                        dependency.remove(dependency[index])
                                        # decrement index for next iteration, as one dependence was removed
                                        # therefore all next dependencies in dependency sublist were pushed by
                                        # one position towards beginning of the sublist, e.g. [...,A,B,C] -> [...,B,C];
                                        # A was removed and now B is under previous position of A so at next
                                        # iteration the same index need to be checked to examine B;
                                        index = index - 1
                                        # exit "for output_link in" loop
                                        break
                                index = index + 1

                    # exit "for i in range" loop
                    break

        # record info
        for sorted_node in self.sorted_node_list:
            Logger.save_in_log_file("ModuleSorter", "Have sorted " + str(sorted_node) + " node", False)

    # Description:
    # This method sorts input data elements if interaction requires to point main data input.
    def sort_input_data_list(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Sorting nodes input data list", False)

        # some kind of actions require to distinguish which input data element should be
        # considered as main data element in order to compute correct results;

        # please consider as example a subtraction between two data elements: temp1 and temp2;
        # the temp1-temp2 gives different result than temp2-temp1, therefore in such case there
        # is a need to define order by pointing which input data element, temp1 or temp2, should
        # be considered as main, i.e. the one which needs to appear at beginning of interaction

        # the main data element in pointed by + marker in node name;
        # input data element with same name as pointed main data element by + marker should be
        # moved at beginning of input data list

        # repeat for all nodes from sorted node list
        for sorted_node in self.sorted_node_list:

            # if node is action type
            if sorted_node.type == ActivityNode.ACTION:

                # and if action is input sensitive, i.e. requires to distinguish main input data
                for input_sensitive_action in ModuleSorter.input_sensitive_action_list:
                    if (sorted_node.name[0:3] == input_sensitive_action) or \
                            (sorted_node.name[0:2] == input_sensitive_action):

                        # get marker position
                        marker_position = sorted_node.name.find("+")
                        # get main input data name
                        main_input_data_name = sorted_node.name[marker_position+1:len(sorted_node.name)]

                        # check each input link
                        for input_link in sorted_node.input_data_list:

                            # if input link contains main input data
                            if input_link[ActivityNode.DATA_NAME_INDEX] == main_input_data_name:

                                # get input link index
                                input_link_index = sorted_node.input_data_list.index(input_link)
                                # remove main input link from current position
                                main_input_link = sorted_node.input_data_list.pop(input_link_index)
                                # insert main input link at beginning of input data list
                                sorted_node.input_data_list.insert(0, main_input_link)

                                # record info
                                Logger.save_in_log_file("ModuleSorter", "Have sorted " + str(sorted_node) + " node",
                                                        False)
                                # exit "for input_link in" loop
                                break

    # Description:
    # This method is responsible for finding and sorting of module nodes.
    def sort_module(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Sorting module details from set of .exml files", True)

        # find activity interactions, nodes and dependencies
        self.find_interactions()
        self.find_nodes()
        self.find_dependencies()

        # sort clauses, add condition nodes and find condition dependencies
        self.sort_clauses()
        self.add_condition_nodes()
        # self.find_condition_dependencies()

        # sort nodes basing on their dependencies
        # self.sort_nodes()

        # sort input data list
        # self.sort_input_data_list()

        # append collected data to module sorter list
        module_sorter_list = []
        module_sorter_list.insert(ModuleSorter.SORTED_NODE_LIST_INDEX, self.sorted_node_list)

        # return module sorter list
        return module_sorter_list
