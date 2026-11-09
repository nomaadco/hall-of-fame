import json, collections
S=json.load(open('sleeper.json'))
NAME={'446054268240130048':'Patrick Tighe','446862255615635456':'Mike Frazier','446866328347734016':'Jared Spicer','516714221155926016':'Shane Costley',
'730200022943113216':'Scott Gilmore','730207554826780672':'Rob Murray','730214714302431232':'Cory Wood','730451329176158208':'Brandon Zamora',
'730453339724201984':"Chris L'Heureux",'869032768028442624':'Brendan Mahoney','732737556466216960':'Derek Saddler','1245364146275373056':'Cam Terio'}
def build():
    games=[]; meta={}
    for s in S['seasons']:
        y=int(s['season']); users={u[0]:u for u in s['users']}
        team={}; owner={}
        for r in s['rosters']:
            rid,oid=r[0],r[1]; u=users.get(oid)
            owner[rid]=NAME[oid]; team[rid]=(u[2].strip() if u and u[2].strip() else (u[1] if u else 'Roster %d'%rid))
        pws=s['pws']; last = 17 if s['status']=='complete' else s['lw']
        wk={int(k):v for k,v in s['weeks'].items() if int(k)<=last}
        for w,ms in sorted(wk.items()):
            if w>=pws: continue
            by=collections.defaultdict(list)
            for rid,mid,p in ms:
                if mid is not None: by[mid].append((rid,p))
            for mid,p in sorted(by.items()):
                assert len(p)==2,(y,w,mid)
                (a,sa),(b,sb)=p
                games.append([y,str(w),'Regular Season','',team[a],owner[a],sa,sb,team[b],owner[b],'A' if sa>sb else 'B' if sb>sa else 'T'])
        pts={w:{rid:p for rid,mid,p in ms} for w,ms in wk.items()}
        for key,typ in (('wb','Playoffs'),('lb','Consolation')):
            for r,m,t1,t2,wn,ls,pl in s[key]:
                w=pws+r-1
                if t1 is None or t2 is None or wn is None or w not in pts: continue
                if typ=='Playoffs':
                    rnd={1:'Championship',3:'3rd Place',5:'5th Place'}.get(pl) or ('Quarterfinal' if r==1 else 'Semifinal')
                else:
                    rnd={1:'Consolation Final',3:'Consolation 3rd'}.get(pl) or 'Consolation Rd %d'%r
                sa,sb=pts[w][t1],pts[w][t2]
                games.append([y,str(w),typ,rnd,team[t1],owner[t1],sa,sb,team[t2],owner[t2],'A' if wn==t1 else 'B'])
        meta[y]={'status':s['status'],'last':last,'pws':pws,'team':team,'owner':owner,'wb':s['wb'],'rosters':s['rosters']}
    return games,meta
if __name__=='__main__':
    games,meta=build()
    print(len(games),'games')
    # check vs Sleeper roster totals
    agg=collections.defaultdict(lambda:[0,0,0,0.0,0.0])
    for y,w,gt,rnd,ta,oa,sa,sb,tb,ob,win in games:
        if gt!='Regular Season': continue
        for o,me,op,iw in ((oa,sa,sb,win=='A'),(ob,sb,sa,win=='B')):
            r=agg[(y,o)];r[3]+=me;r[4]+=op;r[2 if win=='T' else 0 if iw else 1]+=1
    bad=0
    for y,m in meta.items():
        for rid,oid,W,Lo,T,pf,pa in m['rosters']:
            r=agg[(y,NAME[oid])]
            if (r[0],r[1],r[2])!=(W,Lo,T) or abs(r[3]-pf)>0.01 or abs(r[4]-pa)>0.01: print('SLEEPER',y,NAME[oid],r,(W,Lo,T,pf,pa)); bad+=1
    from openpyxl import load_workbook
    wf=load_workbook('/mnt/user-data/attachments/1b63a7c0-6fbd-5ca7-93eb-2fb878b99be3/5e1a0c58-Carvers_Finest_FFL_Tracker_excel.xlsx')
    seat={2021:'Derek Saddler'}
    for y in range(2021,2026):
        for row in wf[str(y)].iter_rows(min_row=2,max_row=11,values_only=True):
            n=row[0].replace('*','') if row[0]!='Brendan Mahoney*' else seat.get(y,'Brendan Mahoney')
            r=agg[(y,n)]
            if (r[0],r[1],r[2])!=(row[1],row[2],row[3]) or abs(r[3]-row[6])>0.01 or abs(r[4]-row[7])>0.01: print('TRACKER',y,n,r,row[1:4],row[6:8]); bad+=1
    print('mismatches',bad)
    for y in sorted(meta):
        champ=[g for g in games if g[0]==y and g[3]=='Championship']
        for g in champ: print(y,'final',g[5],g[6],'-',g[7],g[9],'winner',g[5] if g[10]=='A' else g[9])

