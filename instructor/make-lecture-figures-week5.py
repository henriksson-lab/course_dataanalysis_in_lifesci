"""Rebuild the week 5 lecture diagrams and actual-data plots from repo root."""

from pathlib import Path
import csv
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lecture_svg import Drawing, INK, TEAL, PURPLE, RED, BLUE, GREY

os.environ.setdefault("MPLCONFIGDIR", "/tmp/introcomputing-mpl-week5")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def save(drawing, unit, name):
    return drawing.save(ROOT / "lectures" / unit / name)


def computer(d, x, y, name, colour=TEAL):
    d.rect(x, y, 360, 210, fill="#f8fafc", stroke=colour)
    d.line(x+180, y+210, x+180, y+250, colour, 8)
    d.line(x+100, y+250, x+260, y+250, colour, 8)
    d.text(x+180, y-20, name, anchor="middle", weight="bold")


u = "21-remote-workflow"
d = Drawing(title="Separate projects on a laptop and remote computer")
computer(d, 50, 85, "Your laptop")
computer(d, 690, 85, "Remote computer", PURPLE)
d.folder(105, 155, "course project", width=250)
d.folder(745, 155, "course project", width=250)
d.text(230, 390, "local files", anchor="middle", fill=TEAL)
d.text(870, 390, "remote files", anchor="middle", fill=PURPLE)
d.line(550, 30, 550, 450, dashed=True)
save(d, u, "two-computers.svg")

d = Drawing(title="SSH and remote desktop are two interfaces to a remote environment")
computer(d, 650, 120, "Remote environment", PURPLE)
d.folder(700, 190, "designated files", width=260)
d.rect(45, 70, 300, 115, fill="#eef2ff", stroke=BLUE)
d.text(75, 115, "SSH terminal", weight="bold")
d.text(75, 155, "$ pwd", size=25)
d.rect(45, 295, 300, 115, fill="#e6f3f5")
d.folder(65, 325, "Remote desktop", width=260, height=65)
d.arrow(355, 125, 625, 205, BLUE)
d.arrow(355, 350, 625, 260, TEAL)
d.text(455, 465, "Interfaces are not automatic file transfer", size=26, anchor="middle")
save(d, u, "two-interfaces.svg")

d = Drawing(title="Closing a session does not remove saved files")
d.rect(60, 80, 300, 230, fill="#f1f5f9", stroke=GREY)
d.text(90, 130, "SSH session", weight="bold")
d.text(90, 190, "$ exit", size=32)
d.line(90, 220, 320, 280, RED, 8)
d.line(320, 220, 90, 280, RED, 8)
d.rect(700, 70, 300, 265, fill="#eef2ff", stroke=BLUE)
d.folder(740, 100, "Saved project", width=220)
d.file(810, 210, "report.Rmd", width=90, height=65)
d.arrow(380, 150, 675, 150)
d.text(520, 120, "save", anchor="middle")
d.arrow(380, 300, 675, 300, PURPLE)
d.text(525, 340, "reconnect + find", anchor="middle", size=23)
d.text(550, 440, "A session and persistent storage have different roles", anchor="middle")
save(d, u, "session-storage.svg")

d = Drawing(title="A transfer creates a separately located copy")
d.file(90, 150, "local report.html")
d.file(825, 150, "remote report.html", fill="#f1eaf8")
d.arrow(300, 220, 785, 220)
d.text(550, 175, "supported upload / download", anchor="middle")
d.text(185, 390, "name the source", anchor="middle", fill=TEAL)
d.text(910, 390, "name the destination", anchor="middle", fill=PURPLE)
d.text(550, 465, "Same filename does not mean the same file", anchor="middle")
save(d, u, "transfer.svg")

d = Drawing(title="Transfer, render remotely, and bring the output back")
for x, label, sub in [(35,"Laptop", "source + data"),(420,"Remote", "render report"),(805,"Laptop", "open output")]:
    d.rect(x, 90, 260, 190, fill="#e6f3f5")
    d.text(x+130, 135, label, anchor="middle", weight="bold")
    d.file(x+85, 165, sub, width=90, height=70)
d.arrow(315, 185, 400, 185)
d.arrow(700, 185, 785, 185)
d.text(355, 340, "transfer in", anchor="middle", size=23)
d.text(745, 340, "transfer out", anchor="middle", size=23)
d.text(550, 435, "Identify the computer and folder at every step", anchor="middle")
save(d, u, "roundtrip.svg")

