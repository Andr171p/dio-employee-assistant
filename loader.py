from docx2md import DocxFile, DocxMedia, Converter


def convert(docx_file: str, target_dir: str = "", use_md_table: bool = True) -> str:
    try:
        docx = DocxFile(docx_file)
        media = DocxMedia(docx)
        if target_dir:
            media.save(target_dir)
        converter = Converter(docx.document(), media, use_md_table)
        return converter.convert()
    except Exception as e:
        return f"Exception: {e}"


file_path = r"C:\Users\andre\IdeaProjects\DIORag\knowledge_base\Инструкции\ИНСТРУКЦИЯ_1С_УФФ_АРМ_Специалиста.docx"

md_text = convert(file_path)
# print(md_text)
md_text = str(md_text).replace('# ** skip tcPr', '')
print(md_text)

with open("file.md", "w", encoding="utf-8") as file:
    file.write(md_text)
