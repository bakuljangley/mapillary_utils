# README ── .✦

This repository is a collection of utilities meant to interact with Mapillary API (˶ˆᗜˆ˵):
  
1. The Mapillary Dataset is organized into Sequences (`MapillarySequence` class -- collection of Mapillary Images under the same sequence) and Images (`MapillaryImage` class - containing image_id, lat, long, image_path, etc).
2. Additional functionality to download any Mapillary Image/Sequence
3. Visualization tools to plot sequences using the `folium` python library with customizations to add tiles using PDOK (only in NL)
4. ZOD + Mapillary Overlap ⋆˚✿˖°:
   1. Uses `frames.json` to be constructed using the ZOD dataset to extract ZODFRames metadata.
   2. [Downloading and Using the ZOD Dataset](https://zod.zenseact.com)
   3. Overlap between ZODFrames/ZODDrives and Mapillary Sequences within a bounding box of 0.0005deg 
   4. Visualization tools to plot the overlap and inspect ZOD-Mapillary overlap

## TO DOs ── .✦

1. I've implemented custom a custom myZODFrame class that stores lat, long and overlapping sequenc#es list for ease of use with the `MapillarySequence` class. This can be loaded using: `myZodData.from_json(overlap_file)`, which will create a class instance of all the ZODFrames in the overlap file. Subsequently using the class function `getSequences()` will load all the sequences.
2. Right now, to use the files changes have to be made in utils.py to edit in the Mapillary client id etc
3. Probably just add in one jupyter notebook with all examples in one place -- add it to the .gitignore
4. 

## Setting Up Mapillary API ── .✦

To get a client token, register at the [Mapillary Developer Website](https://www.mapillary.com/dashboard/developers).

Set up a Callback url (which is not necessary for the python code but obligatory to set up your profile). To know more read [Authorization](https://www.mapillary.com/connect?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_CALLBACK_URL&response_type=code&scope=images:read) documentation. 

I used [Netlify](https://app.netlify.com/) to host an `.html` file with the following code (it's very basic, like my knowlege of html [(╥﹏╥)] )

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OAuth Callback</title>
</head>
<body>
  <h1>Mapillary OAuth Callback</h1>
  <p id="authorization-code"></p>

  <script>
    // Parse the authorization code from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    
    // Display the authorization code
    if (code) {
      document.getElementById('authorization-code').textContent = `Authorization Code Found`;
    } else {
      document.getElementById('authorization-code').textContent = 'No authorization code found in the URL.';
    }
  </script>
</body>
</html>
```

Your Authorization Link would be : `https://www.mapillary.com/connect?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_CALLBACK_URL&response_type=code&scope=images:read`. You will have to authorize your application each time you want to interact with Mapillary API.

Make sure to:

1. Replace `YOUR_CLIENT_ID` with the Client ID you got from the Mapillary developer dashboard.
2. Replace `YOUR_CALLBACK_URL` with your Netlify-hosted URL (e.g., `https://your-site-name.netlify.app/`).
3. Set the `response_type=code` to get the authorization code.
4. Use `scope=images:read` to ensure that your app has permission to read Mapillary images.

Troubleshooting [( •̀ ᗜ •́ )ᕗ]:

- [Pretty good blog on how to set up Mapillary API](https://stuyts.xyz/2021/10/15/how-to-get-data-from-the-mapillary-api-v4-using-python/)
- [Resource from Mapillary](https://blog.mapillary.com/update/2021/06/23/getting-started-with-the-new-mapillary-api-v4.html)
