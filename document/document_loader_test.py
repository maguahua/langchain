from langchain_community.document_loaders.csv_loader import CSVLoader

file_path = (
    "test.csv"
)

loader = CSVLoader(file_path=file_path)
data = loader.load()

for record in data:
    print(record)