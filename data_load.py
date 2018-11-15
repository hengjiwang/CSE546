import os
import scipy.io as sio


def load_data(path, subjects):

    # for 1 subject
    # 60 word-picture pairs
    # 360 trials (60 * 6 repetitions)
    # 21764 voxels (CHANGES per person)

    # datasets[0]["data"]          -> 360 trials
    # datasets[0]["data"][0][0][0] -> first trial array
    # datasets[0]["data"][1][0][0] -> second trial array

    # trial array = 21764 voxels (real number)
    datasets = []
    for dt in range(1, subjects + 1):
        dataset_name = os.path.join(path, "data-science-P" + str(dt) + ".mat")
        dataset = sio.loadmat(dataset_name)
        datasets.append(dataset)
    return datasets
    