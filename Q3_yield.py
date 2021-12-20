import string
import hashlib
import os
from multiprocessing import Process, Value


def text_to_md5(text):
    encoded_text = hashlib.md5(text.encode())
    return encoded_text.hexdigest()


def generate_text(n, chars):
    if n == 0:
        yield ''
    else:
        pw_list = generate_text(n - 1, chars)
        for pw in pw_list:
            for c in chars:
                yield pw + c


def single_process(initial_text, chars, length, pwd, flag):
    for i in range(1, length + 1):
        for text in generate_text(i, chars):
            combined_text = initial_text + text
            # print(f"{os.getpid()} of {os.getppid()} is trying {combined_text}\n")
            if flag.value == 1:
                break

            if text_to_md5(combined_text) == pwd:
                flag.value = 1
                print(f"The password is {combined_text}")


def main():
    chars = string.ascii_letters + string.digits
    length = 2
    pwd = "57f14ae2f5dae8d025b56f8afa126400"
    processes = []
    flag = Value('i', 0)
    for c in chars:
        processes.append(Process(target=single_process, args=(c, chars, length, pwd, flag)))
    for process in processes:
        process.start()
    for process in processes:
        process.join()


if __name__ == "__main__":
    main()
