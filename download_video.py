import csv
import logging
import os
import shutil
import subprocess


class DownloadVideo():

    def __init__(self) -> None:
        self.vid_title = input(
            "What are we calling this project:\t").strip().replace("\n", "")
        self.vid_name = input(
            "\nWhat should be the title of youtube video reupload \n[do not include 'part' here]:\t").strip().replace("\n", "")

    def get_vid_info(self) -> None:
        """
        if the video link is available in `links.csv` file, then use it.

        else get the link from the user
        """
        with open("speech_text/assets/links.csv", 'r')as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0].strip() == self.vid_title:
                    self.vid_url = row[1]
                    self.aud_url = row[1]
                    return
        self.vid_url = input("\nvideo link:\t").strip()
        self.aud_url = input("\naudio link:\t").strip()

    def get_filepath(self) -> str:
        """Returns the folder path where vid and aud is saved"""
        file_path = os.path.join(
            os.getcwd(), 'speech_text', 'assets', self.vid_title)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        return file_path

    def get_aud_filepath(self, normal: bool = True) -> str:
        """Returns the folder path where audio file is saved"""
        if normal:
            return os.path.join(os.getcwd(), 'speech_text', 'assets', self.vid_title, f'{self.vid_title}.mp3')
        return os.path.join(os.getcwd(), 'speech_text', 'assets', self.vid_title, 'original', f'{self.vid_title}.mp3')

    def get_vid_filepath(self, normal: bool = True) -> str:
        """Returns the folder path where video file is saved"""
        if normal:
            return os.path.join(
                os.getcwd(), 'speech_text', 'assets', self.vid_title, f'{self.vid_title}.mp4')
        return os.path.join(
            os.getcwd(), 'speech_text', 'assets', self.vid_title, 'original', f'{self.vid_title}.mp4')

    def get_captions_filepath(self, model: str) -> str:
        """Returns the folder path where audio file is saved"""
        return f'{os.getcwd()}\\speech_text\\assets\\{self.vid_title}\\srt\\{model}_{self.vid_title}.srt'

    def cleanup(self) -> None:
        file_path = os.path.join(
            os.getcwd(), 'speech_text', 'assets', self.vid_title)
        try:
            shutil.rmtree(file_path, ignore_errors=True)
        except Exception as e:
            logging.error(f"error in deleting folder {file_path} err:{e}")

    def check_if_not_exists(self, normal: bool) -> bool:
        """checks whether video already exists or not"""
        response = True
        if os.path.exists(self.get_vid_filepath(normal)):
            while True:
                prompt = input(
                    "\nyoutube video is already downloaded,\ndo you want to download again?(yes/no):\t").lower()
                if prompt == "yes" or prompt == "y":
                    response = True
                    break
                elif prompt == "no" or prompt == "n":
                    response = False
                    break
                else:
                    logging.error("invalid choice")
        return response

    def download_video(self, normal: bool = True) -> None:
        """
        The link to the youtube video is expected to be passed through command line argument

        Downloads the youtube video and saves it in assets/{yt.title}.
        """
        if self.check_if_not_exists(normal):
            self.get_vid_info()
            self.cleanup()
            file_path = self.get_filepath()
            if normal:
                subprocess.run(
                    f"""yt-dlp -f "bestvideo+bestaudio" -o "{file_path}/{self.vid_title}.%(ext)s" {self.vid_url} && yt-dlp -f "bestaudio" -o "{file_path}/{self.vid_title}.%(ext)s" --extract-audio --audio-format mp3 {self.aud_url}""", shell=True)
            else:
                subprocess.run(
                    f"""yt-dlp -f "bestvideo+bestaudio" -o "{file_path}/original/{self.vid_title}.%(ext)s" {self.vid_url}""", shell=True)

        # get the subtitle/captions file also
        # currently not working
        # subprocess.run(
        #     f"""yt-dlp -f "bestvideo+bestaudio" -o "{file_path}/{self.vid_title}.%(ext)s" --write-subs --sub-lang en --convert-subs srt {self.vid_url} && yt-dlp -f "bestaudio" -o "{file_path}/{self.vid_title}.%(ext)s" --extract-audio --audio-format mp3 {self.aud_url}""", shell=True)


if __name__ == '__main__':
    main = DownloadVideo()
    main.download_video()
