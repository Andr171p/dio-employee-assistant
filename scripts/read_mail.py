from langchain_community.document_loaders import UnstructuredEmailLoader


path = r"C:\Users\andre\Downloads\Message17420262551822861034.eml"

loader = UnstructuredEmailLoader(path)

data = loader.load()

print(data)
