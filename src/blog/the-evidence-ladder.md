---
title: Climb the evidence ladder, like a drug
description: Most medical artificial intelligence devices are cleared because they resemble an older device, and drug development shows what stronger evidence looks like.
dek: On the US Food and Drug Administration's list of AI devices, almost all reached the market because they resemble a device already sold. The phases of drug development give a scale for judging how far the evidence for such a tool has gone, from tests on past data to monitoring after launch.
summary: On the US Food and Drug Administration's list of AI devices, almost all were cleared because they resemble a device already sold. This post uses the phases of drug development as a scale of evidence and shows what silent testing on live patients and a randomized trial look like in practice.
date: 2026-11-24
topic: Evaluating medical AI
labels: ["Clinical foundations", "Evaluation"]
series: clinical-foundations
part: 4
ogImage: /assets/img/blog/the-evidence-ladder/og.png
ogImageAlt: "Title card for Climb the evidence ladder, like a drug, part 4 of a series on the clinical foundations of medical AI, by Ali Ganjizadeh, MD, MBA. Five bars rise like steps, each matched to a phase of drug development: tested on past data (preclinical), marked as the step where most AI stops; silent deployment (early phase); supervised pilot (Phase II); randomized trial (Phase III); and monitoring after launch (Phase IV). A note above the bars says that, of 130 AI devices cleared by the US Food and Drug Administration from 2015 to 2020, 126 were evaluated only on past data."
disclosure: I work at HOPPR, which builds AI for medical imaging. This post has no product content, and every study in it is independent of my company. The views are my own.
toc:
  - { id: "tldr", n: "·", label: "Take-home messages" }
  - { id: "cleared", n: "01", label: "What FDA clearance means" }
  - { id: "ladder", n: "02", label: "A ladder from drug development" }
  - { id: "silent", n: "03", label: "Silent deployment" }
  - { id: "trials", n: "04", label: "Pilots and randomized trials" }
  - { id: "masai", n: "05", label: "A randomized screening trial" }
  - { id: "questions", n: "06", label: "Five questions to ask" }
  - { id: "sources", n: "A", label: "Sources" }
---

<div class="tiles">
<div class="tile"><div class="v">126 of 130</div><div class="l">AI devices cleared by the FDA from 2015 to 2020 were evaluated only on retrospective data, in one review</div></div>
<div class="tile"><div class="v">0.90, then 0.50</div><div class="l">AUC of a model for obstructed kidneys on infants’ ultrasound: on past images, then in silent deployment on new patients</div></div>
<div class="tile"><div class="v">46 of 86</div><div class="l">randomized trials of AI used a detection rate or another accuracy measure as the primary endpoint, in one review</div></div>
</div>

<section id="tldr" class="tldr">
<span class="lbl">Take-home messages</span>
<ul>
<li><strong>Market clearance shows that an AI device resembles an older one.</strong> On the US Food and Drug Administration's list of AI devices, almost all were cleared by comparison with a device already sold. That comparison does not test whether patients do better.</li>
<li><strong>Ask how far the evidence for an AI tool has gone, as you would for a drug.</strong> Accuracy on past data is only the preclinical step, and in one review, 126 of 130 cleared AI devices had stopped there. The higher steps test the tool on live patients with its output hidden, then its effect on decisions, then patient outcomes in a randomized trial, and finally its performance after launch.</li>
<li><strong>Run a model on live patients, with its output hidden, before anyone acts on it.</strong> At one children's hospital, a model did well on past ultrasound images of infants' kidneys but was no better than chance on new infants. The team traced most of the drop to how the new images were stored, before any patient was affected.</li>
<li><strong>A randomized trial can still measure only accuracy.</strong> In a review of randomized trials of AI, just over half were designed mainly to measure a detection rate or a similar accuracy measure. Finding more cases does not show that patients live longer or feel better.</li>
<li><strong>Read a positive trial for what it actually showed.</strong> In a Swedish randomized trial of about 106,000 women, screening with AI support was not worse than standard reading by two radiologists, within a margin set in advance. The trial measured cancers diagnosed between screening rounds rather than deaths. On that measure, it did not show that AI support was better.</li>
</ul>
</section>

<section id="cleared">

## <span class="n">01</span>What FDA clearance means

A clinician who adopts a new tool wants to know whether patients do better with it. For a drug, the US Food and Drug Administration (FDA) says that a company "must have adequate data from two large, controlled clinical trials" before it files to market the drug. The medical AI that FDA regulates, however, is a medical device, and devices follow different rules.

Most AI devices reach the market through [510(k) clearance](https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/premarket-notification-510k). In a 510(k), the company shows that its device is "as safe and effective" as a legally marketed device with the same intended use. FDA calls that older device the predicate. The [De Novo route](https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/de-novo-classification-request) is for a new kind of lower-risk device that has no predicate, and the highest-risk devices need [premarket approval](https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/premarket-approval-pma). Of the 1,614 devices on FDA's [list of AI-enabled devices](https://www.fda.gov/medical-devices/artificial-intelligence-enabled-medical-devices/list-artificial-intelligence-enabled-medical-devices) with decisions up to June 2026, 1,553 (96%) came through 510(k).

