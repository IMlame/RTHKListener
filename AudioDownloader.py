import requests
import re
from datetime import datetime, timedelta
import subprocess
import os
import FileInfo

queue_size = 10
radio_num = 2
days_offset = 0

offset_date = datetime.today() - timedelta(days=2)

date = str(offset_date.strftime("%Y%m%d"))


def get_audio_urls(radio_num, date):
    # grab today's url
    daily_url = f"https://programme.rthk.hk/channel/radio/txt_timetable.php?mychannel=radio{radio_num}&mydate={date}&lang=eng"
    r = requests.get(daily_url)

    # grab segment urls
    broadcast_urls = re.findall(
        f"player_txt\.php\?mychannel=radio{radio_num}&mydate=[0-9]{{8}}&mytime=[0-9]{{4}}&lang=eng", r.text)

    # list of audio urls to be grabbed
    audio_urls = []

    for url in broadcast_urls:
        # grab m3u8 audio urls from segment html
        r = requests.get("https://programme.rthk.hk/channel/radio/" + url)
        m3u8_url = re.search("hlsStreamUrl\[0\]='(.*)'", r.text)
        audio_urls.append(m3u8_url.group(1))
    return audio_urls


def download_audio(path: str, url, date):
    # format of audio file name: "index-date-radio-broadcast_name"
    audio_file_name = generate_audio_file_name(path, url)

    # download segment
    bashCommand = f"ffmpeg -i {url} -t 100000 -loglevel quiet out/{audio_file_name}.wav"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def generate_audio_file_name(path: str, url: str):
    newest_file = FileInfo.get_newest_file_name(path)
    index = 0
    # if there exists a file, grab index and add one to its index
    if newest_file:
        index = FileInfo.get_file_index(newest_file) + 1

    # grab info from url to name audio files
    info = re.search("(radio[0-9])\/(.*?)\/", url)
    radio = info.group(1)
    broadcast_name = info.group(2)
    return f"{index}-{date}-{radio}-{broadcast_name}"


def is_new(url):
    for file in FileInfo.get_files_in_directory("out"):
        # convert url to file name
        url_file_name = generate_audio_file_name("out", url)
        regex_search = "[0-9]*-([0-9]*-[a-zA-Z0-9]*-[a-zA-Z0-9]*)[\.wav]?"
        if re.search(regex_search, url_file_name).group(1) == re.search(regex_search, file).group(1):
            return False


    return True


def audio_file_updater():
    urls = get_audio_urls(radio_num, date)
    for url in urls:
        if is_new(url):
            print("Downloading", url + ".wav")
            download_audio("out", url, date)

    oldest_file = FileInfo.get_oldest_file("out")
    # remove files if number of audio files is larger than queue size, but only if files are from an older date
    while (len(FileInfo.get_files_in_directory("out")) > queue_size) and FileInfo.get_file_date(oldest_file) != date:
        oldest_file = FileInfo.get_oldest_file("out")
        print("Queue over sized! Removed", oldest_file)
        os.remove(f"out/{oldest_file}")

