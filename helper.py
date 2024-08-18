import os


def format_timestamp(seconds: float, always_include_hours: bool = True, decimal_marker: str = ",") -> str:
    """
        Stole this code from OpenAi's whisper codebase

        Converts the normal timestamp into timestamp which is compatible with `.srt` file format
        with slight modification
        """
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return (
        f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    )


def gen_ffmpeg_cmd(vid_title: str, model: str, text: str, font: str = "Tahoma", fontSize: int = 12, cut_cmd: bool = False) -> list[str]:
    """
        generate ffmpeg commands

        `complete_process` --  convert the video into 9:16 ratio and burn the captions onto the video

        `cut_process`      --  cut the long video into 30 second long video

        Parameters
        ----------
        model : str
            model name `"tiny" | "small" | "medium"`
        text : str
            whether ffmpeg should use long or short words srt file `"long" | "short"`
        font : str = Tahoma
            font family to be used to burn the captions
        fontSize : int = 12
            font size
        cut_cmd : bool = False
            id `cut_cmd` is True return the video cutting command
            else caption burning command
    """
    if cut_cmd:
        cut_process = f"""ffmpeg -i speech_text/assets/{vid_title}/{model}/{text}/{text}_{vid_title}.mp4 -c copy -f segment -segment_time 30 -reset_timestamps 1 speech_text/assets/{vid_title}/{model}/broken/{text}_{vid_title}_%03d.mp4"""
        return [cut_process]
    else:
        complete_process = f"""ffmpeg -i speech_text/assets/{vid_title}/{vid_title}.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/{vid_title}/srt/{model}_{vid_title}_{text}.srt:force_style='Alignment=10,FontName={font},FontSize={fontSize},Outline=0,Shadow=0,Bold=1'" -c:a copy speech_text/assets/{vid_title}/{model}/{text}/{text}_{vid_title}.mp4"""
        return [complete_process]


def remove_srt_file(file: str) -> None:
    """remove existing srt file"""
    print(f"removing {file}")
    if os.path.exists(file):
        os.remove(file)


def write_short_captions(filepath: str, vid_title: str, transcript, model: str) -> None:
    """read each word in each segment"""
    print(f"START writing short transciption of {model} model")
    file = f'{filepath}/srt/{model}_{vid_title}_short.srt'
    remove_srt_file(file=file)

    with open(file, "a+")as f:
        stamps = transcript['segments']
        cnt = 0
        for stamp in stamps:
            for word in stamp["words"]:
                cnt = cnt+1
                start = format_timestamp(
                    word['start'])
                end = format_timestamp(word['end'])
                sub = word["word"]
                line = f"{cnt}\n{start} --> {end}\n{sub.strip()}\n"
                f.write(f'{line}\n')
    print(f"FINISH writing short transciption of {model} model")


def write_long_captions(filepath: str, vid_title: str, transcript, model: str) -> None:
    """read each segment"""
    print(f"START writing long transciption of {model} model")
    file = f'{filepath}/srt/{model}_{vid_title}_long.srt'
    remove_srt_file(file)

    with open(file, 'a+')as f:
        stamps = transcript['segments']
        for stamp in stamps:
            id = stamp['id']+1
            start = format_timestamp(stamp['start'])
            end = format_timestamp(stamp['end'])
            sub = stamp['text']
            line = f"{id}\n{start} --> {end}\n{sub.strip()}\n"
            f.write(f'{line}\n')
    print(f"FINISH writing long transciption of {model} model")


def dir_setup(filepath: str) -> None:
    """setup directories to download srt, json and videos files"""
    print("creating directories")
    try:
        # json and srt
        os.makedirs(filepath+'\\json')
        print("Directory -- json")
        os.makedirs(filepath+'\\srt')
        print("Directory -- srt")

        # tiny
        os.makedirs(os.path.join(filepath, 'tiny', 'short'))
        print("Directory -- tiny/short")
        os.makedirs(os.path.join(filepath, 'tiny', 'long'))
        print("Directory -- tiny/long")
        os.makedirs(os.path.join(filepath, 'tiny', 'broken'))
        print("Directory -- tiny/broken")

        # small
        os.makedirs(os.path.join(filepath, 'small', 'short'))
        print("Directory -- small/short")
        os.makedirs(os.path.join(filepath, 'small', 'long'))
        print("Directory -- small/long")
        os.makedirs(os.path.join(
            filepath, 'small', 'broken'))
        print("Directory -- small/broken")

        # medium
        os.makedirs(os.path.join(
            filepath, 'medium', 'short'))
        print("Directory -- medium/short")
        os.makedirs(os.path.join(filepath, 'medium', 'long'))
        print("Directory -- medium/long")
        os.makedirs(os.path.join(
            filepath, 'medium', 'broken'))
        print("Directory -- medium/broken")
    except Exception as e:
        print("could not create one of the necessary directory")
        print(f"err:\t{e}")
