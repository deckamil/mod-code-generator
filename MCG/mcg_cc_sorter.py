#   FILE:           mcg_cc_sorter.py
#
#   DESCRIPTION:
#       This module contains definition of Sorter class, which is responsible
#       for sorting of model element content, i.e. nodes of activity diagram.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           24 NOV 2021
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
from mcg_cc_supporter import Supporter
from mcg_cc_logger import Logger


# Class:
# Sorter()
#
# Description:
# This is base class responsible for sorting of model element content, i.e. nodes of activity diagram.
class Sorter(object):

    # indexes of sorter list
    SORTED_NODE_LIST_INDEX = 0

    # Method:
    # __init__()
    #
    # Description:
    # This is class constructor.
    #
    # Returns:
    # This method does not return anything.
    def __init__(self, reader_list):

        # initialize object data
        self.model_element_name = reader_list[FileReader.MODEL_ELEMENT_NAME_INDEX]
        self.activity_source = reader_list[FileReader.ACTIVITY_SOURCE_INDEX]
        self.node_list = reader_list[FileReader.NODE_LIST_INDEX]
        self.interaction_list = reader_list[FileReader.INTERACTION_LIST_INDEX]
        self.local_data_list = reader_list[FileReader.LOCAL_DATA_LIST_INDEX]
        self.merged_node_list = []
        self.dependency_list = []
        self.sorted_node_list = []

    # Method:
    # sort_interactions()
    #
    # Description:
    # This method sorts nodes with same interaction in one place within node list.
    #
    # Returns:
    # This method does not return anything.
    def sort_interactions(self):

        # sort interactions
        Logger.save_in_log_file("*** sort interactions")

        # this index tells where to put node (defines new position of node)
        index = 0

        # repeat for each interaction recorded on interaction list
        # sort nodes of given interaction in one place within node list
        # first, nodes with inputs to interaction are sorted (keyword "$TARGET$ + interaction"),
        # then, node with output from interaction is placed after them (keyword "interaction + $TARGET$")
        for i in range(0, len(self.interaction_list)):
            # go through all nodes for each interaction on interaction list
            for node in self.node_list:
                keyword = "$TARGET$ " + str(self.interaction_list[i])
                # if keyword for given action is found
                if keyword in node:
                    # remove node from current position on the list
                    self.node_list.remove(node)
                    # insert node under new position defined by index
                    self.node_list.insert(index, node)
                    # increment index to put next node right after this node
                    index = index + 1
            # go through all nodes for each interaction on interaction list
            for node in self.node_list:
                keyword = str(self.interaction_list[i]) + " $TARGET$"
                # if keyword for given action is found
                if keyword in node:
                    # remove node from current position on the list
                    self.node_list.remove(node)
                    # insert node under new position defined by index
                    self.node_list.insert(index, node)
                    # increment index to put next node right after this node
                    index = index + 1

        # place nodes with empty target (keyword "$TARGET$ $EMPTY$") at the end of node list
        for i in range(index, len(self.node_list)):
            # if data does not have any target
            if "$TARGET$ $EMPTY$" in self.node_list[index]:
                # copy node from given index
                node = self.node_list[index]
                # remove node
                self.node_list.remove(node)
                # insert node at the end of list
                self.node_list.insert(len(self.node_list), node)
                # decrement index for next iteration, as inserted node pushes by one position
                # from right to left other nodes, e.g. [...,...,...,A,B,C] -> [...,...,...,B,C,A];
                # A was placed at the end and now B is under previous position of A,
                # so at next iteration the same index need to be checked to examine B
                index = index - 1
            index = index + 1

    # Method:
    # merge_nodes()
    #
    # Description:
    # This method merges nodes of same interaction from node list into one merged node on merged node
    # list. This method also simplifies merged node by removing of redundant interaction occurrences within
    # merged node.
    #
    # Returns:
    # This method does not return anything.
    def merge_nodes(self):

        # merge nodes
        Logger.save_in_log_file("*** merge nodes")

        # merge nodes of same interaction from node list into one node on merged node list
        for i in range(0, len(self.interaction_list)):
            merged_node = ""
            # go through all nodes for each interaction on interaction list
            for node in self.node_list:
                # if given interaction found in node
                if self.interaction_list[i] in node:
                    keyword = "$TARGET$ " + str(self.interaction_list[i])
                    # if keyword for given interaction is found
                    if keyword in node:
                        # find target position
                        target_position = node.find("$TARGET$")
                        # get data name
                        data_name = node[0:target_position - 1]
                        # get simplified node
                        node = data_name + str(" $TARGET$")
                    # append node of same interaction to temporary merged node
                    if merged_node == "":
                        merged_node = merged_node + str(node)
                    else:
                        merged_node = merged_node + " " + str(node)

            # append merged node to merged node list
            self.merged_node_list.append(merged_node)

        # append "data $TARGET$ data" nodes to merged node list
        for node in self.node_list:

            # interaction marker show whether interaction was found or not within node
            interaction_found = False

            # check if node contains interaction
            for interaction in self.interaction_list:
                # if interaction is found within node
                if interaction in node:
                    # change interaction marker
                    interaction_found = True
                    # exit loop
                    break

            # if any interaction was not found within node and node does not contain "$EMPTY$" keyword
            if (not interaction_found) and ("$EMPTY$" not in node):
                # append node to merged node list
                self.merged_node_list.append(node)

        # merge nodes with empty target from node list into one node on merged node list
        merged_node = ""
        for node in self.node_list:
            if "$TARGET$ $EMPTY$" in node:
                # append node of empty target to temporary merged node
                if merged_node == "":
                    merged_node = merged_node + str(node)
                else:
                    merged_node = merged_node + " " + str(node)

        # append merged node to merged node list
        self.merged_node_list.append(merged_node)

    # Method:
    # count_dependencies()
    #
    # Description:
    # This method counts dependencies between merged nodes, i.e. number of local data elements outputted
    # by merged nodes, which are required to compute another merged node. The number of dependencies is
    # expressed by length of sublist created for each merged node under list of dependencies.
    #
    # Returns:
    # This method does not return anything.
    def count_dependencies(self):

        # count dependencies
        Logger.save_in_log_file("*** count dependencies")

        # each merged node (with exception for target empty node) has its own sublist under dependency list
        # the sublist starts with merged node under index 0 and local data elements required to compute the merged
        # node are appended under further indexes of the sublist;
        # as result, length of sublist express number of local data elements needed to compute the merged node;
        # in special case, if merged node does not need any local data element (i.e. only input interface elements
        # are required to compute the merged node) the length of sublist is equal to 1

        # count dependencies between nodes
        for i in range(0, len(self.merged_node_list)):
            # dependency sublist
            dependency = []
            if "$TARGET$ $EMPTY$" not in self.merged_node_list[i]:
                # copy merged node from given index
                merged_node = self.merged_node_list[i]
                # append merged node to dependency sublist
                dependency.append(merged_node)
                # find output element within merged node
                output_element_name = Sorter.find_output_element_name(merged_node)
                # go through all local data elements for each merged node on list of merged nodes
                for local_data in self.local_data_list:
                    # get name of local data element
                    local_data_name = local_data[0]
                    # if local data element is input to merged node
                    if (local_data_name in merged_node) and (local_data_name not in output_element_name):
                        # append name of local data element to dependency sublist
                        dependency.append(local_data_name)

            # if dependency sublist is not empty
            if len(dependency) > 0:
                # append dependency sublist to list of dependencies
                self.dependency_list.append(dependency)

    # Method:
    # sort_nodes()
    #
    # Description:
    # This method sort nodes basing on their dependencies from sublist under dependency list.
    #
    # Returns:
    # This method does not return anything.
    def sort_nodes(self):

        # sort nodes
        Logger.save_in_log_file("*** sort nodes")

        # sort nodes basing on their dependencies
        # first append merged nodes without dependencies to sorted node list, i.e. those merged nodes which
        # sublist length is equal to 1, which means that given merged node does not consume any local data elements
        # (or consume local data elements outputted by merged node, which was already appended to sorted node list);
        # then remove local data element outputted by above merged node from each sublist under dependency list,
        # which will lead to situation where some of sublist will have new length equal to 1;
        # next repeat the cycle until all merged nodes are sorted

        # number of merged nodes to sort, i.e. length of dependency list
        dependency_list_length = len(self.dependency_list)
        # repeat until all merged nodes are sorted
        while dependency_list_length > 0:
            # go thorough each dependency sublist
            for i in range(0, len(self.dependency_list)):
                # if given merged node under dependency sublist does not have any further dependencies
                if len(self.dependency_list[i]) == 1:
                    # get dependency sublist
                    dependency = self.dependency_list[i]
                    # append merged node to sorted node list
                    self.sorted_node_list.append(dependency[0])
                    # remove dependency sublist from dependency list
                    self.dependency_list.remove(dependency)
                    # find output element within merged node
                    output_element_name = Sorter.find_output_element_name(dependency[0])
                    # recalculate number of merged nodes to sort, i.e. length of dependency list
                    dependency_list_length = len(self.dependency_list)

                    # refresh each dependency sublist
                    for j in range(0, len(self.dependency_list)):
                        # if given merged node under dependency sublist does have further dependencies
                        if len(self.dependency_list[j]) > 1:
                            # get dependency sublist
                            dependency = self.dependency_list[j]
                            # set initial index
                            index = 1
                            # chek local data elements under dependency sublist
                            for k in range(index, len(dependency)):
                                # if given merged node consumes local data elements, which comes from merged node, which
                                # was appended above to sorted node list
                                if output_element_name in dependency[index]:
                                    # remove local data element from dependency sublist
                                    dependency.remove(dependency[index])
                                    # decrement index for next iteration, as one dependence was removed
                                    # therefore all next dependencies in ref was pushed by one position
                                    # towards beginning of ref, e.g. [...,A,B,C] -> [...,B,C];
                                    # A was removed and now B is under previous position of A so at next
                                    # iteration the same index need to be checked to examine B;
                                    index = index - 1
                                index = index + 1

                    # exit "for i in range" loop
                    break

        # append merged nodes with empty target (last element from merged node list)
        self.sorted_node_list.append(self.merged_node_list[len(self.merged_node_list) - 1])

    # Method:
    # find_output_element_name()
    #
    # Description:
    # This method looks for name of output element within merged node, i.e. name of element after last "target"
    # word occurrence within merged node.
    #
    # Returns:
    # This method returns output element name.
    @staticmethod
    def find_output_element_name(merged_node):
        # find position of output element name within merged node
        target_last_position = merged_node.rfind("$TARGET$")
        # get name of output element from merged node
        output_element_name = merged_node[target_last_position + Supporter.TARGET_OFFSET:len(merged_node)]

        # return output element name
        return output_element_name
