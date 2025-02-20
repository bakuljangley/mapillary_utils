import requests
import os

# Replace with your actual credentials
client_id = '8196090173836012'
client_secret = 'MLY|8196090173836012|ddc33067dcc77fbd34f75d4111fa2eed'
redirect_uri = 'https://jangley-vprcallback.netlify.app/'
authorization_code = 'AQAJcMb62JPal1ySRW8_DBm90zTKP3JPkmuAPeSdcRbiFaWasRSXFep7RxbmM0QCUnKYyXBJCQMlY238oOD6f5N0Y_HBOAgKfSkDVyHlt7Hgmz4oipKaVNw3GzajvvAykPK7KPLUSzp_km0tEFKgwME8WpEAyJB5s3diV7n_qRxxxGmZSCKq40pb4ltn1TpI5RM7ZA6MhRwA4R1Q5-cSFYgSFX58fzfivXW6mOfNtxd_TiFOz69Q0CT5ZJbUbP-eM8MN8dT5yALG-3IeXfY-Ut0GMOScB6OidMMgIx18C7LZTw'  # Fresh authorization code

# Step 1: Exchange Authorization Code for Access Token
token_url = 'https://graph.mapillary.com/token'

data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
}

# Request the access token
response = requests.post(token_url, data=data)


if response.status_code == 200:
    access_token = response.json().get('access_token')
    print('Access Token:', access_token)

    # Step 2: Fetch Images by Bounding Box
    # Define the bounding box for your area (min_longitude, min_latitude, max_longitude, max_latitude)
    bounding_box = (-73.0, 40.7, -72.0, 41.0)  # Example: New York City area

    search_url = 'https://graph.mapillary.com/images'

    # Set parameters for the search
    params = {
        'bbox': ','.join(map(str, bounding_box)),  # Convert bounding box to a comma-separated string
        'fields': 'id,thumb_1024_url,geometry',
        'limit': 100  # Adjust the limit as needed
    }

    # Make the API request for images
    response = requests.get(search_url, headers={'Authorization': f'Bearer {access_token}'}, params=params)

    if response.status_code == 200:
        images = response.json()['data']
        
        # Create a directory to save images if it doesn't exist
        os.makedirs('mapillary_images', exist_ok=True)

        for img in images:
            img_id = img['id']
            img_url = img['thumb_1024_url']
            geometry = img.get('geometry', {})
            coordinates = geometry.get('coordinates', [])

            # Print image details
            print(f'Image ID: {img_id}, URL: {img_url}, Coordinates: {coordinates}')

            # Download the image
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                with open(f'mapillary_images/{img_id}.jpg', 'wb') as f:
                    f.write(img_response.content)
                print(f'Downloaded {img_id}.jpg')
            else:
                print(f'Failed to download image {img_id}.jpg')
    else:
        print('Error fetching images in the specified area:', response.json())
else:
    print('Error exchanging authorization code:', response.json())
