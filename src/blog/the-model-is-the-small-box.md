---
title: The model is the small box
description: Many failures of medical machine-learning tools start in the training data, the labels or the evaluation, and clinicians are well placed to find them.
dek: The model is a small part of a medical AI system. Many failures start in how the training images were collected, how the correct answers were assigned and how performance was measured, and clinicians are well placed to find them.
summary: A melanoma model misread far more benign moles as melanoma once they were marked with the ink that surgeons use before removing a lesion. This post explains why finding such failures needs clinical knowledge, because they start in the training data, the labels and the evaluation rather than in the model.
date: 2026-11-10
topic: Evaluating medical AI
labels: ["Clinical foundations", "Data"]
series: clinical-foundations
part: 1
ogImage: /assets/img/blog/the-model-is-the-small-box/og.png
ogImageAlt: "Title card reading The model is the small box, with the label Clinical foundations of medical AI and the author name Ali Ganjizadeh, MD, MBA. A grid of nine tiles shows the parts of a medical AI system, with the model as a small label in the center tile. The tiles for data provenance, label definition and evaluation are highlighted."
disclosure: I work at HOPPR, which builds AI for medical imaging. This post has no product content, and every study in it is independent of my company. The views are my own.
toc:
  - { id: "tldr", n: "·", label: "Take-home messages" }
  - { id: "small-box", n: "01", label: "The model is the small box" }
  - { id: "terms", n: "02", label: "Model, label and threshold" }
  - { id: "provenance", n: "03", label: "Shortcuts in the data" }
  - { id: "label", n: "04", label: "How the labels were made" }
  - { id: "evaluation", n: "05", label: "Subgroups and new hospitals" }
  - { id: "who-notices", n: "06", label: "Who finds the problems" }
  - { id: "ask", n: "07", label: "Questions to ask" }
  - { id: "sources", n: "A", label: "Sources" }
---

<div class="tiles">
<div class="tile"><div class="v">84 → 46%</div><div class="l">specificity of a melanoma classifier approved in Europe on the same benign moles, unmarked and then marked with surgical ink</div></div>
<div class="tile"><div class="v">0.94 vs 0.77</div><div class="l">AUC of a pneumothorax model on chest X-rays with a chest drain and on X-rays without one (0.5 is chance)</div></div>
</div>

<section id="tldr" class="tldr">
<span class="lbl">Take-home messages</span>
<ul>
<li><strong>Many failures start outside the model.</strong> Well-documented failures of imaging models have come from how the training images were collected, how the correct answers were assigned or how performance was measured. People with clinical training found several of them.</li>
<li><strong>A model learns whatever separates its positive examples from its negative ones.</strong> Imaging models have used surgical ink and visible chest drains in place of the disease, and they can also learn which hospital an X-ray came from. So take positive and negative examples from the same hospitals, machines and stages of care.</li>
<li><strong>Errors in the labels become errors in the model.</strong> A label is the answer that a model is trained to reproduce for each example, such as "pneumonia" or "no pneumonia" for one chest X-ray. Ask which reference standard, such as biopsy, set the labels, because labels that dermatologists assigned from photographs alone missed more skin cancers on dark skin than on light skin.</li>
<li><strong>A model can do well on average and poorly in the patients who matter most.</strong> A model for collapsed lung (pneumothorax) was less accurate on chest X-rays without a chest drain, the tube used to treat it. Patients without a drain are more likely to still need treatment, so ask for results in each clinically important subgroup.</li>
<li><strong>Bring clinicians into the data work from the start.</strong> Have a clinician review the cases that the model gets wrong, and test the model at a hospital that contributed no training data.</li>
</ul>
</section>

<section id="small-box">

## <span class="n">01</span>The model is the small box

A medical AI tool exists to support a clinical decision, such as whether a chest X-ray needs urgent review. I believe that most failures of such a tool start outside the model, in the training data, the labels and the evaluation. Each of these is a clinical question as much as a technical one.

Engineers made a related observation in 2015, when a team at Google published [Hidden Technical Debt in Machine Learning Systems](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html). Technical debt is the engineers' term for the cost that a team pays later for building software quickly. The paper's first figure shows a tiny black box labeled "ML Code" among much larger boxes for data collection, configuration, monitoring and other work. Its caption says that only a small fraction of a real-world system is the machine-learning code. For medicine, I redraw that figure as nine tiles.

