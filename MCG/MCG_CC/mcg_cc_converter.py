#   FILE:           mcg_cc_converter.py
#
#   DESCRIPTION:
#       This module contains definition of Converter class, which is responsible
#       for conversion of model module content into configuration file format.
#
#   COPYRIGHT:      Copyright (C) 2021-2022 Kamil Deć github.com/deckamil
#   DATE:           21 JUL 2022
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


import datetime
from mcg_cc_file_reader import FileReader
from mcg_cc_file_finder import FileFinder
from mcg_cc_sorter import Sorter
from mcg_cc_logger import Logger


# Description:
# This allows to convert model module content into configuration file format.
class Converter(object):

    # initialize class data
    configuration_file_disk = ""
    configuration_file_path = ""

    # Description:
    # This is class constructor.
    def __init__(self, file_finder_list, reader_list, sorter_list):

        # initialize object data
        self.model_element_name = file_finder_list[FileFinder.MODEL_ELEMENT_NAME_INDEX]
        self.activity_source = file_finder_list[FileFinder.ACTIVITY_SOURCE_INDEX]
        self.input_interface_list = reader_list[FileReader.INPUT_INTERFACE_LIST_INDEX]
        self.output_interface_list = reader_list[FileReader.OUTPUT_INTERFACE_LIST_INDEX]
        self.local_data_list = reader_list[FileReader.LOCAL_DATA_LIST_INDEX]
        self.interaction_list = reader_list[FileReader.INTERACTION_LIST_INDEX]
        self.sorted_node_list = sorter_list[Sorter.SORTED_NODE_LIST_INDEX]
        self.configuration_file = []

    # Description:
    # This method sets path to configuration file, which will contain input configuration to MCG CGC.
    @staticmethod
    def set_configuration_file_path(output_dir_path):

        # set configuration file path
        Converter.configuration_file_path = output_dir_path + str("\\mcg_cgc_config.txt")

        # open new file in write mode, then close file, to clear previous content
        Converter.configuration_file_disk = open(Converter.configuration_file_path, "w")
        Converter.configuration_file_disk.close()

    # Description:
    # This method saves header info in configuration file.
    @staticmethod
    def save_configuration_file_header():

        # open file in append mode, ready to save fresh configuration file content
        Converter.configuration_file_disk = open(Converter.configuration_file_path, "a")

        # get date
        date = datetime.datetime.now()

        # write header info to configuration file on hard disk
        Converter.configuration_file_disk.write(str("MCG CGC CONFIG START ") + str(date) + str("\n\n"))

        # close file
        Converter.configuration_file_disk.close()

    # Description:
    # This method saves footer info in configuration file.
    @staticmethod
    def save_configuration_file_footer():

        # open file in append mode, ready to save fresh configuration file content
        Converter.configuration_file_disk = open(Converter.configuration_file_path, "a")

        # get date
        date = datetime.datetime.now()

        # write footer info to configuration file on hard disk
        Converter.configuration_file_disk.write(str("MCG CGC CONFIG END ") + str(date))

        # close file
        Converter.configuration_file_disk.close()

    # Description:
    # This method saves configuration in configuration file.
    def save_in_configuration_file(self):

        # open file in append mode, ready to save fresh configuration file content
        Converter.configuration_file_disk = open(Converter.configuration_file_path, "a")

        # for each line in configuration file
        for line in self.configuration_file:
            # write line to configuration file on hard disk
            Converter.configuration_file_disk.write(line)
            Converter.configuration_file_disk.write("\n")

        # append separation
        Converter.configuration_file_disk.write("\n")
        # close file
        Converter.configuration_file_disk.close()

    # Description:
    # This method converts specific interface type into configuration file.
    def convert_specific_interface(self, interface_element_list):

        # append interface details to configuration file
        for interface_element in interface_element_list:
            # get interface element name
            interface_element_name = interface_element[FileReader.INTERFACE_ELEMENT_NAME_INDEX]
            # get interface element type
            interface_element_type = interface_element[FileReader.INTERFACE_ELEMENT_TYPE_INDEX]
            # get configuration file line
            configuration_file_line = "type " + str(interface_element_type) + " name " + str(interface_element_name)
            # append configuration file line to configuration file
            self.configuration_file.append(configuration_file_line)

            # record info
            Logger.save_in_log_file("Converter", "Have converted to " + str(configuration_file_line) + " line", False)

    # Description:
    # This method converts input interface, output interface and local data elements into configuration file.
    def convert_interfaces(self, model_element_type):

        # record info
        Logger.save_in_log_file("Converter", "Converting module input interface into configuration file", False)

        # append start marker of input interface section to configuration file
        self.configuration_file.append(str(model_element_type) + str(" INPUT INTERFACE START"))
        # append input interface details to configuration file
        self.convert_specific_interface(self.input_interface_list)
        # append end marker of input interface section to configuration file
        self.configuration_file.append(str(model_element_type) + str(" INPUT INTERFACE END"))

        # record info
        Logger.save_in_log_file("Converter", "Converting module output interface into configuration file", False)

        # append start marker of output interface section to configuration file
        self.configuration_file.append(str(model_element_type) + str(" OUTPUT INTERFACE START"))
        # append output interface details to configuration file
        self.convert_specific_interface(self.output_interface_list)
        # append end marker of output interface section to configuration file
        self.configuration_file.append(str(model_element_type) + str(" OUTPUT INTERFACE END"))

        # record info
        Logger.save_in_log_file("Converter", "Converting module local data into configuration file", False)

        # append start marker of local parameters section to configuration file
        self.configuration_file.append(str(model_element_type) + str(" LOCAL DATA START"))
        # append local data details to configuration file
        self.convert_specific_interface(self.local_data_list)
        # append end marker of local parameters section to configuration file
        self.configuration_file.append(str(model_element_type) + str(" LOCAL DATA END"))
