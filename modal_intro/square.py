import sys

import modal

stub =  modal.Stub("example-hello-world")

@stub.function
def f(i):
    return i * i

if __name__ == "__main__":
    with stub.run() as application:
        print(f.call(2))
        print(f.call(3))