<figure>
<div class="grid9" role="img" aria-label="Nine tiles of a medical AI system. The model is a small label in the empty center tile. Data provenance, label definition and evaluation are highlighted as the tiles that need clinical knowledge most; data pipelines, infrastructure, integration, monitoring and governance are engineering and operations.">
<div class="g">Data pipelines</div>
<div class="g edge">Data provenance<small>Why each image exists</small></div>
<div class="g">Infrastructure</div>
<div class="g edge">Label definition<small>Which outcome matters, and when</small></div>
<div class="g model"><span>Model</span></div>
<div class="g edge">Evaluation<small>What the numbers mean for your patients</small></div>
<div class="g">Integration</div>
<div class="g">Monitoring</div>
<div class="g">Governance</div>
</div>
<div class="legend"><span><i class="sw-ctx"></i>questions that need clinical knowledge</span><span><i class="sw-frozen"></i>engineering and operations</span><span><i class="sw-ink"></i>the model</span></div>
<figcaption><b>Figure 1. The parts of a medical AI system.</b> Look at the small Model label in the empty center tile and the three highlighted tiles around it, which are the questions that need clinical knowledge most. Adapted from Figure 1 of <a href="https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html">Sculley et al., NeurIPS 2015</a>; the nine tiles and their clinical labels are mine.</figcaption>
</figure>

