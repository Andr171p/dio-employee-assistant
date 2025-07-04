import docx2txt


docx_path = r"C:\Users\andre\IdeaProjects\DIORag\knowledge_base\Инструкции\ИНСТРУКЦИЯ_1С_УФФ_АРМ_Специалиста.docx"
output_image_directory = "extracted_images/"

# Extract text and save images
text = docx2txt.process(docx_path, output_image_directory)

print(f"Text extracted: {text[:200]}...") # Print first 200 characters of extracted text
print(f"Images saved to: {output_image_directory}")