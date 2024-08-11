import multiprocessing as mp
import subprocess


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


if __name__ == '__main__':
    main()
