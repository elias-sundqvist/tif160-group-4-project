import torch
import math
from torch import sin, cos

L = {
    1: 0.055,
    2: 0.315,
    3: 0.045,
    4: 0.108,
    5: 0.005,
    6: 0.034,
    7: 0.015,
    8: 0.088,
    9: 0.204
}


def forward(θ):
    θ1, θ2, θ3 = θ[0], θ[1], θ[2]
    res = torch.zeros([3])
    res[0], res[1], res[2] = [
        (L[4] - L[5]) * sin(θ1) + cos(θ1) * (L[8] * sin(θ2) + L[9] * sin(θ2 + θ3) + L[7] * cos(θ2) + L[6]),
        (L[5] - L[4]) * cos(θ1) + sin(θ1) * (L[8] * sin(θ2) + L[9] * sin(θ2 + θ3) + L[7] * cos(θ2) + L[6]),
        L[7] * sin(θ2) - L[8] * cos(θ2) - L[9] * cos(θ2 + θ3) + L[2] + L[3]
    ]
    return res

min_angles = torch.tensor([0, 0, 0])
max_angles = torch.tensor([math.pi, math.pi, math.pi/2])

if __name__ == '__main__':
    θ = torch.tensor([0.5, 0.5, 0.5], requires_grad=True)
    for i in range(10000):
        target = torch.tensor([0., 0.4, 0.3])
        pos = forward(θ)
        loss = torch.mean(torch.square(torch.sub(pos, target)))
        loss.backward()
        grad = θ.grad
        if i % 100 == 0:
            print(f"loss: {loss}, θ: {θ}, grad:{θ.grad}")
        θ = torch.min(torch.max(min_angles, (θ-0.1*grad)), max_angles).clone().detach().requires_grad_(True)