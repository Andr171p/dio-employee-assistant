import markitdown

file_path = r"C:\Users\andre\IdeaProjects\DIORag\knowledge_base\Презентации\навыки_деловой_переписки.pptx"

md = markitdown.MarkItDown()

md_text = md.convert(file_path)

print(md_text.text_content)
