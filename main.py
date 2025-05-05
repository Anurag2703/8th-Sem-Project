from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
from pydantic import BaseModel
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use relative path based on project structure
PDF_FOLDER = Path("Comics Page/COMICS")

@app.post("/add-comment/")
def add_comment(story_id: int = Form(...), comment: str = Form(...)):
    pdf_path = PDF_FOLDER / f"{story_id}.pdf"
    if not pdf_path.exists():
        return {"error": "PDF not found"}

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Create a new page with the comment
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import io

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(72, 720, f"User Comment for Story {story_id}:")
    can.drawString(72, 700, comment)
    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)
    writer.add_page(new_pdf.pages[0])

    # Save updated PDF
    with open(pdf_path, "wb") as f:
        writer.write(f)

    return {"message": "Comment added successfully"}


class PDFRequest(BaseModel):
    pdf_name: str

@app.post("/erase_comment")
def erase_comment(req: PDFRequest):
    input_path = os.path.join(PDF_FOLDER, req.pdf_name)

    if not os.path.exists(input_path):
        return {"message": "PDF not found."}

    reader = PdfReader(input_path)
    writer = PdfWriter()

    if len(reader.pages) < 2:
        return {"message": "Not enough pages to erase comment."}

    # Write all but the last page
    for i in range(len(reader.pages) - 1):
        writer.add_page(reader.pages[i])

    with open(input_path, "wb") as f:
        writer.write(f)

    return {"message": "Comments erased successfully!"}