u = "22-data-representations"
d = Drawing(title="One DNA string, a pixel grid, and a plant observation represent different information")
d.file(70, 110, "DNA text")
d.text(155, 180, "A C G T", anchor="middle", size=24, fill=PURPLE)
for row in range(5):
    for col in range(5):
        shade = "#d2d2d2" if (row-2)**2+(col-2)**2<3 else "#191919"
        d.rect(425+col*34, 125+row*34, 32, 32, fill=shade, stroke="none", radius=0)
d.text(510, 325, "image pixels", anchor="middle")
d.line(865, 275, 865, 145, TEAL, 7)
d.path("M865,195 Q810,130 820,205 Q845,235 865,215", fill="#a7d7b5")
d.path("M865,170 Q925,110 915,185 Q890,205 865,190", fill="#a7d7b5")
d.rect(810, 275, 110, 50, fill="#e8bd8a", stroke="#9a7820", radius=2)
d.text(865, 365, "plant record", anchor="middle")
save(d, u, "representations.svg")

d = Drawing(title="Eight bits make a byte with 256 possible patterns")
for index in range(8):
    d.rect(120+index*105, 100, 90, 100, fill="#eef2ff", stroke=BLUE)
    d.text(165+index*105, 165, str(index%2), anchor="middle", size=36)
d.line(120, 235, 945, 235, BLUE, 4)
d.text(550, 285, "8 bits = 1 byte", anchor="middle", size=33)
d.text(550, 350, "256 patterns can encode values 0–255", anchor="middle")
d.text(550, 415, "The file format tells software what those values mean", anchor="middle", size=24)
save(d, u, "byte.svg")

sequence = (ROOT / "data/dna.txt").read_text().strip()
fig, ax = plt.subplots(figsize=(8.8, 4.1))
ax.bar(list("ACGT"), [sequence.count(base) for base in "ACGT"], color=[TEAL, PURPLE, BLUE, RED])
ax.set(xlabel="Supplied DNA letter", ylabel="Count in the invented sequence", ylim=(0,13))
ax.set_yticks(range(0,14,2)); ax.spines[['top','right']].set_visible(False)
for index, base in enumerate("ACGT"):
    ax.text(index, sequence.count(base)+0.3, str(sequence.count(base)), ha="center", fontsize=14)
fig.tight_layout(); p=ROOT/"lectures"/u/"base-counts.svg"; p.parent.mkdir(parents=True,exist_ok=True); fig.savefig(p); plt.close(fig)

with (ROOT / "data/pixels.csv").open() as handle:
    reader=csv.reader(handle); next(reader); pixels=[[int(x) for x in row] for row in reader]
fig, axes = plt.subplots(1,2,figsize=(10,4.4))
axes[0].axis("off"); table=axes[0].table(cellText=pixels, loc="center", cellLoc="center"); table.auto_set_font_size(False); table.set_fontsize(11); table.scale(1,1.7)
axes[0].set_title("The saved numeric table")
axes[1].imshow(pixels, cmap="gray", vmin=0, vmax=255, interpolation="nearest"); axes[1].set_title("The same values as brightness"); axes[1].set_xticks([]); axes[1].set_yticks([])
fig.tight_layout(); fig.savefig(ROOT/"lectures"/u/"pixels.svg"); plt.close(fig)
fig, axes=plt.subplots(1,2,figsize=(10,4.4))
for ax, threshold in zip(axes,[100,220]):
    mask=[[value>threshold for value in row] for row in pixels]
    ax.imshow(mask, cmap="gray",vmin=0,vmax=1,interpolation="nearest")
    ax.set_title(f"Intensity > {threshold}: {sum(map(sum,mask))} of 64")
    ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig(ROOT/"lectures"/u/"threshold.svg"); plt.close(fig)

u = "23-mini-study"
d = Drawing(title="Choose one study and one report")
d.rect(40, 80, 440, 270, fill="#e6f3f5")
d.path("M200,130 v50 l-65,100 q-10,20 15,20 h125 q25,0 15,-20 l-65,-100 v-50", fill="#d9edf0", width=4)
d.circle(185,255,10,fill="#629b69"); d.circle(235,265,12,fill="#629b69")
d.text(260, 330, "Duckweed biomass", anchor="middle")
d.rect(620,80,440,270,fill="#f1eaf8",stroke=PURPLE)
d.line(840,140,840,275,PURPLE,5); d.line(740,165,940,165,PURPLE,5)
d.path("M735,170 l-45,85 h90 Z",fill="#ded3ef",stroke=PURPLE)
d.path("M945,170 l-45,85 h90 Z",fill="#ded3ef",stroke=PURPLE)
d.text(840,330,"Collected-product yield",anchor="middle")
d.text(550,430,"One question → one analysis → one reproducible report",anchor="middle")
save(d,u,"study-choice.svg")

