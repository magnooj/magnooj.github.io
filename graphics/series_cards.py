"""Card text for the "Clinical foundations of medical AI" series (rendered by series.py).

Each hero card mirrors the matching slide from the MedAI Summit 2026 talk. The
text and numbers match the fact-checked cards.md for each part.
"""
from render import card, pill


def ppv(p, sens=0.95, spec=0.95):
    return sens * p / (sens * p + (1 - spec) * (1 - p))


# ---------- Part 1: the nine tiles ----------
NINE = (
    '<div class="t9">'
    '<div class="g">Data pipelines</div>'
    '<div class="g edge">Data provenance<small>Why each image exists</small></div>'
    '<div class="g">Infrastructure</div>'
    '<div class="g edge">Label definition<small>Which outcome matters, and when</small></div>'
    '<div class="g model"><span>Model</span></div>'
    '<div class="g edge">Evaluation<small>What the numbers mean for your patients</small></div>'
    '<div class="g">Integration</div>'
    '<div class="g">Monitoring</div>'
    '<div class="g">Governance</div>'
    '</div>')
NINE_LEGEND = ('<div class="legend-row"><span><i style="background:var(--accent)"></i>Questions that need clinical knowledge</span>'
               '<span><i style="background:var(--grey);box-shadow:inset 0 0 0 2px var(--ctx)"></i>Engineering and operations</span>'
               '<span><i style="background:var(--ink)"></i>The model</span></div>')

AUC = (
    '<p class="scale-note">AUC: how well the model separates films with and without pneumothorax <span class="nw">(bars run from 0.5 = chance to 1.0 = perfect)</span></p>'
    '<div class="bars compact">'
    '<div><p class="bar-label">All test films</p>'
    '<div class="bar-row"><div class="bar grey-bar" style="width:518px"></div><span class="bar-val">0.87</span></div></div>'
    '<div><p class="bar-label">Pneumothoraces with a chest drain</p>'
    '<div class="bar-row"><div class="bar ink" style="width:616px"></div><span class="bar-val teal">0.94</span></div></div>'
    '<div><p class="bar-label">Pneumothoraces without a chest drain</p>'
    '<div class="bar-row"><div class="bar acc" style="width:378px"></div><span class="bar-val acc">0.77</span></div></div>'
    '</div>'
    '<p class="axis-note" style="margin-top:18px">80% of the pneumothoraces in the test set already had a drain.</p>'
    '<div class="callbox">A chest drain is a common treatment. <b>Films without one were over-represented among the misses.</b></div>')

# ---------- Part 2: surrogate improved, outcome worsened ----------
VERSUS = (
    '<div class="vs">'
    '<div class="case"><p class="hd">Drug trial · 1989</p><div class="pair">'
    '<div class="cell ok"><b><i>✓</i>Surrogate improved</b>The drugs suppressed the premature beats on the ECG</div>'
    '<div class="cell bad"><b><i>!</i>Outcome worsened</b>7.7% died on the drugs, 3.0% on placebo</div></div></div>'
    '<div class="case"><p class="hd">Medical AI · 2019</p><div class="pair">'
    '<div class="cell ok"><b><i>✓</i>Proxy predicted well</b>Next year’s healthcare cost</div>'
    '<div class="cell bad"><b><i>!</i>Outcome missed</b>Health need, underestimated for Black patients</div></div></div>'
    '</div>'
    '<p class="vs-ask">Is the label the thing that matters, or a stand-in for&nbsp;it?</p>')

CHAIN = (
    '<div class="chain3">'
    '<div class="bx line"><p class="t">Clinical outcome</p><p>How a patient feels, functions or survives</p>'
    '<small>e.g. death, stroke, septic shock</small></div>'
    '<p class="cn">slow to measure, so trials use a stand-in</p>'
    '<div class="bx"><p class="t">Surrogate endpoint</p><p>Expected to predict the outcome</p>'
    '<small>e.g. premature heartbeats, blood pressure</small></div>'
    '<p class="cn">outcomes are rarely recorded as clean labels, so models learn what the record holds</p>'
    '<div class="bx bad"><p class="t">Proxy label</p><p>What the dataset happens to record</p>'
    '<small>e.g. next year’s cost, a billing code, a word in a report</small></div>'
    '</div>'
    '<p class="vs-ask">How far is the label from the patient?</p>')

