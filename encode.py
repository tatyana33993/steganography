#!/usr/bin/env python3
from queue import Queue
import sys


def encode(mess):
    file = open('input.jpg', 'rb')
    outfile = open('output.jpg', 'wb')
    q = Queue()
    for char in mess:
        code_char = ord(char)
        bin_char = bin(code_char)[2:]
        while len(bin_char) != 8:
            bin_char = '0' + bin_char
        q.put(bin_char[:4])
        q.put(bin_char[4:])
    for line in file:
        if line.find(b'\xff') + 1 == line.find(b'\xdb') != -1:
            new_line = b''
            ff = False
            db = False
            count = 0
            for e in line:
                if bytes([e]) == b'\xff':
                    ff = True
                    new_line += bytes([e])
                elif ff:
                    if bytes([e]) == b'\xdb':
                        db = True
                    new_line += bytes([e])
                    ff = False
                elif db:
                    if count < 67:
                        if count < 3:
                            new_line += bytes([e])
                        else:
                            new_byte = bytes([e])
                            if not q.empty():
                                bin_byte = bin(e)[2:]
                                while len(bin_byte) != 8:
                                    bin_byte = '0' + bin_byte
                                new_bin_byte = bin_byte[0:4] + q.get()
                                new_dec_byte = int(new_bin_byte, 2)
                                new_byte = bytes([new_dec_byte])
                            new_line += new_byte
                        count += 1
                    else:
                        db = False
                        count = 0
                        new_line += bytes([e])
                else:
                    new_line += bytes([e])
            outfile.write(new_line)
        else:
            outfile.write(line)
    file.close()
    outfile.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            print("""Программа прячет введённое вами сообщение
в картинку, лежащую в текущей директории, 'input.jpg',
(картинка с вашим сообщением 'output.jpg')
Пример запуска: python encode.py I love python""")
        else:
            arr = sys.argv
            arr[0] = ''
            mess = ''
            for e in arr:
                mess += e + ' '
            encode(mess)
    else:
        print("""Некорректно введены данные,
посмотрите пример запуска с помощью
python encode.py help""")