d = Drawing(title="Count independently assigned flasks and synthesis runs, not internal measurements")
for index in range(4):
    x=110+index*100
    d.path(f'M{x},110 v35 l-30,65 h75 l-30,-65 v-35',fill="#e6f3f5",width=3)
    for j in range(3): d.circle(x+5+j*8,190,4,fill="#529263")
d.text(270,285,"4 flasks",anchor="middle",weight="bold")
d.text(270,335,"many fronds inside each",anchor="middle",size=23)
for index in range(4):
    x=690+index*90
    d.rect(x,125,60,75,fill="#f1eaf8",stroke=PURPLE)
    d.text(x+30,175,str(index+1),anchor="middle",size=25)
d.text(850,285,"4 independent runs",anchor="middle",weight="bold")
d.text(850,335,"repeat weighings stay within a run",anchor="middle",size=23)
d.text(550,445,"The experimental unit follows the design, not the number of readings",anchor="middle",size=24)
save(d,u,"independent-units.svg")

d=Drawing(title="Twenty flasks started; one nutrient biomass measurement is unavailable")
for group,label in enumerate(["Control","Nutrient"]):
    d.text(60,100+group*190,label,weight="bold")
    for index in range(10):
        x=260+index*75; y=70+group*190
        d.rect(x,y,48,65,fill="#e6f3f5",stroke=TEAL,radius=3)
        d.text(x+24,y+100,f"F{group*10+index+1:02d}",anchor="middle",size=17)
        if group==1 and index==6:
            d.line(x,y,x+48,y+65,RED,5); d.line(x+48,y,x,y+65,RED,5)
d.text(550,435,"F17 spilled: 10 + 9 available measurements; never insert zero",anchor="middle",size=25)
save(d,u,"missing-flask.svg")

def dotplot(filename, field, groupfield, groups, unit, ylabel, outname, transform=None):
    with (ROOT/"data"/filename).open() as handle: rows=list(csv.DictReader(handle))
    fig,ax=plt.subplots(figsize=(8.7,4.2))
    for index,group in enumerate(groups):
        values=[transform(row) if transform else float(row[field]) for row in rows if row[groupfield]==group and (transform or row[field])]
        offsets=[((j%5)-2)*0.035 for j in range(len(values))]
        ax.scatter([index+offset for offset in offsets],values,color=[TEAL,PURPLE][index],s=65)
        mean=sum(values)/len(values)
        ax.scatter([index],[mean],marker="D",color=RED,s=95,zorder=5)
    ax.set_xticks(range(len(groups)),groups); ax.set_ylabel(ylabel)
    ax.set_xlim(-0.5,len(groups)-0.5); ax.spines[['top','right']].set_visible(False)
    ax.text(0.5,-0.2,"Dots: independent units. Red diamonds: group means.",transform=ax.transAxes,ha="center",fontsize=11)
    fig.tight_layout(); path=ROOT/"lectures"/unit/outname; path.parent.mkdir(parents=True,exist_ok=True); fig.savefig(path); plt.close(fig)

dotplot("duckweed.csv","biomass_mg","treatment",["control","nutrient"],u,"Dry biomass after seven days (mg)","duckweed.svg")
dotplot("organic-recovery.csv",None,"protocol",["standard","modified"],u,"Isolated product yield (%)","organic-yields.svg",transform=lambda row:100*float(row['isolated_mass_g'])/float(row['theoretical_mass_g']))
d=Drawing(title="Percentage yield is collected mass divided by the supplied maximum")
d.text(75,80,"Y01: theoretical maximum supplied",weight="bold")
d.rect(75,115,850,70,fill="#e2e8f0",stroke=GREY)
d.text(960,160,"1.00 g",size=25)
d.text(75,260,"Dry product collected",weight="bold")
d.rect(75,295,850*0.62,70,fill="#d9caed",stroke=PURPLE)
d.text(640,340,"0.62 g",size=25)
d.text(550,450,"100 × 0.62 / 1.00 = 62% yield",anchor="middle",size=33)
save(d,u,"yield.svg")

