---
title: The model is not the hard part
description: Four questions for any medical AI tool, and why answering them takes clinical training more than code.
dek: Notes from my MedAI Summit talk for medical and pharmacy students. Why the hard parts of medical AI are the data, the label and the evaluation, and four questions anyone can ask about an AI tool.
summary: A melanoma AI that learned surgical ink, a cost label that missed need, an alert that is right 16% of the time and a sepsis model that drifted. Four questions anyone can ask about a medical AI tool, and why they are clinical questions.
date: 2026-10-28
topic: Evaluating medical AI
labels: ["MedAI Summit 2026", "Evaluation"]
talk: "<i>The Model Is Not the Hard Part: The Clinical Foundations of Medical AI.</i> 2nd MedAI Summit (online), 28 October 2026. <a href=\"https://magnooj.github.io/medai-summit-2026/\">One-page checklist</a>"
ogImage: /assets/img/blog/model-not-hard-part/og.png
ogImageAlt: "The model is not the hard part: four questions for any medical AI tool, with a chart of how often an alert is right at different prevalences."
disclosure: I work at HOPPR, which builds AI for medical imaging. This post has no product content, and every study in it is independent of my company. The views are my own.
topLinks:
  - { label: "Checklist (PDF)", url: "https://magnooj.github.io/medai-summit-2026/four-questions-checklist.pdf" }
  - { label: "LinkedIn", url: "https://www.linkedin.com/in/magnooj" }
toc:
  - { id: "tldr", n: "·", label: "In short" }
  - { id: "small-box", n: "01", label: "The small box" }
  - { id: "provenance", n: "02", label: "Data provenance" }
  - { id: "label", n: "03", label: "Label definition" }
  - { id: "evaluation", n: "04", label: "Evaluation" }
  - { id: "after-go-live", n: "05", label: "After go-live" }
  - { id: "four-questions", n: "06", label: "The four questions" }
  - { id: "sources", n: "A", label: "Sources" }
---

<div class="tiles">
<div class="tile"><div class="v">84 → 46%</div><div class="l">specificity of a melanoma AI on the same benign moles, without and with surgical ink</div></div>
<div class="tile"><div class="v">46.5%</div><div class="l">Black patients’ share of extra care if a cost-based label were fixed, up from 17.7% (authors’ estimate)</div></div>
<div class="tile"><div class="v">16%</div><div class="l">of alerts are real for a 95% sensitive, 95% specific tool at 1% prevalence</div></div>
<div class="tile"><div class="v">9 → 21%</div><div class="l">of inpatients triggering a sepsis alert each day, before and after COVID-19 arrived</div></div>
</div>

<section id="tldr" class="tldr">
<span class="lbl">In short</span>
<ul>
<li><strong>The model is the small part.</strong> Most of what decides whether a medical AI tool helps patients sits around the model: where the data came from, what the label means and how the tool was evaluated. Those are clinical questions.</li>
<li><strong>Ask where the data came from.</strong> A commercial melanoma AI lost much of its specificity when benign moles carried surgical ink. Dermatologists knew why the ink was there.</li>
<li><strong>Ask what the label really is.</strong> An algorithm predicted healthcare cost instead of need, and at the same score Black patients were considerably sicker.</li>
<li><strong>Ask for the PPV at your prevalence.</strong> A 95% sensitive, 95% specific tool at 1% prevalence is right on about 16% of its alerts.</li>
<li><strong>Ask who watches it after go-live.</strong> When the patients changed, a sepsis model’s daily alert rate more than doubled.</li>
</ul>
</section>

<section id="small-box">

## <span class="n">01</span>The model is the small box

These are the notes from my talk at the 2nd MedAI Summit, given to medical and pharmacy students, most of whom have never written a line of code. I've written them up for anyone who wants the argument without the slides.

When I teach medical students about AI, I see the same pattern. They massively overestimate the model, the algorithm itself, and underestimate everything around it: where the data came from, how the labels were defined, and how the tool was evaluated. I think that's good news for them, because those underestimated parts are exactly where a physician has an edge over a computer-science graduate.

### Two ideas are all the AI you need

First, a model learns from examples that someone labeled. Someone decided the right answer for every training image or record, and that label became the model's reference standard. If the labels are wrong, the model learns the wrong thing.

