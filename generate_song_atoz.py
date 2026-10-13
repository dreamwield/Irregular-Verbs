"""
Generate Song 2: 02_Irregular_Verbs_Complete_A_to_Z.mp3
The complete PDF study track with all 154 verbs in exact alphabetical order.
Separated into 3 chapters corresponding to Page 1, Page 2, and Page 3 of the PDF.
Set to a mellow study lo-fi hip-hop groove.
"""
import os
import sys
import json
import subprocess
import hashlib
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import scipy.io.wavfile as wav
from gtts import gTTS

from music_engine import generate_backing_track

CACHE_DIR = "cache_audio"
os.makedirs(CACHE_DIR, exist_ok=True)
FFMPEG = r"C:\Users\Jlvillar\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"

def get_hash(text, lang):
    return hashlib.md5(f"{lang}_{text}".encode("utf-8")).hexdigest()[:12]

def fetch_tts(text, lang="en", tld="com"):
    h = get_hash(text, lang)
    mp3_path = os.path.join(CACHE_DIR, f"{h}.mp3")
    wav_path = os.path.join(CACHE_DIR, f"{h}.wav")

    if not os.path.exists(mp3_path) or os.path.getsize(mp3_path) == 0:
        tts = gTTS(text=text, lang=lang, tld=tld)
        tts.save(mp3_path)

    if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
        subprocess.run([
            FFMPEG, "-y", "-i", mp3_path,
            "-ar", "44100", "-ac", "1",
            wav_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    sr, data = wav.read(wav_path)
    thresh = np.max(np.abs(data)) * 0.04 if len(data) > 0 and np.max(np.abs(data)) > 0 else 1
    non_silent = np.where(np.abs(data) > thresh)[0]
    if len(non_silent) > 0:
        data = data[max(0, non_silent[0] - 200) : min(len(data), non_silent[-1] + 200)]
    return data

def main():
    with open("verbs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    verbs = data["verbs"]

    print(f"Loaded {len(verbs)} verbs from verbs_data.json")

    # Split into 3 chapters according to the PDF:
    # Page 1: 1..49 (Arise to Freeze)
    # Page 2: 50..102 (Get to Shut)
    # Page 3: 103..154 (Sing to Write)
    ch1_verbs = verbs[:49]
    ch2_verbs = verbs[49:102]
    ch3_verbs = verbs[102:]

    chapters = [
        {
            "num": 1,
            "title": "Chapter 1: Page 1 — Verbs from Arise to Freeze",
            "intro": "Welcome to Chapter 1! Here are the irregular verbs from page 1, from Arise to Freeze. Follow along with your PDF!",
            "verbs": ch1_verbs
        },
        {
            "num": 2,
            "title": "Chapter 2: Page 2 — Verbs from Get to Shut",
            "intro": "Welcome to Chapter 2! Verbs from page 2, from Get to Shut. Keep up the great focus!",
            "verbs": ch2_verbs
        },
        {
            "num": 3,
            "title": "Chapter 3: Page 3 — Verbs from Sing to Write",
            "intro": "Welcome to Chapter 3! The final stretch from Sing to Write. Let's finish strong!",
            "verbs": ch3_verbs
        }
    ]

    # Pre-fetch all TTS
    fetch_list = [
        ("The Complete Irregular Verbs Study Guide. All 154 verbs from your PDF in exact alphabetical order. Let's begin!", "en"),
        ("Congratulations! You have listened to all 154 irregular verbs from the PDF. Repeat regularly to achieve complete mastery!", "en")
    ]

    for ch in chapters:
        fetch_list.append((ch["intro"], "en"))
        for v in ch["verbs"]:
            # Format: "Arise, arose, arisen"
            en_phrase = f"{v['infinitive']}, {v['past_simple']}, {v['past_participle']}"
            fetch_list.append((en_phrase, "en"))
            fetch_list.append((v["spanish"], "es"))

    unique_items = list({(t, l): True for t, l in fetch_list}.keys())
    print(f"Fetching {len(unique_items)} TTS clips for Song 2...")
    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(lambda item: fetch_tts(item[0], item[1]), unique_items))
    print("All TTS clips fetched!")

    BPM = 88
    beat_sec = 60.0 / BPM
    bar_sec = beat_sec * 4.0
    sample_rate = 44100

    timeline = []
    current_time = 2.0
    lyrics_data = []

    # Intro
    intro_txt = "The Complete Irregular Verbs Study Guide. All 154 verbs from your PDF in exact alphabetical order. Let's begin!"
    intro_aud = fetch_tts(intro_txt, "en")
    timeline.append({"time": current_time, "audio": intro_aud, "lang": "en"})
    lyrics_data.append({
        "type": "intro",
        "section": "Introduction",
        "start": round(current_time, 2),
        "text": intro_txt
    })
    current_time += (len(intro_aud) / sample_rate) + 1.2
    current_time = np.ceil(current_time / bar_sec) * bar_sec

    for ch in chapters:
        # Chapter announcement
        ch_aud = fetch_tts(ch["intro"], "en")
        timeline.append({"time": current_time, "audio": ch_aud, "lang": "en"})
        lyrics_data.append({
            "type": "chapter_header",
            "section": ch["title"],
            "start": round(current_time, 2),
            "text": ch["title"]
        })
        current_time += (len(ch_aud) / sample_rate) + 1.0
        current_time = np.ceil(current_time / bar_sec) * bar_sec

        # Verbs in chapter
        for v in ch["verbs"]:
            en_phrase = f"{v['infinitive']}, {v['past_simple']}, {v['past_participle']}"
            es_phrase = v["spanish"]

            en_aud = fetch_tts(en_phrase, "en")
            es_aud = fetch_tts(es_phrase, "es")

            v_start = current_time
            timeline.append({"time": current_time, "audio": en_aud, "lang": "en"})

            es_time = current_time + (len(en_aud) / sample_rate) + 0.35
            timeline.append({"time": es_time, "audio": es_aud, "lang": "es"})

            total_v_dur = (es_time - v_start) + (len(es_aud) / sample_rate) + 0.4
            needed_beats = max(4, int(np.ceil(total_v_dur / beat_sec)))
            step_sec = needed_beats * beat_sec

            lyrics_data.append({
                "type": "verb",
                "id": v["id"],
                "section": ch["title"],
                "start": round(v_start, 2),
                "end": round(v_start + step_sec, 2),
                "infinitive": v["infinitive"],
                "past_simple": v["past_simple"],
                "past_participle": v["past_participle"],
                "spanish": v["spanish"]
            })
            current_time += step_sec

        # Chapter breather
        current_time += bar_sec

    # Outro
    outro_txt = "Congratulations! You have listened to all 154 irregular verbs from the PDF. Repeat regularly to achieve complete mastery!"
    outro_aud = fetch_tts(outro_txt, "en")
    timeline.append({"time": current_time, "audio": outro_aud, "lang": "en"})
    lyrics_data.append({
        "type": "outro",
        "section": "Conclusion",
        "start": round(current_time, 2),
        "text": outro_txt
    })
    current_time += (len(outro_aud) / sample_rate) + bar_sec * 2.0

    total_duration = current_time
    print(f"Song 2 Duration: {total_duration:.1f}s ({total_duration/60.0:.2f} mins)")

    # Backing track
    print("Generating lo-fi study backing track...")
    backing = generate_backing_track(total_duration, bpm=BPM, sample_rate=sample_rate)

    total_samples = len(backing)
    vox_l = np.zeros(total_samples, dtype=np.float32)
    vox_r = np.zeros(total_samples, dtype=np.float32)

    for ev in timeline:
        st = int(ev["time"] * sample_rate)
        aud = ev["audio"].astype(np.float32) / 32767.0
        en = st + len(aud)
        if st >= total_samples:
            continue
        act_en = min(en, total_samples)
        slen = act_en - st
        pan_l = 0.52 if ev["lang"] == "en" else 0.48
        pan_r = 0.48 if ev["lang"] == "en" else 0.52
        vox_l[st:act_en] += aud[:slen] * pan_l * 1.25
        vox_r[st:act_en] += aud[:slen] * pan_r * 1.25

    back_l = backing[:, 0].astype(np.float32) / 32767.0
    back_r = backing[:, 1].astype(np.float32) / 32767.0

    vox_env = np.abs(vox_l) + np.abs(vox_r)
    duck = 1.0 - np.clip(vox_env * 0.35, 0.0, 0.4)

    mst_l = (back_l * 0.48 * duck) + (vox_l * 0.95)
    mst_r = (back_r * 0.48 * duck) + (vox_r * 0.95)

    peak = max(np.max(np.abs(mst_l)), np.max(np.abs(mst_r)), 1e-4)
    gain = 0.95 / peak
    mst_l = np.clip(mst_l * gain, -1.0, 1.0)
    mst_r = np.clip(mst_r * gain, -1.0, 1.0)

    mst = np.column_stack((mst_l, mst_r))
    temp_wav = "temp_song2_master.wav"
    wav.write(temp_wav, sample_rate, (mst * 32767).astype(np.int16))

    out_mp3 = "02_Irregular_Verbs_Complete_A_to_Z.mp3"
    print(f"Encoding {out_mp3}...")
    subprocess.run([
        FFMPEG, "-y", "-i", temp_wav,
        "-codec:a", "libmp3lame",
        "-b:a", "192k",
        "-metadata", "title=Complete Irregular Verbs A to Z (All 154 Verbs)",
        "-metadata", "artist=English Irregular Verbs Academy",
        "-metadata", "album=Irregular Verbs PDF Songbook",
        "-metadata", "genre=Educational Lo-Fi Chillhop",
        "-metadata", "year=2026",
        out_mp3
    ], check=True)

    if os.path.exists(temp_wav):
        os.remove(temp_wav)

    with open("atoz_lyrics.json", "w", encoding="utf-8") as f:
        json.dump({
            "song_title": "Complete Irregular Verbs A to Z",
            "file": out_mp3,
            "duration_sec": total_duration,
            "bpm": BPM,
            "lyrics": lyrics_data
        }, f, indent=2, ensure_ascii=False)

    print(f"Successfully created {out_mp3} and atoz_lyrics.json!")

if __name__ == "__main__":
    main()
