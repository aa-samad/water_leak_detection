""" =======================================================
                    Leak Detection project
                Coded by Samadzadeh & Nourian
    =======================================================
    compatible with python > 3.5                            
    prerequisites: Numpy, matplotlib, pandas, scipy, obspy"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal as scisig
from obspy.signal import filter, cross_correlation
import os


def main():
    # single_sensor_freq_spect_exam()
    for i in range(8):  # for in number of data files
        dual_sensor_cross_corr_exam(i)


def dual_sensor_cross_corr_exam(only_index):
    # ---- init ----
    print("------------ DUAL ---------------")
    rootfolder, rootfolder2 = "left/", "right/"
    data0 = read_data(rootfolder, only_index=only_index)
    data1 = read_data(rootfolder2, only_index=only_index)
    values0 = preprocess(data0)
    values1 = preprocess(data1)
    values0.append(values1[0])
    # --------- show freq cross-spectogram ------
    show_cross_spect_freq(values0, data_name="orig_cross_corr_sig_pipe_{}".format(only_index), show=False, Fs=7200,
                          log=True)
    # -------- filter and cross-correlate ------
    filtered_values = []
    for i in range(len(values0)):
        filtered_values.append(filter_sig(values0[i]))
    # --------- show filtered freq cross-spectogram ------
    show_cross_spect_freq(filtered_values, data_name="cross_corr_sig_pipe_{}".format(only_index), show=False, Fs=7200,
                          log=True, xlim=[0, 700])
    # --- show filtered spectogram ----
    # show_spectogram(filtered_values[0], data_index="spect_filtered_sig", show=True)
    # --- calc cross-correlation ---
    calc_cross_corr(filtered_values[0], filtered_values[1], show=False, save_addr='output/time_cross_corr_{}.png'.format(only_index),
                    scot=True, plt_title="time_cross_corr_{}".format(only_index))  # , time_scale=False, test_ccor=True)


def single_sensor_freq_spect_exam():
    # ---- init ----
    rootfolder = "right/"
    data0 = read_data(rootfolder)
    values0 = preprocess(data0)
    # --------- show spectogram ------------
    for i in range(len(values0)):
        show_spectogram(values0[i], data_index=i, log=True, xlim=[0, 500])
    # --------- show freq cross-spectogram ------
    # values0.pop(5)  # pop not needed data
    # values0.pop(15)  # pop not needed data
    # show_cross_spect_freq(values0, log=False)
    show_cross_spect_freq(values0, log=True, xlim=[0, 500])


def read_data(root_folder, root_folder2=None, only_index=None, num_data=8):
    """ read all data """
    print("reading data ...")
    data0 = []
    if only_index:
            data0.append(pd.read_csv(root_folder + "analog{:02d}.csv".format(only_index), skiprows=[0, 1]))
            print("\tDone!")
            return data0
    else:
            for i in range(num_data):
                data0.append(pd.read_csv(root_folder + "analog{:02d}.csv".format(i), skiprows=[0, 1]))
            print("\tDone!")
            return data0


def preprocess(data0, use_z_axis_only=False):
    """ get acceleration vector's scale """
    print("preprocess ...")
    values0 = []
    for i in range(len(data0)):
        values0.append(data0[i].values)
        if values0[i].dtype != np.int64:  # there is overrun or other str in the CSV
            values0[i] = np.random.randint(-10, 10, (1000,)) / 10
        else:
            if use_z_axis_only:
                values0[i] = values0[i][:, 2]
            else:
                values0[i] = np.sqrt(np.sum(values0[i] ** 2, axis=1))
            # print("\tdata_{} statistics: std={:.1f}, mean={:.1f}".format(i, np.std(values0[i]), np.mean(values0[i])))
            values0[i] = values0[i] - np.mean(values0[i])
            values0[i] = values0[i] / np.max(values0[i])
        # values0[i] = values0[i][1:] - values0[i][:-1]  # get difference to ignore low freq
    print("\tDone!")
    return values0


def time_plot(data0):
    plt.figure(1)
    plt.plot(data0)
    plt.title("time plot")
    plt.show()


