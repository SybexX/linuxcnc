#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#    GLADE_VCP
#    Copyright 2010 Chris Morley
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import gi
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject
from gi.repository import GLib

import sys
import hal
import getopt

from .hal_widgets import _HalWidgetBase
from .led import HAL_LED
from common.hal_glib import GComponent

from gladevcp.gladebuilder import widget_name

class GladePanel():
    def on_window_destroy(self, widget, data=None):
        self.hal.exit()
        gobject.source_remove(self.timer)
        gtk.main_quit()

    def __init__(self,halcomp,xmlname,builder,buildertype):
        
        self.builder = builder
        self.hal = GComponent(halcomp)
        self.widgets = {}
        self.extension_obj = None

        for widget in builder.get_objects():
            idname = widget_name(widget)

            if idname is None:
                continue

            if isinstance(widget, _HalWidgetBase):
                widget.hal_init(self.hal, idname, self)
                self.widgets[idname] = widget

        self.timer = GLib.timeout_add(100, self.update)   
               
    def get_handler_obj(self):
        return self.extension_obj

    def set_handler(self, data):
        self.extension_obj = data

    def update(self):
        for obj in list(self.widgets.values()):
            obj.hal_update()
        return True
    def __getitem__(self, item):
        return self.widgets[item]
    def __setitem__(self, item, value):
        self.widgets[item] = value
    
if __name__ == "__main__":
    print("Gladevcp_make_pins cannot be run on its own")
    print("It must be called by gladevcp or a python program")
    print("that loads and displays the glade panel and creates a HAL component")

# vim: sts=4 sw=4 et
