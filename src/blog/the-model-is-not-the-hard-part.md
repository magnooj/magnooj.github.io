---
title: The model is not the hard part
description: Four questions for any medical AI tool, and why answering them takes clinical training more than code.
date: 2026-10-28
kicker: Talk notes · MedAI Summit 2026
ogImage: /assets/img/blog/model-not-hard-part/og.png
ogImageAlt: "The model is not the hard part. Four questions for any medical AI tool: data provenance, label definition, evaluation, after go-live."
disclosure: I work at HOPPR, which builds AI for medical imaging. This post has no product content, and every study in it is independent of my company. The views are my own.
---

These are the notes from my talk at the 2nd MedAI Summit, given to medical and pharmacy students, most of whom have never written a line of code. I've written them up for anyone who wants the argument without the slides.

When I teach medical students about AI, I see the same pattern. They massively overestimate the model, the algorithm itself, and underestimate everything around it: where the data came from, how the labels were defined, and how the tool was evaluated. I think that's good news for them, because those underestimated parts are exactly where a physician has an edge over a computer-science graduate.

## Two ideas are all the AI you need

First, a model learns from examples that someone labeled. Someone decided the right answer for every training image or record, and that label became the model's reference standard. If the labels are wrong, the model learns the wrong thing.

Second, a model gives a score, and someone picks a cut-off. It works like troponin: the number is continuous, but the decision isn't. Move the cut-off and you trade missed cases for false alarms.

Everything else in this post is clinical.

<figure>
  <img src="/assets/img/blog/model-not-hard-part/01-small-box.png" width="1080" height="1350" loading="lazy" alt="Diagram of a machine-learning system as boxes of different sizes. The model is the smallest box. Data provenance, label definition and evaluation are three of the largest boxes and are highlighted as the places where a physician has the edge. The other large boxes are data pipelines, infrastructure, integration, monitoring and governance.">
  <figcaption>In a real machine-learning system, the model code is a small part of the whole. After <a href="https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html">Sculley et al., NeurIPS 2015</a>; the clinical labels are mine.</figcaption>
</figure>

I find it helps to judge an AI tool the way you'd judge a diagnostic test and a drug at the same time. It performs like a test, so you ask about sensitivity, specificity and predictive value. It lives like a drug, so you ask about its ingredients, its indication, its trials and its safety monitoring. That gives four questions.

## 1. Data provenance: where did the data come from? {#provenance}

In 2019 a team in Heidelberg tested a commercial melanoma classifier, one already approved as a medical device in Europe, on 130 skin lesions: 107 benign moles and 23 melanomas. Each lesion was shown to the model twice, once clean and once marked with the purple ink surgeons draw around a lesion before excision. Nothing about the moles changed. The model's specificity on benign moles fell from 84% to 46%, and its rate of false alarms more than tripled. Heat maps showed it was looking at the ink, and when the researchers cropped the ink out, performance came back.

<figure>
  <img src="/assets/img/blog/model-not-hard-part/02-ink.png" width="1080" height="1350" loading="lazy" alt="Bar chart. Specificity of a commercial melanoma AI on benign moles: 84 percent on unmarked images, 46 percent on the same moles marked with surgical ink. False alarms rose from 16 percent to 54 percent.">
  <figcaption>Same moles, with and without surgical ink. Data from <a href="https://doi.org/10.1001/jamadermatol.2019.1735">Winkler et al., JAMA Dermatology 2019</a>.</figcaption>
</figure>

The explanation is clinical. Surgeons mark the lesions that worry them, so the authors suspected that ink was over-represented among the melanomas in the training data. If so, the model learned the surgeon's worry, not the disease. The people who suspected the ink were dermatologists, who know why lesions get marked. Without that context, ink is just pixels.

This isn't a one-off. A model learns whatever separates its positives from its negatives. Pneumonia models have learned [which hospital an X-ray came from](https://doi.org/10.1371/journal.pmed.1002683), because one hospital had far more pneumonia than the others. Dermatology models have [performed worse on darker skin](https://doi.org/10.1126/sciadv.abq6147), and the images used to train them have mostly shown lighter skin. So ask three things about the ingredients. Could it be right for the wrong reason? Who is in the data, and do they look like my patients, the way you'd read a trial's inclusion criteria? And how were the labels made: biopsy and follow-up, or software skimming the report text?

In my own work, most of the effort goes into the data, not the model, and I'm not alone. A study of AI practitioners in high-stakes fields was titled, literally, ["Everyone wants to do the model work, not the data work."](https://doi.org/10.1145/3411764.3445518) The authors described data cascades, problems that compound quietly downstream, and 92% of the practitioners they interviewed had hit at least one.

<p class="question"><strong>Question 1.</strong> Where did the data come from, and do those patients look like mine?</p>

## 2. Label definition: what exactly does it predict? {#label}

