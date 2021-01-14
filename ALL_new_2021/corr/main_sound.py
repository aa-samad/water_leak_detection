""" =======================================================
                    Leak Detection project
                Coded by Samadzadeh & Nourian
    =======================================================
    compatible with python > 3.5                            
    prerequisites: Numpy, matplotlib, pandas, scipy, obspy, wave"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal as scisig
from scipy.io.wavfile import read as wave_read
# from obspy.signal import filter, cross_correlation
import corr.waveread24 as waveread24
import os
# matplotlib.use('TkAgg')


def main(max_shift):
    # single_sensor_freq_spect_exam()
    return dual_sensor_cross_corr_exam(0, max_shift)

def dual_sensor_cross_corr_exam(only_index, max_shift):
    # ---- init ----
    print("------------ DUAL ---------------")
    rootaddr = 'sensor/left'
    Fs, data0 = read_data(rootaddr, 1)
    rootaddr = 'sensor/right'
    Fs, data1 = read_data(rootaddr, 1)
    values0 = preprocess(data0)
    values1 = preprocess(data1)

    # --------- show freq cross-spectogram ------
    for i in range(len(values0)):
        show_cross_spect_freq([values0[i], values1[i]], data_name="orig_cross_corr_sig_pipe_{}".format(i), show=False, Fs=Fs,
                          log=False, xlim=[1000, 10000])

    # -------- filter and cross-correlate ------
    values0 = values0 + values1
    filtered_values = values0

    # filtered_values = []
    # for i in range(len(values0)):
    #     filtered_values.append(filter_sig(values0[i], Fs=Fs))

    # --------- show filtered freq cross-spectogram ------
    # for i in range(len(values1)):
    #     show_cross_spect_freq([filtered_values[i], filtered_values[len(values1) + i]], data_name="cross_corr_sig_pipe_{}".format(i), show=False, Fs=Fs,
    #                       log=True, xlim=[1000, 10000])

    # --- calc cross-correlation ---
    for i in range(len(values1)):
        return calc_cross_corr(filtered_values[i], filtered_values[len(values1) + i], show=False, save_addr='../static/img/corr.png'.format(i),
                        scot=False, plt_title="time_cross_corr_{}".format(i), frame_by_frame=False, Fs=Fs, max_shift=max_shift)


def single_sensor_freq_spect_exam():
    # ---- init ----
    rootaddr = 'sensor/left'
    Fs, data0 = read_data(rootaddr, 1)
    rootaddr = 'sensor/right'
    Fs, data1 = read_data(rootaddr, 1)
    values0 = preprocess(data0)
    values1 = preprocess(data1)
    print(len(values0), len(values1))
    values0 = values0 + values1
    # --------- show spectogram ------------
    for i in range(len(values0)):
        show_spectogram(values0[i], data_index=i, xlim=[1000, 10000], Fs=Fs, num_frq_averaging=100)
        # , log=True, ylim=[-20, -10])

    # ---- show cross spectogram
    # show_cross_spect_freq(values0, log=True, xlim=[0, 20000])


def read_data(root_addr, channel=2):
    """ read all data """
    files = sorted(os.listdir(root_addr))
    data0 = []
    for file0 in files:
        rate, data = waveread24.readwav(os.path.join(root_addr, file0))         # 24 bit
        # rate, data = wave_read(os.path.join(root_addr, file0))    # 16 bit
        data0.append(data[:, channel - 1])
    return rate, data0


def preprocess(values0):
    """ get acceleration vector's scale """
    print("preprocess ...")
    for i in range(len(values0)):
        values0[i] = values0[i] - np.mean(values0[i])
        values0[i] = values0[i] / np.max(values0[i])
        # print(values0[i].shape)
        # values0[i] = values0[i][1:] - values0[i][:-1]  # get difference to ignore low freq
        
    print("\tDone!")
    return values0


def time_plot(data0):
    plt.figure(1)
    plt.plot(data0)
    plt.title("time plot")
    plt.show()


