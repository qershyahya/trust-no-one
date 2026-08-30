"""Trust No One -- the lesson server.

    py main.py        (Windows)
    python3 main.py   (macOS and Linux)

Starts one process that does three things:
  1. runs the real game with real pygame, headless (no window opens),
  2. streams its frames to a web page and sends your keys back to it,
  3. serves that page and opens your browser at it.

What plays on the page is steps/stepNN.py running in CPython right here -- the
same file the page prints. Switching step swaps which file runs.

Keys: arrows/WASD move, Space jumps, click throws a pebble, space restarts a finished run.
Stop it with Ctrl+C.
"""
import ast
import difflib
import http.server
import importlib
import io
import json
import keyword
import os
import socketserver
import sys
import threading
import time
import tokenize
import urllib.parse
import webbrowser
from io import StringIO

from build_steps import TITLES, LAST
from lesson_text import STEP_TEXT, NOTES, SYMBOLS, PARAMS, TEXT_BY_STEP, LOCALS

WINDOWS = sys.platform.startswith("win")
PY = "py" if WINDOWS else "python3"          # what a student types to run Python here
SEP = "\\" if WINDOWS else "/"

PYGAME_PARTS = {"draw", "display", "event", "key", "font", "time", "image", "mouse"}

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS_DIR = os.path.join(HERE, "steps")
PORT = int(os.environ.get("LESSON_PORT", "8756"))
BUILD = str(time.time())   # changes when the server restarts, so an open page can refresh itself

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")   # render into memory, never onto a window
# the audio driver is deliberately NOT forced to dummy: from step 46 the game makes sound,
# and the lesson should let you hear it. A machine with no sound card still works -- the
# step files catch that and play on in silence.
sys.path.insert(0, STEPS_DIR)

try:
    import pygame                                   # noqa: E402
except ImportError:
    sys.exit("This needs pygame. In this same window, type:\n"
             "    py -m pip install pygame        (Windows)\n"
             "    python3 -m pip install pygame   (macOS and Linux)\n"
             "  then start the lesson again.")


# ---------------------------------------------------------------- the game side

class Keys:
    """Stands in for pygame.key.get_pressed(). SDL fills that from a real keyboard
    on a real window, and we have neither -- so the browser fills it instead."""

    def __init__(self):
        self.down = set()

    def __getitem__(self, code):
        return code in self.down


class Runner:
    """Runs one step file at a time and keeps the newest frame as a JPEG."""

    MAX_FAILS = 3

    def __init__(self):
        self.keys = Keys()
        self.lock = threading.Condition()
        self.jpeg = b""
        self.count = 0
        self.step = 1
        self.want = 1
        self.error = ""
        self.fails = 0
        self.watchers = 0
        self.buf = io.BytesIO()
        self.running = False

    # -- frames -----------------------------------------------------------
    def capture(self):
        if self.watchers == 0:                      # nobody is looking; do not encode
            with self.lock:
                self.count += 1
                self.lock.notify_all()
            return
        surf = pygame.display.get_surface()
        if surf is None:
            return
        self.buf.seek(0); self.buf.truncate(0)
        pygame.image.save(surf, self.buf, "frame.jpg")
        data = self.buf.getvalue()
        with self.lock:
            self.jpeg = data
            self.count += 1
            self.lock.notify_all()

    def wait_frame(self, seen, timeout=1.0):
        """Returns the newest frame. On timeout it hands back the same one again, so
        the stream keeps writing -- that is how a closed browser connection gets
        noticed instead of being held open forever."""
        with self.lock:
            if self.count == seen:
                self.lock.wait(timeout)
            return self.jpeg, self.count

    # -- input ------------------------------------------------------------
    def key_down(self, code):
        self.keys.down.add(code)
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=code, mod=0, unicode=""))

    def key_up(self, code):
        self.keys.down.discard(code)
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=code, mod=0))

    def click(self, x, y):
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(int(x), int(y)), button=1))

    def set_held(self, codes):
        """The page says exactly which keys are down; believe it. This is how a key
        held through a page reload gets un-stuck."""
        codes = {int(c) for c in codes}
        for gone in self.keys.down - codes:
            self.key_up(gone)
        for new in codes - self.keys.down:
            self.key_down(new)

    # -- which file is playing --------------------------------------------
    def select(self, n, force=False):
        self.want = max(1, min(LAST, int(n)))
        if force or self.want != self.step:
            self.fails = 0
            self.keys.down.clear()
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def loop(self):
        self.running = True
        while self.running:
            if self.fails >= self.MAX_FAILS:        # stop hammering a broken file
                time.sleep(0.4)
                if self.want == self.step:
                    continue
                self.fails = 0
            self.step = self.want
            name = "step%02d" % self.step
            try:
                mod = importlib.import_module(name)
                mod = importlib.reload(mod)         # a fresh game every time
                if pygame.mixer.get_init():
                    pygame.mixer.stop()             # the last step's music does not carry over
                stage(mod, self.step)               # and put it where the step can be seen
                pygame.event.clear()
                self.error = ""
                self.fails = 0
                mod.main()
            except Exception as exc:                # keep the server up and say what broke
                self.fails += 1
                self.error = "%s in %s.py: %s" % (type(exc).__name__, name, exc)
                import traceback
                traceback.print_exc()
                time.sleep(0.4)
            if self.want == self.step and self.fails == 0:
                time.sleep(0.05)                    # main() returned by itself; start it again

    def start(self):
        pygame.init()                               # once, here: the event queue needs it
        pygame.display.set_mode((960, 640))         # into memory -- SDL_VIDEODRIVER is dummy
        pygame.display.flip = _flip_and_capture     # every rendered frame lands in the stream
        pygame.key.get_pressed = lambda: self.keys
        threading.Thread(target=self.loop, daemon=True).start()


