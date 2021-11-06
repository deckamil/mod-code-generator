#   FILE:           mcg_cc_component_sorter.py
#
#   DESCRIPTION:
#       This module contains definition of ComponentSorter class, which is child
#       class of Sorter class and is responsible for sorting of component content,
#       i.e. nodes of activity diagram.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           6 NOV 2021
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
from mcg_cc_supporter import Supporter
from mcg_cc_logger import Logger


# Class:
# ComponentSorter()
#
# Description:
# This is child class responsible for sorting of component content, i.e. nodes of activity diagram.
class ComponentSorter(Sorter):

    # This parameter defines offset, which is used to cut off first input signal node from merged node, i.e. first input
    # signal, its two markers "*FIRST*" and "target" marker, please note that length of first input signal name must be
    # added to the offset in order to calculate final offset used to cut desired part from merged node, an example of
    # merged node with first input signal node and without it:
    # eng_temp1 target *FIRST* eng_temp2 *FIRST* target SUB 4de5134b-40f6-44ae-a649-1cacb525963b target eng_temp_diff
    # eng_temp1 target SUB 4de5134b-40f6-44ae-a649-1cacb525963b target eng_temp_diff
    FIRST_INPUT_SIGNAL_CUT_OFFSET = 23

    # Method:
    # sort_first_input_signals()
    #
    # Description:
    # This method moves node with first input signal, recognized by *FIRST* marker, at beginning of merged
    # node and removes *FIRST* marker from it.
    #
    # Returns:
    # This method does not return anything.
    def sort_first_input_signals(self):

        # sort first input signals
        Logger.save_in_log_file("*** sort first input signals")

        # merged node list, where *FIRST* marker was removed
        merged_node_with_removed_first_marker_list = []

        # for each merged node check if it contains type of action where sorting of first input signal is required
        for merged_node in self.merged_node_list:

            # check if merged node contains action requiring first input signal
            action_type_req_first_input_signal_found = Supporter. \
                check_if_reference_contains_action_type_req_first_input_signal(merged_node)

            # if merged node contains type of action, which requires to distinguish first input signal
            if action_type_req_first_input_signal_found:

                # find start marker of first input signal
                first_input_start = merged_node.find("*FIRST*")
                # find end marker of first input signal
                first_input_end = merged_node.rfind("*FIRST*")
                # get first input signal
                first_input_signal = merged_node[first_input_start + Supporter.FIRST_INPUT_SIGNAL_OFFSET:
                                                 first_input_end - 1]

                # get node with first input signal, but without *FIRST* markers
                first_input_signal_node = str(first_input_signal) + str(" target")

                # cut rest of nodes from merged node, but without node which contains first input signal
                if first_input_start == 0:
                    merged_node_cut = merged_node[len(first_input_signal) +
                                                  ComponentSorter.FIRST_INPUT_SIGNAL_CUT_OFFSET + 1:
                                                  len(merged_node)]
                else:
                    merged_node_cut = merged_node[0:first_input_start - 1] + \
                                      merged_node[first_input_start + len(first_input_signal) +
                                                  ComponentSorter.FIRST_INPUT_SIGNAL_CUT_OFFSET:
                                                  len(merged_node)]

                # merge all nodes in correct order into temporary merged node without *FIRST* marker
                merged_node_with_removed_first_marker = str(first_input_signal_node) + str(" ") + str(merged_node_cut)

                # remove old merged node which contain *FIRST* markers from merged node list
                self.merged_node_list.remove(merged_node)

                # append merged node without *FIRST* marker to temporary merged node list
                merged_node_with_removed_first_marker_list.append(merged_node_with_removed_first_marker)

        # for each merged node, where *FIRST* markers were removed
        for merged_node_with_removed_first_marker in merged_node_with_removed_first_marker_list:
            # append merged node at beginning of merged node list
            self.merged_node_list = [merged_node_with_removed_first_marker] + self.merged_node_list

    # Method:
    # sort_component()
    #
    # Description:
    # This method is responsible for sorting of component details.
    #
    # Returns:
    # This method returns sorted node list.
    def sort_component(self):

        # component sorter
        Logger.save_in_log_file(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> COMPONENT SORTER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

        # sort nodes of same action in one place under node list
        self.sort_interactions()

        # merge nodes of same action into one merged node on merged node list
        self.merge_nodes()

        # sort first input signals within merged node list
        self.sort_first_input_signals()

        # count dependencies between merged nodes
        self.count_dependencies()

        # sort merged nodes basing on their dependencies
        self.sort_nodes()

        # process completed
        Logger.save_in_log_file("PROCESS COMPLETED")

        # display additional details after component sorting
        Logger.save_in_log_file("")
        Logger.save_in_log_file("Sorted Interactions:")
        for node in self.node_list:
            Logger.save_in_log_file("          " + str(node))
        Logger.save_in_log_file("Merged Nodes:")
        for merged_node in self.merged_node_list:
            Logger.save_in_log_file("          " + str(merged_node))
        Logger.save_in_log_file("Sorted Nodes:")
        for sorted_node in self.sorted_node_list:
            Logger.save_in_log_file("          " + str(sorted_node))

        # end of component sorter
        Logger.save_in_log_file("\n>>>>>>>>>>>>>>>>>>>>>>>>>> END OF COMPONENT SORTER <<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # append collected data to component sorter list
        component_sorter_list = []
        component_sorter_list.insert(Sorter.SORTED_NODE_LIST_INDEX, self.sorted_node_list)

        # return component sorter list
        return component_sorter_list