# ---------- Part 3: PPV ----------
PPVGRID = (
    '<p class="pg-top">10,000 inpatients</p>'
    '<div class="pg">'
    '<span></span><p class="ch">Reaction (100)</p><p class="ch">No reaction (9,900)</p>'
    '<p class="rh">AI flags</p><div class="c tp"><b>95</b>true alerts</div><div class="c fp"><b>495</b>false alarms</div>'
    '<p class="rh">AI is quiet</p><div class="c"><b>5</b>missed</div><div class="c"><b>9,405</b>correctly quiet</div>'
    '</div>'
    '<div class="pres"><span class="big">≈ 16%<span class="of">of alerts are true</span></span><span class="eq">PPV = 95 ÷ (95 + 495)</span>'
    '<span class="note teal">On a ward where 1 in 10 react: ≈ 68%</span></div>')

PREV_ROWS = "".join(
    f'<div class="r{" hot" if p <= 0.01 else ""}"><span>{label}{note}</span>'
    f'<div class="tr"><div style="width:{max(ppv(p) * 100, 1.2):.1f}%"></div></div>'
    f'<span class="v">{ppv(p) * 100:.0f}%</span></div>'
    for p, label, note in ((0.001, "1 in 1,000", ""), (0.01, "1 in 100", ""), (0.05, "1 in 20", ""),
                           (0.10, "1 in 10", ""), (0.30, "3 in 10", ""), (0.50, "1 in 2", "<small>Like some test sets</small>")))
PREV = (f'<p class="prev-head">How many patients have it</p><div class="prev">{PREV_ROWS}</div>'
        '<div class="legend-row"><span><i style="background:var(--hot)"></i>Most alerts are false</span>'
        '<span><i style="background:var(--accent)"></i>Half or more are true</span></div>')

# ---------- Part 4: the evidence ladder ----------
LADDER = (
    '<div class="lad-wrap">'
    '<div class="ladstat"><b>126 of 130</b><span>AI devices cleared in the US <span class="nw">(2015 to 2020)</span> evaluated only on past data</span></div>'
    '<div class="lad">'
    '<div class="st red"><span class="flag">Most AI stops here</span><b>Tested on past data</b><span class="d">Images and records from the past</span><span class="ph">Preclinical</span></div>'
    '<div class="st"><b>Silent deployment</b><span class="d">Live patients, output hidden</span><span class="ph">Early phase</span></div>'
    '<div class="st"><b>Supervised pilot</b><span class="d">Does it change decisions?</span><span class="ph">Phase II</span></div>'
    '<div class="st"><b>Randomized trial</b><span class="d">Do patients do better?</span><span class="ph">Phase III</span></div>'
    '<div class="st"><b>Monitoring after launch</b><span class="d">Does it keep working?</span><span class="ph">Phase IV</span></div>'
    '</div></div>')

MASAI = (
    '<div class="stats3 stack">'
    '<div class="s"><b>244 vs 203</b><p>cancers found, first 80,033 women</p><small>Similar detection rate: 6.1 vs 5.1 per 1,000</small></div>'
    '<div class="s teal"><b>44% fewer</b><p>screen reads for radiologists</p><small>46,345 vs 83,231, same 80,033 women</small></div>'
    '<div class="s"><b>0.88</b><p>interval cancer ratio, about 106,000 women</p><small>1.55 vs 1.76 per 1,000: non-inferior, not shown better</small></div>'
    '</div>'
    '<div class="caveat stone"><b>Caveats:</b> interval cancers are a surrogate for deaths · <span class="nw">one product, one country</span></div>')

# ---------- Part 5: integration ----------
INTEG = (
    '<div class="intg"><div class="stat hot"><p class="k">Diabetic eye screening · clinics in Thailand</p>'
    '<p class="big">21%</p><p>of retinal photos rejected as ungradable in the first six months, often because of poor lighting</p>'
    '<small>393 of 1,838 photos</small></div>'
    '<p class="lbl">Three jobs before an imaging model can help a patient</p><div class="jobs">'
    f'<div class="job">{pill(1)}<p>The right images reach the model<small>Sent automatically, so that no one has to remember</small></p></div>'
    f'<div class="job">{pill(2)}<p>The result reaches the clinician in time<small>For a radiologist, before the report is signed</small></p></div>'
    f'<div class="job">{pill(3)}<p>Someone owns re-checking the tool<small>A named person who checks it again after any change in scanner, protocol or patients</small></p></div>'
    '</div></div>')

DRIFT = (
    '<div class="bars">'
    '<div><p class="bar-label">Inpatients triggering a sepsis alert each day · 24 hospitals</p>'
    '<div class="bar-row"><div class="bar ink" style="width:257px"></div><span class="bar-val">9%</span></div>'
    '<p class="axis-note">3 weeks before the first COVID-19 case</p></div>'
    '<div><div class="bar-row"><div class="bar acc" style="width:600px"></div><span class="bar-val acc">21%</span></div>'
    '<p class="axis-note">3 weeks after</p></div>'
    '</div>'
    '<p class="axis-note" style="margin-top:18px">Alert volume, not accuracy.</p>'
    '<div class="callbox"><b>Noticing needs an owner.</b></div>')

