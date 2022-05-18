import numpy as np
from import_proj_matl import extract_projmat
import torch
import torch.nn.functional as F
import torch

def photometric_loss_l1(input, target, weight=None):
    """
    photometric loss
    """
    if weight is None:
        weight = torch.ones_like(input)
    return torch.mean(weight * torch.abs(input - target))


def loss(output, target):
    Q=extract_projmat(path='cam_to_cam.yaml')
    if torch.cuda.is_available() and Q.device.type=='cpu' and output.device.type=='gpu':
        Q=Q.cuda()
    output = output.reshape(target.shape)
    valid_idx = target != 0
    valid_num = torch.count_nonzero(valid_idx)
    # print(Q.device)
    # print(Q[2,3].device)
    # print(output.device)
    # print(target.device)
    depth_output = Q[2,3] / (output+Q[3,3])
    depth_target = Q[2,3] / (target+Q[3,3])
    if torch.cuda.is_available() and output.device.type=='gpu':
        R_k = torch.zeros(target.shape).cuda()
    else:
        R_k = torch.zeros(target.shape)
    R_k[valid_idx] = depth_target[valid_idx] - depth_output[valid_idx]
    loss_val = (1 / valid_num) * torch.sum(R_k ** 2) - (1 / valid_num) ** 2 * (torch.sum(R_k) ** 2)
    return loss_val
