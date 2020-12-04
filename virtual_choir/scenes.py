from moviepy.editor import ColorClip, clips_array, concatenate_videoclips
from .config import width, height, fade

def interpret_clip(clips, name, tile_size):
    if type(name) == str:
        return clips[name].resize(tile_size)
    elif callable(name):
        return name(clips, tile_size)
    else:
        return ColorClip(tile_size, (0, 0, 0))

def create_scene(clips, clip_names, root_size = (width, height)):
    root_width, root_height = root_size
    split = len(clip_names)
    tile_size = root_width // split, root_height // split
    scene_clips = [
        [
            interpret_clip(clips, name, tile_size)
            for name
            in row
        ]
        for row
        in clip_names
    ]
    return clips_array(scene_clips).resize(root_size)

def subscene(clip_names):
    def closure(clips, size):
        return create_scene(clips, clip_names, size)
    return closure

def combine_scenes(scenes, audio, start):
    scene_clips = []
    time = start
    for (scene, end_time) in scenes:
        scene_clips.append(scene.subclip(time, end_time + fade).crossfadein(fade))
        time = end_time
    clip = concatenate_videoclips(scene_clips, method='compose', padding=-fade)
    clip = clip.set_audio(audio.subclip(start, time))
    return clip
