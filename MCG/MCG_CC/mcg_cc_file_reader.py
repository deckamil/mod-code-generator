#   FILE:           mcg_cc_file_reader.py
#
#   DESCRIPTION:
#       This module contains definition of FileReader class, which is
#       responsible for reading of model module content from .exml file.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           3 DEC 2022
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
    # This parameter defines index of target element marker from list of target elements returned
    # by find_target_element_name() method
    TARGET_ELEMENT_FOUND_INDEX = 0

    # This parameter defines index of target element name from list of target elements returned
    # by find_target_element_name() method
    TARGET_ELEMENT_NAME_INDEX = 1

    # This parameter defines index of interface element name
    INTERFACE_ELEMENT_NAME_INDEX = 0

    # This parameter defines index of interface element type
    INTERFACE_ELEMENT_TYPE_INDEX = 1

    # This list defines all valid interface types
    interface_type_list = ["INT8", "INT16", "INT32", "INT64",
                           "UINT8", "UINT16", "UINT32", "UINT64",
                           "FLOAT32", "FLOAT64"]

    # Indexes of reader list
    CONNECTION_LIST_INDEX = 0
    INTERACTION_LIST_INDEX = 1
    INPUT_INTERFACE_LIST_INDEX = 2
    OUTPUT_INTERFACE_LIST_INDEX = 3
    LOCAL_DATA_LIST_INDEX = 4

    # Description:
    # This is class constructor.
    def __init__(self, file_finder_list):

        # initialize object data
        self.module_file = file_finder_list[FileFinder.MODULE_FILE_INDEX]
        self.activity_file = file_finder_list[FileFinder.ACTIVITY_FILE_INDEX]
        self.connection_list = []
        self.data_list = []
        self.interaction_list = []
        self.input_interface_list = []
        self.output_interface_list = []
        self.local_data_list = []

    # Description:
    # This method checks if reference contains valid interface element type
    @staticmethod
    def check_if_interface_element_type(ref_interface_element_type, interface_element):
        # interface element type marker shows whether valid interface element type was found or not within reference
        interface_element_type_found = False

        # if signal is interface element under check
        if interface_element == "signal":

            # for all allowed signal types
            for interface_signal_type in FileReader.interface_signal_type_list:
                # if interface signal type is the same as in reference
                if interface_signal_type == ref_interface_element_type:
                    # change interface element type marker
                    interface_element_type_found = True
                    # exit loop
                    break

        # else if structure is interface element under check
        else:

            # for all allowed structure types
            for interface_structure_type in FileReader.interface_structure_type_list:
                # if interface structure type is the same as in reference
                if interface_structure_type == ref_interface_element_type:
                    # change interface element type marker
                    interface_element_type_found = True
                    # exit loop
                    break

        # return interface element type marker
        return interface_element_type_found

    # Description:
    # This method looks for <name> element, basing on target element type and its uid, within
    # content of .exml file, an example of .exml file line:
    # <ID name="input3" mc="Standard.Attribute" uid="338540aa-439c-4dc7-8414-a275ba3c08e1"/>
    def find_target_element_name(self, target_element_uid, target_element_type):

        # target element marker shows whether target element was found or not
        target_element_found = False
        # target element name
        target_element_name = ""

        # search for uid in file content
        for i in range(0, len(self.activity_file)):

            # if uid within the line
            if ("<OBJECT>" in self.activity_file[i]) and \
                    ("<ID name=" in self.activity_file[i + 1]) and \
                    (target_element_uid in self.activity_file[i + 1]):

                # search for target element definition
                for j in range(i + 1, len(self.activity_file)):

                    # if given line contains definition of target element
                    if ("<ID name=" in self.activity_file[j]) and \
                            (target_element_type in self.activity_file[j]):
                        # get line
                        line = self.activity_file[j]
                        # get line number
                        line_number = j + 1
                        # get target element name
                        target_element_name = FileReader.get_name(line, line_number)
                        # change target element marker
                        target_element_found = True
                        # exit "for j in range" loop
                        break

                    # if line contains </OBJECT> that means end of object definition
                    if "</OBJECT>" in self.activity_file[j]:
                        # exit "for j in range" loop
                        break

                # exit "for i in range" loop
                break

        # if target element has not been found
        if not target_element_found:
            # set target element name
            target_element_name = "TARGET_ELEMENT_NAME_NOT_FOUND"

        # append collected data to target element list
        target_element_list = []
        target_element_list.insert(FileReader.TARGET_ELEMENT_FOUND_INDEX, target_element_found)
        target_element_list.insert(FileReader.TARGET_ELEMENT_NAME_INDEX, target_element_name)

        # return target element list
        return target_element_list

    # Description:
    # This method looks for interface details of module operation.
    def read_interface_elements(self):

        # record info
        Logger.save_in_log_file("Reader", "Looking for module interface details in .exml file", False)

        # search for interface details of operation in module file
        for i in range(0, len(self.module_file)):

            # parameter details
            parameter_name = "UNKNOWN_NAME"
            parameter_direction = "UNKNOWN_DIRECTION"
            parameter_type = "UNKNOWN_TYPE"

            # if parameter name if found
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

        # record info
        for input_interface in self.input_interface_list:
            Logger.save_in_log_file("Reader", "Have found input interface " + str(input_interface) + " element", False)
        for output_interface in self.output_interface_list:
            Logger.save_in_log_file("Reader", "Have found output interface " + str(output_interface) + " element",
                                    False)

    # Description:
    # This method looks for data targets on activity diagram.
    def read_data_targets(self):

        # record info
        Logger.save_in_log_file("Reader", "Looking for module data targets in .exml file", False)

        # search for parameters in activity file
        for i in range(0, len(self.activity_file)):

            # if parameter section if found
            if "<OBJECT>" in self.activity_file[i] and \
                    "<ID name=" in self.activity_file[i + 1] and \
                    (("mc=\"Standard.ActivityParameterNode\"" in self.activity_file[i+1]) or
                     ("mc=\"Standard.InstanceNode\"" in self.activity_file[i+1])):

                # if parameter data
                if "mc=\"Standard.ActivityParameterNode\"" in self.activity_file[i+1]:
                    # set parameter source type
                    source_data_type = Connection.PARAMETER
                # if local data
                else:
                    source_data_type = Connection.LOCAL

                # get source data name
                source_data_name = Supporter.get_name(self.activity_file[i + 1])
                # append data to data list
                self.data_list.append(source_data_name)

                # search for targets
                for j in range(i, len(self.activity_file)):

                    # if parameter has targets
                    if "<COMP relation=\"Outgoing\">" in self.activity_file[j]:

                        # search for target references
                        for k in range(j, len(self.activity_file)):

                            # if target reference if found
                            if "<LINK relation=\"Target\">" in self.activity_file[k]:

                                # new connection instance
                                connection = Connection()
                                connection.source_name = source_data_name
                                connection.source_type = source_data_type

                                # if local data is target
                                if "<ID name=" in self.activity_file[k + 2] and \
                                        "mc=\"Standard.InstanceNode\"" in self.activity_file[k + 2]:
                                    # get target data name
                                    target_data_name = Supporter.get_name(self.activity_file[k + 2])
                                    # set connection target name
                                    connection.target_name = target_data_name
                                    # set connection target type
                                    connection.target_type = Connection.LOCAL
                                    # append connection to connection list
                                    self.connection_list.append(connection)

                                # if local parameter is target
                                if "<ID name=" in self.activity_file[k + 2] and \
                                        "mc=\"Standard.ActivityParameterNode\"" in self.activity_file[k + 2]:
                                    # get target data name
                                    target_data_name = Supporter.get_name(self.activity_file[k + 2])
                                    # set connection target name
                                    connection.target_name = target_data_name
                                    # set connection target type
                                    connection.target_type = Connection.PARAMETER
                                    # append connection to connection list
                                    self.connection_list.append(connection)

                                # if local action is target
                                if "<ID name=" in self.activity_file[k + 2] and \
                                        "mc=\"Standard.OpaqueAction\"" in self.activity_file[k + 2]:
                                    # get target action name
                                    target_action_name = Supporter.get_name(self.activity_file[k + 2])
                                    # get target action uid
                                    target_action_uid = Supporter.get_uid(self.activity_file[k + 2])
                                    # set connection target name
                                    connection.target_name = target_action_name
                                    # set connection target uid
                                    connection.target_uid = target_action_uid
                                    # set connection target type
                                    connection.target_type = Connection.ACTION
                                    # append connection to connection list
                                    self.connection_list.append(connection)

                                # if other operation is target
                                if "<ID name=" in self.activity_file[k + 2] and \
                                        "mc=\"Standard.InputPin\"" in self.activity_file[k + 2]:
                                    # get target pin name
                                    target_pin_name = Supporter.get_name(self.activity_file[k + 2])
                                    # get target pin uid
                                    target_pin_uid = Supporter.get_uid(self.activity_file[k + 2])
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

                            # if end of target section is found
                            if "</COMP>" in self.activity_file[k]:
                                # exit 'for k in range' loop
                                break

                    # if end of parameter section if found
                    if "</DEPENDENCIES>" in self.activity_file[j] and "</OBJECT>" in self.activity_file[j + 1]:
                        # exit 'for j in range' loop
                        break

        # remove duplicates from data list
        self.data_list = list(set(self.data_list))

        # record info
        for connection in self.connection_list:
            Logger.save_in_log_file("Reader", "Have found " + str(connection) + " connection", False)

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
        # self.read_interaction_targets()

        # check module correctness
        # self.check_correctness()

        # append collected data to module reader list
        # component_reader_list = []
        # component_reader_list.insert(ComponentReader.CONNECTION_LIST_INDEX, self.connection_list)
        # component_reader_list.insert(ComponentReader.INTERACTION_LIST_INDEX, self.interaction_list)
        # component_reader_list.insert(ComponentReader.INPUT_INTERFACE_LIST_INDEX, self.input_interface_list)
        # component_reader_list.insert(ComponentReader.OUTPUT_INTERFACE_LIST_INDEX, self.output_interface_list)
        # component_reader_list.insert(ComponentReader.LOCAL_DATA_LIST_INDEX, self.local_data_list)
        #
        # # return module reader list
        # return component_reader_list
