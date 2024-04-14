#   FILE:           mcg_cc_module_sorter.py
#
#   DESCRIPTION:
#       This module contains definition of ModuleSorter class, which is responsible
#       for finding and sorting of module nodes.
#
#   COPYRIGHT:      Copyright (C) 2021-2024 Kamil Deć github.com/deckamil
#   DATE:           5 FEB 2024
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

    # list of action interaction that require to distinguish main data input
    input_sensitive_action_list = ["SUB", "DIV", "BLS", "BRS", "GT", "LT", "GE", "LE"]

    # Description:
    # This is class constructor.
    def __init__(self, file_reader_list):

        # initialize object data
        self.diagram_layer = file_reader_list[FileReader.DIAGRAM_LAYER_INDEX]
        self.condition_layer_list = file_reader_list[FileReader.CONDITION_LAYER_LIST_INDEX]
        self.local_interface_list = file_reader_list[FileReader.LOCAL_INTERFACE_LIST_INDEX]

    # Description:
    # This method looks for list of activity interactions.
    def find_interactions(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for diagram layer interactions", False)

        # search for node interactions under diagram layer
        ModuleSorter.find_interactions_from_layer(self.diagram_layer)

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for clause layer interactions", False)

        # search for node interactions under clause layer
        for condition_layer in self.condition_layer_list:
            Logger.save_in_log_file("ModuleSorter", "Looking under " + str(condition_layer) + " layer", False)
            for clause_layer in condition_layer.clause_layer_list:
                Logger.save_in_log_file("ModuleSorter", "Looking under " + str(clause_layer) + " layer", False)
                ModuleSorter.find_interactions_from_layer(clause_layer)

    # Description:
    # This method looks for interactions from given layer.
    @staticmethod
    def find_interactions_from_layer(layer):

        # search for node interaction
        for connection in layer.connection_list:

            # if action or operation is connection source
            if connection.source_type == ActivityConnection.ACTION or \
                    connection.source_type == ActivityConnection.OPERATION:

                # if new integration is found in connection
                if connection.source_uid not in layer.interaction_uid_list:
                    # append interaction uid to interaction uid list
                    layer.interaction_uid_list.append(connection.source_uid)

            # if action or operation is connection target
            if connection.target_type == ActivityConnection.ACTION or \
                    connection.target_type == ActivityConnection.OPERATION:

                # if new integration is found in connection
                if connection.target_uid not in layer.interaction_uid_list:
                    # append interaction uid to interaction uid list
                    layer.interaction_uid_list.append(connection.target_uid)

        # record info
        for interaction_uid in layer.interaction_uid_list:
            Logger.save_in_log_file("ModuleSorter", "Have found " + str(interaction_uid) + " interaction uid", False)

    # Description:
    # This method looks for list of activity nodes.
    def find_nodes(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for diagram layer nodes", False)

        # search for nodes under diagram layer
        ModuleSorter.find_nodes_from_layer(self.diagram_layer)

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for clause layer nodes", False)

        # search for nodes under clause layer
        for condition_layer in self.condition_layer_list:
            Logger.save_in_log_file("ModuleSorter", "Looking under " + str(condition_layer) + " layer", False)
            for clause_layer in condition_layer.clause_layer_list:
                Logger.save_in_log_file("ModuleSorter", "Looking under " + str(clause_layer) + " layer", False)
                ModuleSorter.find_nodes_from_layer(clause_layer)

    # Description:
    # This method looks for nodes from given layer.
    @staticmethod
    def find_nodes_from_layer(layer):

        # search for nodes with interaction, i.e. nodes that represent either action or operation
        for interaction_uid in layer.interaction_uid_list:

            # new node instance
            node = ActivityNode()

            # check source and target uid of each connection
            for connection in layer.connection_list:

                # if interaction is connection target then
                # connection source is node input data
                if interaction_uid == connection.target_uid:
                    # get input data and pin name
                    input_data_name = connection.source_name
                    input_pin_name = connection.target_pin
                    # set input link and append it to node input data list
                    input_link = [input_data_name, input_pin_name]
                    node.input_data_list.append(input_link)
                    # set node interaction and uid
                    node.interaction = connection.target_name
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
            layer.node_list.append(node)

        # search for nodes without interaction, i.e. nodes that represent connection between two data points
        for connection in layer.connection_list:

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
                layer.node_list.append(node)

        # record info
        for node in layer.node_list:
            Logger.save_in_log_file("ModuleSorter", "Have found " + str(node) + " node", False)

    # Description:
    # This method looks for dependencies between nodes, i.e. list of local data elements, which are inputs to node
    # interaction and are required to compute node output.
    def find_dependencies(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for dependencies of diagram layer nodes", False)

        # search for node dependencies under diagram layer
        self.find_dependencies_from_layer(self.diagram_layer)

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for dependencies of clause layer nodes", False)

        # search for node dependencies under clause layer
        for condition_layer in self.condition_layer_list:
            Logger.save_in_log_file("ModuleSorter", "Looking under " + str(condition_layer) + " layer", False)
            for clause_layer in condition_layer.clause_layer_list:
                Logger.save_in_log_file("ModuleSorter", "Looking under " + str(clause_layer) + " layer", False)
                self.find_dependencies_from_layer(clause_layer)

    # Description:
    # This method looks for dependencies from given layer.
    def find_dependencies_from_layer(self, layer):

        # search for node dependencies
        for node in layer.node_list:
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
    # This method looks for condition nodes that represent condition layer and adds them to diagram node list.
    def find_condition_nodes(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for condition type nodes", False)

        # for each condition layer
        for condition_layer in self.condition_layer_list:

            # new node instance
            node = ActivityNode()

            # set node interaction, uid and type
            node.interaction = condition_layer.name
            node.uid = condition_layer.uid
            node.type = ActivityNode.CONDITION

            # list to collect condition output data
            condition_target_list = []

            # for each clause layer
            for clause_layer in condition_layer.clause_layer_list:
                # for each node in clause
                for clause_node in clause_layer.node_list:
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
            Logger.save_in_log_file("ModuleSorter", "Have found " + str(node) + " node", False)

            # append node to diagram node list
            self.diagram_layer.node_list.append(node)

    # Description:
    # This method looks for condition node dependencies, i.e. list of local data elements, which are inputs to condition
    # node interaction and are required to compute condition node output.
    def find_condition_dependencies(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Looking for dependencies of condition type nodes", False)

        # for each condition layer
        for condition_layer in self.condition_layer_list:
            # temporary list of condition dependencies
            condition_dependency_list = []

            # for each clause layer
            for clause_layer in condition_layer.clause_layer_list:

                # find if node dependency, i.e. local input data element of the node, is generated by any
                # other clause node; if local input data element is not generated by any other clause node
                # then that local data element is local input to entire condition

                # for each node in node list
                for node_under_check in clause_layer.node_list:
                    # for each dependency in dependency list
                    for dependency in list(node_under_check.dependency_list):

                        # flag to distinguish if given dependency is found in output data list of any clause node
                        dependency_in_output_data_found = False

                        for clause_node in clause_layer.node_list:
                            # for each output link in output data list
                            for output_link in clause_node.output_data_list:
                                # if dependency is output from any clause node
                                if dependency == output_link[ActivityNode.DATA_NAME_INDEX]:
                                    # set dependency flag
                                    dependency_in_output_data_found = True
                                    # exit "for output_link in" loop
                                    break

                            # if dependency is found, then exit "for clause_node in" loop
                            if dependency_in_output_data_found:
                                break

                        # if dependency is not found in output data list of any clause node, then add dependency
                        # to condition dependency list
                        if not dependency_in_output_data_found:
                            # move dependency from clause to condition dependency list
                            node_under_check.dependency_list.remove(dependency)
                            condition_dependency_list.append(dependency)

                # find if clause decision contains any dependency on any local data element, if local data
                # element is found in clause decision then it means that it is an additional dependency of
                # entire condition node

                # get clause decision
                clause_decision = clause_layer.decision
                # if this is not "else" clause
                if "[else]" not in clause_decision:
                    # remove clause level number with square bracket
                    clause_level_bracket_position = clause_decision.find("]")
                    clause_decision = clause_decision[clause_level_bracket_position+1:len(clause_decision)]
                    # remove decision round brackets and logical operators
                    clause_decision = clause_decision.replace("(", "")
                    clause_decision = clause_decision.replace(")", "")
                    clause_decision = clause_decision.replace(" AND ", "")
                    clause_decision = clause_decision.replace(" OR ", "")
                    clause_decision = clause_decision.replace(" NOT ", "")
                    clause_decision = clause_decision.replace(" (NOT ", "")
                    clause_decision = clause_decision.replace(" EQ ", "")
                    clause_decision = clause_decision.replace(" NE ", "")
                    clause_decision = clause_decision.replace(" GT ", "")
                    clause_decision = clause_decision.replace(" LT ", "")
                    clause_decision = clause_decision.replace(" GE ", "")
                    clause_decision = clause_decision.replace(" LE ", "")
                    # split decision to get list of data names that appear in clause decision
                    clause_decision_data_name_list = clause_decision.split()

                    # go through all local data elements
                    for local_interface in self.local_interface_list:
                        # get local data name
                        local_data_name = local_interface[FileReader.DATA_ELEMENT_NAME_INDEX]
                        # go trough all clause decision data names
                        for clause_decision_data_name in clause_decision_data_name_list:
                            # if clause decision data name the same as local data name
                            if clause_decision_data_name == local_data_name:
                                # append name of local data element to condition dependency list
                                condition_dependency_list.append(local_data_name)

            # remove duplicates from condition dependency list
            condition_dependency_list = list(dict.fromkeys(condition_dependency_list))

            # find related condition node and add dependencies
            for node in self.diagram_layer.node_list:
                # if it is condition node and its uid match condition layer
                if node.type == ActivityNode.CONDITION and node.uid == condition_layer.uid:
                    # add dependencies to condition node
                    node.dependency_list = condition_dependency_list
                    # record info
                    Logger.save_in_log_file("ModuleSorter", "Have found dependency on " +
                                            str(node.dependency_list) + " in " +
                                            str(node) + " node", False)

    # Description:
    # This method sorts clauses of each condition layer.
    def sort_condition_clauses(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Sorting clauses of each condition layer", False)

        # for each condition layer
        for condition_layer in self.condition_layer_list:
            # record info
            Logger.save_in_log_file("ModuleSorter", "Sorting under " + str(condition_layer) + " layer", False)
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

                # for each clause layer
                for clause_layer in list(condition_layer.clause_layer_list):
                    # if matching clause level is found in clause decision
                    if clause_layer.decision.find(clause_level_str) != -1:
                        # remove clause from clause layer list
                        condition_layer.clause_layer_list.remove(clause_layer)
                        # insert clause at position defined by clause level number
                        condition_layer.clause_layer_list.insert(clause_level_number-1, clause_layer)
                        # set clause flag state
                        clause_level_found = True

            # record info
            for clause_layer in condition_layer.clause_layer_list:
                Logger.save_in_log_file("ModuleSorter", "Have sorted " + str(clause_layer) + " layer", False)

    # Description:
    # This method sorts nodes basing on their dependencies under dependency list.
    def sort_nodes(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Sorting diagram layer nodes basing on their dependencies", False)

        # sort diagram nodes
        ModuleSorter.sort_nodes_under_layer(self.diagram_layer)

        # record info
        Logger.save_in_log_file("ModuleSorter", "Sorting clause layer nodes basing on their dependencies", False)

        # sort clause nodes
        for condition_layer in self.condition_layer_list:
            Logger.save_in_log_file("ModuleSorter", "Sorting under " + str(condition_layer) + " layer", False)
            for clause_layer in condition_layer.clause_layer_list:
                Logger.save_in_log_file("ModuleSorter", "Sorting under " + str(clause_layer) + " layer", False)
                ModuleSorter.sort_nodes_under_layer(clause_layer)

    # Description:
    # This method sorts nodes under given layer.
    @staticmethod
    def sort_nodes_under_layer(layer):

        # sort nodes as long at node list is not empty
        while layer.node_list:

            # sort nodes basing on their dependencies
            # first append nodes without dependencies to sorted node list and remove them from node list
            # then look through outputs from sorted node and remove local data elements outputted by the
            # sorted node from dependency list of other nodes under referenced layer

            # go through all nodes under layer
            for node in list(layer.node_list):
                # if node does not have any dependencies
                if not node.dependency_list:
                    # remove it from node list and add to sorted node list
                    layer.node_list.remove(node)
                    layer.sorted_node_list.append(node)
                    # get output data list from sorted node
                    output_data_list = node.output_data_list

                    # remove outputs of that node from dependency list of other nodes under referenced layer
                    for output_link in output_data_list:
                        # get output data name
                        output_data_name = output_link[ActivityNode.DATA_NAME_INDEX]
                        # go through all nodes under given layer and refresh their dependency list
                        ModuleSorter.remove_data_from_layer_node_dependencies(output_data_name, layer)

        # record info
        for sorted_node in layer.sorted_node_list:
            Logger.save_in_log_file("ModuleSorter", "Have sorted " + str(sorted_node) + " node",
                                    False)

    # Description
    # This method removes given data name from dependency list of each node under related layer.
    @staticmethod
    def remove_data_from_layer_node_dependencies(data_name, layer):

        # go through all nodes under given layer
        for node in layer.node_list:
            # check all dependencies of that node
            for dependency in list(node.dependency_list):
                # if given data is found on dependency list
                if data_name == dependency:
                    # remove dependency form dependency list
                    node.dependency_list.remove(dependency)

    # Description
    # This method sorts input data elements if interaction requires to point main data input.
    def sort_input_data_list(self):

        # record info
        Logger.save_in_log_file("ModuleSorter", "Sorting input data list under diagram layer nodes", False)

        # sort input data nodes under diagram layer
        ModuleSorter.sort_input_data_list_under_layer(self.diagram_layer)

        # record info
        Logger.save_in_log_file("ModuleSorter", "Sorting input data list under clause layer nodes", False)

        # sort input data nodes under clause layer
        for condition_layer in self.condition_layer_list:
            Logger.save_in_log_file("ModuleSorter", "Sorting under " + str(condition_layer) + " layer", False)
            for clause_layer in condition_layer.clause_layer_list:
                Logger.save_in_log_file("ModuleSorter", "Sorting under " + str(clause_layer) + " layer", False)
                ModuleSorter.sort_input_data_list_under_layer(clause_layer)

    # Description:
    # This method sorts input data elements if interaction requires to point main data input.
    @staticmethod
    def sort_input_data_list_under_layer(layer):

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
        for sorted_node in layer.sorted_node_list:

            # if node is action type
            if sorted_node.type == ActivityNode.ACTION:

                # and if action is input sensitive, i.e. requires to distinguish main input data
                for input_sensitive_action in ModuleSorter.input_sensitive_action_list:
                    if (sorted_node.interaction[0:3] == input_sensitive_action) or \
                            (sorted_node.interaction[0:2] == input_sensitive_action):

                        # get marker position
                        marker_position = sorted_node.interaction.find("+")
                        # get main input data name
                        main_input_data_name = sorted_node.interaction[marker_position+1:len(sorted_node.interaction)]

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

        # find condition nodes, dependencies and sort clauses
        self.find_condition_nodes()
        self.find_condition_dependencies()
        self.sort_condition_clauses()

        # sort nodes basing on their dependencies
        self.sort_nodes()

        # sort input data list
        self.sort_input_data_list()
