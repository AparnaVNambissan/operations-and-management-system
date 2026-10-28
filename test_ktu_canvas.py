import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class KTUCanvas(canvas.Canvas):
    """
    Canvas to draw standard KTU academic report headers and footers:
    - Page 1: Cover (no header/footer)
    - Pages 2-12: Preliminaries (Declaration, Certificate, Acknowledgment, Abstract, TOC, Lists)
    - Chapter pages: Running header at top-left ('Chapter X - Name'), page number at bottom-center.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.chapter_header = ""

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations()
            super().showPage()
        super().save()

    def draw_page_decorations(self):
        p = self._pageNumber
        # Cover page (1) has no headers or footers
        if p == 1:
            return

        self.saveState()
        self.setFont("Times-Roman", 11)
        self.setFillColor(colors.black)

        # Preliminary pages (Declaration to List of Appendices: pages 2 to 11)
        # In the original document, pages 2-5 have no page number shown or clean bottom.
        # Starting from Chapter 1 (page 13 in original, or starting chapter page 12/13),
        # page numbers are centered at the bottom.
        # Let's check page range:
        if p >= 13:
            arabic_page = p - 12  # Chapter 1 starts at page 1!
            # Draw bottom-center page number
            self.drawCentredString(A4[0] / 2.0, 45, str(arabic_page))

            # Running header at top-left on non-chapter-first pages
            # Chapter 1: 13, 14, 15 -> header on 14, 15
            # Chapter 2: 16, 17, 18 -> header on 17, 18
            # Chapter 3: 19 to 37 -> header on 20+
            # Chapter 4: 38 to 43 -> header on 39+
            # Chapter 5: 44 to 45 -> header on 45
            header_map = {
                (14, 15): "Chapter 1 - Introduction",
                (17, 18): "Chapter 2 - System Study",
                (20, 37): "Chapter 3 – Methodology",
                (39, 43): "Chapter 4 - Results and Discussions",
                (45, 45): "Chapter 5 - Conclusion and Future Scope",
            }
            for (p_start, p_end), title in header_map.items():
                if p_start <= p <= p_end:
                    self.setFont("Times-Roman", 11)
                    self.drawString(72, A4[1] - 45, title)
                    break
        elif p in [6, 7, 8, 9, 10, 11]:
            # Preliminary roman numerals or clean
            roman_map = {6: "vi", 7: "vii", 8: "viii", 9: "viii", 10: "ix", 11: "x"}
            if p in roman_map:
                self.drawCentredString(A4[0] / 2.0, 45, roman_map[p])

        self.restoreState()

print("KTUCanvas defined successfully")
