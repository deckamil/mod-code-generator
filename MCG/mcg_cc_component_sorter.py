#   FILE:           mcg_cc_component_sorter.py
#
#   DESCRIPTION:
#       This module is responsible for sorting of component content, i.e.
#       nodes of activity diagram from .exml files and preparing sorted list
#       of nodes for conversion into configuration file.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           29 AUG 2021
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
from mcg_cc_parameters import action_type_list


# Function:
# sort_actions()
#
# Description:
# This function sorts nodes of same action in one place within list of nodes.
#
# Returns:
# This function returns list of nodes with sorted actions.
def sort_actions(node_list, action_list):

    # this index tells where to put node (defines new position of node)
    index = 0

    # repeat for each action recorded on list of actions
    # sort nodes of given action in one place within list of nodes
    # first, nodes with inputs to action are sorted (keyword "target + <action name>"),
    # then, node with output from action is placed after them (keyword "<action name> + target")
    for i in range(0, len(action_list)):
        # go through all nodes for each action on list of actions
        for node in node_list:
            keyword = "target " + str(action_list[i])
            # if keyword for given action is found
            if keyword in node:
                # remove action from current position on the list
                node_list.remove(node)
                # insert action under new position defined by index
                node_list.insert(index, node)
                # increment index to put next node right after this node
                index = index + 1
        # go through all nodes for each action on list of actions
        for node in node_list:
            keyword = str(action_list[i]) + " target"
            # if keyword for given action is found
            if keyword in node:
                # remove action from current position on the list
                node_list.remove(node)
                # insert action under new position defined by index
                node_list.insert(index, node)
                # increment index to put next node right after this node
                index = index + 1

    # place nodes with empty target (keyword "target empty") at the end of list of nodes
    for i in range(index, len(node_list)):
        # if signal does not have any target
        if "target empty" in node_list[index]:
            # copy node from given index
            node = node_list[index]
            # remove node
            node_list.remove(node)
            # insert node at the end of list
            node_list.insert(len(node_list), node)
            # decrement index for next iteration, as inserted node pushes by one position
            # from right to left other nodes, e.g. [...,...,...,A,B,C] -> [...,...,...,B,C,A]
            # A was placed at the end and now B is under previous position of A,
            # so at next iteration the same index need to be checked to examine B
            index = index - 1
        index = index + 1

    # display additional details after component sorting for test run
    if MCG_CC_TEST_RUN:

        print()
        print("Sorted Actions:")
        for node in node_list:
            print("          " + str(node))
        print()

    return node_list


# Function:
# merge_nodes()
#
# Description:
# This function merges nodes of same action from node list into one node on list of merged nodes and
# merges local parameters from list into one string. This function also simplifies nodes before merging by
# removing of redundant action and uid occurrences within node.
#
# Returns:
# This function returns list of merged nodes and list of merged local parameters.
def merge_nodes(node_list, action_list, local_parameter_list):

    # list of merged nodes
    merged_node_list = []
    merged_local_parameter = ""

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
        # action marker shows whether any action was found or not within node
        action_found = False

        # for all allowed type of actions
        for action_type in action_type_list:
            # if action type is found within node
            if action_type in node:
                # change action marker
                action_found = True
                # exit loop
                break

        # if any action was not found within node and node does not contain "empty" keyword
        if (not action_found) and ("empty" not in node):
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

    # merge local parameter into one string
    for lpl in local_parameter_list:
        merged_local_parameter = merged_local_parameter + " " + str(lpl[0])

    # display additional details after component sorting for test run
    if MCG_CC_TEST_RUN:

        print("Merged Nodes:")
        for node in merged_node_list:
            print("          " + str(node))
        print()

    return merged_node_list, merged_local_parameter


