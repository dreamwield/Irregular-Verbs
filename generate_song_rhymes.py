"""
Generate Song 1: 01_Irregular_Verbs_Rhyme_Song.mp3
The ultimate pedagogical song grouping irregular verbs by sound and rhyming families.
Includes dual English/Spanish vocals, rhythmic backing track, and synced lyrics output.
"""
import os
import sys
import json
import time
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
    # Trim leading and trailing near-silence
    thresh = np.max(np.abs(data)) * 0.04 if len(data) > 0 and np.max(np.abs(data)) > 0 else 1
    non_silent = np.where(np.abs(data) > thresh)[0]
    if len(non_silent) > 0:
        data = data[max(0, non_silent[0] - 200) : min(len(data), non_silent[-1] + 200)]
    return data

# Build song structure: Intro, Verses, Choruses, Outro
song_script = [
    # INTRO
    {
        "type": "intro",
        "title": "Welcome & Intro",
        "spoken": [
            ("Yo! Welcome to the Irregular Verbs Song!", "en"),
            ("Let's get these verbs inside your brain with rhythm and rhyme!", "en"),
            ("¡Vamos a aprender los verbos irregulares!", "es"),
            ("Repeat each form, feel the groove, and let's go!", "en")
        ]
    },
    # CHORUS 1
    {
        "type": "chorus",
        "title": "Chorus 1",
        "spoken": [
            ("Irregular verbs, sing them on time!", "en"),
            ("Learn every form with the rhythm and rhyme!", "en"),
            ("Infinitive, past, and participle too!", "en"),
            ("Sing it out loud, let the rhythm guide you!", "en")
        ]
    },
    # SECTION 1: The Triple Clones (All 3 forms identical)
    {
        "type": "verse",
        "section_name": "Part 1: The Triple Clones (No Change)",
        "intro_line": ("Part 1: The Triple Clones! All three forms are the same!", "en"),
        "verbs": [
            ("Bet, bet, bet", "Apostar"),
            ("Cost, cost, cost", "Costar"),
            ("Cut, cut, cut", "Cortar"),
            ("Hit, hit, hit", "Golpear"),
            ("Hurt, hurt, hurt", "Herir"),
            ("Let, let, let", "Permitir"),
            ("Put, put, put", "Poner"),
            ("Read, read, read", "Leer"),
            ("Set, set, set", "Establecer"),
            ("Shut, shut, shut", "Cerrar"),
            ("Split, split, split", "Partir"),
            ("Spread, spread, spread", "Extender"),
            ("Burst, burst, burst", "Reventar"),
            ("Wet, wet, wet", "Mojar"),
        ]
    },
    # SECTION 2: The I - A - U Shift
    {
        "type": "verse",
        "section_name": "Part 2: The I - A - U Vowel Shift",
        "intro_line": ("Part 2: The I - A - U Vowel Shift! Sing along!", "en"),
        "verbs": [
            ("Sing, sang, sung", "Cantar"),
            ("Sink, sank, sunk", "Hundir"),
            ("Drink, drank, drunk", "Beber"),
            ("Ring, rang, rung", "Sonar"),
            ("Begin, began, begun", "Empezar"),
            ("Swim, swam, swum", "Nadar"),
            ("Run, ran, run", "Correr"),
            ("Shrink, shrank, shrunk", "Encogerse"),
            ("Spring, sprang, sprung", "Saltar"),
        ]
    },
    # SECTION 3: The OUGHT and AUGHT Group
    {
        "type": "verse",
        "section_name": "Part 3: The OUGHT and AUGHT Rhyme Group",
        "intro_line": ("Part 3: The OUGHT and AUGHT crew! Hear the rhyme!", "en"),
        "verbs": [
            ("Bring, brought, brought", "Traer"),
            ("Buy, bought, bought", "Comprar"),
            ("Catch, caught, caught", "Atrapar"),
            ("Fight, fought, fought", "Luchar"),
            ("Seek, sought, sought", "Buscar"),
            ("Teach, taught, taught", "Enseñar"),
            ("Think, thought, thought", "Pensar"),
        ]
    },
    # CHORUS 2
    {
        "type": "chorus",
        "title": "Chorus 2",
        "spoken": [
            ("Irregular verbs, sing them on time!", "en"),
            ("Learn every form with the rhythm and rhyme!", "en"),
            ("You are doing great, keep up the pace!", "en"),
            ("Three forms of verbs in every case!", "en")
        ]
    },
    # SECTION 4: The OW - EW - OWN Flyers
    {
        "type": "verse",
        "section_name": "Part 4: The Blow, Blew, Blown Family",
        "intro_line": ("Part 4: The Blow, Blew, Blown family! Ready to fly!", "en"),
        "verbs": [
            ("Blow, blew, blown", "Soplar"),
            ("Grow, grew, grown", "Crecer"),
            ("Know, knew, known", "Saber"),
            ("Throw, threw, thrown", "Lanzar"),
            ("Fly, flew, flown", "Volar"),
            ("Draw, drew, drawn", "Dibujar"),
        ]
    },
    # SECTION 5: The SLEPT & KEPT Crew
    {
        "type": "verse",
        "section_name": "Part 5: Sleep, Slept, Slept Group",
        "intro_line": ("Part 5: Sleep, slept, slept! Keep that rhythm tight!", "en"),
        "verbs": [
            ("Sleep, slept, slept", "Dormir"),
            ("Keep, kept, kept", "Guardar"),
            ("Creep, crept, crept", "Arrastrarse"),
            ("Feel, felt, felt", "Sentir"),
            ("Leave, left, left", "Dejar"),
            ("Meet, met, met", "Encontrar"),
            ("Feed, fed, fed", "Alimentar"),
            ("Lead, led, led", "Guiar"),
            ("Mean, meant, meant", "Significar"),
        ]
    },
    # SECTION 6: The -D to -T Transformers
    {
        "type": "verse",
        "section_name": "Part 6: Turn the D into T",
        "intro_line": ("Part 6: Turn the D into T! Listen close!", "en"),
        "verbs": [
            ("Send, sent, sent", "Enviar"),
            ("Spend, spent, spent", "Gastar"),
            ("Lend, lent, lent", "Prestar"),
            ("Bend, bent, bent", "Doblar"),
            ("Build, built, built", "Construir"),
            ("Lose, lost, lost", "Perder"),
            ("Bleed, bled, bled", "Sangrar"),
        ]
    },
    # CHORUS 3
    {
        "type": "chorus",
        "title": "Chorus 3",
        "spoken": [
            ("Irregular verbs, sing them on time!", "en"),
            ("Every single pattern locked in your mind!", "en"),
            ("Almost there, don't stop now!", "en"),
            ("Sing them loud and show them how!", "en")
        ]
    },
    # SECTION 7: The OKE and OKEN Rockers
    {
        "type": "verse",
        "section_name": "Part 7: Break, Broke, Broken",
        "intro_line": ("Part 7: Break, broke, broken! Rock this beat!", "en"),
        "verbs": [
            ("Break, broke, broken", "Romper"),
            ("Choose, chose, chosen", "Elegir"),
            ("Freeze, froze, frozen", "Congelar"),
            ("Speak, spoke, spoken", "Hablar"),
            ("Steal, stole, stolen", "Robar"),
            ("Wake, woke, woken", "Despertar"),
        ]
    },
    # SECTION 8: The WORE and WORN Flow
    {
        "type": "verse",
        "section_name": "Part 8: Wear, Wore, Worn",
        "intro_line": ("Part 8: Wear, wore, worn! Sing it out!", "en"),
        "verbs": [
            ("Wear, wore, worn", "Vestir"),
            ("Tear, tore, torn", "Rasgar"),
            ("Swear, swore, sworn", "Jurar"),
            ("Bear, bore, born", "Soportar"),
        ]
    },
    # SECTION 9: The DRIVE - DROVE - DRIVEN Highway
    {
        "type": "verse",
        "section_name": "Part 9: Drive, Drove, Driven",
        "intro_line": ("Part 9: Hit the highway! Drive, drove, driven!", "en"),
        "verbs": [
            ("Drive, drove, driven", "Conducir"),
            ("Ride, rode, ridden", "Montar"),
            ("Rise, rose, risen", "Levantarse"),
            ("Write, wrote, written", "Escribir"),
            ("Arise, arose, arisen", "Surgir"),
            ("Bite, bit, bitten", "Morder"),
            ("Hide, hid, hidden", "Esconder"),
        ]
    },
    # SECTION 10: The Essential Power Verbs
    {
        "type": "verse",
        "section_name": "Part 10: Essential Power Verbs",
        "intro_line": ("Part 10: Essential Power Verbs! The English classics!", "en"),
        "verbs": [
            ("Be: was or were, been", "Ser o estar"),
            ("Do, did, done", "Hacer"),
            ("Go, went, gone", "Ir"),
            ("Have, had, had", "Tener"),
            ("Come, came, come", "Venir"),
            ("Become, became, become", "Llegar a ser"),
            ("Give, gave, given", "Dar"),
            ("Forgive, forgave, forgiven", "Perdonar"),
            ("Get, got, gotten", "Obtener"),
            ("Forget, forgot, forgotten", "Olvidar"),
            ("See, saw, seen", "Ver"),
            ("Eat, ate, eaten", "Comer"),
            ("Fall, fell, fallen", "Caer"),
            ("Take, took, taken", "Tomar"),
            ("Shake, shook, shaken", "Sacudir"),
            ("Make, made, made", "Hacer"),
            ("Say, said, said", "Decir"),
            ("Pay, paid, paid", "Pagar"),
            ("Tell, told, told", "Contar"),
            ("Sell, sold, sold", "Vender"),
            ("Find, found, found", "Encontrar"),
            ("Win, won, won", "Ganar"),
            ("Understand, understood, understood", "Entender"),
        ]
    },
    # OUTRO
    {
        "type": "outro",
        "title": "Outro & Congratulations",
        "spoken": [
            ("Yeah! You did it! Fantastic job!", "en"),
            ("¡Enhorabuena! Has cantado todos los grupos de verbos.", "es"),
            ("Play this song whenever you study, and you will remember every verb!", "en"),
            ("Keep singing, keep grooving, and see you next time!", "en")
        ]
    }
]

