---
title: Efficacy is not effectiveness
description: Why an artificial intelligence tool that is accurate in a study can fail in everyday care, and what a hospital must set up so that it helps patients.
dek: Accuracy in a study does not guarantee benefit in everyday care, because a model depends on the clinic around it and on patients who change over time. Every AI tool therefore needs a local owner who monitors it and can switch it off.
summary: An accurate eye-screening model could not grade one in five photos in everyday clinics, and a sepsis alert flagged more than twice its usual share of inpatients after COVID-19 arrived. Accuracy in a study does not guarantee benefit in care, so every AI tool needs a local owner who monitors it and can switch it off.
date: 2026-12-01
topic: Evaluating medical AI
labels: ["Clinical foundations", "Deployment"]
series: clinical-foundations
part: 5
ogImage: /assets/img/blog/efficacy-is-not-effectiveness/og.png
ogImageAlt: "Title card for part 5 of the series, Efficacy is not effectiveness, with the subtitle: accuracy in a study does not guarantee benefit in everyday care, so every AI tool needs a local owner who monitors it and can switch it off. A dark panel says that in diabetic eye screening at clinics in Thailand, 21% of retinal photos were rejected as ungradable in the first six months, often because of poor lighting (393 of 1,838 photos). Below it are three jobs before an imaging model can help a patient: the right images reach the model, the result reaches the clinician in time, and someone owns re-checking the tool."
disclosure: I work at HOPPR, which builds AI for medical imaging. This post has no product content, and every study in it is independent of my company. The views are my own.
toc:
  - { id: "tldr", n: "·", label: "Take-home messages" }
  - { id: "efficacy", n: "01", label: "Efficacy and effectiveness" }
  - { id: "thailand", n: "02", label: "An accurate model in real clinics" }
  - { id: "plumbing", n: "03", label: "Three practical jobs" }
  - { id: "drift", n: "04", label: "When the patients change" }
  - { id: "ownership", n: "05", label: "A local owner" }
  - { id: "ask", n: "06", label: "Questions to ask" }
  - { id: "sources", n: "A", label: "Sources" }
---

<div class="tiles">
<div class="tile"><div class="v">91.4%</div><div class="l">sensitivity of an eye-screening model for vision-threatening diabetic retinopathy in a prospective study in Thailand</div></div>
<div class="tile"><div class="v">21%</div><div class="l">of retinal photos were rejected as ungradable when the same model was used in routine clinics in Thailand</div></div>
<div class="tile"><div class="v">9% → 21%</div><div class="l">of inpatients in 24 US hospitals triggered a sepsis alert each day, in the three weeks before and after their first COVID-19 case</div></div>
</div>

<section id="tldr" class="tldr">
<span class="lbl">Take-home messages</span>
<ul>
<li><strong>Accuracy in a study is efficacy, not effectiveness.</strong> Efficacy is how well a test or treatment works under ideal, controlled conditions, and effectiveness is how well it works in everyday practice. Published accuracy is a measure of efficacy, and a model can be much less effective in a busy clinic.</li>
<li><strong>Check the clinic, not only the published accuracy.</strong> In a study, an eye-screening model detected more than 90% of cases of vision-threatening diabetic eye disease. In everyday clinics, where rooms were often too bright for the pupils to dilate, it rejected about one in five photos as too poor to grade.</li>
<li><strong>Three practical jobs decide whether a model helps.</strong> The right input must reach the model automatically, and the result must reach the clinician while it can still change a decision. The model must also be re-checked after every change of scanner, protocol or software.</li>
<li><strong>Patients change while the model stays the same.</strong> Dataset shift, or drift, is a mismatch between the patients that a model sees in use and the patients on whom it was developed. After COVID-19 arrived, a sepsis alert flagged 21% of inpatients each day instead of 9%, and one hospital withdrew it because fever had become a weaker sign of bacterial sepsis.</li>
<li><strong>Every tool needs a local owner.</strong> Someone at the hospital must watch the tool on local patients and must have the authority to switch it off. Clinicians need to know who that person is, because they are often the first to notice a problem.</li>
</ul>
</section>

<section id="efficacy">

## <span class="n">01</span>Efficacy and effectiveness

A medical artificial intelligence (AI) tool is evaluated to learn whether it will help patients. Many published evaluations answer a narrower question, which is how accurately the model performs on data that were prepared for the study. Clinical researchers separate these two questions with the terms efficacy and effectiveness.

