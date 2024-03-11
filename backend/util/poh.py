import hashlib
import libnum

def do_work(x, T, N):
    for i in range(1, T):
        po = pow(2,T,N)
    return(pow(x,po,N))

def compute_vdf(input, time_parameter, bits=32, L=18):
    T = min(time_parameter, 100)  
    N = libnum.generate_prime(bits)
    g = hashlib.sha256(str(input).encode())
    g = int.from_bytes(g.digest(), 'big')
    y = do_work(g, T, N) 

    q = pow(2,T,N) // L

    pi = pow(g,q,N)

    return y, [pi, g, N]

def verify_vdf(vdf_output, vdf_params, time_parameter, L=18):
    y, [pi, g, N] = vdf_output, vdf_params
    T = time_parameter
    r = pow(2, T, L) % L
    ynew = (pow(pi, L, N) * pow(g, r, N)) % N
    return y == ynew