print("Collecting all required audio snippets...")
fetch_tasks = []
for block in song_script:
    if block["type"] in ["intro", "chorus", "outro"]:
        for text, lang in block["spoken"]:
            fetch_tasks.append((text, lang))
    elif block["type"] == "verse":
        fetch_tasks.append((block["intro_line"][0], block["intro_line"][1]))
        for en_text, es_text in block["verbs"]:
            fetch_tasks.append((en_text, "en"))
            fetch_tasks.append((es_text, "es"))

# De-duplicate
unique_tasks = list({(t, l): True for t, l in fetch_tasks}.keys())
print(f"Total unique TTS snippets to cache: {len(unique_tasks)}")

def worker(item):
    text, lang = item
    fetch_tts(text, lang)

with ThreadPoolExecutor(max_workers=8) as executor:
    list(executor.map(worker, unique_tasks))
print("All TTS clips fetched and cached!")

# Now assemble song timeline
print("Assembling song timeline and timing...")
BPM = 102
beat_sec = 60.0 / BPM
bar_sec = beat_sec * 4.0
sample_rate = 44100

timeline_events = []
current_time = 2.0  # 2 seconds of beat before vocals kick in

lyrics_data = []

for block in song_script:
    b_type = block["type"]

    if b_type in ["intro", "chorus", "outro"]:
        lyrics_data.append({
            "section": block["title"],
            "start": round(current_time, 2),
            "type": b_type,
            "text": " / ".join([s[0] for s in block["spoken"]])
        })
        for text, lang in block["spoken"]:
            audio = fetch_tts(text, lang)
            dur = len(audio) / sample_rate
            timeline_events.append({
                "time": current_time,
                "audio": audio,
                "text": text,
                "lang": lang
            })
            current_time += dur + 0.65
        # Round up to next musical bar
        current_time = np.ceil(current_time / bar_sec) * bar_sec

    elif b_type == "verse":
        lyrics_data.append({
            "section": block["section_name"],
            "start": round(current_time, 2),
            "type": "verse_header",
            "text": block["section_name"]
        })
        # Verse Intro Line
        intro_text, intro_lang = block["intro_line"]
        intro_audio = fetch_tts(intro_text, intro_lang)
        timeline_events.append({
            "time": current_time,
            "audio": intro_audio,
            "text": intro_text,
            "lang": intro_lang
        })
        current_time += (len(intro_audio) / sample_rate) + 0.8
        current_time = np.ceil(current_time / bar_sec) * bar_sec

        # Verse Verbs
        for en_verb, es_trans in block["verbs"]:
            en_audio = fetch_tts(en_verb, "en")
            es_audio = fetch_tts(es_trans, "es")

            verb_start = current_time
            en_dur = len(en_audio) / sample_rate
            es_dur = len(es_audio) / sample_rate

            timeline_events.append({
                "time": current_time,
                "audio": en_audio,
                "text": en_verb,
                "lang": "en"
            })
            # Spanish translation plays right after English
            es_start = current_time + en_dur + 0.35
            timeline_events.append({
                "time": es_start,
                "audio": es_audio,
                "text": es_trans,
                "lang": "es"
            })

            verb_total_dur = (es_start - verb_start) + es_dur + 0.45
            # Snap to beats for musical groove (usually 2 or 3 bars)
            needed_beats = int(np.ceil(verb_total_dur / beat_sec))
            # Keep minimum spacing
            if needed_beats < 4:
                needed_beats = 4

            step_sec = needed_beats * beat_sec
            lyrics_data.append({
                "section": block["section_name"],
                "start": round(verb_start, 2),
                "end": round(verb_start + step_sec, 2),
                "type": "verb",
                "english": en_verb,
                "spanish": es_trans
            })
            current_time += step_sec

        # Bar break after each verse
        current_time += bar_sec * 0.5
        current_time = np.ceil(current_time / bar_sec) * bar_sec

