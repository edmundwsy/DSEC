import torch
import math
from model.loss import *

def lg10(x):
    return torch.div(torch.log(x), math.log(10))

def maxOfTwo(x, y):
    z = x.clone()
    maskYLarger = torch.lt(x, y)
    z[maskYLarger.detach()] = y[maskYLarger.detach()]
    return z


def accuracy(output, target):
    with torch.no_grad():
        pred = torch.argmax(output, dim=1)
        assert pred.shape[0] == len(target)
        correct = 0
        correct += torch.sum(pred == target).item()
    return correct / len(target)


def top_k_acc(output, target, k=3):
    with torch.no_grad():
        pred = torch.topk(output, k, dim=1)[1]
        assert pred.shape[0] == len(target)
        correct = 0
        for i in range(k):
            correct += torch.sum(pred[:, i] == target).item()
    return correct / len(target)


def mean_square_error(output, target):
    with torch.no_grad():
        Q=get_projectmat()
        if torch.cuda.is_available() and Q.device.type == "cpu":
            Q = Q.cuda()
        valid_idx = target != 0
        valid_num = torch.count_nonzero(valid_idx)
        invalid_idx = target == 0
        depth_target = Q[2, 3] / ((target - Q[3, 3])*Q[3,2])
        depth_target = torch.clamp(depth_target,0,80)
        depth_target[invalid_idx] = 0
        depth_target = depth_target/torch.amax(torch.amax(depth_target,1,keepdims=True),2,keepdims=True)
        depth_target *= 80
        depth_output = from_log_to_depth(output.reshape(depth_target.shape))
        diffMatrix = torch.abs(depth_output - depth_target)
        diffMatrix[invalid_idx]=0
        return torch.sum(torch.pow(diffMatrix, 2)) / valid_num


def mean_absolute_error(output, target):
    with torch.no_grad():
        Q=get_projectmat()
        if torch.cuda.is_available() and Q.device.type == "cpu":
            Q = Q.cuda()
        valid_idx = target != 0
        valid_num = torch.count_nonzero(valid_idx)
        invalid_idx = target == 0
        depth_target = Q[2, 3] / ((target - Q[3, 3])*Q[3,2])
        depth_target = torch.clamp(depth_target,0,80)
        depth_target[invalid_idx] = 0
        depth_target = depth_target/torch.amax(torch.amax(depth_target,1,keepdims=True),2,keepdims=True)
        depth_target *= 80
        depth_output = from_log_to_depth(output.reshape(depth_target.shape))
        diffMatrix = torch.abs(depth_output - depth_target)
        diffMatrix[invalid_idx]=0
        return torch.sum(diffMatrix) / valid_num


def abs_rel_error(output, target):
    with torch.no_grad():
        diffMatrix = torch.abs(output - target)
        realMatrix = torch.div(diffMatrix, target)
        return torch.sum(realMatrix) / realMatrix.numel()

def lg10_error(output, target):
    with torch.no_grad():
        LG10Matrix = torch.abs(lg10(output) - lg10(target))
        return torch.sum(LG10Matrix) / LG10Matrix.numel()
    
def delta1_error(output, target):
    with torch.no_grad():
        yOverZ = torch.div(output, target)
        zOverY = torch.div(target, output)
        maxRatio = maxOfTwo(yOverZ, zOverY)

        return torch.sum(torch.le(maxRatio, 1.25).float()) / maxRatio.numel()

def delta2_error(output, target):
    with torch.no_grad():
        yOverZ = torch.div(output, target)
        zOverY = torch.div(target, output)
        maxRatio = maxOfTwo(yOverZ, zOverY)

        return torch.sum(torch.le(maxRatio, math.pow(1.25, 2)).float()) / maxRatio.numel()


def delta3_error(output, target):
    with torch.no_grad():
        yOverZ = torch.div(output, target)
        zOverY = torch.div(target, output)
        maxRatio = maxOfTwo(yOverZ, zOverY)

        return torch.sum(torch.le(maxRatio, math.pow(1.25, 3)).float()) / maxRatio.numel()
