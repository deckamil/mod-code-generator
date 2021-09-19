#   FILE:           mcg_cc_component_sorter.py
#
#   DESCRIPTION:
#       This module is responsible for sorting of component content, i.e.
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
from mcg_cc_parameters import FIRST_INPUT_SIGNAL_OFFSET
from mcg_cc_parameters import CUT_FIRST_INPUT_SIGNAL_OFFSET


# Function:
# merge_nodes()
#
# Description:
# This function merges nodes of same action from list of nodes into one merged node on list of merged
# nodes. This function also simplifies nodes before merging by removing of redundant action and uid
# occurrences within node.
#
# Returns:
# This function returns list of merged nodes.
def merge_nodes(node_list, action_list):

    # list of merged nodes
    merged_node_list = []

    # merge nodes of same action from list of nodes into one node on list of merged nodes
    for i in range(0, len(action_list)):
        merged_node = ""
        # go through all nodes for each action on action_list
        for node in node_list:
            # if given action found in node
            if action_list[i] in node:
                keyword = "target " + str(action_list[i])
                # if keyword for given action is found
                if keyword in node:
                    # find target position
                    target_position = node.find("target")
                    # get signal name
                    signal_name = node[0:target_position-1]
                    # get simplified node
                    node = signal_name + str(" target")
                # append node of same action to temporary merged node
                if merged_node == "":
                    merged_node = merged_node + str(node)
                else:
                    merged_node = merged_node + " " + str(node)

        # append merged node to list of merged nodes
        merged_node_list.append(merged_node)

    # append "<signal name> target <signal name>" nodes to list of merged nodes
    for node in node_list:

        # check if node contains any action
        action_type_found = mcg_cc_supporter.check_if_reference_contains_action_type(node)

        # if any action was not found within node and node does not contain "empty" keyword
        if (not action_type_found) and ("empty" not in node):
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

    # display additional details after component sorting for test run
    if MCG_CC_TEST_RUN:

        print("Merged Nodes:")
        for node in merged_node_list:
            print("          " + str(node))
        print()

    return merged_node_list


# Function:
# sort_first_input_signals()
#
# Description:
# This function moves node with first input signal, recognized by *FIRST* marker, at beginning of merged
# node and removes *FIRST* marker from it.
# In case of some type of actions the order of input signals, which take part in action calculation can
# influence on action results. In such case it is important to distinguish first input signal of given
# action and move it at beginning of action equation to get correct results.
#
# Returns:
# This function returns list of merged nodes with sorted first input signals.
def sort_first_input_signals(merged_node_list):

    # list of merged nodes, where *FIRST* marker was removed
    merged_node_with_removed_first_marker_list = []

    # for each merged node check if it contains type of action where sorting of first input signal is required
    for merged_node in merged_node_list:

        # check if merged node contains action requiring first input signal
        action_type_req_first_input_signal_found = mcg_cc_supporter.\
            check_if_reference_contains_action_type_req_first_input_signal(merged_node)

        # if merged node contains type of action, which requires to distinguish first input signal
        if action_type_req_first_input_signal_found:

            # find start marker of first input signal
            first_input_start = merged_node.find("*FIRST*")
            # find end marker of first input signal
            first_input_end = merged_node.rfind("*FIRST*")
            # get first input signal
            first_input_signal = merged_node[first_input_start + FIRST_INPUT_SIGNAL_OFFSET:
                                             first_input_end - 1]

            # get node with first input signal, but without *FIRST* markers
            first_input_signal_node = str(first_input_signal) + str(" target")

            # cut rest of nodes from merged node, but without node which contains first input signal
            if first_input_start == 0:
                cut_merged_node = merged_node[len(first_input_signal) + CUT_FIRST_INPUT_SIGNAL_OFFSET + 1:
                                              len(merged_node)]
            else:
                cut_merged_node = merged_node[0:first_input_start-1] + \
                                  merged_node[first_input_start+len(first_input_signal) +
                                              CUT_FIRST_INPUT_SIGNAL_OFFSET:len(merged_node)]

            # merge all nodes in correct order into temporary merged node without *FIRST* marker
            merged_node_with_removed_first_marker = str(first_input_signal_node) + str(" ") + str(cut_merged_node)

            # remove old merged node which contain *FIRST* markers from list of merged nodes
            merged_node_list.remove(merged_node)

            # append merged node without *FIRST* marker to temporary list of such merged nodes
            merged_node_with_removed_first_marker_list.append(merged_node_with_removed_first_marker)

    # for each merged node, where *FIRST* markers were removed
    for merged_node_with_removed_first_marker in merged_node_with_removed_first_marker_list:
        # append merged node at beginning of list of merged nodes
        merged_node_list = [merged_node_with_removed_first_marker] + merged_node_list

    # display additional details after component sorting for test run
    if MCG_CC_TEST_RUN:

        print("Sorted First Input Signals:")
        for merged_node in merged_node_list:
            print("          " + str(merged_node))
        print()

    return merged_node_list


# Function:
# sort_component()
#
# Description:
# This is main function of this module and is responsible for sorting of component
# details from .exml files.
#
# Returns:
# This function returns list of sorted nodes.
def sort_component(node_list, action_list, local_parameter_list, component_source, component_name):

    # component sorting
    print("***************************** COMPONENT SORTING ****************************")
    print()

    # print component details
    print("Component Source:    " + str(component_source))
    print("Component Name:      " + str(component_name))

    print("*** SORT NODES ***")

    # sort nodes of same action in one place under list of nodes
    node_list = mcg_cc_supporter.sort_interactions(node_list, action_list)

    # merge nodes of same action into one merged node on list of merged nodes
    merged_node_list = merge_nodes(node_list, action_list)

    # sort first input signals within list of merged nodes
    merged_node_list = sort_first_input_signals(merged_node_list)

    # count dependencies between merged nodes
    dependency_list = mcg_cc_supporter.count_dependencies(merged_node_list, local_parameter_list)

    # sort merged nodes basing on their dependencies
    sorted_node_list = mcg_cc_supporter.sort_nodes(merged_node_list, dependency_list)

    print("*** NODES SORTED ***")
    print()

    # end of component sorting
    print("************************* END OF COMPONENT SORTING *************************")
    print()

    # return list of sorted nodes
    return sorted_node_list
