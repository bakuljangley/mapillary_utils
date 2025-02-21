import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from datetime import datetime
import os


class MapillaryImage: 
    #base class to store metadata about image from mapillary
    #comments; probably can add additional fields such as intrinsics 

    def __init__(self, id, captured_at, sequence, lat, lon, orientation, image_path=None):
        self.id = id
        self.captured_at = captured_at #add a function to convert into a readable time format
        self.sequence = sequence
        self.lat = lat
        self.lon = lon
        self.orientation = orientation
        self.imagepath = image_path if image_path is not None else None
        #self.intrinsics = intrinsics 

    def showImage(self):
        img = mpimg.imread(self.imagepath)
        plt.figure(figsize=(10, 8))
        plt.imshow(img)
        plt.title(f"Image ID: {self.id}\nCapture Time: {self.captured_at}")
        plt.axis('off')
        plt.show()
    
    # def convertTime(self, timestamp):
    #     # Convert milliseconds to seconds
    #     timestamp_seconds = int(timestamp) / 1000
    #     # Convert to datetime object
    #     dt_object = datetime.utcfromtimestamp(timestamp_seconds)
    #     # Format as string
    #     return dt_object.strftime('%Y-%m-%d %H:%M:%S UTC')


class MapillarySequence:
    #class to store objects of the MapillaryImage class from the same sequence
    def __init__(self, sequence_id):
        self.sequence_id = sequence_id
        self.images = []

    def add_image(self, image):
        self.images.append(image)

    def get_image_count(self):
        return len(self.images)

    def get_image_by_index(self, index):
        return self.images[index]

    def get_image_by_id(self, image_id):
        return next((img for img in self.images if img.id == image_id), None)



def loadMapillarySequence(sequence_id, sequence_folder='/Users/bakuljangley/Documents/TUDThesis/mapillary_utils/downloads', verbose=False):
    #COMMENT: make the sequence_folder dynamic
    #expects sequence folder to be a common directory with sequences
    #sequences are stores in sub-directories named after sequence_id
    #with a metadata file --> this function is designed to read the sequence given a string of f
    metadata = f"{sequence_folder}/{sequence_id}/metadata.csv"
    sequences = {}
    
    # Check if the file exists
    if not os.path.exists(metadata):
        if verbose:
            print(f"Metadata file not found for sequence {sequence_id}")
        return None
    
    try:
        with open(metadata, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sequence_id = row['sequence']
                if sequence_id not in sequences:
                    sequences[sequence_id] = MapillarySequence(sequence_id)
                
                image = MapillaryImage(
                    id=row['id'],
                    captured_at=row['captured_at'],
                    sequence=sequence_id,
                    lat=float(row['lat']),
                    lon=float(row['long']),
                    orientation=float(row['orientation']),
                    image_path= f"{sequence_folder}/{row['id']}.jpg"
                )
                sequences[sequence_id].add_image(image)
        
        # Assuming we're dealing with a single sequence, return the first one
        return next(iter(sequences.values()))
    
    except Exception as e:
        print(f"An error occurred while processing sequence {sequence_id}: {str(e)}")
        return None



def cameraMatrixMapillary(focal,width,height): #converting open sfm intrinsics to standard
    K = np.array([ [focal * width, 0, width / 2],
      [0, focal * height, height / 2],
      [0, 0, 1] ])
    
    return K



