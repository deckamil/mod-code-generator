#   FILE:           mcg_cc_component_sorter.py
#
#   DESCRIPTION:
#       This module contains definition of ComponentSorter class, which is child
#       class of Sorter class and is responsible for sorting of component content,
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
from mcg_cc_supporter import Supporter
from mcg_cc_logger import Logger


# Class:
# ComponentSorter()
#
# Description:
# This is child class responsible for sorting of component content, i.e. nodes of activity diagram.
class ComponentSorter(Sorter):

    # Method:
    # sort_first_input_signals()
    #
    # Description:
    # This method moves first input signal, recognized by $FIRST$ marker, at beginning of node input list
    # and removes $FIRST$ marker.
    #
    # Returns:
    # This method does not return anything.
    def sort_first_input_signals(self):

        # sort first input signals
        Logger.save_in_log_file("*** sort first input signals")

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

        # sort connections of same action into one place on connections list
        self.sort_connections()

        # find nodes base on connections and interactions
        self.find_nodes()

        # sort first input signals within nodes
        self.sort_first_input_signals()

        # find dependencies between nodes
        self.find_dependencies()

        # sort nodes basing on their dependencies
        self.sort_nodes()

        # process completed
        Logger.save_in_log_file("PROCESS COMPLETED")

        # display additional details after component sorting
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

        # end of component sorter
        Logger.save_in_log_file("\n>>>>>>>>>>>>>>>>>>>>>>>>>> END OF COMPONENT SORTER <<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # append collected data to component sorter list
        component_sorter_list = []
        component_sorter_list.insert(Sorter.SORTED_NODE_LIST_INDEX, self.sorted_node_list)

        # return component sorter list
        return component_sorter_list
