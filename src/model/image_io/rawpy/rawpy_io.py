import rawpy


def load_neutral_image_16_bit(path):
    with rawpy.imread(path) as raw:
        return raw.postprocess(gamma=(1, 1), no_auto_bright=True, output_bps=16)
