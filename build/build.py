from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L
OWN={'CL':"Chris L'Heureux",'JS':'Jared Spicer','SC':'Shane Costley','RM':'Rob Murray','CW':'Cory Wood','PT':'Patrick Tighe','MF':'Mike Frazier','SG':'Scott Gilmore','BZ':'Brandon Zamora','TF':'Tina Frazier','OM':'Owen Moore','DH':'Dan Hanlon','DS':'Derek Saddler'}
TEAMS={2016:{'SG':'Brazzers University','PT':'RIP in peace Harambe','CL':'The Brady Bunch','JS':'Spice Cream Sandwich','MF':'Gurleys Gone Wild','SC':'Drakes New Favorite Team','RM':'LAY IT ON THICK PREZ','BZ':'Antonio Brown Eye','TF':'Team Badonkagronk','CW':'Cuncel That 75..'},
2017:{'RM':"Hillary's Emails",'MF':'Dez-ed and Confused','PT':'90s Buffalo Bills','BZ':'20 dollar Side bet','CL':'The Brady Bunch','OM':'Team Badonkagronk','SC':'Drakes New Favorite Team','JS':'Spice Cream Sandwich','CW':'Play Better','SG':'Cuncel The Season'},
2018:{'SG':'My Ball Zach Ertz','CW':'Saquon Deez Nutz','JS':'Pizza Hunt','BZ':'Zeke-a Leak','CL':'Kittles Cock','MF':'Beats by deanDRE','PT':'2000s Buffalo Bills','DH':'Beaver Munchers','SC':'All Budget Team Moneyball','RM':'Space Force'},
2019:{'PT':'Hanging With Hernandez','MF':"Davante's Inferno",'RM':'King of Israel','CW':'8am Starts','CL':'Boy Genius','SG':'Kareempie My KHunt','SC':'All Budget Team Moneyball','BZ':'Cuncel the Chubb','JS':"Cuncel The SAT's",'DS':'Blackout Warriors'}}
TOP4={2016:'SG PT CL JS',2017:'RM MF PT BZ',2018:'SG CW JS BZ',2019:'PT MF RM CW'}
FINAL={2016:('SG','PT'),2017:('RM','MF'),2018:('SG','CW'),2019:('PT','MF')}
O2020={'Mixon Up The Medicine':'Brandon Zamora','Barron Trump Simp':'Rob Murray','YogurtSlanger':'Mike Frazier','Momoney519':'Derek Saddler','Christian Mingle':"Chris L'Heureux",'Large Black Coffee':'Jared Spicer',"Lebron's Bald":'Cory Wood','AP Daycare':'Patrick Tighe','99 Yard Cuncel':'Scott Gilmore','The Brady Bunch':'Shane Costley'}
Y={'LBC':'Large Black Coffee','YS':'YogurtSlanger','BTS':'Barron Trump Simp','TBB':'The Brady Bunch','LB':"Lebron's Bald",'MX':'Mixon Up The Medicine','MM':'Momoney519','CM':'Christian Mingle','C99':'99 Yard Cuncel','AP':'AP Daycare'}
rows=[]
for line in open('espn.txt'):
    if line.startswith('#') or not line.strip(): continue
    p=line.split(); y=int(p[0]); w=p[1]; a,sa,sb,b=p[2],int(p[3]),int(p[4]),p[5]
    ov='B' if len(p)>6 else ''
    note=''
    if w.startswith('P'):
        top=TOP4[y].split()
        if a in top and b in top:
            gt='Playoffs'
            rnd='Semifinal' if w=='P1' else ('Championship' if {a,b}==set(FINAL[y]) else '3rd Place')
        else:
            gt='Consolation'; rnd='Consolation Rd 1' if w=='P1' else 'Consolation Rd 2'
        wk='14-15' if w=='P1' else '16-17'
    else:
        gt='Regular Season'; rnd=''; wk=int(w)
    if ov: note='ESPN marked the home team as the winner despite the displayed (rounded) score; winner set to match ESPN.'
    if y==2018 and w=='9' and a=='CL': note='Kept the scoreboard score (119-58). ESPN standings show 20 more pts for L\'Heureux PF / Murray PA; tracker corrected to match the scoreboard.'
    rows.append((y,wk,gt,rnd,'ESPN',TEAMS[y][a],sa,sb,TEAMS[y][b],ov,note))
