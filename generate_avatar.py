import requests
import os
import time
# Configuration
API_KEY = "3b8394a77fe048fe85aed0a597795210_405a5f45dd02429fa17c35a01f3aadfb_andoraitools"  # Your API key
BASE_URL = "https://api.lightxeditor.com/external/api/v2"


# Function to upload the image
def upload_image(image_path:str,prompt:str,style_image:str)->str:
    
    # Check if image exists and get size
    if not os.path.isfile(image_path):
        print(f"Error: Image not found at {image_path}")
        exit()
    image_size = os.path.getsize(image_path)
    if image_size > 5242880:  # 5 MB limit
        print("Error: Image size exceeds 5 MB")
        exit()

    # Prepare headers and payload
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "uploadType": "imageUrl",
        "size": image_size,
        "contentType": "image/jpeg"
    }
    print(f"Debug: Sending headers: {headers}")

    # Step 1: Get upload URL
    response = requests.post(f"{BASE_URL}/uploadImageUrl", headers=headers, json=payload)
    print(f"Debug: Response status: {response.status_code}, Response text: {response.text}")
    if response.status_code != 200:
        print(f"Error getting upload URL: {response.text}")
        exit()

    data = response.json()
    upload_url = data["body"]["uploadImage"]
    
    print("Upload URL received.")

    # Step 2: Upload image
    with open(image_path, "rb") as f:
        response = requests.put(upload_url, headers={"Content-Type": "image/jpeg"}, data=f)

    if response.status_code != 200:
        print(f"Error uploading image: {response.status_code} {response.text}")
        exit()

    print("Image uploaded.")
    image_url = data["body"]["imageUrl"]



# Configuration
    
    
    UPLOAD_IMAGE_URL = image_url  # Replace with your uploaded image URL
    
    

# Function to send a request for image transformation

    # headers = {
    #     "Content-Type": "application/json",
    #     "x-api-key": API_KEY
    # }

    # Payload with uploaded image, style image, and text prompt
    payload = {
        "imageUrl": UPLOAD_IMAGE_URL,
        "styleImageUrl": style_image,
        "textPrompt": prompt
    }

    # Make API request to apply transformation
    try:
        response = requests.post(f"https://api.lightxeditor.com/external/api/v1/avatar", headers=headers, json=payload)
        print(f"Debug: Response status: {response.status_code}, Response text: {response.text}")
        response.raise_for_status()  # Will raise an error for bad responses

        # Process the response data
        data = response.json()
        if data.get("statusCode") == 2000 and data.get("message") == "SUCCESS":
            order_id = data["body"]["orderId"]
            print(f"Transformation request successful. Order ID: {order_id}")
            
        else:
            print("Error in transformation request:", data)
            
    except requests.exceptions.RequestException as err:
        print(f"Error during API request: {err}")

    

    
         

# Example usage



# Function to check status of transformation
    
    # headers = {
    #         "Content-Type": "application/json",
    #         "x-api-key": API_KEY
    #     }

    payload = {
            "orderId": order_id
        }

        # Make request to check status
    try:
            # Loop to retry 5 times, checking every 3 seconds
        for _ in range(5):
            response = requests.post(f"{BASE_URL}/order-status", headers=headers, json=payload)
            print(f"Debug: Status check response status: {response.status_code}, Response text: {response.text}")
            response.raise_for_status()  # Will raise an error for bad responses

                # Process response
            data = response.json()
            if data.get("statusCode") == 2000 and data.get("message") == "SUCCESS":
                status = data["body"]["status"]
                if status == "active":
                    output_image_url = data["body"]["output"]
                    print(f"Transformation completed successfully. Output Image URL: {output_image_url}")
                    return output_image_url
                else:
                    print(f"Transformation still in progress (status: {status}). Retrying...")
            else:
                print("Error in status check:", data)
                

                # Wait for 3 seconds before retrying
            time.sleep(3)

        print("Transformation failed or max retries exceeded.")
        
    except requests.exceptions.RequestException as err:
        print(f"Error during status check: {err}")
        

# Check transformation status with your order ID
        # if order_id:
        #     output_url = check_status(order_id, API_KEY)