# Official-result overrides where Sleeper's recalculated weekly points disagree with its own final standings
OVERRIDES={}
NOTE={(2022,'6'):"Score from the Sleeper app (original). Sleeper's data feed has since re-scored this week.",
      (2022,'7'):"Score from the Sleeper app (original). Sleeper's data feed has since re-scored this week.",
      (2022,'1'):"Score from the Sleeper app (original). Sleeper's data feed has since re-scored it to Frazier 152.22-151.68.",
      (2022,'3'):"Score from the Sleeper app (original). Sleeper's data feed has since re-scored it to Mahoney 124.54-122.64."}
# Scores as shown in the Sleeper app (original), where the API feed has re-scored them
APP_SCORES={(2022,'1'):{'Brendan Mahoney':153.68,'Mike Frazier':151.22},(2022,'3'):{"Chris L'Heureux":123.64,'Brendan Mahoney':120.54},
 (2022,'6'):{'Patrick Tighe':104.16,'Cory Wood':97.20,'Scott Gilmore':134.92,'Mike Frazier':134.92,'Shane Costley':128.74,'Brandon Zamora':118.00,'Jared Spicer':119.62,'Brendan Mahoney':122.96,'Rob Murray':153.74,"Chris L'Heureux":111.14},
 (2022,'7'):{'Scott Gilmore':93.22,'Brendan Mahoney':99.24,'Shane Costley':178.32,'Jared Spicer':106.36,'Rob Murray':172.62,'Brandon Zamora':115.00,'Cory Wood':126.44,"Chris L'Heureux":127.70}}
def official():
    games,meta=build(); out=[]
    for g in games:
        fx=APP_SCORES.get((g[0],g[1]))
        if fx and g[2]=='Regular Season' and g[5] in fx and g[9] in fx:
            g=g[:]; g[6]=fx[g[5]]; g[7]=fx[g[9]]; g[10]='A' if g[6]>g[7] else 'B' if g[7]>g[6] else 'T'
        k=(g[0],g[1],g[5],g[9]); ov=OVERRIDES.get(k,'')
        note=NOTE.get((g[0],g[1]),'') if (ov or (fx and g[2]=='Regular Season' and g[5] in fx and g[9] in fx)) else ''
        if g[0] in (2021,2022,2023) and g[2]=='Regular Season' and not note: note=''
        out.append(g[:10]+[ov or g[10],ov,note])
    # finishes
    fin={}
    for y,m in meta.items():
        own=m['owner']; team=m['team']
        rs=sorted(m['rosters'],key=lambda r:(-r[2],-r[5]))
        if m['status']!='complete':
            fin[y]=[{'owner':own[r[0]],'team':team[r[0]]} for r in rs]; continue
        place={}
        for r,mm,t1,t2,wn,ls,pl in m['wb']:
            if pl in (1,3,5) and wn: place[wn]=pl; place[ls]=pl+1
        order=sorted(place,key=lambda k:place[k])+[r[0] for r in rs if r[0] not in place]
        fin[y]=[{'owner':own[k],'team':team[k]} for k in order]
    return out,fin,meta