The three highlighted tiles are where clinical training helps most, because each depends on knowing how clinical care works. The other five tiles are engineering and operations, and [a later post in this series](/blog/efficacy-is-not-effectiveness/#plumbing) returns to integration and monitoring.

</section>

<section id="terms">

## <span class="n">02</span>Model, label and threshold

A model is a function that converts an input, such as a chest radiograph, into a score, such as the probability of pneumonia. Its rules are not written by hand but fitted to training data, a set of examples in which each input is paired with a label. The label is the answer that the model is trained to reproduce. It plays the role of the reference standard, such as biopsy, in a study of diagnostic accuracy, so errors in the labels become errors in the model. The model will also use any feature that separates the positive examples from the negative ones, whether or not that feature belongs to the disease. Such a feature is called a shortcut.

A score becomes a positive or negative result at a threshold. Sensitivity is the proportion of patients with the condition whom the model calls positive, and specificity is the proportion without it whom the model calls negative. The receiver operating characteristic (ROC) curve plots sensitivity against 1 minus specificity at every threshold. The area under this curve (AUC) is the [probability that the model ranks a randomly chosen patient with the outcome above one without it](https://doi.org/10.1148/radiology.143.1.7063747). An AUC of 0.5 is chance and 1.0 is perfect. This AUC is unrelated to the pharmacokinetic AUC of drug exposure.

</section>

<section id="provenance">

## <span class="n">03</span>Data provenance: shortcuts in the data

Data provenance is the record of where each example came from and why it was created. A medical image exists because a clinician ordered it, at a particular hospital, on a particular machine and at a particular stage of a patient's care. When these circumstances differ between the positive and the negative examples, they leave traces in the images, and a model can learn the traces instead of the disease. In each of the four cases below, the authors showed that a model learned such a trace or could learn it.

**Melanoma and surgical ink.** In 2019, [dermatologists from Heidelberg and other European centers](https://doi.org/10.1001/jamadermatol.2019.1735) tested a melanoma classifier that was already approved as a medical device in Europe. They imaged 107 benign nevi (moles) and 23 melanomas with a dermatoscope, which takes magnified photographs of the skin. Each lesion was imaged unmarked and again after marking with the gentian violet ink that surgeons use before an excision. On the same benign nevi, specificity fell from 84% to 46% with ink. A heat map colors the parts of an image that most influenced the score, and here the heat maps linked the ink to the false positives. Cropping the ink out of the images raised specificity to 97%. The authors hypothesize that skin markings were more common among the melanomas in the training data. In that case the model could have learned that ink means melanoma, although the ink only records a surgeon's concern.

<figure class="fig-svg" id="fig-ink">
<svg viewBox="0 0 640 312" role="img" aria-label="Schematic of the ink experiment. Three drawings of the same benign mole on skin: unmarked, marked with blue surgical ink in streaks and dots on the skin beside it, and cropped close to the mole so that the ink is out of the image. Under each drawing, a bar gives the classifier's specificity on the 107 benign moles: 84% unmarked, 46% marked and 97% with the ink cropped out.">
<text x="108" y="30" text-anchor="middle" style="font-size:22px;font-weight:600;fill:var(--ink)">Unmarked</text>
<text x="320" y="30" text-anchor="middle" style="font-size:22px;font-weight:600;fill:var(--ink)">Marked with ink</text>
<text x="532" y="30" text-anchor="middle" style="font-size:22px;font-weight:600;fill:var(--ink)">Ink cropped out</text>
<rect x="15" y="44" width="186" height="168" rx="6" style="fill:var(--amber-soft);stroke:var(--rule-2)"/>
<rect x="227" y="44" width="186" height="168" rx="6" style="fill:var(--amber-soft);stroke:var(--rule-2)"/>
<rect x="439" y="44" width="186" height="168" rx="6" style="fill:var(--amber-soft);stroke:var(--rule-2)"/>
<g transform="translate(108 128)">
<path d="M-34,-6 C-36,-26 -16,-38 4,-36 C26,-34 38,-18 36,2 C34,24 18,36 -2,35 C-24,34 -32,14 -34,-6 Z" style="fill:var(--amber-deep);opacity:.8"/>
<path d="M-20,-4 C-21,-16 -9,-22 3,-21 C16,-20 22,-10 21,1 C20,14 10,21 -1,20 C-14,20 -19,8 -20,-4 Z" style="fill:var(--amber-ink)"/>
</g>
<g transform="translate(320 128)">
<path d="M-34,-6 C-36,-26 -16,-38 4,-36 C26,-34 38,-18 36,2 C34,24 18,36 -2,35 C-24,34 -32,14 -34,-6 Z" style="fill:var(--amber-deep);opacity:.8"/>
<path d="M-20,-4 C-21,-16 -9,-22 3,-21 C16,-20 22,-10 21,1 C20,14 10,21 -1,20 C-14,20 -19,8 -20,-4 Z" style="fill:var(--amber-ink)"/>
</g>
<path d="M364,190 C372,180 380,172 388,162 C394,154 398,148 402,140" style="fill:none;stroke:var(--sig-4);stroke-width:6;stroke-linecap:round"/>
<path d="M244,76 C254,72 264,70 278,71" style="fill:none;stroke:var(--sig-4);stroke-width:5;stroke-linecap:round"/>
<circle cx="390" cy="88" r="4.5" style="fill:var(--sig-4)"/>
<circle cx="402" cy="108" r="4" style="fill:var(--sig-4)"/>
<circle cx="252" cy="186" r="4" style="fill:var(--sig-4)"/>
<g transform="translate(532 128) scale(1.65)">
<path d="M-34,-6 C-36,-26 -16,-38 4,-36 C26,-34 38,-18 36,2 C34,24 18,36 -2,35 C-24,34 -32,14 -34,-6 Z" style="fill:var(--amber-deep);opacity:.8"/>
<path d="M-20,-4 C-21,-16 -9,-22 3,-21 C16,-20 22,-10 21,1 C20,14 10,21 -1,20 C-14,20 -19,8 -20,-4 Z" style="fill:var(--amber-ink)"/>
</g>
<text x="320" y="242" text-anchor="middle" style="font-size:21px;fill:var(--ink-3)">Specificity on the 107 benign moles</text>
<rect x="15" y="254" width="186" height="16" rx="3" style="fill:var(--panel)"/>
<rect x="15" y="254" width="156" height="16" rx="3" style="fill:var(--sig)"/>
<rect x="227" y="254" width="186" height="16" rx="3" style="fill:var(--panel)"/>
<rect x="227" y="254" width="86" height="16" rx="3" style="fill:var(--red)"/>
<rect x="439" y="254" width="186" height="16" rx="3" style="fill:var(--panel)"/>
<rect x="439" y="254" width="180" height="16" rx="3" style="fill:var(--sig)"/>
<text x="108" y="300" text-anchor="middle" style="font-size:27px;font-weight:700;fill:var(--sig)">84%</text>
<text x="320" y="300" text-anchor="middle" style="font-size:27px;font-weight:700;fill:var(--red)">46%</text>
<text x="532" y="300" text-anchor="middle" style="font-size:27px;font-weight:700;fill:var(--sig)">97%</text>
</svg>
<figcaption><b>Figure 2. The ink experiment.</b> The same benign mole is drawn without ink, with ink on the skin beside it, and cropped so that the ink is out of the image. Compare the bars, which give the classifier’s specificity on all 107 benign moles in each condition, on a scale from 0 to 100%. The authors describe the ink as dots, streaks or circles on the skin next to each mole. <span class="credit">Schematic, not a real image. Drawn from the description in <a href="https://doi.org/10.1001/jamadermatol.2019.1735">Winkler et al., JAMA Dermatology 2019</a>, where the real dermoscopic images appear.</span></figcaption>
</figure>

**Pneumonia and the hospital.** [Zech and colleagues](https://doi.org/10.1371/journal.pmed.1002683) trained pneumonia models on chest radiographs from three US hospital systems, including Mount Sinai Hospital and the National Institutes of Health (NIH) Clinical Center. Prevalence is the proportion of films that show the disease. It was 34% at Mount Sinai and about 1% at the other two systems. The authors trained a separate model to predict the hospital system instead of the disease, and it identified the hospital for more than 99.9% of NIH and Mount Sinai films. On the combined films from these two hospitals, a rule reached an AUC of 0.86 by ranking every Mount Sinai film above every NIH film, without looking at the lungs.

<figure class="fig-img" id="fig-hospital">
<a href="/assets/img/blog/the-model-is-the-small-box/zech-2018-fig2.jpg"><img src="/assets/img/blog/the-model-is-the-small-box/zech-2018-fig2.jpg" width="1400" height="457" loading="lazy" alt="Three panels from Zech and colleagues. Panel A is a grid heat map that is dark red at the corners and edges and pale in the center. Panels B and C are frontal chest X-rays with a red overlay in the upper corner, over a small metal letter marker near the shoulder."></a>
<figcaption><b>Figure 3. The image regions that identified the hospital.</b> Red marks the regions that most influenced a model trained to identify the hospital system. Panel A averages these maps over a sample of images. Darker red means a stronger contribution: most regions contributed, and the corners contributed most. Panels B and C are single chest X-rays, shaded to show only the strongest regions. In both, the red covers a metal marker in a corner of the image. Technicians place this marker to show the patient’s left or right side. The authors note that many different regions of an image predicted the hospital, with the strongest contributions from the corners. <span class="credit">Image: © 2018 Zech et al., <a href="https://doi.org/10.1371/journal.pmed.1002683">PLOS Medicine 2018</a>, Figure 2 (panels A to C), <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. <a href="/assets/img/blog/the-model-is-the-small-box/zech-2018-fig2.jpg">Open the full-size image</a>.</span></figcaption>
</figure>

**COVID-19 and laterality markers.** In many early COVID-19 detectors, the positive radiographs came from published figures and other online sources, and the negative ones came from a single US hospital. [DeGrave and colleagues](https://doi.org/10.1038/s42256-021-00338-7) built detectors from data assembled in this way. Saliency maps, another kind of heat map, highlighted laterality markers (the letter that shows the patient's left or right side), arrows and other annotations, and the shoulders. The authors confirmed the shortcut by experiment. When they swapped in a laterality marker that was more common among the positive images, the model's predicted odds of COVID-19 went up.

**Pneumothorax and chest drains.** A pneumothorax (collapsed lung) is air between the lung and the chest wall. A common treatment is a chest drain, a tube placed through the chest wall that is visible on the radiograph. [Oakden-Rayner and colleagues](https://doi.org/10.1145/3368555.3384468) studied a model that reproduced a well-known classifier trained on the public NIH chest X-ray dataset. A radiologist on the team reviewed the model's errors and saw that films without a drain were over-represented among the missed pneumothoraces. He then labeled every pneumothorax in the test set by whether a drain was present, and 80% of them had one. The model did best on films that already showed the treatment.

<figure class="fig-svg" id="fig-drain">
<svg viewBox="0 0 640 344" role="img" aria-label="Schematic of two chest X-rays with the same pneumothorax on the patient's right side: the lung has collapsed away from the chest wall, leaving dark air between them. Left, with a chest drain, a tube that enters through the chest wall into the air space: already treated, 80% of the pneumothoraces in the test set. Right, without a chest drain: may still need treatment, 20% of the pneumothoraces in the test set.">
<defs>
<clipPath id="drain-clip"><rect x="0" y="0" width="250" height="210" rx="6"/></clipPath>
<g id="drain-chest">
<rect x="0" y="0" width="250" height="210" style="fill:var(--night)"/>
<path d="M100,0 L150,0 C154,16 178,26 216,31 C236,35 246,50 246,72 L238,210 L12,210 L4,72 C4,50 14,35 34,31 C72,26 96,16 100,0 Z" style="fill:var(--ink-4)"/>
<path d="M140,40 C172,38 212,56 220,102 C226,140 224,176 216,192 C190,184 162,182 140,188 Z" style="fill:var(--night-3)"/>
<path d="M110,40 C78,38 38,56 30,102 C24,140 26,176 34,192 C60,184 88,182 110,188 Z" style="fill:var(--night)"/>
<path d="M110,70 C92,68 74,82 70,108 C66,136 70,160 78,176 C90,174 102,176 110,180 Z" style="fill:var(--night-3)"/>
<path d="M110,70 C92,68 74,82 70,108 C66,136 70,160 78,176" style="fill:none;stroke:var(--on-night);stroke-width:1.8"/>
<g style="fill:none;stroke:var(--ink-4);stroke-width:2;stroke-linecap:round">
<path d="M146,112 C166,104 184,92 200,80"/><path d="M146,116 C170,118 190,124 208,136"/><path d="M146,120 C162,136 176,152 188,170"/>
<path d="M104,112 C96,104 88,96 82,88"/><path d="M104,116 C94,118 84,122 76,128"/><path d="M104,120 C98,134 92,148 88,162"/>
</g>
<rect x="119" y="0" width="12" height="210" style="fill:var(--on-night-2);opacity:.22"/>
<g style="fill:none;stroke:var(--on-night-2);stroke-width:2.2;opacity:.3">
<path d="M118,52 C86,42 46,54 30,86"/><path d="M118,80 C86,70 46,82 30,114"/><path d="M118,108 C86,98 46,110 30,142"/><path d="M118,136 C86,126 46,138 30,170"/><path d="M118,164 C86,154 50,166 36,192"/>
<path d="M132,52 C164,42 204,54 220,86"/><path d="M132,80 C164,70 204,82 220,114"/><path d="M132,108 C164,98 204,110 220,142"/><path d="M132,136 C164,126 204,138 220,170"/><path d="M132,164 C164,154 200,166 214,192"/>
</g>
<g style="fill:none;stroke:var(--on-night-2);stroke-width:4.5;stroke-linecap:round;opacity:.7">
<path d="M118,30 C96,24 66,22 40,30"/><path d="M132,30 C154,24 184,22 210,30"/>
</g>
</g>
</defs>
<text x="160" y="28" text-anchor="middle" style="font-size:22px;font-weight:600;fill:var(--ink)">With a chest drain</text>
<text x="160" y="53" text-anchor="middle" style="font-size:20px;fill:var(--ink-3)">already treated</text>
<text x="480" y="28" text-anchor="middle" style="font-size:22px;font-weight:600;fill:var(--ink)">Without a chest drain</text>
<text x="480" y="53" text-anchor="middle" style="font-size:20px;fill:var(--ink-3)">may still need treatment</text>
<g transform="translate(35 66)" clip-path="url(#drain-clip)">
<use href="#drain-chest"/>
<path d="M-6,206 C6,190 18,176 32,166 C44,156 46,130 46,108 C46,84 58,64 84,56" style="fill:none;stroke:var(--on-night);stroke-width:3.5;stroke-linecap:round"/>
<path d="M60,193 L38,176" style="stroke:var(--amber);stroke-width:1.5"/>
<text x="62" y="202" style="font-size:21px;font-weight:600;fill:var(--amber)">chest drain</text>
</g>
<g transform="translate(355 66)" clip-path="url(#drain-clip)">
<use href="#drain-chest"/>
<text x="48" y="124" text-anchor="middle" style="font-size:20px;font-weight:600;fill:var(--amber)">air</text>
</g>
<text x="160" y="306" text-anchor="middle" style="font-size:21px;font-weight:700;fill:var(--sig)">80% of the pneumothoraces</text>
<text x="160" y="332" text-anchor="middle" style="font-size:20px;fill:var(--ink-3)">in the test set</text>
<text x="480" y="306" text-anchor="middle" style="font-size:21px;font-weight:700;fill:var(--red)">20% of the pneumothoraces</text>
<text x="480" y="332" text-anchor="middle" style="font-size:20px;fill:var(--ink-3)">in the test set</text>
</svg>
<figcaption><b>Figure 4. Pneumothorax with and without a chest drain.</b> The two drawings differ only in the drain, the tube used to treat a pneumothorax. Both show a collapsed lung on the patient’s right side, with dark air between the edge of the lung and the chest wall. Most pneumothoraces in the test set had a drain, and <a href="#fig-auc">Figure 6</a> shows that the model did better on them. <span class="credit">Schematic, not a real X-ray. Drawn from the description in <a href="https://doi.org/10.1145/3368555.3384468">Oakden-Rayner et al., ACM CHIL 2020</a>.</span></figcaption>
</figure>

Figure 5 puts the four cases side by side.

<figure>
<table class="data">
<thead><tr><th>Meant to detect</th><th>What it could learn instead</th><th>Why that signal was in the data</th></tr></thead>
<tbody>
<tr><td><b>Melanoma</b><span>magnified skin photographs, 2019</span></td><td class="hi"><b>Surgical ink</b><span>heat maps highlighted it</span></td><td><b>Marking follows concern</b><span>surgeons mark the lesions that they plan to remove</span></td></tr>
<tr><td><b>Pneumonia</b><span>chest X-ray, 2018</span></td><td class="hi"><b>Which hospital</b><span>a separate model identified the hospital for over 99.9% of films from two of the hospitals</span></td><td><b>34% vs about 1%</b><span>the share of films with pneumonia differed by hospital</span></td></tr>
<tr><td><b>COVID-19</b><span>chest X-ray, 2021</span></td><td class="hi"><b>Markers and positioning</b><span>the letter for left or right, arrows, how the patient was positioned</span></td><td><b>Different sources</b><span>positive and negative images came from different collections</span></td></tr>
<tr><td><b>Pneumothorax</b><span>chest X-ray, 2020</span></td><td class="hi"><b>Chest drains</b><span>the treatment, not the disease</span></td><td><b>Already treated</b><span>most positive films showed a drain</span></td></tr>
</tbody>
</table>
<figcaption><b>Figure 5. Signals other than the disease.</b> Read each row from left to right. It gives the target, the signal that the model could use instead, and the clinical reason why that signal was in the data. Data: <a href="https://doi.org/10.1001/jamadermatol.2019.1735">Winkler et al., JAMA Dermatology 2019</a>; <a href="https://doi.org/10.1371/journal.pmed.1002683">Zech et al., PLOS Medicine 2018</a>; <a href="https://doi.org/10.1038/s42256-021-00338-7">DeGrave et al., Nature Machine Intelligence 2021</a>; <a href="https://doi.org/10.1145/3368555.3384468">Oakden-Rayner et al., ACM CHIL 2020</a>.</figcaption>
</figure>

Clinicians can often anticipate shortcuts like these, because they know why each image was taken. So positive and negative examples should come from the same hospitals, scanners and stages of care, and where they cannot, the differences should be reported. A clinician should review the model's errors and heat maps, and a suspected shortcut should be tested directly, as the ink and the laterality marker were. The model also needs an external validation, a test on data from hospitals that contributed nothing to its training.

</section>

<section id="label">

## <span class="n">04</span>Label definition: how the reference standard was set

Before I trust a score, I want to know how the labels were made. The pneumonia, COVID-19 and pneumothorax studies above all drew on the public NIH chest X-ray dataset, whose labels were [extracted from the radiology reports by text-mining software](https://doi.org/10.1109/CVPR.2017.369). Luke Oakden-Rayner was the radiologist in the drain study. He also [reviewed samples of the dataset's images by eye](https://doi.org/10.1016/j.acra.2019.10.006) and found that many labels did not match the images.

Labels from specialists have errors too, and the errors are not spread evenly. Many published dermatology models learned from labels that dermatologists assigned from the photograph alone, without biopsy or follow-up. [Daneshjou and colleagues](https://doi.org/10.1126/sciadv.abq6147) assembled the Diverse Dermatology Images set, in which every diagnosis was confirmed by pathology, and compared dermatologists' visual labels with the biopsy result. The sensitivity of the visual labels for malignancy was 0.72 on Fitzpatrick skin types I to II (the lightest) and 0.59 on types V to VI (the darkest). So the labels can be weakest for the patients who are already rare in training data.

A label can also be accurate and still measure the wrong outcome. [Obermeyer and colleagues](https://doi.org/10.1126/science.aax2342) studied a widely used commercial algorithm that helps select patients for extra care, and its label was healthcare cost in place of health need. Because less money is spent on Black patients at the same level of need, the algorithm underestimated how sick they were. Such a stand-in is called a proxy label. In drug trials, the same kind of stand-in is called a surrogate endpoint, such as blood pressure in place of stroke. [The next post](/blog/proxy-surrogate-endpoint/#cost-for-need) describes this algorithm and compares how both kinds of stand-in can fail.

The fix is to state the reference standard for every label, as a study of diagnostic accuracy would, and to prefer pathology or clinical follow-up where they exist. A clinician should then check a sample of labels against that standard in each subgroup that matters.

</section>

<section id="evaluation">

## <span class="n">05</span>Evaluation: subgroups and new hospitals

An evaluation should tell a clinician how the model performs in the patients in front of them. The AUC is an average over the whole test set, and a high average can include a subgroup in which the model does much worse. Oakden-Rayner and colleagues called this hidden stratification, and the pneumothorax model is their example. Its overall AUC of 0.87 closely matched the published result for the classifier that it reproduced. The AUC was 0.94 on pneumothoraces with a chest drain and 0.77 on those without one. The authors note that untreated pneumothoraces are life-threatening while treated ones are usually benign. They also warn that a model like this could be justified for clinical use or regulatory approval on its overall result alone.

Performance can also fall when a model is tested on new patients. Daneshjou and colleagues ran an external validation of DeepDerm, a published classifier for skin cancer that was trained mostly on images of White patients. Its AUC was 0.88 on its own test data and 0.56 on the biopsy-confirmed Diverse Dermatology Images, close to chance. By skin type, it was 0.61 on Fitzpatrick types I to II and 0.50 on types V to VI. The confidence intervals of these two estimates overlap, so the larger finding is the fall from 0.88 to 0.56 on new patients.

<figure id="fig-auc">
<div class="hbars" role="img" aria-label="Model for pneumothorax on chest X-rays, AUC: 0.87 on all test films, 0.94 on pneumothoraces with a chest drain, 0.77 on pneumothoraces without a chest drain. Model for skin cancer on skin photographs, AUC: 0.88 on its own test images; on new biopsy-confirmed images, 0.56 for all skin types, 0.61 for light skin and 0.50 for dark skin.">
<p class="grp">Model for pneumothorax, on chest X-rays (AUC)</p>
<div class="r"><span class="t">All test films</span><div class="track"><div class="bar" style="width:74%;background:var(--ctx)"></div></div><span class="v">0.87</span></div>
<div class="r"><span class="t">Pneumothoraces with a chest drain</span><div class="track"><div class="bar" style="width:88%;background:var(--ctx)"></div></div><span class="v">0.94</span></div>
<div class="r"><span class="t">Pneumothoraces without a chest drain</span><div class="track"><div class="bar" style="width:54%;background:var(--emph)"></div></div><span class="v">0.77</span></div>
<div class="gap"></div>
<p class="grp">Model for skin cancer, on skin photographs (AUC)</p>
<div class="r"><span class="t">Its own test images</span><div class="track"><div class="bar" style="width:76%;background:var(--ctx)"></div></div><span class="v">0.88</span></div>
<div class="r"><span class="t">New images, all skin types</span><div class="track"><div class="bar" style="width:12%;background:var(--ctx)"></div></div><span class="v">0.56</span></div>
<div class="r"><span class="t">New images, light skin</span><div class="track"><div class="bar" style="width:22%;background:var(--ctx)"></div></div><span class="v">0.61</span></div>
<div class="r"><span class="t">New images, dark skin</span><div class="track"><div class="bar" style="width:0%;background:var(--emph)"></div></div><span class="v">0.50</span></div>
</div>
<div class="legend"><span><i class="sw-ctx"></i>all patients, or the group used for comparison</span><span><i class="sw-emph"></i>the group where the model did worst</span></div>
<figcaption><b>Figure 6. AUC overall and in subgroups.</b> Compare each bar with the top bar of its group. Each value is an AUC, and the bars run from 0.5 (chance) to 1.0 (perfect). The new images are the biopsy-confirmed Diverse Dermatology Images set. Light skin is Fitzpatrick types I to II and dark skin is types V to VI, and the confidence intervals of those two results overlap. Data: <a href="https://doi.org/10.1145/3368555.3384468">Oakden-Rayner et al., ACM CHIL 2020</a>; <a href="https://doi.org/10.1126/sciadv.abq6147">Daneshjou et al., Science Advances 2022</a>.</figcaption>
</figure>

So I would ask for results in each clinically important subgroup, such as treated and untreated pneumothorax, light and dark skin, and each hospital. I would also ask for an external validation whose labels come from a stronger reference standard than the training labels. Even then, the positive predictive value depends on the prevalence of the condition in your patients. It is the proportion of positive results that are correct, and [a later post](/blog/five-of-six-alerts-are-false/#count) works through that calculation.

</section>

<section id="who-notices">

## <span class="n">06</span>Who finds the problems

Several of these failures were found by people with clinical training. Dermatologists designed the ink experiment, and a radiologist found both the label errors in the NIH dataset and the chest-drain shortcut. The bias in the cost label was found by a team led by Ziad Obermeyer, an emergency physician. I do not think this is a coincidence, because each imaging problem was easier to spot for someone who knew why the images were taken.

An interview study points the same way. [Sambasivan and colleagues](https://doi.org/10.1145/3411764.3445518) spoke with 53 AI practitioners who worked in high-stakes fields in India, East and West Africa and the US, 19 of them in health. They define a data cascade as a problem in the data whose effects build up and cause harm later in a project. Of these practitioners, 92% had experienced at least one data cascade. For 43.4%, a cascade arose from missing domain expertise, for example when they had to define the labels in a field that they did not know. Interviews cannot show how common this is across the field, but the pattern is familiar to me. In my work on imaging AI, most of the effort goes into the data, and I believe clinicians belong in that work from the start, not only when something breaks.

</section>

<section id="ask">

## <span class="n">07</span>Questions to ask about any medical AI tool

Two documentation standards already cover several of the questions below. Gebru and colleagues proposed a [datasheet for each dataset](https://doi.org/10.1145/3458723) that records why the dataset was created and how its data were acquired. It also records whether the dataset identifies subpopulations, for example by age or gender. Mitchell and colleagues proposed a [model card](https://doi.org/10.1145/3287560.3287596), which states the intended uses of a model and the uses that are out of its scope. It also reports results for groups such as Fitzpatrick skin types. To me, the datasheet is the list of ingredients and the model card is the package insert that comes with a drug.

<ol class="num-list">
<li><strong>Data provenance.</strong> Where and why were these images taken, and did the positive and negative examples come from the same hospitals, scanners and stages of care?<span class="an">Like a drug’s ingredients</span></li>
<li><strong>Shortcuts.</strong> Has a clinician checked what the model relies on, with heat maps and a review of its errors?<span class="an">Ink, hospital, markers, drains</span></li>
<li><strong>Label definition.</strong> Who or what made the labels, and against which reference standard? Is the label the outcome that matters to patients, or a stand-in for it?<span class="an">The model’s reference standard</span></li>
<li><strong>Evaluation.</strong> What are the results in each clinically important subgroup, and at a hospital that contributed no training data?<span class="an">Treated or untreated, skin type, site</span></li>
<li><strong>Documentation.</strong> Is there a datasheet for the data and a model card for the model?<span class="an">Ingredients and package insert</span></li>
</ol>

None of these questions requires programming, but each needs someone who knows why the images were taken and which outcome matters to patients. [The next post](/blog/proxy-surrogate-endpoint/) looks closely at how labels are defined, and the [overview of the series](/blog/the-model-is-not-the-hard-part/) shows how the posts fit together.

</section>

<section id="sources">

## <span class="n">A</span>Sources

<ol class="refs">
  <li>Sculley D, Holt G, Golovin D, et al. <a href="https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html">Hidden technical debt in machine learning systems.</a> Adv Neural Inf Process Syst 2015;28.</li>
  <li>Hanley JA, McNeil BJ. <a href="https://doi.org/10.1148/radiology.143.1.7063747">The meaning and use of the area under a receiver operating characteristic (ROC) curve.</a> Radiology 1982;143:29-36.</li>
  <li>Winkler JK, Fink C, Toberer F, et al. <a href="https://doi.org/10.1001/jamadermatol.2019.1735">Association between surgical skin markings in dermoscopic images and diagnostic performance of a deep learning convolutional neural network for melanoma recognition.</a> JAMA Dermatol 2019;155:1135-41.</li>
  <li>Zech JR, Badgeley MA, Liu M, et al. <a href="https://doi.org/10.1371/journal.pmed.1002683">Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs: a cross-sectional study.</a> PLoS Med 2018;15:e1002683.</li>
  <li>DeGrave AJ, Janizek JD, Lee SI. <a href="https://doi.org/10.1038/s42256-021-00338-7">AI for radiographic COVID-19 detection selects shortcuts over signal.</a> Nat Mach Intell 2021;3:610-9.</li>
  <li>Oakden-Rayner L, Dunnmon J, Carneiro G, Ré C. <a href="https://doi.org/10.1145/3368555.3384468">Hidden stratification causes clinically meaningful failures in machine learning for medical imaging.</a> Proc ACM Conf Health Inference Learn 2020:151-9.</li>
  <li>Wang X, Peng Y, Lu L, et al. <a href="https://doi.org/10.1109/CVPR.2017.369">ChestX-ray8: hospital-scale chest X-ray database and benchmarks on weakly-supervised classification and localization of common thorax diseases.</a> CVPR 2017:3462-71.</li>
  <li>Oakden-Rayner L. <a href="https://doi.org/10.1016/j.acra.2019.10.006">Exploring large-scale public medical image datasets.</a> Acad Radiol 2020;27:106-12.</li>
  <li>Daneshjou R, Vodrahalli K, Novoa RA, et al. <a href="https://doi.org/10.1126/sciadv.abq6147">Disparities in dermatology AI performance on a diverse, curated clinical image set.</a> Sci Adv 2022;8(32):eabq6147.</li>
  <li>Obermeyer Z, Powers B, Vogeli C, Mullainathan S. <a href="https://doi.org/10.1126/science.aax2342">Dissecting racial bias in an algorithm used to manage the health of populations.</a> Science 2019;366:447-53.</li>
  <li>Sambasivan N, Kapania S, Highfill H, et al. <a href="https://doi.org/10.1145/3411764.3445518">"Everyone wants to do the model work, not the data work": data cascades in high-stakes AI.</a> Proc 2021 CHI Conf Hum Factors Comput Syst 2021:article 39, 1-15.</li>
  <li>Gebru T, Morgenstern J, Vecchione B, et al. <a href="https://doi.org/10.1145/3458723">Datasheets for datasets.</a> Commun ACM 2021;64(12):86-92.</li>
  <li>Mitchell M, Wu S, Zaldivar A, et al. <a href="https://doi.org/10.1145/3287560.3287596">Model cards for model reporting.</a> FAT* 2019:220-9.</li>
</ol>

</section>
