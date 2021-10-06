#   FILE:           mcg_cc_package_sorter.py
#
#   DESCRIPTION:
#       This module contains definition of PackageSorter class, which is child
#       class of Sorter class and is responsible for sorting of package content,
#       i.e. nodes of activity diagram.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           6 OCT 2021
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
    # sort_package()
    #
    # Description:
    # This method is responsible for sorting of package details.
    #
    # Returns:
    # This method returns sorted node list.
    def sort_package(self):

        # package sorting
        print("****************************** PACKAGE SORTING *****************************")
        print()

        # print component details
        print("Package Source:      " + str(self.activity_source))
        print("Package Name:        " + str(self.model_element_name))

        print("*** SORT NODES ***")

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

        print("*** NODES SORTED ***")
        print()

        # end of package sorting
        print("************************** END OF PACKAGE SORTING **************************")
        print()

        # append collected data to package sorter list
        package_sorter_list = []
        package_sorter_list.insert(Sorter.SORTED_NODE_LIST_INDEX, self.sorted_node_list)

        # return package sorter list
        return package_sorter_list
