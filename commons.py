import fitz  # PyMuPDF
import base64


def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            images.append({
                "page": page_num + 1,
                "width": base_image["width"],
                "height": base_image["height"],
                "format": base_image["ext"],
                "base64": image_base64
            })

    return images


# Использование
file_path = r"C:\Users\andre\IdeaProjects\DIORag\knowledge_base\Инструкции\Инструкция по системе Тикеты.pdf"
pdf_images = extract_images_from_pdf(file_path)
for idx, img in enumerate(pdf_images[:3]):  # Вывод первых 3 изображений
    print(f"Изображение {idx + 1}:")
    print(f"Страница: {img['page']}")
    print(f"Размер: {img['width']}x{img['height']}")
    print(f"Формат: {img['format']}")
    print(f"Base64 (первые 30 символов): {img['base64'][:30]}...\n")