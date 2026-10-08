import sys
from pathlib import Path

from pypdf import PdfWriter

path: Path = Path(__file__).resolve().parent
pdf_path: Path = path / "pdf"


inputs = sys.argv[1:]


def pdf_combiner(pdf_list: list[str]):
    with PdfWriter() as merger:
        for pdf in pdf_list:
            print(pdf)
            merger.append(pdf)

    merger.write(pdf_path / "super.pdf")


pdf_combiner(inputs)
