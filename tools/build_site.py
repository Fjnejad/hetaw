#!/usr/bin/env python3
"""Generate the hetaw.de pages (home + subpages) from shared fragments."""
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
PUZZLE = (ROOT / "assets" / "puzzle.svg").read_text(encoding="utf-8")
MAIL = "fahrnaz@hetaw.de"

def head(title, desc, path, extra=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://hetaw.de/{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://hetaw.de/assets/hetaw-wordmark.jpg?v=2">
<meta property="og:url" content="https://hetaw.de/{path}">
<meta name="theme-color" content="#0B1A33">
<link rel="icon" type="image/png" href="assets/favicon.png?v=2">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="stylesheet" href="assets/style.css?v=20261108f">{extra}
</head>
<body>
'''

NAV = [("how-it-works.html", "How it works"), ("for-practices.html", "For practices"),
       ("for-partners.html", "For partners"), ("about.html", "About")]

def masthead(current):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>\n      ' for h, t in NAV)
    return f'''<header class="masthead">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="HETAW home">
      <img src="assets/hetaw-icon.png?v=2" alt="" width="36" height="36">
      <span>HETAW</span>
    </a>
    <nav class="nav" aria-label="Main">
      {links}<a class="cta" href="#contact">Contact</a>
    </nav>
  </div>
</header>

<main id="top">
'''

def contact(heading, intro=None, cards=True):
    cards_html = '''      <div class="partners partners-side">
        <div><h3>Endometriosis centres</h3><p>Retrospective validation on your data, joint publication, clinical review of the question set.</p></div>
        <div><h3>GPs and gynaecologists</h3><p>Tell us what would make a first-visit tool workable in your practice. Early-access list for the pilot.</p></div>
        <div><h3>Krankenkassen</h3><p>Validation cooperation (§68a SGB V) leading to a selective-care pilot (§140a SGB V).</p></div>
      </div>
''' if cards else ""
    intro_html = f'      <p class="text">{intro}</p>\n' if intro else ""
    return f'''<section class="flow-contact" id="contact">
  <div class="wrap">
    <div class="contact-grid">
      <div>
        <p class="overline light">Work with us</p>
        <h2>{heading}</h2>
{intro_html}        <a class="mail" href="mailto:{MAIL}">{MAIL}</a>
      </div>
{cards_html}    </div>
  </div>
  <footer class="footer">
    <div class="wrap">
      <div class="foot-brand">
        <img src="assets/hetaw-icon.png" alt="" width="72" height="72">
        <div>
          <span class="brand-small"><b>HETAW</b><span>· Berlin</span></span>
          <p class="disclaimer">HETAW is a decision-support tool in development. It does not diagnose and is not yet available for clinical use.</p>
        </div>
      </div>
      <nav aria-label="Legal"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></nav>
    </div>
  </footer>
</section>

</main>
<script src="assets/motion.js?v=20261108f" defer></script>
</body>
</html>
'''

FIGURES = '''      <div class="figures">
        <div class="figure"><span class="num">10<small> yrs</small></span><span class="label">Median diagnostic delay</span><span class="note">From first symptoms to confirmed diagnosis</span></div>
        <div class="figure"><span class="num">74<small> %</small></span><span class="label">Receive a wrong diagnosis first</span><span class="note">At least one misdiagnosis before endometriosis is named</span></div>
        <div class="figure"><span class="num">510<small> k</small></span><span class="label">Confirmed cases in Germany</span><span class="note">BARMER Arztreport 2026 — many more undiagnosed</span></div>
      </div>
'''

JOURNEY_FIG = '''      <div class="fig">
        <div class="fig-today">
          <div class="fig-head"><div><span class="fig-kicker">Today</span><span class="fig-title">The scatter signature: one patient, five specialists, no connection</span></div><span class="fig-badge">10.4 yrs<small>median delay</small></span></div>
          <ol class="scatter">
            <li><strong>GP</strong><span>abdominal pain</span></li>
            <li><strong>Gastroenterologist</strong><span>bowel complaints</span></li>
            <li><strong>Gynaecologist</strong><span>painful periods</span></li>
            <li><strong>Urologist</strong><span>bladder symptoms</span></li>
            <li><strong>Pain clinic</strong><span>chronic pain</span></li>
          </ol>
          <p class="scatter-loop">… and back to the GP. Each specialist sees one fragment, treats it symptomatically and sends her home.</p>
        </div>
        <div class="fig-hetaw">
          <div class="fig-head"><div><span class="fig-kicker gold">With HETAW</span><span class="fig-title">Recognised at the first visit: five steps in one consultation</span></div></div>
          <ol class="flow">
            <li><span class="flow-n">1</span><strong>Patient presents</strong><span>GP or gynaecologist. Pain, cycle, bowel or bladder complaint.</span><em>first visit</em></li>
            <li><span class="flow-n">2</span><strong>Doctor opens HETAW</strong><span>Structured symptom history: pain, cycle, GI, urinary, fatigue.</span><em>2–3 minutes</em></li>
            <li class="flow-key"><span class="flow-n">3</span><strong>HETAW scores</strong><span>Risk score with plain-language reasons and confidence.</span><em>interpretable model</em></li>
            <li><span class="flow-n">4</span><strong>Doctor decides</strong><span>Watch and re-evaluate, order ultrasound or blood work, or refer.</span><em>doctor stays in charge</em></li>
            <li><span class="flow-n">5</span><strong>Earlier diagnosis</strong><span>Certified endometriosis centre confirms and treats.</span><em>years, not a decade</em></li>
          </ol>
          <p class="fig-foot">All inputs are entered by the doctor in the consultation. HETAW uses no insurer, claims or electronic-record data and does not communicate with the patient.</p>
        </div>
      </div>
      <p class="journey-note">Median delay of 10.4 years from first symptoms to diagnosis: Hudelist et al., Human Reproduction 2012 (Germany and Austria). The HETAW path describes the intended use of a decision-support tool still in validation.</p>
'''

ILLUSTRATION = '''        <figure class="bodymap">
          <img src="assets/endometriosis-blausen.jpg" alt="Medical illustration of endometriosis: uterus, fallopian tubes and ovaries with endometriosis lesions on the ovaries, the outer uterine wall and surrounding tissue; a small body outline shows the location of the pelvis" width="1400" height="930" loading="lazy">
          <figcaption>Endometriosis: tissue similar to the uterine lining growing on the ovaries, tubes, peritoneum and neighbouring organs. Illustration: Blausen Medical Communications, <a href="https://commons.wikimedia.org/wiki/File:Blausen_0349_Endometriosis.png" rel="noopener">Blausen 0349 Endometriosis</a>, <a href="https://creativecommons.org/licenses/by/3.0/" rel="noopener">CC BY 3.0</a>, via Wikimedia Commons.</figcaption>
        </figure>
'''

# ---------------------------------------------------------------- index
index = head("HETAW — Recognise endometriosis earlier, at the first visit",
             "HETAW is a decision-support app that helps GPs and gynaecologists recognise endometriosis earlier: a short structured symptom history at the first visit, an interpretable risk score with reasons, and the doctor decides.",
             "") + masthead(None) + '''
<section class="lp-hero">
  <div class="wrap lp-hero-grid">
    <div class="lp-hero-copy reveal">
      <p class="lp-kicker">Decision support for GPs and gynaecologists</p>
      <h1>Endometriosis is found <span class="hl">ten years</span> too late.</h1>
      <p class="lp-lede">At the first visit, the doctor enters a short structured symptom history. HETAW returns an interpretable risk score with the reasons behind it. The doctor decides whether to investigate or refer.</p>
      <div class="lp-actions">
        <a class="pill pill-solid" href="how-it-works.html">How it works</a>
        <a class="pill pill-ghost" href="#contact">Work with us</a>
      </div>
      <p class="lp-status">In validation · Not yet available for clinical use</p>
    </div>
    <figure class="lp-hero-visual reveal delay-2">
      <img src="assets/endometriosis-blausen.jpg" alt="Medical illustration of endometriosis: uterus, fallopian tubes and ovaries with endometriosis lesions; a small body outline shows the location of the pelvis" width="1400" height="930">
      <figcaption>Illustration: Blausen Medical Communications, <a href="https://commons.wikimedia.org/wiki/File:Blausen_0349_Endometriosis.png" rel="noopener">Blausen 0349 Endometriosis</a>, <a href="https://creativecommons.org/licenses/by/3.0/" rel="noopener">CC BY 3.0</a></figcaption>
    </figure>
  </div>
</section>

<section class="lp-section" id="problem">
  <div class="wrap">
    <div class="lp-head reveal">
      <h2>One disease, many doors</h2>
      <p>Tissue similar to the uterine lining grows outside the uterus — on the ovaries, the bowel, the bladder, the peritoneum, sometimes the diaphragm or nerves. Because the lesions are spread through the body, so are the symptoms. A woman sees one doctor per complaint, and nobody connects the fragments.</p>
    </div>
    <div class="cards cards-3">
      <article class="card reveal"><span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span><h3>10 years</h3><p>Median delay from first symptoms to diagnosis in Germany and Austria — 7.7 of them after the first gynaecologist visit.</p></article>
      <article class="card reveal delay-1"><span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3l9 16H3z"/><path d="M12 10v4M12 17h.01"/></svg></span><h3>74 %</h3><p>Receive at least one wrong diagnosis first — irritable bowel, cystitis, "stress" — before endometriosis is named.</p></article>
      <article class="card reveal delay-2"><span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M16 11a4 4 0 1 0-8 0 4 4 0 0 0 8 0z"/><path d="M4 21a8 8 0 0 1 16 0"/></svg></span><h3>510,000</h3><p>Women with a confirmed diagnosis in Germany in 2024 — more than double 2005, and still below the true number affected.</p></article>
    </div>
    <p class="lp-source reveal">Sources: Hudelist et al., Human Reproduction 2012; BARMER Arztreport 2026.</p>
  </div>
</section>

<section class="lp-section lp-tint" id="pieces">
  <div class="wrap pz-wrap">
    <div class="pz-copy reveal">
      <p class="lp-kicker">What the delay costs</p>
      <h2>Left unrecognised, endometriosis does not stay in the pelvis.</h2>
      <p class="lp-p">Years without a diagnosis mean years of untreated inflammation and pain. The coloured pieces show what commonly follows: chronic pain, fatigue, infertility, bowel and bladder problems, pregnancy complications, depression and anxiety, and associations with autoimmune conditions such as Hashimoto’s thyroiditis.</p>
      <p class="lp-p">The white pieces are the rarer ones — ureteral endometriosis with silent kidney damage, lesions on the diaphragm or lung, and small increases in cardiovascular risk and ovarian cancer. Most women never experience these; they are listed because they are the reason delay is not harmless.</p>
      <p class="lp-source" style="text-align:left;margin:0">Associations reported in the literature (Shigesi et al. 2019, Human Reproduction Update; Gambadauro et al. 2019, AJOG; Barnard et al. 2024, JAMA). Illustration: Blausen Medical Communications, CC BY 3.0, modified.</p>
    </div>
    <div class="pz-stage reveal delay-1">
      ''' + PUZZLE + '''
      <div class="jg-legend"><span><i class="k1"></i>common consequences</span><span><i class="k2"></i>rare, low absolute risk</span></div>
    </div>
  </div>
</section>

<section class="lp-brandband reveal" aria-label="HETAW — Health · Earlier · Through · Awareness">
  <img src="assets/hetaw-wordmark.jpg?v=2" alt="HETAW — Health · Earlier · Through · Awareness" width="1600" height="800">
</section>

<section class="lp-section" id="what">
  <div class="wrap lp-what-wide">
    <div class="lp-what reveal">
      <p class="lp-kicker">What HETAW is</p>
      <h2>A structured history in. A score with reasons out.</h2>
      <p class="lp-p">HETAW is a decision-support app that helps GPs and gynaecologists recognise endometriosis earlier. At the first visit, the doctor enters a short structured symptom history, and HETAW returns an interpretable risk score with the reasons behind it; the doctor decides whether to investigate or refer. HETAW does not diagnose and does not use insurer data: everything it scores is entered by the doctor.</p>
    </div>
    <ol class="what-steps what-steps-row reveal delay-1">
      <li><span>i.</span><div><strong>The doctor enters a short symptom history</strong><p>Pain pattern, cycle, digestive, urinary and fatigue symptoms, reproductive history, prior consultations — two to three minutes.</p></div></li>
      <li><span>ii.</span><div><strong>HETAW returns a risk score with its reasons</strong><p>A calibrated pre-test risk score and the symptom patterns that drove it, in plain language. Interpretable by design.</p></div></li>
      <li><span>iii.</span><div><strong>The doctor decides</strong><p>Watch and re-evaluate, order ultrasound or blood work, or refer to a certified centre. HETAW supports the decision; it never makes it.</p></div></li>
    </ol>
    <div class="lp-center reveal delay-2"><a class="pill pill-outline" href="how-it-works.html">How it works in detail</a></div>
  </div>
</section>

<section class="lp-section lp-tint" id="journey">
  <div class="wrap">
    <div class="lp-head reveal">
      <h2>The journey today — and with HETAW</h2>
      <p>Today the symptoms are treated one fragment at a time across up to five specialties, and the right referral comes years late. With HETAW, the first doctor the patient sees runs a short structured history and receives a risk score with reasons. The referral decision stays with the doctor.</p>
    </div>
    <div class="today reveal">
      <div class="today-head"><span class="today-tag">Today</span><span class="today-title">One patient, five specialists, no connection</span><span class="today-badge">10.4 yrs<small>median delay</small></span></div>
      <ol class="today-row">
        <li><strong>GP</strong><span>abdominal pain</span></li>
        <li><strong>Gastroenterologist</strong><span>bowel complaints</span></li>
        <li><strong>Gynaecologist</strong><span>painful periods</span></li>
        <li><strong>Urologist</strong><span>bladder symptoms</span></li>
        <li><strong>Pain clinic</strong><span>chronic pain</span></li>
      </ol>
      <p class="today-loop">… and back to the GP. Each specialist sees one fragment, treats it symptomatically and sends her home. Years pass between the first visit and the right referral.</p>
    </div>
    <div class="with-head reveal"><img class="with-icon" src="assets/hetaw-icon.png" alt="" width="72" height="72"><span class="today-tag gold">With HETAW</span><span class="today-title">Recognised at the first visit: five steps in one consultation</span></div>
    <ol class="tl">
      <li class="reveal"><span class="tl-n">1</span><div class="card tl-card"><h3>Patient presents</h3><p>GP or gynaecologist. Pain, cycle, bowel or bladder complaint — the first visit.</p></div></li>
      <li class="reveal delay-1"><span class="tl-n">2</span><div class="card tl-card"><h3>Doctor opens HETAW</h3><p>A structured symptom history: pain, cycle, digestive, urinary and fatigue symptoms, reproductive history, prior consultations. Two to three minutes.</p></div></li>
      <li class="reveal delay-2"><span class="tl-n gold">3</span><div class="card tl-card tl-key"><h3>HETAW scores</h3><p>A calibrated risk score with plain-language reasons: which answers raised it, which lowered it, and how confident the estimate is. Interpretable model.</p></div></li>
      <li class="reveal delay-3"><span class="tl-n">4</span><div class="card tl-card"><h3>Doctor decides</h3><p>Watch and re-evaluate, order ultrasound or blood work, or refer to a certified endometriosis centre. The doctor stays in charge.</p></div></li>
      <li class="reveal delay-4"><span class="tl-n">5</span><div class="card tl-card"><h3>Earlier diagnosis</h3><p>The certified centre confirms and treats — years, not a decade, after the first symptoms.</p></div></li>
    </ol>
    <p class="lp-source reveal">All inputs are entered by the doctor in the consultation. HETAW uses no insurer, claims or electronic-record data and does not communicate with the patient.</p>
  </div>
</section>

<section class="lp-band" aria-label="Key facts">
  <div class="wrap stats">
    <div class="reveal"><strong data-count="10.4" data-suffix=" yrs">10.4 yrs</strong><span>median diagnostic delay</span></div>
    <div class="reveal delay-1"><strong data-count="74" data-suffix=" %">74 %</strong><span>misdiagnosed at least once</span></div>
    <div class="reveal delay-2"><strong data-count="3" data-suffix=" min">3 min</strong><span>structured history per patient</span></div>
    <div class="reveal delay-3"><strong data-count="0">0</strong><span>insurer or record data used</span></div>
  </div>
</section>

<section class="lp-section" id="method">
  <div class="wrap">
    <div class="lp-head reveal">
      <h2>Why HETAW</h2>
      <p>Three design principles separate HETAW from a symptom checker.</p>
    </div>
    <div class="cards cards-3">
      <article class="card reveal"><span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3a5 5 0 0 1 5 5v2a5 5 0 0 1-10 0V8a5 5 0 0 1 5-5z"/><path d="M4 21a8 8 0 0 1 16 0"/></svg></span><h3>The doctor stays in charge</h3><p>HETAW does not diagnose and does not communicate with the patient. It gives the doctor a structured, defensible basis for a decision he or she makes anyway.</p></article>
      <article class="card reveal delay-1"><span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 9h8M8 13h8M8 17h5"/></svg></span><h3>Everything scored is entered by the doctor</h3><p>No insurer, claims or electronic-record data. Consent stays inside the consultation, and the tool runs in any practice without an IT integration project.</p></article>
      <article class="card reveal delay-2"><span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 3l2.5 5 5.5.8-4 3.9.9 5.5-4.9-2.6-4.9 2.6.9-5.5-4-3.9L9.5 8z"/></svg></span><h3>Explainable by design</h3><p>An interpretable model class, per-patient reasons, calibrated probabilities and a published model card — requirements of the MDR and the EU AI Act, treated as product features.</p></article>
    </div>
  </div>
</section>

<section class="lp-section lp-tint" id="who">
  <div class="wrap">
    <div class="lp-head reveal">
      <h2>Built for the first consultation</h2>
    </div>
    <div class="cards cards-4">
      <a class="card card-link reveal" href="for-practices.html"><h3>General practitioners</h3><p>Often the first contact for pain, fatigue and cycle complaints — the entry point where endometriosis is least likely to be considered.</p><span class="more">For practices →</span></a>
      <a class="card card-link reveal delay-1" href="for-practices.html"><h3>Gynaecology practices</h3><p>A consistent, documented first-visit assessment that fits the consultation and makes the case for work-up or referral explicit.</p><span class="more">For practices →</span></a>
      <a class="card card-link reveal delay-2" href="for-partners.html"><h3>Endometriosis centres</h3><p>Better-prepared referrals — and HETAW's validation partners: the score is validated first on retrospective centre data.</p><span class="more">For partners →</span></a>
      <a class="card card-link reveal delay-3" href="for-partners.html"><h3>Krankenkassen</h3><p>Earlier recognition shortens the years of unresolved visits, tests and misdirected treatment — measurable against claims data.</p><span class="more">For partners →</span></a>
    </div>
  </div>
</section>

<section class="lp-section" id="research">
  <div class="wrap lp-split">
    <div class="reveal">
      <h2>Validated before it is used</h2>
      <p class="lp-p">The question set is built from published evidence and clinical review, then evaluated on retrospective data from certified endometriosis centres before any practice uses it. Results are published openly.</p>
      <a class="pill pill-outline" href="for-partners.html#research">Validation plan and partners</a>
    </div>
    <ol class="tl tl-compact reveal delay-1">
      <li><span class="tl-n gold">Now</span><div class="card tl-card tl-key"><h3>First-visit symptom triage</h3><p>Question set development and retrospective validation with endometriosis centres.</p></div></li>
      <li><span class="tl-n">Next</span><div class="card tl-card"><h3>After the work-up</h3><p>Combining routine labs, ultrasound and MRI findings into a post-test likelihood.</p></div></li>
      <li><span class="tl-n">Later</span><div class="card tl-card"><h3>Care-pathway integration</h3><p>Pilot within a selective-care contract; CE marking as a medical device.</p></div></li>
    </ol>
  </div>
</section>

<section class="lp-section lp-tint" id="about">
  <div class="wrap lp-about reveal">
    <p class="lp-quote">“Founded in Berlin by a data scientist who read the diagnostic-delay numbers and did not accept them.”</p>
    <p class="lp-p">HETAW is founded by Fahrnaz Jayrannejad, a data scientist with an MSc in AI and a background in software engineering, proteomics and bioinformatics, after eight years building machine-learning systems in industry. The company works with clinicians, epidemiologists and endometriosis centres in Berlin and across Germany. <a class="inline-link" href="about.html">About HETAW →</a></p>
  </div>
</section>

''' + contact("We are looking for partners in three places.")

# ---------------------------------------------------------------- how it works
how = head("How HETAW works — the problem, the method, the validation",
           "What endometriosis is, why it is found late, how HETAW's first-visit risk score works, and how it is validated before use.",
           "how-it-works.html") + masthead("how-it-works.html") + '''
<section class="page-hero">
  <div class="wrap">
    <p class="kicker">How it works</p>
    <h1>Three minutes at the first visit. One interpretable score.</h1>
    <p class="lede">HETAW is a decision-support app for GPs and gynaecologists. It does not diagnose and does not use insurer data: everything it scores is entered by the doctor in the consultation.</p>
  </div>
</section>

<section class="chapter" id="problem">
  <div class="wrap">
    <p class="chapter-label">The problem</p>
    <div class="chapter-body">
      <h2>Endometriosis presents as scattered complaints across several specialties. Each visit sees one piece.</h2>
      <div class="problem-split">
        <div class="problem-text">
          <p class="text">Endometriosis is tissue similar to the uterine lining growing outside the uterus — on the ovaries, the bowel, the bladder, the peritoneum, sometimes the diaphragm or nerves. Because the lesions are spread through the body, so are the symptoms. A woman sees one doctor per complaint, and nobody connects the fragments.</p>
          <p class="text">The first consultation is where the pattern is most often missed, and where it could most easily be caught.</p>
        </div>
''' + ILLUSTRATION + '''      </div>
''' + FIGURES + '''    </div>
  </div>
</section>

<section class="chapter" id="method">
  <div class="wrap">
    <p class="chapter-label">The method</p>
    <div class="chapter-body">
      <h2>A structured history in, a score with reasons out.</h2>
      <div class="steps">
        <div class="step"><span class="roman">i.</span><div><h3>The doctor enters a short symptom history</h3><p>A defined set of questions on pain pattern, cycle, digestive, urinary and fatigue symptoms, reproductive history and prior consultations — designed to be asked in two to three minutes and to capture the fragments that today go unconnected.</p></div></div>
        <div class="step"><span class="roman">ii.</span><div><h3>HETAW returns a risk score with its reasons</h3><p>A calibrated pre-test risk score and the symptom patterns that drove it, in plain language: which answers raised the score, which lowered it, and how confident the estimate is.</p></div></div>
        <div class="step"><span class="roman">iii.</span><div><h3>The doctor decides</h3><p>Watch and re-evaluate, order ultrasound or blood work, or refer to a certified endometriosis centre. HETAW supports the decision; it never makes it, and it does not diagnose.</p></div></div>
      </div>
      <h3 class="subhead">Three design principles</h3>
      <div class="principles">
        <div><strong>The doctor stays in charge.</strong><p>HETAW does not diagnose and does not communicate with the patient. It gives the doctor a structured, defensible basis for a decision he or she makes anyway.</p></div>
        <div><strong>Everything scored is entered by the doctor.</strong><p>No insurer, claims or electronic-record data. Consent stays inside the consultation, and the tool runs in any practice without an IT integration project.</p></div>
        <div><strong>Explainable by design.</strong><p>An interpretable model class, per-patient reasons, calibrated probabilities and a published model card — requirements of the Medical Device Regulation and the EU AI Act, treated as product features.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="chapter dark" id="research">
  <div class="wrap">
    <p class="chapter-label">Research &amp; validation</p>
    <div class="chapter-body">
      <h2>Validated before it is used.</h2>
      <p class="text">HETAW is being developed as research first. The symptom question set is built from published evidence and clinical review, then evaluated on retrospective data from certified endometriosis centres before any practice uses it. Results are published openly.</p>
      <div class="roadmap">
        <div class="roadmap-row now"><span class="when">Now</span><div><div class="what">First-visit symptom triage</div><div class="how">Question set development and retrospective validation with endometriosis centres</div></div></div>
        <div class="roadmap-row"><span class="when">Next</span><div><div class="what">After the work-up</div><div class="how">Combining routine labs, ultrasound and MRI findings into a post-test likelihood</div></div></div>
        <div class="roadmap-row"><span class="when">Later</span><div><div class="what">Care-pathway integration</div><div class="how">Pilot within a selective-care contract; CE marking as a medical device (Class IIa planned)</div></div></div>
      </div>
    </div>
  </div>
</section>

''' + contact("Help us validate it.", "Centres with retrospective cohorts, clinicians who will review the question set, insurers who want measurable earlier recognition — write to us.")

# ---------------------------------------------------------------- for practices
practices = head("HETAW for GPs and gynaecology practices",
                 "What HETAW asks of a practice, what it gives back, and how to join the early-access list for the pilot.",
                 "for-practices.html") + masthead("for-practices.html") + '''
<section class="page-hero">
  <div class="wrap">
    <p class="kicker">For practices</p>
    <h1>A structured reason to consider endometriosis — in the time of a normal consultation.</h1>
    <p class="lede">GPs and office-based gynaecologists are not endometriosis specialists and have few minutes per patient. HETAW gives them a consistent question set and a score they can document and act on.</p>
  </div>
</section>

<section class="chapter" id="who">
  <div class="wrap">
    <p class="chapter-label">Who it helps</p>
    <div class="chapter-body">
      <div class="audience">
        <div><h3>General practitioners</h3><p>Often the first contact for pain, fatigue and cycle complaints — and the entry point where endometriosis is least likely to be considered. HETAW gives the GP a structured reason to refer earlier.</p></div>
        <div><h3>Gynaecology practices</h3><p>A consistent, documented first-visit assessment that fits the consultation and makes the case for work-up or referral explicit — including for patients with regular cycles.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="chapter" id="practice">
  <div class="wrap">
    <p class="chapter-label">In practice</p>
    <div class="chapter-body">
      <h2>What it asks of you, and what it gives back.</h2>
      <div class="steps">
        <div class="step"><span class="roman">i.</span><div><h3>Two to three minutes</h3><p>A defined set of questions on pain pattern, cycle, digestive, urinary and fatigue symptoms, reproductive history and prior consultations, asked during the consultation.</p></div></div>
        <div class="step"><span class="roman">ii.</span><div><h3>No integration project</h3><p>For the pilot HETAW runs as a standalone application; the doctor enters the history directly. Integration with practice-management systems through the standard German interfaces follows once the question set is validated.</p></div></div>
        <div class="step"><span class="roman">iii.</span><div><h3>A documented decision</h3><p>A risk score with the reasons behind it, in plain language — a defensible basis for watching, investigating or referring, and a lower risk of both missing a case and over-referring.</p></div></div>
      </div>
      <div class="tags">
        <span>— Doctor-entered data only</span>
        <span>— No patient app required</span>
        <span>— HETAW does not diagnose</span>
        <span>— Planned as a medical device (MDR Class IIa)</span>
      </div>
    </div>
  </div>
</section>

''' + contact("Join the early-access list.", "Tell us what would make a first-visit tool workable in your practice — how much time it can take, who completes the history, how it should be paid for. Practices on the list are the first to be invited to the pilot.", cards=False)

# ---------------------------------------------------------------- for partners
partners = head("HETAW for endometriosis centres, insurers and research partners",
                "How endometriosis centres, Krankenkassen and research partners can work with HETAW: retrospective validation, selective-care pilots, joint publication.",
                "for-partners.html") + masthead("for-partners.html") + '''
<section class="page-hero">
  <div class="wrap">
    <p class="kicker">For partners</p>
    <h1>Validated with centres. Paid for by the system that saves the years.</h1>
    <p class="lede">HETAW is validated first on retrospective data from certified endometriosis centres, and built for integration into selective-care contracts with statutory health insurers.</p>
  </div>
</section>

<section class="chapter" id="who">
  <div class="wrap">
    <p class="chapter-label">Who we work with</p>
    <div class="chapter-body">
      <div class="audience">
        <div><h3>Certified endometriosis centres</h3><p>Retrospective validation on your cohorts, clinical review of the question set, joint publication. In return: better-prepared referrals with a documented symptom history.</p></div>
        <div><h3>Health insurers (Krankenkassen)</h3><p>Every year of diagnostic delay is a year of paid but ineffective care. The intended route is a validation cooperation under §68a SGB V leading to a selective-care pilot under §140a SGB V, with outcomes measurable against claims data.</p></div>
        <div><h3>Research partners</h3><p>Epidemiologists, general-practice and gynaecology research groups: the question set, the validation design and the results are developed as open research.</p></div>
        <div><h3>Complementing existing pathways</h3><p>Programmes such as ENDO-EVE standardise the initial assessment in gynaecology practices; HETAW adds the GP entry point and, later, integration of work-up results.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="chapter dark" id="research">
  <div class="wrap">
    <p class="chapter-label">Research &amp; validation</p>
    <div class="chapter-body">
      <h2>Validated before it is used.</h2>
      <div class="roadmap">
        <div class="roadmap-row now"><span class="when">Now</span><div><div class="what">First-visit symptom triage</div><div class="how">Question set development and retrospective validation with endometriosis centres</div></div></div>
        <div class="roadmap-row"><span class="when">Next</span><div><div class="what">After the work-up</div><div class="how">Combining routine labs, ultrasound and MRI findings into a post-test likelihood</div></div></div>
        <div class="roadmap-row"><span class="when">Later</span><div><div class="what">Care-pathway integration</div><div class="how">Pilot within a selective-care contract; CE marking as a medical device</div></div></div>
      </div>
    </div>
  </div>
</section>

''' + contact("We are looking for partners in three places.")

# ---------------------------------------------------------------- about
about = head("About HETAW", "HETAW is a pre-incorporation digital-health venture in Berlin, founded by data scientist Fahrnaz Jayrannejad.",
             "about.html") + masthead("about.html") + '''
<section class="page-hero">
  <div class="wrap">
    <p class="kicker">About</p>
    <h1>Founded in Berlin by a data scientist who read the diagnostic-delay numbers and did not accept them.</h1>
  </div>
</section>

<section class="chapter" id="founder">
  <div class="wrap">
    <p class="chapter-label">Founder</p>
    <div class="chapter-body">
      <p class="text">HETAW is founded by Fahrnaz Jayrannejad, a Berlin-based data scientist with an MSc in AI and a background in software engineering, proteomics and bioinformatics, after eight years building machine-learning systems in industry. She works on HETAW full time.</p>
      <p class="text">The company works with clinicians, epidemiologists and endometriosis centres in Berlin and across Germany, and is building its scientific advisory board.</p>
    </div>
  </div>
</section>

<section class="chapter" id="name">
  <div class="wrap">
    <p class="chapter-label">The name</p>
    <div class="chapter-body">
      <h2>Health · Earlier · Through · Awareness</h2>
      <p class="text">HETAW stands for what the product is meant to do: bring health earlier, by making a pattern visible that today goes unseen. The eclipse in the logo is the disease hidden behind everyday complaints; the line that follows is the moment it is recognised.</p>
    </div>
  </div>
</section>

''' + contact("Get in touch.", cards=False)

for name, html in [("index.html", index), ("how-it-works.html", how), ("for-practices.html", practices),
                   ("for-partners.html", partners), ("about.html", about)]:
    (ROOT / name).write_text(html, encoding="utf-8")
    print("wrote", name, len(html))