u="24-reproduce"
d=Drawing(title="An interactive console object is not automatically available to a report")
d.rect(50,90,330,230,fill="#f1eaf8",stroke=PURPLE)
d.text(215,140,"Interactive R memory",anchor="middle",weight="bold")
d.circle(215,220,50,fill="#d9caed"); d.text(215,230,"table",anchor="middle")
d.file(770,130,"report.Rmd")
d.line(420,220,720,220,stroke=RED,width=5,dashed=True)
d.line(550,180,590,260,RED,7); d.line(590,180,550,260,RED,7)
d.text(550,430,"The report must import data and create its own objects",anchor="middle")
save(d,u,"hidden-state.svg")

d=Drawing(title="Source and data produce a readable report")
d.file(60,100,"data.csv")
d.file(330,100,"report.Rmd",fill="#f1eaf8")
d.arrow(555,180,780,180)
d.text(665,140,"render",anchor="middle")
d.file(835,100,"report.html",fill="#e6f3f5")
d.text(290,400,"Keep inputs + instructions",anchor="middle",weight="bold")
d.text(910,400,"Read the result",anchor="middle",weight="bold")
save(d,u,"source-output.svg")

d=Drawing(title="The share folder contains source, inputs, and output")
d.folder(55,175,"report-share",width=240)
d.line(315,230,395,230); d.line(395,65,395,410)
for y,label in [(60,"introcomputing.Rproj"),(160,"chosen-report.Rmd"),(260,"data/ + dictionary"),(360,"HTML + README")]:
    d.line(395,y+35,455,y+35)
    if label.startswith("data"):
        d.folder(470,y,label,width=400,height=70)
    else:
        d.rect(470,y,490,70,fill="#eef2ff",stroke=BLUE)
        d.text(500,y+45,label,size=27)
save(d,u,"portable-folder.svg")

d=Drawing(title="Windows and Ubuntu copies do not automatically synchronise")
d.folder(80,125,"Windows copy",width=330,height=150)
d.folder(690,125,"Ubuntu copy",width=330,height=150)
d.arrow(440,190,655,190)
d.text(550,145,"copy deliberately",anchor="middle",size=24)
d.text(245,350,"Edit here?",anchor="middle",fill=BLUE)
d.text(850,350,"Recopy before making ZIP",anchor="middle",fill=TEAL)
d.text(550,445,"Return the ZIP to Windows for the native RStudio check",anchor="middle",size=25)
save(d,u,"copies.svg")

d=Drawing(title="Test the whole project from a different folder location")
d.folder(40,150,"Original project",width=280,height=140)
d.file(470,145,"project.zip",width=120,height=130)
d.folder(760,150,"Fresh location",width=300,height=140)
d.arrow(345,210,440,210)
d.arrow(620,210,735,210)
d.text(550,425,"Relative data/ paths still work when the parent path changes",anchor="middle",size=25)
save(d,u,"different-location.svg")

u="25-consolidate"
d=Drawing(title="The laboratory analysis workflow returns to saved and reproducible work")
for index,(label,colour) in enumerate([("Find",TEAL),("Check",PURPLE),("Analyse",BLUE),("Explain",RED),("Reproduce",TEAL)]):
    x=35+index*215
    d.circle(x+90,175,67,fill=colour)
    d.text(x+90,185,str(index+1),anchor="middle",fill="white",size=36)
    d.text(x+90,290,label,anchor="middle",weight="bold",size=25)
    if index<4:d.arrow(x+165,175,x+205,175)
d.path("M980,345 V415 H125 V345",stroke=GREY)
d.text(550,460,"Save the source, inputs, output, and a supported backup",anchor="middle",size=25)
save(d,u,"workflow.svg")

d=Drawing(title="Choose the practice station that addresses your current difficulty")
d.circle(550,95,48,fill=TEAL); d.text(550,104,"You",anchor="middle",fill="white")
for index,(name,sub) in enumerate([("Files","locate + inspect"),("R","repair + rerun"),("Meaning","units + limits"),("Report","render + share")]):
    x=35+index*270
    d.arrow(550,150,x+115,245)
    d.rect(x,260,235,130,fill="#eef2ff",stroke=BLUE)
    d.text(x+117,305,name,anchor="middle",weight="bold")
    d.text(x+117,350,sub,anchor="middle",size=21)
