import subprocess

bashCommand = "ffmpeg -i https://rthkaod3-vh.akamaihd.net/i/m4a/radio/archive/radio2/talkwithyou/m4a/20220124.m4a/master.m3u8 -t 10 out/output.wav"
# bashCommand = ""
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()