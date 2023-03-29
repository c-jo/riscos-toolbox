from riscos_toolbox.wimp_events.redraw_window import RedrawWindow
import struct

rw = RedrawWindow(123)
assert(rw.id == 1)
assert(rw.window_handle == 123)
block = struct.pack("i",42)

rw = RedrawWindow.from_block(block)
assert(rw.id == 1)
assert(rw.window_handle == 42)