# Where to put the running game so a step can actually be seen. The file on the left is
# never touched -- this only walks the game to the spot you would have walked it to.
#   level: which of the five to load   at: (column, row)   cursed: after the wizard
STAGE = {
    20: dict(at=(36, 17),
             note="two squares from the first coin, on the far side of the pit -- otherwise"
                  " it is a thirty-seven column run and a jump to reach one."),
    21: dict(at=(31, 17),
             note="three squares from the only spike in the level, which is otherwise a long"
                  " way past the pit."),
    27: dict(at=(13, 17),
             note="beside the coin that kills, with the wizard two squares to your right --"
                  " take the curse first, then find out what that coin was."),
    28: dict(at=(27, 17),
             note="three squares from the floor that is never drawn. Walk right onto nothing."),
    29: dict(at=(38, 17),
             note="two squares from the crumbling bricks, which are otherwise thirty-nine"
                  " columns and a pit away."),
    30: dict(at=(44, 17),
             note="between the exit that lies and the one that does not -- both on screen at"
                  " once from here."),
    32: dict(at=(13, 17), cursed=True,
             note="cursed, beside the rolled bricks. Throw stones at them, press R, and throw"
                  " again: the roll changes, but one of them is always solid."),
    33: dict(level=0, at=(54, 17),
             note="three squares from the way out of level I, so you can see what reaching it"
                  " now does."),
    35: dict(level=4, at=(5, 17), cursed=True,
             note="on the windiest level, cursed -- which is the only way the wind is anything"
                  " but zero. Stand still and you still move."),
    37: dict(level=3, at=(12, 13), cursed=True,
             note="in the air above a coin that kills, on level IV. You die on the way down,"
                  " and the body keeps falling to the floor."),
    38: dict(level=0, at=(39, 17),
             note="with a coin one square away and a spike a few to the left, so a jump, a"
                  " coin, a thrown stone and a death are all within a few seconds."),
    44: dict(level=1, at=(26, 17), cursed=True,
             note="on level II with nine solid squares under you, so you can walk and watch"
                  " the two background layers move at different speeds."),
    45: dict(level=4, at=(28, 17),
             note="one throw from here reveals a fire and a hole in the same handful of"
                  " squares, with rubble to your left and a stone ledge to your right."
                  " (Not cursed, so the wind cannot walk you into the gap while you look.)"),
    46: dict(level=4, at=(44, 17),
             note="on level V, two squares from the exit that lies. Throw a stone at it and"
                  " watch which door it really is. (Not cursed here, so the wind cannot walk"
                  " you into it while you read.)"),
    50: dict(level=0, at=(31, 17), cursed=True,
             note="a few squares from the spike on level I. Walk into it and watch her go"
                  " down where she lands."),
    56: dict(level=1, at=(58, 17), cursed=True,
             note="cursed, on level II with a coin directly overhead: one press of space clears"
                  " the title card (there is no wizard on this level, so the story has nowhere"
                  " to go), then space is a jump sound and a coin sound, a click is a stone,"
                  " and the pit four squares right is the last one."),
    52: dict(level=0, at=(9, 17),
             note="in front of the wizard, before the story exists. He is only breathing"
                  " -- nothing has triggered his other two animations yet."),
}


