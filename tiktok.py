import argparse
import requests
import pandas as pd
from TikTokApi import TikTokApi
import random
import pathlib
import numpy as np
from datetime import datetime, date

# arguments required to pass in the command line
parser = argparse.ArgumentParser()
parser.add_argument("--hashtags", type=str,
                    help="Search hashtags, can be one word or multiple words separated by comma")
parser.add_argument("--count", type=int,
                    help="number of videos to download per hashtag")
parser.add_argument("--data_file", type=str,
                    help="Path to the metadata csv file")
parser.add_argument("--data_dir", type=str,
                    help="Path to the videos directory")

# metadata values to store
headers = ['search_keyword',
           'language',
           'video_id',
           'video_timestamp',
           'video_duration',
           'video_diggcount',
           'video_sharecount',
           'video_commentcount',
           'video_playcount',
           'video_description',
           'video_hashtags',
           'video_is_ad',
           'video_stickers',
           'author_username',
           'author_name',
           'author_verified',
           'author_followercount',
           'author_followingcount',
           'author_heartcount',
           'author_videocount',
           'author_diggcount',
           'download_date']


def tag_search(keyword, offset=0):
    """

    :param keyword: the search keyword/hashtag
    :param offset: number of videos to skip from the top videos list
    :return: metadata of the videos in the search results
    """
    params = {
        'keyword': keyword,
        'offset': offset,
    }
    cookies = {
        'ttwid': 'ttwid', # replace with actual ttwid
        'sessionid': 'sessionid', # replace with actual TikTok sessionid
    }
    request = requests.get("http://us.tiktok.com/api/search/item/full/", params=params, cookies=cookies)
    return request.json()


def get_data_row(video_id, hashtag):
    """

    :param video_id: metadata object of one video
    :param hashtag: hashtag used to get this video
    :return: a dataframe row contains the video metadata
    """
    data_list = [hashtag, '', str(video_id['id'])]
    try:
        ctime = video_id['createTime']
        data_list.append(datetime.fromtimestamp(int(ctime)).strftime('%Y-%m-%d %H:%M:%S'))
    except Exception:
        data_list.append('')
    try:
        data_list.append(video_id['video']['duration'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_id['stats']['diggCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_id['stats']['shareCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_id['stats']['commentCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_id['stats']['playCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_id['desc'])
    except Exception:
        data_list.append('')
    try:
        hashtag_list = [f"#{c['hashtagName']}" for c in video_id['textExtra']]
        data_list.append(','.join(hashtag_list))
    except Exception:
        data_list.append('')
    try:
        data_list.append(video_id['isAd'])
    except Exception:
        data_list.append('')
    try:
        video_stickers = []
        for sticker in video_id['stickersOnItem']:
            for text in sticker['stickerText']:
                video_stickers.append(text)
        data_list.append(';'.join(video_stickers))
    except Exception:
        data_list.append('')
    try:
        data_list.append(video_id['author']['uniqueId'])
    except Exception:
        try:
            data_list.append(video_id['author'])
        except Exception:
            data_list.append('')
    try:
        data_list.append(video_id['author']['nickname'])
    except Exception:
        try:
            data_list.append(video_id['nickname'])
        except Exception:
            data_list.append('')
    try:
        data_list.append(video_id['author']['verified'])
    except Exception:
        data_list.append('')
    try:
        data_list.append(video_id['authorStats']['followerCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_id['authorStats']['followingCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_id['authorStats']['heartCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_id['authorStats']['videoCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(video_id['authorStats']['diggCount'])
    except Exception:
        data_list.append(np.nan)
    try:
        data_list.append(date.today().strftime('%Y-%m-%d'))
    except Exception:
        data_list.append(np.nan)
    data_dict = dict(zip(headers, data_list))
    data_row = pd.DataFrame(data_dict, index=[0])
    return data_row


if __name__ == '__main__':
    args = parser.parse_args()  # parsing commandline arguments
    did = str(random.randint(10000, 999999999))  # generating a random number to use as a device id
    api = TikTokApi(custom_device_id=did)  # connect to the API
    data_file = pathlib.Path(args.data_file)  # path to the metadata file
    if data_file.exists():  # if a metadata file exists
        data_df = pd.read_csv(args.data_file)  # read the file into a dataframe
        data_df['video_id'] = data_df['video_id'].astype("string")  # convert the video_id column to string
    else:  # if no metadata file exists
        data_df = pd.DataFrame(columns=headers)  # create a new dataframe
    hashtags = [tag.strip() for tag in args.hashtags.split(',')]  # read the hashtags from the commandline
    for hashtag in hashtags:  # for each of the hashtags
        try:
            print(hashtag)
            offset = 0
            while offset < args.count:
                res_json = tag_search(hashtag, offset)  # use the search function to retrieve videos metadata
                videos_id = [item['id'] for item in res_json['item_list']]  # get the videos ids
                cnt = 0
                for item in res_json['item_list']:  # for each video
                    if item['id'] not in data_df['video_id'].tolist():  # check if the video is a duplicate
                        try:
                            video = api.video(id=item['id'])
                            video_data = video.bytes()  # download video
                            # write video file
                            with open(f"{args.data_dir}/{item['id']}.mp4", "wb") as out_file:
                                out_file.write(video_data)
                                cnt+=1
                            video_row = get_data_row(item, f'#{hashtag}')  # extract video information
                            data_df = pd.concat([data_df, video_row], ignore_index=True)  # append the video info to the metadata file
                        except Exception:
                            pass
                print(f'Downloaded {cnt} videos')
                offset += cnt
        except Exception:
            pass
    data_df.to_csv(args.data_file, index=False)  # write the metadata dataframe to a csv file


