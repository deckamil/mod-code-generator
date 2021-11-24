#   FILE:           mcg_cc_package_reader.py
#
#   DESCRIPTION:
#       This module contains definition of PackageReader class, which is child
#       class of FileReader class and is responsible for reading of package content,
#       i.e. activity diagram and interface details from .exml files.
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
from mcg_cc_error_handler import ErrorHandler
from mcg_cc_logger import Logger


# Class:
# PackageReader()
#
# Description:
# This is child class responsible for reading of package .exml file content.
class PackageReader(FileReader):

    # Function:
    # check_correctness()
    #
    # Description:
    # This function checks correctness of package content.
    #
    # Returns:
    # This function does not return anything.
    def check_correctness(self):

        # check correctness
        Logger.save_in_log_file("*** check correctness")

        # *** NEW CHECK SECTION ***
        # check if any structure used on diagram does not come from interface element
        for structure_name in self.data_list:
            # structure marker shows whether structure was found or not within interface element
            structure_found = False

            # go through all local data interface elements
            for interface_element in self.local_data_list:

                # get element_name
                element_name = interface_element[0]

                # if diagram structure is identified as interface element
                if (structure_name in element_name) and (element_name in structure_name):
                    # change structure marker
                    structure_found = True
                    # break "for interface_element in" loop
                    break

            # if diagram structure is not found in interface element
            if not structure_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_STR_NOT_IN_INT, structure_name, "none")

    # Function:
    # read_data_targets()
    #
    # Description:
    # This function looks data targets, i.e. package structures and their targets from activity diagram.
    #
    # Returns:
    # This function does not return anything.
    def read_data_targets(self):

        # read data targets
        Logger.save_in_log_file("*** read data targets")

        # search for structures in activity file
        for i in range(0, len(self.activity_file)):

            # if given line contains definition of structure name
            if ("<ID name=" in self.activity_file[i]) and ("Standard.Attribute" in self.activity_file[i]):
                # get line
                line = self.activity_file[i]
                # get line number
                line_number = i + 1
                # get structure name
                structure_name = PackageReader.get_name(line, line_number)
                # append structure name to data list
                self.data_list.append(structure_name)

                # structure marker shows whether signal target has been found or not
                structure_has_targets = False

                # search for targets
                for j in range(i, len(self.activity_file)):

                    # if line contains <COMP that means the structure has some targets
                    if "<COMP" in self.activity_file[j]:
                        # change structure marker
                        structure_has_targets = True

                    # if line contains </DEPENDENCIES> then structure does not have any target
                    if ("</DEPENDENCIES>" in self.activity_file[j]) and (not structure_has_targets):
                        # append node to node list
                        self.node_list.append(str(structure_name) + " $TARGET$ $EMPTY$")
                        # exit "for j in range" loop
                        break

                    # if line contain <LINK relation="Target"> that means target for given structure
                    if ("<LINK relation=" in self.activity_file[j]) and ("Target" in self.activity_file[j]):
                        # if line contains uid of target element
                        if ("<ID name=" in self.activity_file[j + 2]) and \
                                ("Standard.InstanceNode" in self.activity_file[j + 2]):
                            # get line
                            line = self.activity_file[j + 2]
                            # get line number
                            line_number = j + 3
                            # get target uid
                            target_uid = PackageReader.get_uid(line, line_number)
                            # find target component name
                            target_component_list = self.find_target_element_name(target_uid, "Standard.Component")
                            # find target structure name
                            target_structure_list = self.find_target_element_name(target_uid, "Standard.Attribute")

                            # get target component marker
                            target_component_found = target_component_list[PackageReader.TARGET_ELEMENT_FOUND_INDEX]
                            # get target component name
                            target_component_name = target_component_list[PackageReader.TARGET_ELEMENT_NAME_INDEX]

                            # get target structure marker
                            target_structure_found = target_structure_list[PackageReader.TARGET_ELEMENT_FOUND_INDEX]
                            # get target structure name
                            target_structure_name = target_structure_list[PackageReader.TARGET_ELEMENT_NAME_INDEX]

                            # if target element was not found
                            if (not target_component_found) and (not target_structure_found):
                                # record error
                                ErrorHandler.record_error(ErrorHandler.STR_ERR_NO_COM_STR_UID_TARGET,
                                                          target_uid,
                                                          structure_name)
                            # select target element
                            if not target_component_found:
                                target_element_name = target_structure_name
                            else:
                                target_element_name = target_component_name
                            # append node to node list
                            self.node_list.append(str(structure_name) + " $TARGET$ " + str(target_element_name))

                    # if line contains </COMP> that means end of targets for given structure
                    if "</COMP>" in self.activity_file[j]:
                        # exit "for j in range" loop
                        break

        # remove duplicates from data list
        self.data_list = list(set(self.data_list))

    # Function:
    # read_interaction_targets()
    #
    # Description:
    # This function looks interaction targets, i.e. package components and their targets from activity diagram.
    #
    # Returns:
    # This function does not return anything.
    def read_interaction_targets(self):

        # read interaction targets
        Logger.save_in_log_file("*** read interaction targets")

        # search for components in activity file
        for i in range(0, len(self.activity_file)):

            # if given line contains definition of component name
            if ("<ID name=" in self.activity_file[i]) and ("Standard.Component" in self.activity_file[i]):
                # get line
                line = self.activity_file[i]
                # get line number
                line_number = i + 1
                # get component name
                component_name = PackageReader.get_name(line, line_number)
                # append component name to interaction list
                self.interaction_list.append(component_name)

                # component marker shows whether component target has been found or not
                component_has_targets = False

                # search for targets
                for j in range(i, len(self.activity_file)):

                    # if line contains <COMP that means the component has some targets
                    if "<COMP" in self.activity_file[j]:
                        # component has some target
                        component_has_targets = True

                    # if line contains </DEPENDENCIES> then component does not have any target
                    if ("</DEPENDENCIES>" in self.activity_file[j]) and (not component_has_targets):
                        # record error
                        ErrorHandler.record_error(ErrorHandler.COM_ERR_NO_TARGET, component_name, "none")
                        # exit "for j in range" loop
                        break

                    # if line contain <LINK relation="Target"> that means target for given component
                    if ("<LINK relation=" in self.activity_file[j]) and ("Target" in self.activity_file[j]):
                        # if line contains uid of target element
                        if ("<ID name=" in self.activity_file[j + 2]) and \
                                ("Standard.InstanceNode" in self.activity_file[j + 2]):
                            # get line
                            line = self.activity_file[j + 2]
                            # get line number
                            line_number = j + 3
                            # get target structure uid
                            target_uid = PackageReader.get_uid(line, line_number)
                            # find target structure name
                            target_structure_list = self.find_target_element_name(target_uid, "Standard.Attribute")

                            # get target structure marker
                            target_structure_found = target_structure_list[PackageReader.TARGET_ELEMENT_FOUND_INDEX]
                            # get target structure name
                            target_structure_name = target_structure_list[PackageReader.TARGET_ELEMENT_NAME_INDEX]

                            # if target structure was not found
                            if not target_structure_found:
                                # record error
                                ErrorHandler.record_error(ErrorHandler.COM_ERR_NO_STR_UID_TARGET,
                                                          target_uid,
                                                          component_name)
                            # append node to node list
                            self.node_list.append(str(component_name) + " $TARGET$ " + str(target_structure_name))

                    # if line contains </COMP> that means end of targets for given component
                    if "</COMP>" in self.activity_file[j]:
                        # exit "for j in range" loop
                        break

        # remove duplicates from interaction list
        self.interaction_list = list(set(self.interaction_list))

    # Method:
    # read_package()
    #
    # Description:
    # This method is responsible for reading of package details.
    #
    # Returns:
    # This method returns package reader list, which describes package content and its activity.
    def read_package(self):

        # package reader
        Logger.save_in_log_file(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PACKAGE READER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

        # search for structure targets within activity file
        self.read_data_targets()

        # search for component targets within activity file
        self.read_interaction_targets()

        # search for interface elements
        self.read_interface_elements()

        # check package correctness
        self.check_correctness()

        # process completed
        Logger.save_in_log_file("PROCESS COMPLETED")

        # display additional details after package reading
        Logger.save_in_log_file("")
        Logger.save_in_log_file("Nodes:")
        for node in self.node_list:
            Logger.save_in_log_file("          " + str(node))
        Logger.save_in_log_file("Components:")
        for interaction in self.interaction_list:
            Logger.save_in_log_file("          " + str(interaction))
        Logger.save_in_log_file("Structures:")
        for data in self.data_list:
            Logger.save_in_log_file("          " + str(data))
        Logger.save_in_log_file("Input Interface:")
        for input_interface in self.input_interface_list:
            Logger.save_in_log_file("          " + str(input_interface))
        Logger.save_in_log_file("Output Interface:")
        for output_interface in self.output_interface_list:
            Logger.save_in_log_file("          " + str(output_interface))
        Logger.save_in_log_file("Local Data:")
        for local_data in self.local_data_list:
            Logger.save_in_log_file("          " + str(local_data))

        # end of package reader
        Logger.save_in_log_file("\n>>>>>>>>>>>>>>>>>>>>>>>>>>> END OF PACKAGE READER <<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # append collected data to package reader list
        package_reader_list = []
        package_reader_list.insert(PackageReader.MODEL_ELEMENT_NAME_INDEX, self.model_element_name)
        package_reader_list.insert(PackageReader.ACTIVITY_SOURCE_INDEX, self.activity_source)
        package_reader_list.insert(PackageReader.NODE_LIST_INDEX, self.node_list)
        package_reader_list.insert(PackageReader.INTERACTION_LIST_INDEX, self.interaction_list)
        package_reader_list.insert(PackageReader.INPUT_INTERFACE_LIST_INDEX, self.input_interface_list)
        package_reader_list.insert(PackageReader.OUTPUT_INTERFACE_LIST_INDEX, self.output_interface_list)
        package_reader_list.insert(PackageReader.LOCAL_DATA_LIST_INDEX, self.local_data_list)

        # return package reader list
        return package_reader_list
