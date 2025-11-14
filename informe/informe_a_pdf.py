from markdown_pdf import MarkdownPdf, Section
import os

with open("informe.md", "r") as file:
    content = file.read()
    content.replace('../outputs', '/outputs')

    pdf = MarkdownPdf(toc_level=2, optimize=True)

    pdf.add_section(Section(content, toc=False, root=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
    
    pdf.meta["title"] = "Modelación Numérica - 25C2 - Bungee Jumping"
    pdf.meta["author"] = "Tomás Cichero y Valeria Brzoza"

    pdf.save("informe.pdf")