save(d,u,"stations.svg")


# Expanded demonstrations: provenance, controlled changes, and fresh transfer data.
import statistics
import math

u='21-remote-workflow'
d=Drawing(title='A transfer plan specifies both project locations and the evidence checked')
computer(d,45,90,'Source copy',TEAL); computer(d,690,90,'Destination copy',PURPLE)
d.text(225,155,'data/algae.csv',anchor='middle',size=25)
d.text(225,205,'24 rows; A19 unavailable',anchor='middle',size=22)
d.text(870,155,'data/algae.csv',anchor='middle',size=25)
d.text(870,205,'Repeat the content checks',anchor='middle',size=22)
d.arrow(440,190,660,190)
d.text(550,405,'A filename is only one field in the transfer record',anchor='middle',size=25)
save(d,u,'transfer-plan.svg')

def algae_counts(unit,name):
    d=Drawing(title='Twenty-four independent cultures, with one unavailable supplement measurement')
    for group,label in enumerate(['reference: 12 available','supplement: 11 available']):
        d.text(55,60+group*215,label,weight='bold',size=27)
        for index in range(12):
            x=95+index*80;y=90+group*215
            d.path(f'M{x}, {y} v25 l-18,50 h55 l-18,-50 v-25',fill='#e6f3f5',stroke=TEAL,width=3)
            if group==1 and index==6:
                d.line(x-15,y+25,x+33,y+73,RED,5);d.line(x+33,y+25,x-15,y+73,RED,5)
            d.text(x+10,y+112,f'A{group*12+index+1:02d}',anchor='middle',size=17)
    d.text(550,485,'A19 was spilled: an unavailable value is not a zero',anchor='middle',size=23)
    save(d,unit,name)
algae_counts(u,'algae-counts.svg')

d=Drawing(title='Two files can share a filename while containing different versions')
d.file(100,110,'receipt.txt',width=220,height=180)
d.file(780,110,'receipt.txt',width=220,height=180,fill='#f1eaf8')
d.text(210,190,'first revision',anchor='middle',size=25)
d.text(890,190,'second revision',anchor='middle',size=25)
d.line(390,200,690,200,RED,5,dashed=True)
d.text(550,380,'Equal names do not establish equal contents',anchor='middle',size=28)
save(d,u,'same-name-versions.svg')

d=Drawing(title='An unsaved edit and the saved file are different states')
d.rect(65,80,390,220,fill='#f1eaf8',stroke=PURPLE)
d.text(260,130,'Editor buffer',anchor='middle',weight='bold')
d.text(260,195,'second revision',anchor='middle',size=29)
d.file(785,100,'saved receipt.txt',width=180,height=180)
d.text(875,180,'first revision',anchor='middle',size=22)
d.arrow(480,185,750,185);d.text(615,145,'Save?',anchor='middle',size=30)
d.text(550,440,'Read the saved file again before claiming what travelled',anchor='middle',size=24)
save(d,u,'buffer-and-file.svg')

d=Drawing(title='Matching file size is a limited check, not proof of matching content')
for x,label,colour in [(90,'version 1',TEAL),(650,'version 2',PURPLE)]:
    d.rect(x,100,360,130,fill='#f8fafc',stroke=colour)
    d.text(x+180,175,label,anchor='middle',size=36)
    for i in range(9):d.rect(x+i*39,285,34,48,fill='#e6f3f5',stroke=colour,radius=2)
    d.text(x+180,385,'same number of characters',anchor='middle',size=23)
d.text(550,465,'Different contents can occupy the same number of bytes',anchor='middle',size=26)
save(d,u,'size-is-limited.svg')

u='22-data-representations'
changed=list(sequence);changed[0]='G';changed=''.join(changed)
fig,axes=plt.subplots(1,2,figsize=(10.5,4.2),sharey=True)
for ax,text,label in zip(axes,[sequence,changed],['Original','First A changed to G']):
    counts=[text.count(b) for b in 'ACGT']
    ax.bar(list('ACGT'),counts,color=[TEAL,PURPLE,BLUE,RED]);ax.set_title(label)
    ax.set_ylim(0,13);ax.set_xlabel('Base label')
    for i,v in enumerate(counts):ax.text(i,v+.2,str(v),ha='center',fontsize=14)
    ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('Count in the invented string');fig.tight_layout();fig.savefig(ROOT/'lectures'/u/'one-letter-change.svg');plt.close(fig)

