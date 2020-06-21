#! python3

import sys
from pytube import YouTube


def get_user_input(user_choice):
    switcher = {
        1: 'adaptive',
        2: 'audio-only',
        3: 'progressive'
    }
    return switcher.get(user_choice)


def _load_app():
    url = input('Paste url: ')
    youtube = YouTube(f'https://youtube.com/watch?v={url}')

    def process_user_choice(user_choice):
        itag = None
        if user_choice == 'adaptive':
            list_of_all_adaptive = youtube.streams.filter(adaptive=True)

            print("All available video/audio for download:")
            [print(video) for video in list_of_all_adaptive]

            itag = (int(input('Provide itag number\nitag=')))
            while not itag:
                itag = (int(input('Provide itag number\nitag=')))

        if user_choice == 'audio-only':
            list_all_audio_only = youtube.streams.filter(only_audio=True)
            print("All available audio for download:")
            [print(audio) for audio in list_all_audio_only]

            itag = (int(input('Provide itag number\nitag=')))
            while not itag:
                itag = (int(input('Provide itag number\nitag=')))

        if user_choice == 'progressive':
            list_all_progressive = youtube.streams.filter(progressive=True)
            print("All available downloads:")
            [print(video) for video in list_all_progressive]

        if itag is not None:
            selected_video = youtube.streams.get_by_itag(itag)
            selected_video.download()

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

    process_user_choice(user_choice=user_input)


if __name__ == '__main__':
    _load_app()
