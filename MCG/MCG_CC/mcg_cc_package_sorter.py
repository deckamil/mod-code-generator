#   FILE:           mcg_cc_package_sorter.py
#
#   DESCRIPTION:
#       This module contains definition of PackageSorter class, which is child
#       class of Sorter class and is responsible for sorting of package content,
#       i.e. nodes of activity diagram.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           20 FEB 2022
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


from mcg_cc_sorter import Sorter
from mcg_cc_logger import Logger
from mcg_cc_file_reader import FileReader
from mcg_cc_node import Node


# Class:
# PackageSorter()
#
# Description:
# This is child class responsible for sorting of package content, i.e. nodes of activity diagram.
class PackageSorter(Sorter):

    # Method:
    # remove_input_output_interface_element()
    #
    # Description:
    # This method removes Input Interface and Output Interface elements from local data list.
    #
    # Returns:
    # This method does not return anything.
    def remove_input_output_interface_element(self):

        # remove input output interface element
        Logger.save_in_log_file("*** remove input output interface element")

        # remove Input Interface elements from local data list
        for local_data in self.local_data_list:
            # if Input Interface element is found in local data element
            if "Input Interface" in local_data[FileReader.INTERFACE_ELEMENT_NAME_INDEX]:
                # remove local data element from local data list
                self.local_data_list.remove(local_data)
                # break for loop
                break

        # remove Output Interface element from local data list
        for local_data in self.local_data_list:
            # if Output Interface element is found in local data element
            if "Output Interface" in local_data[FileReader.INTERFACE_ELEMENT_NAME_INDEX]:
                # remove local data element from local data list
                self.local_data_list.remove(local_data)
                # break for loop
                break

    # Method:
    # replace_output_assignment()
    #
    # Description:
    # This method replaces nodes, where node input is assignment to Output Interface structure, with one node.
    #
    # Returns:
    # This method does not return anything.
    def replace_output_assignment(self):

        # replace output assignment
        Logger.save_in_log_file("*** replace output assignment")

        # replacement of sorted nodes, with structure assignment to Output Interface
        sorted_node_replacement = Node()
        # set interaction in node replacement
        sorted_node_replacement.node_interaction = str("ASSIGNMENT")
        # set output in node replacement
        sorted_node_replacement.node_output = str("Output Interface")

        # set initial index
        index = 0

        # replace sorted nodes, with structure assignment to Output Interface
        for i in range(index, len(self.sorted_node_list)):
            # get sorted node
            sorted_node = self.sorted_node_list[index]
            # if sorted node contains ASSIGNMENT interaction and Output Interface is node output
            if (sorted_node.node_interaction == "ASSIGNMENT") and (sorted_node.node_output == "Output Interface"):
                # append node input to node replacement
                sorted_node_replacement.node_input_list.append(sorted_node.node_input_list[0])
                # remove sorted node from sorted node list
                self.sorted_node_list.remove(sorted_node)
                # decrement index for next iteration, as one sorted node was removed
                # therefore all next sorted nodes in sorted node list were pushed by
                # one position towards beginning of the list, e.g. [...,A,B,C] -> [...,B,C];
                # A was removed and now B is under previous position of A so at next
                # iteration the same index need to be checked to examine B;
                index = index - 1
            index = index + 1

        # append node replacement to sorted node list
        self.sorted_node_list.append(sorted_node_replacement)

    # Method:
    # sort_package()
    #
    # Description:
    # This method is responsible for sorting of package details.
    #
    # Returns:
    # This method returns sorted node list.
    def sort_package(self):

        # package sorter
        Logger.save_in_log_file(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PACKAGE SORTER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

        # sort connections of same component into one place on connections list
        self.sort_connections()

        # find nodes base on connections and interactions
        self.find_nodes()

        # remove Input Interface and Output Interface elements from local data list
        self.remove_input_output_interface_element()

        # find dependencies between nodes
        self.find_dependencies()

        # sort nodes basing on their dependencies
        self.sort_nodes()

        # replace nodes with structure assignment to Output Interface
        self.replace_output_assignment()

        # process completed
        Logger.save_in_log_file("PROCESS COMPLETED")

        # display additional details after package sorting
        Logger.save_in_log_file("")
        Logger.save_in_log_file("Sorted Connections:")
        for connection in self.connection_list:
            Logger.save_in_log_file("          " + str(connection))
        Logger.save_in_log_file("Nodes:")
        for node in self.node_list:
            Logger.save_in_log_file("          " + str(node))
        Logger.save_in_log_file("Sorted Nodes:")
        for sorted_node in self.sorted_node_list:
            Logger.save_in_log_file("          " + str(sorted_node))

        # end of package sorter
        Logger.save_in_log_file("\n>>>>>>>>>>>>>>>>>>>>>>>>>>> END OF PACKAGE SORTER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # append collected data to package sorter list
        package_sorter_list = []
        package_sorter_list.insert(Sorter.SORTED_NODE_LIST_INDEX, self.sorted_node_list)

        # return package sorter list
        return package_sorter_list
