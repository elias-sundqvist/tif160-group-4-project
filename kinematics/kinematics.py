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

min_angles = torch.tensor([0.001, 0.001, 0.001])
max_angles = torch.tensor([math.pi, math.pi, math.pi/2])

# Takes the current radians for body, shoulder, elbow, and a target x,y,z (in meters) position
# moves the servos one step closer to the desired position.
def step_towards_target(current_radians, target_pos, n_steps):
    θ = torch.tensor(current_radians, requires_grad=True)
    for i in range(n_steps):
        target = torch.tensor(target_pos)
        pos = forward(θ)
        loss = torch.mean(torch.square(torch.sub(pos, target)))
        loss.backward()
        grad = θ.grad
        if i % 100 == 0:
            print(f"loss: {loss}, θ: {θ}, grad:{θ.grad}")
        new_θ = (θ-0.1*grad)
        θ = new_θ.clone().detach().requires_grad_(True)
        #θ = torch.min(torch.max(min_angles, new_θ), max_angles).clone().detach().requires_grad_(True)
    return θ.detach()
