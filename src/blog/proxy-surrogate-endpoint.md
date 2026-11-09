---
title: A proxy label is a surrogate endpoint
description: Clinical prediction models are often trained to reproduce a stand-in for the patient outcome, and medicine has seen such stand-ins fail.
dek: The label that a model learns to predict is often a stand-in for the outcome that patients care about, and medicine has already seen such stand-ins fail. The remedy is to train the model on the clinical outcome itself, within a set time after the prediction, and to count only the predictions made before clinicians act.
summary: In a randomized trial, two antiarrhythmic drugs that suppressed premature heartbeats after myocardial infarction raised mortality, and an algorithm trained to predict healthcare cost underestimated how sick Black patients were. A model should therefore learn the clinical outcome within a set time after the prediction, and be judged only on predictions made before clinicians act.
date: 2026-11-17
topic: Evaluating medical AI
labels: ["Clinical foundations", "Labels"]
series: clinical-foundations
part: 2
ogImage: /assets/img/blog/proxy-surrogate-endpoint/og.png
ogImageAlt: "Title card for A proxy label is a surrogate endpoint, part 2 of a series on the clinical foundations of medical AI, with the subtitle: the label that a model learns is often a stand-in for the patient outcome, and medicine has seen such stand-ins fail. Two panels on the right compare two cases. In a 1989 drug trial, the drugs suppressed the premature beats on the ECG, but 7.7% of patients died on them against 3.0% on placebo. In 2019, an algorithm predicted next year's healthcare cost well but underestimated health need for Black patients. Below the panels is the question: is the label the thing that matters, or a stand-in for it? The author's name, Ali Ganjizadeh, MD, MBA, and the address magnooj.github.io are at the bottom."
disclosure: I work at HOPPR, which builds AI for medical imaging. This post has no product content, and every study in it is independent of my company. The views are my own.
toc:
  - { id: "tldr", n: "·", label: "Take-home messages" }
  - { id: "three-terms", n: "01", label: "Outcome, surrogate, proxy" }
  - { id: "surrogates-fail", n: "02", label: "When a surrogate fails" }
  - { id: "cost-for-need", n: "03", label: "Cost instead of need" }
  - { id: "the-record", n: "04", label: "Labels from billing codes and report text" }
  - { id: "timing", n: "05", label: "Labels recorded after clinicians act" }
  - { id: "clinical-question", n: "06", label: "Write what the model predicts as a clinical question" }
  - { id: "questions", n: "07", label: "Questions to ask about a label" }
  - { id: "label-in-time", n: "08", label: "Choose the outcome and set a time window" }
  - { id: "sources", n: "A", label: "Sources" }
---

<div class="tiles">
<div class="tile"><div class="v">7.7% vs 3.0%</div><div class="l">mortality on encainide or flecainide versus placebo after myocardial infarction, although the drugs had suppressed the premature beats</div></div>
<div class="tile"><div class="v">17.7% vs 46.5%</div><div class="l">share of Black patients automatically selected for extra care by a cost-based algorithm, and the authors’ estimate if its bias were removed</div></div>
<div class="tile"><div class="v">0.47</div><div class="l">AUC of a widely used sepsis model, counting only predictions made before clinicians acted (0.5 is chance)</div></div>
</div>

<section id="tldr" class="tldr">
<span class="lbl">Take-home messages</span>
<ul>
<li><strong>A model predicts its label, which may be only a stand-in for the outcome.</strong> The label is the answer that a model is trained to reproduce. If the label is healthcare cost in place of health need, for example, the model predicts cost.</li>
<li><strong>A stand-in can improve while patients do worse.</strong> In a randomized trial after myocardial infarction (heart attack), two antiarrhythmic drugs suppressed premature heartbeats but raised mortality to 7.7%, against 3.0% with placebo. A model trained on a stand-in label can fail in the same way.</li>
<li><strong>Cost is a biased stand-in for health need.</strong> An algorithm selected patients for extra care by predicting their healthcare costs in the following year. Because less is spent on Black patients than on equally sick White patients, it underestimated how sick Black patients were.</li>
<li><strong>Check labels taken from the medical record.</strong> Billing codes for severe sepsis or septic shock found only about a third of the sepsis cases identified by review of medical records. Many labels drawn from keywords in radiology reports were also wrong, so check a sample of labels against the chart or the image before training.</li>
<li><strong>Give the label a time window.</strong> A label recorded after clinicians have acted lets a model look accurate by repeating what the team already knows. Define the label as an outcome within a set time after the prediction, for example sepsis within the next 12 hours, and evaluate only the predictions made before clinicians act.</li>
</ul>
</section>

<section id="three-terms">

## <span class="n">01</span>Outcome, surrogate, proxy

A clinical prediction model exists to support a decision about a patient, so it should predict the outcome on which that decision depends. The model learns about that outcome only through its label. A model is trained on many examples, such as chest X-rays, and each example comes with an answer, for instance whether that X-ray shows a pneumothorax. That answer is the label, and the model learns to reproduce it. If the label records a stand-in for the outcome, the model predicts the stand-in, and its reported accuracy describes the stand-in.