def stage(mod, n):
    """Nudge the running game to where this step's change can be seen. Wraps whatever the
    step uses to set itself up, so it happens after the game is ready and again on restart.
    reset() only exists from step 22 on; before that a step sets itself up in load()."""
    spot = STAGE.get(n)
    if not spot:
        return
    name = "reset" if hasattr(mod, "reset") else "load"
    real = getattr(mod, name, None)
    if real is None:
        return
    # load() only takes a level number from step 33 on, when there is more than one level
    pick_level = "level" in spot and name == "reset" and mod.load.__code__.co_argcount > 0

    def staged(*args, **kw):
        real(*args, **kw)
        if pick_level:
            mod.load(spot["level"])
        if spot.get("cursed") and hasattr(mod, "cursed"):
            mod.cursed, mod.wizard = True, False
        if "lives" in spot and hasattr(mod, "lives"):
            mod.lives = spot["lives"]
        c, r = spot["at"]
        mod.P.update(x=float(c * mod.TILE), y=float(r * mod.TILE), vx=0.0, vy=0.0)

    setattr(mod, name, staged)


RUN = Runner()
_flip_original = pygame.display.flip


def _flip_and_capture():
    RUN.capture()
    _flip_original()


# ---------------------------------------------------------------- the code side

def read_step(n):
    with open(os.path.join(STEPS_DIR, "step%02d.py" % n), encoding="utf-8") as f:
        return f.read().splitlines()


def functions(lines):
    """name -> source text, for every top-level def, so a step can say which
    functions it rewrites rather than adds."""
    try:
        tree = ast.parse("\n".join(lines))
    except SyntaxError:
        return {}
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out[node.name] = "\n".join(lines[node.lineno - 1:node.end_lineno])
    return out


def controls(src):
    """What this step's file can actually respond to, so the page never promises a
    key that does nothing yet."""
    return {"move": "K_LEFT" in src, "jump": "K_SPACE" in src,
            "restart": "K_r" in src, "click": "MOUSEBUTTONDOWN" in src}


def doc_end(lines):
    """Where the module docstring stops. It names the step, so it always differs
    between files and is never news."""
    if not lines or not lines[0].lstrip().startswith('"""'):
        return -1
    if lines[0].rstrip().endswith('"""') and len(lines[0].strip()) > 3:
        return 0
    for i in range(1, min(len(lines), 12)):
        if lines[i].rstrip().endswith('"""'):
            return i
    return -1


def scopes(lines):
    """line number -> (function it is inside, that function's parameters)."""
    out = {}
    try:
        tree = ast.parse("\n".join(lines))
    except SyntaxError:
        return out
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            params = [a.arg for a in node.args.args]
            for row in range(node.lineno - 1, node.end_lineno):
                out[row] = (node.name, params)
    return out


