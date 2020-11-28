import rpp
import glob

MASTER_TRACKS = ['Sopran', 'Alt', 'Tenor', 'Bas']
tr = str.maketrans('ąćęłńóśźż', 'acelnoszz')
dup_names = []

def simplify_name(name):
    first_name = name.split(' ')[0].lower().translate(tr)
    if first_name in dup_names:
        return first_name + '_' + name.split(' ')[1][0].lower()
    return first_name

def get_video_tracks(reaper_path, video_root):
    with open(reaper_path) as f:
        project = rpp.load(f)

    def is_track(element):
        try:
            return element.tag == 'TRACK'
        except:
            return False

    tracks = filter(is_track, project.children)
    for track in tracks:
        name = track.find('NAME')[1]
        if name in MASTER_TRACKS:
            continue
        position = track.find('ITEM/POSITION')[1]
        files = glob.glob(f'{video_root}/*{name}*')
        if not files:
            raise IOError(f"file not found: {name}")
        yield files[0], position, simplify_name(name)
