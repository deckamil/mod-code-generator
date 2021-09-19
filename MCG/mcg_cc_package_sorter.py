#   FILE:           mcg_cc_package_sorter.py
#
#   DESCRIPTION:
#       This module is responsible for sorting of package content, i.e.
#       nodes of activity diagram from .exml files and preparing sorted list
#       of nodes for conversion into configuration file.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           19 SEP 2021
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


import mcg_cc_supporter
from mcg_cc_parameters import MCG_CC_TEST_RUN


# Function:
# merge_nodes()
#
# Description:
# This function merges nodes of same component from list of nodes into one merged node on list of merged
# nodes. This function also simplifies nodes before merging by removing of redundant component
# occurrences within node.
#
# Returns:
# This function returns list of merged nodes.
def merge_nodes(node_list, component_list):

    # list of merged nodes
    merged_node_list = []

    # merge nodes of same component from list of nodes into one node on list of merged nodes
    for i in range(0, len(component_list)):
        merged_node = ""
        # go through all nodes for each component on component_list
        for node in node_list:
            # if given component found in node
            if component_list[i] in node:
                keyword = "target " + str(component_list[i])
                # if keyword for given component is found
                if keyword in node:
                    # find target position
                    target_position = node.find("target")
                    # get structure name
                    structure_name = node[0:target_position-1]
                    # get simplified node
                    node = structure_name + str(" target")
                # append node of same component to temporary merged node
                if merged_node == "":
                    merged_node = merged_node + str(node)
                else:
                    merged_node = merged_node + " " + str(node)

        # append merged node to list of merged nodes
        merged_node_list.append(merged_node)

    # append "<structure name> target <structure name>" nodes to list of merged nodes
    for node in node_list:

        # component markers show whether component was found or not
        component_found = False

        # check if node contains component
        for component in component_list:
            # if component is found within reference
            if component in node:
                # change component marker
                component_found = True
                # exit loop
                break

        # if any component was not found within node and node does not contain "empty" keyword
        if (not component_found) and ("empty" not in node):
            # append node to list of merged nodes
            merged_node_list.append(node)

    # merge nodes with empty target from list of nodes into one node on list of merged nodes
    merged_node = ""
    for node in node_list:
        if "target empty" in node:
            # append node of empty target to temporary merged node
            if merged_node == "":
                merged_node = merged_node + str(node)
            else:
                merged_node = merged_node + " " + str(node)

    # append merged node to list of merged nodes
    merged_node_list.append(merged_node)

    # display additional details after package sorting for test run
    if MCG_CC_TEST_RUN:

        print("Merged Nodes:")
        for node in merged_node_list:
            print("          " + str(node))
        print()

    return merged_node_list


# Function:
# sort_package()
#
# Description:
# This is main function of this module and is responsible for sorting of package
# details from .exml files.
#
# Returns:
# This function returns list of sorted nodes.
def sort_package(node_list, component_list, local_data_list, package_source, package_name):

    # package sorting
    print("****************************** PACKAGE SORTING *****************************")
    print()

    # print component details
    print("Package Source:      " + str(package_source))
    print("Package Name:        " + str(package_name))

    print("*** SORT NODES ***")

    # sort nodes of same component in one place under list of nodes
    node_list = mcg_cc_supporter.sort_interactions(node_list, component_list)

    # merge nodes of same action into one merged node on list of merged nodes
    merged_node_list = merge_nodes(node_list, component_list)

    # remove Input Interface elements from list of local data elements
    for local_data in local_data_list:
        # if Input Interface element in local data
        if "Input Interface" in local_data[0]:
            # remove local data element from list of local data elements
            local_data_list.remove(local_data)
            # break for loop
            break

    # remove Output Interface element from list of local data elements
    for local_data in local_data_list:
        # if Output Interface element in local data
        if "Output Interface" in local_data[0]:
            # remove local data element from list of local data elements
            local_data_list.remove(local_data)
            # break for loop
            break

    # count dependencies between merged nodes
    dependency_list = mcg_cc_supporter.count_dependencies(merged_node_list, local_data_list)

    # sort merged nodes basing on their dependencies
    sorted_node_list = mcg_cc_supporter.sort_nodes(merged_node_list, dependency_list)

    print("*** NODES SORTED ***")
    print()

    # end of package sorting
    print("************************** END OF PACKAGE SORTING **************************")
    print()

    # return list of sorted nodes
    return sorted_node_list