FDA reviews every 510(k), but the review compares the new device with the predicate and does not test whether patients do better with it. A Stanford team [reviewed 130 FDA-cleared AI devices](https://doi.org/10.1038/s41591-021-01312-x) from 2015 to 2020. Of these, 126 had been evaluated only on retrospective data, which are images and records that were collected before the study began. None of the 54 high-risk devices had a prospective evaluation, one that follows new patients forward in time.

Whether a device helps patients therefore has to be shown by other studies. For most AI tools, nothing requires anyone to ask that question except the clinician who will use the tool.

</section>

<section id="ladder">

## <span class="n">02</span>A ladder from drug development

Drug development already has a scale for how far the evidence for a treatment has gone. It runs from [preclinical research](https://www.fda.gov/patients/drug-development-process/step-2-preclinical-research) in the lab and in animals, through Phases I to III of [clinical research](https://www.fda.gov/patients/drug-development-process/step-3-clinical-research) in people, to safety monitoring after approval in Phase IV. In FDA's description, Phase II studies "aren't large enough to show whether the drug will be beneficial." Phase III studies enroll 300 to 3,000 people to show whether the drug "offers a treatment benefit to a specific population."

Imaging has a similar scale. In 1991, [Fryback and Thornbury](https://doi.org/10.1177/0272989X9101100203) proposed six levels of efficacy for diagnostic imaging:

1. Technical quality of the images.
2. Diagnostic accuracy, such as sensitivity and specificity.
3. Diagnostic thinking: whether the result changes what the referring physician thinks.
4. Patient management: whether the result changes the plan.
5. Patient outcome.
6. Societal costs and benefits.

They wrote that efficacy at each lower level is "logically necessary, but not sufficient" for efficacy at the levels above it. Many AI papers report their main result as an AUC, the area under the receiver operating characteristic curve (not the pharmacokinetic AUC of drug exposure). The AUC is the probability that the model ranks a randomly chosen patient with the outcome above one without it, so 0.5 is chance and 1.0 is perfect. However high it is, an AUC is a level 2 measure and says nothing yet about levels 3 to 5.

Combining the two scales gives five rungs of evidence for an AI tool (Figure 1). The rungs follow the order of drug development, and Figure 5 shows the highest Fryback level that each rung can reach.

1. **Tested on past data.** The model is run on old images or records whose diagnoses are known. This is preclinical work, and most cleared AI stops here.
2. **Silent deployment.** The model runs on live patients, but its output is hidden from the clinicians and later compared with the diagnoses that those patients receive.
3. **Supervised pilot.** Clinicians see the output in a small, closely watched study of whether it changes their decisions and whether the change is right.
4. **Randomized trial with a patient outcome.** Patients are randomly assigned to care with or without the tool. The trial's main measure is named in advance as the primary endpoint and is an outcome that matters to patients.
5. **Monitoring after launch.** Once the tool affects care, someone checks that it keeps working as the patients and the equipment change.

<figure>
<ol class="ladder" role="img" aria-label="A ladder of five rungs. Rung 1, tested on past data, using images and records from the past, is like preclinical work, and most AI stops here. Rung 2, silent deployment, runs on live patients with the output hidden, like an early-phase study. Rung 3, a supervised pilot, asks whether the output changes decisions, like Phase II. Rung 4, a randomized trial, asks whether patients do better, like Phase III. Rung 5, monitoring after launch, asks whether the tool keeps working, like Phase IV.">
<li style="--s:1"><em>Most AI stops here</em><b>Tested on past data</b>Images and records from the past<span class="ph">Preclinical</span></li>
<li style="--s:2"><b>Silent deployment</b>Live patients, output hidden<span class="ph">Early phase</span></li>
<li style="--s:3"><b>Supervised pilot</b>Does it change decisions?<span class="ph">Phase II</span></li>
<li style="--s:4"><b>Randomized trial</b>Do patients do better?<span class="ph">Phase III</span></li>
<li style="--s:5"><b>Monitoring after launch</b>Does it keep working?<span class="ph">Phase IV</span></li>
</ol>
<figcaption><b>Figure 1. The evidence ladder.</b> The question gets harder at each rung, and the label at the foot of each rung names the phase of drug development that it resembles. Adapted from the six levels of <a href="https://doi.org/10.1177/0272989X9101100203">Fryback and Thornbury, Med Decis Making 1991</a>; the labels for the drug phases are mine.</figcaption>
</figure>

The comparison with drugs is imperfect in two places. First, AI has no real equivalent of a drug's first doses in people. Silent deployment is closer to validating a new laboratory assay in parallel with the current one. Second, a drug molecule does not change after approval, whereas the patients, scanners and protocols around a model change all the time. Therefore I believe the top rung matters even more for AI than for drugs.

</section>

<section id="silent">

## <span class="n">03</span>Silent deployment

Silent deployment tests whether a model works on a site's own patients and equipment before anyone relies on it. At the Hospital for Sick Children in Toronto, a pediatric urology team built a model for infants with hydronephrosis, a swelling of the kidney caused by poor urinary drainage. The model reads ultrasound images of the kidney and predicts whether it is obstructed. Its AUC was 0.90 on held-out images, the part of the original dataset that had been kept aside from training.

From August to December 2020, the team [ran the model in silent deployment](https://doi.org/10.3389/fdgth.2022.929508), which they called a silent trial. Clinicians managed the infants as usual and never saw the predictions, which a separate research team recorded (Figure 2). On these new patients, the AUC was 0.50, no better than chance. The team had fixed a cut-off in advance, the score above which the model calls a kidney obstructed. At that cut-off, the model flagged essentially every kidney as obstructed. Sensitivity is the share of obstructed kidneys that a model flags, and it was 100%. Specificity is the share of unobstructed kidneys that it correctly calls unobstructed, and it was 0%.

<figure class="fig-svg" id="fig-silent">
<svg viewBox="0 0 600 534" role="img" style="max-width: 560px; font-family: var(--sans)" aria-label="Schematic of the silent trial. Each new kidney ultrasound goes down two paths. On the left, the clinical team assesses and manages the infant as usual, and the outcome is later taken from chart review: whether the infant needed surgery for the obstruction. On the right, the model reads the same image, and a research team keeps its prediction. The prediction is never shown to clinicians. Later, each prediction is compared with the outcome, using the AUC and the sensitivity and specificity at the cut-off fixed in advance.">
<defs>
<marker id="sd-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" style="fill: var(--ink-3)"/></marker>
<marker id="sd-arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" style="fill: var(--red)"/></marker>
</defs>
<rect x="130" y="2" width="340" height="56" rx="8" style="fill: var(--sig-soft); stroke: var(--sig); stroke-width: 2"/>
<text x="300" y="37" text-anchor="middle" style="fill: var(--ink); font-size: 20px; font-weight: 600">Each new kidney ultrasound</text>
<path d="M300 58 V80 H118 V97" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#sd-arrow)"/>
<path d="M300 80 H482 V97" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#sd-arrow)"/>
<rect x="1" y="102" width="234" height="128" rx="8" style="fill: var(--surface); stroke: var(--sig); stroke-width: 2"/>
<text x="118" y="134" text-anchor="middle" style="fill: var(--ink); font-size: 20px; font-weight: 600">Clinical team</text>
<text x="118" y="162" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">assesses and</text>
<text x="118" y="186" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">manages the infant</text>
<text x="118" y="210" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">as usual</text>
<rect x="365" y="102" width="234" height="128" rx="8" style="fill: var(--surface); stroke: var(--sig); stroke-width: 2; stroke-dasharray: 7 5"/>
<text x="482" y="134" text-anchor="middle" style="fill: var(--ink); font-size: 20px; font-weight: 600">Model</text>
<text x="482" y="162" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">reads the same image.</text>
<text x="482" y="186" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">A research team</text>
<text x="482" y="210" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">keeps the prediction.</text>
<path d="M362 166 H243" style="fill: none; stroke: var(--red); stroke-width: 2; stroke-dasharray: 6 5" marker-end="url(#sd-arrow-red)"/>
<path d="M292 158 L308 174 M308 158 L292 174" style="fill: none; stroke: var(--red); stroke-width: 3; stroke-linecap: round"/>
<text x="300" y="146" text-anchor="middle" style="fill: var(--red); font-size: 18px; font-weight: 600">Never shown</text>
<text x="300" y="198" text-anchor="middle" style="fill: var(--red); font-size: 18px; font-weight: 600">to clinicians</text>
<path d="M118 230 V265" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#sd-arrow)"/>
<rect x="1" y="270" width="234" height="124" rx="8" style="fill: var(--sig-soft); stroke: var(--sig); stroke-width: 2"/>
<text x="118" y="302" text-anchor="middle" style="fill: var(--ink); font-size: 20px; font-weight: 600">Outcome</text>
<text x="118" y="328" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">from chart review:</text>
<text x="118" y="352" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">surgery for the</text>
<text x="118" y="376" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">obstruction, or not</text>
<path d="M118 394 V425" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#sd-arrow)"/>
<path d="M482 230 V425" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#sd-arrow)"/>
<rect x="0" y="430" width="600" height="102" rx="8" style="fill: var(--sig)"/>
<text x="300" y="464" text-anchor="middle" style="fill: var(--on-fill); font-size: 20px; font-weight: 600">Later: compare each prediction with the outcome</text>
<text x="300" y="494" text-anchor="middle" style="fill: var(--on-fill); font-size: 19px">Measures: AUC, and sensitivity and specificity</text>
<text x="300" y="518" text-anchor="middle" style="fill: var(--on-fill); font-size: 19px">at the cut-off fixed in advance</text>
</svg>
<figcaption><b>Figure 2. How the silent trial was set up.</b> Follow the two paths from the same ultrasound. The clinical team worked as usual, and a separate research team recorded the model's predictions, which the clinicians never saw. Each prediction was later compared with the outcome. The outcome was whether the infant needed surgery for the obstruction, taken from chart review. This is a schematic, not a real image, drawn from the description in <a href="https://doi.org/10.3389/fdgth.2022.929508">Kwong, Erdman, et al., Frontiers in Digital Health 2022</a>.</figcaption>
</figure>

The cause was dataset shift, also called drift, which is a difference between the data that a model was trained on and the data that it is used on. The new infants were younger, and more of their obstructed kidneys were on the right side. Their images also differed from the training images, even after the same cleaning steps, called preprocessing (Figure 3).

<figure class="fig-img" id="fig-ultrasound">
<img src="/assets/img/blog/the-evidence-ladder/kwong-2022-fig2c-ultrasound.jpg" width="456" height="442" loading="lazy" style="max-width: 456px; margin: 0 auto" alt="Four grayscale ultrasound images of infants' kidneys in two columns. The left column, labeled Training, shows a sagittal view above a transverse view from the training set; these look grainy and high in contrast. The right column, labeled Silent Trial 1, shows the same two views from the first silent trial; these look smoother and grayer.">
<figcaption><b>Figure 3. The new images looked different.</b> Look at the texture and contrast of the images, not at the kidneys in them. On the left, the images from the training set are grainy and high in contrast. On the right, the images from the first silent trial are smoother and grayer. The top row is a sagittal view and the bottom row a transverse view. Both sets were cropped and normalized in the same way. <span class="credit">Image: <a href="https://doi.org/10.3389/fdgth.2022.929508">Kwong, Erdman, et al., Frontiers in Digital Health 2022</a>, the paper's Figure 2 (panel C), <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>, cropped.</span></figcaption>
</figure>

The fix that mattered most addressed the file format. The original images had been preprocessed and saved as JPEG files, while the new ones arrived as PNG files, some preprocessed and some not. JPEG and PNG are two common formats that store a picture differently. Putting the new images through the same preprocessing steps did not remove the difference. The team then saved the preprocessed images as JPEG and read them back into the model, like the originals. On the same silent-trial data, the AUC rose to 0.84. After retraining on the old and new data together, it reached 0.92 on a second silent dataset (Figure 4).

<figure>
<div class="hbars" role="img" aria-label="AUC of the model at each stage, for the version that reads ultrasound images of infants' kidneys and uses images only: 0.90 on held-out images from the past data, 0.50 on new patients in the first silent trial, 0.84 on the same patients once their images were saved as JPEG like the originals, and 0.92 in the second silent trial after retraining.">
<p class="grp">AUC of the model at each stage (0.5 is chance, 1.0 is perfect)</p>
<div class="r"><span class="t">Past data, held-out images</span><div class="track"><div class="bar" style="width:90%;background:var(--ctx)"></div></div><span class="v">0.90</span></div>
<div class="r"><span class="t">Silent trial 1, new patients</span><div class="track"><div class="bar" style="width:50%;background:var(--emph)"></div></div><span class="v">0.50</span></div>
<div class="r"><span class="t">Same patients, images saved as JPEG</span><div class="track"><div class="bar" style="width:84%;background:var(--ctx)"></div></div><span class="v">0.84</span></div>
<div class="r"><span class="t">Silent trial 2, after retraining</span><div class="track"><div class="bar" style="width:92%;background:var(--ctx)"></div></div><span class="v">0.92</span></div>
</div>
<div class="legend"><span><i class="sw-ctx"></i>model working</span><span><i class="sw-emph"></i>the failure that silent deployment caught</span></div>
<figcaption><b>Figure 4. Silent deployment caught a broken model.</b> Look at the second bar, where the model fell to chance on new patients. The next two bars show its recovery, first after the image format was fixed and then after retraining. The bars show the version of the model that used images only, on a scale from 0 to 1. Data: <a href="https://doi.org/10.3389/fdgth.2022.929508">Kwong, Erdman, et al., Frontiers in Digital Health 2022</a>, Table 3.</figcaption>
</figure>

To me, this is the strongest argument for silent deployment, because the model failed completely before any clinician could act on its output.

A [scoping review published in 2026](https://doi.org/10.1038/s44360-025-00048-z) found 75 silent evaluations of medical AI from 2015 to 2025. Most reported the AUC and similar technical measures, and far fewer compared the outputs with the diagnoses that patients at the site actually received. Until formal guidelines exist, I would fix the cut-off in advance, as the Toronto team did, and report sensitivity and specificity at that cut-off against local diagnoses.

<div class="callout q"><span class="lbl">Ask</span><p>Has this tool run silently here, on our own patients and our own scanners, before anyone acts on its output?</p></div>

</section>

<section id="trials">

## <span class="n">04</span>Pilots and randomized trials

A silent deployment shows whether the model works on local patients, but not whether anyone will act differently because of it. A supervised pilot answers that question at Fryback's levels 3 and 4. For example, a pilot could test a tool that flags chest radiographs in the emergency department. It would record whether each flag changed what the physician thought and did, and whether that change was right. A reporting guideline is a checklist of what a study should report so that readers can judge it. For this stage, the guideline is [DECIDE-AI](https://doi.org/10.1038/s41591-022-01772-9), which was written for the early clinical evaluation of decision support systems driven by AI. Its authors note that a growing number of these systems perform well in preclinical tests on a computer, "but few have yet demonstrated real benefit to patient care."

A randomized trial can show whether patients do better, but only if it measures a patient outcome. A [scoping review published in 2024](https://doi.org/10.1016/S2589-7500(24)00047-5) found 86 randomized trials of AI in clinical practice, published from January 2018 to November 2023. In 46 of them, the primary endpoint was diagnostic yield or performance. Diagnostic yield is how many cases a test finds, as in a detection rate, and performance is how accurate the test is. Randomization strengthens the design but does not move a study up Fryback's levels. Therefore, when a randomized trial has a detection rate as its endpoint, it still measures diagnostic accuracy, which is level 2.

Most rungs of the ladder now have their own reporting guideline (Figure 5).

<figure>
<table class="data">
<thead><tr><th>Rung</th><th>Highest level that it can show</th><th>Reporting guideline</th></tr></thead>
<tbody>
<tr><td><b>Past data</b><span>like preclinical</span></td><td><b>Level 2</b><span>diagnostic accuracy</span></td><td><b>TRIPOD+AI</b><span>2024</span></td></tr>
<tr><td><b>Silent deployment</b><span>like an early-phase study</span></td><td><b>Level 2</b><span>accuracy on live local patients</span></td><td class="hi"><b>None yet</b><span>no formal guideline</span></td></tr>
<tr><td><b>Supervised pilot</b><span>like Phase II</span></td><td><b>Levels 3 and 4</b><span>effect on diagnosis and management</span></td><td><b>DECIDE-AI</b><span>2022</span></td></tr>
<tr><td><b>Randomized trial</b><span>like Phase III</span></td><td><b>Level 5</b><span>only if a patient outcome is the endpoint</span></td><td><b>SPIRIT-AI, CONSORT-AI</b><span>2020</span></td></tr>
<tr><td><b>After launch</b><span>like Phase IV</span></td><td><b>All levels, over time</b><span>does it keep working?</span></td><td><b>Local monitoring</b><span>see the next post</span></td></tr>
</tbody>
</table>
<figcaption><b>Figure 5. Each rung, the highest level that it can show, and its reporting guideline.</b> Read across each row. The highlighted cell marks the one rung that has no guideline yet. Levels from <a href="https://doi.org/10.1177/0272989X9101100203">Fryback and Thornbury 1991</a>. Guidelines: <a href="https://doi.org/10.1136/bmj-2023-078378">TRIPOD+AI</a> (studies that develop or evaluate a prediction model), <a href="https://doi.org/10.1038/s41591-022-01772-9">DECIDE-AI</a> (early clinical evaluation), <a href="https://doi.org/10.1038/s41591-020-1037-7">SPIRIT-AI</a> (trial protocols) and <a href="https://doi.org/10.1038/s41591-020-1034-x">CONSORT-AI</a> (trial reports). The mapping is mine.</figcaption>
</figure>

</section>

<section id="masai">

## <span class="n">05</span>A randomized screening trial

A trial in breast cancer screening shows what the randomized rung looks like for AI. In Swedish screening, two radiologists read every mammogram, which is called double reading. The Mammography Screening with Artificial Intelligence trial (MASAI) randomly assigned women at four screening sites to double reading or to AI-supported screening (Figure 6). For women assigned to AI-supported screening (the AI arm), a commercial system called Transpara scored each exam from 1 to 10. Exams with the highest score of 10 were read by two radiologists, and all other exams by one. The radiologists saw the score and, for scores of 8 to 10, the AI's marks on the image.

<figure class="fig-svg" id="fig-masai-design">
<svg viewBox="0 0 600 636" role="img" style="max-width: 560px; font-family: var(--sans)" aria-label="Schematic of the design of the Swedish screening trial. Women at four screening sites in Sweden were randomly assigned, 1 to 1, to AI-supported screening or to double reading. In AI-supported screening, the AI scores each exam from 1 to 10. An exam with a score of 10 is read by two radiologists, and an exam with a score of 1 to 9 by one radiologist. Radiologists see the score and, for scores 8 to 10, the AI's marks on the image. In double reading, two radiologists read every exam. The primary endpoint in both groups is interval cancers, breast cancers diagnosed between screening rounds after a screen that did not detect them.">
<defs>
<marker id="ma-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" style="fill: var(--ink-3)"/></marker>
</defs>
<rect x="70" y="2" width="460" height="54" rx="8" style="fill: var(--surface); stroke: var(--ink-3); stroke-width: 2"/>
<text x="300" y="36" text-anchor="middle" style="fill: var(--ink); font-size: 20px; font-weight: 600">Women at four screening sites in Sweden</text>
<path d="M300 56 V98" style="fill: none; stroke: var(--ink-3); stroke-width: 2"/>
<text x="312" y="84" style="fill: var(--ink-2); font-size: 19px; font-weight: 600">Randomly assigned, 1 to 1</text>
<path d="M300 98 H170 V125" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#ma-arrow)"/>
<path d="M300 98 H485 V125" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#ma-arrow)"/>
<rect x="0" y="130" width="340" height="50" rx="8" style="fill: var(--sig)"/>
<text x="170" y="162" text-anchor="middle" style="fill: var(--on-fill); font-size: 20px; font-weight: 600">AI-supported screening</text>
<rect x="370" y="130" width="230" height="50" rx="8" style="fill: var(--scale)"/>
<text x="485" y="162" text-anchor="middle" style="fill: var(--on-fill); font-size: 20px; font-weight: 600">Double reading</text>
<path d="M170 180 V203" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#ma-arrow)"/>
<path d="M485 180 V203" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#ma-arrow)"/>
<rect x="1" y="208" width="338" height="76" rx="8" style="fill: var(--sig-soft); stroke: var(--sig); stroke-width: 2"/>
<text x="170" y="240" text-anchor="middle" style="fill: var(--ink); font-size: 20px">AI scores each exam</text>
<text x="170" y="266" text-anchor="middle" style="fill: var(--ink); font-size: 20px">from 1 to 10</text>
<rect x="371" y="208" width="228" height="210" rx="8" style="fill: var(--surface); stroke: var(--ink-3); stroke-width: 2"/>
<text x="485" y="306" text-anchor="middle" style="fill: var(--ink); font-size: 20px">Two radiologists</text>
<text x="485" y="332" text-anchor="middle" style="fill: var(--ink); font-size: 20px">read every exam</text>
<path d="M170 284 V300 H80 V317" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#ma-arrow)"/>
<path d="M170 300 H260 V317" style="fill: none; stroke: var(--ink-3); stroke-width: 2" marker-end="url(#ma-arrow)"/>
<rect x="1" y="322" width="158" height="96" rx="8" style="fill: var(--surface); stroke: var(--sig); stroke-width: 2"/>
<text x="80" y="352" text-anchor="middle" style="fill: var(--ink); font-size: 19px; font-weight: 600">Score 10</text>
<text x="80" y="378" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">read by two</text>
<text x="80" y="402" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">radiologists</text>
<rect x="181" y="322" width="158" height="96" rx="8" style="fill: var(--surface); stroke: var(--sig); stroke-width: 2"/>
<text x="260" y="352" text-anchor="middle" style="fill: var(--ink); font-size: 19px; font-weight: 600">Scores 1 to 9</text>
<text x="260" y="378" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">read by one</text>
<text x="260" y="402" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">radiologist</text>
<text x="170" y="448" text-anchor="middle" style="fill: var(--ink-3); font-size: 18px">Radiologists see the score and,</text>
<text x="170" y="472" text-anchor="middle" style="fill: var(--ink-3); font-size: 18px">for scores 8 to 10, the AI's marks</text>
<text x="170" y="496" text-anchor="middle" style="fill: var(--ink-3); font-size: 18px">on the image</text>
<rect x="1" y="522" width="598" height="112" rx="8" style="fill: var(--amber-soft); stroke: var(--amber-deep); stroke-width: 1.5"/>
<text x="300" y="556" text-anchor="middle" style="fill: var(--ink); font-size: 20px; font-weight: 600">Primary endpoint: interval cancers</text>
<text x="300" y="586" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">breast cancers diagnosed between screening rounds,</text>
<text x="300" y="612" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px">after a screen that did not detect them</text>
</svg>
<figcaption><b>Figure 6. How the screening trial was designed.</b> Follow each group from the top. In the AI arm, one radiologist read each exam with a score of 1 to 9, and two radiologists read each exam with a score of 10. In the double-reading arm (the standard arm), two radiologists read every exam. Both groups were compared on the same primary endpoint, shown at the bottom. This is a schematic, not a real image, drawn from the description in <a href="https://doi.org/10.1016/S1470-2045(23)00298-X">Lång et al., Lancet Oncology 2023</a>.</figcaption>
</figure>

In a [safety analysis](https://doi.org/10.1016/S1470-2045(23)00298-X) of the first 80,033 women, the AI arm detected 244 cancers and the standard arm detected 203. The ratio of the two detection rates was 1.2. Its 95% confidence interval ran from 1.0 to 1.5, so it included 1.0, the ratio that means no difference, and the authors described the detection rates as similar.

The primary endpoint was the rate of interval cancers. An interval cancer is a breast cancer that is diagnosed between two screening rounds after a screen that did not detect it. The rate is a standard measure of the cancers that screening misses, although some interval cancers grow too fast to be visible at the earlier screen. MASAI was a non-inferiority trial, designed to show that AI-supported screening was not worse than double reading by more than a margin set in advance. The margin was 20%, so the rate of interval cancers with AI support could be at most 1.2 times the rate with double reading.

In the [final analysis](https://doi.org/10.1016/S0140-6736(25)02464-X) of 105,934 women, the rate of interval cancers was 1.55 per 1,000 with AI support and 1.76 per 1,000 with double reading. The ratio of the two rates was 0.88, with a 95% confidence interval of 0.65 to 1.18. The upper limit was below 1.2, so AI-supported screening met the test for non-inferiority. Because the interval also included 1.0, it was not shown to be better (Figure 7). Figure 8 shows the main results of both analyses side by side.

<figure class="fig-svg" id="fig-noninferiority">
<svg viewBox="0 0 600 384" role="img" style="max-width: 600px; font-family: var(--sans)" aria-label="Number line of the ratio of interval cancer rates, AI-supported screening divided by double reading, from 0.5 to 1.5. The estimate is 0.88, and its 95% confidence interval runs from 0.65 to 1.18. A solid vertical line at 1.0 marks no difference. A dashed red line at 1.2 marks the margin, and the area to its right is shaded and labeled worse than allowed. Values left of 1.0 mean fewer interval cancers with AI support, and values right of 1.0 mean more. The interval ends below 1.2, so AI-supported screening is not worse than double reading. It also includes 1.0, so it is not shown to be better.">
<rect x="408" y="50" width="162" height="150" style="fill: var(--red-soft)"/>
<text x="489" y="166" text-anchor="middle" style="fill: var(--red); font-size: 19px; font-weight: 600">Worse than</text>
<text x="489" y="190" text-anchor="middle" style="fill: var(--red); font-size: 19px; font-weight: 600">allowed</text>
<line x1="300" y1="50" x2="300" y2="200" style="stroke: var(--ink-3); stroke-width: 2"/>
<line x1="408" y1="50" x2="408" y2="200" style="stroke: var(--red); stroke-width: 2.5; stroke-dasharray: 7 5"/>
<text x="294" y="38" text-anchor="end" style="fill: var(--ink-2); font-size: 19px; font-weight: 600">No difference, 1.0</text>
<text x="414" y="38" style="fill: var(--red); font-size: 19px; font-weight: 600">Margin, 1.2</text>
<line x1="111" y1="128" x2="397.2" y2="128" style="stroke: var(--sig); stroke-width: 5"/>
<circle cx="235.2" cy="128" r="9" style="fill: var(--sig)"/>
<text x="284" y="166" text-anchor="end" style="fill: var(--sig-ink); font-size: 19px; font-weight: 600">0.88 (95% CI 0.65 to 1.18)</text>
<line x1="30" y1="214" x2="570" y2="214" style="stroke: var(--ink-3); stroke-width: 1.5"/>
<path d="M30 214 V222 M165 214 V222 M300 214 V222 M435 214 V222 M570 214 V222" style="fill: none; stroke: var(--ink-3); stroke-width: 1.5"/>
<text x="30" y="244" text-anchor="middle" style="fill: var(--ink-3); font-size: 19px">0.5</text>
<text x="165" y="244" text-anchor="middle" style="fill: var(--ink-3); font-size: 19px">0.75</text>
<text x="300" y="244" text-anchor="middle" style="fill: var(--ink-3); font-size: 19px">1.0</text>
<text x="435" y="244" text-anchor="middle" style="fill: var(--ink-3); font-size: 19px">1.25</text>
<text x="570" y="244" text-anchor="middle" style="fill: var(--ink-3); font-size: 19px">1.5</text>
<text x="300" y="274" text-anchor="middle" style="fill: var(--ink-2); font-size: 19px; font-weight: 600">Ratio of interval cancer rates, AI support ÷ double reading</text>
<text x="30" y="300" style="fill: var(--ink-3); font-size: 19px">← fewer with AI support</text>
<text x="570" y="300" text-anchor="end" style="fill: var(--ink-3); font-size: 19px">more with AI support →</text>
<text x="30" y="344" style="fill: var(--ink); font-size: 20px">Upper limit below 1.2: not worse than double reading</text>
<text x="30" y="374" style="fill: var(--ink); font-size: 20px">Interval includes 1.0: not shown to be better</text>
</svg>
<figcaption><b>Figure 7. On interval cancers: not worse, and not shown to be better.</b> Look at where the blue bar ends. The dot is the estimated ratio of interval cancer rates, and the bar is its 95% confidence interval. The bar ends left of the margin of 1.2, so AI-supported screening was non-inferior. It also crosses the line at 1.0, so it was not shown to be better on this endpoint. Drawn to scale from the published numbers. Data: <a href="https://doi.org/10.1016/S0140-6736(25)02464-X">Gommers et al., Lancet 2026</a>.</figcaption>
</figure>

<figure>
<table class="data">
<thead><tr><th>Swedish screening trial</th><th>AI-supported</th><th>Standard double reading</th></tr></thead>
<tbody>
<tr><td><b>Cancers detected</b><span>first 80,033 women</span></td><td><b>244</b><span>6.1 per 1,000</span></td><td><b>203</b><span>5.1 per 1,000</span></td></tr>
<tr><td><b>Women called back</b><span>share called back for more tests</span></td><td><b>2.2%</b></td><td><b>2.0%</b></td></tr>
<tr><td><b>Screen readings</b><span>by radiologists</span></td><td><b>46,345</b><span>44% fewer</span></td><td><b>83,231</b></td></tr>
<tr><td><b>Interval cancers</b><span>diagnosed between screens, per 1,000 women, final analysis</span></td><td><b>1.55</b><span>ratio 0.88, non-inferior</span></td><td><b>1.76</b></td></tr>
</tbody>
</table>
<figcaption><b>Figure 8. What the randomized rung looks like.</b> Compare the two columns row by row. With AI support, radiologists detected a similar number of cancers and called back a similar share of women while they did far fewer readings. The rate of interval cancers passed the test for non-inferiority. The first three rows come from the safety analysis of the first 80,033 women; the last row is the primary endpoint for 105,934 women. Data: <a href="https://doi.org/10.1016/S1470-2045(23)00298-X">Lång et al., Lancet Oncology 2023</a>; <a href="https://doi.org/10.1016/S0140-6736(25)02464-X">Gommers et al., Lancet 2026</a>.</figcaption>
</figure>

The trial still stops one step short of a patient outcome. Interval cancers are a surrogate endpoint, a measurement that stands in for a clinical outcome because it is faster to measure. [An earlier post in this series](/blog/proxy-surrogate-endpoint/#surrogates-fail) explains how surrogates can mislead. The outcome that matters to women is death from breast cancer, and a trial needs years of follow-up to measure it. The AI arm also detected more in situ cancers, which have not yet invaded the surrounding tissue (60 against 38 in the safety analysis). Some of these may represent overdiagnosis, the detection of a cancer that would never have harmed the woman in her lifetime. The trial also tested one product in one Swedish screening program. What it did well was to set its primary endpoint and margin in advance and to report the primary result as non-inferior rather than as superior.

</section>

<section id="questions">

## <span class="n">06</span>Five questions to ask

When someone shows me an AI tool, I ask first which rung its evidence has reached, and only then look at the AUC.

<ol class="num-list">
<li><strong>Which rung has the evidence reached?</strong> Past data, silent deployment, a supervised pilot, a randomized trial, or monitoring after launch.<span class="an">Like asking which phase a drug is in</span></li>
<li><strong>Has it run silently here?</strong> On our own patients and scanners, with the cut-off fixed in advance and nobody acting on the output.<span class="an">Like validating a new assay in your own lab</span></li>
<li><strong>What did the study measure?</strong> Accuracy, clinicians' decisions or patient outcomes. A randomized design does not change which of these the study measured.<span class="an">A randomized trial can still measure only accuracy</span></li>
<li><strong>How did it reach the market?</strong> Through 510(k), De Novo or premarket approval. If through 510(k), which predicate device it was compared with, and what evidence that predicate itself had.<span class="an">Clearance is not proof of benefit</span></li>
<li><strong>Who monitors it after launch?</strong> A named person, with a plan for when the patients or the scanners change.<span class="an">Like safety monitoring of a drug after approval</span></li>
</ol>

When the evidence for a tool stops at past data, I believe it should run silently on the site's own patients before clinicians act on it. Before launch, the site should also name the person who will keep checking that the tool still works.

[The next post](/blog/efficacy-is-not-effectiveness/) is about monitoring after launch, because a tool that passed every earlier rung can still stop working when the patients or the scanners change. The [overview of the series](/blog/the-model-is-not-the-hard-part/) shows how all the posts fit together.

</section>

<section id="sources">

## <span class="n">A</span>Sources

<ol class="refs">
  <li>Fryback DG, Thornbury JR. <a href="https://doi.org/10.1177/0272989X9101100203">The efficacy of diagnostic imaging.</a> Med Decis Making 1991;11:88-94.</li>
  <li>US Food and Drug Administration. The drug development process: <a href="https://www.fda.gov/patients/drug-development-process/step-2-preclinical-research">Step 2, preclinical research</a> and <a href="https://www.fda.gov/patients/drug-development-process/step-3-clinical-research">Step 3, clinical research</a>. Content current as of 4 January 2018; accessed 4 November 2026.</li>
  <li>US Food and Drug Administration. Device premarket pathways: <a href="https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/premarket-notification-510k">Premarket notification 510(k)</a>, <a href="https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/de-novo-classification-request">De Novo classification request</a> and <a href="https://www.fda.gov/medical-devices/premarket-submissions-selecting-and-preparing-correct-submission/premarket-approval-pma">Premarket approval (PMA)</a>. Accessed 4 November 2026.</li>
  <li>US Food and Drug Administration. <a href="https://www.fda.gov/medical-devices/artificial-intelligence-enabled-medical-devices/list-artificial-intelligence-enabled-medical-devices">Artificial intelligence-enabled medical devices list.</a> Content current as of 4 September 2026; accessed 4 November 2026. Submission-type and panel counts are a tally of the list.</li>
  <li>Wu E, et al. <a href="https://doi.org/10.1038/s41591-021-01312-x">How medical AI devices are evaluated: limitations and recommendations from an analysis of FDA approvals.</a> Nat Med 2021;27:582-4.</li>
  <li>Kwong JCC, Erdman L, et al. <a href="https://doi.org/10.3389/fdgth.2022.929508">The silent trial - the bridge between bench-to-bedside clinical AI applications.</a> Front Digit Health 2022;4:929508.</li>
  <li>Tikhomirov L, et al. <a href="https://doi.org/10.1038/s44360-025-00048-z">A scoping review of silent trials for medical artificial intelligence.</a> Nat Health 2026;1:532-54.</li>
  <li>Vasey B, et al. <a href="https://doi.org/10.1038/s41591-022-01772-9">Reporting guideline for the early-stage clinical evaluation of decision support systems driven by artificial intelligence: DECIDE-AI.</a> Nat Med 2022;28:924-33.</li>
  <li>Han R, et al. <a href="https://doi.org/10.1016/S2589-7500(24)00047-5">Randomised controlled trials evaluating artificial intelligence in clinical practice: a scoping review.</a> Lancet Digit Health 2024;6:e367-73.</li>
  <li>Collins GS, et al. <a href="https://doi.org/10.1136/bmj-2023-078378">TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods.</a> BMJ 2024;385:e078378.</li>
  <li>Cruz Rivera S, et al. <a href="https://doi.org/10.1038/s41591-020-1037-7">Guidelines for clinical trial protocols for interventions involving artificial intelligence: the SPIRIT-AI extension.</a> Nat Med 2020;26:1351-63.</li>
  <li>Liu X, et al. <a href="https://doi.org/10.1038/s41591-020-1034-x">Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension.</a> Nat Med 2020;26:1364-74.</li>
  <li>Lång K, et al. <a href="https://doi.org/10.1016/S1470-2045(23)00298-X">Artificial intelligence-supported screen reading versus standard double reading in the Mammography Screening with Artificial Intelligence trial (MASAI): a clinical safety analysis of a randomised, controlled, non-inferiority, single-blinded, screening accuracy study.</a> Lancet Oncol 2023;24:936-44.</li>
  <li>Gommers J, et al. <a href="https://doi.org/10.1016/S0140-6736(25)02464-X">Interval cancer, sensitivity, and specificity comparing AI-supported mammography screening with standard double reading without AI in the MASAI study: a randomised, controlled, non-inferiority, single-blinded, population-based, screening-accuracy trial.</a> Lancet 2026;407:505-14.</li>
</ol>

</section>
