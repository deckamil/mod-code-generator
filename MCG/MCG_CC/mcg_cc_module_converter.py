#   FILE:           mcg_cc_module_converter.py
#
#   DESCRIPTION:
#       This module contains definition of ModuleConverter class, which is responsible
#       for conversion of module content into configuration file format.
#
#   COPYRIGHT:      Copyright (C) 2021-2024 Kamil Deć github.com/deckamil
#   DATE:           27 JAN 2024
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
from mcg_cc_activity_node import ActivityNode
from mcg_cc_file_finder import FileFinder
from mcg_cc_file_reader import FileReader
from mcg_cc_logger import Logger


# Description:
# This class allows to convert module content into configuration file format.
class ModuleConverter(object):

    # initialize class data
    configuration_file_disk = ""
    configuration_file_path = ""

    # Description:
    # This is class constructor.
    def __init__(self, file_finder_list, file_reader_list):

        # initialize object data
        self.module_name = file_finder_list[FileFinder.MODULE_NAME_INDEX]
        self.operation_name = file_reader_list[FileReader.OPERATION_NAME_INDEX]
        self.constant_list = file_reader_list[FileReader.CONSTANT_LIST_INDEX]
        self.input_interface_list = file_reader_list[FileReader.INPUT_INTERFACE_LIST_INDEX]
        self.output_interface_list = file_reader_list[FileReader.OUTPUT_INTERFACE_LIST_INDEX]
        self.local_interface_list = file_reader_list[FileReader.LOCAL_INTERFACE_LIST_INDEX]
        self.diagram_collection = file_reader_list[FileReader.DIAGRAM_COLLECTION_INDEX]
        self.condition_collection_list = file_reader_list[FileReader.CONDITION_COLLECTION_LIST_INDEX]
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
    # This method appends new line to configuration file.
    def append_to_configuration_file(self, configuration_file_line, save_in_log_file):

        # if there is demand to save configuration file line in log file
        if save_in_log_file:
            Logger.save_in_log_file("ModuleConverter", "Have converted to " + str(configuration_file_line) + " line", False)

        # append configuration file line to configuration file
        self.configuration_file.append(configuration_file_line)

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
    # This method converts module name into configuration file.
    def convert_module_name(self):

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting module name into configuration file", False)

        # append start marker of module name section to configuration file
        self.append_to_configuration_file("$MODULE NAME START$", False)
        # append module name to configuration file
        self.append_to_configuration_file(self.module_name, True)
        # append end marker of module name section to configuration file
        self.append_to_configuration_file("$MODULE NAME END$", False)

    # Description
    # This method converts module constants into configuration file.
    def convert_module_constants(self):

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting module constants into configuration file", False)

        # append start marker of module constant section to configuration file
        self.append_to_configuration_file("$MODULE CONSTANTS START$", False)

        # append constant details to configuration file
        for constant_element in self.constant_list:
            # get constant element type
            constant_element_type = constant_element[FileReader.DATA_ELEMENT_TYPE_INDEX]
            # get constant element name
            constant_element_name = constant_element[FileReader.DATA_ELEMENT_NAME_INDEX]
            # get constant element value
            constant_element_value = constant_element[FileReader.DATA_ELEMENT_VALUE_INDEX]
            # get configuration file line
            configuration_file_line = "type " + str(constant_element_type) + " name " + str(constant_element_name) + \
                                      " value " + str(constant_element_value)
            # append configuration file line to configuration file
            self.append_to_configuration_file(configuration_file_line, True)

        # append end marker of module constant section to configuration file
        self.append_to_configuration_file("$MODULE CONSTANTS END$", False)

    # Description:
    # This method converts operation name into configuration file.
    def convert_operation_name(self):

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting operation name into configuration file", False)

        # append start marker of operation name section to configuration file
        self.append_to_configuration_file("$OPERATION NAME START$", False)
        # append operation name to configuration file
        self.append_to_configuration_file(self.operation_name, True)
        # append end marker of operation name section to configuration file
        self.append_to_configuration_file("$OPERATION NAME END$", False)

    # Description:
    # This method converts specific interface type into configuration file.
    def convert_specific_interface(self, interface_element_list):

        # append interface details to configuration file
        for interface_element in interface_element_list:
            # get interface element type
            interface_element_type = interface_element[FileReader.DATA_ELEMENT_TYPE_INDEX]
            # get interface element name
            interface_element_name = interface_element[FileReader.DATA_ELEMENT_NAME_INDEX]
            # get configuration file line
            configuration_file_line = "type " + str(interface_element_type) + " name " + str(interface_element_name)
            # append configuration file line to configuration file
            self.append_to_configuration_file(configuration_file_line, True)

    # Description:
    # This method converts operation input interface, output interface and local interface elements
    # into configuration file.
    def convert_operation_interfaces(self):

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting operation input interface into configuration file", False)

        # append start marker of input interface section to configuration file
        self.append_to_configuration_file("$INPUT INTERFACE START$", False)
        # append input interface details to configuration file
        self.convert_specific_interface(self.input_interface_list)
        # append end marker of input interface section to configuration file
        self.append_to_configuration_file("$INPUT INTERFACE END$", False)

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting operation output interface into configuration file", False)

        # append start marker of output interface section to configuration file
        self.append_to_configuration_file("$OUTPUT INTERFACE START$", False)
        # append output interface details to configuration file
        self.convert_specific_interface(self.output_interface_list)
        # append end marker of output interface section to configuration file
        self.append_to_configuration_file("$OUTPUT INTERFACE END$", False)

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting operation local interface into configuration file", False)

        # append start marker of local interface section to configuration file
        self.append_to_configuration_file("$LOCAL INTERFACE START$", False)
        # append local interface details to configuration file
        self.convert_specific_interface(self.local_interface_list)
        # append end marker of local interface section to configuration file
        self.append_to_configuration_file("$LOCAL INTERFACE END$", False)

    # Description:
    # This method converts operation node from activity diagram into configuration file.
    def convert_operation_node(self, sorted_node):

        # set operation invocation to configuration file line
        configuration_file_line = str("$OPE ") + str(sorted_node.interaction)
        # append configuration file line to configuration file
        self.append_to_configuration_file(configuration_file_line, True)

        # append input data links
        for input_link in sorted_node.input_data_list:
            # set input link to configuration file line
            configuration_file_line = str("$INP ") + str(input_link[ActivityNode.DATA_NAME_INDEX]) + str("->") + \
                                      str(input_link[ActivityNode.PIN_NAME_INDEX])
            # append configuration file line to configuration file
            self.append_to_configuration_file(configuration_file_line, True)

        # append output data links
        for output_link in sorted_node.output_data_list:
            # set output link to configuration file line
            configuration_file_line = str("$OUT ") + str(output_link[ActivityNode.PIN_NAME_INDEX]) + str("->") + \
                                      str(output_link[ActivityNode.DATA_NAME_INDEX])
            # append configuration file line to configuration file
            self.append_to_configuration_file(configuration_file_line, True)

        # append ending marker for operation
        self.append_to_configuration_file("$OPE -end", True)

    # Description:
    # This method converts specific action node from activity diagram with n-argument operator into configuration file.
    def convert_specific_action_node_arity_n(self, sorted_node, operator):

        # get output link
        output_link = sorted_node.output_data_list[0]
        # set beginning of action interaction to configuration file line
        configuration_file_line = str("$INS ") + str(output_link[ActivityNode.DATA_NAME_INDEX]) + str(" = ")

        # search for all input data elements of sorted node and put them into configuration file line
        for input_link in sorted_node.input_data_list:
            # get input data name
            input_data_name = input_link[ActivityNode.DATA_NAME_INDEX]
            # append input data element to configuration file line
            configuration_file_line = configuration_file_line + str(input_data_name)
            # append operator to configuration file line
            configuration_file_line = configuration_file_line + str(" ") + str(operator) + str(" ")

        # remove spare operator and whitespace
        configuration_file_line = configuration_file_line[0:len(configuration_file_line) - 3]
        # append configuration file line to configuration file
        self.append_to_configuration_file(configuration_file_line, True)

    # Description:
    # This method converts specific action node from activity diagram with 1-argument operator into configuration file.
    def convert_specific_action_node_arity_1(self, sorted_node, operator):

        # get input link
        input_link = sorted_node.input_data_list[0]
        # get output link
        output_link = sorted_node.output_data_list[0]
        # set beginning of action interaction to configuration file line
        configuration_file_line = str("$INS ") + str(output_link[ActivityNode.DATA_NAME_INDEX]) + str(" = ") + \
                                  str(operator) + str(input_link[ActivityNode.DATA_NAME_INDEX])

        # append configuration file line to configuration file
        self.append_to_configuration_file(configuration_file_line, True)

    # Description:
    # This method converts action node from activity diagram into configuration file.
    def convert_action_node(self, sorted_node):

        # depending on the type of action, covert node into configuration file.

        # arithmetic operators
        if sorted_node.interaction[0:3] == "ADD":
            self.convert_specific_action_node_arity_n(sorted_node, "+")

        elif sorted_node.interaction[0:3] == "SUB":
            self.convert_specific_action_node_arity_n(sorted_node, "-")

        elif sorted_node.interaction[0:3] == "MUL":
            self.convert_specific_action_node_arity_n(sorted_node, "*")

        elif sorted_node.interaction[0:3] == "DIV":
            self.convert_specific_action_node_arity_n(sorted_node, "/")

        # logical operators
        elif sorted_node.interaction[0:3] == "AND":
            self.convert_specific_action_node_arity_n(sorted_node, "&&")

        elif sorted_node.interaction[0:2] == "OR":
            self.convert_specific_action_node_arity_n(sorted_node, "||")

        elif sorted_node.interaction[0:3] == "NOT":
            self.convert_specific_action_node_arity_1(sorted_node, "!")

        # bitwise operators
        elif sorted_node.interaction[0:4] == "BAND":
            self.convert_specific_action_node_arity_n(sorted_node, "&")

        elif sorted_node.interaction[0:3] == "BOR":
            self.convert_specific_action_node_arity_n(sorted_node, "|")

        elif sorted_node.interaction[0:4] == "BXOR":
            self.convert_specific_action_node_arity_n(sorted_node, "^")

        elif sorted_node.interaction[0:4] == "BNOT":
            self.convert_specific_action_node_arity_1(sorted_node, "~")

        elif sorted_node.interaction[0:3] == "BLS":
            self.convert_specific_action_node_arity_n(sorted_node, "<<")

        elif sorted_node.interaction[0:3] == "BRS":
            self.convert_specific_action_node_arity_n(sorted_node, ">>")

        # relational operators
        elif sorted_node.interaction[0:2] == "EQ":
            self.convert_specific_action_node_arity_n(sorted_node, "==")

        elif sorted_node.interaction[0:2] == "NE":
            self.convert_specific_action_node_arity_n(sorted_node, "!=")

        elif sorted_node.interaction[0:2] == "GT":
            self.convert_specific_action_node_arity_n(sorted_node, ">")

        elif sorted_node.interaction[0:2] == "LT":
            self.convert_specific_action_node_arity_n(sorted_node, "<")

        elif sorted_node.interaction[0:2] == "GE":
            self.convert_specific_action_node_arity_n(sorted_node, ">=")

        elif sorted_node.interaction[0:2] == "LE":
            self.convert_specific_action_node_arity_n(sorted_node, "<=")

    # Description:
    # This method converts data node into configuration file.
    def convert_data_node(self, sorted_node):

        # get input link
        input_link = sorted_node.input_data_list[0]
        # get input data name
        input_data_name = input_link[ActivityNode.DATA_NAME_INDEX]
        # get output link
        output_link = sorted_node.output_data_list[0]
        # get output data name
        output_data_name = output_link[ActivityNode.DATA_NAME_INDEX]
        # get configuration file line
        configuration_file_line = str("$INS ") + str(output_data_name) + " = " + str(input_data_name)
        # append configuration file line to configuration file
        self.append_to_configuration_file(configuration_file_line, True)

    # Description:
    # This method selects conversion for ordinary nodes.
    def convert_ordinary_node(self, sorted_node):

        # if node is operation type
        if sorted_node.type == ActivityNode.OPERATION:
            # convert operation node
            self.convert_operation_node(sorted_node)
        # if node is action type
        elif sorted_node.type == ActivityNode.ACTION:
            # convert action node
            self.convert_action_node(sorted_node)
        # if node is data type
        elif sorted_node.type == ActivityNode.DATA:
            # convert data node
            self.convert_data_node(sorted_node)

    # Description
    # This method converts string that represents clause decision.
    @staticmethod
    def convert_clause_decision(clause_decision):

        # remove clause level number with square bracket
        clause_level_bracket_position = clause_decision.find("]")
        clause_decision = clause_decision[clause_level_bracket_position + 1:len(clause_decision)]
        # remove spaces at the beginning and at the end of clause decision
        clause_decision = clause_decision.strip()
        # converts logical operators
        clause_decision = clause_decision.replace(" AND ", " && ")
        clause_decision = clause_decision.replace(" OR ", " || ")
        clause_decision = clause_decision.replace(" NOT ", " !")
        clause_decision = clause_decision.replace(" (NOT ", " (!")

        return clause_decision

    # Description:
    # This method converts special node that represents condition.
    def convert_condition_node(self, condition_node):

        # find condition collection for given condition node
        for condition_collection in self.condition_collection_list:
            # if uid identifier is the same
            if condition_collection.uid == condition_node.uid:
                # get clause collection list for given condition collection
                clause_collection_list = condition_collection.collection_list

                # convert decision of first clause section
                clause_decision = self.convert_clause_decision(clause_collection_list[0].decision)
                # get configuration file line
                configuration_file_line = str("$IFC ") + str(clause_decision)
                # append configuration file line to configuration file
                self.append_to_configuration_file(configuration_file_line, True)
                # convert ordinary nodes for first clause
                for sorted_node in clause_collection_list[0].sorted_node_list:
                    self.convert_ordinary_node(sorted_node)

                # when else if section is expected (condition has more clauses than only simple if and else)
                if len(clause_collection_list) > 2:
                    # get sublist for section with else if clauses
                    elseif_clause_collection_sublist = clause_collection_list[1:len(clause_collection_list)-1]
                    # for each clause in that section
                    for clause in elseif_clause_collection_sublist:
                        # convert clause decision
                        clause_decision = self.convert_clause_decision(clause.decision)
                        # get configuration file line
                        configuration_file_line = str("$EIF ") + str(clause_decision)
                        # append configuration file line to configuration file
                        self.append_to_configuration_file(configuration_file_line, True)
                        # convert ordinary nodes for clause
                        for sorted_node in clause.sorted_node_list:
                            self.convert_ordinary_node(sorted_node)

                # append else marker of last clause section
                self.append_to_configuration_file("$ELS", True)
                # convert ordinary nodes for last clause
                for sorted_node in clause_collection_list[-1].sorted_node_list:
                    self.convert_ordinary_node(sorted_node)

                # append ending marker for last clause section
                self.append_to_configuration_file("$IFC -end", True)

    # Description:
    # This method converts operation body into configuration file.
    def convert_operation_body(self):

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting operation body into configuration file", False)

        # append start marker of module body section to configuration file
        self.append_to_configuration_file("$OPERATION BODY START$", False)

        # repeat for all sorted nodes from diagram collection
        for sorted_node in self.diagram_collection.sorted_node_list:

            # if given node represents condition
            if sorted_node.type == ActivityNode.CONDITION:
                # converts condition node
                self.convert_condition_node(sorted_node)
            else:
                # convert ordinary node
                self.convert_ordinary_node(sorted_node)

        # append end marker of module body section to configuration file
        self.append_to_configuration_file("$OPERATION BODY END$", False)

    # Description:
    # This method is responsible for conversion of module content into configuration file format.
    def convert_module(self):

        # record info
        Logger.save_in_log_file("ModuleConverter", "Converting module content into configuration file", True)

        # append start marker of new module section to configuration file
        self.append_to_configuration_file("$MODULE START$", False)

        # convert module name into configuration file.
        self.convert_module_name()

        # convert module constants into configuration file.
        self.convert_module_constants()

        # convert operation name into configuration file.
        self.convert_operation_name()

        # convert operation interfaces into configuration file
        self.convert_operation_interfaces()

        # convert operation body into configuration file.
        self.convert_operation_body()

        # append end marker of new module section to configuration file
        self.append_to_configuration_file("$MODULE END$", False)

        # record info
        Logger.save_in_log_file("ModuleConverter", "Saving conversion results into configuration file", False)

        # save configuration file
        self.save_in_configuration_file()
