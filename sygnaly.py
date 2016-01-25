import wave
import sys
import os
import numpy
import struct
import functools

time_frame_size = 1024


def main():
    hits = 0
    count = 0
    for file in os.listdir(os.getcwd() + '/train'):
        signal = wave.open('./train/' + file)

        max_fouriers = []

        channels, samp_width, frame_rate, nframes, comp_type, comp_name = signal.getparams()
        frames = signal.readframes(channels * nframes)
        out = struct.unpack_from("%dh" % nframes * channels, frames)
        mono = [(out[x]+out[x+1])/2 for x in range(0, len(out), 2)] if channels == 2 else [out[x] for x in range(len(out))]
        avg_mono = functools.reduce(lambda x, y: x+y, mono)/len(mono)
        mono = [mono[x] - avg_mono for x in range(len(mono))]
        for i in range(0, int(len(mono)/2), time_frame_size):
            fourier = numpy.fft.fft(mono[i:i + time_frame_size])
            if numpy.asarray([abs(fourier[i]) for i in range(len(fourier))]).argmax(axis=0) > 0:
                max_fouriers.append(numpy.asarray([abs(fourier[i]) for i in range(len(fourier))]).argmax(axis=0)*frame_rate/time_frame_size)
                fourier_out_extreme = [max_fouriers[x] for x in range(len(max_fouriers)) if 150 < max_fouriers[x] < 1800]
        max_fouriers.sort()

        if len(fourier_out_extreme) > 0:
            count += 1
            avg = functools.reduce(lambda x, y: x+y, fourier_out_extreme)/len(fourier_out_extreme)
            if (avg < 450 and 'M' in file) or (avg > 450 and 'K' in file):
                hits += 1
            print('freq: ' + str((fourier_out_extreme[int(len(fourier_out_extreme)/2)])) + ' hz ' + file + ' : ' + str(avg) + ' : ' + str(hits))
        else:
            print(file + ' : ' + str(frame_rate) + ' : ' + str(nframes))
    print(str(hits/count))
if __name__ == '__main__':
    main()
