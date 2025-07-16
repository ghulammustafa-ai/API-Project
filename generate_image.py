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
        "textPrompt": prompt
    }

    try:
        response = requests.post(text2image_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        order_id = data["body"]["orderId"]
        print("✅ Text-to-Image Request Successful")
        print(f"🆔 Order ID: {order_id}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Network or Request Error: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"❌ Error parsing response: {e}")
        return None

    # -----------------------------
    # Step 2: Poll Order Status
    # -----------------------------
    order_status_url = 'https://api.lightxeditor.com/external/api/v1/order-status'
    status_payload = {
        "orderId": order_id
    }

    print("\n🔁 Checking Order Status...\n")

    for attempt in range(10):
        try:
            status_response = requests.post(order_status_url, headers=headers, json=status_payload, timeout=10)
            status_response.raise_for_status()
            status_data = status_response.json()

            print(f"🔎 Attempt {attempt + 1} | Status Response:")
            print(json.dumps(status_data, indent=2))

            if status_data["body"]["status"] == "active":
                image_url = status_data["body"]["output"]
                print(f"✅ Image Ready: {image_url}")
                return image_url

        except requests.exceptions.RequestException as e:
            print(f"❌ Status Request Failed: {e}")
        except (KeyError, json.JSONDecodeError) as e:
            print(f"❌ Error parsing status response: {e}")

        time.sleep(3)

    print("❗ Image not ready after 10 attempts.")
    return None
