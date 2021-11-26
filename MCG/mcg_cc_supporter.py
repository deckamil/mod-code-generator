#   FILE:           mcg_cc_supporter.py
#
#   DESCRIPTION:
#       This module contains definition of Supporter class, which provides additional
#       supporting methods and parameters reused by other Mod Code Generator (MCG)
#       Converter Component (CC) classes.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           26 NOV 2021
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


# Class:
# Supporter()
#
# Description:
# This is base class, which provides additional methods and parameters reused by other MCG CC classes.
class Supporter(object):

    # This parameter defines offset of signal or structure name after "$TARGET$" marker in merged node,
    # i.e. number of characters after occurrence of "$TARGET$" marker, where beginning of signal or
    # structure name occurs, an example:
    # eng_gain1 $TARGET$ eng_gain2 $TARGET$ ADD a084fca5-1c0a-4dfd-881b-21c3f83284e7 $TARGET$ eng_gain_total
    TARGET_OFFSET = 9

    # This parameter defines offset of signal name after "$FIRST$" marker in merged node or line of .exml file,
    # i.e. number of characters after occurrence of "$FIRST$" marker, where beginning of signal name occurs, an example:
    # $FIRST$ some_signal $FIRST$
    FIRST_INPUT_SIGNAL_OFFSET = 8

    # This parameter defines offset of action or component uid before end of action or component definition,
    # i.e. number of characters before occurrence of action or component definition end, where beginning of action
    # or component uid occurs, plus one additional character to accommodate space between action type or component
    # name and uid, an example:
    # ADD fd5be3ed-0d38-42d0-ab56-d1058657eee8
    UID_OFFSET = -37

    # This list defines all allowed types of actions, which could be used within activity diagram
    # to define signal interactions.
    action_type_list = ["ADD", "SUB"]

    # This list defines all types of actions, which require to distinguish in addition first input signal.
    action_type_req_first_input_signal_list = ["SUB"]

    # Method:
    # check_if_reference_contains_action_type()
    #
    # Description:
    # This method checks if reference contains any action type.
    #
    # Returns:
    # This method returns action marker.
    @staticmethod
    def check_if_reference_contains_action_type(reference):
        # action marker shows whether reference contains action type
        action_type_found = False

        # for all allowed type of actions
        for action_type in Supporter.action_type_list:
            # if action type is found within reference
            if action_type in reference:
                # change action marker
                action_type_found = True
                # exit loop
                break

        # return action marker
        return action_type_found

    # Method:
    # check_if_reference_contains_action_type_req_first_input_signal()
    #
    # Description:
    # This method checks if reference contains any action type requiring first input signal.
    #
    # Returns:
    # This method returns action marker.
    @staticmethod
    def check_if_reference_contains_action_type_req_first_input_signal(reference):
        # action marker shows whether reference contains action type requiring first input signal
        action_type_req_first_input_signal_found = False

        # for all allowed type of actions requiring first input signal
        for action_type_req_first_input_signal in Supporter.action_type_req_first_input_signal_list:
            # if action type requiring first input signal is found within reference
            if action_type_req_first_input_signal in reference:
                # change action marker
                action_type_req_first_input_signal_found = True
                # exit loop
                break

        # return action marker
        return action_type_req_first_input_signal_found
