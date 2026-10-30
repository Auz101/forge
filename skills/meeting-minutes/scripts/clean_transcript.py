"""Clean a Microsoft Teams transcript into readable plain text (forge meeting-minutes).

Supports .vtt (Teams WebVTT), .docx (Teams/Word download) and .txt/.md.
Standard library only. Usage:

    python clean_transcript.py <input> <output.txt>

Output format: one line per turn, "[HH:MM:SS] Name: text",
merging consecutive turns from the same participant.
At the end it prints stats (participants, duration, words).
"""
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
VTT_TIME = re.compile(r"(\d{1,2}:)?\d{1,2}:\d{2}[.,]\d{3}\s*-->\s*")
VOICE = re.compile(r"<v\s+([^>]+)>(.*?)(?:</v>|$)", re.S)
TAG = re.compile(r"</?[^>]+>")
DOCX_HEADER = re.compile(r"^(.{2,80}?)\s{2,}(\d{1,2}:\d{2}(?::\d{2})?)$")


def read_vtt(path):
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    turns = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n")):
        lines = [l for l in block.strip().split("\n") if l.strip()]
        idx = next((i for i, l in enumerate(lines) if VTT_TIME.match(l)), None)
        if idx is None:
            continue
        start = lines[idx].split("-->")[0].strip().split(".")[0].split(",")[0]
        if start.count(":") == 1:
            start = "00:" + start
        content = " ".join(lines[idx + 1:])
        m = VOICE.search(content)
        speaker, phrase = (m.group(1).strip(), m.group(2)) if m else ("(no name)", content)
        phrase = TAG.sub("", phrase).strip()
        if phrase:
            turns.append((start.zfill(8), speaker, phrase))
    return merge(turns)


def merge(turns):
    lines, current = [], None
    for start, speaker, phrase in turns:
        if current and current[1] == speaker:
            current[2].append(phrase)
        else:
            if current:
                lines.append(f"[{current[0]}] {current[1]}: {' '.join(current[2])}")
            current = [start, speaker, [phrase]]
    if current:
        lines.append(f"[{current[0]}] {current[1]}: {' '.join(current[2])}")
    return lines


def read_docx(path):
    with zipfile.ZipFile(path) as z:
        root = ElementTree.fromstring(z.read("word/document.xml"))
    paragraphs = []
    for p in root.iter(f"{W_NS}p"):
        text = "".join(t.text or "" for t in p.iter(f"{W_NS}t")).strip()
        if text:
            paragraphs.append(text)
    # Teams format: "Name   0:03" followed by the turn's text
    turns, current = [], None
    for text in paragraphs:
        m = DOCX_HEADER.match(text)
        if m:
            current = [normalize_time(m.group(2)), m.group(1).strip(), []]
            turns.append(current)
        elif current:
            current[2].append(text)
    if not turns:
        return paragraphs
    return merge([(t, s, " ".join(f)) for t, s, f in turns if f])


def normalize_time(time):
    parts = time.split(":")
    while len(parts) < 3:
        parts.insert(0, "0")
    return ":".join(p.zfill(2) for p in parts)


def stats(lines):
    speakers = {}
    for l in lines:
        m = re.match(r"\[(\d{2}:\d{2}:\d{2})\] ([^:]+):", l)
        if m:
            speakers[m.group(2)] = speakers.get(m.group(2), 0) + 1
    times = re.findall(r"^\[(\d{2}:\d{2}:\d{2})\]", "\n".join(lines), re.M)
    words = sum(len(l.split()) for l in lines)
    print(f"Lines: {len(lines)} | Words: {words}")
    if times:
        print(f"Approximate duration: {times[-1]}")
    if speakers:
        print("Participants (turns):")
        for name, n in sorted(speakers.items(), key=lambda x: -x[1]):
            print(f"  - {name}: {n}")
    else:
        print("No participant marks detected; check the format manually.")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    source, target = Path(sys.argv[1]), Path(sys.argv[2])
    ext = source.suffix.lower()
    if ext == ".vtt":
        lines = read_vtt(source)
    elif ext == ".docx":
        lines = read_docx(source)
    elif ext in (".txt", ".md"):
        lines = [l.rstrip() for l in source.read_text(encoding="utf-8-sig", errors="replace").splitlines() if l.strip()]
    else:
        print(f"Unsupported format: {ext}. Use .vtt, .docx, .txt or .md")
        sys.exit(2)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Clean transcript: {target}")
    stats(lines)


if __name__ == "__main__":
    main()
