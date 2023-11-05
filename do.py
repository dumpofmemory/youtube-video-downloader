#! python3

import sys
from pytube import YouTube
import re
import os

os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/Cellar/ffmpeg/6.0_1/bin/ffmpeg"
from moviepy.editor import *


def convert_mp4_to_mp3(mp4_path, mp3_path):
    command = f"ffmpeg -i {mp4_path} -vn -ar 44100 -ac 2 -b:a 192k {mp3_path}"
    os.system(command)


current_working_directory = os.getcwd()
download_path = f"{current_working_directory}/downloads"


def get_user_input(user_choice):
    switcher = {
        1: 'adaptive',
        2: 'audio-only',
        3: 'progressive'
    }
    return switcher.get(user_choice)


def _load_app():
    url_search_result = ""
    youtube = None

    try:
        url = input('Paste url: ')

        try:
            url_search_result = re.search(r'v=.*&', url).group(0)[2:-1]
            print(url_search_result)
        except AttributeError:
            url_search_result = re.search(r'(.be/).*', url).group(0)[4:]
            print(url_search_result)
    except IndexError:
        url = input('Paste url: ')
    except Exception as e:
        print(e)
        url = input('Paste url: ')

    while not url:
        try:
            url = input('Paste url: ')
        except Exception as e:
            print(e)
            url = input('Paste url: ')

    if url_search_result:
        youtube = YouTube(f'https://youtube.com/watch?v={url_search_result}')

    def process_user_choice(user_choice):
        itag = None
        if user_choice == 'adaptive':
            list_of_all_adaptive = youtube.streams.filter(adaptive=True)

            itag = get_itag(list_of_all_adaptive)

        if user_choice == 'audio-only':
            list_all_audio_only = youtube.streams.filter(only_audio=True)

            itag = get_itag(list_all_audio_only)

            selected_video = youtube.streams.get_by_itag(itag)
            download = selected_video.download(output_path=download_path)

            convert_mp4_to_mp3(download, f'{download_path}/output.mp3')

        if user_choice == 'progressive':
            list_all_progressive = youtube.streams.filter(progressive=True)

            itag = get_itag(list_all_progressive)

        selected_video = youtube.streams.get_by_itag(itag)
        download = selected_video.download(output_path=download_path)
        return download

    def get_itag(list_of_downloads):
        print("All available video/audio for download:")
        [print(list_item) for list_item in list_of_downloads]

        itag = (int(input('Provide itag number\nitag=')))
        while not itag:
            itag = (int(input('Provide itag number\nitag=')))

        return itag

    user_input = None
    print(
        '''
        #1 - Adaptive download: video only/audio only (for high res videos)
        #2 - Download audio only
        #3 - Progressive download (legacy, supports only 720p resolution videos)
        '''
    )

    try:
        while not user_input:
            user_input = (int(input('Choose a number from above\n#')))

    except ValueError:
        while type(user_input) is not int:
            try:
                print("%s is not an integer." % user_input)

                user_input = (int(input('Choose a number from above \n#')))
            except ValueError:
                continue

            except KeyboardInterrupt:
                sys.exit()

    except KeyboardInterrupt:
        print("Aborting and exiting script execution")
        sys.exit()

    user_input = get_user_input(user_choice=user_input)
    while user_input is None:
        try:
            user_input = (int(input('Wrong input. Choose a number from above.\n#')))

            user_input = get_user_input(user_choice=user_input)
        except ValueError:
            pass

        except KeyboardInterrupt:
            print("Aborting and exiting script execution")
            sys.exit()

    if user_input != 'audio-only':
        user_choice_mp3 = input("Rename .mp4 file to .mp3? (y/n): ")
        if user_choice_mp3 == "y":
            res_download = process_user_choice(user_choice=user_input)
            download_filename = \
                re.sub(current_working_directory, '', res_download).split('.mp4')[0]
            print(res_download)
            video = VideoFileClip(res_download)
            video.audio.write_audiofile(f'{download_filename}.mp3')

    process_user_choice(user_choice=user_input)


if __name__ == '__main__':
    _load_app()