fig,ax=plt.subplots(figsize=(9.5,4.1))
ax.barh(['original','one A replaced by G'],[.45,.475],color=[TEAL,PURPLE])
ax.set(xlim=(0,1),xlabel='Fraction of letters labelled G or C')
for y,value in enumerate([.45,.475]):ax.text(value+.025,y,f'{value:.3f}',va='center',fontsize=18)
ax.spines[['top','right']].set_visible(False);fig.tight_layout();fig.savefig(ROOT/'lectures'/u/'gc-fraction.svg');plt.close(fig)

fig,axes=plt.subplots(1,2,figsize=(10.5,4.1))
for ax,matrix,label in zip(axes,[pixels,[[v+30 for v in row] for row in pixels]],['Original: 25 and 210','Add 30: 55 and 240']):
    ax.imshow(matrix,cmap='gray',vmin=0,vmax=255,interpolation='nearest')
    ax.set_title(label);ax.set_xticks([]);ax.set_yticks([])
fig.tight_layout();fig.savefig(ROOT/'lectures'/u/'brightness-shift.svg');plt.close(fig)

thresholds=[0,25,100,209,210,255]
selected=[sum(v>t for row in pixels for v in row) for t in thresholds]
fig,ax=plt.subplots(figsize=(9.8,4.2))
ax.step([0,25,210,255],[64,24,0,0],where='post',color=TEAL,lw=3)
ax.scatter(thresholds,selected,color=PURPLE,s=65,zorder=3)
ax.set(xlabel='Threshold in the strict comparison intensity > threshold',ylabel='Pixels selected',ylim=(-3,70),xlim=(-3,258))
ax.set_xticks([0,25,100,210,255]);ax.set_yticks([0,24,64]);ax.spines[['top','right']].set_visible(False)
fig.tight_layout();fig.savefig(ROOT/'lectures'/u/'threshold-response.svg');plt.close(fig)

d=Drawing(title='One text string and a four-row CSV organise the same four labels differently')
d.file(90,95,'bases.txt',width=250,height=210);d.text(215,205,'ACGT',anchor='middle',size=36)
d.file(735,95,'bases.csv',width=250,height=210,fill='#f1eaf8')
for index,line in enumerate(['position,base','1,A','2,C','3,G','4,T']):d.text(785,145+index*32,line,size=23)
d.text(215,400,'one stored string',anchor='middle',size=27)
d.text(860,400,'four table observations',anchor='middle',size=27)
d.arrow(390,210,685,210);d.text(550,170,'reorganise, not rename',anchor='middle',size=23)
save(d,u,'string-versus-table.svg')

u='23-mini-study'
d=Drawing(title='An analysis claim follows the question and available evidence')
for index,(label,colour) in enumerate([('Question',TEAL),('Unit + data',PURPLE),('Description',BLUE)]):
    x=55+index*360;d.circle(x+125,165,65,fill=colour)
    d.text(x+125,176,str(index+1),anchor='middle',fill='white',size=36)
    d.text(x+125,280,label,anchor='middle',weight='bold')
    if index<2:d.arrow(x+210,165,x+285,165)
d.line(555,320,555,425,PURPLE,4)
d.text(550,475,'Inference requires the taught model and its assumptions',anchor='middle',size=25)
save(d,u,'claim-sequence.svg')
algae_counts(u,'algae-counts.svg')
with (ROOT/'data/algae.csv').open() as handle: algae=list(csv.DictReader(handle))
ref=[float(r['biomass_mg']) for r in algae if r['treatment']=='reference' and r['biomass_mg']]
sup=[float(r['biomass_mg']) for r in algae if r['treatment']=='supplement' and r['biomass_mg']]
for means,outname in [(False,'algae-observations.svg'),(True,'algae-means.svg')]:
    fig,ax=plt.subplots(figsize=(9,4.3))
    for index,values in enumerate([ref,sup]):
        ax.scatter([index+((j%5)-2)*.035 for j in range(len(values))],values,color=[TEAL,PURPLE][index],s=65)
        if means:ax.scatter([index],[statistics.mean(values)],color=RED,marker='D',s=130,zorder=4)
    ax.set_xticks([0,1],['reference','supplement']);ax.set_ylabel('Dry biomass after seven days (mg)');ax.set_xlim(-.5,1.5)
    ax.spines[['top','right']].set_visible(False);fig.tight_layout();fig.savefig(ROOT/'lectures'/u/outname);plt.close(fig)
