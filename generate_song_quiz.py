"""
Generate Song 3: 03_Irregular_Verbs_Challenge_Quiz.mp3
The Active Recall Challenge Track!
Voice announces Infinitive & Past Simple, pauses with rhythmic tension,
then reveals the Past Participle and Spanish translation!
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

quiz_verbs = [
    ("Begin", "Began", "Begun", "Empezar"),
    ("Break", "Broke", "Broken", "Romper"),
    ("Bring", "Brought", "Brought", "Traer"),
    ("Buy", "Bought", "Bought", "Comprar"),
    ("Catch", "Caught", "Caught", "Atrapar"),
    ("Choose", "Chose", "Chosen", "Elegir"),
    ("Come", "Came", "Come", "Venir"),
    ("Do", "Did", "Done", "Hacer"),
    ("Drink", "Drank", "Drunk", "Beber"),
    ("Drive", "Drove", "Driven", "Conducir"),
    ("Eat", "Ate", "Eaten", "Comer"),
    ("Fall", "Fell", "Fallen", "Caer"),
    ("Feel", "Felt", "Felt", "Sentir"),
    ("Find", "Found", "Found", "Encontrar"),
    ("Fly", "Flew", "Flown", "Volar"),
    ("Forget", "Forgot", "Forgotten", "Olvidar"),
    ("Get", "Got", "Gotten", "Obtener"),
    ("Give", "Gave", "Given", "Dar"),
    ("Go", "Went", "Gone", "Ir"),
    ("Grow", "Grew", "Grown", "Crecer"),
    ("Have", "Had", "Had", "Tener"),
    ("Hear", "Heard", "Heard", "Oír"),
    ("Keep", "Kept", "Kept", "Guardar"),
    ("Know", "Knew", "Known", "Saber"),
    ("Leave", "Left", "Left", "Dejar"),
    ("Make", "Made", "Made", "Hacer"),
    ("Pay", "Paid", "Paid", "Pagar"),
    ("Ride", "Rode", "Ridden", "Montar"),
    ("Ring", "Rang", "Rung", "Sonar"),
    ("Run", "Ran", "Run", "Correr"),
    ("Say", "Said", "Said", "Decir"),
    ("See", "Saw", "Seen", "Ver"),
    ("Send", "Sent", "Sent", "Enviar"),
    ("Sing", "Sang", "Sung", "Cantar"),
    ("Sleep", "Slept", "Slept", "Dormir"),
    ("Speak", "Spoke", "Spoken", "Hablar"),
    ("Swim", "Swam", "Swum", "Nadar"),
    ("Take", "Took", "Taken", "Tomar"),
    ("Teach", "Taught", "Taught", "Enseñar"),
    ("Tell", "Told", "Told", "Contar"),
    ("Think", "Thought", "Thought", "Pensar"),
    ("Understand", "Understood", "Understood", "Entender"),
    ("Wear", "Wore", "Worn", "Llevar puesto"),
    ("Win", "Won", "Won", "Ganar"),
    ("Write", "Wrote", "Written", "Escribir"),
]

def main():
    print(f"Preparing Quiz Challenge with {len(quiz_verbs)} verbs...")

    fetch_list = [
        ("Welcome to the Irregular Verbs Beat Challenge!", "en"),
        ("I will say the infinitive and the past. When the beat drops, shout out the participle before I do! Are you ready? Let's go!", "en"),
        ("¡Ponte a prueba! Di el participio en voz alta antes de que suene la respuesta.", "es"),
        ("Halfway mark! You are crushing it, keep going!", "en"),
        ("Boom! Challenge completed! You tested yourself and won! Keep practicing to be an irregular verb master!", "en")
    ]

    for idx, (inf, past, part, esp) in enumerate(quiz_verbs, 1):
        fetch_list.append((f"Number {idx}: {inf}... {past}...", "en"))
        fetch_list.append((part, "en"))
        fetch_list.append((esp, "es"))

    unique_items = list({(t, l): True for t, l in fetch_list}.keys())
    print(f"Fetching {len(unique_items)} TTS clips for Quiz track...")
    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(lambda item: fetch_tts(item[0], item[1]), unique_items))
    print("All quiz TTS clips fetched!")

    BPM = 104
    beat_sec = 60.0 / BPM
    bar_sec = beat_sec * 4.0
    sample_rate = 44100

    timeline = []
    current_time = 2.0
    lyrics_data = []

    # Intro
    intro_lines = [
        ("Welcome to the Irregular Verbs Beat Challenge!", "en"),
        ("I will say the infinitive and the past. When the beat drops, shout out the participle before I do! Are you ready? Let's go!", "en"),
        ("¡Ponte a prueba! Di el participio en voz alta antes de que suene la respuesta.", "es"),
    ]
    lyrics_data.append({
        "type": "intro",
        "section": "Challenge Intro",
        "start": round(current_time, 2),
        "text": "Get ready! Shout the 3rd form on the beat!"
    })
    for text, lang in intro_lines:
        aud = fetch_tts(text, lang)
        timeline.append({"time": current_time, "audio": aud, "lang": lang})
        current_time += (len(aud) / sample_rate) + 0.65
    current_time = np.ceil(current_time / bar_sec) * bar_sec

    mid_point = len(quiz_verbs) // 2

    for idx, (inf, past, part, esp) in enumerate(quiz_verbs, 1):
        if idx == mid_point + 1:
            mid_text = "Halfway mark! You are crushing it, keep going!"
            mid_aud = fetch_tts(mid_text, "en")
            timeline.append({"time": current_time, "audio": mid_aud, "lang": "en"})
            lyrics_data.append({
                "type": "checkpoint",
                "section": "Halfway Checkpoint",
                "start": round(current_time, 2),
                "text": mid_text
            })
            current_time += (len(mid_aud) / sample_rate) + 0.8
            current_time = np.ceil(current_time / bar_sec) * bar_sec

        q_prompt = f"Number {idx}: {inf}... {past}..."
        q_aud = fetch_tts(q_prompt, "en")
        part_aud = fetch_tts(part, "en")
        esp_aud = fetch_tts(esp, "es")

        q_start = current_time
        timeline.append({"time": current_time, "audio": q_aud, "lang": "en"})
        q_dur = len(q_aud) / sample_rate

        # Challenge pause: give user 2.2 seconds of musical anticipation
        answer_time = current_time + q_dur + 1.8
        timeline.append({"time": answer_time, "audio": part_aud, "lang": "en"})
        part_dur = len(part_aud) / sample_rate

        esp_time = answer_time + part_dur + 0.25
        timeline.append({"time": esp_time, "audio": esp_aud, "lang": "es"})
        esp_dur = len(esp_aud) / sample_rate

        item_total_dur = (esp_time - q_start) + esp_dur + 0.4
        needed_beats = max(4, int(np.ceil(item_total_dur / beat_sec)))
        step_sec = needed_beats * beat_sec

        lyrics_data.append({
            "type": "quiz_item",
            "number": idx,
            "start": round(q_start, 2),
            "answer_time": round(answer_time, 2),
            "end": round(q_start + step_sec, 2),
            "infinitive": inf,
            "past_simple": past,
            "past_participle": part,
            "spanish": esp
        })
        current_time += step_sec

    # Outro
    outro_text = "Boom! Challenge completed! You tested yourself and won! Keep practicing to be an irregular verb master!"
    outro_aud = fetch_tts(outro_text, "en")
    timeline.append({"time": current_time, "audio": outro_aud, "lang": "en"})
    lyrics_data.append({
        "type": "outro",
        "section": "Victory Outro",
        "start": round(current_time, 2),
        "text": outro_text
    })
    current_time += (len(outro_aud) / sample_rate) + bar_sec * 2.0

    total_duration = current_time
    print(f"Quiz Track Duration: {total_duration:.1f}s ({total_duration/60.0:.2f} mins)")

    # Backing track
    print("Generating challenge backing track...")
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
        pan_l = 0.54 if ev["lang"] == "en" else 0.46
        pan_r = 0.46 if ev["lang"] == "en" else 0.54
        vox_l[st:act_en] += aud[:slen] * pan_l * 1.3
        vox_r[st:act_en] += aud[:slen] * pan_r * 1.3

    back_l = backing[:, 0].astype(np.float32) / 32767.0
    back_r = backing[:, 1].astype(np.float32) / 32767.0

    vox_env = np.abs(vox_l) + np.abs(vox_r)
    duck = 1.0 - np.clip(vox_env * 0.35, 0.0, 0.42)

    mst_l = (back_l * 0.50 * duck) + (vox_l * 0.95)
    mst_r = (back_r * 0.50 * duck) + (vox_r * 0.95)

    peak = max(np.max(np.abs(mst_l)), np.max(np.abs(mst_r)), 1e-4)
    gain = 0.95 / peak
    mst_l = np.clip(mst_l * gain, -1.0, 1.0)
    mst_r = np.clip(mst_r * gain, -1.0, 1.0)

    mst = np.column_stack((mst_l, mst_r))
    temp_wav = "temp_song3_master.wav"
    wav.write(temp_wav, sample_rate, (mst * 32767).astype(np.int16))

    out_mp3 = "03_Irregular_Verbs_Challenge_Quiz.mp3"
    print(f"Encoding {out_mp3}...")
    subprocess.run([
        FFMPEG, "-y", "-i", temp_wav,
        "-codec:a", "libmp3lame",
        "-b:a", "192k",
        "-metadata", "title=Irregular Verbs Beat Challenge (Active Recall)",
        "-metadata", "artist=English Irregular Verbs Academy",
        "-metadata", "album=Irregular Verbs PDF Songbook",
        "-metadata", "genre=Educational Quiz Track",
        "-metadata", "year=2026",
        out_mp3
    ], check=True)

    if os.path.exists(temp_wav):
        os.remove(temp_wav)

    with open("quiz_lyrics.json", "w", encoding="utf-8") as f:
        json.dump({
            "song_title": "Irregular Verbs Beat Challenge",
            "file": out_mp3,
            "duration_sec": total_duration,
            "bpm": BPM,
            "lyrics": lyrics_data
        }, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {out_mp3} and quiz_lyrics.json!")

if __name__ == "__main__":
    main()
