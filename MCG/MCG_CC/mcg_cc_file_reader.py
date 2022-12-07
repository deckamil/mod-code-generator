#   FILE:           mcg_cc_file_reader.py
#
#   DESCRIPTION:
#       This module contains definition of FileReader class, which is
#       responsible for reading of model module content from .exml file.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           7 DEC 2022
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


from mcg_cc_file_finder import FileFinder
from mcg_cc_logger import Logger
from mcg_cc_supporter import Supporter
from mcg_cc_connection import Connection


# Description:
# This class allows to read model module content from .exml files.
class FileReader(object):

    # indexes of interface element list
    INTERFACE_ELEMENT_NAME_INDEX = 0
    INTERFACE_ELEMENT_TYPE_INDEX = 1

    # indexes of return data
    CONNECTION_LIST_INDEX = 0
    INPUT_INTERFACE_LIST_INDEX = 1
    OUTPUT_INTERFACE_LIST_INDEX = 2
    LOCAL_INTERFACE_LIST_INDEX = 3

    # Description:
    # This is class constructor.
    def __init__(self, file_finder_list):

        # initialize object data
        self.module_file = file_finder_list[FileFinder.MODULE_FILE_INDEX]
        self.activity_file = file_finder_list[FileFinder.ACTIVITY_FILE_INDEX]
        self.connection_list = []
        self.input_interface_list = []
        self.output_interface_list = []
        self.local_interface_list = []

    # Description:
    # This method looks for interface details of module operation.
    def read_interface_elements(self):

        # record info
        Logger.save_in_log_file("Reader", "Looking for module interface details in .exml file", False)

        # search for external interface details of operation in module file
        # i.e. operation input and output parameters
        for i in range(0, len(self.module_file)):

            # parameter details
            parameter_name = "UNKNOWN_NAME"
            parameter_direction = "UNKNOWN_DIRECTION"
            parameter_type = "UNKNOWN_TYPE"

            # if parameter section if found
            if "<ID name=" in self.module_file[i] and "mc=\"Standard.Parameter\"" in self.module_file[i]:
                # get parameter name
                parameter_name = Supporter.get_name(self.module_file[i])

                # search for parameter input/output direction and type
                for j in range(i, len(self.module_file)):

                    # if parameter direction is found
                    if "<ATT name=\"ParameterPassing\">In</ATT>" in self.module_file[j]:
                        # set input direction
                        parameter_direction = "INPUT"
                    elif "<ATT name=\"ParameterPassing\">Out</ATT>" in self.module_file[j]:
                        # set output direction
                        parameter_direction = "OUTPUT"

                    # if parameter type is found
                    if "<ID name=" in self.module_file[j] and "mc=\"Standard.DataType\"" in self.module_file[j]:
                        # get parameter type
                        parameter_type = Supporter.get_name(self.module_file[j])

                        # interface element
                        interface_element = []

                        # append parameter name to interface element
                        interface_element.insert(FileReader.INTERFACE_ELEMENT_NAME_INDEX, parameter_name)
                        # append parameter type to interface element
                        interface_element.insert(FileReader.INTERFACE_ELEMENT_TYPE_INDEX, parameter_type)

                        # if it is input parameter
                        if parameter_direction == "INPUT":
                            # append interface element to input interface list
                            self.input_interface_list.append(interface_element)
                        # else if it is output parameter
                        elif parameter_direction == "OUTPUT":
                            # append interface element to output interface list
                            self.output_interface_list.append(interface_element)

                        # exit 'for j in range' loop
                        break

        # search for internal interface details of operation in activity file
        # i.e. operation local variables
        for i in range(0, len(self.activity_file)):

            # local details
            local_name = "UNKNOWN_NAME"
            local_type = "UNKNOWN_TYPE"

            # if local section if found
            if "<OBJECT>" in self.activity_file[i] and \
                    "<ID name=" in self.activity_file[i+1] and \
                    "mc=\"Standard.InstanceNode\"" in self.activity_file[i+1]:
                # get local name
                local_name = Supporter.get_name(self.activity_file[i+1])

                # search for local direction and type
                for j in range(i, len(self.activity_file)):

                    # if local type is found
                    if "<ID name=" in self.activity_file[j] and "mc=\"Standard.DataType\"" in self.activity_file[j]:
                        # get local type
                        local_type = Supporter.get_name(self.activity_file[j])

                        # interface element
                        interface_element = []

                        # append local name to interface element
                        interface_element.insert(FileReader.INTERFACE_ELEMENT_NAME_INDEX, local_name)
                        # append local type to interface element
                        interface_element.insert(FileReader.INTERFACE_ELEMENT_TYPE_INDEX, local_type)
                        # append interface element to interface list
                        if interface_element not in self.local_interface_list:
                            self.local_interface_list.append(interface_element)

                        # exit 'for j in range' loop
                        break

        # record info
        for input_interface in self.input_interface_list:
            Logger.save_in_log_file("Reader", "Have found input interface " + str(input_interface) + " element",
                                    False)
        for output_interface in self.output_interface_list:
            Logger.save_in_log_file("Reader", "Have found output interface " + str(output_interface) + " element",
                                    False)
        for local_interface in self.local_interface_list:
            Logger.save_in_log_file("Reader", "Have found local interface " + str(local_interface) + " element",
                                    False)

    # Description:
    # This method looks for data targets on activity diagram.
    def read_data_targets(self):

        # record info
        Logger.save_in_log_file("Reader", "Looking for module data targets in .exml file", False)

        # search for data elements in activity file
        for i in range(0, len(self.activity_file)):

            # if data section if found
            if "<OBJECT>" in self.activity_file[i] and \
                    "<ID name=" in self.activity_file[i + 1] and \
                    (("mc=\"Standard.ActivityParameterNode\"" in self.activity_file[i+1]) or
                     ("mc=\"Standard.InstanceNode\"" in self.activity_file[i+1])):

                # get source data name
                source_data_name = Supporter.get_name(self.activity_file[i + 1])

                # if data is parameter type
                if "mc=\"Standard.ActivityParameterNode\"" in self.activity_file[i+1]:
                    # set parameter type
                    source_data_type = Connection.PARAMETER
                # if data is local type
                else:
                    # set local type
                    source_data_type = Connection.LOCAL

                # assume that data element does not have target section
                target_section_found = False

                # search for targets
                for j in range(i, len(self.activity_file)):

                    # if target section is found
                    if "<COMP relation=\"Outgoing\">" in self.activity_file[j]:
                        # set flag
                        target_section_found = True

                    # if target reference if found
                    if "<LINK relation=\"Target\">" in self.activity_file[j]:

                        # new connection instance
                        connection = Connection()
                        connection.source_name = source_data_name
                        connection.source_type = source_data_type

                        # if local data is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.InstanceNode\"" in self.activity_file[j + 2]:
                            # get target data name
                            target_data_name = Supporter.get_name(self.activity_file[j + 2])
                            # set connection target name
                            connection.target_name = target_data_name
                            # set connection target type
                            connection.target_type = Connection.LOCAL
                            # append connection to connection list
                            self.connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("Reader", "Have found " + str(connection) + " connection",
                                                    False)

                        # if local parameter is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.ActivityParameterNode\"" in self.activity_file[j + 2]:
                            # get target data name
                            target_data_name = Supporter.get_name(self.activity_file[j + 2])
                            # set connection target name
                            connection.target_name = target_data_name
                            # set connection target type
                            connection.target_type = Connection.PARAMETER
                            # append connection to connection list
                            self.connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("Reader", "Have found " + str(connection) + " connection",
                                                    False)

                        # if local action is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.OpaqueAction\"" in self.activity_file[j + 2]:
                            # get target action name
                            target_action_name = Supporter.get_name(self.activity_file[j + 2])
                            # get target action uid
                            target_action_uid = Supporter.get_uid(self.activity_file[j + 2])
                            # set connection target name
                            connection.target_name = target_action_name
                            # set connection target uid
                            connection.target_uid = target_action_uid
                            # set connection target type
                            connection.target_type = Connection.ACTION
                            # append connection to connection list
                            self.connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("Reader", "Have found " + str(connection) + " connection",
                                                    False)

                        # if other operation is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.InputPin\"" in self.activity_file[j + 2]:
                            # get target pin name
                            target_pin_name = Supporter.get_name(self.activity_file[j + 2])
                            # get target pin uid
                            target_pin_uid = Supporter.get_uid(self.activity_file[j + 2])
                            # find target operation name and uid
                            target_operation_name, target_operation_uid = self.find_operation(target_pin_uid)
                            # set connection target pin
                            connection.target_pin = target_pin_name
                            # set connection target name
                            connection.target_name = target_operation_name
                            # set connection uid
                            connection.target_uid = target_operation_uid
                            # set connection type
                            connection.target_type = Connection.OPERATION
                            # append connection to connection list
                            self.connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("Reader", "Have found " + str(connection) + " connection",
                                                    False)

                    # if end of target section is found
                    if "</COMP>" in self.activity_file[j]:
                        # exit 'for j in range' loop
                        break

                    # if there is no target section and end of dependencies section is found
                    if "</DEPENDENCIES>" in self.activity_file[j] and not target_section_found:
                        # exit 'for j in range' loop
                        break

    # Description:
    # This method looks for interaction targets on activity diagram.
    def read_interaction_targets(self):

        # record info
        Logger.save_in_log_file("Reader", "Looking for module interaction targets in .exml file", False)

        # search for interaction elements in activity file
        for i in range(0, len(self.activity_file)):

            # if interaction section if found
            if "<OBJECT>" in self.activity_file[i] and \
                    "<ID name=" in self.activity_file[i + 1] and \
                    (("mc=\"Standard.OpaqueAction\"" in self.activity_file[i + 1]) or
                     ("mc=\"Standard.CallOperationAction\"" in self.activity_file[i + 1])):

                # get source interaction name
                source_interaction_name = Supporter.get_name(self.activity_file[i+1])
                # get source interaction uid
                source_interaction_uid = Supporter.get_uid(self.activity_file[i+1])

                # if interaction is action type
                if "mc=\"Standard.OpaqueAction\"" in self.activity_file[i + 1]:
                    # set action type
                    source_interaction_type = Connection.ACTION
                # if interaction is operation type
                else:
                    # set operation type
                    source_interaction_type = Connection.OPERATION

                # unknown output pin from operation
                source_pin_name = "N/A"

                # assume that interaction element does not have target section
                target_section_found = False

                # search for targets
                for j in range(i, len(self.activity_file)):

                    # if target section is found
                    if "<COMP relation=\"Outgoing\">" in self.activity_file[j]:
                        # set flag
                        target_section_found = True

                    # if source pin is found
                    if "<ID name=" in self.activity_file[j] and "mc=\"Standard.OutputPin\"" in self.activity_file[j]:

                        # get source pin name
                        source_pin_name = Supporter.get_name(self.activity_file[j])

                    # if target reference if found
                    if "<LINK relation=\"Target\">" in self.activity_file[j]:

                        # new connection instance
                        connection = Connection()
                        connection.source_name = source_interaction_name
                        connection.source_uid = source_interaction_uid
                        connection.source_type = source_interaction_type

                        # if operation
                        if connection.source_type == Connection.OPERATION:
                            # set connection source pin
                            connection.source_pin = source_pin_name

                        # if local data is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.InstanceNode\"" in self.activity_file[j + 2]:
                            # get target data name
                            target_data_name = Supporter.get_name(self.activity_file[j + 2])
                            # set connection target name
                            connection.target_name = target_data_name
                            # set connection target type
                            connection.target_type = Connection.LOCAL
                            # append connection to connection list
                            self.connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("Reader", "Have found " + str(connection) + " connection",
                                                    False)

                        # if local parameter is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.ActivityParameterNode\"" in self.activity_file[j + 2]:
                            # get target data name
                            target_data_name = Supporter.get_name(self.activity_file[j + 2])
                            # set connection target name
                            connection.target_name = target_data_name
                            # set connection target type
                            connection.target_type = Connection.PARAMETER
                            # append connection to connection list
                            self.connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("Reader", "Have found " + str(connection) + " connection",
                                                    False)

                    # if end of target section if found
                    if "</COMP>" in self.activity_file[j]:
                        # exit "for j in range" loop
                        break

                    # if there is no target section and end of dependencies section is found
                    if "</DEPENDENCIES>" in self.activity_file[j] and not target_section_found:
                        # exit 'for j in range' loop
                        break

    # Description:
    # This method looks for operation on activity diagram, basing on uid of operation input pis.
    def find_operation(self, input_pin_uid):

        # operation details
        operation_name = "UNKNOWN_NAME"
        operation_uid = "UNKNOWN_UID"

        # search for operation in activity file
        for i in range(0, len(self.activity_file)):

            # if operation section if found
            if "<OBJECT>" in self.activity_file[i] and \
                    "<ID name=" in self.activity_file[i + 1] and \
                    "mc=\"Standard.CallOperationAction\"" in self.activity_file[i + 1]:
                # get operation name
                operation_name = Supporter.get_name(self.activity_file[i + 1])
                # get operation uid
                operation_uid = Supporter.get_uid(self.activity_file[i + 1])

            # if input uid if found under above operation
            if "<OBJECT>" in self.activity_file[i] and \
                    "<ID name=" in self.activity_file[i + 1] and \
                    "mc=\"Standard.InputPin\"" in self.activity_file[i + 1] and \
                    input_pin_uid in self.activity_file[i + 1]:
                # exit 'for i in range' loop
                break

        # return operation
        return operation_name, operation_uid

    # Description:
    # This method is responsible for reading of module details.
    def read_files(self):

        # record info
        Logger.save_in_log_file("Reader", "Reading module details from set of .exml files", True)

        # search for interface details
        self.read_interface_elements()

        # search for data targets
        self.read_data_targets()

        # search for interaction targets
        self.read_interaction_targets()

        # append collected data to file reader list
        file_reader_list = []
        file_reader_list.insert(FileReader.CONNECTION_LIST_INDEX, self.connection_list)
        file_reader_list.insert(FileReader.INPUT_INTERFACE_LIST_INDEX, self.input_interface_list)
        file_reader_list.insert(FileReader.OUTPUT_INTERFACE_LIST_INDEX, self.output_interface_list)
        file_reader_list.insert(FileReader.LOCAL_INTERFACE_LIST_INDEX, self.local_interface_list)

        # return file reader list
        return file_reader_list