fig,ax=plt.subplots(figsize=(9.6,4.2))
correct=statistics.mean(sup);invented=sum(sup)/12
ax.bar(['available measurements','incorrectly inserted zero'],[correct,invented],color=[TEAL,RED])
ax.set_ylabel('Supplement mean biomass (mg)');ax.set_ylim(0,40)
for i,value in enumerate([correct,invented]):ax.text(i,value+.6,f'{value:.2f}',ha='center',fontsize=17)
ax.set_title('A changed number does not replace missing information')
ax.spines[['top','right']].set_visible(False);fig.tight_layout();fig.savefig(ROOT/'lectures'/u/'zero-changes-mean.svg');plt.close(fig)

d=Drawing(title='The same observed difference has opposite signs when comparison order reverses')
d.line(140,245,950,245,INK,4)
for x,label,value,col in [(240,'reference','28.20 mg',TEAL),(860,'supplement','33.92 mg',PURPLE)]:
    d.circle(x,245,17,fill=col);d.text(x,330,label,anchor='middle',size=29);d.text(x,380,value,anchor='middle',size=26)
d.arrow(270,140,830,140,RED);d.text(550,95,'supplement − reference = +5.72 mg',anchor='middle',size=28)
d.arrow(830,440,270,440,BLUE);d.text(550,485,'reference − supplement = −5.72 mg',anchor='middle',size=27)
save(d,u,'comparison-sign.svg')

u='24-reproduce'
d=Drawing(title='Execution success and supported interpretation are separate checks')
d.arrow(210,410,990,410,INK);d.arrow(210,410,210,45,INK)
d.text(700,465,'Interpretation supported?',anchor='middle',size=25)
d.text(155,230,'Runs?',anchor='middle',size=25)
for x,y,label,col in [(425,140,'Runs; supported',TEAL),(825,140,'Runs; misleading',RED),(425,320,'Fails; reasoning may be sound',PURPLE),(825,320,'Fails; unsupported',RED)]:
    d.circle(x,y,28,fill=col);d.text(x,y+60,label,anchor='middle',size=21)
d.text(245,72,'yes',size=20);d.text(245,335,'no',size=20)
d.text(405,395,'yes',size=20);d.text(810,395,'no',size=20)
save(d,u,'runs-versus-valid.svg')

d=Drawing(title='A report path must match the input filename in the received project')
d.file(65,100,'report.Rmd',width=200,height=170)
d.text(165,185,'data/algae.csv',anchor='middle',size=20)
d.file(760,100,'algae-missing.csv',width=220,height=170,fill='#f1eaf8')
d.line(315,180,705,180,RED,5,dashed=True);d.text(510,135,'path mismatch',anchor='middle',fill=RED,size=29)
d.text(550,405,'Restore the copied input name, then verify the result',anchor='middle',size=26)
save(d,u,'missing-file-case.svg')

d=Drawing(title='A report can render a false prose claim successfully')
d.file(60,100,'report.Rmd',width=210,height=190)
d.text(165,180,'wrong sentence',anchor='middle',size=23)
d.arrow(320,200,740,200);d.text(530,150,'render succeeds',anchor='middle',size=28)
d.file(800,100,'report.html',width=210,height=190,fill='#f1eaf8')
d.text(905,180,'wrong sentence',anchor='middle',fill=RED,size=23)
d.text(550,430,'Software execution is not a check of the biological claim',anchor='middle',size=26)
save(d,u,'wrong-prose-renders.svg')

d=Drawing(title='A fresh session and a fresh folder test different dependencies')
d.rect(55,95,425,250,fill='#f1eaf8',stroke=PURPLE)
d.circle(265,185,60,fill=PURPLE);d.text(265,196,'R',anchor='middle',fill='white',size=40)
d.text(265,285,'Fresh session',anchor='middle',weight='bold')
d.rect(620,95,425,250,fill='#e6f3f5');d.folder(725,150,'New location',width=220)
d.text(835,285,'Fresh folder',anchor='middle',weight='bold')
d.text(265,410,'checks hidden memory',anchor='middle',size=24)
d.text(835,410,'checks portable inputs + paths',anchor='middle',size=24)
save(d,u,'two-fresh-checks.svg')