# Function:
# sort_first_input_signals()
#
# Description:
# This function moves node with first input signal, recognized by *FIRST* marker, at beginning of merged
# node and removes *FIRST* marker from it.
# In case of some type of actions the order of input signals, which take part in action calculation can
# influence on action results. In such case it is important to distinguish first input signal of given
# action and move it at beginning of action equation to get correct results of action calculation, which
# is done by this function.
#
# Returns:
# This function returns list of merged nodes with sorted first input signals.
def sort_first_input_signals(merged_node_list):

    # placeholder
    new_merged_node_list = []

    # for each merged node check if it contains type of action where sorting of first input signal is required
    for mnl in merged_node_list:

        # if node contains SUB action
        if "SUB" in mnl:

            # find start marker of first input signal
            first_input_start = mnl.find("*FIRST*")
            # find end marker of first input signal
            first_input_end = mnl.rfind("*FIRST*")
            # get first input signal
            first_input_signal = mnl[first_input_start + FIRST_INPUT_SIGNAL_OFFSET:
                                     first_input_end - 1]

            # get node with first input signal, but without *FIRST* markers
            first_input_signal_node = str(first_input_signal) + str(" target")

            # cut rest of nodes from merged node, but without node which contains first input signal
            if first_input_start == 0:
                cut_merged_node = mnl[len(first_input_signal) + CUT_FIRST_INPUT_SIGNAL_OFFSET + 1:len(mnl)]
            else:
                cut_merged_node = mnl[0:first_input_start-1] + mnl[first_input_start+len(first_input_signal)
                                                                   + CUT_FIRST_INPUT_SIGNAL_OFFSET:len(mnl)]

            # merge all nodes in correct order into new merged node without *FIRST* marker
            new_merged_node = str(first_input_signal_node) + str(" ") + str(cut_merged_node)

            # remove old merged node which contain *FIRST* markers from list of merged nodes
            merged_node_list.remove(mnl)

            # append new merged node to list of new merged nodes
            new_merged_node_list.append(new_merged_node)

    # for each node on list of new merged nodes
    for nmnl in new_merged_node_list:
        # append new merged node at beginning of list of merged nodes
        merged_node_list = [nmnl] + merged_node_list

    # display additional details after component sorting for test run
    if MCG_CC_TEST_RUN:

        print("Sorted First Input Signals:")
        for n in merged_node_list:
            print("          " + str(n))
        print()

    return merged_node_list


# Function:
# count_dependencies()
#
# Description:
# This function count dependencies between nodes, i.e. local parameters, which are inputs to nodes, and
# append them to sublist of dependence list.
#
# Returns:
# This function returns list of nodes with counted dependencies.
def count_dependencies(merged_node_list, merged_local_parameter, signal_list):

    # count dependencies between nodes
    # each node (with exception for target empty node) from merged_node_list has its own sublist on dependence_list
    # the sublist starts with node from merged_node_list (under index 0) and under further positions of the
    # sublist local parameters required to compute the node are appended, therefore if more local parameters are
    # needed to compute the node, then sublist is longer
    # in special case, if node does not need any local parameter (i.e. only input interface signals are inputs to node)
    # the length of sublist is equal to 1
    dependence_list = []
    for i in range(0, len(merged_node_list)):
        dependence = []
        if "target empty" not in merged_node_list[i]:
            # copy node from given index
            m = merged_node_list[i]
            # append node to dependence
            dependence.append(m)
            # find output signal within appended node
            output_signal = mcg_cc_supporter.find_output_signal(m)
            # go through all signal for each node on merged_node_list
            for s in signal_list:
                # if given signal is local signal of the node, i.e. there is signal occurrence within node,
                # signal is not in same time output signal from the node and signal belongs to local parameters
                if (s in m) and (s not in output_signal) and (s in merged_local_parameter):
                    # append signal to dependence
                    dependence.append(s)

        # if dependence is not empty
        if len(dependence) > 0:
            # append dependence to dependence_list
            dependence_list.append(dependence)

    # display additional details after component sorting for test run
    if MCG_CC_TEST_RUN:

        print("Dependencies:")
        for n in dependence_list:
            print("          " + str(n))
        print()

    return dependence_list


