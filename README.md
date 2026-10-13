# 🎵 Irregular Verbs Music Academy (Canción y Entrenador de Verbos Irregulares)

> Aprende y memoriza los **154 verbos irregulares en inglés** de la lista oficial del PDF a través del ritmo, la música y técnicas mnemotécnicas de rima y repetición auditiva.

---

## 🎧 Contenido Musical (Archivos MP3 Incluidos)

El repositorio incluye 3 canciones producidas en formato MP3 (192 kbps) con bases rítmicas originales y pronunciación nativa:

1. **`01_Irregular_Verbs_Rhyme_Song.mp3`** (8 min 45 s · 12.6 MB)
   - **El método más rápido por asociación sonora:** Agrupa los verbos en 10 familias con terminaciones y patrones que riman (*The Triple Clones [Bet-Bet-Bet], Sing-Sang-Sung, Ought-Aught, Blow-Blew-Blown, Sleep-Slept-Slept, D a T, Break-Broke-Broken, Wear-Wore-Worn, Drive-Drove-Driven y Power Verbs*).
2. **`02_Irregular_Verbs_Complete_A_to_Z.mp3`** (12 min 15 s · 17.6 MB)
   - **Pista de estudio Lo-Fi Chillhop completa:** Recorre los **154 verbos en el orden exacto del PDF original** (*Arise* a *Write*).
   - Dividida en 3 capítulos correspondientes a las páginas del PDF:
     - **Página 1 (#1 a #49):** *Arise* a *Freeze*
     - **Página 2 (#50 a #102):** *Get* a *Shut*
     - **Página 3 (#103 a #154):** *Sing* a *Write*
3. **`03_Irregular_Verbs_Challenge_Quiz.mp3`** (5 min 44 s · 8.26 MB)
   - **Entrenamiento de memoria activa:** La voz dice el infinitivo y pasado, deja un silencio musical para que cantes el participio en voz alta y luego te confirma el resultado con su traducción.

---

## 💻 Aplicación Web Interactiva (`index.html`)

Puedes abrir directamente el archivo `index.html` en cualquier navegador web moderno (Edge, Chrome, Firefox, Safari).

### Características:
- **Reproductor con Visualizador:** Control de volumen, salto de 10s y velocidad regulable (**0.75x**, **0.9x**, **1.0x**, **1.25x**).
- **Karaoke en Vivo Sincronizado:** Las letras y tarjetas de verbos se iluminan en tiempo real según el compás de la canción. Puedes hacer clic en cualquier línea para saltar a ese segundo del audio.
- **Selector de Rango para el Quiz:**
  - Practica por bloques:
    - **Página 1 (#1 a #49):** *Arise a Freeze*
    - **Página 2 (#50 a #102):** *Get a Shut*
    - **Página 3 (#103 a #154):** *Sing a Write*
    - **Todos (#1 a #154)**
    - **Rango Personalizado:** Define libremente qué rango de verbos estudiar (por ejemplo del 1 al 49).
- **Explorador y Soundboard de los 154 Verbos:** Buscador en inglés y español, filtros por familias fonéticas y botón de audio para escuchar la pronunciación aislada de cada verbo.
- **Centro de Descargas:** Enlaces directos para descargar los MP3 y consultar el `IRREGULAR-VERBS.pdf` original.

---

## 🚀 Publicación en GitHub Pages

Para ver y usar la aplicación directamente desde la web sin descargar nada:
1. En GitHub, ve a **Settings** > **Pages**.
2. En **Build and deployment** > **Branch**, selecciona `main` y la carpeta `/ (root)`.
3. Haz clic en **Save**. En un minuto estará disponible en `https://dreamwield.github.io/Irregular-Verbs/`.

---

## 🛠️ Generadores y Código Fuente

- `parse_verbs.py`: Extractor y clasificador de los 154 verbos del PDF a `verbs_data.json`.
- `music_engine.py`: Motor de síntesis de audio musical estéreo en Python (baterías, bajo sub-bass, acordes de piano Rhodes y arpegios melódicos).
- `generate_song_rhymes.py`: Compilador y masterizador de la canción de rimas con timecodes karaoke.
- `generate_song_atoz.py`: Compilador del tema de estudio A-Z.
- `generate_song_quiz.py`: Compilador de la pista de desafío interactivo.
