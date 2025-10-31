"""
Precomputation file to export the peak residues from an audio database.

Example use:
python compute_fakeprint.py --save fp_sonics.npy --path sonics/fake_songs --sr 16000
"""

import os
import numpy as np
from glob import glob
import argparse
from tqdm import tqdm  # supprimable
import torch
import torchaudio
import soxr
from scipy import interpolate

parser = argparse.ArgumentParser()
parser.add_argument("--save", help="save file", type=str, default="")
parser.add_argument("--path", help="audio files dir", type=str)
parser.add_argument("--sr", help="audio sampling rate", type=int, default=44100)
parser.add_argument("--fmin", help="low freq cutoff (in Hz)", type=int, default=5000)
parser.add_argument("--fmax", help="high freq cutoff (in Hz)", type=int, default=16000)
args = parser.parse_args()
N_FFT = 1 << 14

##

def open_audio_slice(f_path):
    audio_raw, sr = torchaudio.load( f_path, channels_first = False)
    audio_raw = audio_raw.numpy()
    return audio_raw, sr

stft_transformer = torchaudio.transforms.Spectrogram(n_fft=N_FFT, power=2)
def get_stft(p):
    stft = stft_transformer(torch.Tensor(p.T)).numpy()
    stft = 10 * np.log10( np.clip( stft, 1e-10, 1e6 ) )
    return stft


def spectrogram(f_name, max_duration = 180, SR = 44100):
    p, sr = open_audio_slice( f_name )
    if sr != SR:
        p = soxr.resample(p, sr, SR)
    sr = SR
    p = p[:sr*max_duration]  # cut long audios
    spectro_p = get_stft(p)
    return spectro_p


def lower_hull(x, area = 10):
    idx = []
    hull = []
    for i in range(len(x)-area+1):
        patch = x[i:i+area]
        rel_idx = np.argmin(patch)
        abs_idx = rel_idx + i
        if abs_idx not in idx:
            idx.append(abs_idx)
            hull.append(patch[rel_idx])

    if idx[0] != 0:
        idx.insert(0, 0)
        hull.insert(0, x[0])
    if idx[-1] != len(x)-1:
        idx.append(len(x)-1)
        hull.append(x[-1])

    return np.array(idx), np.array(hull)


def curve_profile(x, c, f_range = [5000, 16000], min_dB = -45):
    cutoff_idx = np.where( (f_range[0] < x) & (x < f_range[1] ))
    x_ = x[cutoff_idx]
    c_ = c[cutoff_idx]
    lower_x, lower_c = lower_hull(c_, area=10)

    low_hull_curve = interpolate.interp1d(x_[ lower_x ], lower_c, kind="quadratic")(x_)
    low_hull_curve = np.clip( low_hull_curve, min_dB, None)

    return x_, np.clip( c_ - low_hull_curve, 0, None )


def max_normalise(x, max_dB = 5):
    x = np.clip(x, 0, max_dB)
    return x / (1e-6 + np.max(x))


def fakeprint(stft, f_range = [0, 16000], SR = 44100):
    fp = np.mean( stft, axis=(0, 2) )
    X_real = np.linspace(0, SR / 2, num = len(fp) )
    x_curve, fp_curve = curve_profile(X_real, fp, f_range)
    fp_curve = max_normalise(fp_curve)
    return fp_curve

## main loop

if __name__ == "__main__":
    # Create a dictionnary of fakeprints
    fakeprints = {}
    x_freqs = np.linspace(0, args.sr / 2, num = (N_FFT//2)+1 )
    path_mp3 = os.path.join(args.path, "*.mp3" )
    f_list = glob(path_mp3)
    print("found {} files in `{}`".format(len(f_list), path_mp3 ))

    n_completed = 0
    for f in tqdm(f_list):
        f_name = f.split("/")[-1]
        spectro_f = spectrogram( f, SR = args.sr )
        fakeprint_f = fakeprint(spectro_f, f_range=[args.fmin, args.fmax], SR = args.sr)
        fakeprints[f_name] = fakeprint_f

    np.save(args.save, fakeprints)
    print("Finished and saved!")