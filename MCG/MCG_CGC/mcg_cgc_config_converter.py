#   FILE:           mcg_cgc_config_converter.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigConverter class, which allows to
#       generate source code modules from the configuration file.
#
#   COPYRIGHT:      Copyright (C) 2022-2024 Kamil Deć github.com/deckamil
#   DATE:           13 APR 2024
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
from mcg_cgc_logger import Logger


# Description:
# This class allows to generate source code modules from the configuration file.
class ConfigConverter(object):

    # expected data/marker positions or properties of configuration file
    INTERFACE_TYPE_POSITION_IN_CFG = 5
    INTERFACE_NAME_POSITION_IN_CFG = 6
    INTERFACE_VALUE_POSITION_IN_CFG = 7
    BODY_DATA_POSITION_IN_CFG = 5

    # indexes of operation and module names on list
    OPERATION_NAME_INDEX = 0
    MODULE_NAME_INDEX = 1

    # contains list of operation and module name links
    operation_module_name_list = []

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

        # record info
        Logger.save_in_log_file("ConfigConverter",
                                "Starting conversion of the configuration file into source code", True)

        # get date
        date = datetime.now()
        # format date
        date = date.strftime("%d %b %Y, %H:%M:%S")
        # set date
        Module.generation_date = date

        # get new Module
        module = Module()
        module_name = ""

        # find list of operation and module name links
        ConfigConverter.find_operation_module_name_list(config_file)

        # set file index
        file_index = 0
        # set number of config file lines
        number_of_config_file_lines = len(config_file)

        # continue conversion until end of the configuration file is reached
        while file_index < number_of_config_file_lines:

            # when new module definition is found
            if config_file[file_index] == "$MODULE START$":
                # get new module
                module = Module()

            # when module name is found
            elif config_file[file_index] == "$MODULE NAME START$":
                # record info
                Logger.save_in_log_file("ConfigConverter",
                                        "Reading module name from line " + str(file_index + 2),
                                        False)
                # get module name
                module_name = config_file[file_index+1]
                # set module name
                module.module_name = module_name

            # when module constants are found
            elif config_file[file_index] == "$MODULE CONSTANTS START$":

                # increment file index to definition of first constant element
                file_index = file_index + 1

                # continue reading of constants definition until end of constant section is reached
                while config_file[file_index] != "$MODULE CONSTANTS END$":
                    # record info
                    Logger.save_in_log_file("ConfigConverter",
                                            "Reading module constant from line " + str(file_index + 1),
                                            False)
                    # get line
                    line = config_file[file_index]
                    # extract constant element type, name and value from line of the configuration file
                    constant_element = ConfigConverter.extract_constant_element(line)
                    # append constant element to module constant list
                    module.module_constant_list.append(constant_element)
                    # append constant element to module appendix constant list
                    Module.module_appendix_constant_list.append(constant_element)
                    # increment file index
                    file_index = file_index + 1

            # when operation name is found
            elif config_file[file_index] == "$OPERATION NAME START$":
                # record info
                Logger.save_in_log_file("ConfigConverter",
                                        "Reading operation name from line " + str(file_index + 2),
                                        False)
                # get operation name
                operation_name = config_file[file_index+1]
                # set operation name
                module.operation_name = operation_name

            # when operation input interface is found
            elif config_file[file_index] == "$INPUT INTERFACE START$":

                # increment file index to definition of first input interface element
                file_index = file_index + 1

                # continue reading of input interface definition until end of input interface section is reached
                while config_file[file_index] != "$INPUT INTERFACE END$":
                    # record info
                    Logger.save_in_log_file("ConfigConverter",
                                            "Reading operation input interface from line " + str(file_index + 1),
                                            False)
                    # get line
                    line = config_file[file_index]
                    # extract interface element type and name from line of the configuration file
                    interface_element = ConfigConverter.extract_interface_element(line)
                    # append interface element
                    module.input_interface_list.append(interface_element)
                    # increment file index
                    file_index = file_index + 1

            # when operation output interface is found
            elif config_file[file_index] == "$OUTPUT INTERFACE START$":

                # increment file index to definition of first output interface element
                file_index = file_index + 1

                # continue reading of output interface definition until end of output interface section is reached
                while config_file[file_index] != "$OUTPUT INTERFACE END$":
                    # record info
                    Logger.save_in_log_file("ConfigConverter",
                                            "Reading operation output interface from line " + str(file_index + 1),
                                            False)
                    # get line
                    line = config_file[file_index]
                    # extract interface element type and name from line of the configuration file
                    interface_element = ConfigConverter.extract_interface_element(line)
                    # append interface element
                    module.output_interface_list.append(interface_element)
                    # increment file index
                    file_index = file_index + 1

            # when operation local interface is found
            elif config_file[file_index] == "$LOCAL INTERFACE START$":

                # increment file index to definition of first local interface element
                file_index = file_index + 1

                # continue reading of local interface definition until end of local interface section is reached
                while config_file[file_index] != "$LOCAL INTERFACE END$":
                    # record info
                    Logger.save_in_log_file("ConfigConverter",
                                            "Reading operation local interface from line " + str(file_index + 1),
                                            False)
                    # get line
                    line = config_file[file_index]
                    # extract interface element type and name from line of the configuration file
                    interface_element = ConfigConverter.extract_interface_element(line)
                    # append interface element
                    module.local_interface_list.append(interface_element)
                    # increment file index
                    file_index = file_index + 1

            # when operation body is found
            elif config_file[file_index] == "$OPERATION BODY START$":

                # increment file index to definition of first body element
                file_index = file_index + 1

                # name of invoked operation
                operation_name = ""

                # set indent level
                indent = Module.INDENT_LEVEL_1

                # continue reading of body elements until end of body section is reached
                while config_file[file_index] != "$OPERATION BODY END$":

                    # record info
                    Logger.save_in_log_file("ConfigConverter",
                                            "Reading operation body from line " + str(file_index + 1),
                                            False)

                    # get line
                    line = config_file[file_index]

                    # if body line contains instruction
                    if "$INS " in line:

                        # get instruction
                        instruction = line[ConfigConverter.BODY_DATA_POSITION_IN_CFG:len(line)]
                        # append instruction
                        module.operation_body_list.append(indent + instruction + ";")
                        # append new line command
                        module.operation_body_list.append("$NEW_LINE$")

                    # if body line contains operation call
                    elif "$OPE " in line and "$OPE -end" not in line:

                        # get operation name
                        operation_name = line[ConfigConverter.BODY_DATA_POSITION_IN_CFG:len(line)]
                        # find module to include
                        for operation_module_link in ConfigConverter.operation_module_name_list:
                            # if matching operation name is found
                            if operation_module_link[ConfigConverter.OPERATION_NAME_INDEX] == operation_name:
                                # append header of invoked module
                                module.include_list.append(operation_module_link[ConfigConverter.MODULE_NAME_INDEX] +
                                                           ".h")

                        # get operation input interface element
                        interface_element = []
                        interface_element.insert(Module.DATA_ELEMENT_NAME_INDEX, operation_name + "_input_type")
                        interface_element.insert(Module.DATA_ELEMENT_NAME_INDEX, operation_name + "_input")

                        # append interface element to local interface
                        module.local_interface_list.append(interface_element)

                        # get operation output interface element
                        interface_element = []
                        interface_element.insert(Module.DATA_ELEMENT_NAME_INDEX, operation_name + "_output_type")
                        interface_element.insert(Module.DATA_ELEMENT_NAME_INDEX, operation_name + "_output")

                        # append interface element to local interface
                        module.local_interface_list.append(interface_element)

                    # if body line contains input interface write
                    elif "$INP " in line:

                        # get input interface link
                        input_interface_link = line[ConfigConverter.BODY_DATA_POSITION_IN_CFG:len(line)]
                        # split to input data and pin
                        input_data, input_pin = input_interface_link.split("->")
                        # append operation input interface write to instruction
                        module.operation_body_list.append(indent + operation_name + "_input." + input_pin +
                                                          " = " + input_data + ";")

                        # if that was last input interface write for given operation call
                        if "$INP " not in config_file[file_index+1]:
                            # append operation instruction to instruction
                            module.operation_body_list.append(indent + operation_name + "(&" + operation_name +
                                                              "_input,&" + operation_name + "_output);")

                    # if body line contains output interface read
                    elif "$OUT " in line:

                        # get output interface link
                        output_interface_link = line[ConfigConverter.BODY_DATA_POSITION_IN_CFG:len(line)]
                        # split to output pin and data
                        output_pin, output_data = output_interface_link.split("->")
                        # append operation output interface read to instruction
                        module.operation_body_list.append(indent + output_data + " = " + operation_name +
                                                          "_output." + output_pin + ";")

                    # if body line contains end of operation call
                    elif "$OPE -end" in line:

                        # append new line command
                        module.operation_body_list.append("$NEW_LINE$")

                    # if body line contains conditional IF branch
                    elif "$IFC " in line and "$IFC -end" not in line:

                        # get branch decision
                        branch_decision = line[ConfigConverter.BODY_DATA_POSITION_IN_CFG:len(line)]
                        # append branch decision
                        module.operation_body_list.append(indent + "if(" + branch_decision + ") {")
                        # append new line command
                        module.operation_body_list.append("$NEW_LINE$")
                        # change indent level
                        indent = Module.INDENT_LEVEL_2

                    # if body line contains conditional ELSE IF branch
                    elif "$EIF " in line:

                        # change indent level
                        indent = Module.INDENT_LEVEL_1
                        # append end of previous conditional branch
                        module.operation_body_list.append(indent + "}")
                        # get branch decision
                        branch_decision = line[ConfigConverter.BODY_DATA_POSITION_IN_CFG:len(line)]
                        # append branch decision
                        module.operation_body_list.append(indent + "else if(" + branch_decision + ") {")
                        # append new line command
                        module.operation_body_list.append("$NEW_LINE$")
                        # change indent level
                        indent = Module.INDENT_LEVEL_2

                    # if body line contains ELSE branch
                    elif "$ELS" in line:

                        # change indent level
                        indent = Module.INDENT_LEVEL_1
                        # append end of previous conditional branch
                        module.operation_body_list.append(indent + "}")
                        # append branch
                        module.operation_body_list.append(indent + "else {")
                        # append new line command
                        module.operation_body_list.append("$NEW_LINE$")
                        # change indent level
                        indent = Module.INDENT_LEVEL_2

                    # if body line contains end of conditional branch
                    elif "$IFC -end" in line:

                        # change indent level
                        indent = Module.INDENT_LEVEL_1
                        # append conditional branch end
                        module.operation_body_list.append(indent + "}")
                        # append new line command
                        module.operation_body_list.append("$NEW_LINE$")

                    # increment file index
                    file_index = file_index + 1

            # when module end is found
            elif config_file[file_index] == "$MODULE END$":

                # record info
                Logger.save_in_log_file("ConfigConverter",
                                        "Generating source code file for " + module_name + " module",
                                        False)
                # generate source file code
                module_source = module.generate_module_source()
                # set module source name
                module_source_name = module_name + ".c"
                # save module source to file
                ConfigConverter.save_module_file(module_source_name, module_source)

                # record info
                Logger.save_in_log_file("ConfigConverter",
                                        "Generating header code file for " + module_name + " module",
                                        False)
                # generate header file code
                module_header = module.generate_module_header()
                # set module header name
                module_header_name = module_name + '.h'
                # save module header to file
                ConfigConverter.save_module_file(module_header_name, module_header)

            # increment file index
            file_index = file_index + 1

        # record info
        Logger.save_in_log_file("ConfigConverter",
                                "Generating header code file for " + Module.module_appendix_name + " module",
                                False)
        # generate header file code
        module_header = Module.generate_module_appendix()
        # set module header name
        module_header_name = Module.module_appendix_name + '.h'
        # save module header to file
        ConfigConverter.save_module_file(module_header_name, module_header)

    # Description:
    # This method looks for operation and module name links in the configuration file.
    @staticmethod
    def find_operation_module_name_list(config_file):

        # set file index
        file_index = 0
        # set number of config file lines
        number_of_config_file_lines = len(config_file)

        # module and operation names
        module_name = ""
        operation_name = ""

        # continue conversion until end of the configuration file is reached
        while file_index < number_of_config_file_lines:

            # when module name is found
            if config_file[file_index] == "$MODULE NAME START$":
                # get module name
                module_name = config_file[file_index + 1]

            # when operation name is found
            elif config_file[file_index] == "$OPERATION NAME START$":
                # get operation name
                operation_name = config_file[file_index + 1]

                # set operation - module link
                operation_module_link = []
                operation_module_link.insert(ConfigConverter.OPERATION_NAME_INDEX, operation_name)
                operation_module_link.insert(ConfigConverter.MODULE_NAME_INDEX, module_name)
                # append link to module operation name list
                ConfigConverter.operation_module_name_list.append(operation_module_link)

            # increment file index
            file_index = file_index + 1

    # Description:
    # This method extracts constant element type, name and value from line of the configuration file.
    @staticmethod
    def extract_constant_element(line):

        # get name position within line
        name_position = line.find(" name ")
        # get value position within line
        value_position = line.find(" value ")
        # get constant element type
        constant_element_type = line[ConfigConverter.INTERFACE_TYPE_POSITION_IN_CFG:name_position]
        # get constant element name
        constant_element_name = line[name_position + ConfigConverter.INTERFACE_NAME_POSITION_IN_CFG:value_position]
        # get constant element value
        constant_element_value = line[value_position + ConfigConverter.INTERFACE_VALUE_POSITION_IN_CFG:len(line)]

        # append collected data to constant element
        constant_element = []
        constant_element.insert(Module.DATA_ELEMENT_NAME_INDEX, constant_element_type)
        constant_element.insert(Module.DATA_ELEMENT_NAME_INDEX, constant_element_name)
        constant_element.insert(Module.DATA_ELEMENT_VALUE_INDEX, constant_element_value)

        # return constant element
        return constant_element

    # Description:
    # This method extracts interface element type and name from line of the configuration file.
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
        interface_element.insert(Module.DATA_ELEMENT_NAME_INDEX, interface_element_type)
        interface_element.insert(Module.DATA_ELEMENT_NAME_INDEX, interface_element_name)

        # return interface element
        return interface_element
