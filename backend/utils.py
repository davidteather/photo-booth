import rawpy
import imageio

def convert_arw_to_jpeg(arw_path, jpeg_path):
    # TODO: Might have to play around with more options to get a good conversion
    #       If so, might just be worth using camera to have RAW & jpeg
    #  Params: https://letmaik.github.io/rawpy/api/rawpy.Params.html
    # TODO: This also takes awhile to process
    with rawpy.imread(arw_path) as raw:
        rgb = raw.postprocess(use_camera_wb=True)
    imageio.imsave(jpeg_path, rgb)