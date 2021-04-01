#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
'''
    KiCad BoardFactory
    Generates KiCad board file templates based on templates and a variable list.
'''
# @author    Jochen Oberreiter <jochen@oberreiternet.de>
# @date      2021-03-31
# @copyright Copyright (c) by Jochen Oberreiter

import datetime
import os
from pydoc import __date__

__package__ = 'KiCad BoardFactory'
__version__ = '1.0'
__author__  = 'Jochen Oberreiter'
__email__   = 'jochen@oberreiternet.de'
__date__    = '2021-03-31'
__stage__   = 'development'
__license__ = 'MIT'

#---<ConfigurationZone>--------------------------------------------------------
#
__data_directory__ =  os.path.join('.', 'data')
__output_directory__ =  os.path.join('.', 'output')
__data_file = os.path.join(__data_directory__, 'data.json')

#---</ConfigurationZone>-------------------------------------------------------

# Set up logging. Default output is a text
# file under Windows and syslog under Linux.
import logging
import platform
logger = logging.getLogger(__package__.replace(' ', '_'))
logger.setLevel(logging.DEBUG)
if platform.system() == 'Windows':
    handler = logging.FileHandler(os.path.splitext(os.path.basename(__file__))[0] + '.log', mode='w')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
else:
    handler = logging.handlers.SysLogHandler(address = '/dev/log', facility=logging.handlers.SysLogHandler.LOG_DAEMON)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s[%(process)d]: %(levelname)s %(message)s')
    handler.setFormatter(formatter)
logger.addHandler(handler)


#---<Main>---------------------------------------------------------------------

# Output basic package data (title, author).
logger.info(__package__ + ' v%s', __version__)
logger.info(__author__ + ' <' + __email__ + '>, ' + __date__)
logger.info('Starting.')

# Load data variables
import json
data = []
logger.info('Reading data from ''%s''...', __data_file)
with open(__data_file, encoding='utf-8') as f:
    raw_data = f.read()
    data = json.JSONDecoder().decode(raw_data)
logger.debug('data = %s', json.JSONEncoder().encode(data))

# Looping through templates and do a simple string replace.

for board in data:

    # Get board name.
    board_name = board['name']
    logger.info('Start processing board %s', board_name)

    # Ensure the output path is existent.
    output_path = os.path.join(__output_directory__, board_name)
    if not os.path.isdir(output_path):
        logger.info("Create new directory %s", output_path)
        try:
            os.mkdir(output_path)
        except OSError:
            logger.error("Creation of the directory %s failed" % output_path)

    # Loop through template files.
    for template_file in os.listdir(__data_directory__):
        if template_file.endswith('.template'):
            template_file = os.path.join(__data_directory__, template_file)
            logger.info('Start processing file %s', template_file)

            # Read file content.
            with open(template_file, encoding='utf-8') as f:
                raw_template = f.read()

            # Do a regex search and replace.
            for variable in board:
                logger.info('Replacing variable %s with %s', variable, str(board[variable]))
                raw_template = raw_template.replace('{' + variable + '}', str(board[variable]))

            # Save the result back onto disk.
            result_filename = board_name + os.path.splitext(os.path.basename(template_file.replace('.template', '')))[1]
            result_file = os.path.join(output_path, result_filename)
            logger.info('Save result to %s', result_file)
            with open(result_file, 'x', encoding='utf-8') as f:
                f.write(raw_template)

            logger.info('Finished processing file %s', template_file)
    logger.info('Finished processing board %s', board_name)

logger.info('Exiting.')
