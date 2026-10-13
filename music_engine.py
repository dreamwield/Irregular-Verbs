"""
Advanced Multi-Style Music Synthesizer Engine in pure Python (numpy + scipy).
Produces full stereo musical backing tracks for educational songs.
"""
import numpy as np
import scipy.io.wavfile as wav

def midi_to_freq(m):
    return 440.0 * (2.0 ** ((m - 69) / 12.0))

def create_kick(sample_rate=44100, length_sec=0.35, pitch_start=170.0, pitch_end=48.0):
    t = np.linspace(0, length_sec, int(sample_rate * length_sec), endpoint=False)
    freq = pitch_end + (pitch_start - pitch_end) * np.exp(-t * 26.0)
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    env = np.exp(-t * 9.5)
    kick = np.sin(phase) * env
    # Click transient for punch
    click = np.sin(2 * np.pi * 1200 * t[:int(0.005 * sample_rate)]) * np.exp(-np.linspace(0, 1, int(0.005 * sample_rate)) * 5)
    kick[:len(click)] += click * 0.4
    return np.clip(kick, -1.0, 1.0)

def create_snare(sample_rate=44100, length_sec=0.32, snap=0.7):
    t = np.linspace(0, length_sec, int(sample_rate * length_sec), endpoint=False)
    noise = (np.random.rand(len(t)) * 2 - 1) * np.exp(-t * 20.0)
    # High-pass filter noise slightly
    noise_hp = np.diff(noise, prepend=noise[0])
    tone = np.sin(2 * np.pi * 196.0 * t) * np.exp(-t * 24.0)
    tone2 = np.sin(2 * np.pi * 330.0 * t) * np.exp(-t * 32.0)
    snare = snap * noise_hp + 0.25 * tone + 0.12 * tone2
    return np.clip(snare, -1.0, 1.0)

def create_hihat(sample_rate=44100, length_sec=0.07, open_hat=False):
    length = length_sec if not open_hat else length_sec * 3.5
    t = np.linspace(0, length, int(sample_rate * length), endpoint=False)
    noise = np.random.rand(len(t)) * 2 - 1
    noise_hp = np.diff(noise, prepend=noise[0])
    decay = 45.0 if not open_hat else 10.0
    env = np.exp(-t * decay)
    return np.clip(noise_hp * env * 0.5, -1.0, 1.0)

def create_rhodes_chord(frequencies, duration_sec, sample_rate=44100):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    chord = np.zeros(len(t), dtype=np.float32)
    env = np.exp(-t * 1.6) * (1.0 - np.exp(-t * 50.0))
    for f in frequencies:
        # Fundamental + gentle 2nd, 3rd, 4th harmonics + detuned stereo chorus
        note = (
            1.00 * np.sin(2 * np.pi * f * t) +
            0.42 * np.sin(2 * np.pi * (f * 2.0) * t) +
            0.18 * np.sin(2 * np.pi * (f * 3.0) * t) +
            0.08 * np.sin(2 * np.pi * (f * 4.0) * t) +
            0.22 * np.sin(2 * np.pi * (f * 1.003) * t)
        )
        chord += note
    return chord * env * 0.18

def create_bell_note(freq, duration_sec=0.6, sample_rate=44100):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    env = np.exp(-t * 5.0)
    bell = (
        np.sin(2 * np.pi * freq * t) +
        0.5 * np.sin(2 * np.pi * (freq * 2.0) * t) +
        0.2 * np.sin(2 * np.pi * (freq * 3.01) * t)
    ) * env * 0.15
    return bell

