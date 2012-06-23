#!/usr/bin/python
#
# You must enable assistive technologies before running this!
# gconftool-2 --set "/desktop/gnome/interface/accessibility" --type boolean "True"

import pyatspi
from traceback import *

abbrs = {
    'vasi': 'pants',
    'ms': 'M$',
    'linux': 'GNU/Linux',
    'faq': 'Please read the dagnabbed FAQ!'
}

def handler(event):
    if handler.spurious:
        return
    try:
        txt_iface = event.source.queryEditableText()
    except NotImplementedError:
        return
    
    # TODO: Multiple replacements at once (fast typer)? Don't look at pastes?
    #   Prevent cascading replacement? Trigger on space, other char?
    
    global abbrs
    txt = txt_iface.getText(0, -1) # get all
    start, length = event.detail1, event.detail2
    # If multiple chars are typed in quick succession, only one insert event is
    # generated. So we need to look at each character of the event in turn
    for off_end in xrange(start + 1, start + length + 1):
        for k, v in abbrs.items(): # TODO: define an order?
            if len(k) <= off_end: # don't go past beginning
                off_start = off_end - len(k)
                if txt[off_start:off_end] == k:
                    handler.spurious = True
                    # OpenOffice has drawing problems when you arbitrarily
                    # modify its text: Use keystrokes instead?
                    txt_iface.deleteText(off_start, off_end)
                    txt_iface.insertText(off_start, v, len(v))
                    txt_iface.setCaretOffset(off_start + len(v))
                    handler.spurious = False
                    break
# 'deleteText' triggers a spurious 'insert' notification, detect it
handler.spurious = False
 
reg = pyatspi.Registry
reg.registerEventListener(handler, "object:text-changed:insert")
try:
    reg.start()
finally:
    reg.deregisterEventListener(handler, "object:text-changed:insert")

