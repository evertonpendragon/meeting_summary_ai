from moviepy.editor import *
import uuid


def mp4_to_mp3(mp4_filename, mp3_filename):
    to_convert = AudioFileClip(mp4_filename)
    to_convert.write_audiofile(mp3_filename)
    to_convert.close()



if __name__ == "__main__":
    mp4_filename="C:\\Users\\evert\\VSCode Projects\\meeting_summary_ai\\meeting_summary_ai\\meeting_mp4\\entrevista de Boechat com Jô Soares 360.mp4"
    mp3_filename="C:\\Users\\evert\\VSCode Projects\\meeting_summary_ai\\meeting_summary_ai\\meeting_mp3\\{arq_mp3}.mp3".format(arq_mp3=uuid.uuid4().hex)
    mp4_to_mp3(mp4_filename, mp3_filename)