def generate_backing_track(total_duration_sec, bpm=102, style="upbeat", sample_rate=44100):
    """
    Generates a continuous stereo backing track with drums, bass, keys, and melodic hooks.
    """
    total_samples = int(total_duration_sec * sample_rate)
    left = np.zeros(total_samples, dtype=np.float32)
    right = np.zeros(total_samples, dtype=np.float32)

    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * 4.0
    total_bars = int(np.ceil(total_duration_sec / bar_sec))

    kick = create_kick(sample_rate)
    snare = create_snare(sample_rate)
    closed_hh = create_hihat(sample_rate, 0.065, False)
    open_hh = create_hihat(sample_rate, 0.22, True)

    # 4-bar catchy chord cycle:
    # Bar 0: Am7 (A2, C3, E3, G3, C4)
    # Bar 1: Fmaj7 (F2, C3, E3, A3, C4)
    # Bar 2: C (C2, G2, E3, G3, D4)
    # Bar 3: G (G2, D3, G3, B3, D4)
    progression = [
        ([45, 57, 60, 64, 67, 72], 45, [69, 72, 76, 72]),  # Am7
        ([41, 53, 60, 64, 69, 72], 41, [65, 69, 72, 77]),  # Fmaj7
        ([48, 55, 60, 64, 67, 74], 48, [67, 72, 76, 79]),  # C
        ([43, 55, 59, 62, 67, 74], 43, [67, 71, 74, 79]),  # G
    ]

    def add_sound(buf, start_s, snd, gain=1.0):
        if snd is None or len(snd) == 0:
            return
        end_s = start_s + len(snd)
        if start_s >= total_samples:
            return
        if end_s > total_samples:
            buf[start_s:total_samples] += snd[:total_samples - start_s] * gain
        else:
            buf[start_s:end_s] += snd * gain

    for bar in range(total_bars):
        bar_start_s = int(bar * bar_sec * sample_rate)
        chord_midis, root_midi, melody_midis = progression[bar % len(progression)]
        chord_freqs = [midi_to_freq(m) for m in chord_midis]
        root_freq = midi_to_freq(root_midi)

        # 1. Chords (Rhodes) on beat 1 and beat 2.5
        ch_dur = bar_sec * 0.9
        chord_snd = create_rhodes_chord(chord_freqs, ch_dur, sample_rate)
        add_sound(left, bar_start_s, chord_snd, 0.42)
        add_sound(right, bar_start_s, chord_snd, 0.48)

        # 2. Bassline
        bass_len = int(bar_sec * sample_rate)
        bt = np.linspace(0, bar_sec, bass_len, endpoint=False)
        bass = np.zeros(bass_len, dtype=np.float32)

        # Note on beat 1 (root)
        n1_len = int(beat_sec * 1.5 * sample_rate)
        t1 = bt[:n1_len]
        bass[:n1_len] += (np.sin(2 * np.pi * root_freq * t1) + 0.35 * np.sin(2 * np.pi * root_freq * 2 * t1)) * np.exp(-t1 * 1.3)

        # Note on beat 2.5 (octave or fifth)
        n2_start = int(beat_sec * 2.0 * sample_rate)
        n2_len = int(beat_sec * 1.0 * sample_rate)
        if n2_start + n2_len <= bass_len:
            t2 = bt[:n2_len]
            bass[n2_start:n2_start+n2_len] += (np.sin(2 * np.pi * (root_freq * 1.5) * t2) + 0.25 * np.sin(2 * np.pi * (root_freq * 3) * t2)) * np.exp(-t2 * 2.2)

        # Note on beat 3.5 (fifth or turnaround)
        n3_start = int(beat_sec * 3.5 * sample_rate)
        n3_len = bass_len - n3_start
        if n3_len > 0:
            t3 = bt[:n3_len]
            bass[n3_start:n3_start+n3_len] += (np.sin(2 * np.pi * root_freq * t3) * np.exp(-t3 * 3.2))

        add_sound(left, bar_start_s, bass, 0.45)
        add_sound(right, bar_start_s, bass, 0.45)

        # 3. Arpeggiated melody bells (adds subtle musicality in stereo)
        for idx, m_note in enumerate(melody_midis):
            bell_time_s = bar_start_s + int((idx * beat_sec) * sample_rate)
            bell_snd = create_bell_note(midi_to_freq(m_note), 0.5, sample_rate)
            pan_l = 0.3 if idx % 2 == 0 else 0.1
            pan_r = 0.1 if idx % 2 == 0 else 0.3
            add_sound(left, bell_time_s, bell_snd, pan_l)
            add_sound(right, bell_time_s, bell_snd, pan_r)

        # 4. Drums
        for b in range(4):
            b_s = bar_start_s + int(b * beat_sec * sample_rate)

            # Kick pattern: Beat 0, Beat 2 (and syncopation on 2.5)
            if b == 0:
                add_sound(left, b_s, kick, 0.72)
                add_sound(right, b_s, kick, 0.72)
            elif b == 2:
                add_sound(left, b_s, kick, 0.65)
                add_sound(right, b_s, kick, 0.65)
                syn_s = b_s + int(beat_sec * 0.5 * sample_rate)
                add_sound(left, syn_s, kick, 0.45)
                add_sound(right, syn_s, kick, 0.45)

            # Snare on 1 and 3
            if b in [1, 3]:
                add_sound(left, b_s, snare, 0.62)
                add_sound(right, b_s, snare, 0.62)

            # Hi-hats: 8th notes
            hh1_s = b_s
            hh2_s = b_s + int(beat_sec * 0.5 * sample_rate)
            add_sound(left, hh1_s, closed_hh, 0.32)
            add_sound(right, hh1_s, closed_hh, 0.35)
            if b == 3: # open hat
                add_sound(left, hh2_s, open_hh, 0.38)
                add_sound(right, hh2_s, open_hh, 0.42)
            else:
                add_sound(left, hh2_s, closed_hh, 0.22)
                add_sound(right, hh2_s, closed_hh, 0.25)

    # Master normalization
    peak = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-5)
    left = np.clip(left / peak * 0.82, -1.0, 1.0)
    right = np.clip(right / peak * 0.82, -1.0, 1.0)

    stereo = np.column_stack((left, right))
    return (stereo * 32767).astype(np.int16)
