from moviepy.editor import ColorClip, CompositeVideoClip, clips_array, concatenate_videoclips
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

def span(row_range, col_range, name):
    row, rows = row_range
    col, cols = col_range
    def closure(clips, size, split):
        width, height = size
        clip = clips[name]
        x = (row / split) * width
        y = (col / split) * height
        w = (rows / split) * width
        h = (cols / split) * height
        return clip.resize((w, h)).set_position((x, y))
    return closure

def create_superscene(clips, clip_names, spans, root_size = (width, height)):
    base_scene = create_scene(clips, clip_names, root_size)
    split = len(clip_names)
    span_clips = [span(clips, root_size, split) for span in spans]
    return CompositeVideoClip([base_scene] + span_clips)


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
