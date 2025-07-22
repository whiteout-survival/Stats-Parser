import base64
import requests

image_path_1 = "../images/minime/1.png"
image_path_2 = "../images/minime/2.png"

with open(image_path_1, "rb") as img_file:
    image_data_1 = base64.b64encode(img_file.read()).decode('utf-8')
with open(image_path_2, "rb") as img_file:
    image_data_2 = base64.b64encode(img_file.read()).decode('utf-8')

base_url = "http://cd2db4qq-8000.use.devtunnels.ms/" # Replace with your actual base URL
endpoint = "api/v1/read_stats"
url = f"{base_url}{endpoint}"

response = requests.post(url,
    json = {
        "images": [
            {"image_data": image_data_1},
            {"image_data": image_data_2}
        ]
    }
)

if response.status_code == 200:
    print("Merged stats:")
    print(response.json().get("merged_stats"))
else:
    print(f"Error: {response.status_code}")
    print(response.text)