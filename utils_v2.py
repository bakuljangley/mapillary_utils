import requests
import os
import csv
import json
import pandas as pd
import folium
from IPython.display import display

# Define your access token and sequence ID
access_token = 'MLY|8196090173836012|99bcaed29312ec0d1c06b22447943d94'
header = {'Authorization' : 'OAuth {}'.format(access_token)}
metadata_endpoint = "https://graph.mapillary.com"


def getSequence(sequence_id, access_token=access_token, headers=header):
    url = "https://graph.mapillary.com/image_ids?sequence_id={}".format(sequence_id)
    r = requests.get(url, headers=header)
    data_sequence = r.json()
    # print("Number of Images found in Sequence: " + str(len(data_sequence['data'])))
    return data_sequence



def getBoundingBoxImages(testpoint, x_dist, y_dist, access_token=access_token , headers=header):
    # Construct the image search URL with the bounding box
    url_imagesearch = metadata_endpoint + '/images?fields=id,location&bbox={}, {}, {}, {}'.format(
        testpoint[1] - x_dist, testpoint[0] - y_dist,
        testpoint[1] + x_dist, testpoint[0] + y_dist
    )
    # Request to search for images
    response_imagesearch = requests.get(url_imagesearch, headers=headers)
    data_imagesearch = response_imagesearch.json()
    # print("Number of Images found in bounding box: " + str(len(data_imagesearch['data'])))
    return data_imagesearch

def getImage(image_id, access_token=access_token, headers=header):
    url = "https://graph.mapillary.com/:image_ids={}".format(image_id)
    r = requests.get(url, headers=header)
    data_sequence = r.json()
    print(data_sequence)
    #print("Number of Images found in Sequence: " + str(len(data_sequence['data'])))
    return data_sequence



# Define bounding box center and distances to get an area to download from 
x_dist = 0.050
y_dist = 0.050
testpoint = [52.0881575, 5.1143055]  # Example: Center point
zod_sequence_000002 = [52.204000594370456,9.937544328537447]

def saveImages(folder_name, data, headers=header):
    metadata_endpoint = "https://graph.mapillary.com"

    if 'data' in data:
        # Create a directory to save images if it doesn't exist
        os.makedirs(str(folder_name), exist_ok=True)
        csv_file_path = str(folder_name)+'/metadata.csv'
        with open(csv_file_path, mode='w', newline='') as csv_file:
            fieldnames = ['id', 'thumb_2048_url', 'captured_at', 'sequence', 'lat', 'long', 'orientation','rotation','f', 'k1', 'k2', 'sfm_lat', 'sfm_long']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for image in data['data']:
                # Fetch detailed information for each image
                url_image = metadata_endpoint + '/{}?fields=id,thumb_2048_url,captured_at,sequence,geometry,compass_angle,computed_rotation,camera_parameters,computed_geometry'.format(image['id'])
                response_image = requests.get(url_image, headers=headers)
                data_image = response_image.json()

                # Print image data (for debugging)
                #print(data_image)

                # Extract information
                img_id = data_image.get('id')
                img_url = data_image.get('thumb_2048_url')
                captured_at = data_image.get('captured_at')
                sequence = data_image.get('sequence')
                location = data_image.get('geometry')
                sfm_location = data_image.get('computed_geometry')
                orientation = data_image.get('compass_angle')
                rotation = data_image.get('computed_rotation')
                camera_params = data_image.get('camera_parameters')

                # Extract coordinates and orientation
                if location:
                    coordinates = location.get('coordinates')
                    print("coordinates",coordinates)
                    if coordinates:
                        longitude = coordinates[0]
                        latitude = coordinates[1]
                    else:
                        longitude = None
                        latitude = None
                else:
                    longitude = None
                    latitude = None

                #extract sfm location    
                if sfm_location:
                    print("sfm_location: ",sfm_location)
                    sfm_coordinates = sfm_location.get('coordinates')
                    if coordinates:
                        sfm_longitude = sfm_coordinates[0]
                        sfm_latitude = sfm_coordinates[1]
                    else:
                        sfm_longitude = None
                        sfm_latitude = None
                else:
                    sfm_longitude = None
                    sfm_latitude = None

                
                #extract intrinsics
                if camera_params:
                    focal_length = camera_params[0]
                    k1 = camera_params[1]
                    k2 = camera_params[2]
                else: 
                    focal_length = None
                    k1 = None
                    k2 = None


                

                # Save image metadata to CSV
                writer.writerow({
                    'id': img_id,
                    'thumb_2048_url': img_url,
                    'captured_at': captured_at,
                    'sequence': sequence,
                    'lat': latitude,
                    'long': longitude,
                    'orientation': orientation,
                    'rotation': rotation,
                    'f': focal_length,
                    'k1': k1,
                    'k2': k2,
                    'sfm_lat': sfm_latitude,
                    'sfm_long': sfm_longitude
                })

                # Download the image and save it to the local directory
                if img_url:
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        img_filename = f'{folder_name}/{img_id}.jpg'
                        with open(img_filename, 'wb') as f:
                            f.write(img_response.content)
                        print(f'Downloaded {img_id}.jpg')
                    else:
                        print(f'Failed to download image {img_id}.jpg')
                else:
                    print(f'No URL found for image {img_id}')
    else:
        print(f"No images found for sequence.")



