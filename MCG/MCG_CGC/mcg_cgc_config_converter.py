#   FILE:           mcg_cgc_config_converter.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigConverter class, which allows to
#       generate source code modules from the configuration file.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           21 MAY 2022
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


from datetime import datetime
from mcg_cgc_module import Module


# Description:
# This class allows to generate source code modules from the configuration file.
class ConfigConverter(object):

    # expected data/marker positions or properties of configuration file
    COMPONENT_NAME_POSITION_IN_CFG = 15
    COMPONENT_SOURCE_POSITION_IN_CFG = 17
    INTERFACE_TYPE_POSITION_IN_CFG = 5
    INTERFACE_NAME_POSITION_IN_CFG = 6
    BODY_DATA_POSITION_IN_CFG = 4

    # path to source code directory
    code_dir_path = ""

    # Description:
    # This method sets path to output directory where source code will be generated.
    @staticmethod
    def set_code_dir_path(output_dir_path):

        # set code directory path
        ConfigConverter.code_dir_path = output_dir_path

    # Description:
    # This method saves module file on hard disk.
    @staticmethod
    def save_module_file(module_name, module_file):

        # set module file path
        module_file_path = ConfigConverter.code_dir_path + "\\" + module_name

        # open file in write mode
        module_file_disk = open(module_file_path, "w")
        # write module to file on hard disk
        module_file_disk.write(module_file)
        # close file
        module_file_disk.close()

    # Description:
    # This method generates source code modules from the configuration file.
    @staticmethod
    def generate_code_from_config_file(config_file):

        # get date
        date = datetime.now()
        # format date
        date = date.strftime("%d %b %Y, %H:%M:%S")

        # get new module
        module = Module()
        # module name
        module_name = ""

        # set file index
        file_index = 0
        # set number of config file lines
        number_of_config_file_lines = len(config_file)

        # continue conversion until end of the configuration file is reached
        while file_index < number_of_config_file_lines:

            # when new component definition is found
            if "COMPONENT START" in config_file[file_index]:
                # get new module
                module = Module()
                # set date
                module.generation_date = date

            # when component name is found
            elif "COMPONENT NAME" in config_file[file_index]:
                # get line
                line = config_file[file_index]
                # get module name
                module_name = line[ConfigConverter.COMPONENT_NAME_POSITION_IN_CFG:len(line)]
                # set module name
                module.module_name = module_name

            # when component comment is found
            elif "COMPONENT SOURCE" in config_file[file_index]:
                # get line
                line = config_file[file_index]
                # get comment
                comment = "The module was generated from file " + \
                          line[ConfigConverter.COMPONENT_SOURCE_POSITION_IN_CFG:len(line)]
                # append comment
                module.header_comment_list.append(comment)

            # when component input interface is found
            elif "COMPONENT INPUT INTERFACE START" in config_file[file_index]:

                # increment file index to definition of first input interface element
                file_index = file_index + 1

                # continue reading of input interface definition until end of input interface section is reached
                while "COMPONENT INPUT INTERFACE END" not in config_file[file_index]:
                    # get line
                    line = config_file[file_index]
                    # extract interface element type and name from line of the configuration file
                    interface_element = ConfigConverter.extract_interface_element(line)
                    # append interface element
                    module.input_interface_list.append(interface_element)
                    # increment file index
                    file_index = file_index + 1

            # when component output interface is found
            elif "COMPONENT OUTPUT INTERFACE START" in config_file[file_index]:

                # increment file index to definition of first output interface element
                file_index = file_index + 1

                # continue reading of output interface definition until end of output interface section is reached
                while "COMPONENT OUTPUT INTERFACE END" not in config_file[file_index]:
                    # get line
                    line = config_file[file_index]
                    # extract interface element type and name from line of the configuration file
                    interface_element = ConfigConverter.extract_interface_element(line)
                    # append interface element
                    module.output_interface_list.append(interface_element)
                    # increment file index
                    file_index = file_index + 1

            # when component local data is found
            elif "COMPONENT LOCAL DATA START" in config_file[file_index]:

                # increment file index to definition of first local data element
                file_index = file_index + 1

                # continue reading of local data definition until end of local data section is reached
                while "COMPONENT LOCAL DATA END" not in config_file[file_index]:
                    # get line
                    line = config_file[file_index]
                    # extract interface element type and name from line of the configuration file
                    interface_element = ConfigConverter.extract_interface_element(line)
                    # append interface element
                    module.local_data_list.append(interface_element)
                    # increment file index
                    file_index = file_index + 1

            # when component body is found
            elif "COMPONENT BODY START" in config_file[file_index]:

                # increment file index to definition of first body element
                file_index = file_index + 1

                # continue reading of body elements until end of body section is reached
                while "COMPONENT BODY END" not in config_file[file_index]:
                    # get line
                    line = config_file[file_index]

                    # if body line contains module comment
                    if "COM " in line:
                        # get comment
                        comment = "// " + line[ConfigConverter.BODY_DATA_POSITION_IN_CFG:len(line)]
                        # append comment
                        module.module_body_list.append(comment)
                    # otherwise when line contains module instruction
                    else:
                        # get instruction
                        instruction = line[ConfigConverter.BODY_DATA_POSITION_IN_CFG:len(line)]
                        # append instruction
                        module.module_body_list.append(instruction)

                    # increment file index
                    file_index = file_index + 1

            # when component end is found
            elif "COMPONENT END" in config_file[file_index]:

                # generate source file code
                module_source = module.generate_module_source()
                # set module source name
                module_source_name = module_name + ".c"
                # save module source to file
                ConfigConverter.save_module_file(module_source_name, module_source)

                # generate header file code
                module_header = module.generate_module_header()
                # set module header name
                module_header_name = module_name + '.h'
                # save module header to file
                ConfigConverter.save_module_file(module_header_name, module_header)

            # increment file index
            file_index = file_index + 1

    # Description:
    # This method extracts interface element type and interface element name from line of the configuration file.
    @staticmethod
    def extract_interface_element(line):

        # get name position within line
        name_position = line.find(" name ")
        # get interface element type
        interface_element_type = line[ConfigConverter.INTERFACE_TYPE_POSITION_IN_CFG:name_position]
        # get interface element name
        interface_element_name = line[name_position + ConfigConverter.INTERFACE_NAME_POSITION_IN_CFG:len(line)]

        # append collected data to interface element
        interface_element = []
        interface_element.insert(Module.INTERFACE_ELEMENT_TYPE_INDEX, interface_element_type)
        interface_element.insert(Module.INTERFACE_ELEMENT_NAME_INDEX, interface_element_name)

        # return interface element
        return interface_element