A widely used commercial algorithm helped US health systems choose patients for an extra-care program. The goal was to find the patients who needed help most. But need isn't a column in a database, so the developers predicted something that is: each patient's healthcare cost over the next year. In the US, less is spent on Black patients than on white patients at the same level of illness, partly because of unequal access to care. So at the same risk score, Black patients were considerably sicker. The algorithm predicted cost well. It was answering the wrong question.

<figure>
  <img src="/assets/img/blog/model-not-hard-part/03-cost.png" width="1080" height="1350" loading="lazy" alt="The goal was to find patients who need extra care, but the label was next year's healthcare cost. At the same risk score, Black patients were considerably sicker. Removing the bias would raise Black patients' share of the extra help from 17.7 percent to 46.5 percent, the authors estimated.">
  <figcaption>A proxy label that predicted well and still failed. Data from <a href="https://doi.org/10.1126/science.aax2342">Obermeyer et al., Science 2019</a>.</figcaption>
</figure>

The authors, led by Ziad Obermeyer, an emergency physician, estimated that removing the bias would raise Black patients' share of the extra help from 17.7% to 46.5%. Working with the manufacturer, they then changed only the label, to a mix of health and cost, and one measure of the bias fell by 84%. The fix was a better clinical question.

Pharmacy students will recognize the pattern. In the [Cardiac Arrhythmia Suppression Trial](https://doi.org/10.1056/NEJM198908103210629), drugs that suppressed the extra beats on the ECG looked excellent on the surrogate, and more patients died. A proxy label is a surrogate endpoint, and surrogates can fail.

A label can also be wrong in a quieter way: it predicts something that doesn't change what the team does. When Michigan Medicine [independently tested the Epic Sepsis Model](https://doi.org/10.1001/jamainternmed.2021.2626) across 38,455 hospitalizations, it measured an AUC of 0.63, against the 0.76 to 0.83 the vendor had reported. The model missed two-thirds of sepsis cases and alerted on 18% of all hospitalizations. Of 2,552 patients with sepsis, it flagged only 183 whom clinicians hadn't already treated in time. An alert that mostly repeats what the team already knows, or stays silent, changes very little.

My fix is to rewrite any vague claim, such as "AI detects sepsis", as a clinical question. Which patients? Predicting what, exactly? Who sees the output? At what moment? And what will they do differently? It's PICO, plus the user and the moment. If nothing changes at the bedside, the model has no indication. I believe the decisions about the label and the moment of use need a clinician in the room, and across the field, many teams still make them without one. That empty seat is where clinicians belong.

<p class="question"><strong>Question 2.</strong> What exactly does it predict, for whom, and who acts on it, when?</p>

## 3. Evaluation: what evidence is there beyond accuracy? {#evaluation}

Here's a question from the talk. An AI flags inpatients at high risk of a serious adverse drug reaction. It's 95% sensitive and 95% specific, and 1 in 100 patients will have the reaction. When it flags a patient, what's the chance that patient actually has the reaction?

Take 10,000 inpatients. A hundred will have the reaction, and the model catches 95 of them. Of the 9,900 who won't, 5% are flagged anyway: 495 false alarms. So of 590 alerts, 95 are real, about 16%. Five of every six alerts are false. Put the same tool on a ward where 1 in 10 patients react, and the figure rises to about 68%. Same tool, different value.

<figure>
  <img src="/assets/img/blog/model-not-hard-part/04-ppv.png" width="1080" height="1350" loading="lazy" alt="Worked example with 10,000 inpatients and a 1 percent rate of the reaction. The AI raises 590 alerts: 95 true and 495 false, so about 16 percent of alerts are true. Five of every six alerts are false. On a ward where 10 percent react, about 68 percent of alerts would be true.">
  <figcaption>A 95% sensitive, 95% specific tool at 1% prevalence. Worked example.</figcaption>
</figure>

If your gut said 95%, you're in good company. In a [2014 survey of 61 doctors and students at a Boston-area hospital](https://doi.org/10.1001/jamainternmed.2014.1059), only about a quarter got a version of this question right, and the most common answer was 95%. Many AI papers still lead with accuracy or AUC. Clinical training teaches us to ask for the positive predictive value at our own prevalence, even if few of us can do the arithmetic on the spot, and I believe that habit matters more than any detail of how the model is built.

Regulatory clearance doesn't settle the question either. A drug must show in trials that it works before approval. Most AI devices reach the US market through 510(k) clearance, which shows they are similar to an existing device, not that they help patients. A [review of 130 FDA-cleared AI devices](https://doi.org/10.1038/s41591-021-01312-x) found that 126 had been evaluated only on past data, and none of the 54 high-risk devices had a prospective evaluation.

Drug development already has a language for this gap, and an [older hierarchy from diagnostic imaging](https://doi.org/10.1177/0272989X9101100203) maps onto it well. Accuracy on past data is preclinical. Silent mode, where the model runs live but nobody sees its output, is an early-phase study. A supervised pilot asks whether it changes decisions. A randomized trial asks whether it changes outcomes. Monitoring after go-live is Phase IV. Most AI tools you'll meet are still on the first rung.

The best example I know of a tool that climbed is MASAI, a randomized trial of AI-supported mammography screening in Sweden, where two radiologists normally read every exam. In the AI arm, the exams the AI scored as highest risk got two readers and the rest got one. Among the [first 80,033 women](https://doi.org/10.1016/S1470-2045(23)00298-X), the AI arm found 244 cancers against 203, with a similar number of recalls, and radiologists did 44% fewer reads. The [final results](https://doi.org/10.1016/S0140-6736(25)02464-X), for about 106,000 women, showed AI-supported screening was non-inferior on interval cancers, not proven better, and interval cancers are still a surrogate for deaths. To me, that's what honest evidence looks like.

<p class="question"><strong>Question 3.</strong> What evidence is there beyond accuracy, at my prevalence?</p>

## 4. After go-live: who watches it once it's in use? {#after-go-live}

Strong results in testing don't guarantee that a tool will work in a real clinic. Google's diabetic retinopathy AI did well in earlier testing, but when it went into [11 clinics in Thailand](https://doi.org/10.1145/3313831.3376718), more than one in five images were rejected as too low in quality, often because of poor lighting, and slow internet in some clinics delayed results, because the images were sent to the cloud. That's efficacy versus effectiveness, the same gap you know from drug trials.

Then the world changes. In [24 hospitals using the Epic sepsis model](https://doi.org/10.1001/jamanetworkopen.2021.35286), the share of hospitalized patients triggering a sepsis alert each day rose from 9% in the three weeks before each hospital's first COVID-19 case to 21% in the three weeks after, and Michigan paused its sepsis alerts. The study measured alert volume, not accuracy, but the authors suggest dataset shift as a likely cause. Nothing in the code changed; the patients did. Noticing that the patients have changed is a clinical skill too, and I believe clinicians often notice it before any dashboard does.

<figure>
  <img src="/assets/img/blog/model-not-hard-part/05-drift.png" width="1080" height="1350" loading="lazy" alt="Bar chart. Share of hospitalized patients triggering a sepsis alert each day across 24 hospitals: 9 percent in the three weeks before each hospital's first COVID-19 case, 21 percent in the three weeks after. Same model, different patients.">
  <figcaption>Same model, different patients. Data from <a href="https://doi.org/10.1001/jamanetworkopen.2021.35286">Wong et al., JAMA Network Open 2021</a>.</figcaption>
</figure>

Drugs come with a package insert, and so should models. A team at Duke proposed a ["Model Facts" label](https://doi.org/10.1038/s41746-020-0253-3) and published an example for their own sepsis model. It states what the model predicts (sepsis in the next four hours), for whom (adults in their emergency department), and how well it performed, with "TBD" where the evidence doesn't exist yet. Most usefully, it says when not to use it without further testing: in the ICU, after a first episode of sepsis, or at another hospital. And it says plainly that it is not a diagnosis.

<figure>
  <img src="/assets/img/blog/model-not-hard-part/06-package-insert.png" width="1080" height="1350" loading="lazy" alt="A drug package insert compared with a Model Facts label for Duke University Hospital's sepsis model. The label gives a summary (probability of meeting sepsis criteria in the next 4 hours), for whom and when (adults in the emergency department, a new score every hour), validation (AUC 0.88 on past Duke data, 0.94 on later Duke data, TBD in live use and at other hospitals) and warnings (without further evaluation, do not use it in the ICU, after a first sepsis episode or at other hospitals; it is not a diagnosis).">
  <figcaption>Every model needs a package insert. Adapted from <a href="https://doi.org/10.1038/s41746-020-0253-3">Sendak et al., npj Digital Medicine 2020</a>, Fig. 1 (CC BY 4.0).</figcaption>
</figure>

<p class="question"><strong>Question 4.</strong> Who watches it once it's in use?</p>

## Four questions for any medical AI tool {#four-questions}

<figure>
  <img src="/assets/img/blog/model-not-hard-part/07-four-questions.png" width="1080" height="1350" loading="lazy" alt="Four questions for any medical AI tool. One, data provenance: where did the data come from, and do those patients look like mine? Two, label definition: what exactly does it predict, and who acts on it, when? Three, evaluation: what evidence is there beyond accuracy, at my prevalence? Four, after go-live: who watches it once it's in use?">
</figure>

1. **Data provenance.** Where did the data come from, and do those patients look like mine?
2. **Label definition.** What exactly does it predict, and who acts on it, when?
3. **Evaluation.** What evidence is there beyond accuracy, at my prevalence?
4. **After go-live.** Who watches it once it's in use?

None of the four is about the model. A computer-science graduate can build the model. I believe the room where the label is chosen needs someone who knows why the image exists, which outcome matters, and what a positive predictive value means at the bedside. If you're a medical or pharmacy student, that empty seat is yours.

There's a [one-page version of the checklist](https://magnooj.github.io/medai-summit-2026/), with a short reading list, that you can print or share.

<hr>

### Sources

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
