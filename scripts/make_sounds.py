#!/usr/bin/env python3
"""Generate wake.wav (wake-word confirmation) and alarm.wav (timer alarm).

Pure stdlib (wave + math), no dependencies. Output: 16-bit PCM, mono, 16 kHz.
Run:  python make_sounds.py
"""
import math
import struct
import wave
import os

RATE = 16000
SOUNDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "sounds")
os.makedirs(SOUNDS, exist_ok=True)


def _tone(freq, dur, vol=0.6, rate=RATE):
    """One sine tone with short fade in/out to avoid clicks."""
    n = int(rate * dur)
    fade = max(1, int(rate * 0.005))  # 5 ms fade
    out = []
    for i in range(n):
        env = 1.0
        if i < fade:
            env = i / fade
        elif i > n - fade:
            env = (n - i) / fade
        out.append(vol * env * math.sin(2 * math.pi * freq * i / rate))
    return out


def _silence(dur, rate=RATE):
    return [0.0] * int(rate * dur)


def _write(path, samples, rate=RATE):
    with wave.open(path, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        frames = b"".join(
            struct.pack("<h", max(-32767, min(32767, int(s * 32767)))) for s in samples
        )
        w.writeframes(frames)
    print(f"wrote {path}  ({len(samples) / rate:.2f}s)")


# wake.wav - friendly rising two-tone chime (~0.22s)
wake = _tone(880, 0.09) + _tone(1320, 0.12)
_write(os.path.join(SOUNDS, "wake.wav"), wake)

# alarm.wav - urgent alternating beeps, 3 bursts (~2.0s)
alarm = []
for _ in range(3):
    alarm += _tone(1000, 0.18, vol=0.8)
    alarm += _silence(0.07)
    alarm += _tone(1400, 0.18, vol=0.8)
    alarm += _silence(0.20)
_write(os.path.join(SOUNDS, "alarm.wav"), alarm)
