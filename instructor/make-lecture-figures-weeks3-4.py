"""Rebuild SVG diagrams and actual-data plots for lecture days 11–20.

Run from the repository root. All numeric course plots read the supplied CSVs;
conceptual diagrams are explicitly schematic rather than screenshots.
"""
from pathlib import Path
import csv
import math
import random
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from lecture_svg import Drawing, INK, TEAL, PURPLE, RED, BLUE, GREY, PALE
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
matplotlib.rcParams.update({'svg.fonttype': 'none', 'font.size': 16,
                             'axes.spines.top': False, 'axes.spines.right': False,
                             'axes.labelsize': 17, 'figure.facecolor': 'white'})

STEMS = {11:'11-data-quality',12:'12-variation',13:'13-group-summaries',
14:'14-replicates-uncertainty',15:'15-descriptive-report',16:'16-comparisons',
17:'17-welch-test',18:'18-paired',19:'19-calibration',20:'20-association'}
def dest(day, name):
    p = ROOT / 'lectures' / STEMS[day] / name
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def save_plot(fig, day, name):
    fig.tight_layout()
    fig.savefig(dest(day, name), format='svg', bbox_inches='tight')
    plt.close(fig)

def records(name):
    with (ROOT / 'data' / name).open() as f:
        return list(csv.DictReader(f))

plants = records('seedlings.csv')
control = [float(r['final_mm'])-float(r['initial_mm']) for r in plants if r['treatment']=='control']
treated = [float(r['final_mm'])-float(r['initial_mm']) for r in plants if r['treatment']=='treated']
means = [statistics.mean(control), statistics.mean(treated)]
sds = [statistics.stdev(control), statistics.stdev(treated)]
diff = means[1]-means[0]
lo, hi = 2.700984, 9.732349
paired = records('paired.csv')
before = [float(r['before_umol_m2_s']) for r in paired]
after = [float(r['after_umol_m2_s']) for r in paired]

# A small plant pictogram: independently potted plant, not a data table.
def plant(d, x, y, colour=TEAL, label=None, scale=1):
    s=scale
    d.path(f'M{x-22*s},{y} h{44*s} l{-7*s},{34*s} h{-30*s} Z', fill='#cfb797', stroke='#80664b', width=2)
    d.line(x, y, x, y-58*s, colour, width=3)
    d.path(f'M{x},{y-28*s} Q{x-45*s},{y-65*s} {x-30*s},{y-65*s} Q{x},{y-65*s} {x},{y-28*s}', fill=colour, stroke=colour, width=2)
    d.path(f'M{x},{y-42*s} Q{x+45*s},{y-80*s} {x+30*s},{y-80*s} Q{x},{y-80*s} {x},{y-42*s}', fill=colour, stroke=colour, width=2)
    if label: d.text(x, y+60*s, label, size=22, anchor='middle')

# Day 11: provenance, supported unit conversion, missingness, and traceability.
d=Drawing(title='One plant can be accidentally recorded twice')
plant(d,110,245,label='P01')
d.arrow(180,220,310,170);d.arrow(180,230,310,320)
for y in [100,270]:
    d.file(340,y,'P01 record',width=180,height=105)
    d.text(430,y+65,'25.7 → 44.3 mm',size=20,anchor='middle')
d.rect(660,160,350,150,fill='#f8e9ec',stroke=RED)
d.text(835,215,'Two rows',anchor='middle',size=32)
d.text(835,265,'one measured plant',anchor='middle',size=27)
d.arrow(545,175,640,215);d.arrow(545,340,640,270)
d.save(dest(11,'duplicate-record.svg'))

d=Drawing(title='The same length can be written in millimetres or centimetres')
for start,label in [(75,'43.8 mm'),(620,'4.38 cm')]:
    d.line(start,230,start+400,230,INK,width=6)
    for i in range(11):d.line(start+40*i,220,start+40*i,250 if i%5 else 270,INK,width=3)
    d.text(start+200,160,label,size=44,anchor='middle')
