import base64, html, json, pathlib, io
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parent
A=ROOT/'assets'; A.mkdir(exist_ok=True)
# Crops are decorative artwork only, from the supplied concept; all labels are editable SVG text.
def b64(p): return 'data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode()
ART=b64(A/'armor.jpg'); AV=b64(A/'emblem.jpg'); CITY=b64(A/'city.jpg')
P=json.loads((ROOT/'projects.json').read_text())
E=html.escape
O='#ff9b19'; Y='#ffda55'; FG='#f4f3f6'; M='#b0b3c2'
def t(x,y,s,size=16,c=FG,w=400,space=0):
 return f'<text x="{x}" y="{y}" fill="{c}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{w}" letter-spacing="{space}">{E(str(s))}</text>'
def mono(x,y,s,size=11,c=M): return f'<text x="{x}" y="{y}" font-family="monospace" font-size="{size}" fill="{c}" letter-spacing="1">{E(str(s))}</text>'
def frame(w,h,body,art=False,anim=False):
 path=f'M 2 20 L 20 2 H {w-23} L {w-2} 23 V {h-20} L {w-20} {h-2} H 22 L 2 {h-22} Z'
 return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
 <defs><linearGradient id="base" x2=".9" y2="1"><stop stop-color="#242731"/><stop offset=".42" stop-color="#12141b"/><stop offset="1" stop-color="#090b10"/></linearGradient><linearGradient id="edge"><stop stop-color="#ffbd39"/><stop offset=".16" stop-color="#ff7911"/><stop offset=".34" stop-color="#626674"/><stop offset=".8" stop-color="#414552"/><stop offset="1" stop-color="#ff8714"/></linearGradient><linearGradient id="hot"><stop stop-color="#fb5b0c"/><stop offset=".65" stop-color="#ffc133"/><stop offset="1" stop-color="#fff08b"/></linearGradient><linearGradient id="fade"><stop stop-color="#11131a"/><stop offset="1" stop-color="#11131a" stop-opacity="0"/></linearGradient><linearGradient id="artfade"><stop stop-color="white" stop-opacity="0"/><stop offset=".35" stop-color="white" stop-opacity=".8"/><stop offset="1" stop-color="white"/></linearGradient><mask id="artmask" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#artfade)"/></mask><pattern id="mesh" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M0 11 11 0 22 11 11 22Z" fill="none" stroke="#9396a5" stroke-opacity=".045"/></pattern><clipPath id="clip"><path d="{path}"/></clipPath><filter id="glow"><feGaussianBlur stdDeviation="2.5"/></filter></defs>
 <style>@keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}@keyframes scan{{0%{{transform:translateX(-200px);opacity:0}}20%{{opacity:.5}}80%{{opacity:.5}}100%{{transform:translateX({w+100}px);opacity:0}}}}.pulse{{animation:pulse 3s ease-in-out infinite}}.scan{{animation:scan 6s linear infinite}}@media(prefers-reduced-motion:reduce){{.pulse,.scan{{animation:none}}}}</style>
 <path d="{path}" fill="url(#base)"/><g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="url(#mesh)"/>{f'<image x="{w*.58}" y="0" width="{w*.42}" height="{h}" preserveAspectRatio="xMidYMid slice" opacity=".75" mask="url(#artmask)" href="{ART}"/>' if art else ''}<path d="M{w-120} 0 H{w} V74 L{w-25} 48 H{w-45} Z" fill="#727482" opacity=".14"/><path d="M{w-87} 0 {w-19} 68 H{w} V54 L{w-55} 0Z" fill="#9b9da8" opacity=".16"/>{body}{f'<path class="scan" d="M0 0H26L-65 {h}H-91Z" fill="#ffb432" opacity=".1"/>' if anim else ''}</g><path d="{path}" fill="none" stroke="url(#edge)" stroke-width="1.5"/><path d="M3 39V20L20 3H105 M{w-111} {h-3}H{w-20}L{w-3} {h-20}V{h-40}" fill="none" stroke="#ff9014" stroke-width="5" opacity=".45" filter="url(#glow)"/><path class="pulse" d="M3 39V20L20 3H105 M{w-111} {h-3}H{w-20}L{w-3} {h-20}V{h-40}" fill="none" stroke="url(#hot)" stroke-width="2.5"/><path d="M115 3h22m5 0h10m-{0} 0" stroke="#737582" opacity=".5"/></svg>'''
def save(name,w,h,b,art=False,anim=False): (A/(name+'.svg')).write_text(frame(w,h,b,art,anim))
def head(x,y,name):return t(x,y,'//',22,O,800)+t(x+32,y,name,19,FG,700)
def icon(x,y,kind):
 shapes={'wifi':'<path d="M2 12 Q16 -1 30 12 M7 18 Q16 8 25 18 M12 24 Q16 20 20 24"/><circle cx="16" cy="29" r="1.7" fill="#ffbc45"/>','privacy':'<path d="M16 2 28 7V17Q28 25 16 31 4 25 4 17V7Z"/><path d="m10 16 4 4 8-9"/>','map':'<circle cx="16" cy="16" r="11"/><circle cx="16" cy="16" r="4"/><path d="M16 0v9m0 14v9M0 16h9m14 0h9"/>','cat':'<path d="M3 4 11 11H21L29 4V22L16 30 3 22Z"/><path d="m8 16 5 3m11-3-5 3"/>','shell':'<path d="m5 7 10 9-10 9m14 0h12"/>','scope':'<path d="M16 2 29 9V23L16 30 3 23V9Z"/><circle cx="16" cy="16" r="6"/>'}
 return f'<g transform="translate({x} {y})" fill="none" stroke="#ffb62c" stroke-width="2.3" stroke-linejoin="round" stroke-linecap="round">{shapes[kind]}</g>'
# Header, inspired by the exact first mockup.
b=f'<image x="670" y="0" width="310" height="244" href="{ART}" preserveAspectRatio="xMidYMid slice" mask="url(#artmask)"/><path d="M24 54 50 28H170L199 57V179L172 206H52L24 179Z" fill="#101217" stroke="#ff9b19" stroke-width="2"/><image x="31" y="35" width="161" height="164" href="{AV}" preserveAspectRatio="xMidYMid slice"/>'
b+=mono(225,36,'IDENTITY  /  INFINITE667',13,O)+t(225,81,'Murat Mehmeti',39,FG,800)+t(225,111,'@infinite667',21,M,600)+t(225,145,'Cybersecurity  /  PowerShell  /  IT Support',16,FG,600)+t(225,178,'Vulnerabilities are like ghosts – they exist',15,M)+t(225,198,'whether you believe in them or not.',15,M)+mono(720,27,'PROJECT: RENEKTON',12,Y)+mono(738,45,'COMMAND CENTER',11,FG)+mono(225,224,'KOSOVO  /  SECURITY RESEARCH  /  OPEN SOURCE',10,O)
save('hero',980,244,b,False,True)
# Snapshot is intentionally limited to verified numbers or design counts.
b='';
for i,(value,label) in enumerate([('16','PUBLIC REPOS*'),('6','FEATURED CARDS'),('04','VERIFIED LINKS'),('02','LINKS TO CONFIRM')]):
 x=22+i*239;b+=f'<path d="M{x} 14h205l14 14v45H{x+13}l-13-13Z" fill="#171a22" stroke="#464954"/>'+t(x+18,45,value,25,Y,800)+mono(x+18,63,label,10)
save('stats',980,88,b)
save('about',460,175,head(20,31,'About')+t(20,65,'Security-minded IT professional',19,FG,700)+t(20,89,'Interested in practical security, automation,',15,M)+t(20,111,'open-source tooling and system operations.',15,M)+mono(20,144,'CYBERSECURITY  /  IT SUPPORT  /  RESEARCH',10,O),True)
save('focus',460,175,head(20,31,'Current focus')+''.join(t(22,65+i*25,'◆',12,O)+t(44,65+i*25,s,15,FG,500) for i,s in enumerate(['Security research & documentation','Privacy & network tooling','PowerShell and system automation','Authorized lab environments'])))
save('repos-title',980,57,head(23,35,'Top repositories')+mono(722,34,'SELECT A MODULE  /  01–06',11,O),True)
for i,p in enumerate(P):
 w=480; b=f'<rect x="18" y="23" width="52" height="52" rx="10" fill="#1a191b" stroke="#81501f"/>'+icon(28,33,p['icon'])+mono(87,24,f'MODULE {i+1:02d}  /  {p["category"].upper()}',10,O)+t(87,54,p['name'],26,FG,800)
 for j,line in enumerate(p['lines']): b+=t(87,78+j*18,line,14,M)
 b+=mono(20,132,p['language'].upper()+'  /  '+('PUBLIC REPOSITORY' if p['verified'] else 'LINK TO CONFIRM'),10,O)+t(444,132,'↗',19,Y,700)
 save('repo-'+p['id'],w,147,b,True, i==0)
save('technology',460,195,head(20,32,'Technologies')+''.join(f'<rect x="{20+(i%2)*218}" y="{53+(i//2)*43}" width="202" height="33" rx="5" fill="#161820" stroke="#414450"/>'+t(31+(i%2)*218,75+(i//2)*43,s,15,FG,600) for i,s in enumerate(['Python','PowerShell','TypeScript','Shell','Go','Git / Windows'])))
save('activity',460,195,head(20,32,'Activity & contributions')+t(20,65,'Explore the real GitHub contribution graph.',14,M)+f'<image x="250" y="76" width="204" height="113" href="{CITY}" opacity=".75" preserveAspectRatio="xMidYMid slice"/>'+mono(20,99,'PUBLIC ACTIVITY',11,O)+t(20,128,'View profile activity',18,FG,700)+t(20,151,'Open on GitHub ↗',14,Y),False)
save('footer',980,105, f'<image x="650" width="330" height="105" href="{CITY}" opacity=".7" preserveAspectRatio="xMidYMid slice"/>'+mono(25,29,'// COMMAND CENTER  /  INFINITE667',12,O)+t(25,58,'Research. Build. Secure.',24,FG,800)+mono(25,82,'INDEPENDENT FAN-INSPIRED DESIGN  /  NO AFFILIATION',10,M),False,True)
