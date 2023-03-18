#   FILE:           mcg_cc_module_converter.py
#
#   DESCRIPTION:
#       This module contains definition of ModuleConverter class, which is responsible
#       for conversion of module content into configuration file format.
#
#   COPYRIGHT:      Copyright (C) 2021-2023 Kamil Deć github.com/deckamil
#   DATE:           18 MAR 2023
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
from mcg_cc_module_sorter import ModuleSorter
from mcg_cc_logger import Logger


# Description:
# This class allows to convert module content into configuration file format.
class ModuleConverter(object):

    # initialize class data
    configuration_file_disk = ""
    configuration_file_path = ""

    # Description:
    # This is class constructor.
    def __init__(self, file_finder_list, file_reader_list, module_sorter_list):

        # initialize object data
        self.module_name = file_finder_list[FileFinder.MODULE_NAME_INDEX]
        self.operation_name = file_finder_list[FileFinder.OPERATION_NAME_INDEX]
        self.input_interface_list = file_reader_list[FileReader.INPUT_INTERFACE_LIST_INDEX]
        self.output_interface_list = file_reader_list[FileReader.OUTPUT_INTERFACE_LIST_INDEX]
        self.local_interface_list = file_reader_list[FileReader.LOCAL_INTERFACE_LIST_INDEX]
        self.sorted_node_list = module_sorter_list[ModuleSorter.SORTED_NODE_LIST_INDEX]
        self.configuration_file = []

    # Description:
    # This method sets path to configuration file, which will contain input configuration to MCG CGC.
    @staticmethod
    def set_configuration_file_path(output_dir_path):

        # set configuration file path
        ModuleConverter.configuration_file_path = output_dir_path + str("\\mcg_cgc_config.txt")

        # open new file in write mode, then close file, to clear previous content
        ModuleConverter.configuration_file_disk = open(ModuleConverter.configuration_file_path, "w")
        ModuleConverter.configuration_file_disk.close()

    # Description:
    # This method saves header info in configuration file.
    @staticmethod
    def save_configuration_file_header():

        # open file in append mode, ready to save fresh configuration file content
        ModuleConverter.configuration_file_disk = open(ModuleConverter.configuration_file_path, "a")

        # get date
        date = datetime.datetime.now()

        # write header info to configuration file on hard disk
        ModuleConverter.configuration_file_disk.write(str("MCG CGC CONFIG START ") + str(date) + str("\n\n"))

        # close file
        ModuleConverter.configuration_file_disk.close()

    # Description:
    # This method saves footer info in configuration file.
    @staticmethod
    def save_configuration_file_footer():

        # open file in append mode, ready to save fresh configuration file content
        ModuleConverter.configuration_file_disk = open(ModuleConverter.configuration_file_path, "a")

        # get date
        date = datetime.datetime.now()

        # write footer info to configuration file on hard disk
        ModuleConverter.configuration_file_disk.write(str("MCG CGC CONFIG END ") + str(date))

        # close file
        ModuleConverter.configuration_file_disk.close()

    # Description:
    # This method saves configuration in configuration file.
    def save_in_configuration_file(self):

        # open file in append mode, ready to save fresh configuration file content
        ModuleConverter.configuration_file_disk = open(ModuleConverter.configuration_file_path, "a")

        # for each line in configuration file
        for line in self.configuration_file:
            # write line to configuration file on hard disk
            ModuleConverter.configuration_file_disk.write(line)
            ModuleConverter.configuration_file_disk.write("\n")

        # append separation
        ModuleConverter.configuration_file_disk.write("\n")
        # close file
        ModuleConverter.configuration_file_disk.close()

    # Description:
    # This method converts header details into configuration file.
    def convert_header(self):

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting module name into configuration file", False)

        # append start marker of module name section to configuration file
        self.configuration_file.append(str("$MODULE NAME START$"))
        # get configuration file line
        configuration_file_line = str(self.module_name)
        # append configuration file line to configuration file
        self.configuration_file.append(configuration_file_line)
        # append end marker of module name section to configuration file
        self.configuration_file.append(str("$MODULE NAME END$"))

        # record info
        Logger.save_in_log_file("ModuleConverter", "Have converted to " + str(configuration_file_line) + " line", False)

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting operation name into configuration file", False)

        # append start marker of operation name section to configuration file
        self.configuration_file.append(str("$OPERATION NAME START$"))
        # get configuration file line
        configuration_file_line = str(self.operation_name)
        # append configuration file line to configuration file
        self.configuration_file.append(configuration_file_line)
        # append end marker of operation name section to configuration file
        self.configuration_file.append(str("$OPERATION NAME END$"))

        # record info
        Logger.save_in_log_file("ModuleConverter", "Have converted to " + str(configuration_file_line) + " line", False)

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
            Logger.save_in_log_file("ModuleConverter", "Have converted to " + str(configuration_file_line) + " line", False)

    # Description:
    # This method converts input interface, output interface and local interface elements into configuration file.
    def convert_interfaces(self):

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting module input interface into configuration file", False)

        # append start marker of input interface section to configuration file
        self.configuration_file.append(str("$INPUT INTERFACE START$"))
        # append input interface details to configuration file
        self.convert_specific_interface(self.input_interface_list)
        # append end marker of input interface section to configuration file
        self.configuration_file.append(str("$INPUT INTERFACE END$"))

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting module output interface into configuration file", False)

        # append start marker of output interface section to configuration file
        self.configuration_file.append(str("$OUTPUT INTERFACE START$"))
        # append output interface details to configuration file
        self.convert_specific_interface(self.output_interface_list)
        # append end marker of output interface section to configuration file
        self.configuration_file.append(str("$OUTPUT INTERFACE END$"))

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting module local interface into configuration file", False)

        # append start marker of local interface section to configuration file
        self.configuration_file.append(str("$LOCAL INTERFACE START$"))
        # append local interface details to configuration file
        self.convert_specific_interface(self.local_interface_list)
        # append end marker of local interface section to configuration file
        self.configuration_file.append(str("$LOCAL INTERFACE END$"))

    # Description:
    # This method is responsible for conversion of module content into configuration file format.
    def convert_module(self):

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting module content into configuration file", True)

        # append start marker of new module section to configuration file
        self.configuration_file.append(str("$MODULE START$"))

        # convert header details
        self.convert_header()

        # convert interfaces
        self.convert_interfaces()

        # append end marker of new module section to configuration file
        self.configuration_file.append(str("$MODULE END$"))

        # record info
        Logger.save_in_log_file("ModuleConverter", "Saving conversion results into configuration file", False)

        # save configuration file
        self.save_in_configuration_file()

