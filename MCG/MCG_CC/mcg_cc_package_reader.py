#   FILE:           mcg_cc_package_reader.py
#
#   DESCRIPTION:
#       This module contains definition of PackageReader class, which is
#       responsible for reading of package content (activity diagram and
#       interface details) from .exml files.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           7 JUL 2022
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
from mcg_cc_connection import Connection


# Description:
# This class allows to read package content (activity diagram and interface details) from .exml files.
class PackageReader(FileReader):

    # Description:
    # This method checks correctness of package content.
    def check_correctness(self):

        # check correctness
        Logger.save_in_log_file("*** check correctness")

        # check structure-related errors
        self.check_structure_errors()

        # check interface-related errors
        self.check_interface_errors()

    # Description:
    # This method checks any structure-related errors and issues.
    def check_structure_errors(self):

        # **********************************************************************
        # check if any structure on data list has more than one input connection
        for structure_name in self.data_list:
            # input counter shows how many inputs (sources) are connected to given structure
            input_counter = 0

            # Output Interface structure is expected to have at least one input connection
            # therefore it is excluded from this check activity
            if structure_name != "Output Interface":

                # go through all connections for each structure
                for connection in self.connection_list:
                    # if connection target is same as structure name, then it means that
                    # structure has input connection (source)
                    if connection.connection_target == structure_name:
                        # increment input counter
                        input_counter = input_counter + 1

                # if structure has more than one input connection
                if input_counter > 1:
                    # record error
                    ErrorHandler.record_error(ErrorHandler.STR_ERR_MORE_INPUTS, structure_name, "none")

    # Description:
    # This method checks any interface-related errors and issues.
    def check_interface_errors(self):

        # ***************************************************************************
        # check if any structure used on diagram does not come from interface element
        for structure_name in self.data_list:
            # structure marker shows whether structure was found or not within interface element
            structure_found = False

            # go through all local data interface elements
            for interface_element in self.local_data_list:

                # get interface element name
                interface_element_name = interface_element[PackageReader.INTERFACE_ELEMENT_NAME_INDEX]

                # if diagram structure is identified as interface element
                if (structure_name in interface_element_name) and (interface_element_name in structure_name):
                    # change structure marker
                    structure_found = True
                    # break "for interface_element in" loop
                    break

            # if diagram structure is not found in interface element
            if not structure_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_STR_NOT_IN_INT, structure_name, "none")

        # *****************************************************************************
        # check if any input interface signal type in not valid
        for interface_element in self.input_interface_list:
            # get interface element name
            interface_element_name = interface_element[PackageReader.INTERFACE_ELEMENT_NAME_INDEX]
            # get interface element type
            interface_element_type = interface_element[PackageReader.INTERFACE_ELEMENT_TYPE_INDEX]

            # check if interface element type is valid
            interface_element_type_found = PackageReader.check_if_interface_element_type(interface_element_type,
                                                                                         "signal")

            # if interface element type is not valid
            if not interface_element_type_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_INC_INP_INT_TYPE_IN_PAC, interface_element_name,
                                          interface_element_type)

        # *****************************************************************************
        # check if any output interface signal type in not valid
        for interface_element in self.output_interface_list:
            # get interface element name
            interface_element_name = interface_element[PackageReader.INTERFACE_ELEMENT_NAME_INDEX]
            # get interface element type
            interface_element_type = interface_element[PackageReader.INTERFACE_ELEMENT_TYPE_INDEX]

            # check if interface element type is valid
            interface_element_type_found = PackageReader.check_if_interface_element_type(interface_element_type,
                                                                                         "signal")

            # if interface element type is not valid
            if not interface_element_type_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_INC_OUT_INT_TYPE_IN_PAC, interface_element_name,
                                          interface_element_type)

        # *****************************************************************************
        # check if any local data structure type in not valid
        for interface_element in self.local_data_list:
            # get interface element name
            interface_element_name = interface_element[PackageReader.INTERFACE_ELEMENT_NAME_INDEX]
            # get interface element type
            interface_element_type = interface_element[PackageReader.INTERFACE_ELEMENT_TYPE_INDEX]

            # check if interface element type is valid
            interface_element_type_found = PackageReader.check_if_interface_element_type(interface_element_type,
                                                                                         "structure")

            # if interface element type is not valid
            if not interface_element_type_found:
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_INC_LOC_DAT_TYPE_IN_PAC, interface_element_name,
                                          interface_element_type)

        # ****************************************************************************
        # check if input interface structure is connected as output (target) of another element
        for connection in self.connection_list:
            # if connection target is same as interface element name, then it means that
            # input interface element is connected as output (target) of another element
            if connection.connection_target == "Input Interface":
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_INP_INT_STR_IS_TAR_IN_PAC,
                                          connection.connection_source,
                                          "none")

        # ****************************************************************************
        # check if output interface structure is connected as input (source) of another element
        for connection in self.connection_list:
            # if connection source is same as interface element name, then it means that
            # output interface element is connected as input (source) of another element
            if (connection.connection_source == "Output Interface") and (connection.connection_target != "$EMPTY$"):
                # record error
                ErrorHandler.record_error(ErrorHandler.INT_ERR_OUT_INT_STR_IS_SRC_IN_PAC,
                                          connection.connection_target,
                                          "none")

    # Description:
    # This method looks for data targets, i.e. package structures and their targets from activity diagram.
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

                    # new connection instance
                    connection = Connection()

                    # if line contains <COMP that means the structure has some targets
                    if "<COMP" in self.activity_file[j]:
                        # change structure marker
                        structure_has_targets = True

                    # if line contains </DEPENDENCIES> then structure does not have any target
                    if ("</DEPENDENCIES>" in self.activity_file[j]) and (not structure_has_targets):
                        # set connection source
                        connection.connection_source = structure_name
                        # set connection $EMPTY$ target
                        connection.connection_target = "$EMPTY$"
                        # append connection to connection list
                        self.connection_list.append(connection)
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
                                target_element = target_structure_name
                            else:
                                target_element = str(target_component_name) + " " + str(target_uid)

                            # set connection source
                            connection.connection_source = structure_name
                            # set connection target
                            connection.connection_target = target_element
                            # append connection to connection list
                            self.connection_list.append(connection)

                    # if line contains </COMP> that means end of targets for given structure
                    if "</COMP>" in self.activity_file[j]:
                        # exit "for j in range" loop
                        break

        # remove duplicates from data list
        self.data_list = list(set(self.data_list))

    # Description:
    # This method looks for interaction targets, i.e. package components and their targets from activity diagram.
    def read_interaction_targets(self):

        # read interaction targets
        Logger.save_in_log_file("*** read interaction targets")

        # search for components in activity file
        for i in range(0, len(self.activity_file)):

            # if given line contains definition of model object
            if ("<ID name=" in self.activity_file[i]) and ("Standard.InstanceNode" in self.activity_file[i]) and \
                    ("<ATTRIBUTES>" in self.activity_file[i + 1]):

                # get line
                line = self.activity_file[i]
                # get line number
                line_number = i + 1
                # get object uid
                object_uid = PackageReader.get_uid(line, line_number)

                # search for component definition
                for j in range(i, len(self.activity_file)):

                    # if given line contains definition of component
                    if ("<LINK relation" in self.activity_file[j]) and ("Type" in self.activity_file[j]) and \
                            ("<ID name=" in self.activity_file[j + 1]) and \
                            ("Standard.Component" in self.activity_file[j + 1]):

                        # get line
                        line = self.activity_file[j + 1]
                        # get line number
                        line_number = j + 2
                        # get component name
                        component_name = PackageReader.get_name(line, line_number)
                        # get component uid
                        component_uid = object_uid
                        # get component
                        component = str(component_name) + " " + str(component_uid)
                        # append component name to interaction list
                        self.interaction_list.append(component)

                        # component marker shows whether component target has been found or not
                        component_has_targets = False

                        # search for targets
                        for k in range(j, len(self.activity_file)):

                            # new connection instance
                            connection = Connection()

                            # if line contains <COMP that means the component has some targets
                            if "<COMP" in self.activity_file[k]:
                                # component has some target
                                component_has_targets = True

                            # if line contains </DEPENDENCIES> then component does not have any target
                            if ("</DEPENDENCIES>" in self.activity_file[k]) and (not component_has_targets):
                                # record error
                                ErrorHandler.record_error(ErrorHandler.COM_ERR_NO_TARGET, component, "none")
                                # exit "for k in range" loop
                                break

                            # if line contain <LINK relation="Target"> that means target for given component
                            if ("<LINK relation=" in self.activity_file[k]) and ("Target" in self.activity_file[k]):
                                # if line contains uid of target element
                                if ("<ID name=" in self.activity_file[k + 2]) and \
                                        ("Standard.InstanceNode" in self.activity_file[k + 2]):
                                    # get line
                                    line = self.activity_file[k + 2]
                                    # get line number
                                    line_number = k + 3
                                    # get target structure uid
                                    target_uid = PackageReader.get_uid(line, line_number)
                                    # find target structure name
                                    target_structure_list = \
                                        self.find_target_element_name(target_uid, "Standard.Attribute")

                                    # get target structure marker
                                    target_structure_found = \
                                        target_structure_list[PackageReader.TARGET_ELEMENT_FOUND_INDEX]
                                    # get target structure name
                                    target_structure_name = \
                                        target_structure_list[PackageReader.TARGET_ELEMENT_NAME_INDEX]

                                    # if target structure was not found
                                    if not target_structure_found:
                                        # record error
                                        ErrorHandler.record_error(ErrorHandler.COM_ERR_NO_STR_UID_TARGET,
                                                                  target_uid,
                                                                  component)

                                    # set connection source
                                    connection.connection_source = component
                                    # set connection target
                                    connection.connection_target = target_structure_name
                                    # append connection to connection list
                                    self.connection_list.append(connection)

                            # if line contains </COMP> that means end of targets for given component
                            if "</COMP>" in self.activity_file[k]:
                                # exit "for k in range" loop
                                break

                    # if line contains <OBJECT> then stop searching as component definition should be detected earlier
                    if "<OBJECT>" in self.activity_file[j]:
                        # exit "for j in range" loop
                        break

        # remove duplicates from interaction list
        self.interaction_list = list(set(self.interaction_list))

    # Description:
    # This method is responsible for reading of package details.
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
        Logger.save_in_log_file("Connections:")
        for connection in self.connection_list:
            Logger.save_in_log_file("          " + str(connection))
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
        package_reader_list.insert(PackageReader.CONNECTION_LIST_INDEX, self.connection_list)
        package_reader_list.insert(PackageReader.INTERACTION_LIST_INDEX, self.interaction_list)
        package_reader_list.insert(PackageReader.INPUT_INTERFACE_LIST_INDEX, self.input_interface_list)
        package_reader_list.insert(PackageReader.OUTPUT_INTERFACE_LIST_INDEX, self.output_interface_list)
        package_reader_list.insert(PackageReader.LOCAL_DATA_LIST_INDEX, self.local_data_list)

        # return package reader list
        return package_reader_list
