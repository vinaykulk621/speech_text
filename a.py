import multiprocessing as mp
import subprocess
import srt
import pysubs2


def run(cmd):
    subprocess.run(cmd)


def main():
    job = []
    cmd = [
        # """ffmpeg -i nature.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,pad=iw+40:ih+20:20:20:color=black,subtitles=music.srt:force_style='Alignment=5,FontSize=12'" -c:a copy cropped_output_video_1.mp4""",
        # """ffmpeg -i nature.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,pad=iw+20:ih+20:10:10:color=black,subtitles=music.srt:force_style='Alignment=5,FontSize=10'" -c:a copy cropped_output_video_2.mp4"""
        # """ffmpeg -i nature.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=music.srt:force_style='Alignment=5,FontSize=8,MarginV=0'" -c:a copy cropped_output_video_3.mp4""",
        # """ffmpeg -i nature.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=music.srt:force_style='Alignment=5,FontSize=6,MarginV=ih*1/2'" -c:a copy cropped_output_video_4.mp4"""
        # """ffmpeg -i nature.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=music.srt:force_style='Alignment=5,FontSize=6,MarginV=-ih*1/2'" -c:a copy cropped_output_video_5.mp4"""
        # """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontSize=10'" -c:a copy speech_text/assets/output_video_FontSize=10.mp4""",
        # """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontSize=8,Outline=0,Shadow=0'" -c:a copy speech_text/assets/output_video_2.mp4""",
        # """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontSize=8,Outline=0,Shadow=0,Bold=1'" -c:a copy speech_text/assets/output_video_3.mp4""",
        # """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontSize=8,Outline=0,Shadow=0'" -c:a copy speech_text/assets/output_video_4.mp4""",
        # """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontName=Helvetica,FontSize=8,Outline=0,Shadow=0'" -c:a copy speech_text/assets/output_video_Helvetica.mp4""",
        # """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontName=Helvetica,FontSize=8,Outline=0,Shadow=0,Bold=1'" -c:a copy speech_text/assets/output_video_Helvetica_bold.mp4""",
        # """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontName=Courier,FontSize=8,Outline=0,Shadow=0'" -c:a copy speech_text/assets/output_video_Courier.mp4""",
        # """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontName=Courier,FontSize=8,Outline=0,Shadow=0,Bold=1'" -c:a copy speech_text/assets/output_video_Courier_bold.mp4""",
        """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontName=Impact,FontSize=8,Outline=0,Shadow=0'" -c:a copy speech_text/assets/output_video_Impact.mp4""",
        """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontName=Impact,FontSize=8,Outline=0,Shadow=0,Bold=1'" -c:a copy speech_text/assets/output_video_Impact_bold.mp4""",
        """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontName=Tahoma,FontSize=8,Outline=0,Shadow=0'" -c:a copy speech_text/assets/output_video_Tahoma.mp4""",
        """ffmpeg -i speech_text/assets/video.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920,subtitles=speech_text/assets/music.srt:force_style='Alignment=10,FontName=Tahoma,FontSize=8,Outline=0,Shadow=0,Bold=1'" -c:a copy speech_text/assets/output_video_Tahoma_bold.mp4""",
    ]
    for i, cmd in enumerate(cmd):
        process = mp.Process(target=run, args=(cmd, ))
        process.start()
        job.append(process)

    for j in job:
        j.wait()


def srt_to_ass(srt_file_path, ass_file_path):
    # Read the SRT file
    with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
        srt_content = srt_file.read()

    # Parse the SRT content
    subtitles = list(srt.parse(srt_content))

    # Create a new ASS file
    subs = pysubs2.SSAFile()
    subs.info["title"] = "Converted Subtitle"
    subs.info["wrap_style"] = "0"
    subs.info["play_depth"] = "0"

    # Set default style
    subs.styles["Default"] = pysubs2.SSAStyle(
        fontname="Arial",
        fontsize=20,
        primarycolor=pysubs2.Color(255, 255, 255),
        backcolor=pysubs2.Color(0, 0, 0, 128),
        bold=False,
        italic=False,
        underline=False,
        alignment=pysubs2.Alignment.BOTTOM_CENTER,
        marginl=10,
        marginr=10,
        marginv=10,
    )

    # Convert SRT to ASS
    for subtitle in subtitles:
        subs.append(pysubs2.SSAEvent(
            start=int(subtitle.start.total_seconds() * 1000),
            end=int(subtitle.end.total_seconds() * 1000),
            text=subtitle.content.replace('\n', '\\N')
        ))

    # Save the ASS file
    subs.save(ass_file_path)


if __name__ == '__main__':
    # main()
    srt_to_ass("speech_text/assets/bye/srt/medium_bye_short.srt",
               "speech_text/assets/bye/srt/ass_file.ass")