def show_spectogram(values0, data_index="0", show=False, log=None, xlim=None, ylim=None, Fs=7200, num_frq_averaging=50):
    """ a tool to plot spectogram """
    print("plotting spectogram {} ...".format(data_index), end='')
    nperseg0 = 500
    next_pow2 = lambda x: 1 if x == 0 else 2**(x - 1).bit_length()
    # ---- calc and plot spectogram ---
    plt.figure(2, figsize=(13, 7))
    plt.clf()
    plt.subplot(1, 2, 1)
    spectrum0, freq0, t0, _ = plt.specgram(values0, Fs=Fs, NFFT=next_pow2(nperseg0), noverlap=nperseg0 // 2, sides='onesided',
                 detrend='linear', #window=np.blackman(len(values0)),
                 mode='psd', cmap='gist_heat')  # detrend = linear to remove linear bias movement
    plt.title("spectogram of data_{}".format(data_index)); plt.ylabel('Frequency [Hz]'); plt.xlabel('Time [sec]')

    # --- remove freq < 25 ---
    freq0 = freq0[2:]
    spectrum0 = spectrum0[2:, :]

    # --- add freq averaging filter ---
    spectrum0_old = spectrum0
    spectrum0 = np.zeros((spectrum0_old.shape[0], spectrum0_old.shape[1] // num_frq_averaging))
    for i in range(spectrum0.shape[1]):
        spectrum0[:, i] = np.mean(spectrum0_old[:, i: i + num_frq_averaging], axis=1)

    # --- show some part of spectogram ---
    num_small_fft = 4
    for i in range(num_small_fft):
        plt.subplot(num_small_fft, 2, 2 * (i + 1))
        chosen_batch_num = (spectrum0.shape[1] // (num_small_fft + 1)) * (i + 1)
        if log:
            plt.plot(freq0, np.log(spectrum0[:, chosen_batch_num]))
            plt.ylabel('Log(dB)')
        else:
            plt.plot(freq0, spectrum0[:, chosen_batch_num])
            plt.ylabel('dB')
        if xlim:
            plt.xlim(xlim)
        if ylim:
            plt.ylim(ylim)
        if i == 0:  # display the title
            str0 = ""
            for i in range(num_small_fft):
                str0 += "{}/{} ".format((i + 1), (num_small_fft + 1))
            plt.title("{} sample of spectogram Avg - fft plot of a ".format(num_frq_averaging) + str0 + " in t of spectrum");
        if i == num_small_fft - 1:  # display the xlabel
            plt.xlabel('Frequency [Hz]')

    # --- save and show the plots
    save_addr = 'output/spect_{}.png'.format(data_index)
    if not os.path.exists(os.path.dirname(save_addr)):
        os.mkdir(os.path.dirname(save_addr))
    if show:
        plt.show()
    else:
        plt.savefig(save_addr)
    print("\tDone!")


def show_cross_spect_freq(signal_list, log=None, xlim=None, ylim=None, data_name=None, show=False, Fs=6400):
    for i in range(len(signal_list) - 1):
        signal_list[i + 1] = scisig.fftconvolve(signal_list[i], signal_list[i + 1], "same")
    value0 = signal_list[-1]

    if data_name:
        data_name0 = data_name
    elif log:
        data_name0 = "cross_cor_log"
    else:
        data_name0 = "cross_cor"

    show_spectogram(value0, data_index=data_name0, log=log, xlim=xlim, ylim=ylim, show=show, Fs=Fs)


def filter_sig(value0, Fs=7200):
    return filter.bandpass(data=value0, freqmin=300, freqmax=550, df=Fs, corners=104)    # Butterworth bandpass filter


def calc_cross_corr(value0, value1, Fs=7200, show=False, save_addr='output/a.png', scot=False, time_scale=False,
                    test_ccor=False, plt_title=""):
    """ Function to plot ccor in time and calc peak point of it """
    if test_ccor:
        value0 = np.roll(value0, 100)  # just to test the scot

    if scot:
        sqrt_abs_Sxx = np.sqrt(np.abs(np.fft.fft(scisig.correlate(value0, value0))))
        sqrt_abs_Syy = np.sqrt(np.abs(np.fft.fft(scisig.correlate(value1, value1))))
        Sxy = np.fft.fft(scisig.correlate(value0, value1))
        value0 = Sxy / sqrt_abs_Syy / sqrt_abs_Sxx
        value0 = np.fft.ifft(value0)
        value0 = value0 / np.max(np.abs(value0))
    else:
        value0 = scisig.correlate(value0, value1)
        value0 = value0 / np.max(np.abs(value0))

    # --- interpolate the sharp edges
    mid = (len(value0) - 1) // 2
    value0[mid - 1: mid + 2] = 0
    # for i in range(1, mid):
    #     if abs(value0[i] - value0[i - 1]) > 0.1:
    #         value0[i] = value0[i - 1]
    # for i in reversed(range(mid, len(value0))):
    #     if abs(value0[i] - value0[i - 1]) > 0.1:
    #         value0[i - 1] = value0[i]

    # ---- plot cross-correlation
    plt.figure(4, figsize=(16, 16))
    plt.clf()
    plt.subplot("211")
    if time_scale:
        a = len(value0) / 2 / Fs
        plt.xlabel("time [sec]")
    else:
        a = len(value0) / 2         # to have sample output
        plt.xlabel("time [sample]")
    plt.plot(np.linspace(-a, a, len(value0)), value0)
    plt.ylabel("normalized power")
    plt.title(plt_title + "_zoomed")
    plt.grid(True)
    # ---- CHANGE THESE ACCORDING TO DATA ----
    lims = [-20, 20, -0.5, 0.5]
    plt.xlim([lims[0], lims[1]])
    plt.ylim([lims[2], lims[3]])
    plt.xticks(np.linspace(lims[0], lims[1], 21))
    plt.yticks(np.linspace(lims[2], lims[3], 11))

    # ---- zoomed out
    plt.subplot("212")
    plt.plot(np.linspace(-a, a, len(value0)), value0)
    plt.ylabel("normalized power")
    plt.title(plt_title)
    plt.grid(True)
    if time_scale:
        a = len(value0) / 2 / Fs
        plt.xlabel("time [sec]")
    else:
        a = len(value0) / 2         # to have sample output
        plt.xlabel("time [sample]")
    # ---- CHANGE THESE ACCORDING TO DATA ----
    lims = [-200, 200, -0.2, 0.2]
    plt.xlim([lims[0], lims[1]])
    plt.ylim([lims[2], lims[3]])
    plt.xticks(np.linspace(lims[0], lims[1], 21))
    plt.yticks(np.linspace(lims[2], lims[3], 11))

    if show:
        plt.show()
    else:
        if not os.path.exists(os.path.dirname(save_addr)):
            os.mkdir(os.path.dirname(save_addr))
        plt.savefig(save_addr)

    # --- print cross corr peak point
    mid = (len(value0) - 1) // 2
    shift = np.argmax(np.abs(value0[mid - 100: mid + 100])) - 100      # only search for max in 1 Sec distance
    value = np.abs(value0[shift])
    if time_scale:
        shift = shift / Fs
        print("shift amount = {} Sec, with confedence = {:3f}%".format(shift, value * 100))
    else:
        print("shift amount = {} Samples, with confedence = {:3f}%".format(shift, value * 100))


if __name__ == "__main__":
    main()
