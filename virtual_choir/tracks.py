import rpp
import os

MASTER_TRACKS = ['Sopran', 'Alt', 'Tenor', 'Bas']
tr = str.maketrans('ąćęłńóśźż', 'acelnoszz')
dup_names = []

def normalize(string):
    return string.lower().translate(tr)

def simplify_name(name):
    first_name, last_name = normalize(name).split(' ')
    if first_name in dup_names:
        return first_name + '_' + last_name[0]
    return first_name

def get_video_tracks(reaper_path, video_root):
    with open(reaper_path) as f:
        project = rpp.load(f)

    def is_track(element):
        try:
            return element.tag == 'TRACK'
        except:
            return False

    video_files = {normalize(f): f for f in os.listdir(video_root)}
    tracks = filter(is_track, project.children)
    for track in tracks:
        name = track.find('NAME')[1]
        if name in MASTER_TRACKS:
            continue
        norm_name = normalize(name)
        position = track.find('ITEM/POSITION')[1]
        files = [f_name for key, f_name in video_files.items() if norm_name in key]
        if not files:
            raise IOError(f"file not found: {name}\n{norm_name}\n{video_files}")
        yield files[0], position, simplify_name(name)
