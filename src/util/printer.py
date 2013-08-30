#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Instashow System
# Copyright (C) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Instashow System.
#
# Hive Instashow System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Instashow System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Instashow System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import win32ui
import win32print

import PIL.Image
import PIL.ImageWin

HORZ_RES = 8
VERT_RES = 10

PHYSICAL_WIDTH = 110
PHYSICAL_HEIGHT = 111

def print_image(file_path):
    # retrieves the name (as a string) of the currently
    # defined default printer for the system
    printer_name = win32print.GetDefaultPrinter()

    # creates the device independent bitmap from the provided
    # printer name and then gathers the size of both the printable
    # area as resolution and real size
    hdc = win32ui.CreateDC()
    hdc.CreatePrinterDC(printer_name)
    printable_area = hdc.GetDeviceCaps(HORZ_RES), hdc.GetDeviceCaps(VERT_RES)
    printer_size = hdc.GetDeviceCaps(PHYSICAL_WIDTH), hdc.GetDeviceCaps(PHYSICAL_HEIGHT)

    # opens the image, rotates it if it's wider than
    # it is high, and work out how much to multiply
    # each pixel by to get it as big as possible on
    # the page without distorting
    bmp = PIL.Image.open(file_path)
    if bmp.size[0] > bmp.size[1]: bmp = bmp.rotate(90)

    # calculates the rations and sets the scale as the minimum
    # value of both rations (optimizes area)
    ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
    scale = min(ratios)

    # starts the print job, and draws the bitmap to
    # the printer device at the scaled size
    hdc.StartDoc(file_path)
    hdc.StartPage()

    # creates the dib object from the bitmap one provided
    # and then scales it properly to occupy the complete area
    # of the page that is going to be created
    dib = PIL.ImageWin.Dib(bmp)
    scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
    x1 = int((printer_size[0] - scaled_width) / 2)
    y1 = int((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw(hdc.GetHandleOutput(), (x1, y1, x2, y2))

    # closes the current page, the document and deletes
    # the current drawing context (avoids memory leaks)
    hdc.EndPage()
    hdc.EndDoc()
    hdc.DeleteDC()
