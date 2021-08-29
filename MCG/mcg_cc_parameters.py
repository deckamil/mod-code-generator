#   FILE:           mcg_cc_parameters.py
#
#   DESCRIPTION:
#       This module contains additional parameters, which are used across other
#       modules of Mod Code Generator (MCG) Converter Component (CC).
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           29 AUG 2021
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


# This parameter for production version of Mod Code Generator (MCG) Converter Component (CC)
# should be set to false, otherwise it allows to display additional information in console
# during run of Mod Code Generator (MCG) Converter Component (CC)
MCG_CC_TEST_RUN = True

# This parameter express length of model file names, i.e. names of .exml files, which are used
# to store and save model data; an example of model file name: b17d413f-fa9f-4e26-8e8c-9485d9c9ed3d.exml
EXML_FILE_NAME_LENGTH = 41

# This parameter defines offset of signal name after "target" marker in merged node, i.e. number of
# characters after "target" marker occurrence, where beginning of signal name occurs, an example:
# eng_gain1 target eng_gain2 target ADD a084fca5-1c0a-4dfd-881b-21c3f83284e7 target eng_gain_total
TARGET_OFFSET = 7

# This parameter defines offset of signal name after "*FIRST*" marker in merged node or line of .exml file,
# i.e. number of characters after "*FIRST*" marker occurrence, where beginning of signal name occurs, an example:
# *FIRST* some_signal *FIRST*
FIRST_INPUT_SIGNAL_OFFSET = 8

# This parameter defines offset of action uid before last "target" marker in merged node, i.e. number of
# characters before last "target" marker occurrence, where beginning of action uid occurs, an example:
# eng_gain1 target eng_gain2 target ADD a084fca5-1c0a-4dfd-881b-21c3f83284e7 target eng_gain_total
ACTION_UID_OFFSET = -37

# This parameter defines offset, which is used to cut off first input signal node from merged node, i.e. first input
# signal, its two markers "*FIRST*" and "target" marker, please note that length of first input signal name must be
# added to the offset in order to calculate final offset used to cut desired part from merged node, an example of
# merged node with first input signal node and without it:
# eng_temp1 target *FIRST* eng_temp2 *FIRST* target SUB 4de5134b-40f6-44ae-a649-1cacb525963b target eng_temp_diff
# eng_temp1 target SUB 4de5134b-40f6-44ae-a649-1cacb525963b target eng_temp_diff
CUT_FIRST_INPUT_SIGNAL_OFFSET = 23

# This parameter defines start offset of name element after "name" marker in line of .exml file, i.e.
# number of characters after "name" marker occurrence, where beginning of name element occurs, an example:
# <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
NAME_START_OFFSET = 6

# This parameter defines end offset of name element before "mc" marker in line of .exml file, i.e.
# number of characters before "mc" marker occurrence, where end of name element occurs, an example:
# <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
NAME_END_OFFSET = -2

# This parameter defines start offset of uid element after "uid" marker in line of .exml file, i.e.
# number of characters after "uid" marker occurrence, where beginning of uid element occurs, an example:
# <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
UID_START_OFFSET = 5

# This parameter defines end offset of uid element before end of .exml file line, i.e.
# number of characters before end of .exml file line occurrence, where end of uid element occurs, an example:
# <ID name="ADD" mc="Standard.OpaqueAction" uid="4f855500-ccdd-43a6-87d3-cc06dd16a59b"/>
UID_END_OFFSET = -3

# This parameter defines expected number of command line arguments passed to Mod Code Generator (MCG)
# Converter Component (CC), i.e. list of arguments:
#       - model path
NUMBER_OF_MCG_CC_CMD_LINE_ARGS = 1

# This list defines all allowed types of actions, which could be used within activity diagram to define signal
# processing
action_type_list = ["ADD", "SUB"]

# This list defines all types of actions, which require to distinguish in addition name of first input signal
action_type_req_first_input_signal_list = ["SUB"]