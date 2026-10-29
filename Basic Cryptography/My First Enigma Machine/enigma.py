"""
My First Enigma Machine -- a 3-rotor substitution machine.

    "Characters are inputted (A=0, B=1, ...). When a character is inputted,
     Rotor 1 advances first (MACHINE... -> ACHINE...M). The character is passed
     through the rotor by its index: Z=25 -> rotor1[25]=M. This happens again
     for Rotor 2 and Rotor 3. Rotor 2 only rotates when Rotor 1 has made a full
     rotation, and Rotor 3 only when Rotor 2 has. Rotors start at 0,0,0."
     Message: HKV{BSBU-B-SJYZNNB-DNFW-IXH-YTA-RPL-RTXOLWFQ}

How the machine works (encryption)
----------------------------------
Three fixed rotor alphabets:
    R1 = MACHINEBDFGJKLOPQRSTUVWXYZ
    R2 = ORBITACDEFGHJKLMNPQSUVWXYZ
    R3 = CIPHERABDFGJKLMNOQSTUVWXYZ

Each rotor is a substitution table: feed in a letter's index 0..25 and read out
the letter sitting at that position in the rotor's (rotated) alphabet. The three
rotors are applied in series 1 -> 2 -> 3, and the result is the cipher letter.

The rotors step like an odometer, BEFORE each letter is encoded:
  * Rotor 1 advances by one every letter (its alphabet rotates left by one, so
    after position p it reads R1[p:] + R1[:p]).
  * Rotor 2 advances one step only after Rotor 1 completes a full 26-letter
    turn; Rotor 3 only after Rotor 2 completes one. So positions behave like a
    base-26 counter (p0, p1, p2).
  * Non-letters ({ } -) are passed straight through and do NOT step the rotors.

Encrypting one letter c (with current positions p):
    x  = index(c)
    x  = index( R1_rotated[x] )
    x  = index( R2_rotated[x] )
    x  = index( R3_rotated[x] )
    cipher = alphabet[x]

How we break it
---------------
There is no secret key here -- the rotor wirings and the start position (0,0,0)
are all given -- so this is just a known machine run backwards. Each rotor is a
bijection, so it is invertible: to decrypt we reproduce the exact same stepping
schedule and, per letter, undo the rotors in reverse order (3, then 2, then 1)
using `rotor.index(letter)` instead of `rotor[index]`.

    Flag: CNS{JOHN-F-KENNEDY-SAID-ICH-BIN-EIN-BERLINER}
          ("Ich bin ein Berliner" -- JFK's 1963 Berlin speech, from the German bakers)

Lesson: a rotor machine is a poly-alphabetic substitution whose security lives
entirely in the secret wiring and start positions. Publish those (as here) and
it is a plain, reversible encoding -- no secret, no security.
"""

ROTORS = [
    "MACHINEBDFGJKLOPQRSTUVWXYZ",  # Rotor 1
    "ORBITACDEFGHJKLMNPQSUVWXYZ",  # Rotor 2
    "CIPHERABDFGJKLMNOQSTUVWXYZ",  # Rotor 3
]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CIPHERTEXT = "HKV{BSBU-B-SJYZNNB-DNFW-IXH-YTA-RPL-RTXOLWFQ}"


def run(msg, decrypt):
    pos = [0, 0, 0]  # rotor positions, start at 0,0,0
    out = ""
    for ch in msg:
        if ch not in ALPHABET:  # { } - pass through; rotors don't move
            out += ch
            continue

        # Step the rotors (odometer) BEFORE encoding this letter.
        pos[0] += 1
        if pos[0] == 26:
            pos[0] = 0
            pos[1] += 1
        if pos[1] == 26:
            pos[1] = 0
            pos[2] += 1

        # Each rotor's alphabet rotated left by its current position.
        rotated = [r[k:] + r[:k] for r, k in zip(ROTORS, pos)]

        x = ALPHABET.index(ch)
        if decrypt:  # undo rotors in reverse order: 3, 2, 1
            for r in reversed(rotated):
                x = r.index(ALPHABET[x])
        else:        # forward: rotor 1, 2, 3
            for r in rotated:
                x = ALPHABET.index(r[x])
        out += ALPHABET[x]
    return out


def solve():
    flag = run(CIPHERTEXT, decrypt=True)
    print(flag)
    # Sanity check: re-encrypting the recovered plaintext reproduces the message.
    print("round-trip OK:", run(flag, decrypt=False) == CIPHERTEXT)
    return flag


if __name__ == "__main__":
    solve()
