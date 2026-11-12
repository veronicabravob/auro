import re, html, sys
SRC = sys.argv[1]; OUT = sys.argv[2]
md = open(SRC, encoding="utf-8").read()

PUR="#6A48F5"; INK="#1B1533"; YEL="#FFC83D"; LIL="#F7F5FF"; MUT="#5B5375"; LINE="#DDD6FB"; PUR2="#EDE8FF"

def esc(s): return html.escape(s, quote=True)

# ---------------- SVG helpers ----------------
def wrap(text, maxch):
    words = text.split(); lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+1 > maxch and cur:
            lines.append(cur); cur=w
        else:
            cur = (cur+" "+w).strip()
    if cur: lines.append(cur)
    return lines or [""]

def svg_text(x, y, text, size=12, weight=400, fill=INK, anchor="middle", maxch=None, lh=None):
    lines = wrap(text, maxch) if maxch else [text]
    lh = lh or size*1.3
    y0 = y - (len(lines)-1)*lh/2
    out = []
    for i,l in enumerate(lines):
        out.append(f'<text x="{x:.1f}" y="{y0+i*lh:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" dominant-baseline="middle">{esc(l)}</text>')
    return "".join(out)

def box(x,y,w,h,label,sub=None,fill="#fff",stroke=PUR,tc=INK,r=10,size=12.5,weight=700,dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ''
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{d}/>'
    mc = max(8, int(w/(size*0.6)))
    if sub:
        tl = wrap(label, mc); sl = wrap(sub, int(w/5.9))
        th = len(tl)*size*1.2; sh = len(sl)*13; tot = th+3+sh
        top = y+h/2-tot/2
        for k,t in enumerate(tl):
            s += f'<text x="{x+w/2:.1f}" y="{top+size*0.6+k*size*1.2:.1f}" font-size="{size}" font-weight="{weight}" fill="{tc}" text-anchor="middle" dominant-baseline="middle">{esc(t)}</text>'
        for k,t in enumerate(sl):
            s += f'<text x="{x+w/2:.1f}" y="{top+th+3+6.5+k*13:.1f}" font-size="10.5" fill="{MUT if tc==INK else tc}" text-anchor="middle" dominant-baseline="middle">{esc(t)}</text>'
    else:
        s += svg_text(x+w/2, y+h/2, label, size, weight, tc, maxch=mc)
    return s

ARROW_DEFS = f'''<defs>
<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>
<marker id="ahp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{PUR}"/></marker>
</defs>'''

def line(x1,y1,x2,y2,color=INK,dash=False,marker="ah",both=False,w=1.4):
    d = ' stroke-dasharray="5 4"' if dash else ''
    m = f' marker-end="url(#{marker})"' + (f' marker-start="url(#{marker})"' if both else '')
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d}{m}/>'

