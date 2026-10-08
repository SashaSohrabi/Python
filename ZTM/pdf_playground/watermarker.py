from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

path: Path = Path(__file__).resolve().parent
pdf_path: Path = path / "pdf"

try:
    with (
        open(pdf_path / "super.pdf", mode="rb") as template_file,
        open(pdf_path / "wtr.pdf", mode="rb") as watermark_file,
    ):
        template = PdfReader(template_file)
        watermark = PdfReader(watermark_file)
        output = PdfWriter()

        print(f"Template: {len(template.pages)} pages")
        print(f"Watermark: {len(watermark.pages)} pages")

        for i in range(template.get_num_pages()):
            page = template.get_page(i)
            page.merge_page(watermark.get_page(0))
            output.add_page(page)

            with open(pdf_path / "watermarked_output.pdf", "wb") as file:
                output.write(file)

except (OSError, PdfReadError) as error:
    print(f"Could not read the PDFs: {error}")