Second, a model gives a score, and someone picks a cut-off. It works like troponin: the number is continuous, but the decision isn't. Move the cut-off and you trade missed cases for false alarms.

Everything else in this post is clinical.

<figure>
<div class="sysmap" role="img" aria-label="Diagram of a machine-learning system as boxes of different sizes. The model is the smallest box. Data provenance, label definition and evaluation are three of the largest boxes and are where a physician has the edge. The other boxes are data pipelines, infrastructure, integration, monitoring and governance.">
<div class="b edge" style="grid-column:1/4;grid-row:1/3">Data provenance<small>Why the image exists</small></div>
<div class="b ops" style="grid-column:4/7;grid-row:1">Data pipelines</div>
<div class="b ops" style="grid-column:4/7;grid-row:2">Infrastructure</div>
<div class="b edge" style="grid-column:1/3;grid-row:3/5">Label definition<small>Which outcome matters</small></div>
<div class="b model" style="grid-column:3;grid-row:3/5">Model</div>
<div class="b ops" style="grid-column:4/7;grid-row:3">Integration</div>
<div class="b ops" style="grid-column:4/7;grid-row:4">Monitoring</div>
<div class="b edge" style="grid-column:1/5;grid-row:5/7">Evaluation<small>What a PPV means at the bedside</small></div>
<div class="b ops" style="grid-column:5/7;grid-row:5/7">Governance</div>
</div>
<div class="legend"><span><i class="sw-line"></i>where a physician has the edge</span><span><i class="sw-frozen"></i>engineering and operations</span><span><i class="sw-ink"></i>the model</span></div>
<figcaption><b>Figure 1. The model is the small box.</b> In a real machine-learning system, the model code is a small part of the whole. After <a href="https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html">Sculley et al., NeurIPS 2015</a>; the clinical labels are mine.</figcaption>
</figure>

I find it helps to judge an AI tool the way you'd judge a diagnostic test and a drug at the same time. It performs like a test, so you ask about sensitivity, specificity and predictive value. It lives like a drug, so you ask about its ingredients, its indication, its trials and its safety monitoring. That gives four questions.

</section>

<section id="provenance">

## <span class="n">02</span>Data provenance: where did the data come from?

In 2019 a team in Heidelberg tested a commercial melanoma classifier, one already approved as a medical device in Europe, on 130 skin lesions: 107 benign moles and 23 melanomas. Each lesion was shown to the model twice, once clean and once marked with the purple ink surgeons draw around a lesion before excision. Nothing about the moles changed. The model's specificity on benign moles fell from 84% to 46%, and its rate of false alarms more than tripled. Heat maps showed it was looking at the ink, and when the researchers cropped the ink out, performance came back.

<figure>
<div class="hbars" role="img" aria-label="Specificity on benign moles fell from 84 percent unmarked to 46 percent with surgical ink; the false-alarm rate rose from 16 percent to 54 percent.">
<p class="grp">Specificity on benign moles</p>
<div class="r"><span class="t">Unmarked</span><div class="track"><div class="bar" style="width:84%;background:var(--ctx)"></div></div><span class="v">84%</span></div>
<div class="r"><span class="t">Marked with surgical ink</span><div class="track"><div class="bar" style="width:46%;background:var(--emph)"></div></div><span class="v">46%</span></div>
<div class="gap"></div>
<p class="grp">False alarms on the same moles</p>
<div class="r"><span class="t">Unmarked</span><div class="track"><div class="bar" style="width:16%;background:var(--ctx)"></div></div><span class="v">16%</span></div>
<div class="r"><span class="t">Marked with surgical ink</span><div class="track"><div class="bar" style="width:54%;background:var(--emph)"></div></div><span class="v">54%</span></div>
</div>
<div class="legend"><span><i class="sw-ctx"></i>clean photograph</span><span><i class="sw-emph"></i>same mole with surgical ink</span></div>
<figcaption><b>Figure 2. Same moles, different answer.</b> A commercial melanoma classifier on 107 benign moles, photographed without and with surgical ink. Data: <a href="https://doi.org/10.1001/jamadermatol.2019.1735">Winkler et al., JAMA Dermatology 2019</a>.</figcaption>
</figure>

The explanation is clinical. Surgeons mark the lesions that worry them, so the authors suspected that ink was over-represented among the melanomas in the training data. If so, the model learned the surgeon's worry, not the disease. The people who suspected the ink were dermatologists, who know why lesions get marked. Without that context, ink is just pixels.

