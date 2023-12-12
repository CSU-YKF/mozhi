# from https://github.com/facebookresearch/deit/blob/main/samplers.py
# Copyright (c) 2015-present, Facebook, Inc.
# All rights reserved.
#
import torch
import torch.distributed as dist
import math


class RASamplWer(torch.utils.data.Sampler):
    """
    采样器将数据加载限制在分布式数据集的一个子集、重复增强。
    它能确保样本的每个增强版本都能被不同的进程（GPU）看到。
    不同的进程（GPU）主要基于 torch.utils.data.DistributedSampler
    """

    def __init__(self, dataset, num_replicas=None, rank=None, shuffle=True):
        """

        :param dataset: 待采样的数据集。
        :param num_replicas:  进程的数量（GPU）。
        :param rank: 进程的排序（GPU）。
        :param shuffle: 是否打乱数据集。
        """
        if num_replicas is None:  # num_replicas = 1
            if not dist.is_available():  # 如果没有安装分布式包
                raise RuntimeError("Requires distributed package to be available")
            num_replicas = dist.get_world_size()  # 获取进程的数量（GPU）
        if rank is None:  # rank = 0
            if not dist.is_available():
                raise RuntimeError("Requires distributed package to be available")
            rank = dist.get_rank()
        self.dataset = dataset
        self.num_replicas = num_replicas
        self.rank = rank
        self.epoch = 0
        self.num_samples = int(math.ceil(len(self.dataset) * 3.0 / self.num_replicas))  # 采样的数量为数据集的3倍
        self.total_size = self.num_samples * self.num_replicas  # 采样的总数量
        # self.num_selected_samples = int(math.ceil(len(self.dataset) / self.num_replicas))
        self.num_selected_samples = int(math.floor(len(self.dataset) // 256 * 256 / self.num_replicas))
        self.shuffle = shuffle

    def __iter__(self):
        # deterministically shuffle based on epoch
        g = torch.Generator()
        g.manual_seed(self.epoch)
        if self.shuffle:
            indices = torch.randperm(len(self.dataset), generator=g).tolist()
        else:
            indices = list(range(len(self.dataset)))

        # add extra samples to make it evenly divisible
        indices = [ele for ele in indices for i in range(3)]
        indices += indices[:(self.total_size - len(indices))]
        assert len(indices) == self.total_size

        # subsample
        indices = indices[self.rank:self.total_size:self.num_replicas]
        assert len(indices) == self.num_samples

        return iter(indices[:self.num_selected_samples])

    def __len__(self):
        return self.num_selected_samples

    def set_epoch(self, epoch):
        self.epoch = epoch