# Function:
# sort_nodes()
#
# Description:
# This function sort nodes basing on their dependencies from sublist of dependence_list.
#
# Returns:
# This function returns list of sorted nodes.
def sort_nodes(dependence_list, merged_node_list):

    # empty placeholder
    sorted_node_list = []

    # sort nodes basing on their dependencies
    # first append to sorted_node_list nodes with no dependencies, i.e. nodes from sublist which length is equal to 1,
    # which means that nodes do not consume any local parameters
    # then refresh dependencies of the rest of nodes on dependence_list, i.e. remove signal dependence if signal
    # comes from (is output from) appended node to sorted_node_list

    # dependence_list length
    dependence_list_length = len(dependence_list)
    # repeat as long dependence_list is not empty
    while dependence_list_length > 0:
        # go thorough all nodes on dependence_list
        for dep in dependence_list:
            # if given node does not have any dependencies
            if len(dep) == 1:
                # append node to sorted_node_list
                sorted_node_list.append(dep[0])
                # remove node from dependence_list
                dependence_list.remove(dep)
                # find output signal within appended node
                output_signal = mcg_cc_supporter.find_output_signal(dep[0])
                # compute new dependence_list_length
                dependence_list_length = len(dependence_list)
                # refresh dependencies of the rest of nodes on dependence_list
                for ref in dependence_list:
                    # if given node has dependencies
                    if len(ref) > 1:
                        # go through all dependencies of given node on dependence_list
                        index = 1
                        for i in range(index, len(ref)):
                            # if given node consumes signal, which comes from node appended to sorted_node_list
                            if output_signal in ref[index]:
                                # remove dependence from dependence_list
                                ref.remove(ref[index])
                                # decrement index for next iteration, as one dependence was removed
                                # therefore all next dependencies in ref was pushed by one position
                                # towards beginning of ref, e.g. [...,A,B,C] -> [...,B,C]
                                # A was removed now B is under previous position of A so at next
                                # iteration the same index need to be checked to examine B
                                # this technique is used because same local parameter could be used
                                # two or more times as input to same action
                                index = index - 1
                            index = index + 1
                # exit "dep in dependence_list" loop
                break

    # append merged nodes with empty target (last element of merged_node_list)
    sorted_node_list.append(merged_node_list[len(merged_node_list)-1])

    # display additional details after component sorting for test run
    if MCG_CC_TEST_RUN:

        print("Sorted Nodes:")
        for n in sorted_node_list:
            print("          " + str(n))
        print()

    # return sorted list of nodes
    return sorted_node_list


# Function:
# sort_component()
#
# Description:
# This is main function of this module and is responsible for sorting of component
# details from .exml files.
#
# Returns:
# This function returns sorted list of nodes.
def sort_component(node_list, action_list, signal_list, local_parameter_list, component_source, component_name):

    # component sorting
    print("***************************** COMPONENT SORTING ****************************")
    print()

    # print component details
    print("Component Source:    " + str(component_source))
    print("Component Name:      " + str(component_name))

    print("*** SORT NODES ***")

    # sort nodes of same action in one place of nodes list
    node_list = sort_actions(node_list, action_list)

    # merge nodes of same action on node list into one node on merged node list
    merged_node_list, merged_local_parameter = merge_nodes(node_list, action_list, local_parameter_list)

    # sort first input signals in merged node list
    merged_node_list = sort_first_input_signals(merged_node_list)

    # count dependencies between nodes
    dependence_list = count_dependencies(merged_node_list, merged_local_parameter, signal_list)

    # sort nodes basing on their dependencies
    sorted_node_list = sort_nodes(dependence_list, merged_node_list)

    print("*** NODES SORTED ***")
    print()

    # end of component sorting
    print("************************* END OF COMPONENT SORTING *************************")
    print()

    # return sorted list of nodes
    return sorted_node_list
