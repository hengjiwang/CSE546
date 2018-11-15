from nilearn import plotting, datasets, image
import data_load
import argparse
import nibabel as nib
import numpy as np
import os
import pyprind


def plot(path, subjects):
    """
    Reads the data and plots images given the voxel data.
    """
    transformToXYZmm = np.array([[-3.125, 0, 0, 81.250], [0, 3.125, 0, -115.625], [0, 0, 6, -54.000], [0, 0, 0, 1.000]])
    data = data_load.load_data(path, subjects)
    dimx = int(data[0]["meta"]["dimx"][0])
    dimy = int(data[0]["meta"]["dimy"][0])
    dimz = int(data[0]["meta"]["dimz"][0])
    coordToCol = data[0]["meta"]["coordToCol"][0][0]
    images = {}
    max_val = 0
    voxels = np.load("data/general_selected_500_1.npy")
    directory = os.listdir("data/input/")
    bar = pyprind.ProgBar(len(directory), title='Info extraction and Image Building')
    bar2 = pyprind.ProgBar(len(images.keys()), title='Saving Pictures')
    for file in directory:
        file_name = "data/input/{}".format(file)
        fh = open(file_name)
        activation_values = np.asarray(list(map(lambda x: float(x), filter(lambda x: x != '', fh.read().split(",")))))
        fh.close()
        plot_matrix = np.zeros((dimx, dimy, dimz))
        for x in range(dimx):
            for y in range(dimy):
                for z in range(dimz):
                    indice = coordToCol[x][y][z]
                    if indice != 0:
                        if indice in list(voxels):
                            voxel_indice = list(voxels).index(indice)
                            value = activation_values[voxel_indice]
                            if abs(value) > max_val:
                                max_val = abs(value)
                            plot_matrix[x][y][z] = value
        image = nib.Nifti1Image(plot_matrix, transformToXYZmm)
        images[file_name] = image
        bar.update(force_flush=True)
    print(bar)
    for image in images:
        plotting.plot_glass_brain(images[image], display_mode='ortho', vmax=max_val, plot_abs=False, threshold=None, colorbar=True, output_file="{}-wom1.png".format(image))
        bar2.update(force_flush=True)
    print(bar2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot brain images from voxel data")
    parser.add_argument("path", type=str, help="Path to voxel data")
    parser.add_argument("subjects", type=int, help="Number of subjects")
    args = parser.parse_args()
    plot(args.path, args.subjects)