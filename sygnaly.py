import wave
import sys
import numpy
import struct

time_frame_size = 1024



def main():
    count = 0
    sum = 0
    file_u = ''
    for index in range(1, 92):
        file = './train/0'
        if index < 10:
            file += '0'
        file += str(index) + '_'

        try:
            file_k = file + 'K.wav'
            file_u = file_k
            sygnal = wave.open(file_k)
        except:
            file_m = file + 'M.wav'
            file_u = file_m
            sygnal = wave.open(file_m)

        max_fouriers = []

        channels = sygnal.getnchannels()
        frame_rate = sygnal.getframerate()
        nframes = sygnal.getnframes()
        frames = sygnal.readframes(channels * nframes)
        out = struct.unpack_from("%dh" % nframes * channels, frames)
        if channels == 2:
            mono = [((out[x]+out[x+1])/2) for x in range(0, len(out), 2)]
        else:
            mono = [(out[x]) for x in range(len(out))]
        for i in range(0, len(mono), time_frame_size):
            fourier = numpy.fft.fft(mono[i:i+time_frame_size])
            # print(numpy.asarray([abs(fourier[i]) for i in range(len(fourier))]).argmax(axis=0))
            if numpy.asarray([abs(fourier[i]) for i in range(len(fourier))]).argmax(axis=0) > 0:
                max_fouriers.append(numpy.asarray([abs(fourier[i]) for i in range(len(fourier))]).argmax(axis=0))
        max_fouriers.sort()
        if len(max_fouriers) > 0:
            print('freq: ' + str((max_fouriers[int(len(max_fouriers)/2)])*frame_rate/time_frame_size) + ' hz' + file_u)
            count += 1
            sum += (max_fouriers[int(len(max_fouriers)/2)])*frame_rate/time_frame_size

    print(sum/count)

if __name__ == '__main__':
    main()
