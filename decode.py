#!/usr/bin/env python3
import sys


def decode():
    file = open('output.jpg', 'rb')
    mess = ''
    for line in file:
        if line.find(b'\xff') + 1 == line.find(b'\xdb') != -1:
            res = ''
            ff = False
            db = False
            k = 0
            count = 0
            for e in line:
                if bytes([e]) == b'\xff':
                    ff = True
                elif ff:
                    if bytes([e]) == b'\xdb':
                        db = True
                    ff = False
                elif db:
                    if count < 67:
                        if count > 2:
                            bin_byte = bin(e)[2:]
                            while len(bin_byte) != 8:
                                bin_byte = '0' + bin_byte
                            if k < 1:
                                res += bin_byte[4:]
                                k += 1
                            else:
                                res += bin_byte[4:] + ','
                                k = 0
                        count += 1
                    else:
                        db = False
                        count = 0
            for e in res.split(','):
                if e != '':
                    num = int(e, 2)
                    mess += chr(num)
    print(mess)
    file.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            print("""Программа получает сообщение из картинки,
лежащей в текущей директории, 'output.jpg',
в которую вы предварительно закодировали ваше сообщение
с помощью программы encode.py.
Пример запуска: python decode.py""")
        else:
                print("""Некорректно введены данные,
посмотрите пример запуска с помощью
python decode.py help""")
    else:
        decode()
