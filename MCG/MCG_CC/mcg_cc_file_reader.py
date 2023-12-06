#   FILE:           mcg_cc_file_reader.py
#
#   DESCRIPTION:
#       This module contains definition of FileReader class, which is
#       responsible for reading of module content from .exml file.
#
#   COPYRIGHT:      Copyright (C) 2021-2023 Kamil Deć github.com/deckamil
#   DATE:           6 DEC 2023
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


from mcg_cc_activity_connection import ActivityConnection
from mcg_cc_activity_collection import *
from mcg_cc_file_supporter import FileSupporter
from mcg_cc_file_finder import FileFinder
from mcg_cc_logger import Logger


# Description:
# This class allows to read module content from .exml files.
class FileReader(object):

    # indexes of data element list
    DATA_ELEMENT_TYPE_INDEX = 0
    DATA_ELEMENT_NAME_INDEX = 1
    DATA_ELEMENT_VALUE_INDEX = 2

    # indexes of return data
    OPERATION_NAME_INDEX = 0
    CONSTANT_LIST_INDEX = 1
    INPUT_INTERFACE_LIST_INDEX = 2
    OUTPUT_INTERFACE_LIST_INDEX = 3
    LOCAL_INTERFACE_LIST_INDEX = 4
    DIAGRAM_COLLECTION_INDEX = 5
    CONDITION_COLLECTION_LIST_INDEX = 6

    # Description:
    # This is class constructor.
    def __init__(self, file_finder_list):

        # initialize object data
        self.activity_file = file_finder_list[FileFinder.ACTIVITY_FILE_INDEX]
        self.module_file = file_finder_list[FileFinder.MODULE_FILE_INDEX]
        self.operation_name = "UNKNOWN"
        self.constant_list = []
        self.input_interface_list = []
        self.output_interface_list = []
        self.local_interface_list = []
        self.total_connection_list = []
        self.diagram_collection = ActivityDiagramCollection()
        self.condition_collection_list = []

    # Description:
    # This method looks for name of module operation.
    def read_operation_name(self):

        # record info
        Logger.save_in_log_file("FileReader", "Looking for module operation name in .exml file", False)

        # search for operation definition in module file
        for i in range(0, len(self.module_file)):

            # if operation section is found
            if "<COMP relation=\"OwnedOperation\">" in self.module_file[i]:
                # get operation name
                self.operation_name = FileSupporter.get_name(self.module_file[i + 2])
                # record info
                Logger.save_in_log_file("FileReader", "Have found " + str(self.operation_name) + " operation name",
                                        False)

    # Description:
    # This method looks for constant elements of module operation.
    def read_constant_elements(self):

        # record info
        Logger.save_in_log_file("FileReader", "Looking for module constant elements in .exml file", False)

        # search for constant definition in module file
        for i in range(0, len(self.module_file)):

            constant_name = "UNKNOWN"
            constant_type = "UNKNOWN"
            constant_value = "UNKNOWN"

            # if constant section is found
            if "<ID name=" in self.module_file[i] and "mc=\"Standard.Attribute\"" in self.module_file[i]:
                # get constant name
                constant_name = FileSupporter.get_name(self.module_file[i])

                # search for constant value and type
                for j in range(i, len(self.module_file)):

                    # if constant value is found
                    if "<ATT name=\"Value\"" in self.module_file[j]:
                        # get constant value start position
                        constant_value_start_position = self.module_file[j].find("[CDATA[")
                        # get constant value end position
                        constant_value_end_position = self.module_file[j].find("]]")
                        # get constant value
                        constant_value = self.module_file[j][constant_value_start_position+7:constant_value_end_position]

                    # if constant type is found
                    if "<ID name=" in self.module_file[j] and "mc=\"Standard.DataType\"" in self.module_file[j]:
                        # get constant type
                        constant_type = FileSupporter.get_name(self.module_file[j])

                        # constant element
                        constant_element = []

                        # append constant type to constant element
                        constant_element.insert(FileReader.DATA_ELEMENT_TYPE_INDEX, constant_type)
                        # append constant name to constant element
                        constant_element.insert(FileReader.DATA_ELEMENT_NAME_INDEX, constant_name)
                        # append constant value to constant element
                        constant_element.insert(FileReader.DATA_ELEMENT_VALUE_INDEX, constant_value)
                        # append constant element to constant list
                        self.constant_list.append(constant_element)
                        # record info
                        Logger.save_in_log_file("FileReader",
                                                "Have found constant " + str(constant_element) + " element",
                                                False)

                        # exit 'for j in range' loop
                        break

    # Description:
    # This method looks for interface elements of module operation.
    def read_interface_elements(self):

        # record info
        Logger.save_in_log_file("FileReader", "Looking for module interface elements in .exml file", False)

        # search for external interface details of operation in module file
        # i.e. operation input and output parameters
        for i in range(0, len(self.module_file)):

            # parameter details
            parameter_name = "UNKNOWN"
            parameter_direction = "UNKNOWN"
            parameter_type = "UNKNOWN"

            # if parameter section if found
            if "<ID name=" in self.module_file[i] and "mc=\"Standard.Parameter\"" in self.module_file[i]:
                # get parameter name
                parameter_name = FileSupporter.get_name(self.module_file[i])

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
                        parameter_type = FileSupporter.get_name(self.module_file[j])

                        # interface element
                        interface_element = []

                        # append parameter type to interface element
                        interface_element.insert(FileReader.DATA_ELEMENT_TYPE_INDEX, parameter_type)
                        # append parameter name to interface element
                        interface_element.insert(FileReader.DATA_ELEMENT_NAME_INDEX, parameter_name)

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
            local_name = "UNKNOWN"
            local_type = "UNKNOWN"

            # if local section is found and it is not an attribute
            if "<OBJECT>" in self.activity_file[i] and \
                    "<ID name=" in self.activity_file[i+1] and \
                    "mc=\"Standard.InstanceNode\"" in self.activity_file[i+1] and \
                    "mc=\"Standard.Attribute\"" not in self.activity_file[i + 13]:
                # get local name
                local_name = FileSupporter.get_name(self.activity_file[i+1])

                # search for local direction and type
                for j in range(i, len(self.activity_file)):

                    # if local type is found
                    if "<ID name=" in self.activity_file[j] and "mc=\"Standard.DataType\"" in self.activity_file[j]:
                        # get local type
                        local_type = FileSupporter.get_name(self.activity_file[j])

                        # interface element
                        interface_element = []

                        # append local type to interface element
                        interface_element.insert(FileReader.DATA_ELEMENT_TYPE_INDEX, local_type)
                        # append local name to interface element
                        interface_element.insert(FileReader.DATA_ELEMENT_NAME_INDEX, local_name)
                        # append interface element to interface list
                        if interface_element not in self.local_interface_list:
                            self.local_interface_list.append(interface_element)

                        # exit 'for j in range' loop
                        break

        # record info
        for input_interface in self.input_interface_list:
            Logger.save_in_log_file("FileReader", "Have found input interface " + str(input_interface) + " element",
                                    False)
        for output_interface in self.output_interface_list:
            Logger.save_in_log_file("FileReader", "Have found output interface " + str(output_interface) + " element",
                                    False)
        for local_interface in self.local_interface_list:
            Logger.save_in_log_file("FileReader", "Have found local interface " + str(local_interface) + " element",
                                    False)

    # Description:
    # This method looks for data targets on activity diagram.
    def read_data_targets(self):

        # record info
        Logger.save_in_log_file("FileReader", "Looking for module data targets in .exml file", False)

        # search for data elements in activity file
        for i in range(0, len(self.activity_file)):

            # if data section if found
            if "<OBJECT>" in self.activity_file[i] and \
                    "<ID name=" in self.activity_file[i + 1] and \
                    (("mc=\"Standard.ActivityParameterNode\"" in self.activity_file[i+1]) or
                     ("mc=\"Standard.InstanceNode\"" in self.activity_file[i+1])):

                # get connection index
                connection_index = i + 1

                # if it is local data represented by an attribute
                if "mc=\"Standard.Attribute\"" in self.activity_file[i + 13]:
                    # get source data name from attribute
                    source_data_name = FileSupporter.get_name(self.activity_file[i + 13])
                else:
                    # get source data name from instance node or activity parameter node
                    source_data_name = FileSupporter.get_name(self.activity_file[i + 1])

                # set data type depending on data section type
                if "mc=\"Standard.ActivityParameterNode\"" in self.activity_file[i+1]:
                    # set parameter data type
                    source_data_type = ActivityConnection.PARAMETER
                else:
                    # set local data type
                    source_data_type = ActivityConnection.LOCAL

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
                        connection = ActivityConnection()

                        # set connection index
                        connection.index = connection_index
                        # set connection source name
                        connection.source_name = source_data_name
                        # set connection source type
                        connection.source_type = source_data_type

                        # if local data is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.InstanceNode\"" in self.activity_file[j + 2]:
                            # get target data name
                            target_data_name = FileSupporter.get_name(self.activity_file[j + 2])
                            # set connection target name
                            connection.target_name = target_data_name
                            # set connection target type
                            connection.target_type = ActivityConnection.LOCAL
                            # append connection to total connection list
                            self.total_connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("FileReader", "Have found " + str(connection) + " connection",
                                                    False)

                        # if local parameter is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.ActivityParameterNode\"" in self.activity_file[j + 2]:
                            # get target data name
                            target_data_name = FileSupporter.get_name(self.activity_file[j + 2])
                            # set connection target name
                            connection.target_name = target_data_name
                            # set connection target type
                            connection.target_type = ActivityConnection.PARAMETER
                            # append connection to total connection list
                            self.total_connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("FileReader", "Have found " + str(connection) + " connection",
                                                    False)

                        # if local action is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.OpaqueAction\"" in self.activity_file[j + 2]:
                            # get target action name
                            target_action_name = FileSupporter.get_name(self.activity_file[j + 2])
                            # get target action uid
                            target_action_uid = FileSupporter.get_uid(self.activity_file[j + 2])
                            # set connection target name
                            connection.target_name = target_action_name
                            # set connection target uid
                            connection.target_uid = target_action_uid
                            # set connection target type
                            connection.target_type = ActivityConnection.ACTION
                            # append connection to total connection list
                            self.total_connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("FileReader", "Have found " + str(connection) + " connection",
                                                    False)

                        # if other operation is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.InputPin\"" in self.activity_file[j + 2]:
                            # get target pin name
                            target_pin_name = FileSupporter.get_name(self.activity_file[j + 2])
                            # get target pin uid
                            target_pin_uid = FileSupporter.get_uid(self.activity_file[j + 2])
                            # find target operation name and uid
                            target_operation_name, target_operation_uid = self.find_operation(target_pin_uid)
                            # set connection target pin
                            connection.target_pin = target_pin_name
                            # set connection target name
                            connection.target_name = target_operation_name
                            # set connection uid
                            connection.target_uid = target_operation_uid
                            # set connection type
                            connection.target_type = ActivityConnection.OPERATION
                            # append connection to total connection list
                            self.total_connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("FileReader", "Have found " + str(connection) + " connection",
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
        Logger.save_in_log_file("FileReader", "Looking for module interaction targets in .exml file", False)

        # search for interaction elements in activity file
        for i in range(0, len(self.activity_file)):

            # if interaction section if found
            if "<OBJECT>" in self.activity_file[i] and \
                    "<ID name=" in self.activity_file[i + 1] and \
                    (("mc=\"Standard.OpaqueAction\"" in self.activity_file[i + 1]) or
                     ("mc=\"Standard.CallOperationAction\"" in self.activity_file[i + 1])):

                # get connection index
                connection_index = i + 1
                # get source interaction name
                source_interaction_name = FileSupporter.get_name(self.activity_file[i+1])
                # get source interaction uid
                source_interaction_uid = FileSupporter.get_uid(self.activity_file[i+1])

                # if interaction is action type
                if "mc=\"Standard.OpaqueAction\"" in self.activity_file[i + 1]:
                    # set action type
                    source_interaction_type = ActivityConnection.ACTION
                # if interaction is operation type
                else:
                    # set operation type
                    source_interaction_type = ActivityConnection.OPERATION

                # unknown output pin from operation
                source_pin_name = "UNKNOWN"

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
                        source_pin_name = FileSupporter.get_name(self.activity_file[j])

                    # if target reference if found
                    if "<LINK relation=\"Target\">" in self.activity_file[j]:

                        # new connection instance
                        connection = ActivityConnection()

                        # ser connection index
                        connection.index = connection_index
                        # set connection source name
                        connection.source_name = source_interaction_name
                        # set connection source uid
                        connection.source_uid = source_interaction_uid
                        # set connection source type
                        connection.source_type = source_interaction_type

                        # if operation
                        if connection.source_type == ActivityConnection.OPERATION:
                            # set connection source pin
                            connection.source_pin = source_pin_name

                        # if local data is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.InstanceNode\"" in self.activity_file[j + 2]:
                            # get target data name
                            target_data_name = FileSupporter.get_name(self.activity_file[j + 2])
                            # set connection target name
                            connection.target_name = target_data_name
                            # set connection target type
                            connection.target_type = ActivityConnection.LOCAL
                            # append connection to total connection list
                            self.total_connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("FileReader", "Have found " + str(connection) + " connection",
                                                    False)

                        # if local parameter is target
                        if "<ID name=" in self.activity_file[j + 2] and \
                                "mc=\"Standard.ActivityParameterNode\"" in self.activity_file[j + 2]:
                            # get target data name
                            target_data_name = FileSupporter.get_name(self.activity_file[j + 2])
                            # set connection target name
                            connection.target_name = target_data_name
                            # set connection target type
                            connection.target_type = ActivityConnection.PARAMETER
                            # append connection to total connection list
                            self.total_connection_list.append(connection)
                            # record info
                            Logger.save_in_log_file("FileReader", "Have found " + str(connection) + " connection",
                                                    False)

                    # if end of action target section is found
                    if "</COMP>" in self.activity_file[j] and \
                            source_interaction_type == ActivityConnection.ACTION:
                        # exit "for j in range" loop
                        break

                    # if end of operation target section is found
                    if "</COMP>" in self.activity_file[j] and \
                            "</DEPENDENCIES>" in self.activity_file[j+1] and \
                            "</OBJECT>" in self.activity_file[j+2] and \
                            "</COMP>" in self.activity_file[j+3] and \
                            source_interaction_type == ActivityConnection.OPERATION:
                        # exit "for j in range" loop
                        break

                    # if there is no target section and end of dependencies section is found
                    if "</DEPENDENCIES>" in self.activity_file[j] and not target_section_found:
                        # exit 'for j in range' loop
                        break

    # Description:
    # This method looks for condition elements of module operation.
    def read_condition_elements(self):

        # record info
        Logger.save_in_log_file("FileReader", "Looking for module condition elements in .exml file", False)

        # counts how many "<OBJECT>" and "/<OBJECT>" occurs within condition or clause sections
        # when given counter is decremented back to 0 then it means end of given section
        condition_object_counter = 0
        clause_object_counter = 0

        # allows to determine whether beginning of condition or clause section have been found
        condition_found = False
        clause_found = False

        # new condition and clause collection instances
        condition = ActivityConditionCollection()
        clause = ActivityClauseCollection()

        # search for conditional elements in activity file
        for i in range(0, len(self.activity_file)):

            # if condition section is found
            if "<OBJECT>" in self.activity_file[i-1] and \
                    "<ID name=" in self.activity_file[i] and \
                    "mc=\"Standard.ConditionalNode\"" in self.activity_file[i]:

                # get condition name
                condition_name = FileSupporter.get_name(self.activity_file[i])
                # get condition uid
                condition_uid = FileSupporter.get_uid(self.activity_file[i])

                # new condition collection instance
                condition = ActivityConditionCollection()

                # set condition name
                condition.name = condition_name
                # set condition uid
                condition.uid = condition_uid

                # new condition section is found, therefore enable counting of
                # "<OBJECT>" and "/<OBJECT>" for condition element
                condition_object_counter = 1
                condition_found = True

            # if clause section is found
            if "<OBJECT>" in self.activity_file[i - 1] and \
                    "<ID name=" in self.activity_file[i] and \
                    "mc=\"Standard.Clause\"" in self.activity_file[i]:

                # get decision start position
                decision_start_position = self.activity_file[i+2].find("[CDATA[")
                # get decision end position
                decision_end_position = self.activity_file[i+2].find("]]")
                # get clause decision
                clause_decision = self.activity_file[i+2][decision_start_position + 7:decision_end_position]

                # get clause uid
                clause_uid = FileSupporter.get_uid(self.activity_file[i])

                # new clause collection instance
                clause = ActivityClauseCollection()

                # set clause start index
                clause.start_index = i
                # set clause decision
                clause.decision = clause_decision
                # set clause uid
                clause.uid = clause_uid

                # new clause section is found, therefore enable counting of
                # "<OBJECT>" and "/<OBJECT>" for clause element
                clause_object_counter = 1
                clause_found = True

            # if new "<OBJECT>" then increment required counters
            if ("<OBJECT>" in self.activity_file[i]) and condition_found:
                condition_object_counter = condition_object_counter+1

                if clause_found:
                    clause_object_counter = clause_object_counter+1

            # if new "</OBJECT>" then decrement required counters
            if ("</OBJECT>" in self.activity_file[i]) and condition_found:
                condition_object_counter = condition_object_counter-1

                if clause_found:
                    clause_object_counter = clause_object_counter-1

            # if end of clause section is found
            if (clause_object_counter == 0) and clause_found:

                # disable counting of "<OBJECT>" and "/<OBJECT>" for clause element
                clause_found = False
                # set clause end index
                clause.end_index = i
                # append clause to collection list
                condition.collection_list.append(clause)

            # if end of condition section is found
            if (condition_object_counter == 0) and condition_found:

                # disable counting of "<OBJECT>" and "/<OBJECT>" for condition element
                condition_found = False
                # append condition to condition list
                self.condition_collection_list.append(condition)

        # record info
        for condition in self.condition_collection_list:
            Logger.save_in_log_file("FileReader", "Have found " + str(condition) + " element", False)

            for clause in condition.collection_list:
                Logger.save_in_log_file("FileReader", "Have found " + str(clause) + " element", False)

    # Description:
    # This method allocates connections to their parental clauses under condition collection
    def allocate_connections_to_clauses(self):

        # record info
        Logger.save_in_log_file("FileReader", "Allocating connections to clause elements", False)

        # allocate connections to clause elements
        for condition in self.condition_collection_list:

            # record info
            Logger.save_in_log_file("FileReader", "Allocating to " + str(condition) + " element of .exml file", False)

            # for each clause
            for clause in condition.collection_list:

                # record info
                Logger.save_in_log_file("FileReader", "Allocating to " + str(clause) + " element of .exml file", False)

                # get clause start index
                clause_start_index = clause.start_index
                # get clause end index
                clause_end_index = clause.end_index

                # search for connections that appear between start and end index
                for connection in list(self.total_connection_list):

                    # get connection index
                    connection_index = connection.index
                    # if connection appears between both indexes it means
                    # that the connection belong to given clause
                    if (connection_index >= clause_start_index) and (connection_index <= clause_end_index):
                        # append connection to clause connection list
                        clause.collection_list.append(connection)
                        # remove connection from original connection list
                        self.total_connection_list.remove(connection)
                        # record info
                        Logger.save_in_log_file("FileReader", "Have allocated " + str(connection) + " connection", False)

    # Description:
    # This method allocates connections to diagram collection
    def allocate_connections_to_diagram(self):

        # record info
        Logger.save_in_log_file("FileReader", "Allocating connections to diagram element", False)

        # for each remaining connection that was not allocated to any other collection type
        for connection in list(self.total_connection_list):
            # append connection to diagram connection list
            self.diagram_collection.collection_list.append(connection)
            # remove connection from original connection list
            self.total_connection_list.remove(connection)
            # record info
            Logger.save_in_log_file("FileReader", "Have allocated " + str(connection) + " connection", False)

    # Description:
    # This method looks for operation on activity diagram, basing on uid of operation input pins.
    def find_operation(self, input_pin_uid):

        # operation details
        operation_name = "UNKNOWN"
        operation_uid = "UNKNOWN"

        # search for operation in activity file
        for i in range(0, len(self.activity_file)):

            # if operation section if found
            if "<OBJECT>" in self.activity_file[i] and \
                    "<ID name=" in self.activity_file[i + 1] and \
                    "mc=\"Standard.CallOperationAction\"" in self.activity_file[i + 1]:
                # get operation name
                operation_name = FileSupporter.get_name(self.activity_file[i + 1])
                # get operation uid
                operation_uid = FileSupporter.get_uid(self.activity_file[i + 1])

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
    # This method is responsible for reading of module content.
    def read_files(self):

        # record info
        Logger.save_in_log_file("FileReader", "Reading module details from set of .exml files", True)

        # search for operation name
        self.read_operation_name()

        # search for constant elements
        self.read_constant_elements()

        # search for interface elements
        self.read_interface_elements()

        # search for data targets
        self.read_data_targets()

        # search for interaction targets
        self.read_interaction_targets()

        # search for condition elements
        self.read_condition_elements()

        # allocate connections to clauses
        self.allocate_connections_to_clauses()

        # allocate connections to diagram
        self.allocate_connections_to_diagram()

        # append collected data to file reader list
        file_reader_list = []
        file_reader_list.insert(FileReader.OPERATION_NAME_INDEX, self.operation_name)
        file_reader_list.insert(FileReader.CONSTANT_LIST_INDEX, self.constant_list)
        file_reader_list.insert(FileReader.INPUT_INTERFACE_LIST_INDEX, self.input_interface_list)
        file_reader_list.insert(FileReader.OUTPUT_INTERFACE_LIST_INDEX, self.output_interface_list)
        file_reader_list.insert(FileReader.LOCAL_INTERFACE_LIST_INDEX, self.local_interface_list)
        file_reader_list.insert(FileReader.DIAGRAM_COLLECTION_INDEX, self.diagram_collection)
        file_reader_list.insert(FileReader.CONDITION_COLLECTION_LIST_INDEX, self.condition_collection_list)

        # return file reader list
        return file_reader_list
