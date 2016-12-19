#!/usr/bin/env python3


def str_to_handle(f, *args, **kwargs):
    if isinstance(f, str):
        return open(f, *args, **kwargs)
    else:
        return f


def parser(f):
    f = str_to_handle(f)
    defline, sequence = '', []
    for line in f:
        if line[0] == '>':
            if defline:
                yield {'defline': defline, 'sequence': ''.join(sequence)}
            defline, sequence = line[1:].rstrip('\n'), []
        else:
            sequence.append(line.rstrip('\n'))
    if defline:
        yield {'defline': defline, 'sequence': ''.join(sequence)}


class Writer:
    def __init__(self, f, mode='w'):
        self.f = str_to_handle(f, mode)

    def write(self, defline, sequence):
        self.f.write(">" + defline + "\n")
        self.f.write(sequence + "\n")

    def close(self):
        self.f.close()