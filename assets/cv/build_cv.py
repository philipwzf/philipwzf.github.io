from pathlib import Path
import re, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/pdf/Philip_Wang_CV.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
styles={
 'body':ParagraphStyle('body',fontName='Times-Roman',fontSize=10.5,leading=12.7,spaceAfter=4),
 'small':ParagraphStyle('small',fontName='Times-Roman',fontSize=9.8,leading=11.8,spaceAfter=4),
 'bullet':ParagraphStyle('bullet',fontName='Times-Roman',fontSize=10.5,leading=12.7,leftIndent=10,firstLineIndent=-8,spaceAfter=3),
 'title':ParagraphStyle('title',fontName='Times-Roman',fontSize=26,leading=29,alignment=TA_CENTER,spaceAfter=6),
 'contact':ParagraphStyle('contact',fontName='Times-Roman',fontSize=10,leading=12,alignment=TA_CENTER,spaceAfter=8),
 'section':ParagraphStyle('section',fontName='Times-Bold',fontSize=13,leading=15,spaceBefore=8,spaceAfter=3,keepWithNext=True),
 'role':ParagraphStyle('role',fontName='Times-Roman',fontSize=10.5,leading=12.7,spaceAfter=4,keepWithNext=True),
}
story=[]
def p(t,style='body'): return Paragraph(t,styles[style])
def add(t,style='body'): story.append(p(t,style))
def section(t):
 add(t,'section'); story.append(HRFlowable(width='100%',thickness=.45,color=colors.black,spaceAfter=5))
def row(left,right):
 table=Table([[p(left),p(right)]],colWidths=[366,126],hAlign="LEFT")
 table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
 table._cellvalues[0][1].style=ParagraphStyle('right',parent=styles['body'],alignment=2)
 story.append(table)
def bullet(t): add('&#8226; '+t,'bullet')
def link(url,label):return f'<a href="{url}" color="#24465f">{label}</a>'
add('Zhaofeng (Philip) Wang','title')
add(' | '.join([link('mailto:philipwang2025@u.northwestern.edu','philipwang2025@u.northwestern.edu'),link('https://scholar.google.com/citations?user=DwhK3lMAAAAJ&amp;hl=en','Scholar'),link('https://github.com/philipwzf','GitHub'),link('https://philipwzf.github.io/','Website')]),'contact')
section('Education')
row('<b>Northwestern University</b>, PhD in ECE, <i>Advised by Prof. Qi Zhu</i>','Sept. 2026 - Present')
row('<b>Northwestern University</b>, BA in Mathematics and Psychology','Sept. 2021 - June 2025')
bullet('GPA: 3.9/4.0')
bullet('<b>Relevant Coursework:</b> Probability and Stochastic Processes, Graduate Seminar in Algorithm, Graduate Seminar in Statistical Network Analysis, Probabilistic Graphical Models, Game Theory and Networked Systems')
section('Research Interests')
add('Reinforcement learning, formal methods, and control for safe autonomous systems. I integrate formal verification and control-theoretic tools with learning-based methods to develop safe, interpretable, and scalable embodied agents.')
section('Research Experience')
row('<b>IDEAS Lab, Northwestern University</b>, Evanston, IL','Jan. 2024 - Present')
add('<i>Advised by Prof. Qi Zhu</i>','role')
bullet("Lead a team of five master's and undergraduate students developing <b>ManiGuard</b>, a robotic manipulation safety benchmark with 200 tasks, 1,000 evaluation scenarios, and 8,000 safety-annotated demonstrations; co-developed specification-grounded runtime monitoring to evaluate safety independently of task success.")
bullet('Co-developed <b>SENTINEL</b> (<b>NeurIPS 2026</b>), using temporal logic to evaluate foundation model-based agents across semantic interpretation, planning, and execution, with counterexample feedback for safety improvement.')
bullet('Developed transition-aware reward shaping for <b>Model-Enhanced IRL</b> (<b>L4DC 2026</b>), establishing theoretical guarantees and improving sample efficiency and performance in stochastic MuJoCo and Atari environments.')
bullet('Co-developed <b>belief-based offline RL</b> (<b>ICLR 2026</b>) using transformer-based belief prediction for delay-robust deployment from delay-free data; developed inverse RL methods for delayed demonstrations.')
story.append(Spacer(1,5))
row('<b>Center for Deep Learning, Northwestern University</b>, Evanston, IL','Aug. 2025 - June 2026')
add('<b>Research Assistant</b>, <i>Advised by Prof. Zhaoran Wang</i>','role')
bullet('Proposed a hierarchical latent-token reasoning framework for transformers and empirically validated it on a synthetic dataset with natural language evidence.')
bullet('Created a synthetic two-level generative dataset with explicit latent ground truth for interpretable circuit tracing using a transcoder-based approach.')
bullet('Analyzed circuit formation and token-wise behaviors during training; identified reasoning patterns systematically through circuit clustering.')
story.append(Spacer(1,5))
row('<b>Causal Inference Lab, Northwestern University</b>, Evanston, IL','Mar. 2024 - Aug. 2024')
add('<b>Undergraduate Researcher</b>, <i>Advised by Prof. Zach Wood-Doughty</i>','role')
bullet('Augmented MIMIC-III benchmarks for medical LLMs in collaboration with physicians to prevent shortcut learning when evaluating clinical reasoning across NLP tasks.')
bullet('Fine-tuned transformer models with LoRA, achieving state-of-the-art results on existing benchmarks and demonstrating a more than 30% performance decrease on the augmented dataset.')
bullet('Conducted statistical analysis using scikit-learn to assess consistency across physician annotations and quantify discrepancies between human and LLM annotations.')
section('Teaching Experience')
row('<b>Peer Mentor</b>, CS_474 Probabilistic Graphical Models, Northwestern University','Fall 2024')
row('<b>Academic Advisor</b>, Intensive Law &amp; Trial, Stanford Law School','Summer 2022, 2023')
story.append(PageBreak())
section('Publications <font size="10">(* indicates equal contribution)</font>')
source=(ROOT/'index.html').read_text()
for title,auth,venue,year,arxiv in re.findall(r'<h3>(.*?)</h3>\s*<br>\s*(.*?)\s*<br>\s*<em>(.*?)</em>, (\d{4})\.\s*<br>\s*<a href="(https://arxiv.org/abs/[^\"]+)"',source,re.S):
 auth=html.unescape(auth).replace('<strong><ins>','<b>').replace('</ins></strong>','</b>').replace('∗','*')
 links=link(arxiv,'Paper')
 if title.startswith(('ManiGuard:','SENTINEL:')):
  project='ManiGuard' if title.startswith('ManiGuard:') else 'SENTINEL'
  links+=' | '+link(f'https://nu-ideas-lab.github.io/{project}/','Project')+' | '+link(f'https://github.com/NU-IDEAS-Lab/{project}','Code')
 story.append(KeepTogether([p(f'<b>{title}.</b>','small'),p(auth+'.','small'),p(f'<i>{venue} {year}</i> | {links}','small'),Spacer(1,3)]))
