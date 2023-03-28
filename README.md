# Multi-Modal Corpus

This is a Python script that allows you to search for videos on TikTok using hashtags and download the video results along with their metadata. This script can be useful for creating a corpus of multimodal data for research purposes.

The script first constructs a URL to send a request to TikTok's search API, using the entered hashtag as a query parameter. Then, it sends a GET request to the constructed URL using the "requests" library.
The response from TikTok's search API is a JSON object containing information about the videos that matched the search query, including each video's metadata (such as title, description, and URL).
The script parses the JSON response to extract the metadata for each video, and saves the metadata to a CSV file that can be specified in the run command.

The metadata stored includes: 
- video id
- video create timestamp
- video duration
- video dig count
- video share count
- video comment count
- video play count
- video description
- video hashtags
- video is_ad
- video stickers
- author username
- author name
- author is_verified
- author follower count
- author following count
- author heartcount
- author video count
- author digg count


To store the videos, the script uses [TikTokApi API](https://github.com/davidteather/TikTok-Api) to download and saves the video usind the video id to the data folder specified in the run command as an MP4 file.

# Getting Started
## Prerequisites
To use this script, you'll need to have Python 3 installed on your computer. You'll also need to install the packages and libraries in the requirements file:
- [Install Python](https://www.python.org/downloads/) 
- Install the required libraries: In the project directory run:
<code>
pip install -r requirements.txt
</code>

## Installation
To get started with this script, first clone the repository:
<code>
git clone git@github.com:saranabhani/multimodal_corpus.git
</code>


Then, navigate to the project directory:
<code>
cd multimodal_corpus
</code>

# Running the Script
To run the script, run the following command:
<code>
python tiktok.py --hashtags [hashtags used to search] --count [number of videos to download] --data_file [path of the metadata file] --data_dir [path to the videos directory] 
</code>
