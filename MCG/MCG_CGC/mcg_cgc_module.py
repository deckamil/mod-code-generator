#   FILE:           mcg_cgc_module.py
#
#   DESCRIPTION:
#       This module contains definition of Module class, which represents module
#       source code and module header to be generated from the configuration file.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           8 MAY 2022
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
        self.filename = ""
        self.generation_date = ""
        self.header_comment_list = []
        self.input_interface_list = []
        self.output_interface_list = []
        self.local_data_list = []
        self.module_body_list = []

    # Description:
    # This method returns string representation of module source file.
    def generate_module_source(self):

        # ********** HEADER ********** #

        # set module header
        module = "/*\n" + " *   Generated with Mod Code Generator (MCG) Code Generator Component (CGC)\n" + " *   on "
        # set module date
        module = module + self.generation_date + "\n"

        # set module comment
        module = module + " *\n"

        # append comments to module body
        for header_comment in self.header_comment_list:
            module = module + " *   " + header_comment + "\n"

        # set end of module header
        module = module + " */\n\n"

        # ********** INCLUDES ********** #

        # set includes
        module = module + "#include \"" + self.filename + ".h\"\n"
        module = module + "#include \"basic_data_types.h\"\n\n"

        # ********** FUNCTION BEGINNING ********** #

        # set return type
        module = module + self.filename + "_output_type "
        # set function name
        module = module + self.filename
        # set function argument
        module = module + "(" + self.filename + "_input_type *" + self.filename + "_input){\n\n"

        # ********** FUNCTION INTERFACE ********** #

        # set input interface comment
        module = module + self.indent + "// Input Interface\n"

        # set input interface
        for input_interface in self.input_interface_list:
            module = module + self.indent + input_interface[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + input_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + " = " \
                     + self.filename + "_input->" + input_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + "\n"

        # set local data comment
        module = module + self.indent + "// Local Data\n"

        # set local data
        for local_data in self.local_data_list:
            module = module + self.indent + local_data[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + local_data[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + "\n"

        # set output interface comment
        module = module + self.indent + "// Output Interface\n"

        # set output interface
        for output_interface in self.output_interface_list:
            module = module + self.indent + output_interface[Module.INTERFACE_ELEMENT_TYPE_INDEX] + " " \
                     + output_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + self.indent + self.filename + "_output_type " + self.filename + "_output;\n"
        module = module + "\n"




        # ********** COLLECT OUTPUT DATA ********** #

        # set comment
        module = module + self.indent + "// Collect output data\n"

        # collect output data into output data structure
        for output_interface in self.output_interface_list:
            module = module + self.indent + self.filename + "_output->" + \
                     output_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + " = " + \
                     output_interface[Module.INTERFACE_ELEMENT_NAME_INDEX] + ";\n"

        module = module + "\n"

        # ********** FUNCTION END ********** #

        module = module + "}\n\n"

        # ********** FOOTER ********** #

        # set module footer
        module = module + "/*\n" + " * END OF MODULE\n" + " */\n"

        # return string representation
        return module

    # Description
    # This method returns string representation of module header file
    def generate_module_header(self):

        # set module header
        module = "/*\n" + " *   Generated with Mod Code Generator (MCG) Code Generator Component (CGC)\n" + " *   on "
        # set module date
        module = module + self.generation_date + "\n"
