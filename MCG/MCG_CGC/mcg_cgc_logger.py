#   FILE:           mcg_cgc_logger.py
#
#   DESCRIPTION:
#       This module contains definition of Logger class, which is responsible
#       for log recording during MCG CGC run.
#
#   COPYRIGHT:      Copyright (C) 2022 Kamil Deć github.com/deckamil
#   DATE:           17 MAR 2022
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


# Description:
# This class is responsible for log recording during MCG CGC run.
class Logger(object):

    # initialize class data
    log_file_disk = ""
    log_file_path = ""

    # Description:
    # This method sets path to log file, which will contain events record from MCG CGC.
    @staticmethod
    def set_log_file_path(output_dir_path):

        # set log file path
        Logger.log_file_path = output_dir_path + str("\\mcg_cgc_log.txt")

        # open new file in write mode, then close file, to clear previous content
        Logger.log_file_disk = open(Logger.log_file_path, "w")
        Logger.log_file_disk.close()

    # Description:
    # This method saves header info in log file.
    @staticmethod
    def save_log_file_header():

        # open file in append mode, ready to save fresh info in log content
        Logger.log_file_disk = open(Logger.log_file_path, "a")

        # get date
        date = datetime.datetime.now()

        # write header info to log file on hard disk
        Logger.log_file_disk.write(str("MCG CGC LOG START\n"))
        Logger.log_file_disk.write(str("MCG CGC LOG DATE ") + str(date) + str("\n"))

        # close file
        Logger.log_file_disk.close()

    # Description:
    # This method saves footer info in log file.
    @staticmethod
    def save_log_file_footer():

        # open file in append mode, ready to save fresh info in log content
        Logger.log_file_disk = open(Logger.log_file_path, "a")

        # get date
        date = datetime.datetime.now()

        # write footer info to log file on hard disk
        Logger.log_file_disk.write(str("\nMCG CGC LOG DATE ") + str(date))
        Logger.log_file_disk.write(str("\nMCG CGC LOG END"))

        # close file
        Logger.log_file_disk.close()

    # Description:
    # This method prints and saves info in log file.
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