def file_spans(lines):
    """Line number -> the coloured pieces of that line, from Python's own tokenizer:
    keywords, strings, numbers, comments, and the names you can hover. A # inside a
    string stays a #, and a docstring is coloured on every line it covers."""
    out = {}
    src = StringIO("\n".join(lines) + "\n")

    def mark(row, a, b, kind, sym=None):
        span = {"a": a, "b": b, "t": kind}
        if sym:
            span["sym"] = sym
        out.setdefault(row, []).append(span)

    prev = None
    where = scopes(lines)
    try:
        for tok in tokenize.generate_tokens(src.readline):
            before = prev                       # the token to our left, whatever we do next
            if tok.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                                tokenize.DEDENT, tokenize.COMMENT):
                prev = tok
            kind, sym = None, None
            if tok.type == tokenize.COMMENT:
                kind = "com"
            elif tok.type == tokenize.STRING:
                kind = "str"
            elif tok.type == tokenize.NUMBER:
                kind = "num"
            elif tok.type == tokenize.NAME:
                after_dot = before is not None and before.type == tokenize.OP and before.string == "."
                entry = SYMBOLS.get(tok.string)
                if keyword.iskeyword(tok.string) or tok.string in ("self", "match", "case"):
                    kind = "kw"
                elif after_dot and tok.string in PYGAME_PARTS:
                    kind = "lib"                # pygame.draw is not the game's own draw()
                elif entry and after_dot and "." not in (entry.get("sig") or ""):
                    kind = "var"                # an attribute that happens to share a name
                elif entry and not after_dot and "." in (entry.get("sig") or ""):
                    kind = "var"                # rect() is pygame.draw.rect; a bare rect is not
                elif entry:
                    sym = tok.string
                    kind = {"func": "fn", "const": "con", "lib": "lib"}.get(entry.get("kind"), "var")
                elif tok.string.isupper() and len(tok.string) > 1:
                    kind = "con"                # a constant we have no note for
            if tok.type == tokenize.NAME and kind in (None, "var"):
                fn, params = where.get(tok.start[0] - 1, (None, ()))
                if fn and tok.string in params and tok.string in (PARAMS.get(fn) or {}):
                    kind, sym = "var", "%s.%s" % (fn, tok.string)
                elif fn and (fn, tok.string) in LOCALS:
                    kind, sym = "var", "%s.%s" % (fn, tok.string)
            if not kind:
                continue
            first, last = tok.start[0], tok.end[0]
            if first == last:
                mark(first - 1, tok.start[1], tok.end[1], kind, sym)
            else:                               # a docstring or other multi-line string
                for row in range(first, last + 1):
                    text = lines[row - 1] if row - 1 < len(lines) else ""
                    a = tok.start[1] if row == first else 0
                    b = tok.end[1] if row == last else len(text)
                    if b > a:
                        mark(row - 1, a, b, kind)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass                                    # unfinished file: no colour, no crash
    return out


_ORIGINS = {}


def code_only(lines, spans):
    """(file line number, the code on it) for every line that has any code, with
    trailing comments cut off. Comment-only and blank lines are left out, so a
    comment moving from above a line to the end of it is not a change."""
    out, head = [], doc_end(lines)
    for i, line in enumerate(lines):
        if i <= head:                           # the docstring names the step; never news
            continue
        cut = min([sp["a"] for sp in spans.get(i, []) if sp["t"] == "com"], default=None)
        code = (line[:cut] if cut is not None else line).rstrip()
        if code.strip():
            out.append((i, code))
    return out


def origins(n):
    """For every line of step n, the step its code first appeared at."""
    if n in _ORIGINS:
        return _ORIGINS[n]
    lines = read_step(n)
    code = code_only(lines, file_spans(lines))
    if n == 1:
        out = {i: 1 for i, _ in code}
    else:
        before = read_step(n - 1)
        was_code = code_only(before, file_spans(before))
        was = origins(n - 1)
        out = {i: n for i, _ in code}
        sm = difflib.SequenceMatcher(None, [c for _, c in was_code],
                                     [c for _, c in code], autojunk=False)
        for tag, i1, _i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                for k in range(j2 - j1):
                    out[code[j1 + k][0]] = was.get(was_code[i1 + k][0], n)
    _ORIGINS[n] = out
    return out


def local_symbols(n, lines):
    """The hint for a function, as that function exists at this step: the real
    signature from the file, only the arguments it actually has, and what it does
    at this point in the lesson."""
    out = {}
    try:
        tree = ast.parse("\n".join(lines))
    except SyntaxError:
        return out
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        params = [a.arg for a in node.args.args]
        entry = dict(SYMBOLS.get(node.name, {}))
        entry["kind"] = "func"
        entry["sig"] = "%s(%s)" % (node.name, ", ".join(params))
        described = PARAMS.get(node.name)
        if described:
            takes = [described[p] and "%s: %s" % (p, described[p]) for p in params if p in described]
            entry["takes"] = ". ".join(t for t in takes if t) or "nothing"
        elif not params:
            entry["takes"] = "nothing"
        for p in params:
            if p in (PARAMS.get(node.name) or {}):
                out["%s.%s" % (node.name, p)] = {
                    "kind": "param", "name": p,
                    "expand": "a value handed to %s()" % node.name,
                    "text": PARAMS[node.name][p][0].upper() + PARAMS[node.name][p][1:] + ".",
                }
        for (fname, local), (expand, text) in LOCALS.items():
            if fname == node.name:
                out["%s.%s" % (fname, local)] = {"kind": "var", "name": local,
                                                 "expand": expand, "text": text}
        for since, text in TEXT_BY_STEP.get(node.name, []):
            if since <= n:
                entry["text"] = text
        out[node.name] = entry
    return out


