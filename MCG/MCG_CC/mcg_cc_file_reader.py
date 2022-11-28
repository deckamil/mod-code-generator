#   FILE:           mcg_cc_file_reader.py
#
#   DESCRIPTION:
#       This module contains definition of FileReader class, which is
#       responsible for reading of model module content from .exml file.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           28 NOV 2022
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


# Description:
# This class allows to read model module content from .exml files.
class FileReader(object):

    # This parameter defines index of target element marker from list of target elements returned
    # by find_target_element_name() method
    TARGET_ELEMENT_FOUND_INDEX = 0

    # This parameter defines index of target element name from list of target elements returned
    # by find_target_element_name() method
    TARGET_ELEMENT_NAME_INDEX = 1

    # This parameter defines index of interface element name from list of interface element returned
    # by find_interface_elements() method
    INTERFACE_ELEMENT_NAME_INDEX = 0

    # This parameter defines index of interface element type from list of interface element returned
    # by find_interface_elements() method
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
    # This method looks for name and type of interface signals/structures within content of .exml file,
    # an example of .exml file line:
    # <ID name="loc_add_result" mc="Standard.Attribute" uid="47398f97-728c-4e18-aa19-d36a5c099ba7"/>
    # <ID name="INT16" mc="Standard.DataType" uid="e7213c05-8c48-4585-8bc5-cc8690ffd6be"/>
    @staticmethod
    def find_interface_elements(interface_file):
        # local data
        interface_element = []
        interface_element_list = []

        # search for interface elements in interface file
        for i in range(0, len(interface_file)):

            # if given line contains definition of interface element name
            if ("<ID name=" in interface_file[i]) and ("Standard.Attribute" in interface_file[i]):
                # get line
                line = interface_file[i]
                # get line number
                line_number = i + 1
                # get interface element name
                interface_element_name = FileReader.get_name(line, line_number)
                # append interface element name to interface element
                interface_element.insert(FileReader.INTERFACE_ELEMENT_NAME_INDEX, interface_element_name)
            # if given line contain definition of interface element type
            if ("<ID name=" in interface_file[i]) and ("Standard.DataType" in interface_file[i]):
                # get line
                line = interface_file[i]
                # get line number
                line_number = i + 1
                # get interface element type
                interface_element_type = FileReader.get_name(line, line_number)
                # append interface element type to interface element
                interface_element.insert(FileReader.INTERFACE_ELEMENT_TYPE_INDEX, interface_element_type)
                # append interface element to interface element list
                interface_element_list.append(interface_element)
                # clear interface element
                interface_element = []

        # return interface element list
        return interface_element_list

    # Description:
    # This method looks for signals/structures of input interface, output interface and local data elements.
    def read_interface_elements(self):

        # record info
        Logger.save_in_log_file("Reader", "Looking for module interface details in .exml files", False)

        # find input interface elements
        self.input_interface_list = FileReader.find_interface_elements(self.input_interface_file)

        # find output interface elements
        self.output_interface_list = FileReader.find_interface_elements(self.output_interface_file)

        # find local data interface elements
        self.local_data_list = FileReader.find_interface_elements(self.local_data_file)

        # record info
        for input_interface in self.input_interface_list:
            Logger.save_in_log_file("Reader", "Have found input interface " + str(input_interface) + " element", False)
        for output_interface in self.output_interface_list:
            Logger.save_in_log_file("Reader", "Have found output interface " + str(output_interface) + " element", False)
        for local_data in self.local_data_list:
            Logger.save_in_log_file("Reader", "Have found local data " + str(local_data) + " element", False)

    # Description:
    # This method is responsible for reading of module details.
    def read_files(self):

        # record info
        Logger.save_in_log_file("Reader", "Reading module details from set of .exml files", True)

        # search for interface details
        # self.read_interface_elements()

        # search for data targets
        # self.read_data_targets()

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
