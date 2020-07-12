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

def duplicate_frames(source_path: Path, count):
    inframes_folder = inframes_root / (source_path.stem)
    inframes_folder.mkdir(parents=True, exist_ok=True)
    for i in range(0,count):
        shutil.copyfile(source_path,str(inframes_folder / '%5d.jpg').format(i))

def extract_raw_frames(source_path: Path):
    inframes_folder = inframes_root / (source_path.stem)
    inframe_path_template = str(inframes_folder / '%5d.jpg')
    inframes_folder.mkdir(parents=True, exist_ok=True)
    purge_images(inframes_folder)
    ffmpeg.input(str(source_path)).output(
        str(inframe_path_template), format='image2', vcodec='mjpeg', qscale=0
    ).run(capture_stdout=True)
    NUM_FRAMES = len([name for name in os.listdir(inframes_folder) if os.path.isfile(name)])
    print("Extracted {} video frames to {}".format(NUM_FRAMES,str(inframes_folder)))

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

def save_video(input_video, output_path):
    shutil.copyfile(input_video, output_path)

def vid_format_validate(vid_path : Path) -> Path:
    new_path = vid_path
    ret = 0
    # change containers, copy A/V and timestamps
    if ".flv" in vid_path.name:
        new_path = str(vid_path.replace('.flv','.mp4'))
        if os.path.isfile(new_path) == False:
            ret = os.system(
            'ffmpeg -i "'
            + str(vid_path)
            + '" -c copy -copyts "'
            + str(vid_path.replace('.flv','.mp4'))
            + '"'
            )
        
    elif ".avi" in vid_path.name:
        new_path = str(vid_path.replace('.avi','.mp4'))
        if os.path.isfile(new_path) == False:
            ret = os.system(
            'ffmpeg -i "'
            + str(vid_path)
            + '" -c copy -copyts "'
            + str(vid_path.replace('.avi','.mp4'))
            + '"'
            )
    
    if ".mp4" not in new_path.name or ret != 0:
        raise Exception("Input video not mp4 or can't be converted to mp4")
    return new_path


''' split vid into sections, based on image sz and duration '''
def vid_split_by_size(vid_path : Path) -> list:
    vid_path_list = []
    vid_path_list.append(vid_path)
    '''TODO'''
    # Get video details
    # build -ss -t commands
    # run list of commands, append vid_path with index as first 3 chars
    # save vid_path list to csv for persistance
        # ideally save like 1 | path | done/not done for checkpointing

    #  ffmpeg -ss 00:00:30.00 -i .mp4 -t 00:00:10.00 -c:v copy -c:a copy .mp4
    return vid_path_list

