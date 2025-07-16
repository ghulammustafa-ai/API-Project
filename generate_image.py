import requests
import json
import time

# -----------------------------
# Step 1: Send Text-to-Image Request
# -----------------------------
def generate_image_from_prompt(prompt):
    text2image_url = 'https://api.lightxeditor.com/external/api/v1/text2image'
    api_key = '87b1e24549624f7fbefdcad28dc121d3_937bb44022594dcd8103c8453f41703b_andoraitools'

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    payload = {
        "textPrompt": prompt  # Change prompt as needed
    }

    response = requests.post(text2image_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Text-to-Image Request Successful")
        data = response.json()
        order_id = data["body"]["orderId"]
        print(f"🆔 Order ID: {order_id}")
    else:
        print(f"❌ Text-to-Image Request Failed | Status: {response.status_code}")
        print(response.text)
        exit()

    # -----------------------------
    # Step 2: Poll Order Status
    # -----------------------------
    order_status_url = 'https://api.lightxeditor.com/external/api/v1/order-status'

    status_payload = {
        "orderId": order_id
    }

    print("\n🔁 Checking Order Status...\n")

    for attempt in range(5):
        status_response = requests.post(order_status_url, headers=headers, json=status_payload)

        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"🔎 Attempt {attempt + 1} | Status Response:")
            print(json.dumps(status_data, indent=2))
            
            # Check if image is ready
            if status_data["body"]["status"] == "active":
                image_url = status_data["body"]["output"]
                print(image_url)
                return image_url
                
                break
        else:
            print(f"❌ Failed to get status | Status: {status_response.status_code}")
            print(status_response.text)

        time.sleep(3)