d=Drawing(title='An old HTML file does not update merely because the source was edited')
d.file(70,115,'source revised',width=210,height=180)
d.file(800,115,'old HTML',width=210,height=180,fill='#f1eaf8')
d.text(175,205,'new code',anchor='middle',size=25);d.text(905,205,'old result',anchor='middle',size=25)
d.line(325,205,750,205,RED,5,dashed=True);d.text(540,155,'render not rerun',anchor='middle',size=28)
d.text(550,435,'Check the generated output, not only the editor buffer',anchor='middle',size=26)
save(d,u,'stale-output.svg')

u='25-consolidate'
fig,ax=plt.subplots(figsize=(9.2,4.1))
for index,(values,group) in enumerate([(ref,'reference'),(sup,'supplement')]):
    ax.scatter([index+((j%5)-2)*.035 for j in range(len(values))],values,color=[TEAL,PURPLE][index],s=65)
ax.scatter([0],[41.7],s=220,facecolors='none',edgecolors=RED,lw=2,zorder=5)
ax.annotate('A11: investigate, do not silently delete',xy=(0,41.7),xytext=(.18,43),fontsize=12)
ax.set_xticks([0,1],['reference','supplement']);ax.set_ylabel('Biomass (mg)');ax.set_xlim(-.4,1.55);ax.set_ylim(10,47)
ax.spines[['top','right']].set_visible(False);fig.tight_layout();fig.savefig(ROOT/'lectures'/u/'algae-high-reading.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(9.5,4.2))
primary=statistics.mean(sup)-statistics.mean(ref)
diagnostic_reference=[float(row['biomass_mg']) for row in algae
                      if row['treatment']=='reference' and row['culture_id']!='A11']
diagnostic=statistics.mean(sup)-statistics.mean(diagnostic_reference)
ax.barh(['Primary: all available','Diagnostic: A11 omitted'],[primary,diagnostic],color=[TEAL,RED])
ax.set(xlabel='Observed supplement − reference mean biomass (mg)',xlim=(0,9))
for y,value in enumerate([primary,diagnostic]):ax.text(value+.1,y,f'{value:.2f}',va='center',fontsize=17)
ax.set_title('The diagnostic does not justify replacing the primary analysis');ax.spines[['top','right']].set_visible(False)
fig.tight_layout();fig.savefig(ROOT/'lectures'/u/'sensitivity-check.svg');plt.close(fig)

d=Drawing(title='An unavailable reading and a high recorded reading require different reasoning')
for x,label,sub,col in [(115,'A19','unavailable after spill',RED),(720,'A11','recorded high value',TEAL)]:
    d.path(f'M{x+85},90 v55 l-50,110 h140 l-50,-110 v-55',fill='#e6f3f5',stroke=col,width=4)
    d.text(x+100,330,label,anchor='middle',weight='bold',size=35)
    d.text(x+100,390,sub,anchor='middle',size=25)
d.text(215,190,'?',anchor='middle',size=45,fill=RED)
d.text(820,190,'41.7',anchor='middle',size=30)
d.text(550,475,'Missing is not zero; high is not automatically erroneous',anchor='middle',size=25)
save(d,u,'missing-and-high.svg')
fig,ax=plt.subplots(figsize=(9.5,3.6))
ax.axvline(0,ls='--',color=GREY);ax.errorbar([3],[1],xerr=[[5],[5]],fmt='D',color=PURPLE,ms=12,capsize=10,lw=3)
ax.set(xlim=(-5,11),ylim=(.4,1.6),yticks=[],xlabel='Supplied treatment − control mean difference (mm)')
for x,text,y in [(-2,'−2',.78),(3,'estimate 3',1.22),(8,'8',.78)]:ax.text(x,y,text,ha='center',fontsize=19)
ax.spines[['top','right','left']].set_visible(False);fig.tight_layout();fig.savefig(ROOT/'lectures'/u/'uncertain-interval.svg');plt.close(fig)

d=Drawing(title='A usable handover connects the recipient to source, inputs, and a tested result')
d.rect(35,110,265,230,fill='#e6f3f5');d.text(168,165,'Recipient',anchor='middle',weight='bold')
d.circle(168,225,35,fill=TEAL)
d.file(470,110,'source + data',width=150,height=150)
d.folder(830,130,'Tested project',width=220,height=130)
d.arrow(325,220,445,220);d.arrow(655,220,800,220)
d.text(550,430,'Instructions are usable when another person can follow them',anchor='middle',size=25)
save(d,u,'handover.svg')

print("Built week 5 lecture diagrams and plots in lectures/21–25 directories.")
