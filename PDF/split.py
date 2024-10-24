import pymupdf
import re

filename = "/Users/qpair/Library/CloudStorage/Box-Box/Q's Cloud/Dell Med/MS3/CID/Biodesign Textbook - Yock.PDF"
src = pymupdf.open(filename)


class PDF_File:
    def __init__(self, file_path):
        self.src = pymupdf.open(filename)
        self.path = file_path

    # ! make this thing
    def export_pages(
        self,
    ):
        tar = pymupdf.open()
        tar.insert_pdf(self.src, from_page=start, to_page=end)
        tar.save(f"{page.number}.pdf")
        tar.close()


toc = src.get_toc()
chapters = []
for x in toc:
    if re.match(r"^\d\.\d", x[1]) and x[0] == 3:
        chapters.append(x)

for x in range(len(chapters) - 1):
    tar = pymupdf.open()  # output PDF for 1 page
    # copy over current page
    tar.insert_pdf(src, from_page=chapters[x][2] - 1, to_page=chapters[x + 1][2] - 2)
    tar.save(f"{chapters[x][1]}.pdf")
    tar.close()