This isn't a one-off. A model learns whatever separates its positives from its negatives. Pneumonia models have learned [which hospital an X-ray came from](https://doi.org/10.1371/journal.pmed.1002683), because one hospital had far more pneumonia than the others. Dermatology models have [performed worse on darker skin](https://doi.org/10.1126/sciadv.abq6147), and the images used to train them have mostly shown lighter skin. So ask three things about the ingredients. Could it be right for the wrong reason? Who is in the data, and do they look like my patients, the way you'd read a trial's inclusion criteria? And how were the labels made: biopsy and follow-up, or software skimming the report text?

In my own work, most of the effort goes into the data, not the model, and I'm not alone. A study of AI practitioners in high-stakes fields was titled, literally, ["Everyone wants to do the model work, not the data work."](https://doi.org/10.1145/3411764.3445518) The authors described data cascades, problems that compound quietly downstream, and 92% of the practitioners they interviewed had hit at least one.

<div class="callout q"><span class="lbl">Question 1</span><p>Where did the data come from, and do those patients look like mine?</p></div>

</section>

<section id="label">

## <span class="n">03</span>Label definition: what exactly does it predict?

A widely used commercial algorithm helped US health systems choose patients for an extra-care program. The goal was to find the patients who needed help most. But need isn't a column in a database, so the developers predicted something that is: each patient's healthcare cost over the next year. In the US, less is spent on Black patients than on white patients at the same level of illness, partly because of unequal access to care. So at the same risk score, Black patients were considerably sicker. The algorithm predicted cost well. It was answering the wrong question.

<figure>
<div class="flow">
<div class="row"><div class="box"><div class="t1">The goal</div><div class="t2">Find the patients who need extra care most</div></div><div class="side">what the program wanted</div></div>
<div class="conn">“need” isn’t a column in a database, so the developers predicted something that is</div>
<div class="row"><div class="box dark"><div class="t1">The label</div><div class="t2">Each patient’s healthcare cost over the next year</div></div><div class="side">what the model learned</div></div>
<div class="conn">less is spent on Black patients at the same level of illness</div>
<div class="row"><div class="box line"><div class="t1">The result</div><div class="t2">At the same risk score, Black patients were considerably sicker</div></div><div class="side"><span><b>17.7% → 46.5%</b><br>Black patients’ share of the extra help if the bias were removed (authors’ estimate)</span></div></div>
</div>
<figcaption><b>Figure 3. Accurate at predicting cost, answering the wrong question.</b> Changing only the label, to a mix of health and cost, cut one measure of the bias by 84%. Data: <a href="https://doi.org/10.1126/science.aax2342">Obermeyer et al., Science 2019</a>.</figcaption>
</figure>

The authors, led by Ziad Obermeyer, an emergency physician, estimated that removing the bias would raise Black patients' share of the extra help from 17.7% to 46.5%. Working with the manufacturer, they then changed only the label, to a mix of health and cost, and one measure of the bias fell by 84%. The fix was a better clinical question.