story.append(KeepTogether([p('<b>Towards Rigorously Evaluating Clinical Reasoning in LLMs.</b>','small'),p('Christopher Wong, Divy Kumar*, Amiin Muse*, <b>Philip Wang*</b>, Finn Wintz*, Zach Wood-Doughty.','small')]))
section('Leadership Experience')
row('<b>Treasurer and Competing Attorney &amp; Witness</b>, Northwestern Mock Trial Team','Sept. 2021 - June 2025')
for t in ['Managed a budget of over $50,000; revised the budget structure, reducing student membership fees by 20%.','Placed 8th out of approximately 700 teams at the American Mock Trial Association National Championship Tournament.','Instructed 120 high school students across six ten-day summer sessions at Stanford Law School in mock trial, legal research, public speaking, and argument drafting.']:
 add('&#8226; '+t,'small')
row('<b>Residential Assistant</b>, Northwestern Residential Services','Aug. 2022 - June 2025')
for t in ['Advised 150 residents over three years, supporting community, individual growth, diversity, and well-being.','Connected residents with campus organizations and resources in crises and everyday situations.','Managed community funds and organized biweekly community events.']:
 add('&#8226; '+t,'small')
section('Awards')
for name,date in [('Northwestern Computer Science Department Summer Research Grant','2024'),('Sponsorship to compete in United States Bridge Championships','2024, 2025'),('Award for Excellence in Mathematics by a First-Year Student','2022'),('Selected for US U21 National Bridge Team twice','2019, 2022')]:
 row(name,date)
section('Technologies')
add('<b>Languages:</b> Python, C++, Java, Lean','small')
add('<b>Packages and Frameworks:</b> PyTorch, scikit-learn, OpenCV, OpenAI Gymnasium, Stable Baselines, AI2Thor, BEHAVIOR-1k','small')
def footer(canvas,doc):
 canvas.setFont('Times-Roman',9);canvas.setFillColor(colors.HexColor('#666666'));canvas.drawRightString(558,26,str(doc.page))
doc=SimpleDocTemplate(str(OUT),pagesize=letter,rightMargin=54,leftMargin=54,topMargin=38,bottomMargin=38,title='Zhaofeng (Philip) Wang - Curriculum Vitae',author='Zhaofeng (Philip) Wang')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