A [primer on clinical trials](https://doi.org/10.1038/ctg.2013.13) defines efficacy as the performance of an intervention under ideal and controlled circumstances, and effectiveness as its performance under real-world conditions. Outside a trial, the intervention also has to be available, recommended to the right patients and accepted by them, so an efficacy trial can overestimate its effect in practice.

The primer's imaging example is ultrasound for early liver cancer. Sensitivity is the share of patients with the disease whom a test detects. In prospective efficacy studies, ultrasound detected early-stage liver cancer with a sensitivity of 63%. In a later effectiveness study, its sensitivity was only 32%. Alpha-fetoprotein had a comparable sensitivity of 46%, although this blood test had been considered less efficacious. The authors linked the gap to how rarely ultrasound was performed and to its dependence on the operator.

In these terms, the accuracy reported in a paper measures efficacy. I believe medical AI has the same gap as ultrasound, and often a wider one. A model cannot adjust to a poor input or to a new kind of patient the way that a clinician can. In AI the gap usually opens in two places. The first is integration, which means whether a usable input reaches the model and whether its result reaches a clinician in time. Integration depends on the clinic as much as on the software. The second is the patients, who change over time while the model stays the same.

<figure>
<div class="split" role="img" aria-label="Left: in everyday clinics in Thailand, an eye-screening model rejected 21 percent of retinal photos as ungradable in the first six months, often because of poor lighting. Right: three jobs that must work for an imaging model to help a patient. One, the right images reach the model, sent automatically so that no one has to remember. Two, the result reaches the clinician in time, which for a radiologist means before the report is signed. Three, someone owns re-checking the tool, a named person who checks it again after any change in scanner, protocol or patients.">
<div class="statpanel"><p class="k">Diabetic eye screening · clinics in Thailand</p><p class="big">21%</p><p>of retinal photos rejected as ungradable in the first six months, often because of poor lighting</p></div>
<ol class="steps">
<li><b>The right images reach the model</b>Sent automatically, so that no one has to remember</li>
<li><b>The result reaches the clinician in time</b>For a radiologist, before the report is signed</li>
<li><b>Someone owns re-checking the tool</b>A named person who checks it again after any change in scanner, protocol or patients</li>
</ol>
</div>
<figcaption><b>Figure 1. An accurate model and the three jobs around it.</b> The left panel shows the share of photos that the eye-screening model could not grade in everyday clinics in Thailand (393 of 1,838); section 02 describes the study. On the right are the three practical jobs that must work before an imaging model can help a patient; this division is my own. Data: <a href="https://doi.org/10.1145/3313831.3376718">Beede et al., CHI 2020</a>.</figcaption>
</figure>

</section>

<section id="thailand">

## <span class="n">02</span>An accurate model in real clinics

Diabetic retinopathy is damage to the retina's blood vessels caused by diabetes, and Thailand's national screening program for it shows both sides of the gap. Nurses photograph the retina during routine diabetes care and send the images to an ophthalmologist, and the result could take up to 10 weeks. Google had developed a model that grades these photographs, and the plan was to grade each photograph in the clinic and give patients their result before they left.

<figure class="fig-svg" id="fig-paths">
<svg viewBox="0 0 560 280" role="img" aria-label="Schematic, not a real image, of two paths from a retinal photograph to its result. Before the model, the photos went to an ophthalmologist by email or on a compact disc by mail, and the result came up to 10 weeks later; this path is drawn as a long gray bar. With the model, the plan was to upload each photo for grading while the patient waits and to give the result before the patient leaves; this path is drawn as a short blue bar. The bar lengths are not to scale.">
<text x="0" y="24" style="font-size: 21px; font-weight: 700; fill: var(--ink)">Before the model</text>
<rect x="0" y="38" width="560" height="80" rx="4" style="fill: var(--stone)"/>
<text x="14" y="71" style="font-size: 19px; fill: var(--ink-2)">Photos go to an ophthalmologist by email</text>
<text x="14" y="99" style="font-size: 19px; fill: var(--ink-2)">or on a compact disc by mail</text>
<text x="560" y="148" text-anchor="end" style="font-size: 20px; font-weight: 700; fill: var(--ink)">Result up to 10 weeks later</text>
<text x="0" y="198" style="font-size: 21px; font-weight: 700; fill: var(--ink)">Planned with the model</text>
<rect x="0" y="212" width="100" height="56" rx="4" style="fill: var(--sig)"/>
<text x="116" y="236" style="font-size: 20px; font-weight: 700; fill: var(--sig-ink)">Result before the patient leaves</text>
<text x="116" y="262" style="font-size: 19px; fill: var(--ink-3)">Uploaded and graded while the patient waits</text>
</svg>
<figcaption><b>Figure 2. The change that the model was meant to bring.</b> Compare the two bars. Before the model, the result of a screening photograph could take up to 10 weeks. With the model, the plan was to give each patient the result during the same visit. The bar lengths are not to scale. <span class="credit">Schematic, not a real image. Drawn from the description in <a href="https://doi.org/10.1145/3313831.3376718">Beede et al., CHI 2020</a>.</span></figcaption>
</figure>

Researchers at Google and Rajavithi Hospital in Bangkok ran a [field study of this plan](https://doi.org/10.1145/3313831.3376718). They observed and interviewed nurses at 11 clinics before deployment, and again at the three clinics where the system went live. Most of the problems that they found were outside the model.

**Photo quality.** A clear retinal photograph needs a large pupil, which requires a dark room, dilating drops or both. Only two of the 11 clinics had a screening room that could be darkened, and the clinics where the system went live did not use dilating drops. For patient safety, the system was designed to reject any image with a bit of blur or a dark area, because the model might miss disease in such an image. In the first six months, it rejected 393 of 1,838 images (21%) as ungradable.

<figure class="fig-svg" id="fig-fundus">
<svg viewBox="0 0 620 372" role="img" aria-label="Schematic, not a real photograph: two drawings of retinal photographs side by side. Left, taken in a dark room with a large pupil: the whole round image is evenly lit, and the optic disc and the branching blood vessels are sharp. It is labeled graded, no blur and no dark area. Right, taken in a bright room with a small pupil: the vessels and the optic disc are blurred, and a dark shadow covers the lower left part of the image. It is labeled rejected as ungradable, a bit of blur or a dark area.">
<defs>
<g id="fu-vessels" style="fill: none; stroke: var(--sig-4); stroke-linecap: round">
<path d="M-4,-8 C-20,-55 -80,-78 -165,-62" style="stroke-width: 6"/>
<path d="M-4,8 C-20,55 -80,78 -165,62" style="stroke-width: 6"/>
<path d="M-86,-65 C-94,-84 -102,-100 -112,-124" style="stroke-width: 3.5"/>
<path d="M-86,65 C-94,84 -102,100 -112,124" style="stroke-width: 3.5"/>
<path d="M-117,-67 C-121,-54 -124,-42 -128,-26" style="stroke-width: 3"/>
<path d="M-117,67 C-121,54 -124,42 -128,26" style="stroke-width: 3"/>
<path d="M6,-6 C25,-30 45,-55 60,-100" style="stroke-width: 4"/>
<path d="M6,6 C25,30 45,55 60,100" style="stroke-width: 4"/>
<path d="M10,0 C35,-4 55,-8 85,-14" style="stroke-width: 3"/>
<circle cx="0" cy="0" r="17" style="fill: var(--amber); stroke: none"/>
</g>
<clipPath id="fu-clip-l"><circle cx="155" cy="170" r="112"/></clipPath>
<clipPath id="fu-clip-r"><circle cx="465" cy="170" r="112"/></clipPath>
<filter id="fu-blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.2"/></filter>
<filter id="fu-shade" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="12"/></filter>
</defs>
<text x="155" y="30" text-anchor="middle" style="font-size: 20px; fill: var(--ink-2)">Dark room, large pupil</text>
<text x="465" y="30" text-anchor="middle" style="font-size: 20px; fill: var(--ink-2)">Bright room, small pupil</text>
<circle cx="155" cy="170" r="112" style="fill: var(--sig-soft)"/>
<g clip-path="url(#fu-clip-l)"><use href="#fu-vessels" transform="translate(199,170)"/></g>
<circle cx="155" cy="170" r="112" style="fill: none; stroke: var(--sig-3); stroke-width: 2"/>
<circle cx="465" cy="170" r="112" style="fill: var(--sig-soft)"/>
<g clip-path="url(#fu-clip-r)">
<use href="#fu-vessels" transform="translate(509,170)" style="opacity: .75" filter="url(#fu-blur)"/>
<path d="M340,40 H590 V300 H340 Z M490,150 m-109,0 a109,109 0 1,0 218,0 a109,109 0 1,0 -218,0 Z" fill-rule="evenodd" filter="url(#fu-shade)" style="fill: var(--ink-3); opacity: .8"/>
</g>
<circle cx="465" cy="170" r="112" style="fill: none; stroke: var(--sig-3); stroke-width: 2"/>
<text x="155" y="324" text-anchor="middle" style="font-size: 22px; font-weight: 700; fill: var(--sig-ink)">Graded</text>
<text x="155" y="353" text-anchor="middle" style="font-size: 20px; fill: var(--ink-2)">No blur, no dark area</text>
<text x="465" y="324" text-anchor="middle" style="font-size: 22px; font-weight: 700; fill: var(--red)">Rejected as ungradable</text>
<text x="465" y="353" text-anchor="middle" style="font-size: 20px; fill: var(--ink-2)">A bit of blur or a dark area</text>
</svg>
<figcaption><b>Figure 3. What the system graded and what it rejected.</b> Compare the two drawings of retinal photographs. In a dark room the pupil is large, and the whole image is evenly lit and sharp. In a bright room the pupil is small, and a bit of blur or a dark area was enough for the system to reject the image as ungradable. <span class="credit">Schematic, not a real photograph. Drawn from the description in <a href="https://doi.org/10.1145/3313831.3376718">Beede et al., CHI 2020</a>.</span></figcaption>
</figure>

**Workflow.** Some clinics allotted about 90 seconds to each patient. On slow connections, some images took 60 to 90 seconds to upload to the cloud for grading, which is almost all of that time. A positive or ungradable result meant referral to a provincial hospital about an hour's drive away, and not every patient had a car. Nurses were reluctant to send a patient on that trip for an ungradable image alone, given the low likelihood that such a patient had severe retinopathy.

<figure>
<div class="flow" role="img" aria-label="The screening path in the clinics in Thailand. Step one, take the photo: a bright room means a small pupil, and only 2 of 11 clinics could darken the screening room. Step two, upload the photo for grading: some images took 60 to 90 seconds on slow connections, and a two-hour internet outage cut one clinic's screening from 200 to 100 patients. Step three, grade or reject: a bit of blur or a dark area means no grade, and 393 of 1,838 images, 21 percent, were rejected in the first six months. Step four, an ungradable photo means a referral to a hospital about an hour's drive away, and nurses were reluctant to refer a patient for an ungradable photo alone.">
<div class="row"><div class="box"><div class="t1">Take the photo</div><div class="t2">A bright room means a small pupil</div></div><div class="side">2 of 11 clinics could darken the room</div></div>
<div class="conn">the photo is uploaded for grading</div>
<div class="row"><div class="box dark"><div class="t1">Upload</div><div class="t2">Some took 60 to 90 seconds on slow internet</div></div><div class="side">a two-hour outage: 100 patients screened, not 200</div></div>
<div class="conn">a bit of blur or a dark area means no grade</div>
<div class="row"><div class="box dark"><div class="t1">Grade or reject</div><div class="t2">393 of 1,838 images rejected</div></div><div class="side"><span><b>21%</b><br>in the first six months</span></div></div>
<div class="conn">an ungradable photo means a referral</div>
<div class="row"><div class="box line"><div class="t1">Referral</div><div class="t2">A hospital about an hour’s drive away</div></div><div class="side">nurses were reluctant to refer a patient for an ungradable photo alone</div></div>
</div>
<figcaption><b>Figure 4. Where an accurate model got stuck.</b> Follow one photo from the camera to the result. The notes on the right show what the field team observed at each step. Data: <a href="https://doi.org/10.1145/3313831.3376718">Beede et al., CHI 2020</a>.</figcaption>
</figure>

The model's grading accuracy, by contrast, held up. It was measured in parallel in a [prospective interventional cohort study](https://doi.org/10.1016/S2589-7500(22)00017-6) of the same system, with 7,651 patients at nine primary care sites in the national program. Against a reference standard of grades adjudicated by retina specialists, the model had a sensitivity of 91.4% and a specificity of 95.4% for vision-threatening diabetic retinopathy. Specificity is the share of patients without the disease whom a test correctly calls negative. As a safety check, retina specialists over-read every image, and their sensitivity was 84.8%. Even so, the authors concluded that a screening program must plan for the clinics' setting and workflows when it implements such a system.

To me, the accuracy study measured efficacy, which is how well the model graded photographs. The field study measured part of effectiveness, which is how often the clinics could produce a photograph that the model would grade.

</section>

<section id="plumbing">

## <span class="n">03</span>Three practical jobs

A radiology department has the same problem as the eye clinics, and I divide the work into three practical jobs. The first two keep integration working, and the third keeps the model safe when the equipment or the patients change. If any of them fails, the model helps no patient, however accurate it is.

**1. The right images reach the model.** A CT or MRI exam is stored as several series, which are separate stacks of images that differ in slice thickness or reconstruction. A model is usually trained on one kind of series. Software has to select the right series, send it automatically and raise a flag when it never arrives. The selection often depends on a series description that was typed at the scanner, and these descriptions differ between scanners and hospitals. If any step depends on someone remembering, I would assume that it gets missed on the busiest nights.

**2. The result reaches the clinician in time.** In radiology, the practical deadline is the final signed report, because a finding that is added after signing must be communicated separately and may come too late to change care. So the result has to appear in the radiologist's own viewer, attached to the right study, before the report is signed.

**3. Someone owns re-checking the tool.** Hospitals replace scanners, update software and change their acquisition protocols, which are the scanner settings used for each type of exam. Each change can alter the images that a model receives. A [letter in the New England Journal of Medicine](https://doi.org/10.1056/NEJMc2104626) describes a model for detecting hip fractures on radiographs. Part of what it had learned was which type of scanner and which technician had taken the image. The letter advises watching actively for new acquisition devices and protocols, and asking frontline clinicians to flag protocol changes. I would make one named person responsible for both.

Shared standards help. Integrating the Healthcare Enterprise (IHE) is an initiative of healthcare professionals and industry. It publishes profiles, which are agreed specifications for how systems from different vendors exchange information. Three of its profiles for AI in radiology match the three jobs (Figure 5). One specifies how an AI task is [requested, performed and monitored](https://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_Suppl_AIW-I.pdf), and another how [AI results are stored and displayed](https://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_Suppl_AIR.pdf) in the radiologist's viewer. The third specifies how to [record whether the radiologist accepted or rejected each result](https://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_Suppl_AIRA.pdf). All three are still in trial implementation, which means that they are published for testing and may change. I am a member of IHE, where I help develop guidelines for AI standards, so I am a bit biased. Still, asking a vendor which of these profiles a product supports is a fair question.

<figure>
<table class="data">
<thead><tr><th>Job</th><th>What can go wrong</th><th>What helps</th></tr></thead>
<tbody>
<tr><td><b>1</b><span>The right images reach the model</span></td><td>The wrong series is sent, or nothing is sent</td><td>Automatic routing; the IHE profile for AI workflow</td></tr>
<tr><td><b>2</b><span>The result reaches the clinician in time</span></td><td>The result arrives after the report is signed, or outside the viewer</td><td>Results shown in the reading viewer; the IHE profile for AI results</td></tr>
<tr><td><b>3</b><span>Someone re-checks the tool after a change</span></td><td class="hi">Performance changes after a new scanner, protocol, software version or patient mix, and no one notices</td><td>A named owner and a monitoring page; the IHE profile for assessing AI results</td></tr>
</tbody>
</table>
<figcaption><b>Figure 5. Three jobs, what can go wrong, and what helps.</b> Read each row from left to right. The examples of what can go wrong are mine. Standards: IHE Radiology supplements on <a href="https://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_Suppl_AIW-I.pdf">AI workflow for imaging</a>, <a href="https://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_Suppl_AIR.pdf">AI results</a> and <a href="https://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_Suppl_AIRA.pdf">AI result assessment</a>, all in trial implementation. Changes to watch for: <a href="https://doi.org/10.1056/NEJMc2104626">Finlayson et al., NEJM 2021</a>.</figcaption>
</figure>

</section>

<section id="drift">

## <span class="n">04</span>When the patients change

I find the third job the hardest, because sometimes nothing in the department changes except the patients. Dataset shift, also called drift, is a mismatch between the data that a model receives in use and the data on which it was developed. It can lower the model's performance.

A [retrospective multicenter study](https://doi.org/10.1001/jamanetworkopen.2021.35286) counted sepsis alerts in 24 US hospitals from four health systems. Sepsis is life-threatening organ dysfunction caused by the body's response to an infection, most often a bacterial one. All 24 hospitals used the Epic Sepsis Model, a proprietary model from Epic, which sells electronic health records. In the three weeks before each hospital's first COVID-19 case, 9% of hospitalized patients triggered a sepsis alert each day. In the three weeks after, 21% did. The number of inpatients fell by 35%, yet the total number of alerts per day rose by 43%.

<figure>
<div class="hbars" role="img" aria-label="Share of hospitalized patients who triggered a sepsis alert each day across 24 US hospitals: 9 percent in the three weeks before each hospital’s first COVID-19 case, 21 percent in the three weeks after.">
<p class="grp">Hospitalized patients who triggered a sepsis alert each day, 24 US hospitals</p>
<div class="r"><span class="t">3 weeks before the first COVID-19 case</span><div class="track"><div class="bar" style="width:36%;background:var(--ctx)"></div></div><span class="v">9%</span></div>
<div class="r"><span class="t">3 weeks after</span><div class="track"><div class="bar" style="width:84%;background:var(--emph)"></div></div><span class="v">21%</span></div>
</div>
<figcaption><b>Figure 6. The same model, different patients.</b> Compare the two bars, which show the share of inpatients flagged each day by the Epic Sepsis Model before and after each hospital's first COVID-19 case. The bars are drawn on a 0 to 25% scale. Total alerts per day rose 43% while the number of inpatients fell 35%. Data: <a href="https://doi.org/10.1001/jamanetworkopen.2021.35286">Wong et al., JAMA Network Open 2021</a>.</figcaption>
</figure>

The study counted alerts and did not measure accuracy. Part of the rise is clinically plausible, because elective surgery was cancelled and the patients who remained in hospital were sicker. At the University of Michigan, nurses reported overalerting, and the hospital paused the alerts in April 2020. The model for hip fractures was described in a letter in the New England Journal of Medicine, and the same letter explains what happened at Michigan. In its authors' words, "dataset shift fundamentally altered the relationship between fevers and bacterial sepsis," and the hospital's committee that governs clinical AI decommissioned the model. My reading is that COVID-19 brought many febrile patients with a viral infection. A fever therefore pointed to bacterial sepsis less often than it had in the data on which the model was developed.

<figure class="fig-img" id="fig-wong">
<a href="/assets/img/blog/efficacy-is-not-effectiveness/wong-2021-figure1.jpg"><img src="/assets/img/blog/efficacy-is-not-effectiveness/wong-2021-figure1.jpg" width="780" height="438" loading="lazy" alt="Line chart from the 24-hospital study. The horizontal axis shows days from each hospital's first COVID-19 case, from about 56 days before to 35 days after. A light gray area shows the total number of inpatients across the hospitals, which is steady before day 0 and falls after it. One thin colored line per hospital, darker for hospitals with more beds, and a thick black line for their average show the percentage of patients who generated sepsis alerts each day. The black line stays near 9% before day 0 and climbs above 20% within about four weeks after it, and most hospital lines rise with it. A gray dashed vertical line marks the first COVID-19 case, and an orange dashed line about three weeks later marks the day the University of Michigan paused its sepsis alerts."></a>
<figcaption><b>Figure 7. The same rise, hospital by hospital.</b> Each thin line is one hospital (darker lines are hospitals with more beds), and the thick black line is the average. The light gray area is the total number of inpatients, read on the right-hand axis. After day 0, the week of each hospital's first COVID-19 case, the gray area falls while the black line rises. The orange dashed line marks the day the University of Michigan paused its alerts. <span class="credit">Image: Wong A, Cao J, Lyons PG, et al., JAMA Network Open 2021, Figure 1, <a href="https://jamanetwork.com/pages/cc-by-license-permissions">CC BY</a>. © 2021 Wong A et al. JAMA Network Open. <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC8605481/">Full article on PubMed Central</a>.</span></figcaption>
</figure>

The letter's authors also ask clinicians to notice when a model's predictions stop matching their own clinical judgment. In both cases in this post, the staff who used the tool noticed the problem early. The Thai clinics reported the ungradable images before the research team reviewed the system logs, and Michigan's nurses reported the overalerting. I believe it is a clinical skill to notice when a tool's output no longer fits the patients, and a local owner should make such reports easy to send.

</section>

<section id="ownership">

## <span class="n">05</span>A local owner who can switch it off

Re-checking a tool requires a local owner, who can be one person or a small team. The owner watches the tool on local patients, receives reports from clinicians and can switch the tool off. The most complete published example that I know is Sepsis Watch at Duke. It is a deep learning model that predicts sepsis and sends its high-risk alerts to a nurse on the rapid response team. The Duke team [described the implementation](https://doi.org/10.2196/15182) in detail.

First, the model ran silently for three months. In a silent deployment, also called silent mode, the model runs on live patient data, but its output is not yet part of routine care. The team used this period to confirm that each value from the health record was mapped correctly to the model's inputs. It also built two monitoring pages. One checked the live connection to the health record, and the other showed daily and weekly counts and averages of the model's inputs and outputs. A committee of nursing, physician and administrative leaders reviewed weekly reports, including compliance with the sepsis bundle (the standard set of early treatments). Personnel time for the project came to about 8,000 hours, not counting trainees. By my arithmetic, that is roughly four people working full time for a year.

<figure class="fig-svg" id="fig-sepsiswatch">
<svg viewBox="0 0 660 552" role="img" aria-label="Schematic, not a real image, of the setup around Sepsis Watch at Duke. At the top, a timeline: three months of silent mode before launch, on live data, then launch, after which high-risk alerts go to a nurse. In the middle, the path of an alert: the health record feeds the Sepsis Watch deep learning model, which updates each patient's risk every hour and sends high-risk alerts to a rapid response nurse. Below it, two monitoring pages. Page 1 checks whether the live connection to the health record is working. Page 2 shows daily and weekly counts and mean values of the model's inputs and outputs. At the bottom, a weekly report on alert volume and sepsis bundle compliance goes to the rapid response nurses and to a committee of nursing, physician and administrative leaders.">
<defs>
<marker id="sw-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" style="fill: var(--ink-3)"/></marker>
</defs>
<polygon points="0,0 300,0 320,40 300,80 0,80" style="fill: var(--stone)"/>
<text x="18" y="34" style="font-size: 22px; font-weight: 700; fill: var(--ink)">Silent mode, 3 months</text>
<text x="18" y="63" style="font-size: 20px; fill: var(--ink-2)">before launch, on live data</text>
<rect x="330" y="0" width="330" height="80" rx="4" style="fill: var(--sig)"/>
<text x="348" y="34" style="font-size: 22px; font-weight: 700; fill: var(--on-fill)">After launch</text>
<text x="348" y="63" style="font-size: 20px; fill: var(--sig-on)">high-risk alerts go to a nurse</text>
<rect x="0" y="114" width="190" height="104" rx="4" style="fill: var(--surface); stroke: var(--rule-2); stroke-width: 1.5"/>
<text x="95" y="149" text-anchor="middle" style="font-size: 21px; font-weight: 700; fill: var(--ink)">Health record</text>
<text x="95" y="177" text-anchor="middle" style="font-size: 20px; fill: var(--ink-2)">live patient</text>
<text x="95" y="202" text-anchor="middle" style="font-size: 20px; fill: var(--ink-2)">data</text>
<rect x="235" y="114" width="190" height="104" rx="4" style="fill: var(--sig)"/>
<text x="330" y="149" text-anchor="middle" style="font-size: 21px; font-weight: 700; fill: var(--on-fill)">Sepsis Watch</text>
<text x="330" y="177" text-anchor="middle" style="font-size: 20px; fill: var(--sig-on)">deep learning</text>
<text x="330" y="202" text-anchor="middle" style="font-size: 20px; fill: var(--sig-on)">model</text>
<rect x="470" y="114" width="190" height="104" rx="4" style="fill: var(--sig-soft); stroke: var(--sig); stroke-width: 1.5"/>
<text x="565" y="146" text-anchor="middle" style="font-size: 21px; font-weight: 700; fill: var(--sig-ink)">Rapid response</text>
<text x="565" y="171" text-anchor="middle" style="font-size: 21px; font-weight: 700; fill: var(--sig-ink)">nurse</text>
<text x="565" y="202" text-anchor="middle" style="font-size: 20px; fill: var(--ink-2)">high-risk alerts</text>
<line x1="192" y1="166" x2="231" y2="166" marker-end="url(#sw-arrow)" style="stroke: var(--ink-3); stroke-width: 2"/>
<line x1="427" y1="166" x2="466" y2="166" marker-end="url(#sw-arrow)" style="stroke: var(--ink-3); stroke-width: 2"/>
<line x1="212" y1="172" x2="212" y2="256" style="stroke: var(--sig-3); stroke-width: 2; stroke-dasharray: 5 5"/>
<line x1="400" y1="218" x2="400" y2="256" style="stroke: var(--sig-3); stroke-width: 2; stroke-dasharray: 5 5"/>
<rect x="0" y="256" width="318" height="138" rx="4" style="fill: var(--sig-soft); stroke: var(--sig-3); stroke-width: 1.5"/>
<text x="16" y="290" style="font-size: 21px; font-weight: 700; fill: var(--sig-ink)">Monitoring page 1</text>
<text x="16" y="319" style="font-size: 20px; fill: var(--ink-2)">Is the live connection</text>
<text x="16" y="346" style="font-size: 20px; fill: var(--ink-2)">to the health record</text>
<text x="16" y="373" style="font-size: 20px; fill: var(--ink-2)">working?</text>
<rect x="342" y="256" width="318" height="138" rx="4" style="fill: var(--sig-soft); stroke: var(--sig-3); stroke-width: 1.5"/>
<text x="358" y="290" style="font-size: 21px; font-weight: 700; fill: var(--sig-ink)">Monitoring page 2</text>
<text x="358" y="319" style="font-size: 20px; fill: var(--ink-2)">Daily and weekly counts</text>
<text x="358" y="346" style="font-size: 20px; fill: var(--ink-2)">and mean values of the</text>
<text x="358" y="373" style="font-size: 20px; fill: var(--ink-2)">model's inputs and outputs</text>
<rect x="0" y="428" width="660" height="118" rx="4" style="fill: var(--panel); stroke: var(--rule-2); stroke-width: 1.5"/>
<text x="16" y="462" style="font-size: 21px; font-weight: 700; fill: var(--ink)">Weekly report: alert volume and bundle compliance</text>
<text x="16" y="492" style="font-size: 20px; fill: var(--ink-2)">sent to the rapid response nurses and to a committee</text>
<text x="16" y="520" style="font-size: 20px; fill: var(--ink-2)">of nursing, physician and administrative leaders</text>
</svg>
<figcaption><b>Figure 8. The setup around Sepsis Watch at Duke.</b> Read from the top. The model first ran in silent mode for three months before its alerts reached nurses. Two monitoring pages checked the connection to the health record and summarized the model's inputs and outputs. A weekly report went to the nurses and to a committee of clinical and administrative leaders. <span class="credit">Schematic, not a real image. Drawn from the description in <a href="https://doi.org/10.2196/15182">Sendak et al., JMIR Medical Informatics 2020</a>.</span></figcaption>
</figure>

The same group proposed a one-page summary of a model for clinicians, which they call a ["Model Facts" label](https://doi.org/10.1038/s41746-020-0253-3) by analogy with the package insert for a drug. They argue that this summary has to be localized and updated over time, as a hospital's antibiogram is. An antibiogram is a yearly table of how often the bacteria isolated at that hospital are susceptible to each antibiotic.

Regulation covers only part of this. In December 2024, the US Food and Drug Administration (FDA) issued final [guidance on predetermined change control plans](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence). Under it, a manufacturer can have its planned model updates reviewed in advance, together with the methods that it will use to validate them. Such a plan covers the changes that the manufacturer intends to make. It does not cover changes at a hospital, such as a new scanner in one department or a sudden change in the patient mix. The authors of the 24-hospital study argued that health systems that use AI-based alerts are responsible for being able to assess them rapidly and to disable them.

In practice, the owner needs a monitoring page of the tool's daily inputs and outputs, and clinicians need a known way to report problems to the owner. After a change in scanner, protocol or software, I would also run the tool silently again before it returns to routine care. During that period, the owner can compare the share of positive results and the distribution of the inputs with those of the previous period.

</section>

<section id="ask">

## <span class="n">06</span>Questions to ask about any AI tool

These questions are fair to ask whoever runs an AI tool in your department.

<ol class="num-list">
<li><strong>How does the input reach the model?</strong> Are the images or the values from the health record sent automatically, and what happens when they never arrive?<span class="an">Job 1</span></li>
<li><strong>Where and when do I see the result?</strong> Is it in my usual viewer or worklist, before I make the decision that it is meant to inform?<span class="an">Job 2</span></li>
<li><strong>Who is the named owner?</strong> How do I tell them when the equipment, the protocol or the patients change?<span class="an">Job 3</span></li>
<li><strong>Did it run in silent mode here first?</strong> Was that at this hospital, on this equipment and these patients?<span class="an">Like a parallel run of a new lab analyzer</span></li>
<li><strong>Is there a local “Model Facts” label?</strong> When was it last updated?<span class="an">Like an antibiogram</span></li>
</ol>

Across this series, I have argued that the model is rarely the part that fails first. The [overview of the series](/blog/the-model-is-not-the-hard-part/) brings together the questions for every stage, from the data to deployment.

</section>

<section id="sources">

## <span class="n">A</span>Sources

<ol class="refs">
  <li>Singal AG, Higgins PDR, Waljee AK. <a href="https://doi.org/10.1038/ctg.2013.13">A primer on effectiveness and efficacy trials.</a> Clin Transl Gastroenterol 2014;5:e45.</li>
  <li>Beede E, et al. <a href="https://doi.org/10.1145/3313831.3376718">A human-centered evaluation of a deep learning system deployed in clinics for the detection of diabetic retinopathy.</a> CHI 2020.</li>
  <li>Ruamviboonsuk P, et al. <a href="https://doi.org/10.1016/S2589-7500(22)00017-6">Real-time diabetic retinopathy screening by deep learning in a multisite national screening programme: a prospective interventional cohort study.</a> Lancet Digit Health 2022;4:e235-44.</li>
  <li>Finlayson SG, Subbaswamy A, Singh K, et al. <a href="https://doi.org/10.1056/NEJMc2104626">The clinician and dataset shift in artificial intelligence.</a> N Engl J Med 2021;385:283-6.</li>
  <li>IHE Radiology Technical Committee. <a href="https://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_Suppl_AIW-I.pdf">IHE Radiology Technical Framework Supplement: AI Workflow for Imaging (AIW-I).</a> Rev. 1.1, trial implementation. IHE International; 2020.</li>
  <li>IHE Radiology Technical Committee. <a href="https://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_Suppl_AIR.pdf">IHE Radiology Technical Framework Supplement: AI Results (AIR).</a> Rev. 1.3, trial implementation. IHE International; 2025.</li>
  <li>IHE Radiology Technical Committee. <a href="https://www.ihe.net/uploadedFiles/Documents/Radiology/IHE_RAD_Suppl_AIRA.pdf">IHE Radiology Technical Framework Supplement: AI Result Assessment for Imaging (AIRA).</a> Rev. 1.1, trial implementation. IHE International; 2025.</li>
  <li>Wong A, et al. <a href="https://doi.org/10.1001/jamanetworkopen.2021.35286">Quantification of sepsis model alerts in 24 US hospitals before and during the COVID-19 pandemic.</a> JAMA Netw Open 2021;4:e2135286.</li>
  <li>Sendak MP, et al. <a href="https://doi.org/10.2196/15182">Real-world integration of a sepsis deep learning technology into routine clinical care: implementation study.</a> JMIR Med Inform 2020;8:e15182.</li>
  <li>Sendak MP, Gao M, Brajer N, Balu S. <a href="https://doi.org/10.1038/s41746-020-0253-3">Presenting machine learning model information to clinical end users with model facts labels.</a> npj Digit Med 2020;3:41.</li>
  <li>US Food and Drug Administration. <a href="https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence">Marketing submission recommendations for a predetermined change control plan for artificial intelligence-enabled device software functions.</a> Guidance for industry and FDA staff. Originally issued 4 December 2024; current version issued 18 August 2025.</li>
</ol>

</section>
