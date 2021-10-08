#   FILE:           mcg_cc_file_reader.py
#
#   DESCRIPTION:
#       This module contains definition of FileReader class, which is child
#       class or Reader class and is responsible for reading of .exml file
#       content.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           8 OCT 2021
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


from mcg_cc_reader import Reader
from mcg_cc_file_finder import FileFinder


# Class:
# FileReader()
#
# Description:
# This is child class responsible for reading of .exml file content.
class FileReader(Reader):

    # This parameter defines index of target element marker from list of target elements returned
    # by find_target_element_name() method
    TARGET_ELEMENT_FOUND_INDEX = 0

    # This parameter defines index of target element name from list of target elements returned
    # by find_target_element_name() method
    TARGET_ELEMENT_NAME_INDEX = 1

    # indexes of reader list
    MODEL_ELEMENT_NAME_INDEX = 0
    ACTIVITY_SOURCE_INDEX = 1
    NODE_LIST_INDEX = 2
    INTERACTION_LIST_INDEX = 3
    INPUT_INTERFACE_LIST_INDEX = 4
    OUTPUT_INTERFACE_LIST_INDEX = 5
    LOCAL_DATA_LIST_INDEX = 6

    # Method:
    # __init__()
    #
    # Description:
    # This is class constructor.
    #
    # Returns:
    # This method does not return anything.
    def __init__(self, file_finder_list):

        # initialize object data
        self.model_element_name = file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX]
        self.activity_source = file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX]
        self.activity_file = file_finder_list[FileFinder.ACTIVITY_FILE_INDEX]
        self.input_interface_source = file_finder_list[FileFinder.INPUT_INTERFACE_SOURCE_INDEX]
        self.input_interface_file = file_finder_list[FileFinder.INPUT_INTERFACE_FILE_INDEX]
        self.output_interface_source = file_finder_list[FileFinder.OUTPUT_INTERFACE_SOURCE_INDEX]
        self.output_interface_file = file_finder_list[FileFinder.OUTPUT_INTERFACE_FILE_INDEX]
        self.local_data_source = file_finder_list[FileFinder.LOCAL_DATA_SOURCE_INDEX]
        self.local_data_file = file_finder_list[FileFinder.LOCAL_DATA_FILE_INDEX]
        self.node_list = []
        self.data_list = []
        self.interaction_list = []
        self.input_interface_list = []
        self.output_interface_list = []
        self.local_data_list = []

    # Method:
    # find_target_element_name()
    #
    # Description:
    # This method looks for <name> element, basing on target element type and its uid, within
    # content of .exml file, an example of .exml file line:
    # <ID name="input3" mc="Standard.Attribute" uid="338540aa-439c-4dc7-8414-a275ba3c08e1"/>
    #
    # Returns:
    # This method returns target element list.
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

    # Method:
    # find_interface_signals()
    #
    # Description:
    # This method looks for name and type of interface signals within content of .exml file,
    # an example of .exml file line:
    # <ID name="loc_add_result" mc="Standard.Attribute" uid="47398f97-728c-4e18-aa19-d36a5c099ba7"/>
    # <ID name="INT16" mc="Standard.DataType" uid="e7213c05-8c48-4585-8bc5-cc8690ffd6be"/>
    #
    # Returns:
    # This method returns interface signal list.
    @staticmethod
    def find_interface_signals(interface_file):
        # local data
        interface_signal = []
        interface_signal_list = []

        # search for interface signals in interface file
        for i in range(0, len(interface_file)):

            # if given line contains definition of signal name
            if ("<ID name=" in interface_file[i]) and ("Standard.Attribute" in interface_file[i]):
                # get line
                line = interface_file[i]
                # get line number
                line_number = i + 1
                # get signal name
                signal_name = FileReader.get_name(line, line_number)
                # append signal name to interface signal
                interface_signal.append(signal_name)
            # if given line contain definition of signal type
            if ("<ID name=" in interface_file[i]) and ("Standard.DataType" in interface_file[i]):
                # get line
                line = interface_file[i]
                # get line number
                line_number = i + 1
                # get signal type
                signal_type = FileReader.get_name(line, line_number)
                # append signal type to interface signal
                interface_signal.append(signal_type)
                # append interface signal to interface signal list
                interface_signal_list.append(interface_signal)
                # clear interface signal
                interface_signal = []

        # return interface signal list
        return interface_signal_list

    # Method:
    # read_interface_signals()
    #
    # Description:
    # This method looks for signals of input interface, output interface and local data elements.
    #
    # Returns:
    # This method does not return anything.
    def read_interface_signals(self):

        # print details of interface file
        print("Interface Source:    " + str(self.input_interface_source))
        print("Interface Type:      " + str("Input Interface"))

        # record interface signal list
        print("*** RECORD INTERFACE ***")

        # find interface signals
        self.input_interface_list = FileReader.find_interface_signals(self.input_interface_file)

        # interface signal list recorded
        print("*** INTERFACE RECORDED ***")
        print()

        # print details of interface file
        print("Interface Source:    " + str(self.output_interface_source))
        print("Interface Type:      " + str("Output Interface"))

        # record interface signal list
        print("*** RECORD INTERFACE ***")

        # find interface signals
        self.output_interface_list = FileReader.find_interface_signals(self.output_interface_file)

        # interface signal list recorded
        print("*** INTERFACE RECORDED ***")
        print()

        # print details of interface file
        print("Interface Source:    " + str(self.local_data_source))
        print("Interface Type:      " + str("Local Data"))

        # record interface signal list
        print("*** RECORD INTERFACE ***")

        # find interface signals
        self.local_data_list = FileReader.find_interface_signals(self.local_data_file)

        # interface signal list recorded
        print("*** INTERFACE RECORDED ***")
        print()
