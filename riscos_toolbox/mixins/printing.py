from ..events import toolbox_handler
from ..objects.printdbox import PrintEvent
from .. import report_exception, BBox, Point

import ctypes
import swi

class PrintMixin:
    Transform = ctypes.c_int32*2*2

    @property
    def pages(self):
        return 1

    def declare_fonts(self):
        """
        Declare the fonts used in this document, returns a list of
        handle, name, flags, as required by PDriver_DeclareFont. There is no
        need to add the final 0,0,0 to the list as the Mixin will call
        PDriver_DeclareFont with the 0,0,0 end-of-list marker.

        Drawfile_DelcareFonts etc can also be called here.
        """
        return []

    def give_rectangles(self, page, sideways, scale):
        """
        Gets the rectangles needed to draw the given page. If sideways is True
        it should be drawn sidewase, otherwise upright.

        Returns a list of
        ( id (unsigned int),
          rect (BBox),
          transform (PrintMixin.Transform),
          origin (point),
          background_colour (unsigned int) ) # 0xBBGGRR00
        """
        return []

    def draw_rectangle(self, page, rectangle, sideways, scale, id):
        """
        Called to draw the given rectangle.
        """
        pass

    @toolbox_handler(PrintEvent)
    def print_event(self, code, id_block, event):

        copies = event.copies
        scale = event.scale_factor
        sideways = event.sideways

        try:
            features = swi.swi("PDriver_Info",";...I")
        except:
            raise RuntimeError("Printer driver not loaded.")

        job = swi.swi("OS_Find","Is;I",0x83,"printer:")
        if job == 0:
            raise RuntimeError("Failed to open printer:")

        try:
            prev_job = swi.swi("PDriver_SelectJob","Is;I",job,"Pyper")

            if features & 1<<29: # Declare font
                declared_fonts = self.declare_fonts()
                if declared_fonts is not None:
                    for handle,name,flags in declared_fonts:
                        swi.swi("PDriver_DeclareFont","IsI",handle,name,flags)
                swi.swi("PDriver_DeclareFont","000")

            start_page = event.start_page
            if start_page == -1:
                start_page = 1
                finish_page = self.pages
            else:
                finish_page = event.finish_page

            for page in range(start_page, finish_page+1):
                for id,rect,transform,origin,background in \
                        self.give_rectangles(page, sideways, scale):
                    swi.swi("PDriver_GiveRectangle", "IIIII",
                        id,
                        ctypes.addressof(rect),
                        ctypes.addressof(transform),
                        ctypes.addressof(origin),
                        background)

                    rect = BBox.zero()
                    more,rect_id = \
                    swi.swi("PDriver_DrawPage","IIII;I.I",
                        copies, ctypes.addressof(rect),
                        0,0 )

                while more:
                    self.draw_rectangle(page, rect, sideways, scale, rect_id)

                    more,rect_id = \
                        swi.swi("PDriver_GetRectangle",".I;I.I",
                            ctypes.addressof(rect))

            if job != 0:
                swi.swi("PDriver_EndJob","I",job)
                swi.swi("OS_Find","II",0,job)
                job = 0

            if prev_job != 0:
                swi.swi("PDriver_SelectJob","II",prev_job, 0)

        except Exception as e:
            if job != 0:
                swi.swi("PDriver_AbortJob","I",job)
                swi.swi("OS_Find","II",0,job)
            report_exception(e)