d.arrow(500,230,590,230)
d.text(550,330,'same length; different unit',anchor='middle',size=31)
d.text(550,405,'Correct P21 only because the source notebook confirms 43.8 mm.',anchor='middle',size=26)
d.save(dest(11,'unit-evidence.svg'))

d=Drawing(title='Missing measurement differs from an observed zero change')
plant(d,240,260,label='P06')
d.circle(350,150,40,fill='#fff',stroke=RED);d.text(350,164,'?',size=44,fill=RED,anchor='middle')
d.text(240,370,'No final reading',size=31,anchor='middle')
d.text(240,415,'growth is NA',size=27,anchor='middle')
plant(d,740,260,label='another plant')
d.line(830,110,830,260,BLUE,width=5)
d.text(890,185,'same length',size=25,anchor='middle')
d.text(770,370,'Observed no change',size=31,anchor='middle')
d.text(770,415,'growth is 0 mm',size=27,anchor='middle')
d.line(530,70,530,440,GREY,dashed=True)
d.save(dest(11,'missing-versus-zero.svg'))

d=Drawing(title='An original file, a repair script and new output preserve provenance')
for x,name in [(65,'raw CSV'),(455,'repair.R'),(845,'clean CSV')]:
    d.file(x,150,name,width=170,height=150)
d.arrow(255,220,420,220);d.arrow(645,220,810,220)
d.text(150,100,'PRESERVE',anchor='middle',fill=BLUE,weight='bold')
d.text(540,100,'EXPLAIN',anchor='middle',fill=PURPLE,weight='bold')
d.text(930,100,'RECREATE',anchor='middle',fill=TEAL,weight='bold')
d.text(550,440,'The script records the evidence for each change.',anchor='middle',size=30)
d.save(dest(11,'provenance.svg'))

