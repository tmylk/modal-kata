import sys

import modal

stub = modal.Stub("example-hello-world")

def f_local(i):
    return i * i


@stub.function
def f_modal(i):
    return f_local(i)

def run_f(i):
    with stub.run():
        return f_modal.call(i)


if __name__ == "__main__":
    print(run_f(2))
