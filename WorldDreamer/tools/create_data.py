import argparse

from .data_converter import nuscenes_converter as nuscenes_converter, nuplan_converter


def nuscenes_data_prep(
    root_path,
    info_prefix,
    version,
    dataset_name,
    out_dir,
    max_sweeps=10,
    load_augmented=None,
    only_info=False,
    with_cam_sweeps=False,
):
    """Prepare data related to nuScenes dataset.

    Related data consists of '.pkl' files recording basic infos,
    2D annotations and groundtruth database.

    Args:
        root_path (str): Path of dataset root.
        info_prefix (str): The prefix of info filenames.
        version (str): Dataset version.
        dataset_name (str): The dataset class name.
        out_dir (str): Output directory of the groundtruth database info.
        max_sweeps (int): Number of input consecutive frames. Default: 10
    """
    if load_augmented is None:
        # otherwise, infos must have been created, we just skip.
        nuscenes_converter.create_nuscenes_infos(
            root_path, info_prefix, version=version, max_sweeps=max_sweeps,
            out_path=out_dir, with_cam_sweeps=with_cam_sweeps,
        )
        if only_info:
            return

        # if version == "v1.0-test":
        #     info_test_path = osp.join(root_path, f"{info_prefix}_infos_test.pkl")
        #     nuscenes_converter.export_2d_annotation(root_path, info_test_path, version=version)
        #     return

        # info_train_path = osp.join(root_path, f"{info_prefix}_infos_train.pkl")
        # info_val_path = osp.join(root_path, f"{info_prefix}_infos_val.pkl")
        # nuscenes_converter.export_2d_annotation(root_path, info_train_path, version=version)
        # nuscenes_converter.export_2d_annotation(root_path, info_val_path, version=version)

    # create_groundtruth_database(
    #     dataset_name,
    #     root_path,
    #     info_prefix,
    #     f"{out_dir}/{info_prefix}_infos_train.pkl",
    #     load_augmented=load_augmented,
    # )


def nuplan_data_prep(
    root_path,
    info_prefix,
    version,
    split_yaml,
    dataset_name,
    out_dir,
    map_version="nuplan-maps-v1.0",
    load_augmented=None,
    only_info=False,
):
    """Prepare data related to nuScenes dataset.

    Related data consists of '.pkl' files recording basic infos,
    2D annotations and groundtruth database.

    Args:
        root_path (str): Path of dataset root.
        info_prefix (str): The prefix of info filenames.
        version (str): Dataset version.
        dataset_name (str): The dataset class name.
        out_dir (str): Output directory of the groundtruth database info.
        max_sweeps (int): Number of input consecutive frames. Default: 10
    """
    if load_augmented is None:
        nuplan_converter.create_nuplan_infos(
            root_path,
            info_prefix,
            split_yaml=split_yaml,
            version=version,
            map_version=map_version,
            out_path=out_dir,
        )
        if only_info:
            return

parser = argparse.ArgumentParser(description="Data converter arg parser")
parser.add_argument("dataset", metavar="nuscenes", help="name of the dataset")
parser.add_argument(
    "--root-path",
    type=str,
    default="./data/nuscenes",
    help="specify the root path of dataset",
)
parser.add_argument(
    "--version",
    type=str,
    default="v1.0-trainval",
    required=False,
    help="specify the dataset version, no need for kitti",
)
parser.add_argument(
    "--max-sweeps",
    type=int,
    default=10,
    required=False,
    help="specify sweeps of lidar per example",
)
parser.add_argument(
    "--out-dir",
    type=str,
    default="./data/kitti",
    required=False,
    help="name of info pkl",
)
parser.add_argument(
    "--split-yaml",
    type=str,
    default="./tools/data_converter/nuplan.yaml",
    required=False,
    help="path to the yaml file with ",
)
parser.add_argument("--extra-tag", type=str, default="kitti")
parser.add_argument("--painted", default=False, action="store_true")
parser.add_argument("--with_cam_sweeps", default=False, action="store_true")
parser.add_argument("--virtual", default=False, action="store_true")
parser.add_argument("--only_info", default=False, action="store_true")
parser.add_argument(
    "--workers", type=int, default=4, help="number of threads to be used"
)
args = parser.parse_args()

if __name__ == "__main__":
    load_augmented = None
    if args.virtual:
        if args.painted:
            load_augmented = "mvp"
        else:
            load_augmented = "pointpainting"

    if args.dataset == "nuscenes" and args.version != "v1.0-mini":
        nuscenes_data_prep(
            root_path=args.root_path,
            info_prefix=args.extra_tag,
            version=args.version,
            dataset_name="NuScenesDataset",
            out_dir=args.out_dir,
            max_sweeps=args.max_sweeps,
            load_augmented=load_augmented,
            only_info=args.only_info,
            with_cam_sweeps=args.with_cam_sweeps,
        )
    elif args.dataset == "nuscenes" and args.version == "v1.0-mini":
        train_version = f"{args.version}"
        nuscenes_data_prep(
            root_path=args.root_path,
            info_prefix=args.extra_tag,
            version=train_version,
            dataset_name="NuScenesDataset",
            out_dir=args.out_dir,
            max_sweeps=args.max_sweeps,
            load_augmented=load_augmented,
            only_info=args.only_info,
            with_cam_sweeps=args.with_cam_sweeps,
        )
    elif args.dataset == "nuplan" and args.version != "v1.1-mini":
        nuplan_data_prep(
            root_path=args.root_path,
            info_prefix=args.extra_tag,
            version=args.version,
            split_yaml=args.split_yaml,
            dataset_name="NuPlanDataset",
            out_dir=args.out_dir,
            # max_sweeps=args.max_sweeps,
            load_augmented=load_augmented,
            only_info=args.only_info,
            # with_cam_sweeps=args.with_cam_sweeps,
        )
    elif args.dataset == "nuplan" and args.version == "v1.1-mini":
        nuplan_data_prep(
            root_path=args.root_path,
            info_prefix=args.extra_tag,
            version=args.version,
            split_yaml=args.split_yaml,
            dataset_name="NuPlanDataset",
            out_dir=args.out_dir,
            # max_sweeps=args.max_sweeps,
            load_augmented=load_augmented,
            only_info=args.only_info,
            # with_cam_sweeps=args.with_cam_sweeps,
        )