def show_spectogram(values0, data_index="0", show=False, log=False, xlim=None, ylim=None, Fs=7200, num_frq_averaging=100):
    """ a tool to plot spectogram """
    print("plotting spectogram {} ...".format(data_index), end='')

    nperseg0 = 520
    next_pow2 = lambda x: 1 if x == 0 else 2**(x - 1).bit_length()

    # ---- calc and plot spectogram ---
    plt.figure(2, figsize=(13, 7))
    plt.clf()
    plt.subplot(1, 2, 1)

    spectrum0, freq0, t0, _ = plt.specgram(values0, Fs=Fs, NFFT=next_pow2(nperseg0), noverlap=nperseg0 // 2, sides='onesided',
                 detrend='linear', #window=np.blackman(len(values0)),
                 mode='psd', cmap='gist_heat')  # detrend = linear to remove linear bias movement
    plt.title("spectogram of data_{}".format(data_index)); plt.ylabel('Frequency [Hz]'); plt.xlabel('Time [sec]')

    print(spectrum0.shape)
    # # --- remove freq < 1000 Hz ---
    # freq0 = freq0[2:]
    # spectrum0 = spectrum0[2:, :]

    # --- limit the plot to have better results
    if xlim:
        lower_bound = np.max(np.where(freq0 < xlim[0])[0])
        upper_bound = np.min(np.where(freq0 > xlim[1])[0])
        freq0 = freq0[lower_bound: upper_bound]
        spectrum0 = spectrum0[lower_bound: upper_bound]

    # --- add freq averaging filter ---
    spectrum0_old = spectrum0
    spectrum0 = np.zeros((spectrum0_old.shape[0], spectrum0_old.shape[1] // num_frq_averaging))
    for i in range(spectrum0.shape[1]):
        spectrum0[:, i] = np.sum(spectrum0_old[:, i: i + num_frq_averaging], axis=1)

    # --- show some part of spectogram ---
    num_small_fft = 4
    # ylim = [0, 0.0001]
    for i in range(num_small_fft):
        plt.subplot(num_small_fft, 2, 2 * (i + 1))
        chosen_batch_num = (spectrum0.shape[1] // (num_small_fft + 1)) * (i + 1)
        # plt.yticks(["0", "2", "4"])
        if log:
            plt.plot(freq0, np.log(spectrum0[:, chosen_batch_num]))
            plt.ylabel('Log(dB)')
        else:
            plt.plot(freq0, spectrum0[:, chosen_batch_num])
            plt.ylabel('dB')
            # if np.max(spectrum0[:, chosen_batch_num]) > ylim[1]:
            #     print(spectrum0.shape[0])
            #     ylim[1] = np.max(spectrum0[:, chosen_batch_num])
            # plt.ylim(ylim)
        if xlim:
            plt.xlim(xlim)
        if ylim:
            plt.ylim(ylim)
        plt.yticks([])
        if i == 0:  # display the title
            str0 = ""
            for i in range(num_small_fft):
                str0 += "{}/{} ".format((i + 1), (num_small_fft + 1))
            plt.title("{} sample of spectogram Avg - fft plot of a ".format(num_frq_averaging) + str0 + " in t of spectrum");
        if i == num_small_fft - 1:  # display the xlabel
            plt.xlabel('Frequency [Hz]')

    # --- save and show the plots
    save_addr = '../static/img/spect.png'.format(data_index)
    if not os.path.exists(os.path.dirname(save_addr)):
        os.mkdir(os.path.dirname(save_addr))
    if show:
        plt.show()
    else:
        plt.savefig(save_addr)
    print("\tDone!")


def show_cross_spect_freq(signal_list, log=None, xlim=None, ylim=None, data_name=None, show=False, Fs=6400):
    print("plotting spectogram {} ...".format(data_name))
    if data_name:
        data_name0 = data_name
    elif log:
        data_name0 = "cross_cor_log"
    else:
        data_name0 = "cross_cor"
    for i in range(len(signal_list) - 1):
        signal_list[i + 1] = scisig.fftconvolve(signal_list[i], signal_list[i + 1], "same")
        signal_list[i + 1] = signal_list[i + 1] / np.sum(signal_list[i + 1])
    value0 = signal_list[-1]

    show_spectogram(value0, data_index=data_name0, log=log, xlim=xlim, ylim=ylim, show=show, Fs=Fs)


def filter_sig(value0, Fs=7200):
    return filter.bandpass(data=value0, freqmin=1000, freqmax=2000, df=Fs, corners=51)    # Butterworth bandpass filter


def calc_cross_corr(value0, value1, Fs=7200, show=False, save_addr='../static/img/a.png', scot=False, time_scale=False,
                    test_ccor=False, plt_title="", frame_by_frame=False, max_shift=500):
    """ Function to plot ccor in time and calc peak point of it """
    # if test_ccor:
    #     value0 = np.roll(value0, 100)  # just to test the scot
    
    # *************************************************************************
    value0 = value0 / np.max(np.abs(value0))
    value0 = value0 - np.mean(value0)
    value1 = value1 / np.max(np.abs(value1))
    value1 = value1 - np.mean(value1)

    if scot:
        sqrt_abs_Sxx = np.sqrt(np.abs(np.fft.fft(scisig.correlate(value0, value0))))
        sqrt_abs_Syy = np.sqrt(np.abs(np.fft.fft(scisig.correlate(value1, value1))))
        xsi = 1 / sqrt_abs_Syy / sqrt_abs_Sxx
        Sxy = np.fft.fft(scisig.correlate(value0, value1))
        value0 = np.fft.ifft(Sxy * xsi)
        value0 = value0 / np.max(np.abs(value0))
    else:
        value0 = scisig.correlate(value0, value1)
        value0 = value0 / np.max(np.abs(value0))

    # --- interpolate the sharp edges
    mid = (len(value0) - 1) // 2
    # value0[mid - 10: mid + 11] = 0
    # for i in range(1, mid):
    #     if abs(value0[i] - value0[i - 1]) > 0.1:
    #         value0[i] = value0[i - 1]
    # for i in reversed(range(mid, len(value0))):
    #     if abs(value0[i] - value0[i - 1]) > 0.1:
    #         value0[i - 1] = value0[i]

    # ---- plot cross-correlation
    plt.figure(4, figsize=(16, 8))
    plt.clf()
    if time_scale:
        a = len(value0) / 2 / Fs
        plt.xlabel("time [sec]")
    else:
        a = len(value0) / 2         # to have sample output
        plt.xlabel("time [sample]")
    plt.plot(np.linspace(-a, a, len(value0)), np.abs(value0))
    plt.ylabel("normalized power")
    plt.title(plt_title + "_zoomed")
    plt.grid(True)
    # ---- CHANGE THESE ACCORDING TO DATA ----
    max_shift = int(max_shift * Fs)
    lims = [-max_shift, max_shift, 0, 1]
    plt.xlim([lims[0], lims[1]])
    plt.ylim([lims[2], lims[3]])
    # plt.show()
    plt.xticks(np.linspace(lims[0], lims[1], 21))
    plt.yticks(np.linspace(lims[2], lims[3], 11))
    # plt.show()

    # ---- CHANGE THESE ACCORDING TO DATA ----
    # lims = [0, 300, 0, 1]
    # plt.xlim([lims[0], lims[1]])
    # plt.ylim([lims[2], lims[3]])
    # plt.xticks(np.linspace(lims[0], lims[1], 21))
    # plt.yticks(np.linspace(lims[2], lims[3], 11))

    if show:
        plt.show()
    else:
        if not os.path.exists(os.path.dirname(save_addr)):
            os.mkdir(os.path.dirname(save_addr))
        plt.savefig(save_addr)

    # --- print cross corr peak point
    mid = (len(value0) - 1) // 2
    shift = np.argmax(np.abs(value0[mid - max_shift: mid + max_shift])) - max_shift      # only search for max in 1 Sec distance
    # value = np.abs(value0[shift])
    # if time_scale:
    #     shift = shift / Fs
    speed_of_sound = 3000
    # print(shift)
    # print(Fs)
    # print(speed_of_sound)
    print("shift amount = {:4f} Sec, {} Samples, {:3f} Meter".format(shift / Fs, shift, shift / Fs * speed_of_sound))
    # print("shift amount = {} Meter".format(shift))
    # else:
    #     print("shift amount = {} Samples, with confedence = {:3f}%".format(shift, value * 100))
    #     shift = shift / Fs *
    #     print("shift amount = {} Meter".format(shift))
    return shift / Fs

if __name__ == "__main__":
    main()
