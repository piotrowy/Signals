import wave
import sys
import os
import numpy
import struct
import functools


def main():
    hits = 0
    count = 0
    for file in os.listdir(os.getcwd() + '/train'):
        signal = wave.open('./train/' + file)

        max_fouriers = []

        channels, samp_width, frame_rate, nframes, comp_type, comp_name = signal.getparams()
        time_frame_size = int(frame_rate/5)
        frames = signal.readframes(channels * nframes)
        out = struct.unpack_from("%dh" % nframes * channels, frames)
        mono = [(out[x]+out[x+1])/2 for x in range(0, len(out), 2)] if channels == 2 else [out[x] for x in range(len(out))]
        avg_mono = functools.reduce(lambda x, y: x+y, mono)/len(mono)
        mono = [mono[x] - avg_mono for x in range(len(mono))]
        for i in range(0, len(mono), time_frame_size):
            fourier = numpy.fft.fft(mono[i:i + time_frame_size])
            if len(fourier) == time_frame_size:
                max_fouriers.append(numpy.asarray([abs(fourier[i]) for i in range(1, 56, 1)]).argmax(axis=0)*frame_rate/time_frame_size)
        max_fouriers.sort()

        if len(max_fouriers) > 0:
            count += 1
            if ((max_fouriers[int(len(max_fouriers)/2)]) < 165 and 'M' in file) or ((max_fouriers[int(len(max_fouriers)/2)]) >= 165 and 'K' in file):
                hits += 1
            print('freq: ' + str((max_fouriers[int(len(max_fouriers)/2)])) + ' hz ' + file + ' : ' + str((max_fouriers[int(len(max_fouriers)/2)])) + ' : ' + str(hits))
        else:
            print(file + ' : ' + str(frame_rate) + ' : ' + str(nframes))
    print(str(hits/count))
if __name__ == '__main__':
    main()
