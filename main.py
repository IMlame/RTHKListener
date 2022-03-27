import threading
import time
import sys

import AudioDownloader
import AudioPlayer

def main(args):
    # main thread
    t1 = threading.Thread(target=audio_download, name='audio_downloader')
    # listener thread
    t2 = threading.Thread(target=audio_play, name='audio_player')

    t1.start()
    t2.start()

def audio_download():
    while True:
        # attempt to download audio clips every 60 minutes
        AudioDownloader.audio_file_updater()
        time.sleep(60*60)

def audio_play():
    while True:
        audio_file = AudioPlayer.next_audio_file()
        AudioPlayer.play_audio(audio_file)

if __name__ == "__main__":
    main(sys.argv)