seen=set()
for line in open('yahoo.txt'):
    t,*g=line.strip().split('|')
    for w,x in enumerate(g,1):
        o,a,b=x.split()
        k=(w,frozenset((t,o)))
        if k in seen: continue
        seen.add(k)
        rows.append((2020,w,'Regular Season','','Yahoo',Y[t],float(a),float(b),Y[o],'',''))
for wk,gt,rnd,ta,sa,sb,tb in [
    (16,'Playoffs','Semifinal','Barron Trump Simp',116.32,145.94,'Momoney519'),
    (16,'Playoffs','Semifinal','Mixon Up The Medicine',141.60,119.14,'YogurtSlanger'),
    (17,'Playoffs','Championship','Momoney519',131.94,176.56,'Mixon Up The Medicine'),
    (17,'Playoffs','3rd Place','Barron Trump Simp',119.88,128.58,'YogurtSlanger'),
    (17,'Consolation','7th Place','AP Daycare',182.80,127.32,'99 Yard Cuncel'),
    (17,'Consolation','5th Place','Large Black Coffee',149.28,145.44,'Christian Mingle'),
    (16,'Consolation','Consolation Rd 1','AP Daycare',120.40,187.78,'Large Black Coffee'),
    (16,'Consolation','Consolation Rd 1','99 Yard Cuncel',129.52,131.16,'Christian Mingle')]:
    rows.append((2020,wk,gt,rnd,'Yahoo',ta,sa,sb,tb,'',''))
from sleeper_games import official as _off
_sg,_sfin,_smeta=_off()
for g in _sg:
    rows.append((g[0],int(g[1]),g[2],g[3],'Sleeper',g[4],g[6],g[7],g[8],g[11],g[12]))
rows.sort(key=lambda r:(r[0],str(r[1]).zfill(5)))

wb=Workbook()
F=Font(name='Arial',size=10); FB=Font(name='Arial',size=10,bold=True); FH=Font(name='Arial',size=10,bold=True,color='FFFFFF')
HF=PatternFill('solid',fgColor='1F3864'); YF=PatternFill('solid',fgColor='FFFF00'); BLUE=Font(name='Arial',size=10,color='0000FF')
def hdr(ws,cols,r=1):
    for i,c in enumerate(cols,1):
        x=ws.cell(r,i,c); x.font=FH; x.fill=HF; x.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
    ws.freeze_panes=ws.cell(r+1,1)

# Read Me
rm=wb.active; rm.title='Read Me'
txt=[('CFFFL Matchup History — ESPN 2016–2019, Yahoo 2020, Sleeper 2021–2026',FB),('',F),
('How it works',FB),
('Matchups lists every game once. Owners are looked up from Owner Map by season + team name, so the H2H tabs follow the person, not the team name.',F),
('2020 Yahoo owners were matched to your CFFFL tracker by W-L, Pts For and Pts Agnst (all ten unique matches).',F),
('Winner Override (Matchups col J): A, B or T (tie) forces the winner when the platform ruled differently than the displayed score. Blue = typed-in data.',F),
('',F),('Checks run',FB),
('ESPN 2016–2019: every owner\'s W-L-T matches the final standings screenshots; points match within ESPN rounding except the one game flagged below.',F),
('Yahoo 2020: both teams\' schedules agree on every game, and every W-L, Pts For and Pts Agnst match the standings to the cent.',F),
('',F),('Open items',FB),
('1. Names match the CFFFL tracker. Your tracker groups Tina Frazier (2016), Owen Moore (2017), Dan Hanlon (2018) and Derek Saddler (2019–2021) into the Brendan Mahoney* seat; here they stay separate people.',F),
('2. 2020: Yahoo weeks 1–15 were regular season; playoffs were weeks 16–17. All playoff and consolation games are loaded.',F),
("3. 2018 Wk 9 L'Heureux 119 – Murray 58: kept the scoreboard score. ESPN's standings are 20 pts higher for both teams.",F),
('4. ESPN shows whole-number scores and 2-week combined playoff scores (Wk 14-15, 16-17).',F),
('5. Sleeper 2021–2026 pulled from Sleeper on Oct 31, 2026; 2026 runs through Week 7. Sleeper has since recalculated some 2021–2023 weekly scores, so those seasons\' point totals can differ from your tracker by a few points. Records follow Sleeper\'s official final standings (two 2022 games set by Winner Override).',F),
('6. Names follow your CFFFL tracker, including Cam Terio (Sleeper user CTerio, new in 2026).',F)]
for i,(t,f) in enumerate(txt,1): rm.cell(i,1,t).font=f
rm.column_dimensions['A'].width=140

