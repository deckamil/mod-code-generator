#   FILE:           mcg_cgc_module.py
#
#   DESCRIPTION:
#       This module contains definition of Module class, which represents module
#       source code and module header to be generated from the configuration file.
#
#   COPYRIGHT:      Copyright (C) 2022-2023 Kamil Deć github.com/deckamil
#   DATE:           29 MAY 2023
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


# Description:
# This class represents module source code and module header to be generated from the configuration file.
class Module(object):

    # This parameter defines index of interface element type in list which defines interface element
    INTERFACE_ELEMENT_TYPE_INDEX = 0

    # This parameter defines index of interface element name in list which defines interface element
    INTERFACE_ELEMENT_NAME_INDEX = 1

    # Indent used in module definition
    indent = "    "

    # Description:
    # This is class constructor.
    def __init__(self):
        # initialize object data
        self.module_name = ""
        self.operation_name = ""
        self.generation_date = ""
        self.header_comment_list = []
        self.include_list = []
        self.input_interface_list = []
        self.output_interface_list = []
        self.local_interface_list = []
        self.operation_body_list = []

    # Description:
    # This method removes duplicate elements from interface list.
    @staticmethod
    def remove_duplicate_interface_elements(interface_element_list):

        # temporary interface list
        tmp_interface_element_list = []

        # for each interface element
        for interface_element in interface_element_list:
            # merge interface element type and name
            tmp_interface_element = interface_element[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " + \
                                    interface_element[Module.INTERFACE_ELEMENT_NAME_INDEX]
            # append temporary interface element to the list
            tmp_interface_element_list.append(tmp_interface_element)

        # remove duplicates from the list
        tmp_interface_element_list = list(dict.fromkeys(tmp_interface_element_list))

        # clear interface element list
        interface_element_list = []

        # for each temporary interface element
        for tmp_interface_element in tmp_interface_element_list:
            # split temporary interface element to interface element type and name
            interface_element_type, interface_element_name = tmp_interface_element.split(" ")
            # append collected data to interface element
            interface_element = []
            interface_element.insert(Module.INTERFACE_ELEMENT_TYPE_INDEX, interface_element_type)
            interface_element.insert(Module.INTERFACE_ELEMENT_NAME_INDEX, interface_element_name)
            # append interface element to the list
            interface_element_list.append(interface_element)

        # return interface element list
        return interface_element_list

    # Description:
    # This method returns string representation of module source file.
    def generate_module_source(self):

        # ********** MODULE HEADER ********** #

        # set module header
        module = "/*\n" + " *   Generated with Mod Code Generator (MCG) Code Generator Component (CGC)\n" + " *   on "
        # set module date
        module = module + self.generation_date + "\n"

        # set module comment
        module = module + " *\n"

        # set generic comment
        module = module + " *   " + "This is source file of " + self.module_name + " module.\n"

        # append header comments
        for header_comment in self.header_comment_list:
            module = module + " *   " + header_comment + "\n"

        # set end of module header
        module = module + " */\n\n"

        # ********** MODULE INCLUDES ********** #

        # set includes
        module = module + "#include \"" + self.module_name + ".h\"\n"
        module = module + "#include \"basic_data_types.h\"\n"

        # remove duplicates from include list
        self.include_list = list(dict.fromkeys(self.include_list))

        # append additional includes
        for include in self.include_list:
            module = module + "#include \"" + include + "\"\n"

        # set separator line
        module = module + "\n"

        # ********** FUNCTION HEADER ********** #

        # set function comment
        module = module + "// This is definition of module function\n"

        # set return type
        module = module + "void "
        # set function name
        module = module + self.operation_name
        # set function argument
        module = module + "(" + \
                 self.operation_name + "_input_type *" + self.operation_name + "_input," + \
                 self.operation_name + "_output_type *" + self.operation_name + "_output) {\n\n"

        # ********** FUNCTION INTERFACE ********** #

        # set input interface comment
        module = module + self.indent + "// Input interface\n"

        # remove duplicate from interface list
        self.input_interface_list = Module.remove_duplicate_interface_elements(self.input_interface_list)

        # append input interface
        for input_interface in self.input_interface_list:
            module = module + self.indent + input_interface[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + input_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + " = " \
                     + self.operation_name + "_input->" + input_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + "\n"

        # set local data comment
        module = module + self.indent + "// Local interface\n"

        # remove duplicate from interface list
        self.local_interface_list = Module.remove_duplicate_interface_elements(self.local_interface_list)

        # append local interface
        for local_interface in self.local_interface_list:
            module = module + self.indent + local_interface[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + local_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + "\n"

        # set output interface comment
        module = module + self.indent + "// Output interface\n"

        # remove duplicate from interface list
        self.output_interface_list = Module.remove_duplicate_interface_elements(self.output_interface_list)

        # append output interface
        for output_interface in self.output_interface_list:
            module = module + self.indent + output_interface[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + output_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + "\n"

        # ********** FUNCTION BODY ********** #

        # set function body comment
        module = module + self.indent + "// Function body\n"

        # append function body
        for operation_body in self.operation_body_list:

            # if new line command is found
            if operation_body == "$NEW_LINE$":
                # add new line separation
                module = module + "\n"
            else:
                # add new body line
                module = module + self.indent + operation_body + ";\n"

        # ********** COLLECT OUTPUT DATA ********** #

        # set comment
        module = module + self.indent + "// Collect output data\n"

        # collect output data into output data structure
        for output_interface in self.output_interface_list:
            module = module + self.indent + self.operation_name + "_output->" + \
                     output_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + " = " + \
                     output_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + "\n"

        # ********** FUNCTION END ********** #

        module = module + "}\n\n"

        # ********** MODULE END ********** #

        # set module footer
        module = module + "/*\n" + " * END OF MODULE\n" + " */\n"

        # return string representation
        return module

    # Description
    # This method returns string representation of module header file
    def generate_module_header(self):

        # ********** MODULE HEADER ********** #

        # set module header
        module = "/*\n" + " *   Generated with Mod Code Generator (MCG) Code Generator Component (CGC)\n" + " *   on "
        # set module date
        module = module + self.generation_date + "\n"

        # set module comment
        module = module + " *\n"

        # set generic comment
        module = module + " *   " + "This is header file of " + self.module_name + " module.\n"

        # append header comments
        for header_comment in self.header_comment_list:
            module = module + " *   " + header_comment + "\n"

        # set end of module header
        module = module + " */\n\n"

        # ********** HEADER GUARD ********** #

        # set header guard
        module = module + "#ifndef " + self.module_name + "_H_\n"
        module = module + "#define " + self.module_name + "_H_\n\n"

        # ********** MODULE INCLUDES ********** #

        # set includes
        module = module + "#include \"basic_data_types.h\"\n\n"

        # ********** INPUT INTERFACE TYPE ********** #

        # set input interface type comment
        module = module + "// This is input interface type of module function\n"

        # set input interface struct definition
        module = module + "typedef struct {\n"

        # append input interface
        for input_interface in self.input_interface_list:
            module = module + self.indent + input_interface[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + input_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        # set input interface type name
        module = module + "} " + self.operation_name + "_input_type;\n\n"

        # ********** OUTPUT INTERFACE TYPE ********** #

        # set output interface type comment
        module = module + "// This is output interface type of module function\n"

        # set output interface struct definition
        module = module + "typedef struct {\n"

        # append output interface
        for output_interface in self.output_interface_list:
            module = module + self.indent + output_interface[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + output_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        # set output interface type name
        module = module + "} " + self.operation_name + "_output_type;\n\n"

        # ********** FUNCTION PROTOTYPE ********** #

        # set function comment
        module = module + "// This is prototype of module function\n"

        # set return type
        module = module + "void "
        # set function name
        module = module + self.operation_name
        # set function argument
        module = module + "(" + \
                 self.operation_name + "_input_type *" + self.operation_name + "_input," + \
                 self.operation_name + "_output_type *" + self.operation_name + "_output);\n\n"

        # ********** HEADER GUARD END ********** #

        # set header guard end
        module = module + "#endif " + "// " + self.module_name + "_H_\n\n"

        # ********** MODULE END ********** #

        # set module footer
        module = module + "/*\n" + " * END OF MODULE\n" + " */\n"

        # return string representation
        return module
