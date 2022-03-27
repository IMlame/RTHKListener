import pyaudio
import wave
import sys
import time
import FileInfo

# current audio being played
audio_file_number = -1
# define stream chunk
chunk = 1024


def get_next_file(path: str):
    global audio_file_number
    file_name = ""
    min_distance = sys.maxsize

    # find the next number after audio_file_number
    for file in FileInfo.get_files_in_directory(path):
        # grab first number in file name representing index
        file_index = FileInfo.get_file_index(file)

        if (file_index > audio_file_number) and ((file_index - audio_file_number) < min_distance):
            file_name = file
            min_distance = file_index - audio_file_number

    return file_name


def next_audio_file():
    global audio_file_number
    # wait for audio files to be generated
    while len(FileInfo.get_files_in_directory("out")) == 0:
        print("waiting on audio files...")
        time.sleep(60)

    # find closest index to audio file last played
    file_name = get_next_file(path="out")
    # if there is not a next audio file, loop back to beginning
    if not file_name:
        file_name = FileInfo.get_oldest_file(path="out")

    audio_file_number = FileInfo.get_file_index(file_name)
    return file_name


def play_audio(audio_file):
    print("Now playing:", audio_file)
    # open a wav format music
    f = wave.open(f"out/{audio_file}", "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()