d=Drawing(title='Missing values affect available counts without removing the plant')
for panel,(label,n,missing) in enumerate([('control',12,5),('treated',12,None)]):
    x0=80+panel*560
    for i in range(n):
        x=x0+(i%6)*72;y=160+(i//6)*110
        d.circle(x,y,22,fill=TEAL if panel==0 else PURPLE)
        if i==missing:
            d.circle(x,y,29,fill='white',stroke=RED)
            d.text(x,y+9,'?',size=29,fill=RED,anchor='middle')
    d.text(x0+180,80,label,anchor='middle',size=35)
    d.text(x0+180,375,'12 plant records',anchor='middle',size=28)
    d.text(x0+180,425,'11 available growths' if missing is not None else '12 available growths',anchor='middle',size=25)
d.save(dest(11,'available-counts.svg'))

# Day 12: centre, deviations, squared units and a change of scale.
fig,ax=plt.subplots(figsize=(10,4))
ax.scatter(control,[1]*len(control),s=90,color=TEAL)
ax.axvline(means[0],color=RED,lw=2,label=f'mean = {means[0]:.2f} mm')
ax.set(xlabel='Control growth (mm)',yticks=[],ylim=(.7,1.3))
ax.legend(loc='upper left');save_plot(fig,12,'control-centre.svg')

fig,ax=plt.subplots(figsize=(10,4))
for x in [12,14,16]:
    ax.scatter(x,1,s=170,color=TEAL,zorder=3)
    ax.annotate(f'{x-14:+d} mm',(x,.93),ha='center',fontsize=19)
ax.axvline(14,color=RED,ls='--',label='mean 14 mm')
ax.annotate('',(12,.78),(14,.78),arrowprops={'arrowstyle':'<->','color':PURPLE,'lw':2})
ax.annotate('',(14,.78),(16,.78),arrowprops={'arrowstyle':'<->','color':PURPLE,'lw':2})
ax.set(xlim=(10,18),ylim=(.6,1.3),yticks=[],xlabel='Measured growth (mm)')
ax.legend(loc='upper left');save_plot(fig,12,'deviations.svg')

d=Drawing(title='Squaring a two millimetre deviation gives four square millimetres')
d.rect(120,100,220,220,fill='#e6f3f5')
d.line(230,100,230,320,TEAL);d.line(120,210,340,210,TEAL)
d.text(230,370,'2 mm',anchor='middle',size=31)
d.text(75,220,'2',anchor='middle',size=31)
d.arrow(385,210,500,210)
d.text(770,170,'4 mm²',anchor='middle',size=48,fill=PURPLE)
d.text(770,235,'one squared deviation',anchor='middle',size=30)
d.text(770,305,'SD takes the square root',anchor='middle',size=28)
d.text(770,355,'back to millimetres',anchor='middle',size=28)
d.save(dest(12,'squared-units.svg'))

fig,axes=plt.subplots(1,3,figsize=(12,4))
for ax,values,label in zip(axes,[[13,14,15],[23,24,25],[1.3,1.4,1.5]],['Original (mm)','Add 10 mm','Convert to cm']):
    ax.scatter(values,[1]*3,s=95,color=TEAL)
    ax.axvline(statistics.mean(values),color=RED,ls='--')
    ax.set(yticks=[],title=label,ylim=(.8,1.2))
    ax.set_xlabel(f'mean {statistics.mean(values):g}; SD {statistics.stdev(values):g}')
save_plot(fig,12,'shift-and-scale.svg')

# Day 13: individual data, grouped summaries, SD and histogram choices.
fig,ax=plt.subplots(figsize=(10,4))
for i,(values,colour) in enumerate([(control,TEAL),(treated,PURPLE)]):
    xs=[i+(.025*(j%5-2)) for j in range(len(values))]
    ax.scatter(xs,values,color=colour,s=55,alpha=.8)
    ax.scatter([i],[statistics.mean(values)],marker='D',s=170,color=RED,zorder=5)
ax.set(xticks=[0,1],xticklabels=['control','treated'],ylabel='Seven-day growth (mm)',xlim=(-.5,1.5))
save_plot(fig,13,'individuals-and-means.svg')

fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
for i,values in enumerate([control,treated]):
    axes[0].scatter([i]*len(values),values,s=45,color=[TEAL,PURPLE][i],alpha=.8)
    axes[1].scatter(i,statistics.mean(values),s=190,marker='D',color=RED)
for ax in axes: ax.set(xticks=[0,1],xticklabels=['control','treated'],xlim=(-.4,1.4))
axes[0].set(title='24 observations',ylabel='Growth (mm)');axes[1].set_title('2 summary rows')
save_plot(fig,13,'observations-to-summary.svg')

fig,ax=plt.subplots(figsize=(10,4))
for i,values in enumerate([control,treated]):
    ax.errorbar(i,statistics.mean(values),yerr=statistics.stdev(values),fmt='D',color=RED,capsize=12,ms=10)
    ax.scatter([i+.15]*len(values),values,color=[TEAL,PURPLE][i],alpha=.7,s=45)
ax.set(xticks=[0,1],xticklabels=['control','treated'],ylabel='Growth (mm)',title='Diamonds and whiskers: mean ± sample SD',xlim=(-.5,1.5))
save_plot(fig,13,'sd-bars.svg')

fig,axes=plt.subplots(1,2,figsize=(11,4),sharex=True,sharey=True)
for ax,values,label,colour in zip(axes,[control,treated],['control','treated'],[TEAL,PURPLE]):
    ax.hist(values,bins=np.arange(4,36,4),color=colour,edgecolor='white')
    ax.set(title=label,xlabel='Growth (mm)')
axes[0].set_ylabel('Number of plants');save_plot(fig,13,'group-histograms.svg')

fig,axes=plt.subplots(1,3,figsize=(12,4),sharex=True)
for ax,width in zip(axes,[2,4,6]):
    ax.hist(control,bins=np.arange(0,36,width),color=TEAL,edgecolor='white')
    ax.set(title=f'Bin width {width} mm',xlabel='Growth (mm)',xlim=(4,24))
axes[0].set_ylabel('Number of control plants');save_plot(fig,13,'histogram-bins.svg')

# Day 14: the experimental unit is visible in the physical arrangement.
d=Drawing(title='Twelve independently potted plants are twelve units when independently allocated')
for i in range(12):plant(d,95+(i%6)*180,180+(i//6)*190,TEAL if i%2==0 else PURPLE,scale=.8)
d.text(550,475,'Treatment allocated to individual pots',anchor='middle',size=32)
d.save(dest(14,'independent-pots.svg'))

d=Drawing(title='Repeated ruler readings still measure one plant')
plant(d,270,280,label='P01',scale=1.5)
for i in range(6):
    y=70+i*58;d.line(600,y,900,y,BLUE,width=6)
    for j in range(7):d.line(600+50*j,y,600+50*j,y+15,BLUE,width=2)
d.arrow(380,240,550,240)
d.text(740,455,'six readings; one plant',anchor='middle',size=31)
d.save(dest(14,'repeated-readings.svg'))

d=Drawing(title='A shared tray treatment creates a tray-level experimental unit')
for j,label in enumerate(['tray A: control','tray B: treated']):
    x0=35+j*560;d.rect(x0,90,505,305,fill='#f6f0de',stroke='#9a7820')
    for i in range(6):plant(d,x0+80+(i%3)*170,190+(i//3)*125,TEAL if j==0 else PURPLE,scale=.55)
    d.text(x0+250,55,label,size=31,anchor='middle')
d.text(550,465,'Many plants per tray do not create more independently treated trays.',anchor='middle',size=25)
d.save(dest(14,'shared-trays.svg'))

rng=random.Random(14)
pop=control+treated
samples4=[statistics.mean(rng.choices(pop,k=4)) for _ in range(400)]
samples16=[statistics.mean(rng.choices(pop,k=16)) for _ in range(400)]
fig,axes=plt.subplots(1,3,figsize=(12,4),sharex=True)
for ax,vals,title in zip(axes,[pop,samples4,samples16],['Individual values','Means of 4 draws','Means of 16 draws']):
    ax.hist(vals,bins=np.arange(4,34,1.5),color=TEAL,edgecolor='white')
    ax.set(title=title,xlabel='Growth / mean growth (mm)')
axes[0].set_ylabel('Count in this illustration')
save_plot(fig,14,'values-versus-estimates.svg')

# Day 15: briefing figures show the source, report anatomy and a fresh-session test.
d=Drawing(title='Question to observation to interpretation')
plant(d,120,230,label='question',scale=1.2)
d.file(385,150,'data/seedlings.csv',width=190,height=140)
d.file(810,150,'descriptive-report.html',width=190,height=140)
d.arrow(200,210,350,210);d.arrow(610,210,770,210)
d.text(550,420,'One question; measured evidence; explained result',anchor='middle',size=32)
d.save(dest(15,'question-to-report.svg'))

d=Drawing(title='The structure of a short scientific report')
d.rect(240,25,620,445,fill='white',stroke=INK)
for y,label,width in [(85,'Question',400),(150,'Data and methods',500),(215,'Results',400),(390,'Interpretation and limitation',540)]:
    d.text(285,y,label,size=28,weight='bold')
    if y!=390:d.line(285,y+18,285+width,y+18,GREY,width=2)
for i,v in enumerate([0.4,.8,.65,.9,.5,.75]):d.circle(360+i*60,335-v*80,8,fill=TEAL)
d.line(330,350,720,350,INK,width=2)
d.save(dest(15,'report-anatomy.svg'))

d=Drawing(title='Keep the report beside the project and its relative data folder')
d.folder(40,55,'project root',width=280)
d.line(180,155,180,420,INK)
for y,label in [(225,'report.Rmd'),(335,'data/'),(430,'output/')]:
    d.line(180,y-30,390,y-30,INK)
    if label.endswith('/'):d.folder(420,y-70,label,width=260,height=70)
    else:d.file(420,y-85,label,width=175,height=70)
d.text(830,180,'data/seedlings.csv',size=28,anchor='middle')
d.text(830,225,'starts at this project',size=26,anchor='middle')
d.text(830,350,'A personal absolute path',size=25,anchor='middle')
d.text(830,390,'will not move with the folder.',size=25,anchor='middle',fill=RED)
d.save(dest(15,'portable-project.svg'))

d=Drawing(title='A fresh session rebuilds report objects from files')
for x,label in [(65,'saved data'),(455,'saved .Rmd'),(845,'new HTML')]:d.file(x,145,label,width=170,height=130)
d.arrow(250,205,420,205);d.arrow(645,205,810,205)
d.circle(545,365,48,fill='white',stroke=RED)
d.text(545,379,'0',size=42,fill=RED,anchor='middle')
d.text(550,455,'Old console objects are not an input to the report.',anchor='middle',size=28)
d.save(dest(15,'fresh-session.svg'))

# Day 16: allocation, differences and an independence contrast.
d=Drawing(title='Two groups with independent pots and random allocation')
for j,(label,colour) in enumerate([('12 controls',TEAL),('12 treated',PURPLE)]):
    x0=35+j*560
    for i in range(12):plant(d,x0+65+(i%6)*80,150+(i//6)*150,colour,scale=.5)
    d.text(x0+250,400,label,size=33,anchor='middle')
d.text(550,465,'Allocation is part of the study description, not something a sorted table proves.',anchor='middle',size=23)
d.save(dest(16,'randomised-groups.svg'))

fig,ax=plt.subplots(figsize=(10,4))
ax.scatter(means,[1,1],color=[TEAL,PURPLE],s=160)
ax.annotate('',(means[0],.85),(means[1],.85),arrowprops={'arrowstyle':'<->','color':RED,'lw':3})
ax.text(sum(means)/2,.72,f'treated − control = {diff:.2f} mm',ha='center',fontsize=20,color=RED)
for mean,label in zip(means,['control 15.28','treated 21.49']):ax.text(mean,1.12,label,ha='center',fontsize=17)
ax.set(xlim=(10,27),ylim=(.5,1.4),yticks=[],xlabel='Mean seven-day growth (mm)')
save_plot(fig,16,'difference-direction.svg')

d=Drawing(title='Independent groups and repeated measurements are different designs')
plant(d,150,245,TEAL,'P01');plant(d,380,245,PURPLE,'P13')
d.text(265,100,'Different plants',size=33,anchor='middle')
d.line(550,40,550,440,GREY,dashed=True)
plant(d,730,245,TEAL,'L01 before');plant(d,960,245,PURPLE,'L01 after')
d.arrow(800,195,885,195)
d.text(850,100,'Same plant twice',size=33,anchor='middle')
d.text(550,450,'Pairing comes from identities and design, not from two columns.',size=27,anchor='middle')
d.save(dest(16,'independent-or-paired.svg'))

# Day 17: actual CI, actual equal-means reference and a conceptual coverage picture.
fig,ax=plt.subplots(figsize=(10,4))
ax.axvline(0,color=GREY,ls='--',label='zero difference')
ax.errorbar(diff,1,xerr=[[diff-lo],[hi-diff]],fmt='D',color=RED,capsize=12,ms=11,lw=3)
ax.text(diff,1.18,f'estimate {diff:.2f} mm',ha='center',fontsize=20)
ax.text(lo,.75,f'{lo:.2f}',ha='center',fontsize=19);ax.text(hi,.75,f'{hi:.2f}',ha='center',fontsize=19)
ax.set(ylim=(.5,1.5),xlim=(-2,12),yticks=[],xlabel='Treated − control mean growth (mm)')
save_plot(fig,17,'difference-interval.svg')

n1,n0=len(treated),len(control)
v1,v0=statistics.variance(treated),statistics.variance(control)
se=math.sqrt(v1/n1+v0/n0)
tstat=diff/se
df=(v1/n1+v0/n0)**2/((v1/n1)**2/(n1-1)+(v0/n0)**2/(n0-1))
xs=np.linspace(-5,5,1001)
normalizer=math.exp(math.lgamma((df+1)/2)-math.lgamma(df/2))/math.sqrt(df*math.pi)
y=normalizer*(1+xs*xs/df)**(-(df+1)/2)
fig,ax=plt.subplots(figsize=(10,4))
ax.plot(xs,y,color=INK)
ax.fill_between(xs,y,where=np.abs(xs)>=tstat,color=RED,alpha=.65)
ax.axvline(tstat,color=RED,ls='--');ax.axvline(-tstat,color=RED,ls='--')
ax.set(xlabel='Welch t statistic under an equal-means model',ylabel='Reference density')
ax.text(0,.3,'Both tails count',ha='center',fontsize=21)
ax.text(0,.23,'p ≈ 0.0015',ha='center',fontsize=21,color=RED)
save_plot(fig,17,'null-tail-area.svg')

rng=random.Random(45)
fig,ax=plt.subplots(figsize=(9,5))
truth=6
for i in range(20):
    centre=rng.gauss(truth,1.7);half=1.96*1.7
    covers=centre-half<=truth<=centre+half
    ax.plot([centre-half,centre+half],[i,i],color=TEAL if covers else RED,lw=2)
    ax.scatter(centre,i,color=TEAL if covers else RED,s=18)
ax.axvline(truth,color=INK,ls='--');ax.set(yticks=[],xlabel='Estimated difference (illustrative units)',ylabel='Separate repeated studies',title='A schematic repeated-study illustration')
save_plot(fig,17,'interval-procedure.svg')

fig,axes=plt.subplots(1,2,figsize=(11,4))
for i,values in enumerate([control,treated]):
    axes[0].scatter([i]*len(values),values,color=[TEAL,PURPLE][i],s=45)
axes[0].set(xticks=[0,1],xticklabels=['control','treated'],ylabel='Individual growth (mm)',title='Spread among plants')
axes[1].errorbar(diff,1,xerr=[[diff-lo],[hi-diff]],fmt='D',capsize=10,color=RED,ms=10)
axes[1].axvline(0,color=GREY,ls='--');axes[1].set(yticks=[],xlabel='Mean difference (mm)',title='Uncertainty in a difference',xlim=(-1,11))
save_plot(fig,17,'spread-versus-interval.svg')

# Day 18: identity, actual before/after values, subtraction, and order limitation.
d=Drawing(title='Match observations by plant identifier even when row order changes')
left=['L01','L02','L03'];right=['L03','L01','L02']
for i,label in enumerate(left):
    y=100+i*125;d.circle(240,y,34,fill=TEAL);d.text(240,y+9,label,size=22,fill='white',anchor='middle')
    j=right.index(label);d.arrow(285,y,780,100+j*125,stroke=TEAL)
for i,label in enumerate(right):
    y=100+i*125;d.circle(825,y,34,fill=PURPLE);d.text(825,y+9,label,size=22,fill='white',anchor='middle')
d.text(240,440,'before',anchor='middle',size=32);d.text(825,440,'after',anchor='middle',size=32)
d.save(dest(18,'match-identities.svg'))

fig,ax=plt.subplots(figsize=(10,4))
for b,a in zip(before,after):ax.plot([0,1],[b,a],marker='o',color=TEAL,alpha=.8)
ax.set(xticks=[0,1],xticklabels=['Before','After'],ylabel='Photosynthesis rate (µmol CO₂ m⁻² s⁻¹)',xlim=(-.3,1.3))
save_plot(fig,18,'paired-lines.svg')

fig,ax=plt.subplots(figsize=(10,4))
for i in range(3):
    ax.plot([before[i],after[i]],[i,i],color=TEAL,lw=3,marker='o')
    ax.text((before[i]+after[i])/2,i+.16,f'+{after[i]-before[i]:.2f}',ha='center',fontsize=18)
ax.set(yticks=[0,1,2],yticklabels=[r['plant_id'] for r in paired[:3]],ylim=(-.4,2.5),xlabel='Photosynthesis rate (µmol CO₂ m⁻² s⁻¹)')
save_plot(fig,18,'within-plant-change.svg')

d=Drawing(title='Light condition and time both change in an ordered before-after study')
for x,label,colour in [(100,'before: lower light',TEAL),(750,'after: higher light',PURPLE)]:
    plant(d,x+120,240,colour,scale=1.2)
    d.text(x+120,350,label,size=27,anchor='middle')
d.arrow(380,200,700,200)
d.text(540,135,'time passes',anchor='middle',size=31,fill=RED)
d.text(550,445,'Without an unchanged-light comparison, change is not isolated to light.',size=25,anchor='middle')
d.save(dest(18,'order-confounding.svg'))

# Day 19: standards, inverse reading and a deliberately pictured dilution.
standards=records('calibration.csv')
c=np.array([float(r['concentration_mg_l']) for r in standards])
a=np.array([float(r['absorbance']) for r in standards])
slope,intercept=np.polyfit(c,a,1)
d=Drawing(title='Known standards establish a scale before measuring an unknown')
for i,concentration in enumerate(c):
    x=60+i*145;d.rect(x,90,75,220,fill='white',stroke=INK,radius=18)
    d.rect(x+5,170,65,135,fill=f'rgb({int(220-15*i)},{int(235-20*i)},240)',stroke='none',radius=12)
    d.text(x+38,360,f'{concentration:g}',anchor='middle',size=28)
d.text(440,420,'Known concentration (mg/L)',anchor='middle',size=30)
d.text(1000,170,'?',anchor='middle',size=70,fill=RED)
d.text(1000,235,'unknown',anchor='middle',size=25)
d.save(dest(19,'standards.svg'))

fig,ax=plt.subplots(figsize=(10,4))
ax.scatter(c,a,color=TEAL,s=60);ax.plot(c,intercept+slope*c,color=BLUE)
unknown=(.520-intercept)/slope
ax.plot([0,unknown,unknown],[.520,.520,0],color=RED,ls='--')
ax.scatter(unknown,.520,color=RED,s=95)
ax.text(.3,.55,'reading 0.520',color=RED,fontsize=17)
ax.text(unknown,.07,f'{unknown:.2f} mg/L',color=RED,fontsize=17,ha='center')
ax.set(xlim=(0,10.5),ylim=(0,.75),xlabel='Known concentration (mg/L)',ylabel='Absorbance')
save_plot(fig,19,'inverse-reading.svg')

fig,ax=plt.subplots(figsize=(10,4))
ax.scatter(c,a,color=TEAL,s=60);ax.plot(c,intercept+slope*c,color=BLUE)
ax.axhline(.9,color=RED,ls='--');ax.text(5,.915,'U3 reading 0.900: above measured standards',ha='center',color=RED,fontsize=16)
ax.axvspan(0,10,color=TEAL,alpha=.06)
ax.set(xlim=(-.5,10.5),ylim=(0,1),xlabel='Known concentration (mg/L)',ylabel='Absorbance')
save_plot(fig,19,'unsupported-reading.svg')

d=Drawing(title='A measured dilution has a stated final volume, not an added solvent volume')
d.rect(125,150,130,200,fill='#b8dfe6',stroke=TEAL,radius=18)
d.text(190,110,'original',anchor='middle',size=30)
d.text(190,405,'take 1.00 mL',anchor='middle',size=27)
d.arrow(300,240,630,240)
d.text(470,180,'add solvent to',anchor='middle',size=28)
d.rect(730,65,170,330,fill='#e6f3f5',stroke=TEAL,radius=22)
d.text(815,440,'10.00 mL total',anchor='middle',size=29)
d.text(815,250,'diluted',anchor='middle',size=28)
d.save(dest(19,'dilution.svg'))

# Day 20: leaf area as a measured property; slope, sensitivity and extrapolation.
leaves=records('leaf-mass.csv')
areas=np.array([float(r['leaf_area_cm2']) for r in leaves]);masses=np.array([float(r['dry_mass_mg']) for r in leaves])
leaf_slope,leaf_intercept=np.polyfit(areas,masses,1)
d=Drawing(title='One leaf from each of eighteen independent plants')
for j,scale in enumerate([.65,1,1.35]):
    x=190+j*350;y=245
    d.path(f'M{x},{y+100*scale} Q{x-120*scale},{y-10*scale} {x},{y-130*scale} Q{x+120*scale},{y-10*scale} {x},{y+100*scale}',fill='#b8d9b3',stroke=TEAL,width=3)
    d.line(x,y+100*scale,x,y-100*scale,TEAL,width=3)
    d.text(x,440,'one different plant',size=26,anchor='middle')
d.text(550,55,'Area and dry mass are measured; no treatment was assigned.',size=27,anchor='middle')
d.save(dest(20,'leaf-observations.svg'))

fig,ax=plt.subplots(figsize=(10,4))
ax.scatter(areas,masses,color=TEAL,s=50)
ax.plot(areas,leaf_intercept+leaf_slope*areas,color=BLUE)
x0=8;x1=9;y0=leaf_intercept+leaf_slope*x0;y1=leaf_intercept+leaf_slope*x1
ax.plot([x0,x1,x1],[y0,y0,y1],color=RED,lw=3)
ax.text(8.5,y0-7,'1 cm²',ha='center',color=RED,fontsize=17)
ax.text(9.3,(y0+y1)/2,'4.11 mg',ha='left',color=RED,fontsize=17)
ax.set(xlabel='Leaf area (cm²)',ylabel='Dry mass (mg)')
save_plot(fig,20,'slope-units.svg')

fig,ax=plt.subplots(figsize=(10,4))
ax.scatter(areas,masses,color=TEAL,s=50)
ax.scatter(areas[-1],masses[-1],facecolors='none',edgecolors=RED,s=180,lw=2)
ax.plot(areas,leaf_intercept+leaf_slope*areas,color=BLUE,label='all 18 plants')
s2,b2=np.polyfit(areas[:-1],masses[:-1],1)
ax.plot(areas,b2+s2*areas,color=RED,ls='--',label='labelled sensitivity: omit A18')
ax.set(xlabel='Leaf area (cm²)',ylabel='Dry mass (mg)');ax.legend(fontsize=13)
save_plot(fig,20,'sensitivity.svg')

fig,ax=plt.subplots(figsize=(10,4))
ax.scatter(areas,masses,color=TEAL,s=50)
ax.plot(areas,leaf_intercept+leaf_slope*areas,color=BLUE,lw=2)
ext=np.linspace(max(areas),25,80)
ax.plot(ext,leaf_intercept+leaf_slope*ext,color=RED,ls='--',lw=2)
ax.axvspan(max(areas),25,color=RED,alpha=.08)
ax.text(21,35,'No observations\nin this region',ha='center',fontsize=17,color=RED)
ax.set(xlabel='Leaf area (cm²)',ylabel='Dry mass (mg)',xlim=(0,26))
save_plot(fig,20,'extrapolation.svg')

print('Lecture diagrams rebuilt for days 11–20.')