def step_payload(n):
    """The whole step file, diffed against the step before. The diff is taken on
    the code alone, so a comment that has been reworded or moved never shows up as
    a change -- only real work does."""
    now, before = read_step(n), (read_step(n - 1) if n > 1 else [])
    now_spans, old_spans = file_spans(now), file_spans(before)
    now_code, old_code = code_only(now, now_spans), code_only(before, old_spans)
    came = origins(n)

    kind = {}                                   # file line -> add / same
    deleted = {}                                # file line to insert before -> old lines
    rewritten, new_fns = [], []
    if n == 1:
        kind = {i: "add" for i in range(len(now))}
    else:
        sm = difflib.SequenceMatcher(None, [c for _, c in old_code],
                                     [c for _, c in now_code], autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag in ("insert", "replace"):
                for j in range(j1, j2):
                    kind[now_code[j][0]] = "add"
            elif tag == "equal":
                for j in range(j1, j2):
                    kind[now_code[j][0]] = "same"
            if tag in ("delete", "replace"):
                at = now_code[j1][0] if j1 < len(now_code) else len(now)
                deleted.setdefault(at, []).extend(before[old_code[i][0]] for i in range(i1, i2))
        old_fn, new_fn = functions(before), functions(now)
        for fname, text in new_fn.items():
            if fname not in old_fn:
                new_fns.append(fname)
            elif old_fn[fname] != text:
                rewritten.append(fname)

    # a deleted line belongs above the whole replacement, comments included
    def lift(at):
        while at > 0:
            prev = now[at - 1].strip()
            if (at - 1) in kind or not (prev.startswith("#") or prev == ""):
                break
            at -= 1
        return at

    if deleted:
        deleted = {lift(at): rows for at, rows in sorted(deleted.items())}

    # a comment or a blank belongs to the code line under it
    def kind_of(i):
        if i in kind:
            return kind[i]
        for j in range(i + 1, len(now)):
            if j in kind:
                return kind[j]
        return "same"

    rows = []
    for i, text in enumerate(now):
        for gone in deleted.get(i, []):
            rows.append({"kind": "del", "n": "-", "text": gone, "ids": [], "from": None})
        rows.append({"kind": kind_of(i), "n": i + 1, "text": text,
                     "ids": now_spans.get(i, []),
                     "from": came.get(i) or came.get(next((j for j in range(i + 1, len(now))
                                                           if j in came), -1))})
    for gone in deleted.get(len(now), []):
        rows.append({"kind": "del", "n": "-", "text": gone, "ids": [], "from": None})

    meta = dict(STEP_TEXT[n])
    if n in STAGE:                                  # say where the game has been put
        meta["trial"] = meta["trial"] + " <b>You start</b> " + STAGE[n]["note"]
    meta.update(title=TITLES[n - 1], last=LAST, step=n,
                file="steps" + SEP + "step%02d.py" % n,
                folder=HERE, lines=rows, total=len(now), code_lines=len(now_code),
                py=PY, sep=SEP, windows=WINDOWS,
                added=sum(1 for r in rows if r["kind"] == "add"),
                removed=sum(1 for r in rows if r["kind"] == "del"),
                rewritten=sorted(rewritten), new_functions=sorted(new_fns),
                symbols=local_symbols(n, now),
                controls=controls("\n".join(now)))
    return meta


# ---------------------------------------------------------------- the web side

class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass                                        # the terminal belongs to the game

    def _send(self, code, body, ctype="application/json"):
        if isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _local(self):
        """Only this machine's own lesson page may drive the game -- so no other
        site you have open can post keys at it."""
        origin = self.headers.get("Origin")
        if origin and not (origin.startswith("http://127.0.0.1")
                           or origin.startswith("http://localhost")):
            return False
        host = (self.headers.get("Host") or "").split(":")[0]
        return host in ("127.0.0.1", "localhost", "")

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        try:
            if url.path in ("/", "/index.html"):
                with open(os.path.join(HERE, "lesson.html"), "rb") as f:
                    return self._send(200, f.read(), "text/html; charset=utf-8")
            if url.path == "/api/steps":
                return self._send(200, json.dumps([{"n": n, "title": TITLES[n - 1]}
                                                   for n in range(1, LAST + 1)]))
            if url.path == "/api/step":
                q = urllib.parse.parse_qs(url.query)
                try:
                    n = max(1, min(LAST, int(q.get("n", ["1"])[0])))
                except ValueError:
                    return self._send(400, json.dumps({"error": "step must be a number from 1 to %d" % LAST}))
                return self._send(200, json.dumps(step_payload(n)))
            if url.path == "/api/keys":
                names = {"ArrowLeft": "K_LEFT", "ArrowRight": "K_RIGHT", "ArrowUp": "K_UP",
                         "ArrowDown": "K_DOWN", "Space": "K_SPACE", "KeyA": "K_a",
                         "KeyD": "K_d", "KeyW": "K_w", "KeyS": "K_s", "KeyR": "K_r"}
                return self._send(200, json.dumps({k: getattr(pygame, v) for k, v in names.items()}))
            if url.path == "/api/symbols":
                return self._send(200, json.dumps(SYMBOLS))
            if url.path == "/api/state":
                return self._send(200, json.dumps({"step": RUN.step, "error": RUN.error,
                                                   "frames": RUN.count, "build": BUILD,
                                                   "stuck": RUN.fails >= RUN.MAX_FAILS}))
            if url.path == "/stream.mjpg":
                return self.stream()
            return self._send(404, json.dumps({"error": "no such page"}))
        except Exception as exc:
            return self._send(500, json.dumps({"error": "%s: %s" % (type(exc).__name__, exc)}))

    def do_POST(self):
        if not self._local():
            return self._send(403, json.dumps({"error": "only this machine's lesson page may do that"}))
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self._send(400, json.dumps({"error": "bad Content-Length"}))
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
            if not isinstance(data, dict):
                raise ValueError("expected an object")
        except ValueError:
            return self._send(400, json.dumps({"error": "that was not a JSON object"}))
        try:
            if self.path == "/api/input":
                kind = data.get("t")
                if kind == "kd":
                    RUN.key_down(int(data["k"]))
                elif kind == "ku":
                    RUN.key_up(int(data["k"]))
                elif kind == "click":
                    RUN.click(float(data["x"]), float(data["y"]))
                elif kind == "held":
                    RUN.set_held(data.get("keys") or [])
                else:
                    return self._send(400, json.dumps({"error": "unknown input type"}))
                return self._send(200, json.dumps({"ok": True}))
            if self.path == "/api/select":
                RUN.select(data.get("n", 1), force=bool(data.get("restart")))
                return self._send(200, json.dumps({"ok": True, "step": RUN.want}))
            return self._send(404, json.dumps({"error": "no such page"}))
        except (KeyError, TypeError, ValueError) as exc:
            return self._send(400, json.dumps({"error": "bad input: %s" % exc}))

    def stream(self):
        """MJPEG: one JPEG per rendered frame, forever, down a single connection."""
        self.send_response(200)
        self.send_header("Age", "0")
        self.send_header("Cache-Control", "no-cache, private")
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=FRAME")
        self.end_headers()
        RUN.watchers += 1
        seen = 0
        try:
            while True:
                jpeg, seen = RUN.wait_frame(seen)
                if not jpeg:
                    continue
                self.wfile.write(b"--FRAME\r\nContent-Type: image/jpeg\r\nContent-Length: ")
                self.wfile.write(str(len(jpeg)).encode())
                self.wfile.write(b"\r\n\r\n")
                self.wfile.write(jpeg)
                self.wfile.write(b"\r\n")
        except OSError:
            pass                                    # the page went away; that is normal
        finally:
            RUN.watchers -= 1


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    missing = [n for n in range(1, LAST + 1)
               if not os.path.exists(os.path.join(STEPS_DIR, "step%02d.py" % n))]
    if missing:
        print("Missing step files: %s\nRun:  %s build_steps.py" % (missing, PY))
        return 1
    try:
        srv = Server(("127.0.0.1", PORT), Handler)
    except OSError as exc:
        print("Cannot use port %d (%s)." % (PORT, exc.strerror or exc))
        print("A lesson may already be running -- try http://127.0.0.1:%d/ first." % PORT)
        if WINDOWS:
            print("Or pick another port:  set LESSON_PORT=8757 && %s main.py" % PY)
        else:
            print("Or pick another port:  LESSON_PORT=8757 %s main.py" % PY)
        return 1
    RUN.start()
    url = "http://127.0.0.1:%d/" % PORT
    print("Trust No One -- lesson server")
    print("  the real game is running here, in pygame")
    print("  open:  %s" % url)
    print("  stop:  press Ctrl+C in this window")
    threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    RUN.running = False
    return 0


if __name__ == "__main__":
    sys.exit(main())