CARDS = {
    "1-hero": card(f"{pill(1)} The big idea", "The model is the small box.", NINE + NINE_LEGEND,
                   sub="Three of the tiles need clinical knowledge most.",
                   source="After Sculley D et al., NeurIPS 2015 (Fig. 1). The nine tiles and their clinical labels are my adaptation."),
    "1-b": card(f"{pill(1)} Hidden stratification", "Best on the patients already treated.", AUC,
                sub="A pneumothorax model scored 0.87 overall, but 0.77 on pneumothoraces without a chest drain.",
                source="Oakden-Rayner L et al. Hidden stratification causes clinically meaningful failures in machine learning for medical imaging. ACM CHIL 2020."),
    "2-hero": card(f"{pill(2)} Label definition", "A proxy label is a surrogate endpoint.", VERSUS,
                   sub="Medicine has seen stand-ins fail: in a drug trial in 1989, and in a care algorithm in 2019.",
                   source="CAST Investigators. N Engl J Med 1989;321:406-12 · Obermeyer Z et al. Science 2019;366:447-53"),
    "2-b": card(f"{pill(2)} Outcome to proxy", "The further from the patient, the more can fail.", CHAIN,
                source="Definitions: US Food and Drug Administration, Surrogate Endpoint Resources. The proxy row is mine."),
    "3-hero": card(f"{pill(3)} Evaluation", "Five of every six alerts are false.",
                   PPVGRID + '<p class="footline">Similar question, Boston-area survey: the most common answer was 95%.</p>',
                   sub="An AI flags inpatients at risk of a serious drug reaction. 95% sensitive, 95% specific. 1 in 100 will react.",
                   source="Worked example · Survey: Manrai AK et al. JAMA Intern Med 2014;174:991-3"),
    "3-b": card(f"{pill(3)} Prevalence", "Same tool, different ward.", PREV,
                sub="Share of alerts that are true for one AI tool, 95% sensitive and 95% specific.",
                source="Worked example, rounded · A test set with 47.5% bleeds: Voter AF et al. J Am Coll Radiol 2021"),
    "4-hero": card(f"{pill(4)} Evaluation", "Climb the evidence ladder, like a drug.", LADDER,
                   sub="In one review, almost all cleared AI devices stopped at past data. In drug terms, that’s preclinical.",
                   source="Adapted from Fryback DG, Thornbury JR. Med Decis Making 1991 · Wu E et al. Nat Med 2021;27:582-4"),
    "4-b": card(f"{pill(4)} The randomized rung", "MASAI: AI-supported mammography, randomized.", MASAI, title_cls="md",
                sub="Sweden double-reads every screen. In the AI arm, exams scoring 1 to 9 got one reader; 10 got two.",
                source="Lång K et al. Lancet Oncol 2023;24:936-44 · Gommers J et al. Lancet 2026;407:505-14"),
    "5-hero": card(f"{pill(5)} Integration", "Efficacy is not effectiveness.", INTEG,
                   sub="An accurate eye-screening AI met real clinics in Thailand.",
                   source="Beede E et al. A human-centered evaluation of a deep learning system deployed in clinics for the detection of diabetic retinopathy. CHI 2020."),
    "5-b": card(f"{pill(5)} After go-live", "Same model, different patients.", DRIFT,
                sub="When COVID-19 arrived, the share of inpatients a sepsis model flagged each day more than doubled. The University of Michigan paused the alerts.",
                source="Wong A et al. JAMA Netw Open 2021;4:e2135286"),
}

OG = {
    "the-model-is-the-small-box": (1, "The model is the small box", "Many failures start outside the model, in the training data, the labels and the evaluation, and clinicians are well placed to find them.", NINE),
    "proxy-surrogate-endpoint": (2, "A proxy label is a surrogate endpoint", "The label that a model learns is often a <span class=\"nw\">stand-in</span> for the patient outcome, and medicine has seen such <span class=\"nw\">stand-ins</span> fail.", VERSUS),
    "five-of-six-alerts-are-false": (3, "Five of every six alerts are false", "How often an alert is right depends on how common the condition is, so an accurate tool can be wrong on most of its alerts.", PPVGRID),
    "the-evidence-ladder": (4, "Climb the evidence ladder, like a drug", "Judge the evidence for an AI tool as you would for a drug, from tests on past data to monitoring after launch.", LADDER),
    "efficacy-is-not-effectiveness": (5, "Efficacy is not effectiveness", "Accuracy in a study does not guarantee benefit in everyday care, so every AI tool needs a local owner who monitors it and can switch it off.", INTEG),
}
