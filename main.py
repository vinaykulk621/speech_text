import json
import logging
import subprocess
import time
import multiprocessing as mp
from download_video import DownloadVideo
from helper import dir_setup, gen_ffmpeg_cmd, write_long_captions, write_short_captions
from models import Models


class Main():

    def __init__(self) -> None:
        self.dv = DownloadVideo()
        self.get_short_captions = None
        self.burn_vid_title = True

    def burn_vid_title_on_video(self) -> None:
        """prompt to ask whether to burn the video title on the video"""
        prompt = input(
            "\ndo you want to burn the video title on the video?[default: yes](yes/no):\t").lower()
        if prompt == "yes" or prompt == "y":
            self.burn_vid_title = True
        elif prompt == "no" or prompt == "n":
            self.burn_vid_title = False
        else:
            logging.warn("using default value NO")
            self.burn_vid_title = False

    def short_captions(self) -> None:
        """configure whether you want to extract short captions"""
        prompt = input(
            "\ndo you want to extract short captions? [default value No] (yes/no)?:\t").strip().lower()
        if prompt == "yes" or prompt == "y":
            self.get_short_captions = True
        elif prompt == "no" or prompt == "n":
            self.get_short_captions = False
        else:
            logging.info("Invalid choice\n set to default value No")
            self.get_short_captions = False

    def download_vd(self, normal: bool = True) -> None:
        """download the youtube video and audio only if needed"""
        self.dv.download_video(normal)

    def transcribe(self, model_name: str, model, verbose: bool = False):
        """use OpenAi's whisper model to transcribe the text or dialogues from the audio file"""
        match model_name:
            case "tiny":
                logging.info("tiny model transcribe START")
                tiny_result = model.transcribe(
                    self.dv.get_aud_filepath(),  word_timestamps=True, no_speech_threshold=0.7, verbose=verbose)
                with open(f"speech_text/assets/{self.dv.vid_title}/json/tiny_{self.dv.vid_title}.json", "w")as f:
                    json.dump(tiny_result, f)
                logging.info("tiny model transcribe DONE")
                return tiny_result
            case "small":
                logging.info("small model transcribe START")
                small_result = model.transcribe(
                    self.dv.get_aud_filepath(),  word_timestamps=True, no_speech_threshold=0.7, verbose=verbose)
                with open(f"speech_text/assets/{self.dv.vid_title}/json/small_{self.dv.vid_title}.json", "w")as f:
                    json.dump(small_result, f)
                logging.info("small model transcribe DONE")
                return small_result
            case "medium":
                logging.info("medium model transcribe START")
                medium_result = model.transcribe(
                    self.dv.get_aud_filepath(),  word_timestamps=True, no_speech_threshold=0.7, verbose=verbose)
                with open(f"speech_text/assets/{self.dv.vid_title}/json/medium_{self.dv.vid_title}.json", "w")as f:
                    json.dump(medium_result, f)
                logging.info("medium model transcribe DONE")
                return medium_result
            case _:
                logging.warning(
                    "choose valid model name [tiny, small, medium]")

    def main(self) -> None:
        """gather all the transcripts from 3 models and write the transcript to respective json file"""

        # I fucking hate this
        models = Models()

        # tiny_model
        logging.info("START tiny model and it's transcription")
        tiny_model = models.get_tiny_model()
        tiny_transcript = self.transcribe(model=tiny_model, model_name="tiny")
        del tiny_model
        logging.info("FINISH tiny model transcription and deleted tiny_model")

        # small_model
        logging.info("START small model transcription")
        small_model = models.get_small_model()
        small_transcript = self.transcribe(
            model=small_model, model_name="small")
        del small_model
        logging.info("FINISH small model transcription")

        # medium_model
        logging.info("START medium model transcription")
        medium_model = models.get_medium_model()
        medium_transcript = self.transcribe(
            model=medium_model, model_name="medium")
        del medium_model
        logging.info("FINISH medium model transcription")

        # write long captions into each separate srt file
        write_long_captions(self.dv.get_filepath(),
                            self.dv.vid_title, tiny_transcript, "tiny")
        write_long_captions(self.dv.get_filepath(),
                            self.dv.vid_title, small_transcript, "small")
        write_long_captions(self.dv.get_filepath(),
                            self.dv.vid_title, medium_transcript, "medium")

        if self.get_short_captions:
            # write short captions into each separate srt file
            write_short_captions(self.dv.get_filepath(),
                                 self.dv.vid_title, tiny_transcript, "tiny")
            write_short_captions(self.dv.get_filepath(),
                                 self.dv.vid_title, small_transcript, "small")
            write_short_captions(self.dv.get_filepath(),
                                 self.dv.vid_title, medium_transcript, "medium")

    def run(self, cmd) -> None:
        """Just run the damn command already!!"""
        subprocess.run(cmd)

    def process_video(self) -> None:
        """Process the downloaded video"""

        # how to faltten out a list in python 101
        # https://stackoverflow.com/a/952946/17724990

        # caption burn commands
        # currently i fuckin hate this
        # but i don't have enough energy to change the program structure now
        # will doo it later
        # TODO: Fix this garbage ass code man
        if self.get_short_captions:
            tiny_cmds = sum([gen_ffmpeg_cmd(self.dv.vid_title,  "tiny", "long"),
                             gen_ffmpeg_cmd(self.dv.vid_title, "tiny", "short")], [])
            small_cmds = sum([gen_ffmpeg_cmd(self.dv.vid_title, "small", "long"),
                              gen_ffmpeg_cmd(self.dv.vid_title, "small", "short")], [])
            medium_cmds = sum([gen_ffmpeg_cmd(self.dv.vid_title, "medium", "long"),
                               gen_ffmpeg_cmd(self.dv.vid_title, "medium", "short")], [])

            # cut video into 30s segment commands
            tiny_cut_cmds = sum([gen_ffmpeg_cmd(self.dv.vid_title, "tiny", "long", cut_cmd=True),
                                gen_ffmpeg_cmd(self.dv.vid_title, "tiny", "short", cut_cmd=True)], [])
            small_cut_cmds = sum([gen_ffmpeg_cmd(self.dv.vid_title, "small", "long", cut_cmd=True),
                                  gen_ffmpeg_cmd(self.dv.vid_title, "small", "short", cut_cmd=True)], [])
            medium_cut_cmds = sum([gen_ffmpeg_cmd(self.dv.vid_title, "medium", "long", cut_cmd=True),
                                   gen_ffmpeg_cmd(self.dv.vid_title, "medium", "short", cut_cmd=True)], [])
        else:
            tiny_cmds = gen_ffmpeg_cmd(self.dv.vid_title,  "tiny", "long")
            small_cmds = gen_ffmpeg_cmd(self.dv.vid_title, "small", "long")
            medium_cmds = gen_ffmpeg_cmd(self.dv.vid_title, "medium", "long")

            # cut video into 30s segment commands
            tiny_cut_cmds = gen_ffmpeg_cmd(
                self.dv.vid_title, "tiny", "long", cut_cmd=True)
            small_cut_cmds = gen_ffmpeg_cmd(
                self.dv.vid_title, "small", "long", cut_cmd=True)
            medium_cut_cmds = gen_ffmpeg_cmd(
                self.dv.vid_title, "medium", "long", cut_cmd=True)

        full_cmds = [tiny_cmds, small_cmds, medium_cmds]
        cut_cmds = [tiny_cut_cmds, small_cut_cmds, medium_cut_cmds]

        for cmd in full_cmds:
            with mp.Pool(4)as pool:
                pool.map(self.run, cmd)
        for cmd in cut_cmds:
            with mp.Pool(4)as pool:
                pool.map(self.run, cmd)

    def cut_video(self):
        """ffmpeg command to cut the video and name parts starting from 1"""
        if self.burn_vid_title:
            cmd = f"""ffmpeg -i "speech_text/assets/{self.dv.vid_title}/original/{self.dv.vid_title}.mp4" -vf "crop=ih*9/16:ih,scale=1080:1920,drawtext=fontfile='c\:\/windows\/fonts\/arial.ttf':text={self.dv.vid_name}:fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2" -c:v libx264 -f segment -segment_time 30 -reset_timestamps 1 -segment_start_number 1 "speech_text/assets/{self.dv.vid_title}/broken/{self.dv.vid_name} part %d.mp4" """  # type: ignore
        else:
            cmd = f"""ffmpeg -i "speech_text/assets/{self.dv.vid_title}/original/{self.dv.vid_title}.mp4" -vf "scale=ih*9/16:ih,setsar=1:1" -c copy -f segment -segment_time 30 -reset_timestamps 1 -segment_start_number 1 "speech_text/assets/{self.dv.vid_title}/broken/{self.dv.vid_name} part %d.mp4" """
        subprocess.run(cmd)


def flow_decision(obj: Main) -> None:
    """decides the flow of the program"""
    while True:
        decision = input(
            "\nare we using openai whisper model?(yes/no):\t").lower()
        if decision == "yes" or decision == "y":
            obj.short_captions()
            obj.download_vd()
            dir_setup(obj.dv.get_filepath())
            obj.main()
            obj.process_video()
            break
        elif decision == "no" or decision == "n":
            obj.download_vd(False)
            dir_setup(obj.dv.get_filepath(), long_dirs=False)
            obj.burn_vid_title_on_video()
            obj.cut_video()
            break
        else:
            logging.error("invlid choice")


if __name__ == '__main__':
    start = time.time()
    obj = Main()
    flow_decision(obj)
    end = time.time()
    logging.info(
        f"total process took -- {end-start}s | {round((end-start)/60)}m {round((end-start)/3600)}h")
