import platform

from mmcv.utils import Registry, build_from_cfg
from mmdet.datasets import DATASETS
from mmdet.datasets.builder import _concat_dataset

if platform.system() != "Windows":
    # https://github.com/pytorch/pytorch/issues/973
    import resource

    rlimit = resource.getrlimit(resource.RLIMIT_NOFILE)
    base_soft_limit = rlimit[0]
    hard_limit = rlimit[1]
    soft_limit = min(max(4096, base_soft_limit), hard_limit)
    resource.setrlimit(resource.RLIMIT_NOFILE, (soft_limit, hard_limit))

OBJECTSAMPLERS = Registry("Object sampler")


def build_dataset(cfg, default_args=None):
    from mmdet3d.datasets.dataset_wrappers import CBGSDataset
    from mmdet.datasets.dataset_wrappers import (
        ClassBalancedDataset,
        ConcatDataset,
        RepeatDataset,
    )

    if isinstance(cfg, (list, tuple)):
        dataset = ConcatDataset([build_dataset(c, default_args) for c in cfg])
    elif "type" in cfg and cfg["type"] == "ConcatDataset":
        dataset = ConcatDataset(
            [build_dataset(c, default_args) for c in cfg["datasets"]],
            cfg.get("separate_eval", True),
        )
    elif "type" in cfg and cfg["type"] == "RepeatDataset":
        dataset = RepeatDataset(
            build_dataset(cfg["dataset"], default_args), cfg["times"]
        )
    elif "type" in cfg and cfg["type"] == "ClassBalancedDataset":
        dataset = ClassBalancedDataset(
            build_dataset(cfg["dataset"], default_args), cfg["oversample_thr"]
        )
    elif "type" in cfg and cfg["type"] == "CBGSDataset":
        dataset = CBGSDataset(build_dataset(cfg["dataset"], default_args))
    elif "ann_file" in cfg and isinstance(cfg.get("ann_file"), (list, tuple)):
        dataset = _concat_dataset(cfg, default_args)
    elif "nuscenes" in cfg and "nuplan" in cfg:
        dataset_keys = ["nuscenes", "nuplan"]
        dataset = ConcatDataset(
            [build_dataset(cfg[c], default_args) for c in dataset_keys]
        ) 
    elif "nuscenes" in cfg and isinstance(cfg, dict):
        dataset = build_from_cfg(cfg["nuscenes"], DATASETS, default_args)
    elif "nuplan" in cfg and isinstance(cfg, dict):
        dataset = build_from_cfg(cfg["nuplan"], DATASETS, default_args)
    else:
        dataset = build_from_cfg(cfg, DATASETS, default_args)

    return dataset
