import requests

url = 'http://localhost:8000/upload-yaml/'
file_path = 'C:\\python\\diplomniy_proekt\\pythonProject\\auto_procurement\\shop1.yaml'

with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())
