import csv
import os
import shutil
import subprocess


class DownloadVideo():

    def __init__(self) -> None:
        self.vid_title = input(
            "What do you want to save this project as:\t").strip()

    def get_vid_info(self) -> None:
        """
        if the video link is available in `links.csv` file, then use it.

        else get the link from the user
        """
        with open("speech_text/assets/links.csv", 'r')as f:
            reader = csv.reader(f)
        for row in reader:
            if row[0] == self.vid_title:
                self.vid_url = row[1]
                self.aud_url = row[1]
                return
        self.vid_url = input("Video link:\t").strip()
        self.aud_url = input("Audio link:\t").strip()

    def get_filepath(self) -> str:
        """Returns the folder path where vid and aud is saved"""
        file_path = os.path.join(
            os.getcwd(), 'speech_text', 'assets', self.vid_title)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        return file_path

    def get_aud_filepath(self) -> str:
        """Returns the folder path where audio file is saved"""
        return os.path.join(os.getcwd(), 'speech_text', 'assets', self.vid_title, f'{self.vid_title}.mp3')

    def get_captions_filepath(self, model: str) -> str:
        """Returns the folder path where audio file is saved"""
        return f'{os.getcwd()}\\speech_text\\assets\\{self.vid_title}\\srt\\{model}_{self.vid_title}.srt'

    def get_vid_filepath(self) -> str:
        """Returns the folder path where video file is saved"""
        return os.path.join(
            os.getcwd(), 'speech_text', 'assets', self.vid_title, f'{self.vid_title}.mp4')

    def cleanup(self) -> None:
        file_path = os.path.join(
            os.getcwd(), 'speech_text', 'assets', self.vid_title)
        try:
            shutil.rmtree(file_path, ignore_errors=True)
        except Exception as e:
            print(f"Error in deleting folder {file_path}")
            print(f"Error {e}")

    def download_video(self) -> None:
        """
        The link to the youtube video is expected to be passed through command line argument

        Downloads the youtube video and saves it in assets/{yt.title}.
        """
        self.get_vid_info()
        self.cleanup()
        file_path = self.get_filepath()
        subprocess.run(
            f"""yt-dlp -f "bestvideo+bestaudio" -o "{file_path}/{self.vid_title}.%(ext)s" {self.vid_url} && yt-dlp -f "bestaudio" -o "{file_path}/{self.vid_title}.%(ext)s" --extract-audio --audio-format mp3 {self.aud_url}""", shell=True)


if __name__ == '__main__':
    main = DownloadVideo()
    main.download_video()
