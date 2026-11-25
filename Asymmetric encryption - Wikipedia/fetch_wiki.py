"""Download Wikipedia articles as Markdown (math kept as LaTeX) into a folder.

usage: python3 -I fetch_wiki.py <out_dir>
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

OUT = sys.argv[1]
UA = "ctf-notes-fetcher/1.0 (personal study notes)"

TOPICS = {
    "01 Fundamentals": [
        "Public-key cryptography",
        "Trapdoor function",
        "Key size",
        "Malleability (cryptography)",
        "Semantic security",
    ],
    "02 RSA": [
        "RSA cryptosystem",
        "Optimal asymmetric encryption padding",
        "Rabin cryptosystem",
        "Coppersmith method",
        "Wiener's attack",
        "Blind signature",
    ],
    "03 Discrete log systems": [
        "ElGamal encryption",
        "ElGamal signature scheme",
        "Diffie–Hellman key exchange",
        "Discrete logarithm",
        "Schnorr signature",
        "Digital Signature Algorithm",
        "Paillier cryptosystem",
        "Safe and Sophie Germain primes",
        "Primitive root modulo n",
    ],
    "04 Elliptic curves": [
        "Elliptic-curve cryptography",
        "Elliptic Curve Digital Signature Algorithm",
        "Elliptic-curve Diffie–Hellman",
    ],
    "05 Digital signatures": [
        "Digital signature",
        "Hash-based cryptography",
    ],
    "06 Number theory": [
        "Euler's totient function",
        "Fermat's little theorem",
        "Euler's theorem",
        "Extended Euclidean algorithm",
        "Modular multiplicative inverse",
        "Modular exponentiation",
        "Chinese remainder theorem",
        "Quadratic residue",
        "Tonelli–Shanks algorithm",
        "Carmichael function",
    ],
    "07 Attacks - factoring": [
        "Integer factorization",
        "Fermat's factorization method",
        "Pollard's p − 1 algorithm",
        "Pollard's rho algorithm",
        "Lenstra elliptic-curve factorization",
        "Quadratic sieve",
    ],
    "08 Attacks - discrete log": [
        "Baby-step giant-step",
        "Pohlig–Hellman algorithm",
        "Pollard's rho algorithm for logarithms",
        "Index calculus algorithm",
        "Small subgroup confinement attack",
    ],
    "09 Attacks - lattices": [
        "Lenstra–Lenstra–Lovász lattice basis reduction algorithm",
    ],
}

DROP_SECTIONS = {"references", "notes", "further reading", "external links", "sources",
                 "citations", "bibliography", "footnotes", "notes and references"}
SKIP_CLASSES = {"mw-ref", "reference", "navbox", "mw-editsection", "mw-cite-backlink",
                "metadata", "ambox", "noprint", "mw-references-wrap", "reflist",
                "hatnote", "shortdescription", "sistersitebox", "side-box", "navbox-styles"}
SKIP_TAGS = {"style", "script", "figure", "noscript", "title"}
VOID = {"br", "img", "link", "meta", "hr", "wbr", "input", "source", "col"}


class ToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0          # >0 while inside a skipped subtree
        self.stack = []        # (tag, skipping?) for non-void tags
        self.lists = []        # 'ul' / 'ol' counters
        self.pre = 0

    def w(self, s):
        if not self.skip:
            self.out.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in VOID:
            if tag == "br":
                self.w("\n")
            return
        classes = set((a.get("class") or "").split())
        skipping = (tag in SKIP_TAGS or bool(classes & SKIP_CLASSES)
                    or (tag == "table" and "infobox" not in classes and "wikitable" not in classes)
                    and "box" in " ".join(classes))
        if tag == "math" and not self.skip:
            tex = ""
            try:
                tex = json.loads(a.get("data-mw", "{}"))["body"]["extsrc"].strip()
            except Exception:  # noqa: BLE001
                pass
            tex = re.sub(r"\s+", " ", tex)
            if "block" in classes or (a.get("display") == "block"):
                self.out.append(f"\n\n$$ {tex} $$\n\n")
            else:
                self.out.append(f"${tex}$")
            skipping = True
        self.stack.append((tag, skipping))
        if skipping:
            self.skip += 1
            return
        if tag in ("h2", "h3", "h4", "h5"):
            self.w("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "p":
            self.w("\n\n")
        elif tag in ("ul", "ol"):
            self.lists.append(0 if tag == "ol" else None)
            self.w("\n")
        elif tag == "li":
            depth = max(len(self.lists) - 1, 0)
            if self.lists and self.lists[-1] is not None:
                self.lists[-1] += 1
                bullet = f"{self.lists[-1]}."
            else:
                bullet = "-"
            self.w("\n" + "  " * depth + bullet + " ")
        elif tag == "dd":
            self.w("\n    ")
        elif tag == "dt":
            self.w("\n**")
        elif tag == "pre":
            self.pre += 1
            self.w("\n\n```\n")
        elif tag == "sup":
            self.w("^(")
        elif tag == "sub":
            self.w("_(")
        elif tag in ("b", "strong"):
            self.w("**")
        elif tag in ("i", "em"):
            self.w("*")
        elif tag == "code" and not self.pre:
            self.w("`")
        elif tag == "tr":
            self.w("\n| ")
        elif tag in ("td", "th"):
            pass
        elif tag == "table":
            self.w("\n\n")

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        # pop to the matching tag (HTML may be slightly unbalanced)
        while self.stack:
            t, skipping = self.stack.pop()
            if skipping:
                self.skip -= 1
            elif not self.skip:
                self._close(t)
            if t == tag:
                break

    def _close(self, tag):
        if tag in ("h2", "h3", "h4", "h5"):
            self.w("\n")
        elif tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
            self.w("\n")
        elif tag == "dt":
            self.w("**")
        elif tag == "pre":
            self.pre -= 1
            self.w("\n```\n")
        elif tag in ("sup", "sub"):
            self.w(")")
        elif tag in ("b", "strong"):
            self.w("**")
        elif tag in ("i", "em"):
            self.w("*")
        elif tag == "code" and not self.pre:
            self.w("`")
        elif tag in ("td", "th"):
            self.w(" | ")
        elif tag == "table":
            self.w("\n\n")

    def handle_data(self, data):
        if self.skip:
            return
        if not self.pre:
            data = re.sub(r"[ \t\r\n]+", " ", data)
        self.out.append(data)


def tidy(md):
    md = md.replace("⁠", "")
    md = re.sub(r"\^\((\w)\)", r"^\1", md)          # ^(2) -> ^2
    md = re.sub(r"_\((\w)\)", r"_\1", md)
    md = re.sub(r"\*\*\s*\*\*", "", md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n[ \t]+(?=[^ \t\-\d$])", "\n", md)  # strip stray leading spaces on prose
    md = re.sub(r"\n{3,}", "\n\n", md)
    # drop reference-ish trailing sections
    parts = re.split(r"(?m)^(?=## )", md)
    keep = [p for p in parts
            if not (p.startswith("## ") and p[3:].splitlines()[0].strip().lower() in DROP_SECTIONS)]
    return "".join(keep).strip() + "\n"


def get(url):
    for attempt in range(8):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8"), r.geturl()
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = int(e.headers.get("Retry-After") or 0) or min(5 * 2 ** attempt, 120)
                print(f"   {e.code}, waiting {wait}s", flush=True)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("gave up after retries")


def fetch(title):
    path = urllib.parse.quote(title.replace(" ", "_"), safe="")
    html, final = get(f"https://en.wikipedia.org/api/rest_v1/page/html/{path}?redirect=true")
    m = re.search(r'<link rel="dc:isVersionOf" href="//en.wikipedia.org/wiki/([^"]+)"', html)
    real = urllib.parse.unquote(m.group(1)).replace("_", " ") if m else title
    p = ToMarkdown()
    p.feed(html)
    return real, "https://en.wikipedia.org/wiki/" + urllib.parse.quote(real.replace(" ", "_")), tidy("".join(p.out))


def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "", name)


index = ["# Asymmetric encryption — Wikipedia reference\n\n",
         "Offline Markdown copies of Wikipedia articles for the asymmetric-crypto hacking session. "
         "Formulas are kept as LaTeX (`$...$`); `^(...)` / `_(...)` mean superscript / subscript in prose. "
         "Search everything with `grep -ri <term> .`\n\n",
         f"Downloaded {time.strftime('%Y-%m-%d')}. Content © Wikipedia contributors, CC BY-SA 4.0.\n"]
failed = []
for section, titles in TOPICS.items():
    os.makedirs(os.path.join(OUT, section), exist_ok=True)
    index.append(f"\n## {section}\n\n")
    for t in titles:
        try:
            title, url, body = fetch(t)
        except Exception as e:  # noqa: BLE001
            print("ERR", t, e, flush=True)
            failed.append(t)
            continue
        fn = safe(title) + ".md"
        with open(os.path.join(OUT, section, fn), "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\nSource: <{url}>\n\n{body}")
        index.append(f"- [{title}](<{section}/{fn}>)\n")
        print(f"ok  {len(body):>7}  {section}/{fn}", flush=True)
        time.sleep(1.5)

with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
    f.writelines(index)
print("FAILED:", failed)