def mean_absolute_error_10(output, target):
    with torch.no_grad():
        Q=get_projectmat()
        if torch.cuda.is_available() and Q.device.type == "cpu":
            Q = Q.cuda()
        invalid_idx = target == 0
        depth_target = Q[2, 3] / ((target - Q[3, 3])*Q[3,2])
        depth_target = torch.clamp(depth_target,0,80)
        depth_target[invalid_idx] = 0
        invalid_idx=invalid_idx+(depth_target>10)
        valid_num = torch.count_nonzero(~invalid_idx)
        depth_target = depth_target/torch.amax(torch.amax(depth_target,1,keepdims=True),2,keepdims=True)
        depth_target *= 80
        depth_output = from_log_to_depth(output.reshape(depth_target.shape))
        diffMatrix = torch.abs(depth_output - depth_target)
        diffMatrix[invalid_idx]=0
        return torch.sum(diffMatrix) / valid_num 
def mean_absolute_error_20(output, target):
    with torch.no_grad():
        Q=get_projectmat()
        if torch.cuda.is_available() and Q.device.type == "cpu":
            Q = Q.cuda()
        invalid_idx = target == 0
        depth_target = Q[2, 3] / ((target - Q[3, 3])*Q[3,2])
        depth_target = torch.clamp(depth_target,0,80)
        depth_target[invalid_idx] = 0
        invalid_idx=invalid_idx+(depth_target>20)
        valid_num = torch.count_nonzero(~invalid_idx)
        depth_target = depth_target/torch.amax(torch.amax(depth_target,1,keepdims=True),2,keepdims=True)
        depth_target *= 80
        depth_output = from_log_to_depth(output.reshape(depth_target.shape))
        diffMatrix = torch.abs(depth_output - depth_target)
        diffMatrix[invalid_idx]=0
        return torch.sum(diffMatrix) / valid_num
def mean_absolute_error_30(output, target):
    with torch.no_grad():
        Q=get_projectmat()
        if torch.cuda.is_available() and Q.device.type == "cpu":
            Q = Q.cuda()
        invalid_idx = target == 0
        depth_target = Q[2, 3] / ((target - Q[3, 3])*Q[3,2])
        depth_target = torch.clamp(depth_target,0,80)
        depth_target[invalid_idx] = 0
        invalid_idx=invalid_idx+(depth_target>30)
        valid_num = torch.count_nonzero(~invalid_idx)
        depth_target = depth_target/torch.amax(torch.amax(depth_target,1,keepdims=True),2,keepdims=True)
        depth_target *= 80
        depth_output = from_log_to_depth(output.reshape(depth_target.shape))
        diffMatrix = torch.abs(depth_output - depth_target)
        diffMatrix[invalid_idx]=0
        return torch.sum(diffMatrix) / valid_num
def log_ssim_error(output, target):
    with torch.no_grad():
        Q=get_projectmat()
        if torch.cuda.is_available() and Q.device.type == "cpu":
            Q = Q.cuda()
        invalid_idx = target == 0
        depth_target = Q[2, 3] / ((target - Q[3, 3])*Q[3,2])
        valid_idx=~invalid_idx
        log_depth_target = get_log_depth_gt(depth_target, valid_idx)
        log_depth_output = output.reshape(log_depth_target.shape).clone()
        log_depth_output[invalid_idx]=0
        ssim_val = get_ssim_loss(log_depth_target.unsqueeze(0),log_depth_output.unsqueeze(0))
        return ssim_val
def ssim_error(output, target):
    with torch.no_grad():
        Q=get_projectmat()
        if torch.cuda.is_available() and Q.device.type == "cpu":
            Q = Q.cuda()
        invalid_idx = target == 0
        depth_target = Q[2, 3] / ((target - Q[3, 3])*Q[3,2])
        depth_target = torch.clamp(depth_target,0,80)
        depth_target[invalid_idx] = 0
        depth_target = depth_target/torch.amax(torch.amax(depth_target,1,keepdims=True),2,keepdims=True)
        depth_target *= 80
        depth_output = from_log_to_depth(output.reshape(depth_target.shape)).clone()
        depth_output[invalid_idx]=0
        ssim_val = get_ssim_loss(depth_target.unsqueeze(0),depth_output.unsqueeze(0))
        return ssim_val