# Owner Map
om=wb.create_sheet('Owner Map')
hdr(om,['Key','Season','Platform','Team','Owner'])
r=2
for y in (2016,2017,2018,2019):
    for code,team in sorted(TEAMS[y].items(),key=lambda kv:kv[1].lower()):
        om.cell(r,1,f'=B{r}&"|"&D{r}'); om.cell(r,2,y); om.cell(r,3,'ESPN'); om.cell(r,4,team); om.cell(r,5,OWN[code]); r+=1
for team in sorted(Y.values(),key=str.lower):
    om.cell(r,1,f'=B{r}&"|"&D{r}'); om.cell(r,2,2020); om.cell(r,3,'Yahoo'); om.cell(r,4,team)
    c=om.cell(r,5,O2020[team])
    c.comment=Comment('Matched to the 2020 tab of your CFFFL tracker by W-L, PF and PA.','Claude')
    r+=1
for y in sorted(_smeta):
    for rid in sorted(_smeta[y]['team'],key=lambda k:_smeta[y]['team'][k].lower()):
        om.cell(r,1,f'=B{r}&"|"&D{r}'); om.cell(r,2,y); om.cell(r,3,'Sleeper'); om.cell(r,4,_smeta[y]['team'][rid]); om.cell(r,5,_smeta[y]['owner'][rid])
        r+=1
for row in om.iter_rows(min_row=2,max_row=r-1):
    for c in row:
        if c.font!=FH: c.font=BLUE if c.column>1 else F
for col,w in zip('ABCDE',(26,8,9,28,20)): om.column_dimensions[col].width=w
OMN=r-1

# Matchups
mt=wb.create_sheet('Matchups')
cols=['Season','Week','Game Type','Round','Platform','Team A','Owner A','Score A','Score B','Winner Override','Team B','Owner B','Result','Winner','Loser','Margin','Notes']
hdr(mt,cols)
for i,(y,wk,gt,rnd,pl,ta,sa,sb,tb,ov,note) in enumerate(rows,2):
    vals={1:y,2:wk,3:gt,4:rnd,5:pl,6:ta,8:sa,9:sb,10:ov or None,11:tb,17:note or None}
    for c,v in vals.items():
        x=mt.cell(i,c,v); x.font=BLUE if c in (1,2,3,4,5,6,8,9,10,11) else F
    mt.cell(i,7,f'=IFERROR(INDEX(\'Owner Map\'!$E$2:$E$1000,MATCH(A{i}&"|"&F{i},\'Owner Map\'!$A$2:$A$1000,0)),"")')
    mt.cell(i,12,f'=IFERROR(INDEX(\'Owner Map\'!$E$2:$E$1000,MATCH(A{i}&"|"&K{i},\'Owner Map\'!$A$2:$A$1000,0)),"")')
    mt.cell(i,13,f'=IF(J{i}="T","Tie",IF(J{i}="A","A Win",IF(J{i}="B","B Win",IF(H{i}>I{i},"A Win",IF(I{i}>H{i},"B Win","Tie")))))')
    mt.cell(i,14,f'=IF(M{i}="A Win",G{i},IF(M{i}="B Win",L{i},""))')
    mt.cell(i,15,f'=IF(M{i}="A Win",L{i},IF(M{i}="B Win",G{i},""))')
    mt.cell(i,16,f'=ABS(H{i}-I{i})')
    for c in (7,12,13,14,15,16): mt.cell(i,c).font=F
    for c in (8,9,16): mt.cell(i,c).number_format='0.00'
