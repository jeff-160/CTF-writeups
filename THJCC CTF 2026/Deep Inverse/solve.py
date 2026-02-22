import torch
import numpy as np
from scipy.optimize import minimize
from pwn import *
import re

model = torch.jit.load("model.pt")
model.eval()

target = 1337.0

def objective(x_np):
    x_tensor = torch.tensor(x_np, dtype=torch.float32)
    with torch.no_grad():
        y = model(x_tensor).item()
    return (y - target)**2

x0 = np.random.randn(10)

res = minimize(objective, x0, method='Nelder-Mead', options={'maxiter': 10000, 'disp': True})

x_sol = res.x
y_sol = model(torch.tensor(x_sol, dtype=torch.float32)).item()

print("Solution:", x_sol)
print("Output:", y_sol)

# submit solution
io = remote("chal.thjcc.org", 1337)

payload = ','.join(map(str, x_sol))

io.sendlineafter(b'>', payload.encode())

resp = io.recvline().decode().strip()
io.close()

flag = re.findall(r'(THJCC{.+})', resp)[0]
print("Flag:", flag)