def label(x,y,text,size=10.5,fill=MUT):
    w = len(text)*size*0.58+12
    return (f'<rect x="{x-w/2}" y="{y-9}" width="{w}" height="18" rx="9" fill="#fff" stroke="{LINE}"/>'
            f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="middle" dominant-baseline="middle">{esc(text)}</text>')

def wrap_svg(inner, w, h, title, minw=760):
    return (f'<figure class="diagram"><div class="scroll"><svg role="img" aria-label="{esc(title)}" viewBox="0 0 {w} {h:.0f}" '
            f'style="min-width:{minw}px" xmlns="http://www.w3.org/2000/svg" font-family="Plus Jakarta Sans, Inter, Segoe UI, system-ui, sans-serif">'
            f'{ARROW_DEFS}{inner}</svg></div><figcaption>{esc(title)}</figcaption></figure>')

# ---------------- Context diagram ----------------
def diagram_contexto():
    W,H=1100,780; s=[]
    s.append(box(30,20,190,54,"Pyme cliente","Laura Gómez, representante legal",fill=YEL,stroke=INK))
    s.append(box(880,20,190,54,"Personas del BFE","Analista · Cumplimiento",fill=YEL,stroke=INK))
    chans=[("Web responsive",250),("App móvil",410),("Correo de facturas",570),("Consola de analista",730)]
    for t,x in chans: s.append(box(x,24,140,46,t,fill="#fff",size=12))
    s.append(line(220,47,248,47)); s.append(line(880,47,872,47))
    s.append(box(250,100,620,42,"API Gateway · identidad OIDC + MFA · firma OTP de mandatos",fill=INK,stroke=INK,tc="#fff",size=12.5))
    for x in (320,480,640,800): s.append(line(x,70,x,98))
    s.append(f'<rect x="30" y="165" width="1040" height="285" rx="18" fill="{LIL}" stroke="{PUR}" stroke-width="2"/>')
    s.append(svg_text(50,186,"Auro · plataforma agéntica",13,800,PUR,anchor="start"))
    s.append(line(560,142,560,198))
    s.append(box(60,200,170,48,"Guardia de entrada","clasificador · Haiku 5.5",fill="#fff"))
    s.append(box(470,200,180,48,"Orquestador A0","Sonnet 5.5 · informa",fill=PUR,stroke=PUR,tc="#fff"))
    s.append(line(232,224,468,224))
    specs=[("A1 Vinculación","KYC/SARLAFT"),("A2 Datos y caja","ingesta y proyección"),("A3 Validación","anomalías y fraude"),("A4 Uso del cupo","y pagos"),("A5 Acompañamiento","acciones y plan"),("A6 Redactor","mensajes"),("A7 Copiloto","de analista")]
    x0=55; sw=134; gap=10
    for i,(t,sub) in enumerate(specs):
        x=x0+i*(sw+gap)
        s.append(box(x,275,sw,50,t,sub,fill="#fff",size=11.5))
        s.append(line(560,248,x+sw/2,273,color=PUR,marker="ahp",w=1))
    s.append(box(55,350,420,44,"Gateway de herramientas","allowlist por agente · esquema estricto · mandato · idempotencia",fill=YEL,stroke=INK))
    s.append(box(490,350,170,44,"Motor de políticas","políticas como código",fill="#fff"))
    s.append(box(675,350,180,44,"Servicio de proyección","determinístico, sin LLM",fill="#fff"))
    s.append(box(870,350,180,44,"Memoria","sesión · cliente estructurada",fill="#fff"))
    s.append(box(490,404,560,32,"Evals, observabilidad (OpenTelemetry) y evaluador en línea",fill=PUR2,stroke=LINE,weight=600,size=11.5))
    s.append(line(477,372,488,372,both=True))
    for i in range(7):
        x=x0+i*(sw+gap)+sw/2
        if x<470: s.append(line(x,325,x,348,w=1,color=MUT))
    s.append(f'<rect x="30" y="480" width="610" height="280" rx="18" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')
    s.append(svg_text(50,500,"Sistemas del BFE",13,800,INK,anchor="start"))
    bfe=[("Motor de decisión de crédito","reglas + modelo de riesgo (comité)",YEL),("Originación","expediente y 7 controles","#fff"),("Núcleo bancario","cupo, cuentas registradas","#fff"),("Pagos","desembolsos y abonos (ejecuta)",YEL),("CRM y cola de casos","handoff con SLA","#fff"),("Registro de consentimientos","por finalidad y fuente","#fff"),("Bitácora inmutable","WORM + hashes encadenados",PUR2),("Repositorio documental","cédula, RUT, EEFF, extractos","#fff")]
    for i,(t,sub,f) in enumerate(bfe):
        c=i%2; r=i//2
        s.append(box(50+c*295,518+r*58,280,48,t,sub,fill=f,stroke=INK if f==YEL else PUR,size=12))
    s.append(f'<rect x="660" y="480" width="410" height="280" rx="18" fill="#fff" stroke="{MUT}" stroke-width="1.6" stroke-dasharray="6 4"/>')
    s.append(svg_text(680,500,"Fuentes externas (solo lectura)",13,800,INK,anchor="start"))
    ext=[("Siigo","API OAuth lectura"),("Buzón de facturas","XML UBL y PDF"),("DIAN","listado .zip del cliente"),("RADIAN","acuses de facturas"),("RUES","registro mercantil"),("Validación de identidad","cédula + prueba de vida"),("Listas restrictivas","SARLAFT"),("Centrales de riesgo","con autorización")]
    for i,(t,sub) in enumerate(ext):
        c=i%2; r=i//2
        s.append(box(678+c*192,518+r*58,180,48,t,sub,fill="#fff",stroke=MUT,size=12))
    s.append(line(200,394,200,478,color=INK,w=1.8)); s.append(label(200,440,"L · E-int · E-mandato"))
    s.append(f'<path d="M420 394 V 464 H 865 V 476" fill="none" stroke="{MUT}" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#ah)"/>')
    s.append(label(640,464,"solo lectura, con consentimiento"))
    return wrap_svg("".join(s),W,H,"Diagrama de contexto y contenedores (C4 niveles 1 y 2)",minw=820)

# ---------------- Agents diagram ----------------
def diagram_agentes():
    W,H=1100,540; s=[]
    s.append(box(30,30,160,50,"Cliente","web o móvil",fill=YEL,stroke=INK))
    s.append(box(250,30,190,50,"Guardia de entrada","intención y señales",fill="#fff"))
    s.append(box(500,30,220,50,"A0 Orquestador","delega y responde con fuentes",fill=PUR,stroke=PUR,tc="#fff"))
    s.append(line(190,55,248,55)); s.append(line(440,55,498,55))
    col={"Informar":PUR2,"Recomendar":"#fff","Ejecutar con aprobación del cliente":YEL}
    ags=[("A1 Vinculación","ejecuta controles de lectura","Recomendar"),("A2 Datos y caja","informa y recomienda","Informar"),("A3 Validación","recomienda y detiene","Recomendar"),("A4 Uso del cupo","ejecuta con mandato","Ejecutar con aprobación del cliente"),("A5 Acompañamiento","recomienda acciones","Recomendar"),("A6 Redactor","prepara borradores","Informar")]
    sw=110; gap=10; x0=30
    for i,(t,sub,a) in enumerate(ags):
        x=x0+i*(sw+gap)
        s.append(box(x,150,sw,62,t,sub,fill=col[a],stroke=INK if a.startswith("Ejecutar") else PUR,size=10.5))
        s.append(line(610,80,x+sw/2,148,color=PUR,marker="ahp",w=1))
    s.append(box(30,280,710,54,"Gateway de herramientas + motor de políticas","allowlist · validación · mandato firmado · idempotencia · bitácora",fill=YEL,stroke=INK,size=13))
    for i in range(6):
        x=x0+i*(sw+gap)+sw/2
        s.append(line(x,212,x,278,w=1,color=MUT))
    s.append(box(30,400,340,54,"Sistemas del BFE","el motor de decisión decide · Pagos ejecuta",fill="#fff",stroke=INK))
    s.append(box(400,400,340,54,"Fuentes externas","Siigo, buzón, DIAN, RADIAN, RUES, listas, centrales",fill="#fff",stroke=MUT,dash=True))
    s.append(line(200,334,200,398)); s.append(line(570,334,570,398,dash=True,color=MUT))
    s.append(box(800,150,270,62,"A7 Copiloto de analista","informa a la persona",fill=PUR2,stroke=PUR,size=12))
    s.append(box(800,280,270,54,"CRM y cola de casos","paquete de handoff + SLA",fill="#fff",stroke=INK))
    s.append(box(800,400,270,54,"Analista u oficial","decide con el caso armado",fill=YEL,stroke=INK))
    s.append(line(935,334,935,398)); s.append(line(935,278,935,214,color=PUR,marker="ahp"))
    s.append(f'<path d="M720 70 C 790 70, 760 300, 798 305" fill="none" stroke="{INK}" stroke-width="1.3" stroke-dasharray="5 4" marker-end="url(#ah)"/>')
    s.append(label(760,110,"handoff"))
    s.append(svg_text(935,248,"anomalía · >$100 M · muestra · pedido",10.5,500,MUT))
    ly=490
    for i,(k,v) in enumerate(col.items()):
        x=30+i*250
        s.append(f'<rect x="{x}" y="{ly}" width="22" height="16" rx="4" fill="{v}" stroke="{PUR}"/>')
        s.append(svg_text(x+30,ly+8,f"Autonomía máxima: {k.lower()}",11.5,500,INK,anchor="start"))
    return wrap_svg("".join(s),W,H,"Agentes, puerta de herramientas y camino a las personas",minw=820)

# ---------------- Sequence diagrams ----------------
CH=6.1  # px per char at 11px
def diagram_seq(code, title):
    parts=[]; msgs=[]
    for raw in code.strip().splitlines():
        l=raw.strip()
        if not l: continue
        if l.startswith("@"):
            k,v=l[1:].split(":",1); parts.append((k.strip(),v.strip()))
        elif l.lower().startswith("nota:"):
            msgs.append(("note",None,None,l.split(":",1)[1].strip()))
        else:
            m=re.match(r"(\w+)\s*(-->|->)\s*(\w+)\s*:\s*(.*)",l)
            msgs.append(("dash" if m.group(2)=="-->" else "solid",m.group(1),m.group(3),m.group(4)))
    n=len(parts); colw=150 if n>6 else 180; left=20
    W=left*2+n*colw
    xs={k:left+colw*i+colw/2 for i,(k,_) in enumerate(parts)}
    s=[]; y=20
    for k,v in parts:
        s.append(box(xs[k]-colw/2+8,y,colw-16,46,v,fill=PUR if k=="O" else "#fff",tc="#fff" if k=="O" else INK,size=11.5))
    y=86; rows=[]
    for kind,a,b,t in msgs:
        if kind=="note":
            lines=wrap(t,int((W-80)/6.6)); h=len(lines)*15+12
            rows.append((kind,a,b,lines,y,h)); y+=h+12; continue
        if a==b:
            avail = min(colw*1.7, W-xs[a]-30)
            lines=wrap(t,max(14,int((avail-12)/CH))); h=len(lines)*14.5+22
        else:
            lines=wrap(t,max(14,int((abs(xs[a]-xs[b])-16)/CH))); h=len(lines)*14.5+12
        rows.append((kind,a,b,lines,y,h)); y+=h+10
    H=y+16
    for k,_ in parts:
        s.insert(0,f'<line x1="{xs[k]}" y1="66" x2="{xs[k]}" y2="{H-8}" stroke="{LINE}" stroke-width="1.6" stroke-dasharray="4 4"/>')
    for kind,a,b,lines,y0,h in rows:
        if kind=="note":
            s.append(f'<rect x="30" y="{y0}" width="{W-60}" height="{h}" rx="8" fill="#FFF3D1" stroke="{YEL}"/>')
            for i,lt in enumerate(lines):
                s.append(f'<text x="{W/2}" y="{y0+13+i*15}" font-size="11.5" font-weight="600" fill="{INK}" text-anchor="middle" dominant-baseline="middle">{esc(lt)}</text>')
            continue
        dash = kind=="dash"; color = PUR if dash else INK; mk = "ahp" if dash else "ah"
        dd = ' stroke-dasharray="5 4"' if dash else ''
        if a==b:
            x=xs[a]
            for i,lt in enumerate(lines):
                s.append(f'<text x="{x+8}" y="{y0+7+i*14.5}" font-size="11" fill="{INK}" dominant-baseline="middle">{esc(lt)}</text>')
            ly=y0+h-12
            s.append(f'<path d="M{x} {ly-6} h24 v12 h-22" fill="none" stroke="{color}" stroke-width="1.3"{dd} marker-end="url(#{mk})"/>')
        else:
            x1,x2=xs[a],xs[b]; ay=y0+h-3; sign=1 if x2>x1 else -1
            for i,lt in enumerate(lines):
                s.append(f'<text x="{(x1+x2)/2}" y="{y0+6+i*14.5}" font-size="11" fill="{INK}" text-anchor="middle" dominant-baseline="middle">{esc(lt)}</text>')
            s.append(f'<line x1="{x1}" y1="{ay}" x2="{x2-sign*2}" y2="{ay}" stroke="{color}" stroke-width="1.4"{dd} marker-end="url(#{mk})"/>')
    return wrap_svg("".join(s),W,H,title,minw=max(720,int(W*0.68)))

SEQ_TITLES={"seq_principal":"Secuencia del journey principal: del NIT al primer uso del cupo",
"seq_falla_a":"Camino de falla A: anomalía documental (aclarada o pasada a analista)",
"seq_falla_b":"Camino de falla B: uso no permitido e inyección de instrucciones",
"seq_falla_c":"Camino de falla C: abono programado sin pago del cliente"}

# ---------------- Markdown -> HTML ----------------
def inline(t):
    t=esc(t)
    t=re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t=re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t=re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<em>\1</em>", t)
    t=re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m:f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>', t)
    return t

def slug(t):
    t=re.sub(r"[^\w\s-]","",t.lower(),flags=re.U); return re.sub(r"\s+","-",t.strip())

lines=md.splitlines()
LIST_RE=r"^(\s*)([-*]|\d+\.)\s+(.*)$"
def parse_list(i):
    items=[]
    while i<len(lines):
        m=re.match(LIST_RE,lines[i])
        if not m: break
        items.append((len(m.group(1)), m.group(2)[0].isdigit(), m.group(3))); i+=1
    def build(idx, indent):
        tag="ol" if items[idx][1] else "ul"; parts=[]
        while idx<len(items) and items[idx][0]>=indent:
            if items[idx][0]>indent:
                sub,idx=build(idx, items[idx][0])
                if parts: parts[-1]=parts[-1][:-5]+sub+"</li>"
                else: parts.append("<li>"+sub+"</li>")
                continue
            parts.append(f"<li>{inline(items[idx][2])}</li>"); idx+=1
        return f"<{tag}>"+"".join(parts)+f"</{tag}>", idx
    h,_=build(0, items[0][0]); return h, i

i=0; out=[]; toc=[]; pending=None
while i<len(lines):
    l=lines[i]
    if not l.strip(): i+=1; continue
    m=re.match(r"<!-- diagram:(\w+) -->",l.strip())
    if m: pending=m.group(1); i+=1; continue
    if l.startswith("```"):
        j=i+1; buf=[]
        while not lines[j].startswith("```"): buf.append(lines[j]); j+=1
        code="\n".join(buf); i=j+1
        if pending:
            d=pending; pending=None
            out.append(diagram_contexto() if d=="contexto" else diagram_agentes() if d=="agentes" else diagram_seq(code, SEQ_TITLES[d]))
        else: out.append(f"<pre><code>{esc(code)}</code></pre>")
        continue
    m=re.match(r"^(#{1,4})\s+(.*)$",l)
    if m:
        lvl=len(m.group(1)); t=m.group(2); sid=slug(t)
        if lvl==1: out.append(f'<h1>{inline(t)}</h1>')
        else:
            if lvl==2: toc.append((sid,t))
            out.append(f'<h{lvl} id="{sid}">{inline(t)}</h{lvl}>')
        i+=1; continue
    if l.strip()=="---": out.append("<hr>"); i+=1; continue
    if l.startswith(">"):
        out.append(f'<blockquote>{inline(l.lstrip("> ").strip())}</blockquote>'); i+=1; continue
    if l.startswith("|"):
        rows=[]
        while i<len(lines) and lines[i].startswith("|"): rows.append(lines[i]); i+=1
        cells=lambda r:[c.strip() for c in r.strip().strip("|").split("|")]
        hdr=cells(rows[0]); body=[cells(r) for r in rows[2:]]
        t=['<div class="tbl"><table><thead><tr>']+[f"<th>{inline(c)}</th>" for c in hdr]+["</tr></thead><tbody>"]
        for r in body: t+=["<tr>"]+[f"<td>{inline(c)}</td>" for c in r]+["</tr>"]
        t.append("</tbody></table></div>"); out.append("".join(t)); continue
    if re.match(LIST_RE,l):
        h,i=parse_list(i); out.append(h); continue
    buf=[l.strip()]; i+=1
    while i<len(lines) and lines[i].strip() and not re.match(r"^(#|\||>|```|<!--)",lines[i]) and not re.match(LIST_RE,lines[i]) and lines[i].strip()!="---":
        buf.append(lines[i].strip()); i+=1
    out.append(f"<p>{inline(' '.join(buf))}</p>")

body="\n".join(out)
h1_end=body.index("</h1>")+5
hero_title=body[:h1_end]; rest=body[h1_end:]
sub_end=rest.index("</p>")+4
hero_sub=rest[:sub_end].replace('</strong> ','</strong><br>',1); rest=rest[sub_end:]
tochtml="".join(f'<li><a href="#{a}">{esc(t)}</a></li>' for a,t in toc)

CSS=f"""
:root{{--pur:{PUR};--ink:{INK};--yel:{YEL};--lil:{LIL};--mut:{MUT};--line:{LINE};--pur2:{PUR2}}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--lil);color:var(--ink);font:16px/1.6 "Plus Jakarta Sans",Inter,"Segoe UI",system-ui,sans-serif;-webkit-text-size-adjust:100%}}
a{{color:var(--pur)}}
.hero{{background:var(--ink);color:#fff;padding:56px 16px 44px;position:relative;overflow:hidden}}
.hero:after{{content:"";position:absolute;right:-120px;top:-140px;width:380px;height:380px;border:36px solid var(--yel);border-radius:50%;opacity:.9}}
.hero .in{{max-width:1120px;margin:auto;position:relative;z-index:1}}
.eyebrow{{color:var(--yel);font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:12px}}
.hero h1{{font-size:clamp(30px,5vw,52px);line-height:1.08;margin:10px 0 14px;letter-spacing:-.03em;max-width:18ch}}
.hero p{{color:#DCD6F5;max-width:760px;margin:0}}
.wrap{{max-width:1120px;margin:auto;padding:0 16px 64px;display:grid;grid-template-columns:230px minmax(0,1fr);gap:36px}}
nav.toc{{position:sticky;top:16px;align-self:start;margin-top:32px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 14px;font-size:13.5px;max-height:calc(100vh - 32px);overflow:auto}}
nav.toc b{{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin-bottom:6px}}
nav.toc ol{{margin:0;padding-left:0;list-style:none}}nav.toc li{{margin:6px 0}}nav.toc a{{color:var(--ink);text-decoration:none}}nav.toc a:hover{{color:var(--pur)}}
main{{min-width:0;padding-top:20px}}
h2{{font-size:clamp(23px,3vw,30px);letter-spacing:-.02em;margin:48px 0 14px;padding-top:14px;border-top:3px solid var(--pur);line-height:1.15;scroll-margin-top:12px}}
h3{{font-size:19px;margin:30px 0 10px;color:var(--pur);scroll-margin-top:12px}}
p,li{{max-width:80ch}}
ul,ol{{padding-left:22px}}li{{margin:5px 0}}
code{{font-family:"JetBrains Mono",Consolas,monospace;font-size:.85em;background:var(--pur2);color:#3A2A9A;padding:1px 5px;border-radius:5px;overflow-wrap:anywhere}}
pre{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px;overflow:auto}}pre code{{background:none;padding:0}}
blockquote{{margin:18px 0;padding:12px 16px;border-left:5px solid var(--yel);background:#fff;border-radius:0 10px 10px 0;color:var(--mut)}}
hr{{border:0;border-top:1px solid var(--line);margin:28px 0}}
.tbl{{overflow-x:auto;margin:14px 0 22px;border:1px solid var(--line);border-radius:12px;background:#fff;-webkit-overflow-scrolling:touch}}
table{{border-collapse:collapse;width:100%;font-size:14px;min-width:560px}}
th{{background:var(--ink);color:#fff;text-align:left;font-weight:700;padding:9px 10px;vertical-align:bottom}}
td{{padding:8px 10px;border-top:1px solid var(--line);vertical-align:top}}
tbody tr:nth-child(even) td{{background:#FBFAFF}}
td:first-child{{font-weight:600}}
figure.diagram{{margin:18px 0 26px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px}}
figure.diagram .scroll{{overflow-x:auto;-webkit-overflow-scrolling:touch}}
figure.diagram svg{{width:100%;height:auto;display:block}}
figcaption{{font-size:13px;color:var(--mut);margin-top:8px;text-align:center}}
footer{{background:var(--ink);color:#BDB6D8;font-size:13px;padding:24px 16px;text-align:center}}
@media (max-width:880px){{.wrap{{grid-template-columns:minmax(0,1fr);gap:0}}nav.toc{{position:static;max-height:none;margin-top:20px}}.hero:after{{opacity:.3;width:260px;height:260px;right:-110px;top:-90px}}}}
@media print{{nav.toc{{display:none}}.wrap{{display:block}}body{{background:#fff}}figure.diagram svg{{min-width:0!important}}}}
"""
doc=f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Arquitectura de Auro</title>
<meta name="description" content="Arquitectura agéntica y general de Auro by BFE: agentes, autonomía, controles, integración, evals y costos de IA.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header class="hero"><div class="in"><div class="eyebrow">Auro by BFE · Arquitectura</div>{hero_title}{hero_sub}</div></header>
<div class="wrap"><nav class="toc" aria-label="Contenido"><b>Contenido</b><ol>{tochtml}</ol></nav><main>{rest}</main></div>
<footer>Auro y el Banco de Fomento Empresarial son ficticios. Prueba técnica AI Product Engineer · Banca Pyme. Generado desde arquitectura-auro.md.</footer>
</body></html>"""
open(OUT,"w",encoding="utf-8").write(doc)
print("ok", len(doc), "secciones", len(toc))
