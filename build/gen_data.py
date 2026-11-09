import json, re
src=open('build.py').read()
ns={}
# reuse OWN/TEAMS/TOP4/FINAL/Y and the rows-building section from build.py without writing the workbook
code=src.split("wb=Workbook()")[0]
exec(code,ns)
rows=ns['rows']; TEAMS=ns['TEAMS']; OWN=ns['OWN']; Y=ns['Y']
team2own={}
for y,d in TEAMS.items():
    for c,t in d.items(): team2own[(y,t)]=OWN[c]
for t,o in ns['O2020'].items(): team2own[(2020,t)]=o
from sleeper_games import official as _o
_g,_f,_m=_o()
for _y,_mm in _m.items():
    for _r,_t in _mm['team'].items(): team2own[(_y,_t)]=_mm['owner'][_r]
games=[]
for (y,wk,gt,rnd,pl,ta,sa,sb,tb,ov,note) in rows:
    w = ov if ov in ('A','B','T') else ('A' if sa>sb else 'B' if sb>sa else 'T')
    games.append([y,str(wk),gt,rnd,ta,team2own.get((y,ta),''),sa,sb,tb,team2own.get((y,tb),''),w])
order={2016:'SG PT CL JS MF SC RM BZ TF CW',2017:'RM MF PT BZ CL OM SC JS CW SG',2018:'SG CW JS BZ CL MF PT DH SC RM',2019:'PT MF RM CW CL SG SC BZ JS DS'}
fin={}
for y,s in order.items():
    fin[y]=[{'owner':OWN[c],'team':TEAMS[y][c]} for c in s.split()]
fin[2020]=[{'owner':team2own.get((2020,t),''),'team':t} for t in ['Mixon Up The Medicine','Momoney519','YogurtSlanger','Barron Trump Simp','Large Black Coffee','Christian Mingle','AP Daycare','99 Yard Cuncel',"Lebron's Bald",'The Brady Bunch']]
from sleeper_games import official
sg,sfin,smeta=official()
for y,f in sfin.items(): fin[y]=f
plat={2016:'ESPN',2017:'ESPN',2018:'ESPN',2019:'ESPN',2020:'Yahoo'}
for y in smeta: plat[y]='Sleeper'
inprog={y:smeta[y]['last'] for y in smeta if smeta[y]['status']!='complete'}
off={}
for _y,_mm in smeta.items():
    if _y in (2021,2022,2023): off[_y]={_mm['owner'][r[0]]:[r[5],r[6]] for r in _mm['rosters']}
json.dump({'official':off,'inprogress':inprog,'games':games,'finish':fin,'platform':plat},open('hof_data.json','w'),separators=(',',':'))
print(len(games), len(open('hof_data.json').read()))
