from email.policy import default
import json
import subprocess
import time
import multiprocessing as mp
from download_video import DownloadVideo
from helper import dir_setup,  gen_ffmpeg_cmd, write_long_captions, write_short_captions
from models import Models


class Main():

    def __init__(self) -> None:
        self.dv = DownloadVideo()

    def download_vd(self) -> None:
        """download the youtube video and audio only if needed"""
        self.dv.download_video()

    def transcribe(self, model_name: str, model, verbose: bool = False):
        """use OpenAi's whisper model to transcribe the text or dialogues from the audio file"""
        match model_name:
            case "tiny":
                print("tiny model transcribe START")
                tiny_result = model.transcribe(
                    self.dv.get_aud_filepath(),  word_timestamps=True, no_speech_threshold=0.7, verbose=verbose)
                with open(f"speech_text/assets/{self.dv.vid_title}/json/tiny_{self.dv.vid_title}.json", "w")as f:
                    json.dump(tiny_result, f)
                print("tiny model transcribe DONE")
                return tiny_result
            case "small":
                print("small model transcribe START")
                small_result = model.transcribe(
                    self.dv.get_aud_filepath(),  word_timestamps=True, no_speech_threshold=0.7, verbose=verbose)
                with open(f"speech_text/assets/{self.dv.vid_title}/json/small_{self.dv.vid_title}.json", "w")as f:
                    json.dump(small_result, f)
                print("small model transcribe DONE")
                return small_result
            case "medium":
                print("medium model transcribe START")
                medium_result = model.transcribe(
                    self.dv.get_aud_filepath(),  word_timestamps=True, no_speech_threshold=0.7, verbose=verbose)
                with open(f"speech_text/assets/{self.dv.vid_title}/json/medium_{self.dv.vid_title}.json", "w")as f:
                    json.dump(medium_result, f)
                print("medium model transcribe DONE")
                return medium_result
            case _:
                print("choose valid model name [tiny, small, medium]")

    def main(self) -> None:
        """gather all the transcripts from 3 models and write the transcript to respective json file"""

        # I fucking hate this
        models = Models()

        # tiny_model
        print("START tiny model and it's transcription")
        tiny_model = models.get_tiny_model()
        tiny_transcript = self.transcribe(model=tiny_model, model_name="tiny")
        del tiny_model
        print("FINISH tiny model transcription and deleted tiny_model")

        # small_model
        print("START small model transcription")
        small_model = models.get_small_model()
        small_transcript = self.transcribe(
            model=small_model, model_name="small")
        del small_model
        print("FINISH small model transcription")

        # medium_model
        print("START medium model transcription")
        medium_model = models.get_medium_model()
        medium_transcript = self.transcribe(
            model=medium_model, model_name="medium")
        del medium_model
        print("FINISH medium model transcription")

        # write long captions into each separate srt file
        write_long_captions(self.dv.get_filepath(),
                            self.dv.vid_title, tiny_transcript, "tiny")
        write_long_captions(self.dv.get_filepath(),
                            self.dv.vid_title, small_transcript, "small")
        write_long_captions(self.dv.get_filepath(),
                            self.dv.vid_title, medium_transcript, "medium")

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

        models = [tiny_cmds,
                  small_cmds,
                  medium_cmds,
                  tiny_cut_cmds,
                  small_cut_cmds,
                  medium_cut_cmds]

        for model in models:
            with mp.Pool(4)as pool:
                pool.map(self.run, model)


if __name__ == '__main__':
    start = time.time()
    obj = Main()
    obj.download_vd()
    print("video download complete")
    dir_setup(obj.dv.get_filepath())
    obj.main()
    obj.process_video()
    end = time.time()
    print(
        f"total process took -- {end-start}s | {round((end-start)/60)}m {round((end-start)/3600)}h")
