"""pussy — a flipbook of kaomoji cats is the program; one live cat is the state.

Opcode = eyes.  Operand counter = mouth.  JMP target = paw prints on the frame.
  (ﾟ ﾟ)  INC x            ｡  tail      (～ wags inside )～ノ)
  (ー ﾟ)  DEC x, skip next frame if x == 0
  (ﾟ ー)  JMP n            ω  tracks    (🐾 trailing behind)
  (ー ー)  HALT (asleep)    ､  whiskers  (~ on the cheek line)
"""
import re, sys

TEMPLATE = " ／l、\n（{le}､ {m} ７\n l、ﾞ {w}ヽ\n じし{t})ノ\n"

def render(tail, tracks, whisk, le="ﾟ", re_="ﾟ", m="｡"):
    # tail wags inside )～ノ ; tracks trail off behind ; whiskers on the cheek
    return (" ／l、\n"
            f"（{le}､ {m} {re_}７\n"
            f" l、ﾞ {'~'*max(whisk,1)}ヽ\n"
            f" じし_,){'～'*tail}ノ{' ...'+'🐾'*tracks if tracks else ''}\n")

EYE = {("ﾟ","ﾟ"):"INC", ("ー","ﾟ"):"DEC", ("ﾟ","ー"):"JMP", ("ー","ー"):"HALT"}
MOUTH = {"｡":"tail", "ω":"tracks", "､":"whisk"}

def frame(op, ctr="tail", target=0):
    le, re_ = [k for k,v in EYE.items() if v==op][0]
    m = [k for k,v in MOUTH.items() if v==ctr][0]
    return render(0, target, 1, le, re_, m)

def parse(frm):
    face = re.search(r"（(.)､ (.) (.)７", frm)
    le, m, re_ = face.groups()
    op = EYE[(le, re_)]
    ctr = MOUTH[m]
    paws = frm.count("🐾")
    return op, ctr, paws

def run(program, steps=400, state=None):
    st = state or {"tail":1, "tracks":1, "whisk":0}
    frames = [p for p in program.split("\n\n") if p.strip()]
    pc, trace = 0, []
    for _ in range(steps):
        if pc >= len(frames): break
        op, ctr, n = parse(frames[pc])
        trace.append((pc, op, ctr, n, dict(st)))
        if op == "HALT": break
        if op == "INC": st[ctr] += 1; pc += 1
        elif op == "DEC":
            if st[ctr] > 0: st[ctr] -= 1; pc += 1
            else: pc += 2
        elif op == "JMP": pc = n
    return st, trace

# Fibonacci: (tail, tracks) alternate holding the next number.
#   loop A: tail -> tracks & whisk ; whisk -> tail      (tracks = a+b, tail = a)
#   loop B: tracks -> tail & whisk ; whisk -> tracks      (tail = a+b, tracks = a)
FIB = "\n\n".join([
    frame("DEC","tail"),  frame("JMP",target=3),  frame("JMP",target=6),   # 0-2
    frame("INC","tracks"),  frame("INC","whisk"),   frame("JMP",target=0),   # 3-5
    frame("DEC","whisk"), frame("JMP",target=9),  frame("JMP",target=11),  # 6-8
    frame("INC","tail"),  frame("JMP",target=6),                           # 9-10
    frame("DEC","tracks"),  frame("JMP",target=14), frame("JMP",target=17),  # 11-13
    frame("INC","tail"),  frame("INC","whisk"),   frame("JMP",target=11),  # 14-16
    frame("DEC","whisk"), frame("JMP",target=20), frame("JMP",target=0),   # 17-19
    frame("INC","tracks"),  frame("JMP",target=17),                          # 20-21
])

if __name__ == "__main__":
    st, trace = run(FIB, steps=int(sys.argv[1]) if len(sys.argv)>1 else 300)
    fibs = []
    for pc, op, ctr, n, s in trace:
        if pc in (0, 11) and s["whisk"] == 0:
            fibs.append(max(s["tail"], s["tracks"]))
            print(render(s["tail"], s["tracks"], s["whisk"]))
    print("fib seen:", sorted(set(fibs)))
