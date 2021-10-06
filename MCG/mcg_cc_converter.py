#   FILE:           mcg_cc_converter.py
#
#   DESCRIPTION:
#       This module contains definition of Converter class, which is responsible
#       for conversion of model element content into configuration file.
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


from mcg_cc_file_reader import FileReader
from mcg_cc_sorter import Sorter


# Class:
# Converter()
#
# Description:
# This is base class responsible for conversion of model element content into configuration file.
class Converter(object):

    # Method:
    # __init__()
    #
    # Description:
    # This is class constructor.
    #
    # Returns:
    # This method does not return anything.
    def __init__(self, reader_list, sorter_list):

        # initialize object data
        self.model_element_name = reader_list[FileReader.MODEL_ELEMENT_NAME_INDEX]
        self.activity_source = reader_list[FileReader.ACTIVITY_SOURCE_INDEX]
        self.input_interface_list = reader_list[FileReader.INPUT_INTERFACE_LIST_INDEX]
        self.output_interface_list = reader_list[FileReader.OUTPUT_INTERFACE_LIST_INDEX]
        self.local_data_list = reader_list[FileReader.LOCAL_DATA_LIST_INDEX]
        self.interaction_list = reader_list[FileReader.INTERACTION_LIST_INDEX]
        self.sorted_node_list = sorter_list[Sorter.SORTED_NODE_LIST_INDEX]
        self.configuration_file = []

    # Method:
    # convert_specific_interface()
    #
    # Description:
    # This method converts specific interface type into configuration file.
    #
    # Returns:
    # This method does not return anything.
    def convert_specific_interface(self, interface_signal_list):

        # append interface details to configuration file
        for interface_signal in interface_signal_list:
            # get signal name
            signal_name = interface_signal[0]
            # get signal type
            signal_type = interface_signal[1]
            # get configuration file line
            configuration_file_line = "type " + str(signal_type) + " name " + str(signal_name)
            # append configuration file line to configuration file
            self.configuration_file.append(configuration_file_line)

    # Method:
    # convert_interfaces()
    #
    # Description:
    # This method converts input interface, output interface and local data elements into configuration file.
    #
    # Returns:
    # This method does not return anything.
    def convert_interfaces(self):

        # append start marker of input interface section to configuration file
        self.configuration_file.append(str("INPUT INTERFACE START"))
        # append input interface details to configuration file
        self.convert_specific_interface(self.input_interface_list)
        # append end marker of input interface section to configuration file
        self.configuration_file.append(str("INPUT INTERFACE END"))

        # append start marker of output interface section to configuration file
        self.configuration_file.append(str("OUTPUT INTERFACE START"))
        # append output interface details to configuration file
        self.convert_specific_interface(self.output_interface_list)
        # append end marker of output interface section to configuration file
        self.configuration_file.append(str("OUTPUT INTERFACE END"))

        # append start marker of local parameters section to configuration file
        self.configuration_file.append(str("LOCAL DATA START"))
        # append local data details to configuration file
        self.convert_specific_interface(self.local_data_list)
        # append end marker of local parameters section to configuration file
        self.configuration_file.append(str("LOCAL DATA END"))
