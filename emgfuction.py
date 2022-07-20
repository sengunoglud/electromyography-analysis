import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.signal


def remove_mean(emg, time):
    emg_correctmean = emg - np.mean(emg)
    fig = plt.figure()
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title('Mean offset present')
    plt.plot(time, emg)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    #plt.ylim(-1.5, 1.5)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')
    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title('Mean-corrected values')
    plt.plot(time, emg_correctmean)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    #plt.ylim(-1.5, 1.5)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')
    fig.tight_layout()
    fig_name = 'fig2.png'
    fig.set_size_inches(w=11, h=7)
    fig.savefig(fig_name)
    return emg_correctmean

def emg_filter(emg_correctmean,time):
    """
    time: Time data
    emg: EMG data
    high: high-pass cut off frequency
    low: low-pass cut off frequency
    sfreq: sampling frequency
    """

    # normalise cut-off frequencies to sampling frequency
    high = 2/(1000/2)
    low = 45/(1000/2)

    # create bandpass filter for EMG
    b, a = sp.signal.butter(4, [high, low], btype='bandpass')

    # process EMG signal: filter EMG
    emg_filtered = sp.signal.filtfilt(b, a, emg_correctmean)

    # plot graphs
    fig = plt.figure()
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title('Unfiltered EMG')
    plt.plot(time, emg_correctmean)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    #plt.ylim(-1.5, 1.5)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')

    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title('Filtered EMG')
    plt.plot(time, emg_filtered)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    #plt.ylim(-0.05, 0.05)
    #plt.plot([0.9, 1.0], [1.0, 1.0], 'r-', lw=5)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')

    fig.tight_layout()
    figname = "fig3.png"
    fig.set_size_inches(w=5, h=3)
    fig.savefig(figname)
    return emg_filtered

def emg_rectify(emg_filtered, time):
    emg_rectified = abs(emg_filtered)
    fig = plt.figure()
    plt.subplot(1,2,1)
    plt.subplot(1,2,1).set_title("Unrectified EMG")
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    plt.plot(time,emg_filtered)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')

    plt.subplot(1,2,2)
    plt.subplot(1,2,2).set_title("Rectified EMG")
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    plt.plot(time,emg_rectified)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')
    fig.tight_layout()
    figname = "fig4.png"
    fig.set_size_inches(w=5, h=3)
    fig.savefig(figname)
    return emg_rectified
def allinone(time, emg, low_pass=10,sfreq=800,high_band=20,low_band=450):
    high_band = high_band/(sfreq/2)
    low_band = low_band/(sfreq/2)
    b1, a1 = sp.signal.butter(4,[high_band,low_band],btype='bandpass')
    emg_filtered = sp.signal.filtfilt(b1,a1,emg)
    emg_rectified = abs(emg_filtered)
    low_pass = low_pass/(sfreq/2)
    b2, a2 = sp.signal.butter(4,low_pass,btype='lowpass')
    emg_envelope = sp.signal.filtfilt(b2,a2,emg_rectified)
    fig = plt.figure()
    plt.subplot(1,3,1)
    plt.subplot(1,3,1).set_title("Unfiltered," + "\n" +"unrectified EMG")
    plt.plot(time,emg)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    plt.ylabel("EMG (a.u.)")
    plt.xlabel("Time (s)")

    plt.subplot(1,3,2)
    plt.subplot(1,3,2).set_title("Filtered," + "\n" + "rectified EMG")
    plt.plot(time, emg_rectified)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    plt.xlabel("Time (s)")

    plt.subplot(1,3,3)
    plt.subplot(1,3,3).set_title("Filtered, rectified" + "\n" + "enveloped EMG")
    plt.plot(time, emg_envelope)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    plt.xlabel("Time (s)")


    figurename= "fig_" + str(int(low_pass*sfreq)) + '.png'
    fig.set_size_inches(w=11, h=7)
    fig.savefig(figurename)
