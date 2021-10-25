#   FILE:           mcg_cc_package_sorter.py
#
#   DESCRIPTION:
#       This module contains definition of PackageSorter class, which is child
#       class of Sorter class and is responsible for sorting of package content,
#       i.e. nodes of activity diagram.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           25 OCT 2021
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
#       You should have received a copy of the GNU General Public License
#       along with this program. If not, see <https://www.gnu.org/licenses/>.


from mcg_cc_sorter import Sorter
from mcg_cc_supporter import Supporter
from mcg_cc_logger import Logger


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
        Logger.record_in_log("*** remove input output interface element")

        # remove Input Interface elements from local data list
        for local_data in self.local_data_list:
            # if Input Interface element in local data
            if "Input Interface" in local_data[0]:
                # remove local data element from local data list
                self.local_data_list.remove(local_data)
                # break for loop
                break

        # remove Output Interface element from local data list
        for local_data in self.local_data_list:
            # if Output Interface element in local data
            if "Output Interface" in local_data[0]:
                # remove local data element from local data list
                self.local_data_list.remove(local_data)
                # break for loop
                break

    # Method:
    # merge_output_assignment()
    #
    # Description:
    # This method merges sorted nodes with output structure assignment into one sorted node on sorted node list.
    #
    # Returns:
    # This method does not return anything.
    def merge_output_assignment(self):

        # merge output assignment
        Logger.record_in_log("*** merge output assignment")

        # sorted node, where output structure assignment is merged
        sorted_node_with_merged_output_assignment = ""

        # search output structures within sorted node starting from this position
        index = 0

        # merge sorted node with output structure assignment
        for i in range(index, len(self.sorted_node_list)):
            # count number of keyword "target"
            target_number = self.sorted_node_list[index].count("target")

            # if sorted node contains only one target and it is Output Interface structure
            if (target_number == 1) and ("target Output Interface" in self.sorted_node_list[index]):
                # copy sorted node from given index
                sorted_node = self.sorted_node_list[index]
                # remove sorted node from sorted node list
                self.sorted_node_list.remove(sorted_node)
                # find output structure position within sorted node
                output_structure_position = sorted_node.rfind("target")
                # cut output structure name and target keyword from sorted node
                sorted_node_cut = sorted_node[0:output_structure_position + Supporter.TARGET_OFFSET]

                # append sorted node cut
                if sorted_node_with_merged_output_assignment == "":
                    sorted_node_with_merged_output_assignment = str(sorted_node_cut)
                else:
                    sorted_node_with_merged_output_assignment = sorted_node_with_merged_output_assignment + \
                                                                str(sorted_node_cut)

                # decrement index for next iteration, as one sorted node was removed
                # therefore all next sorted nodes were pushed by one position
                # towards beginning of list, e.g. [...,A,B,C] -> [...,B,C];
                # A was removed and now B is under previous position of A so at next
                # iteration the same index need to be checked to examine B;
                index = index - 1
            index = index + 1

        # append Output Interface target
        sorted_node_with_merged_output_assignment = sorted_node_with_merged_output_assignment + str("Output Interface")

        # append sorted node to sorted node list
        self.sorted_node_list.append(sorted_node_with_merged_output_assignment)

        # place sorted nodes with empty target (keyword "target empty") at the end of sorted node list
        for sorted_node in self.sorted_node_list:

            # if sorted node contains empty target
            if "target empty" in sorted_node:
                # remove sorted node from sorted node list
                self.sorted_node_list.remove(sorted_node)
                # append sorted node at the end of sorted node list
                self.sorted_node_list.append(sorted_node)
                # exit "for sorted_node in" loop
                break

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
        Logger.record_in_log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PACKAGE SORTER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

        # sort nodes of same component in one place under node list
        self.sort_interactions()

        # merge nodes of same component into one merged node on merged node list
        self.merge_nodes()

        # remove Input Interface and Output Interface elements from local data list
        self.remove_input_output_interface_element()

        # count dependencies between merged nodes
        self.count_dependencies()

        # sort merged nodes basing on their dependencies
        self.sort_nodes()

        # merge sorted nodes with output structure assignment
        self.merge_output_assignment()

        # process completed
        Logger.record_in_log("PROCESS COMPLETED")

        # display additional details after sorting
        if Supporter.PRINT_EXTRA_INFO:

            # print package details
            Logger.record_in_log("")
            Logger.record_in_log("Sorted Interactions:")
            for node in self.node_list:
                Logger.record_in_log("          " + str(node))
            Logger.record_in_log("Merged Nodes:")
            for merged_node in self.merged_node_list:
                Logger.record_in_log("          " + str(merged_node))
            Logger.record_in_log("Sorted Nodes:")
            for sorted_node in self.sorted_node_list:
                Logger.record_in_log("          " + str(sorted_node))

        # end of package sorter
        Logger.record_in_log("\n>>>>>>>>>>>>>>>>>>>>>>>>>>> END OF PACKAGE SORTER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # append collected data to package sorter list
        package_sorter_list = []
        package_sorter_list.insert(Sorter.SORTED_NODE_LIST_INDEX, self.sorted_node_list)

        # return package sorter list
        return package_sorter_list
