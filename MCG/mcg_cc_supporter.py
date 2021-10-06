#   FILE:           mcg_cc_supporter.py
#
#   DESCRIPTION:
#       This module provides additional, supporting functions, which are used
#       by Mod Code Generator (MCG) Converter Component (CC) to read details of
#       .exml file or merged nodes.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           6 OCT 2021
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


from mcg_cc_parameters import action_type_list
from mcg_cc_parameters import action_type_req_first_input_signal_list


# Function:
# check_if_reference_contains_action_type()
#
# Description:
# This function checks if reference contains any action type.
#
# Returns:
# This function returns action found marker.
def check_if_reference_contains_action_type(reference):
    # action marker shows whether reference contains action type
    action_type_found = False

    # for all allowed type of actions
    for action_type in action_type_list:
        # if action type is found within reference
        if action_type in reference:
            # change action marker
            action_type_found = True
            # exit loop
            break

    # return action marker
    return action_type_found


# Function:
# check_if_reference_contains_action_type_req_first_input_signal()
#
# Description:
# This function checks if reference contains any action type requiring first input signal.
#
# Returns:
# This function returns action found marker.
def check_if_reference_contains_action_type_req_first_input_signal(reference):
    # action marker shows whether reference contains action type requiring first input signal
    action_type_req_first_input_signal_found = False

    # for all allowed type of actions requiring first input signal
    for action_type_req_first_input_signal in action_type_req_first_input_signal_list:
        # if action type requiring first input signal is found within reference
        if action_type_req_first_input_signal in reference:
            # change action marker
            action_type_req_first_input_signal_found = True
            # exit loop
            break

    # return action marker
    return action_type_req_first_input_signal_found