Pharmacy students will recognize the pattern. In the [Cardiac Arrhythmia Suppression Trial](https://doi.org/10.1056/NEJM198908103210629), drugs that suppressed the extra beats on the ECG looked excellent on the surrogate, and more patients died. A proxy label is a surrogate endpoint, and surrogates can fail.

A label can also be wrong in a quieter way: it predicts something that doesn't change what the team does. When Michigan Medicine [independently tested the Epic Sepsis Model](https://doi.org/10.1001/jamainternmed.2021.2626) across 38,455 hospitalizations, it measured an AUC of 0.63, against the 0.76 to 0.83 the vendor had reported. The model missed two-thirds of sepsis cases and alerted on 18% of all hospitalizations. Of 2,552 patients with sepsis, it flagged only 183 whom clinicians hadn't already treated in time. An alert that mostly repeats what the team already knows, or stays silent, changes very little.

My fix is to rewrite any vague claim, such as "AI detects sepsis", as a clinical question. Which patients? Predicting what, exactly? Who sees the output? At what moment? And what will they do differently? It's PICO, plus the user and the moment. If nothing changes at the bedside, the model has no indication. I believe the decisions about the label and the moment of use need a clinician in the room, and across the field, many teams still make them without one. That empty seat is where clinicians belong.

<div class="callout q"><span class="lbl">Question 2</span><p>What exactly does it predict, for whom, and who acts on it, when?</p></div>

</section>

<section id="evaluation">

## <span class="n">04</span>Evaluation: what evidence is there beyond accuracy?

Here's a question from the talk. An AI flags inpatients at high risk of a serious adverse drug reaction. It's 95% sensitive and 95% specific, and 1 in 100 patients will have the reaction. When it flags a patient, what's the chance that patient actually has the reaction?

Take 10,000 inpatients. A hundred will have the reaction, and the model catches 95 of them. Of the 9,900 who won't, 5% are flagged anyway: 495 false alarms. So of 590 alerts, 95 are real, about 16%. Five of every six alerts are false. Put the same tool on a ward where 1 in 10 patients react, and the figure rises to about 68%. Same tool, different value.

<figure>
<table class="data">
<thead><tr><th>10,000 inpatients</th><th>AI flags</th><th>AI stays quiet</th></tr></thead>
<tbody>
<tr><td><b>100</b><span>will have the reaction</span></td><td><b>95</b><span>true alerts</span></td><td><b>5</b><span>missed</span></td></tr>
<tr><td><b>9,900</b><span>will not</span></td><td class="hi"><b>495</b><span>false alarms</span></td><td><b>9,405</b><span>correctly quiet</span></td></tr>
</tbody>
</table>
<div class="stack" role="img" aria-label="Of 590 alerts, 95 are true and 495 are false alarms."><div class="s-true" style="flex:95;min-width:64px">95 true</div><div class="s-false" style="flex:495">495 false alarms</div></div>
<p class="stack-note"><span>All 590 alerts</span><span>PPV = 95 ÷ 590 ≈ <b>16%</b> · on a ward where 1 in 10 react ≈ <b>68%</b></span></p>
<figcaption><b>Figure 4. Five of every six alerts are false.</b> A 95% sensitive, 95% specific tool when 1 in 100 patients will have the reaction. Worked example.</figcaption>
</figure>

If your gut said 95%, you're in good company. In a [2014 survey of 61 doctors and students at a Boston-area hospital](https://doi.org/10.1001/jamainternmed.2014.1059), only about a quarter got a version of this question right, and the most common answer was 95%. Many AI papers still lead with accuracy or AUC. Clinical training teaches us to ask for the positive predictive value at our own prevalence, even if few of us can do the arithmetic on the spot, and I believe that habit matters more than any detail of how the model is built.

Regulatory clearance doesn't settle the question either. A drug must show in trials that it works before approval. Most AI devices reach the US market through 510(k) clearance, which shows they are similar to an existing device, not that they help patients. A [review of 130 FDA-cleared AI devices](https://doi.org/10.1038/s41591-021-01312-x) found that 126 had been evaluated only on past data, and none of the 54 high-risk devices had a prospective evaluation.

Drug development already has a language for this gap, and an [older hierarchy from diagnostic imaging](https://doi.org/10.1177/0272989X9101100203) maps onto it well. Accuracy on past data is preclinical. Silent mode, where the model runs live but nobody sees its output, is an early-phase study. A supervised pilot asks whether it changes decisions. A randomized trial asks whether it changes outcomes. Monitoring after go-live is Phase IV. Most AI tools you'll meet are still on the first rung.

The best example I know of a tool that climbed is MASAI, a randomized trial of AI-supported mammography screening in Sweden, where two radiologists normally read every exam. In the AI arm, the exams the AI scored as highest risk got two readers and the rest got one. Among the [first 80,033 women](https://doi.org/10.1016/S1470-2045(23)00298-X), the AI arm found 244 cancers against 203, with a similar number of recalls, and radiologists did 44% fewer reads. The [final results](https://doi.org/10.1016/S0140-6736(25)02464-X), for about 106,000 women, showed AI-supported screening was non-inferior on interval cancers, not proven better, and interval cancers are still a surrogate for deaths. To me, that's what honest evidence looks like.

<div class="callout q"><span class="lbl">Question 3</span><p>What evidence is there beyond accuracy, at my prevalence?</p></div>

</section>

<section id="after-go-live">

## <span class="n">05</span>After go-live: who watches it once it’s in use?

Strong results in testing don't guarantee that a tool will work in a real clinic. Google's diabetic retinopathy AI did well in earlier testing, but when it went into [11 clinics in Thailand](https://doi.org/10.1145/3313831.3376718), more than one in five images were rejected as too low in quality, often because of poor lighting, and slow internet in some clinics delayed results, because the images were sent to the cloud. That's efficacy versus effectiveness, the same gap you know from drug trials.

Then the world changes. In [24 hospitals using the Epic sepsis model](https://doi.org/10.1001/jamanetworkopen.2021.35286), the share of hospitalized patients triggering a sepsis alert each day rose from 9% in the three weeks before each hospital's first COVID-19 case to 21% in the three weeks after, and Michigan paused its sepsis alerts. The study measured alert volume, not accuracy, but the authors suggest dataset shift as a likely cause. Nothing in the code changed; the patients did. Noticing that the patients have changed is a clinical skill too, and I believe clinicians often notice it before any dashboard does.

<figure>
<div class="hbars" role="img" aria-label="Share of hospitalized patients triggering a sepsis alert each day: 9 percent in the three weeks before each hospital’s first COVID-19 case, 21 percent in the three weeks after.">
<p class="grp">Hospitalized patients triggering a sepsis alert each day, 24 hospitals</p>
<div class="r"><span class="t">3 weeks before the first COVID-19 case</span><div class="track"><div class="bar" style="width:36%;background:var(--ctx)"></div></div><span class="v">9%</span></div>
<div class="r"><span class="t">3 weeks after</span><div class="track"><div class="bar" style="width:84%;background:var(--emph)"></div></div><span class="v">21%</span></div>
</div>
<figcaption><b>Figure 5. Same code, different patients.</b> The Epic Sepsis Model as COVID-19 arrived; bars are drawn on a 0 to 25% scale. The study measured alert volume, not accuracy. Data: <a href="https://doi.org/10.1001/jamanetworkopen.2021.35286">Wong et al., JAMA Network Open 2021</a>.</figcaption>
</figure>

Drugs come with a package insert, and so should models. A team at Duke proposed a ["Model Facts" label](https://doi.org/10.1038/s41746-020-0253-3) and published an example for their own sepsis model. It states what the model predicts (sepsis in the next four hours), for whom (adults in their emergency department), and how well it performed, with "TBD" where the evidence doesn't exist yet. Most usefully, it says when not to use it without further testing: in the ICU, after a first episode of sepsis, or at another hospital. And it says plainly that it is not a diagnosis.

<figure>
<div class="insert">
<div class="drug"><p class="hd">Drug package insert</p><ol><li>Indications and usage</li><li>Dosage</li><li>Contraindications</li><li class="w">Warnings</li><li>Clinical studies</li><li>Post-marketing experience</li></ol></div>
<div class="facts"><p class="hd">Model Facts</p><p class="mname">Deep Sepsis · Duke University Hospital · v1.0</p>
<div class="row"><b>Summary</b>Probability of meeting sepsis criteria in the next 4 hours, from EHR data</div>
<div class="row"><b>For whom, when</b>Adults in the emergency department; a new score every hour</div>
<div class="row"><b>Validation</b>Past Duke data: AUC 0.88 · later Duke data: 0.94 · live use: <span class="tbd">TBD</span> · other hospitals: <span class="tbd">TBD</span></div>
<div class="row"><b>Warnings</b>Without further evaluation, do not use in the ICU, after a first sepsis episode, or at other hospitals · not a diagnosis</div>
</div>
</div>
<figcaption><b>Figure 6. Every model needs a package insert.</b> Adapted from <a href="https://doi.org/10.1038/s41746-020-0253-3">Sendak et al., npj Digital Medicine 2020</a>, Fig. 1 (CC BY 4.0).</figcaption>
</figure>

<div class="callout q"><span class="lbl">Question 4</span><p>Who watches it once it’s in use?</p></div>

</section>

<section id="four-questions">

## <span class="n">06</span>Four questions for any medical AI tool

<ol class="num-list">
<li><strong>Data provenance.</strong> Where did the data come from, and do those patients look like mine?<span class="an">Like a drug’s ingredients and trial population</span></li>
<li><strong>Label definition.</strong> What exactly does it predict, and who acts on it, when?<span class="an">Like a drug’s indication and endpoint</span></li>
<li><strong>Evaluation.</strong> What evidence is there beyond accuracy, at my prevalence?<span class="an">Like a drug’s trial phases</span></li>
<li><strong>After go-live.</strong> Who watches it once it’s in use?<span class="an">Like a package insert and pharmacovigilance</span></li>
</ol>

None of the four is about the model. A computer-science graduate can build the model. I believe the room where the label is chosen needs someone who knows why the image exists, which outcome matters, and what a positive predictive value means at the bedside. If you're a medical or pharmacy student, that empty seat is yours.



</section>

<section id="sources">

## <span class="n">A</span>Sources

<ol class="refs">
  <li>Sculley D, et al. <a href="https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html">Hidden technical debt in machine learning systems.</a> NeurIPS 2015.</li>
  <li>Winkler JK, et al. <a href="https://doi.org/10.1001/jamadermatol.2019.1735">Association between surgical skin markings in dermoscopic images and diagnostic performance of a deep learning convolutional neural network for melanoma recognition.</a> JAMA Dermatol 2019;155:1135-41.</li>
  <li>Zech JR, et al. <a href="https://doi.org/10.1371/journal.pmed.1002683">Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs.</a> PLoS Med 2018;15:e1002683.</li>
  <li>Daneshjou R, et al. <a href="https://doi.org/10.1126/sciadv.abq6147">Disparities in dermatology AI performance on a diverse, curated clinical image set.</a> Sci Adv 2022;8:eabq6147.</li>
  <li>Sambasivan N, et al. <a href="https://doi.org/10.1145/3411764.3445518">"Everyone wants to do the model work, not the data work": data cascades in high-stakes AI.</a> CHI 2021.</li>
  <li>Obermeyer Z, Powers B, Vogeli C, Mullainathan S. <a href="https://doi.org/10.1126/science.aax2342">Dissecting racial bias in an algorithm used to manage the health of populations.</a> Science 2019;366:447-53.</li>
  <li>Cardiac Arrhythmia Suppression Trial (CAST) Investigators. <a href="https://doi.org/10.1056/NEJM198908103210629">Preliminary report: effect of encainide and flecainide on mortality in a randomized trial of arrhythmia suppression after myocardial infarction.</a> N Engl J Med 1989;321:406-12.</li>
  <li>Wong A, et al. <a href="https://doi.org/10.1001/jamainternmed.2021.2626">External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients.</a> JAMA Intern Med 2021;181:1065-70.</li>
  <li>Manrai AK, et al. <a href="https://doi.org/10.1001/jamainternmed.2014.1059">Medicine's uncomfortable relationship with math: calculating positive predictive value.</a> JAMA Intern Med 2014;174:991-3.</li>
  <li>Wu E, et al. <a href="https://doi.org/10.1038/s41591-021-01312-x">How medical AI devices are evaluated: limitations and recommendations from an analysis of FDA approvals.</a> Nat Med 2021;27:582-4.</li>
  <li>Fryback DG, Thornbury JR. <a href="https://doi.org/10.1177/0272989X9101100203">The efficacy of diagnostic imaging.</a> Med Decis Making 1991;11:88-94.</li>
  <li>Lång K, et al. <a href="https://doi.org/10.1016/S1470-2045(23)00298-X">Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study.</a> Lancet Oncol 2023;24:936-44.</li>
  <li>Gommers J, et al. <a href="https://doi.org/10.1016/S0140-6736(25)02464-X">Interval cancer, sensitivity, and specificity comparing AI-supported mammography screening with standard double reading without AI in the MASAI study: a randomised, controlled, non-inferiority, single-blinded, population-based, screening-accuracy trial.</a> Lancet 2026;407:505-14.</li>
  <li>Beede E, et al. <a href="https://doi.org/10.1145/3313831.3376718">A human-centered evaluation of a deep learning system deployed in clinics for the detection of diabetic retinopathy.</a> CHI 2020.</li>
  <li>Wong A, et al. <a href="https://doi.org/10.1001/jamanetworkopen.2021.35286">Quantification of sepsis model alerts in 24 US hospitals before and during the COVID-19 pandemic.</a> JAMA Netw Open 2021;4:e2135286.</li>
  <li>Sendak MP, Gao M, Brajer N, Balu S. <a href="https://doi.org/10.1038/s41746-020-0253-3">Presenting machine learning model information to clinical end users with model facts labels.</a> npj Digit Med 2020;3:41.</li>
</ol>

</section>