def csvPlot(csv_file_path):
    metadata = pd.read_csv(csv_file_path)
    # Create a map centered at the average coordinates
    avg_latitude = metadata['lat'].mean()
    avg_longitude = metadata['long'].mean()
    map_center = [avg_latitude, avg_longitude]

    # Initialize the map
    mymap = folium.Map(location=map_center, zoom_start=15)

    # Add markers for each image's GPS location with orientation
    for index, row in metadata.iterrows():
        lat = row['lat']
        long = row['long']
        img_id = row['id']
        img_url = row['thumb_2048_url']
        angle = row['orientation']  # Assuming this is the compass angle
        
        # Circle with a bold arrow inside, rotating the arrow based on the angle
        icon_html = f"""
        <div style="
            position: relative;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background-color: blue;
            border: 1px solid white;
            text-align: center;
            line-height: 30px;
            ">
            <div style="
                transform: rotate({angle}deg);
                position: absolute;
                top: 50%;
                left: 50%;
                transform-origin: center;
                font-size: 20px;  /* Increased font size */
                font-weight: bold; /* Makes the arrow appear bolder */
                color: black;
                ">
                &#x21E7;  <!-- Thicker arrow character -->
            </div>
        </div>
        """

        # Add the marker with the custom circle + bold arrow icon
        folium.Marker(
            location=[lat, long],
            popup=f'<img src="{img_url}" width="200"><br>ID: {img_id}',
            icon=folium.DivIcon(html=icon_html)
        ).add_to(mymap)

    # Display the map in the Jupyter Notebook
    display(mymap)

def getAreaStats(testpoint, x_dist=0.0005, y_dist=0.0005, access_token=access_token, headers=header):
    # Use the existing getBoundingBoxImages function
    data_imagesearch = getBoundingBoxImages(testpoint, x_dist, y_dist, access_token, headers)
    # print(data_imagesearch)
    if data_imagesearch:
        # Get the number of images
        num_images = len(data_imagesearch['data'])
        
        
        # Get the number of unique sequences
        unique_sequences = set()
        for image in data_imagesearch['data']:
            # Fetch detailed information for each image to get the sequence
            url_image = f"https://graph.mapillary.com/{image['id']}?fields=sequence"
            response_image = requests.get(url_image, headers=headers)
            data_image = response_image.json()
            sequence = data_image.get('sequence')
            if sequence:
                unique_sequences.add(sequence)
        
        num_sequences = len(unique_sequences)
        # Get total images for each unique sequence
        sequence_counts = {}
        for sequence in unique_sequences:
            sequence_data = getSequence(sequence, access_token, headers)
            sequence_counts[sequence] = len(sequence_data['data'])
        
        return num_images, num_sequences, sequence_counts
    else:
        print("No Images found")
        return None, None, None









