#   FILE:           mcg_cgc_module.py
#
#   DESCRIPTION:
#       This module contains definition of Module class, which represents module
#       source code and module header to be generated from the configuration file.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           26 OCT 2022
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
        self.generation_date = ""
        self.header_comment_list = []
        self.include_list = []
        self.input_interface_list = []
        self.output_interface_list = []
        self.local_data_list = []
        self.module_body_list = []

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

        # append additional includes
        for include in self.include_list:
            module = module + "#include \"" + include + "\"\n"

        # set separator line
        module = module + "\n"

        # ********** FUNCTION HEADER ********** #

        # set function comment
        module = module + "// This is definition of module function\n"

        # set return type
        module = module + self.module_name + "_output_type "
        # set function name
        module = module + self.module_name
        # set function argument
        module = module + "(" + self.module_name + "_input_type *" + self.module_name + "_input) {\n\n"

        # ********** FUNCTION INTERFACE ********** #

        # set input interface comment
        module = module + self.indent + "// Input Interface\n"

        # append input interface
        for input_interface in self.input_interface_list:
            module = module + self.indent + input_interface[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + input_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + " = " \
                     + self.module_name + "_input->" + input_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + "\n"

        # set local data comment
        module = module + self.indent + "// Local Data\n"

        # append local data
        for local_data in self.local_data_list:
            module = module + self.indent + local_data[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + local_data[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + "\n"

        # set output interface comment
        module = module + self.indent + "// Output Interface\n"

        # append output interface
        for output_interface in self.output_interface_list:
            module = module + self.indent + output_interface[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + output_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + self.indent + self.module_name + "_output_type " + self.module_name + "_output;\n"
        module = module + "\n"

        # ********** FUNCTION BODY ********** #

        # distinguish if first line of function body was added or not to module content
        first_body_line_added = False

        # append function body
        for module_body in self.module_body_list:

            # if first line was added and current line contains comment
            if first_body_line_added and "// " in module_body:
                # add new line separation before comment
                module = module + "\n" + self.indent + module_body + ";\n"
            else:
                # add new body line
                module = module + self.indent + module_body + ";\n"

            # first body line was added
            first_body_line_added = True

        module = module + "\n"

        # ********** COLLECT OUTPUT DATA ********** #

        # set comment
        module = module + self.indent + "// Collect output data\n"

        # collect output data into output data structure
        for output_interface in self.output_interface_list:
            module = module + self.indent + self.module_name + "_output." + \
                     output_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + " = " + \
                     output_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + "\n"

        # set comment
        module = module + self.indent + "// Return output data\n"

        # set return
        module = module + self.indent + "return " + self.module_name + "_output;\n"

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
        module = module + "} " + self.module_name + "_input_type;\n\n"

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
        module = module + "} " + self.module_name + "_output_type;\n\n"

        # ********** FUNCTION PROTOTYPE ********** #

        # set function comment
        module = module + "// This is prototype of module function\n"

        # set return type
        module = module + self.module_name + "_output_type "
        # set function name
        module = module + self.module_name
        # set function argument
        module = module + "(" + self.module_name + "_input_type *" + self.module_name + "_input);\n\n"

        # ********** HEADER GUARD END ********** #

        # set header guard end
        module = module + "#endif " + "// " + self.module_name + "_H_\n\n"

        # ********** MODULE END ********** #

        # set module footer
        module = module + "/*\n" + " * END OF MODULE\n" + " */\n"

        # return string representation
        return module
