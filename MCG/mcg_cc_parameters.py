#   FILE:           mcg_cc_parameters.py
#
#   DESCRIPTION:
#       This module contains additional parameters, which are used across other
#       modules of Mod Code Generator (MCG) Converter Component (CC).
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           10 SEP 2021
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

# This parameter defines offset of signal name after "target" marker in merged node, i.e. number of
# characters after occurrence of "target" marker, where beginning of signal name occurs, an example:
# eng_gain1 target eng_gain2 target ADD a084fca5-1c0a-4dfd-881b-21c3f83284e7 target eng_gain_total
TARGET_OFFSET = 7

# This parameter defines offset of signal name after "*FIRST*" marker in merged node or line of .exml file,
# i.e. number of characters after occurrence of "*FIRST*" marker, where beginning of signal name occurs, an example:
# *FIRST* some_signal *FIRST*
FIRST_INPUT_SIGNAL_OFFSET = 8

# This parameter defines offset of action uid before end of action definition, i.e. number of characters
# before occurrence of action definition end, where beginning of action uid occurs, plus one additional
# character to accommodate space between action type and action uid, an example:
# ADD fd5be3ed-0d38-42d0-ab56-d1058657eee8
ACTION_UID_OFFSET = -37

# This parameter defines expected number of command line arguments passed to Mod Code Generator (MCG)
# Converter Component (CC), i.e. list of arguments:
#       - model path
NUMBER_OF_MCG_CC_CMD_LINE_ARGS = 1

# This list defines all allowed types of actions, which could be used within activity diagram to define signal
# processing
action_type_list = ["ADD", "SUB"]

# This list defines all types of actions, which require to distinguish in addition first input signal
action_type_req_first_input_signal_list = ["SUB"]
