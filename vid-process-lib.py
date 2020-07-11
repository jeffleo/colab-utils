import ffmpeg
import os
from pathlib import Path
import shutil
import re

workfolder = Path('./video')
source_folder = workfolder / "source"
inframes_root = workfolder / "inframes"
audio_root = workfolder / "audio"
outframes_root = workfolder / "outframes"
result_folder = workfolder / "result"

RESULT_VID = None
NUM_FRAMES = 1

def purge_images(dir):
  for f in os.listdir(dir):
    if re.search('.*?\.jpg', f):
      os.remove(os.path.join(dir, f))

def extract_raw_frames(source_path: Path):
    inframes_folder = inframes_root / (source_path.stem)
    inframe_path_template = str(inframes_folder / '%5d.jpg')
    inframes_folder.mkdir(parents=True, exist_ok=True)
    purge_images(inframes_folder)
    ffmpeg.input(str(source_path)).output(
        str(inframe_path_template), format='image2', vcodec='mjpeg', qscale=0
    ).run(capture_stdout=True)
    print("extracted video frames to " + str(inframes_folder))

def get_fps(source_path: Path) -> str:
    print(source_path)
    probe = ffmpeg.probe(str(source_path))
    stream_data = next(
        (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
        None,
    )
    return stream_data['avg_frame_rate']

def build_video(source_path: Path) -> Path:
        out_path = result_folder / (
            source_path.name.replace('.mp4', '_no_audio.mp4')
        )
        outframes_folder = outframes_root / (source_path.stem)
        outframes_path_template = str(outframes_folder / '%5d.jpg')
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if out_path.exists():
            out_path.unlink()
        fps = get_fps(source_path)
        print('Original FPS is: ', fps)

        ffmpeg.input(
            str(outframes_path_template),
            format='image2',
            vcodec='mjpeg',
            framerate=fps,
        ).output(str(out_path), crf=17, vcodec='libx264').run(capture_stdout=True)

        result_path = result_folder / source_path.name
        if result_path.exists():
            result_path.unlink()
        # making copy of non-audio version in case adding back audio doesn't apply or fails.
        shutil.copyfile(str(out_path), str(result_path))

        # adding back sound here
        audio_file = Path(str(source_path).replace('.mp4', '.aac'))
        if audio_file.exists():
            audio_file.unlink()

        os.system(
            'ffmpeg -y -i "'
            + str(source_path)
            + '" -vn -acodec copy "'
            + str(audio_file)
            + '"'
        )

        if audio_file.exists:
            os.system(
                'ffmpeg -y -i "'
                + str(out_path)
                + '" -i "'
                + str(audio_file)
                + '" -shortest -c:v copy -c:a aac -b:a 256k "'
                + str(result_path)
                + '"'
            )
        print('Video created here: ' + str(result_path))
        RESULT_VID = result_path
        return result_path

def save_video(output_path):
    shutil.copyfile(RESULT_VID, output_path)