N=len(rows)+1
NR=5000
mt.auto_filter.ref=f'A1:Q{N}'
for col,w in zip(range(1,18),(8,7,15,16,9,26,17,9,9,10,26,17,9,17,17,8,60)): mt.column_dimensions[L(col)].width=w

# H2H
owners=sorted(list(OWN.values())+['Brendan Mahoney','Cam Terio'],key=lambda s:s.split()[-1]+s)
R=lambda c:f"Matchups!${c}$2:${c}${NR}"
def h2h(name,cond):
    ws=wb.create_sheet(name)
    ws.cell(1,1,f'{name}: row owner\'s W-L-T vs column owner. Blank yellow slots: type a 2020 owner\'s name in both the row and column header.').font=FB
    n=len(owners)+2
    hr=3
    ws.cell(hr,1,'Owner').font=FH; ws.cell(hr,1).fill=HF
    names=owners+['','']
    for j,o in enumerate(names):
        c=ws.cell(hr,j+2,o if o else None); c.font=FH; c.fill=HF if o else YF; c.alignment=Alignment(horizontal='center',wrap_text=True)
        if not o: c.font=FB
        rc=ws.cell(hr+1+j,1,o if o else None); rc.font=FB; 
        if not o: rc.fill=YF
    tot=len(names)+2
    ws.cell(hr,tot,'Total W').font=FH; ws.cell(hr,tot).fill=HF
    ws.cell(hr,tot+1,'Total L').font=FH; ws.cell(hr,tot+1).fill=HF
    ws.cell(hr,tot+2,'Total T').font=FH; ws.cell(hr,tot+2).fill=HF
    for i in range(len(names)):
        r=hr+1+i
        for j in range(len(names)):
            c=L(j+2); me=f'$A{r}'; op=f'{c}${hr}'
            W=f'COUNTIFS({R("N")},{me},{R("O")},{op}{cond})'
            Lo=f'COUNTIFS({R("N")},{op},{R("O")},{me}{cond})'
            T=f'COUNTIFS({R("G")},{me},{R("L")},{op},{R("M")},"Tie"{cond})+COUNTIFS({R("G")},{op},{R("L")},{me},{R("M")},"Tie"{cond})'
            x=ws.cell(r,j+2,f'=IF(OR({me}="",{op}="",{me}={op}),"",IF({W}+{Lo}+{T}=0,"",{W}&"-"&{Lo}&"-"&{T}))')
            x.font=F; x.alignment=Alignment(horizontal='center')
        ws.cell(r,tot,f'=IF($A{r}="","",COUNTIFS({R("N")},$A{r}{cond}))').font=F
        ws.cell(r,tot+1,f'=IF($A{r}="","",COUNTIFS({R("O")},$A{r}{cond}))').font=F
        ws.cell(r,tot+2,f'=IF($A{r}="","",COUNTIFS({R("G")},$A{r},{R("M")},"Tie"{cond})+COUNTIFS({R("L")},$A{r},{R("M")},"Tie"{cond}))').font=F
    ws.column_dimensions['A'].width=17
    for j in range(2,tot+3): ws.column_dimensions[L(j)].width=10
    ws.row_dimensions[hr].height=30
    ws.freeze_panes='B4'
h2h('H2H Regular Season',f',{R("C")},"Regular Season"')
h2h('H2H All Games','')
wb.save('CFFFL_Matchup_History.xlsx')
print(len(rows),'games')
