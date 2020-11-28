import random
from scenes import create_scene, subscene

def sub(indices):
    def closure(names):
        return subscene(from_indices(indices, names))
    return closure

def from_indices(indices, names):
    return [
        [
            names[index] if type(index) == int
            else index(names)
            for index
            in row
        ]
        for row
        in indices
    ]

def build_scenes(indices, clips, names):
    return [
        create_scene(clips, from_indices(scene_indices, names))
        for scene_indices in indices
    ]

def sequence_3x3(clips, base_order):
    return build_scenes([
        [[1,10,7],[6,11,2],[5,9,4]],
        [[1,3,7],[6,11,13],[15,9,4]],
        [[1,3,0],[12,11,13],[15,14,4]],
        [[5,3,0],[12,2,13],[15,14,10]],
    ], clips, base_order)

def sequence_2x2_to_4x4_split(clips, base_order):
    return build_scenes([
        [[4,3],[12,11]],
        [[4,sub([[2,3],[6,7]])],[12,11]],
        [[4,sub([[2,3],[6,7]])],[sub([[8,9],[12,13]]),11]],
        [[sub([[0,1],[4,5]]),sub([[2,3],[6,7]])],[sub([[8,9],[12,13]]),11]],
    ], clips, base_order)
