import folium
from owslib.wmts import WebMapTileService
from IPython.display import Image
from io import BytesIO
import base64
from PIL import Image as PILImage



def getImageHTML(img_path, width=50, rotate=False):
    # Load and resize the image
    with PILImage.open(img_path) as img:
        if rotate:
            img = img.rotate(-90, expand=True)
        img.thumbnail((width, width))
        # Convert the image to base64
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f'<img src="data:image/jpeg;base64,{img_str}" width="{width}" height="{width}">'

# Function to add Mapillary sequence markers with images as popups
def addMapillarySequenceToMap(map, sequence, color='blue', addwithImages=False):
    for image in sequence.images:
        # Coordinates of the image
        if addwithImages:
            location = [image.lat, image.lon]
        # Create a marker with the image as the popup
            folium.Marker(
                location=location,
                popup=folium.Popup(getImageHTML(image.imagepath), max_width=300),
                icon=folium.Icon(color=color),
                tooltip="Anchor Image"
            ).add_to(map)
        else:
            coordinates = [(img.lat, img.lon) for img in sequence.images]
            
            # Create a polyline for the sequence
            folium.PolyLine(
                locations=coordinates,
                color=color,
                weight=3,
                opacity=0.8,
                popup=f"Sequence: {len(sequence.images)} images"
            ).add_to(map)


def drawBoundingBox(m, point, x_dist=0.0005, y_dist=0.0005):
    #draws a bounding box with default dimensions (in deg)
    #xdist and ydist in degree
    south = point[0] - y_dist
    north = point[0] + y_dist
    west = point[1] - x_dist
    east = point[1] + x_dist
    folium.Rectangle(
        bounds=[[south, west], [north, east]],
        color='red',
        fill=True,
        fillColor='red',
        fillOpacity=0.2,
        weight=2
    ).add_to(m)

def addLayer(m, verbose=False):
    #add layer to folium map m

    #--- PDOK WMTS Service ---
    url = "https://service.pdok.nl/hwh/luchtfotorgb/wmts/v1_0?request=GetCapabilities&service=wmts"

    # Connect to the WMTS service
    wmts = WebMapTileService(url)

    if verbose: # Inspect the available layers and tilematrixsets
        print("Available Layers:", list(wmts.contents.keys()))
        print("Available TileMatrixSets:", list(wmts.tilematrixsets.keys()))

    layer_name = "Actueel_orthoHR"  # Confirm layer name from GetCapabilities
    tilematrixset = "EPSG:3857"  # Confirm tilematrixset from GetCapabilities
    min_zoom = 0  # Adjust these from GetCapabilities
    max_zoom = 15
    #--- Tile URL (CRITICAL - Verify parameters from GetCapabilities XML!) ---
    tiles_url = (
        f"https://service.pdok.nl/hwh/luchtfotorgb/wmts/v1_0?"
        f"service=WMTS&version=1.0.0&request=GetTile&layer={layer_name}"
        f"&tilematrixset={tilematrixset}&tilematrix={{z}}&tilerow={{y}}&tilecol={{x}}&format=image/png"
    )
    
    folium.TileLayer(
        tiles=tiles_url,
        attr="PDOK",
        name="Actueel_ortho25",
        overlay=True,  # Ensure this is an overlay
        max_zoom=max_zoom,  # Adjust this to the *maximum* zoom from GetCapabilities
        min_zoom=min_zoom   # Adjust this to the *minimum* zoom from GetCapabilities
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    return m