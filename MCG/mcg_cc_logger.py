#   FILE:           mcg_cc_logger.py
#
#   DESCRIPTION:
#       This module contains definition of Logger class, which
#       is responsible for log recording during MCG CC run.
#
#   COPYRIGHT:      Copyright (C) 2021 Kamil Deć github.com/deckamil
#   DATE:           27 OCT 2021
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


import datetime


# Class:
# Logger()
#
# Description:
# This is base class responsible for log recording during MCG CC run.
class Logger(object):

    # initialize class data
    log_file_disk = ""
    log_file_path = ""

    # Method:
    # set_log_file_path()
    #
    # Description:
    # This method sets path to directory, where configuration file will be recorded.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def set_log_file_path(output_dir_path):

        # set log file path
        Logger.log_file_path = output_dir_path + str("\\mcg_cc_log.txt")

        # open new file in write mode, then close file, to clear previous content
        Logger.log_file_disk = open(Logger.log_file_path, "w")
        Logger.log_file_disk.close()

    # Method:
    # save_log_file_header()
    #
    # Description:
    # This method saves header info in log file.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def save_log_file_header():

        # open file in append mode, ready to save fresh info in log content
        Logger.log_file_disk = open(Logger.log_file_path, "a")

        # get date
        date = datetime.datetime.now()

        # write header info to log file on hard disk
        Logger.log_file_disk.write(str("MCG CC LOG START\n"))
        Logger.log_file_disk.write(str("MCG CC LOG DATE ") + str(date) + str("\n"))

        # close file
        Logger.log_file_disk.close()

    # Method:
    # saves_log_file_footer()
    #
    # Description:
    # This method saves footer info in log file.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def saves_log_file_footer():

        # open file in append mode, ready to save fresh info in log content
        Logger.log_file_disk = open(Logger.log_file_path, "a")

        # get date
        date = datetime.datetime.now()

        # write header info to log file on hard disk
        Logger.log_file_disk.write(str("\nMCG CC LOG DATE ") + str(date))
        Logger.log_file_disk.write(str("\nMCG CC LOG END"))

        # close file
        Logger.log_file_disk.close()

    # Method:
    # save_in_log_file()
    #
    # Description:
    # This method prints and saves info in log file.
    #
    # Returns:
    # This method does not return anything.
    @staticmethod
    def save_in_log_file(info):

        # open file in append mode, ready to save fresh info in log content
        Logger.log_file_disk = open(Logger.log_file_path, "a")

        # print info
        print(info)

        # write info to log file on hard disk
        Logger.log_file_disk.write(info)
        Logger.log_file_disk.write("\n")

        # close file
        Logger.log_file_disk.close()