Clinical trials have a precise term for such a stand-in. The [US Food and Drug Administration](https://www.fda.gov/drugs/development-resources/surrogate-endpoint-resources-drug-and-biologic-development) (FDA) defines a surrogate endpoint as “a substitute for a direct measure of how a patient feels, functions, or survives.” That direct measure is the clinical outcome, such as death or stroke. Trials use a surrogate endpoint when the clinical outcome would take a very long time to study. Blood pressure is a validated surrogate endpoint, because many trials showed that lowering it reduces the risk of stroke.

Machine learning uses a third term, the proxy label. A proxy label is whatever the dataset happens to record in place of the outcome, such as next year’s healthcare cost, a billing code or a word in a radiology report. To me, a proxy label is a surrogate endpoint that usually has not been validated.

<figure>
<div class="flow" role="img" aria-label="A chain of three boxes, each one step further from the patient. Clinical outcome: how a patient feels, functions or survives, for example death, stroke or septic shock. Slow to measure, so trials use a stand-in. Surrogate endpoint: expected to predict the outcome, for example premature heartbeats or blood pressure. Outcomes are rarely recorded as clean labels, so models learn what the record holds. Proxy label: what the dataset happens to record, for example next year's cost, a billing code or a word in a report.">
<div class="row"><div class="box line"><div class="t1">Clinical outcome</div><div class="t2">How a patient feels, functions or survives</div></div><div class="side">death, stroke, septic shock</div></div>
<div class="conn">slow to measure, so trials use a stand-in</div>
<div class="row"><div class="box"><div class="t1">Surrogate endpoint</div><div class="t2">Expected to predict the outcome</div></div><div class="side">premature heartbeats, blood pressure</div></div>
<div class="conn">outcomes are rarely recorded as clean labels, so models learn what the record holds</div>
<div class="row"><div class="box dark"><div class="t1">Proxy label</div><div class="t2">What the dataset happens to record</div></div><div class="side">next year’s cost, a billing code, a word in a report</div></div>
</div>
<figcaption><b>Figure 1. From the outcome to the label.</b> Read from top to bottom. Each step is further from the patient and gives a model more room to look accurate while it predicts the wrong thing. Definitions: <a href="https://www.fda.gov/drugs/development-resources/surrogate-endpoint-resources-drug-and-biologic-development">US FDA, Surrogate Endpoint Resources</a>; the bottom row extends the same chain to machine learning.</figcaption>
</figure>

</section>

<section id="surrogates-fail">

## <span class="n">02</span>When a surrogate fails

A surrogate endpoint lets a trial reach an answer sooner, but it is valid only if a treatment’s effect on the surrogate predicts its effect on the clinical outcome. The classic counterexample is the [Cardiac Arrhythmia Suppression Trial](https://doi.org/10.1056/NEJM198908103210629) (CAST), a randomized trial of antiarrhythmic drugs after myocardial infarction. After myocardial infarction, frequent ventricular premature beats were a known risk factor for sudden death, and the drugs encainide and flecainide suppressed them. Patients first took a drug in an open-label phase and were randomized to that drug or placebo only if an ambulatory electrocardiogram (ECG) showed that it suppressed their premature beats. After an average of 10 months, mortality was 7.7% with encainide or flecainide and 3.0% with placebo, and the encainide and flecainide arms were stopped. The surrogate improved, and more patients died.

<figure class="fig-svg" id="fig-ecg">
<svg viewBox="0 0 720 306" role="img" aria-label="Schematic of two ECG strips, not a real recording. Top strip, before the drug: regular beats interrupted by three premature beats, drawn in red, which arrive before the next regular beat is due and look different from the regular beats. Bottom strip, on the drug: regular beats only, because the premature beats are suppressed."><rect x="8" y="50" width="704" height="106" rx="5" style="fill: var(--bg); stroke: var(--rule)"/><rect x="8" y="192" width="704" height="106" rx="5" style="fill: var(--bg); stroke: var(--rule)"/><text x="8" y="34" font-size="23" style="fill: var(--ink)"><tspan font-weight="700">Before the drug:</tspan> frequent <tspan font-weight="700" style="fill: var(--red)">premature beats</tspan></text><text x="8" y="178" font-size="23" style="fill: var(--ink)"><tspan font-weight="700">On the drug:</tspan> premature beats suppressed</text><path d="M 20 120 L 24 120 Q 32 106 40 120 L 48 120 L 51 124 L 56 74 L 61 130 L 64 120 L 74 120 Q 87 96 100 120 L 104 120 L 113 64 L 125 138 L 133 120 Q 150 150 167 120 L 216 120 Q 224 106 232 120 L 240 120 L 243 124 L 248 74 L 253 130 L 256 120 L 266 120 Q 279 96 292 120 L 312 120 Q 320 106 328 120 L 336 120 L 339 124 L 344 74 L 349 130 L 352 120 L 362 120 Q 375 96 388 120 L 392 120 L 401 64 L 413 138 L 421 120 Q 438 150 455 120 L 504 120 Q 512 106 520 120 L 528 120 L 531 124 L 536 74 L 541 130 L 544 120 L 554 120 Q 567 96 580 120 L 584 120 L 593 64 L 605 138 L 613 120 Q 630 150 647 120 L 700 120" fill="none" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round" style="stroke: var(--ink-2)"/><path d="M 104 120 L 113 64 L 125 138 L 133 120 Q 150 150 167 120" fill="none" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" style="stroke: var(--red)"/><path d="M 392 120 L 401 64 L 413 138 L 421 120 Q 438 150 455 120" fill="none" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" style="stroke: var(--red)"/><path d="M 584 120 L 593 64 L 605 138 L 613 120 Q 630 150 647 120" fill="none" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" style="stroke: var(--red)"/><path d="M 20 262 L 24 262 Q 32 248 40 262 L 48 262 L 51 266 L 56 216 L 61 272 L 64 262 L 74 262 Q 87 238 100 262 L 120 262 Q 128 248 136 262 L 144 262 L 147 266 L 152 216 L 157 272 L 160 262 L 170 262 Q 183 238 196 262 L 216 262 Q 224 248 232 262 L 240 262 L 243 266 L 248 216 L 253 272 L 256 262 L 266 262 Q 279 238 292 262 L 312 262 Q 320 248 328 262 L 336 262 L 339 266 L 344 216 L 349 272 L 352 262 L 362 262 Q 375 238 388 262 L 408 262 Q 416 248 424 262 L 432 262 L 435 266 L 440 216 L 445 272 L 448 262 L 458 262 Q 471 238 484 262 L 504 262 Q 512 248 520 262 L 528 262 L 531 266 L 536 216 L 541 272 L 544 262 L 554 262 Q 567 238 580 262 L 600 262 Q 608 248 616 262 L 624 262 L 627 266 L 632 216 L 637 272 L 640 262 L 650 262 Q 663 238 676 262 L 700 262" fill="none" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round" style="stroke: var(--ink-2)"/></svg>
<figcaption><b>Figure 2. The surrogate endpoint in the Cardiac Arrhythmia Suppression Trial.</b> Compare the two strips. The red beats in the top strip are ventricular premature beats. Each one arrives before the next regular beat is due. On the drug, they are suppressed. Only patients whose ambulatory ECG showed this suppression were randomized. Figure 3 shows what happened to mortality. <span class="credit">Schematic, not a real ECG. Drawn from the trial design described by the <a href="https://doi.org/10.1056/NEJM198908103210629">CAST Investigators, NEJM 1989</a>.</span></figcaption>
</figure>

In 1996, [Fleming and DeMets](https://doi.org/10.7326/0003-4819-125-7-199610010-00011) explained why a treatment’s effect on a surrogate so often fails to predict its effect on the outcome. The disease may lead to the outcome through pathways that bypass the surrogate. They considered a second route even more likely, in which the treatment affects the outcome through unintended mechanisms that are independent of the disease. They advised using the clinical outcome in definitive phase 3 trials, the large trials on which approval usually rests, unless the surrogate has already been rigorously validated.

Both routes have a counterpart in medical AI. First, illness can harm a patient without changing the label. A very sick patient with poor access to care generates small bills, so a model that predicts cost rates that patient as low risk. Second, a model can predict the label from features other than the disease. Examples are the way that a hospital codes diagnoses for billing, and a chest drain on the X-ray, which shows that a pneumothorax has already been treated. The next two sections give the evidence for each.

</section>

<section id="cost-for-need">

## <span class="n">03</span>Cost instead of need

Health systems in the US use commercial algorithms to select patients with complex health needs for programs of extra care. In a retrospective study of primary care patients at a large US academic hospital, [Obermeyer and colleagues](https://doi.org/10.1126/science.aax2342) examined one widely used algorithm of this kind. Its input was a year of insurance claims, which are the bills sent to insurers, and its label was each patient’s total medical cost in the following year. It did not use race.

The algorithm was well calibrated, which means that a given risk score corresponded to about the same observed cost in Black and White patients. In the US, however, less money is spent on Black patients at the same level of illness, partly because of unequal access to care. So at the same score, Black patients were considerably sicker. Patients with the very highest scores were chosen for the program automatically. The authors estimated that if Black and White patients with the same score had been equally sick, Black patients would have made up 46.5% of those chosen rather than 17.7%.

<figure>
<div class="versus" role="img" aria-label="Two cases side by side. Drug trial, 1989: the surrogate improved, because the drugs suppressed the premature beats on the ECG, but the outcome worsened, with 7.7% dying on the drugs against 3.0% on placebo. Medical AI, 2019: the proxy, next year's healthcare cost, was predicted well, but the outcome, health need, was underestimated for Black patients. Below both: Is the label the thing that matters, or a stand-in for it?">
<div class="col"><p class="hd">Drug trial · 1989</p>
<p class="ok"><b>Surrogate improved</b>The drugs suppressed the premature beats on the ECG</p>
<p class="bad"><b>Outcome worsened</b>7.7% died on the drugs, 3.0% on placebo</p></div>
<div class="col"><p class="hd">Medical AI · 2019</p>
<p class="ok"><b>Proxy predicted well</b>Next year’s healthcare cost</p>
<p class="bad"><b>Outcome missed</b>Health need, underestimated for Black patients</p></div>
</div>
<p class="versus-ask">Is the label the thing that matters, or a stand-in for it?</p>
<figcaption><b>Figure 3. A proxy label fails in the same way as a surrogate endpoint.</b> In each column, compare the top row, the stand-in, with the bottom row, the outcome that matters to patients. The trial compared 730 patients on encainide or flecainide with 725 on placebo. Data: <a href="https://doi.org/10.1056/NEJM198908103210629">CAST Investigators, NEJM 1989</a>; <a href="https://doi.org/10.1126/science.aax2342">Obermeyer et al., Science 2019</a>.</figcaption>
</figure>

The authors then tested the label itself. On the same data, they trained models with three labels: total cost, avoidable cost from emergency visits and hospitalizations, and the number of chronic conditions that flared up during the year. All three models predicted all three outcomes reasonably well, so accuracy alone could not show which label was right. The choice of label still changed who was selected. Black patients made up 14.1% of the highest-risk group with the total-cost label and 26.7% with the chronic-conditions label. The authors call the choice of label “perhaps the single most important decision made in the development of a prediction algorithm.”

The algorithm’s manufacturer replicated these results on its own data. Working with the authors, it then kept the data, inputs and training the same and changed only the label, to an index that combined predicted health with predicted cost. On the manufacturer’s data, this reduced one measure of the bias by 84%. That measure counted how many more chronic conditions Black patients had than White patients with the same risk score.

</section>

<section id="the-record">

## <span class="n">04</span>Labels from billing codes and report text

Most proxy labels come from the medical record, and every part of the record was created for another purpose. Billing codes, for example, exist for reimbursement. In a retrospective cohort study of adults admitted to 409 US hospitals, [Rhee and colleagues](https://doi.org/10.1001/jama.2017.13836) identified sepsis in two ways. One used clinical criteria applied to data from the electronic health record, and the other used billing codes for severe sepsis or septic shock. The authors checked both methods against a review of medical records in a subset of patients. The sensitivity of a method is the share of true cases that it identifies. It was about 32% for the codes and about 70% for the clinical criteria, although the second estimate was imprecise. Over the six years of the study, sepsis identified by codes rose by about 10% a year, while sepsis by clinical criteria stayed stable. A model trained on these codes is therefore likely to learn coding practice as well as sepsis. Changing coding practice is one cause of dataset shift, also called drift. Dataset shift is a difference between the data that a model was trained on and the data that it is used on.

Radiology reports are the other large source of labels. ChestX-ray14 is a public dataset of 112,120 chest X-rays from the US National Institutes of Health (NIH). Software assigned its labels by searching the reports for keywords, and the dataset’s authors expected the labels to be more than 90% accurate. The positive predictive value of a label is the share of images with that label that truly show the finding. When [Luke Oakden-Rayner](https://doi.org/10.1016/j.acra.2019.10.006), a radiologist, reviewed a sample of the images, most labels had a positive predictive value 10% to 30% lower than the dataset’s documentation reported. For example, most images labeled pneumothorax showed a chest drain, which suggests that the pneumothorax had been treated. A model trained on these labels can [learn to find the drain rather than the air](/blog/the-model-is-the-small-box/#provenance), and so detect the cases that clinicians already know about.

<figure class="fig-svg" id="fig-drain">
<svg viewBox="0 0 720 548" role="img" aria-label="Left: a real frontal chest X-ray from the ChestX-ray14 dataset whose only label is Pneumothorax. Two chest drains enter the chest low on the patient's right side, which is the left side of the image, and run up toward the top of the lung; a line labeled chest drains points to one of them below the lung. Right, a schematic: the report, with the keyword pneumothorax highlighted; software finds the keyword; the label, Pneumothorax. Below: a model can learn to find the drain, not the air."><text x="200.0" y="26" font-size="22" font-weight="700" text-anchor="middle" style="fill: var(--ink-2)">The image</text><text x="580" y="26" font-size="22" font-weight="700" text-anchor="middle" style="fill: var(--ink-2)">The report</text><defs><clipPath id="cxr416-clip"><rect x="0" y="40" width="400" height="400" rx="4"/></clipPath></defs><image href="/assets/img/blog/proxy-surrogate-endpoint/nih-chestxray14-00000416_006.jpg" x="0" y="40" width="400" height="400" clip-path="url(#cxr416-clip)"/><path d="M 38.3 456 L 38.3 396.5" stroke-width="2.5" stroke-linecap="round" style="stroke: var(--sig)"/><text x="8" y="478" font-size="22" font-weight="700" text-anchor="start" style="fill: var(--sig)">chest drains</text><path d="M 408 130 L 424 130" stroke-width="2.5" style="stroke: var(--ink-4)"/><path d="M 434 130 L 422 124 L 422 136 Z" style="fill: var(--ink-4)"/><rect x="440" y="40" width="280" height="182" rx="6" stroke-width="1.5" style="fill: var(--surface); stroke: var(--rule-2)"/><rect x="460" y="58" width="214" height="9" rx="4.5" style="fill: var(--rule)"/><rect x="460" y="80" width="176" height="9" rx="4.5" style="fill: var(--rule)"/><rect x="460" y="166" width="232" height="9" rx="4.5" style="fill: var(--rule)"/><rect x="460" y="188" width="150" height="9" rx="4.5" style="fill: var(--rule)"/><rect x="452" y="104" width="256" height="44" rx="4" style="fill: var(--highlight)"/><text x="580" y="134" font-size="24" font-weight="700" text-anchor="middle" style="fill: var(--ink)">pneumothorax</text><path d="M 480 232 L 480 290" stroke-width="2.5" style="stroke: var(--ink-4)"/><path d="M 480 302 L 474 290 L 486 290 Z" style="fill: var(--ink-4)"/><text x="500" y="260" font-size="22" text-anchor="start" style="fill: var(--ink-3)">software finds</text><text x="500" y="286" font-size="22" text-anchor="start" style="fill: var(--ink-3)">the keyword</text><text x="580" y="336" font-size="22" font-weight="700" text-anchor="middle" style="fill: var(--ink-2)">The label</text><rect x="440" y="348" width="280" height="92" rx="6" style="fill: var(--sig)"/><text x="580" y="403" font-size="26" font-weight="700" text-anchor="middle" style="fill: var(--on-fill)">Pneumothorax</text><text x="360" y="530" font-size="24" font-weight="700" text-anchor="middle" style="fill: var(--red)">A model can learn to find the drain, not the air.</text></svg>
<figcaption><b>Figure 4. A real chest X-ray with the label pneumothorax.</b> Read the panels from left to right. The X-ray comes from ChestX-ray14, and its only label is Pneumothorax. Two chest drains enter the chest low on the patient’s right side, which is the left side of the image. They run up toward the top of the lung. Software found the keyword in the report and turned it into the label. In the radiologist’s review, most images labeled pneumothorax showed a chest drain, which suggests that the pneumothorax had already been treated. <span class="credit">Image: NIH Clinical Center, <a href="https://nihcc.app.box.com/v/ChestXray-NIHCC">ChestX-ray14 dataset</a>, file 00000416_006.png, label Pneumothorax; <a href="https://doi.org/10.1109/CVPR.2017.369">Wang et al., CVPR 2017</a>. Use is unrestricted with attribution, according to the <a href="https://nihcc.app.box.com/v/ChestXray-NIHCC/file/249502714403">dataset FAQ</a>. I added the line and the words “chest drains”. The report and the label are drawn as a schematic, because the dataset’s reports are not public. Review of the labels: <a href="https://doi.org/10.1016/j.acra.2019.10.006">Oakden-Rayner, Academic Radiology 2020</a>. <a href="/assets/img/blog/proxy-surrogate-endpoint/nih-chestxray14-00000416_006.jpg">Open the full-size image</a>.</span></figcaption>
</figure>

At Mayo Clinic I built pipelines that use language models to extract data from clinical reports, so I understand the appeal of report text as a source of labels. But a radiology report is written for the referring clinician. As Oakden-Rayner points out, radiologists often leave out findings that are already known or not relevant to that clinician, so a missing word does not mean a missing finding. A proxy label therefore needs the same validation as a surrogate endpoint. Before training, review a random sample of labels against the chart or the image, and report the sensitivity and positive predictive value of each label.

</section>

<section id="timing">

## <span class="n">05</span>Labels recorded after clinicians act

A model that predicts sepsis is useful only if it warns clinicians before they recognize sepsis themselves. Sepsis is life-threatening organ dysfunction caused by a dysregulated response to infection. The label is often based on formal sepsis criteria, and these may be met only after the team has drawn blood cultures, measured lactate and started antibiotics. A prediction made after the team has acted counts as correct but tells the team nothing new.

The Epic Sepsis Model comes from Epic, a vendor of electronic health records, and it was in use at hundreds of US hospitals. Its performance is usually reported as the AUC, the area under the receiver operating characteristic curve. The AUC is the probability that the model ranks a randomly chosen patient with sepsis above one without; 0.5 is chance and 1.0 is perfect. Epic’s internal documentation had reported an AUC of 0.76 to 0.83. A [2021 external validation at Michigan Medicine](https://doi.org/10.1001/jamainternmed.2021.2626) tested the model outside the setting where it was developed. Across 38,455 hospitalizations, counting only scores made before sepsis onset, the AUC was 0.63. It rose to 0.80 when the authors also counted scores from up to three hours after onset.

Sepsis onset by formal criteria can still come after clinicians have started to act. A 2024 retrospective study by [Kamran and colleagues](https://doi.org/10.1056/AIoa2300032) tested the same model in 77,582 hospitalizations at the University of Michigan. The authors took the first sign of a treatment plan (antibiotics, fluids, a blood culture or a lactate measurement) as the point at which clinicians had recognized sepsis. When they counted all predictions made before sepsis criteria were met, the AUC was 0.62, but some of these predictions came after that recognition. When they counted only the predictions made before recognition, the AUC was 0.47, no better than chance.

<figure class="fig-svg" id="fig-recognition">
<svg viewBox="0 0 720 298" role="img" aria-label="Schematic timeline of one admission, not data. Small squares along the time axis are the model's predictions. Clinicians act, with the first treatment or test for sepsis, before the sepsis criteria are met. A red bar covers only the predictions made before clinicians act. A blue bar covers all predictions made before the sepsis criteria are met, including late predictions made after clinicians acted."><text x="10" y="24" font-size="22" text-anchor="start" style="fill: var(--ink-3)">Predictions counted in each analysis</text><rect x="10" y="38" width="370" height="38" rx="3" style="fill: var(--red)"/><text x="22" y="65" font-size="22" font-weight="700" text-anchor="start" style="fill: var(--on-fill)">Before clinicians act</text><rect x="10" y="94" width="370" height="38" rx="3" style="fill: var(--sig)"/><rect x="380" y="94" width="220" height="38" rx="3" style="fill: var(--sig-3)"/><rect x="380" y="94" width="6" height="38" style="fill: var(--sig-3)"/><text x="22" y="121" font-size="22" font-weight="700" text-anchor="start" style="fill: var(--on-fill)">Before sepsis criteria are met</text><text x="490.0" y="121" font-size="22" font-weight="600" text-anchor="middle" style="fill: var(--ink)">late predictions</text><path d="M 380 34 L 380 196" stroke-width="1.5" stroke-dasharray="5 5" style="stroke: var(--ink-3)"/><path d="M 600 90 L 600 196" stroke-width="1.5" stroke-dasharray="5 5" style="stroke: var(--ink-3)"/><path d="M 10 190 L 698 190" stroke-width="2" style="stroke: var(--ink-3)"/><path d="M 710 190 L 698 184 L 698 196 Z" style="fill: var(--ink-3)"/><rect x="21" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="51" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="81" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="111" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="141" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="171" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="201" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="231" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="261" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="291" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="321" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="351" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="381" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="411" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="441" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="471" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="501" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="531" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><rect x="561" y="166" width="10" height="10" rx="1.5" style="fill: var(--ink-3)"/><text x="10" y="223" font-size="22" text-anchor="start" style="fill: var(--ink-2)">Admission</text><text x="380" y="223" font-size="22" font-weight="700" text-anchor="middle" style="fill: var(--ink)">Clinicians act</text><text x="380" y="250" font-size="22" text-anchor="middle" style="fill: var(--ink-3)">first treatment or test</text><text x="600" y="223" font-size="22" font-weight="700" text-anchor="middle" style="fill: var(--ink)">Sepsis criteria met</text><text x="712" y="288" font-size="22" text-anchor="end" style="fill: var(--ink-3)">time during the admission</text></svg>
<figcaption><b>Figure 5. Which predictions each analysis counted.</b> The timeline shows one admission in which clinicians act before the sepsis criteria are met. Each square is a prediction by the model. The red bar stops when clinicians act. The blue bar also counts the late predictions, made after clinicians acted. The authors took the first antibiotic, fluids, blood culture or lactate measurement as the moment when clinicians acted. Figure 6 gives the AUC of each analysis in the same colors. Each AUC comes from all the hospitalizations in the study, not from one admission. <span class="credit">Schematic, not data; positions are illustrative and not to scale. Order of events from <a href="https://doi.org/10.1056/AIoa2300032">Kamran et al., NEJM AI 2024</a>.</span></figcaption>
</figure>

<figure>
<div class="hbars" role="img" aria-label="AUC of the Epic Sepsis Model at the University of Michigan, which is the probability that the model ranks a patient with sepsis above one without, where 0.5 is chance and 1.0 is perfect. 2021 study, 38,455 hospitalizations: 0.80 when scores up to 3 hours after sepsis onset were also counted, and 0.63 with only scores made before onset. 2024 study, 77,582 hospitalizations: 0.62 with predictions made before sepsis criteria were met, some of them after clinicians acted, and 0.47 with only predictions made before clinicians acted. The cut-off is the last moment at which a prediction still counts. The 0.63 and 0.62 results use similar cut-offs, and only the 0.47 result leaves out every prediction made after clinicians acted.">
<p class="grp">2021 study · 38,455 hospitalizations</p>
<div class="r"><span class="t">Also counting up to 3 hours after onset</span><div class="track"><div class="bar" style="width:80%;background:var(--ctx)"></div></div><span class="v">0.80</span></div>
<div class="r"><span class="t">Only before onset</span><div class="track"><div class="bar" style="width:63%;background:var(--emph)"></div></div><span class="v">0.63</span></div>
<div class="gap"></div>
<p class="grp">2024 study · 77,582 hospitalizations</p>
<div class="r"><span class="t">Before criteria were met, some after clinicians acted</span><div class="track"><div class="bar" style="width:62%;background:var(--ctx)"></div></div><span class="v">0.62</span></div>
<div class="r"><span class="t">Only before clinicians acted</span><div class="track"><div class="bar" style="width:47%;background:var(--emph)"></div></div><span class="v">0.47</span></div>
</div>
<div class="legend"><span><i class="sw-ctx"></i>later cut-off</span><span><i class="sw-emph"></i>earlier cut-off</span></div>
<figcaption><b>Figure 6. Counting late predictions makes the same model look better.</b> The cut-off is the last moment at which a prediction still counts. Compare the two bars within each study: with the later cut-off, the same model scores higher. The 0.63 and 0.62 bars use similar cut-offs (sepsis onset by formal criteria). Only the 0.47 bar leaves out every prediction made after clinicians acted. Each bar is the AUC, the probability that the model ranks a patient with sepsis above one without, on a scale from 0 to 1 where 0.5 is chance. The two studies used different groups of patients and different definitions of sepsis. Data: <a href="https://doi.org/10.1001/jamainternmed.2021.2626">Wong et al., JAMA Internal Medicine 2021</a>; <a href="https://doi.org/10.1056/AIoa2300032">Kamran et al., NEJM AI 2024</a>.</figcaption>
</figure>

</section>

<section id="clinical-question">

## <span class="n">06</span>Write what the model predicts as a clinical question

To avoid these failures, state what the model should predict as a clinical question before any data are labeled. Evidence-based medicine already has a format for this, the [well-built clinical question](https://doi.org/10.7326/ACPJC-1995-123-3-A12). It is known as [PICO](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-03) after its four elements: population (which patients), intervention (what is done), comparison (what is done instead) and outcome (what should change). A model needs two more elements, the user who sees the output and the moment at which that person sees it. Figure 7 applies this format to the vague claim “AI detects sepsis”.

<figure>
<table class="data">
<thead><tr><th>Question</th><th>“AI detects sepsis”, rewritten</th><th>Element</th></tr></thead>
<tbody>
<tr><th scope="row">Which patients?</th><td>Adults on general wards</td><td>Population (P)</td></tr>
<tr><th scope="row">Predicting what?</th><td>Sepsis in the next 12 hours</td><td>Outcome (O)</td></tr>
<tr><th scope="row">Who sees it?</th><td>The rapid-response nurse</td><td>User</td></tr>
<tr><th scope="row">At what moment?</th><td>Before anyone suspects sepsis</td><td>Moment</td></tr>
<tr><th scope="row">What changes?</th><td>A bedside review within 30 minutes</td><td>Intervention versus comparison (I and C)</td></tr>
</tbody>
</table>
<figcaption><b>Figure 7. A vague claim rewritten as a clinical question.</b> Read the middle column from top to bottom: each answer narrows what the model must predict, for whom and when. PICO stands for population, intervention, comparison and outcome; the user and the moment are the two added elements. The answers are an illustration, not a published model.</figcaption>
</figure>

The intervention is what the team does differently because of the output, and the comparison is usual care. If nothing changes at the bedside, there is no clinical situation in which the model should be used, so in the terms of pharmacology it has no indication. These choices need clinical knowledge, and I believe a clinician should help define every label that a clinical model learns.

</section>

<section id="questions">

## <span class="n">07</span>Questions to ask about a label

None of these questions requires programming.

<ol class="num-list">
<li><strong>What exactly is the label?</strong> The variable recorded for each patient, not the name of the disease.<span class="an">Like asking for a trial’s primary endpoint</span></li>
<li><strong>Who or what assigned it?</strong> Chart review, biopsy with follow-up, a billing code, or software that read the report?<span class="an">Like asking how outcomes were adjudicated</span></li>
<li><strong>Is it the outcome or a stand-in?</strong> If a stand-in, has anyone shown that it tracks the outcome in patients like mine?<span class="an">Like asking whether a surrogate endpoint was validated</span></li>
<li><strong>When is it recorded?</strong> Before the clinician acts, or after?<span class="an">Like asking when a trial starts to count outcome events</span></li>
<li><strong>Who sees the output, and what will that person do differently?</strong> If the answer is “nothing”, stop there.<span class="an">Like asking for a drug’s indication</span></li>
</ol>

</section>

<section id="label-in-time">

## <span class="n">08</span>Choose the outcome and set a time window

I believe the fix for a late or indirect label starts with its definition. First, set the moment of prediction, when the model runs and the user sees the output, and give the model only the data available at that moment. Then define the label as the clinical outcome within a set time after that moment, for example sepsis within the next 12 hours. For a patient whose sepsis begins at hour 30 of the admission, a prediction made at hour 20 is then a positive example. A prediction made at hour 10 is a negative example, because sepsis did not begin within the following 12 hours.

<figure class="fig-svg" id="fig-window">
<svg viewBox="0 0 720 284" role="img" aria-label="Schematic of the example in the text, not data. A time axis marks hours 0, 10, 20 and 30 of an admission, and sepsis begins at hour 30. A prediction at hour 10 looks 12 hours ahead, to hour 22, which ends before sepsis begins, so it is a negative example. A prediction at hour 20 looks 12 hours ahead, to hour 32, and sepsis begins inside that window, so it is a positive example."><text x="570" y="26" font-size="22" font-weight="700" text-anchor="middle" style="fill: var(--ink)">Sepsis begins</text><path d="M 210 98 L 210 118 M 210 152 L 210 212" stroke-width="1.5" stroke-dasharray="3 5" style="stroke: var(--rule-2)"/><path d="M 390 180 L 390 212" stroke-width="1.5" stroke-dasharray="3 5" style="stroke: var(--rule-2)"/><text x="30" y="60" font-size="22" style="fill: var(--ink)"><tspan font-weight="700">Prediction at hour 10:</tspan> <tspan font-weight="700" style="fill: var(--ink-3)">negative</tspan></text><rect x="210" y="70" width="216" height="32" rx="3" stroke-width="1.5" style="fill: var(--stone); stroke: var(--rule-2)"/><text x="324.0" y="94" font-size="22" text-anchor="middle" style="fill: var(--ink-2)">next 12 hours</text><circle cx="210" cy="86" r="11" stroke-width="3.5" style="fill: var(--surface); stroke: var(--ink-3)"/><text x="30" y="142" font-size="22" style="fill: var(--ink)"><tspan font-weight="700">Prediction at hour 20:</tspan> <tspan font-weight="700" style="fill: var(--sig)">positive</tspan></text><rect x="390" y="152" width="216" height="32" rx="3" style="fill: var(--sig-2)"/><text x="486.0" y="176" font-size="22" text-anchor="middle" style="fill: var(--sig)">next 12 hours</text><circle cx="390" cy="168" r="11" style="fill: var(--sig)"/><path d="M 570 36 L 570 212" stroke-width="3" style="stroke: var(--ink)"/><path d="M 30 212 L 698 212" stroke-width="2" style="stroke: var(--ink-3)"/><path d="M 710 212 L 698 206 L 698 218 Z" style="fill: var(--ink-3)"/><path d="M 30 206 L 30 218" stroke-width="2" style="stroke: var(--ink-3)"/><text x="30" y="245" font-size="22" text-anchor="middle" style="fill: var(--ink-2)">0</text><path d="M 210 206 L 210 218" stroke-width="2" style="stroke: var(--ink-3)"/><text x="210" y="245" font-size="22" text-anchor="middle" style="fill: var(--ink-2)">10</text><path d="M 390 206 L 390 218" stroke-width="2" style="stroke: var(--ink-3)"/><text x="390" y="245" font-size="22" text-anchor="middle" style="fill: var(--ink-2)">20</text><path d="M 570 206 L 570 218" stroke-width="2" style="stroke: var(--ink-3)"/><text x="570" y="245" font-size="22" text-anchor="middle" style="fill: var(--ink-2)">30</text><text x="712" y="276" font-size="22" text-anchor="end" style="fill: var(--ink-3)">hour of the admission</text></svg>
<figcaption><b>Figure 8. A label defined as sepsis within the next 12 hours.</b> Each bar shows the 12 hours after a prediction. Sepsis begins at hour 30, inside the window of the prediction made at hour 20, so that prediction is a positive example. The window of the prediction made at hour 10 ends at hour 22, before sepsis begins, so that prediction is a negative example. <span class="credit">Schematic of the example in the text, not data.</span></figcaption>
</figure>

Next, evaluate the model only on the predictions made before clinicians act. The cut-off is the first sign that the team has recognized the condition, as in the 2024 sepsis study. Predictions made after that point cannot change care, so they should not count toward the model’s performance. Report the AUC for these early predictions as the main result. Give the AUC over all predictions next to it, so that readers can see how much the usual figure depends on late predictions.

When the label is indirect rather than late, choose the outcome that the decision depends on, not the one that is easiest to count in the record. Examples are health need rather than cost, and a radiologist’s review of the image rather than keywords from the report. If a stand-in cannot be avoided, validate it against that outcome in a sample of patients.

Once the label is right, the next question is how often an alert is correct, and [the next post](/blog/five-of-six-alerts-are-false/) takes it up. [The overview of the series](/blog/the-model-is-not-the-hard-part/) shows how all the posts fit together.

</section>

<section id="sources">

## <span class="n">A</span>Sources

<ol class="refs">
  <li>US Food and Drug Administration. <a href="https://www.fda.gov/drugs/development-resources/surrogate-endpoint-resources-drug-and-biologic-development">Surrogate endpoint resources for drug and biologic development.</a> FDA; 2018. Definitions from the FDA-NIH <a href="https://www.fda.gov/drugs/development-resources/best-resource-taxonomy">BEST Resource</a>.</li>
  <li>Cardiac Arrhythmia Suppression Trial (CAST) Investigators. <a href="https://doi.org/10.1056/NEJM198908103210629">Preliminary report: effect of encainide and flecainide on mortality in a randomized trial of arrhythmia suppression after myocardial infarction.</a> N Engl J Med 1989;321:406-12.</li>
  <li>Fleming TR, DeMets DL. <a href="https://doi.org/10.7326/0003-4819-125-7-199610010-00011">Surrogate end points in clinical trials: are we being misled?</a> Ann Intern Med 1996;125:605-13.</li>
  <li>Obermeyer Z, Powers B, Vogeli C, Mullainathan S. <a href="https://doi.org/10.1126/science.aax2342">Dissecting racial bias in an algorithm used to manage the health of populations.</a> Science 2019;366:447-53.</li>
  <li>Rhee C, et al. <a href="https://doi.org/10.1001/jama.2017.13836">Incidence and trends of sepsis in US hospitals using clinical vs claims data, 2009-2014.</a> JAMA 2017;318:1241-9.</li>
  <li>Oakden-Rayner L. <a href="https://doi.org/10.1016/j.acra.2019.10.006">Exploring large-scale public medical image datasets.</a> Acad Radiol 2020;27:106-12.</li>
  <li>Wong A, et al. <a href="https://doi.org/10.1001/jamainternmed.2021.2626">External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients.</a> JAMA Intern Med 2021;181:1065-70.</li>
  <li>Kamran F, et al. <a href="https://doi.org/10.1056/AIoa2300032">Evaluation of sepsis prediction models before onset of treatment.</a> NEJM AI 2024;1(3):AIoa2300032.</li>
  <li>Richardson WS, Wilson MC, Nishikawa J, Hayward RS. <a href="https://doi.org/10.7326/ACPJC-1995-123-3-A12">The well-built clinical question: a key to evidence-based decisions.</a> ACP J Club 1995;123:A12-3.</li>
  <li>McKenzie JE, et al. <a href="https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-03">Chapter 3: Defining the criteria for including studies and how they will be grouped for the synthesis.</a> In: Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane; 2024.</li>
</ol>

</section>