# Add final musical outro padding
total_song_duration = current_time + bar_sec * 2.0
print(f"Total Song Duration: {total_song_duration:.1f} seconds ({total_song_duration/60.0:.2f} minutes)")

# Synthesize the full musical backing track
print("Synthesizing rich stereo musical backing track...")
backing_audio = generate_backing_track(total_song_duration, bpm=BPM, sample_rate=sample_rate)

# Mix vocals into buffer
total_samples = len(backing_audio)
vocal_buffer_l = np.zeros(total_samples, dtype=np.float32)
vocal_buffer_r = np.zeros(total_samples, dtype=np.float32)

print(f"Mixing {len(timeline_events)} vocal events into the master timeline...")
for ev in timeline_events:
    start_s = int(ev["time"] * sample_rate)
    aud = ev["audio"].astype(np.float32) / 32767.0
    end_s = start_s + len(aud)
    if start_s >= total_samples:
        continue
    actual_end = min(end_s, total_samples)
    seg_len = actual_end - start_s

    # English slightly left-centered (0.55/0.45), Spanish slightly right-centered (0.45/0.55)
    pan_l = 0.55 if ev["lang"] == "en" else 0.45
    pan_r = 0.45 if ev["lang"] == "en" else 0.55
    vocal_buffer_l[start_s:actual_end] += aud[:seg_len] * pan_l * 1.3
    vocal_buffer_r[start_s:actual_end] += aud[:seg_len] * pan_r * 1.3

