#   FILE:           mcg_cgc_config_converter.py
#
#   DESCRIPTION:
#       This module contains definition of ConfigConverter class, which allows to
#       generate source code modules from the configuration file.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           12 JUN 2022
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
    COMPONENT_NAME_POSITION_IN_CFG = 15
    PACKAGE_NAME_POSITION_IN_CFG = 13
    COMPONENT_SOURCE_POSITION_IN_CFG = 17
    PACKAGE_SOURCE_POSITION_IN_CFG = 15
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

        # record info
        Logger.save_in_log_file("ConfigConverter",
                                "Starting conversion of the configuration file into source code", True)

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

            # when new module definition is found
            if ("COMPONENT START" in config_file[file_index]) or ("PACKAGE START" in config_file[file_index]):
                # get new module
                module = Module()
                # set date
                module.generation_date = date

            # when component name is found
            elif "COMPONENT NAME" in config_file[file_index]:
                # record info
                Logger.save_in_log_file("ConfigConverter",
                                        "Reading component name from line " + str(file_index + 1),
                                        False)
                # get line
                line = config_file[file_index]
                # get module name
                module_name = line[ConfigConverter.COMPONENT_NAME_POSITION_IN_CFG:len(line)]
                # set module name
                module.module_name = module_name

            # when package name is found
            elif "PACKAGE NAME" in config_file[file_index]:
                # record info
                Logger.save_in_log_file("ConfigConverter",
                                        "Reading package name from line " + str(file_index + 1),
                                        False)
                # get line
                line = config_file[file_index]
                # get module name
                module_name = line[ConfigConverter.PACKAGE_NAME_POSITION_IN_CFG:len(line)]
                # set module name
                module.module_name = module_name

            # when component comment is found
            elif "COMPONENT SOURCE" in config_file[file_index]:
                # record info
                Logger.save_in_log_file("ConfigConverter",
                                        "Reading component source from line " + str(file_index + 1),
                                        False)
                # get line
                line = config_file[file_index]
                # get comment
                comment = "The module was generated from file " + \
                          line[ConfigConverter.COMPONENT_SOURCE_POSITION_IN_CFG:len(line)]
                # append comment
                module.header_comment_list.append(comment)

            # when package comment is found
            elif "PACKAGE SOURCE" in config_file[file_index]:
                # record info
                Logger.save_in_log_file("ConfigConverter",
                                        "Reading package source from line " + str(file_index + 1),
                                        False)
                # get line
                line = config_file[file_index]
                # get comment
                comment = "The module was generated from file " + \
                          line[ConfigConverter.PACKAGE_SOURCE_POSITION_IN_CFG:len(line)]
                # append comment
                module.header_comment_list.append(comment)

            # when module input interface is found
            elif ("COMPONENT INPUT INTERFACE START" in config_file[file_index]) or \
                    ("PACKAGE INPUT INTERFACE START" in config_file[file_index]):

                # increment file index to definition of first input interface element
                file_index = file_index + 1

                # continue reading of input interface definition until end of input interface section is reached
                while ("COMPONENT INPUT INTERFACE END" not in config_file[file_index]) and \
                        ("PACKAGE INPUT INTERFACE END" not in config_file[file_index]):
                    # record info
                    Logger.save_in_log_file("ConfigConverter",
                                            "Reading module input interface from line " + str(file_index + 1),
                                            False)
                    # get line
                    line = config_file[file_index]
                    # extract interface element type and name from line of the configuration file
                    interface_element = ConfigConverter.extract_interface_element(line)
                    # append interface element
                    module.input_interface_list.append(interface_element)
                    # increment file index
                    file_index = file_index + 1

            # when module output interface is found
            elif ("COMPONENT OUTPUT INTERFACE START" in config_file[file_index]) or \
                    ("PACKAGE OUTPUT INTERFACE START" in config_file[file_index]):

                # increment file index to definition of first output interface element
                file_index = file_index + 1

                # continue reading of output interface definition until end of output interface section is reached
                while ("COMPONENT OUTPUT INTERFACE END" not in config_file[file_index]) and \
                        ("PACKAGE OUTPUT INTERFACE END" not in config_file[file_index]):
                    # record info
                    Logger.save_in_log_file("ConfigConverter",
                                            "Reading module output interface from line " + str(file_index + 1),
                                            False)
                    # get line
                    line = config_file[file_index]
                    # extract interface element type and name from line of the configuration file
                    interface_element = ConfigConverter.extract_interface_element(line)
                    # append interface element
                    module.output_interface_list.append(interface_element)
                    # increment file index
                    file_index = file_index + 1

            # when module local data is found
            elif ("COMPONENT LOCAL DATA START" in config_file[file_index]) or \
                    ("PACKAGE LOCAL DATA START" in config_file[file_index]):

                # increment file index to definition of first local data element
                file_index = file_index + 1

                # continue reading of local data definition until end of local data section is reached
                while ("COMPONENT LOCAL DATA END" not in config_file[file_index]) and \
                        ("PACKAGE LOCAL DATA END" not in config_file[file_index]):
                    # record info
                    Logger.save_in_log_file("ConfigConverter",
                                            "Reading module local data from line " + str(file_index + 1),
                                            False)
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

                    # record info
                    Logger.save_in_log_file("ConfigConverter",
                                            "Reading module body from line " + str(file_index + 1),
                                            False)

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

            # when package body is found
            elif "PACKAGE BODY START" in config_file[file_index]:

                # increment file index to definition of first body element
                file_index = file_index + 1

                # continue reading of body elements until end of body section is reached
                while "PACKAGE BODY END" not in config_file[file_index]:

                    # record info
                    Logger.save_in_log_file("ConfigConverter",
                                            "Reading module body from line " + str(file_index + 1),
                                            False)

                    # get line
                    line = config_file[file_index]

                    # if body line contains module comment
                    if "COM " in line:
                        # get comment
                        comment = "// " + line[ConfigConverter.BODY_DATA_POSITION_IN_CFG:len(line)]
                        # append comment
                        module.module_body_list.append(comment)

                    # otherwise when line contains call of another module
                    elif "INV " in line:

                        # get invoked module output data name
                        invoked_module_output_data_name = line[line.find("INV ")+4:line.find(" = ")]
                        # get invoked module name
                        invoked_module_name = line[line.find(" = ")+3:line.find(" (")]
                        # get invoked module arguments
                        invoked_module_arguments = line[line.find("(")+1:line.find(")")]
                        # split string representation of invoked module arguments into list form
                        invoked_module_argument_list = invoked_module_arguments.split(", ")

                        # find input interface of invoked module
                        invoked_module_input_interface_list = \
                            ConfigConverter.find_module_input_interface(invoked_module_name, config_file)
                        # find structure of each argument, i.e. output interface definition of other modules
                        # which generate input data passed to invoked module
                        invoked_module_argument_interface_list = \
                            ConfigConverter.find_argument_interface(invoked_module_argument_list, config_file)

                        # TO DO:
                        # 1. get instance of input data from input data pointer
                        # 2. remove input interface, local interface, output interface and
                        # collection of output interface section from package source code item
                        # 3. add setup of output data structure

                        # set instance of module input data
                        module.module_body_list.append(invoked_module_name + "_input_type " +
                                                       invoked_module_name + "_input")

                        # set instance of module output data
                        module.module_body_list.append(invoked_module_name + "_output_type " +
                                                       invoked_module_output_data_name)

                        # set module inputs
                        for invoked_module_input_interface in invoked_module_input_interface_list:

                            # get input interface type
                            input_interface_type = invoked_module_input_interface[Module.INTERFACE_ELEMENT_TYPE_INDEX]
                            # get input interface name
                            input_interface_name = invoked_module_input_interface[Module.INTERFACE_ELEMENT_NAME_INDEX]

                            # check interface of each argument
                            for common_index in range(0, len(invoked_module_argument_interface_list)):

                                # get interface of specific argument
                                invoked_module_argument_interface = invoked_module_argument_interface_list[common_index]

                                # check each interface element of given argument
                                for invoked_module_argument_element in invoked_module_argument_interface:

                                    # get potential type match
                                    potential_interface_type_match = \
                                        invoked_module_argument_element[Module.INTERFACE_ELEMENT_TYPE_INDEX]
                                    # get potential name match
                                    potential_interface_name_match = \
                                        invoked_module_argument_element[Module.INTERFACE_ELEMENT_NAME_INDEX]

                                    # check if there is a match between required input data to invoked module
                                    # and data generated by another module
                                    if ((input_interface_type == potential_interface_type_match) and
                                            (input_interface_name == potential_interface_name_match)):

                                        # get argument passed to invoked module
                                        invoked_module_argument = invoked_module_argument_list[common_index]

                                        # if input data comes from main Input Interface
                                        if invoked_module_argument == "Input Interface":
                                            # replace Input Interface with name of input data structure
                                            invoked_module_argument = module_name + "_input"

                                        # set module input
                                        module.module_body_list.append(invoked_module_name + "_input." +
                                                                       input_interface_name + " = " +
                                                                       invoked_module_argument + "." +
                                                                       potential_interface_name_match)

                                        # break "for invoked_module_argument_element in" loop
                                        break

                        # set module invocation
                        module.module_body_list.append(invoked_module_output_data_name + " = " + invoked_module_name +
                                                       "(&" + invoked_module_name + "_input)")

                    # otherwise when line contains collection of output data
                    else:

                        TBD = ""

                    # increment file index
                    file_index = file_index + 1

            # when module end is found
            elif ("COMPONENT END" in config_file[file_index]) or ("PACKAGE END" in config_file[file_index]):

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

    # Description
    # This method looks for definition of module input interface in the configuration file.
    @staticmethod
    def find_module_input_interface(module_name, config_file):

        # module input interface list
        module_input_interface_list = []
        # module definition found in the configuration file
        found_module_definition = False

        # search for input interface definition of given module in the configuration file
        for file_index in range(0, len(config_file)):

            # if given module was found
            if (("COMPONENT NAME " in config_file[file_index]) or
                ("PACKAGE NAME " in config_file[file_index])) and \
                    (module_name in config_file[file_index]):
                # change flag
                found_module_definition = True

            # if input interface definition of given module was found
            elif (("COMPONENT INPUT INTERFACE START" in config_file[file_index]) or
                  ("PACKAGE INPUT INTERFACE START" in config_file[file_index])) and \
                    found_module_definition:

                # increment file index to definition of first input interface element
                file_index = file_index + 1

                # continue reading of input interface definition until end of input interface section is reached
                while ("COMPONENT INPUT INTERFACE END" not in config_file[file_index]) and \
                        ("PACKAGE INPUT INTERFACE END" not in config_file[file_index]):

                    # get line
                    line = config_file[file_index]
                    # extract interface element type and name from line of the configuration file
                    interface_element = ConfigConverter.extract_interface_element(line)
                    # append interface element
                    module_input_interface_list.append(interface_element)
                    # increment file index
                    file_index = file_index + 1

                # break "for file_index in" loop
                break

        # return module input interface list
        return module_input_interface_list

    # Description
    # This method looks for definition of module output interface in the configuration file.
    @staticmethod
    def find_module_output_interface(module_name, config_file):

        # module output interface list
        module_output_interface_list = []
        # module definition found in the configuration file
        found_module_definition = False

        # search for output interface definition of given module in the configuration file
        for file_index in range(0, len(config_file)):

            # if given module was found
            if (("COMPONENT NAME " in config_file[file_index]) or
                ("PACKAGE NAME " in config_file[file_index])) and \
                    (module_name in config_file[file_index]):
                # change flag
                found_module_definition = True

            # if output interface definition of given module was found
            elif (("COMPONENT OUTPUT INTERFACE START" in config_file[file_index]) or
                  ("PACKAGE OUTPUT INTERFACE START" in config_file[file_index])) and \
                    found_module_definition:

                # increment file index to definition of first output interface element
                file_index = file_index + 1

                # continue reading of output interface definition until end of output interface section is reached
                while ("COMPONENT OUTPUT INTERFACE END" not in config_file[file_index]) and \
                        ("PACKAGE OUTPUT INTERFACE END" not in config_file[file_index]):
                    # get line
                    line = config_file[file_index]
                    # extract interface element type and name from line of the configuration file
                    interface_element = ConfigConverter.extract_interface_element(line)
                    # append interface element
                    module_output_interface_list.append(interface_element)
                    # increment file index
                    file_index = file_index + 1

                # break "for file_index in" loop
                break

        # return module output interface list
        return module_output_interface_list

    # Description
    # This method looks for interface details of each argument element from the given list.
    @staticmethod
    def find_argument_interface(argument_list, config_file):

        # argument interface list
        argument_interface_list = []

        # for given argument element find its interface details
        for argument in argument_list:

            # if Input Interface is argument
            if argument == "Input Interface":

                # check the configuration file for package name
                for file_index in range(0, len(config_file)):

                    # when package name is found
                    if "PACKAGE NAME " in config_file[file_index]:

                        # get line
                        line = config_file[file_index]
                        # get module name
                        module_name = line[ConfigConverter.PACKAGE_NAME_POSITION_IN_CFG:len(line)]
                        # find interface details
                        module_interface_list = ConfigConverter.find_module_input_interface(module_name, config_file)
                        # append interface to argument interface list
                        argument_interface_list.append(module_interface_list)
                        # break "for file_index in" loop
                        break

            # otherwise look for data generated by other modules
            else:

                # look for specific string where argument is output of another module
                keyword = "INV " + argument + " = "

                # check the configuration file for above keyword
                for file_index in range(0, len(config_file)):

                    # if given keyword is found in the configuration file
                    if keyword in config_file[file_index]:

                        # get line
                        line = config_file[file_index]
                        # get module name
                        module_name = line[line.find(" = ") + 3:line.find(" (")]
                        # find interface details
                        module_interface_list = ConfigConverter.find_module_output_interface(module_name, config_file)
                        # append interface to argument interface list
                        argument_interface_list.append(module_interface_list)
                        # break "for file_index in" loop
                        break

        # return argument interface list
        return argument_interface_list
