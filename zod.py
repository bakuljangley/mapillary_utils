import json
from collections import Counter
from typing import Dict, List, Set
from mapillary import MapillarySequence, loadMapillarySequence

def loadJSON(path):
    with open(path, "r") as file:
        file = json.load(file)
    return file


def getCountryCounts(frameDict):
    #count countries and number of frames under each country
    country_counts = Counter(frame_data['country_code'] for frame_data in frameDict.values())
    return country_counts


def getMapillaryOverlap(json_file):
    #loads info json file that outlines overlapping sequences with zodframes
    zod_frames_list = loadJSON(json_file)
    zod_frames_dict = {frame['frame_id']: frame for frame in zod_frames_list}
    return zod_frames_dict


class myFrame:
    def __init__(self, frame_id, latitude, longitude, num_photos, unique_sequences):
        self.frame_id = frame_id
        self.latitude = latitude
        self.longitude = longitude
        self.num_photos = num_photos
        self.unique_sequences = unique_sequences

    def getSequences(self):
        #returns overlapped sequences -- for the specific frame
        sequences_ids = [x for x in self.unique_sequences]
        sequences = {}
        for sequence_id in sequences_ids:
            sequences[sequence_id]=loadMapillarySequence(sequence_id)
        return sequences

class myZodData: #a dictionary of frame class types
    def __init__(self):
        self.frames = {}

    def add_frame(self, frame_data):
        frame = myFrame(**frame_data)
        self.frames[frame.frame_id] = frame

    @classmethod
    def from_json(cls, file_path): #loads the frame from a file_path
        zod_data = cls()
        frames_data = getMapillaryOverlap(file_path)
        for frame_data in frames_data.values():
            zod_data.add_frame(frame_data)
        return zod_data

    def get_all_sequences(self): #returns a list of all sequences in the overlap
        all_sequences = set()
        for frame in self.frames.values():
            all_sequences.update(frame.unique_sequences)
        return list(all_sequences)
    
    def __getitem__(self, frame_id): #return frame by frame_id
        return self.frames[frame_id]
    
    def getAllFrames(self):
        return list(self.frames.keys())

    
    