# Final mixdown with soft mastering compression
backing_l = backing_audio[:, 0].astype(np.float32) / 32767.0
backing_r = backing_audio[:, 1].astype(np.float32) / 32767.0

# Sidechain ducking: when vocals are loud, dip backing track by ~2.5 dB
vocal_envelope = np.abs(vocal_buffer_l) + np.abs(vocal_buffer_r)
duck_factor = 1.0 - np.clip(vocal_envelope * 0.35, 0.0, 0.45)

master_l = (backing_l * 0.52 * duck_factor) + (vocal_buffer_l * 0.95)
master_r = (backing_r * 0.52 * duck_factor) + (vocal_buffer_r * 0.95)

# Limiter & Normalization
peak = max(np.max(np.abs(master_l)), np.max(np.abs(master_r)), 1e-4)
gain = 0.95 / peak
master_l = np.clip(master_l * gain, -1.0, 1.0)
master_r = np.clip(master_r * gain, -1.0, 1.0)

master_stereo = np.column_stack((master_l, master_r))
temp_wav = "temp_song1_master.wav"
wav.write(temp_wav, sample_rate, (master_stereo * 32767).astype(np.int16))

# Render to 192k MP3 with metadata ID3 tags
output_mp3 = "01_Irregular_Verbs_Rhyme_Song.mp3"
print(f"Encoding master MP3: {output_mp3}...")
subprocess.run([
    FFMPEG, "-y", "-i", temp_wav,
    "-codec:a", "libmp3lame",
    "-b:a", "192k",
    "-metadata", "title=Irregular Verbs Rhyme Song (Learn by Rhyme)",
    "-metadata", "artist=English Irregular Verbs Academy",
    "-metadata", "album=Irregular Verbs PDF Songbook",
    "-metadata", "genre=Educational / Hip-Hop Groove",
    "-metadata", "year=2026",
    output_mp3
], check=True)

if os.path.exists(temp_wav):
    os.remove(temp_wav)

# Save lyrics sync JSON
with open("rhymes_lyrics.json", "w", encoding="utf-8") as f:
    json.dump({
        "song_title": "Irregular Verbs Rhyme Song",
        "file": output_mp3,
        "duration_sec": total_song_duration,
        "bpm": BPM,
        "lyrics": lyrics_data
    }, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {output_mp3} and rhymes_lyrics.json!")
