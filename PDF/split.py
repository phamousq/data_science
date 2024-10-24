import pymupdf
import re

filename = "/Users/qpair/Library/CloudStorage/Box-Box/Q's Cloud/Dell Med/MS3/CID/Biodesign Textbook - Yock.PDF"
src = pymupdf.open(filename)


class PDF_File:
    def __init__(self, file_path):
        self.src = pymupdf.open(filename)
        self.path = file_path

    def export_pages(self, chapters):
        for x in range(len(chapters) - 1):
            tar = pymupdf.open()  # output PDF for 1 page
            # copy over current page
            tar.insert_pdf(
                self.src, from_page=chapters[x][2] - 1, to_page=chapters[x + 1][2] - 2
            )
            tar.save(f"{chapters[x][1]}.pdf")
            tar.close()

    def get_chapters(self):
        chapters = []
        toc = self.src.get_toc()
        for x in toc:
            if re.match(r"^\d\.\d", x[1]) and x[0] == 3:
                chapters.append(x)
        return chapters


a = PDF_File(filename)

a.export_pages(a.get_chapters())
