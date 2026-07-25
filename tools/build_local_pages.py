#!/usr/bin/env python3
"""
Generates the local city pages and industry pages for gentoolinkwebservices.com.

Output is plain static HTML in the repo root — no build step is needed to serve
the site, and the generated files are safe to hand-edit afterward. Re-running
this script overwrites them, so if you edit a page by hand, either fold the
change back into the CONTENT dicts below or stop running the script.

    python tools/build_local_pages.py
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://gentoolinkwebservices.com"
OG_IMG = f"{SITE}/assets/images/og-default.png"

# ─────────────────────────────────────────────────────────────────────────────
# Shared shell
# ─────────────────────────────────────────────────────────────────────────────

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-S2FCSXLN1E"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-S2FCSXLN1E');
  </script>

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}}</title>
  <meta name="description" content="{{DESC}}">
  <meta name="keywords" content="{{KEYWORDS}}">
  <meta name="author" content="Gentoolink Web Services">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{{CANON}}" />

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{{CANON}}">
  <meta property="og:title" content="{{OGTITLE}}">
  <meta property="og:description" content="{{OGDESC}}">
  <meta property="og:image" content="{{OGIMG}}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Gentoolink Web Services — websites and AI visibility for local business">
  <meta property="og:image:type" content="image/png">
  <meta property="og:locale" content="en_CA">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="{{CANON}}">
  <meta name="twitter:title" content="{{OGTITLE}}">
  <meta name="twitter:description" content="{{OGDESC}}">
  <meta name="twitter:image" content="{{OGIMG}}">

  <!-- Schema.org -->
  <script type="application/ld+json">
{{SCHEMA}}
  </script>

  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="stylesheet" href="style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
</head>
<body>

<!-- ─── Nav ──────────────────────────────────────────────── -->
<nav aria-label="Main navigation">
  <div class="container">
    <div class="nav-inner">
      <a href="/" class="nav-logo" aria-label="Gentoolink Web Services — home">
        <picture>
          <source srcset="/assets/images/gentoolink-mark.webp" type="image/webp">
          <img src="/assets/images/gentoolink-mark.png" alt="Gentoolink Web Services" class="nav-logo-img">
        </picture>
        <span>Gentoo<span>link</span></span>
      </a>
      <span class="nav-links">
        <a href="services.html">Services</a>
        <a href="templates.html">Templates</a>
        <a href="time-money-audit.html" style="color: var(--gold);">Local Audit</a>
        <a href="about.html">About</a>
        <a href="blog.html">Blog</a>
      </span>
      <a href="contact.html" class="nav-cta">Book My Audit</a>
    </div>
  </div>
</nav>

<main>
{{BODY}}
</main>

<!-- ─── Footer ────────────────────────────────────────────── -->
<footer>
  <div class="container">
    <picture>
      <source srcset="/assets/images/gentoolink-logo.webp" type="image/webp">
      <img src="/assets/images/gentoolink-logo.png" alt="Gentoolink Web Services" class="footer-logo" loading="lazy">
    </picture>
    <p class="footer-tagline">{{FOOTER_TAG}}</p>
    <nav aria-label="Footer navigation" style="margin-bottom: 18px;">
      <span style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap;">
        <a href="services.html" style="font-size:13px;color:var(--text-subtle);">Services</a>
        <a href="templates.html" style="font-size:13px;color:var(--text-subtle);">Templates</a>
        <a href="time-money-audit.html" style="font-size:13px;color:var(--text-subtle);">Time &amp; Money Audit</a>
        <a href="about.html" style="font-size:13px;color:var(--text-subtle);">About</a>
        <a href="blog.html" style="font-size:13px;color:var(--text-subtle);">Blog</a>
        <a href="contact.html" style="font-size:13px;color:var(--text-subtle);">Contact</a>
        <a href="privacy-policy.html" style="font-size:13px;color:var(--text-subtle);">Privacy Policy</a>
      </span>
    </nav>
    <div class="footer-areas">
      <span class="footer-areas-label">Serving Northern BC</span>
      <span class="footer-areas-links">
{{FOOTER_AREAS}}
      </span>
    </div>
    <p class="footer-copy">© 2026 Gentoolink Web Services · Vanderhoof, BC · <a href="mailto:ken@gentoolinkwebservices.com">ken@gentoolinkwebservices.com</a></p>
  </div>
</footer>

<!-- Botpress webchat widget -->
<script src="https://cdn.botpress.cloud/webchat/v3.6/inject.js"></script>
<script src="https://files.bpcontent.cloud/2026/06/16/18/20260616185415-YA0VJZEI.js" defer></script>

<script>
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
</script>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
# City pages
# ─────────────────────────────────────────────────────────────────────────────

CITIES = [
    {
        "slug": "web-design-prince-george",
        "city": "Prince George",
        "region": "BC",
        "eyebrow": "Prince George, BC · Websites &amp; AI Visibility",
        "h1": "Web Design in Prince George That Customers — and AI — Can Actually Find",
        "hero_sub": "Most Prince George businesses already have a website. Far fewer show up when someone asks ChatGPT or Google AI for a recommendation. I build sites that do both.",
        "title": "Web Design Prince George, BC | Gentoolink Web Services",
        "desc": "Website design and AI search visibility for Prince George businesses. Built to rank on Google and get cited by ChatGPT and Perplexity. Sites from $1,500, audits $1,000.",
        "keywords": "web design Prince George, website designer Prince George BC, small business website Prince George, SEO Prince George, AI visibility Prince George",
        "local_h2": "Prince George is the most competitive market I work in.",
        "local_body": [
            "Prince George is the service hub for the whole northern half of the province. If you run a trade, a clinic, a shop, or a professional practice here, you are not competing with two other businesses the way you would in a village on Highway 16 — you are competing with a dozen, and most of them have had a website for years.",
            "That changes what actually wins. Having a website in Prince George is table stakes. The differentiator now is whether search engines and AI assistants can understand your site well enough to recommend you by name. When a homeowner asks an AI assistant for a plumber in Prince George, it returns a short list — usually three names. Everyone else is invisible, regardless of how nice their site looks.",
            "The businesses that make that list tend to have three things in common: clean structured data, a complete and consistent Google Business Profile, and pages written to answer the questions people actually ask. None of it is exotic. Most Prince George sites simply have never had it done.",
        ],
        "hook": "A good-looking site that AI can't read is a brochure. I build the other kind.",
        "travel": "Prince George is about an hour east of my office in Vanderhoof on Highway 16. In-person visits are easy to arrange, and most web work happens remotely either way.",
        "faqs": [
            ("Do you build websites for businesses in Prince George?",
             "Yes. Gentoolink Web Services builds small business websites for Prince George and the surrounding region, starting at $800 for a single page and $1,500 for a typical 5–8 page site. Ken McGonigal is based in Vanderhoof, about an hour west on Highway 16, and travels to Prince George for in-person work. Most design and build work is done remotely, so distance rarely affects the timeline."),
            ("How much does a website cost in Prince George?",
             "A single-page site starts at $800, a typical 5–8 page local business website at $1,500, and a product launch site at $2,000. Most builds run 2–4 weeks. Domain and DNS setup is included, and an online store or logo design can be added for $500 each. The $1,000 AI Visibility Audit checks whether an existing site appears in ChatGPT, Perplexity, and Google AI Overviews. The $2,500 AI Search Foundation Package implements the fixes. All prices are in Canadian dollars."),
            ("Why doesn't my Prince George business show up in ChatGPT?",
             "Usually one of three reasons: the site has no structured data, so AI tools can't reliably tell what the business does or where it operates; the site isn't indexed in Bing, which is what ChatGPT's web search draws on; or the Google Business Profile is incomplete or inconsistent with the website. In a market as crowded as Prince George, any one of these is enough to keep a business off the shortlist."),
            ("Do I need a new website, or can you fix the one I have?",
             "Often the existing site is fine and only needs the AI visibility work — schema markup, Bing indexing, content restructuring, and Google Business Profile cleanup. The $1,000 AI Visibility Audit tells you which situation you're in before you spend anything on a rebuild."),
        ],
    },
    {
        "slug": "web-design-vanderhoof",
        "city": "Vanderhoof",
        "region": "BC",
        "eyebrow": "Vanderhoof, BC · My Home Town",
        "h1": "Web Design in Vanderhoof, BC — From Someone Who Lives Here",
        "hero_sub": "I'm on Burrard Avenue, not in a call centre in another province. Websites from $800, AI visibility audits at $1,000, and an in-person Time &amp; Money Audit for businesses right here in the Nechako Valley.",
        "title": "Web Design Vanderhoof, BC | Gentoolink Web Services",
        "desc": "Local website design and AI search visibility for Vanderhoof businesses. Vanderhoof-based, Chamber of Commerce member. Sites from $1,500, in-person audits available.",
        "keywords": "web design Vanderhoof, website designer Vanderhoof BC, small business website Vanderhoof, Nechako Valley web design, AI visibility Vanderhoof",
        "local_h2": "The advantage of hiring someone who lives in the valley.",
        "local_body": [
            "Vanderhoof sits at the geographic centre of British Columbia, and the business community here runs on the same thing it always has: people know each other. That is a real advantage when word of mouth is working, and a real problem when someone new moves to town, or when a customer from Fort St. James or Fraser Lake starts their search on a phone instead of asking a neighbour.",
            "A lot of good businesses here are effectively invisible to that second kind of customer. No website, or a website that hasn't been touched since it was built, or a Google listing with the wrong hours. Meanwhile the search results fill up with businesses in Prince George that are perfectly happy to drive out here for the work.",
            "I'm a member of the Vanderhoof Chamber of Commerce and I've been doing web and tech work for businesses in this area since 2018. When something breaks, you get my cell — not a ticket number.",
        ],
        "hook": "I can be at your shop this week. That's the whole pitch.",
        "travel": "I'm based in Vanderhoof, so in-person work here costs no travel time. That's also why the in-person Time &amp; Money Audit starts here.",
        "faqs": [
            ("Do you work with businesses in Vanderhoof in person?",
             "Yes. Ken McGonigal is based in Vanderhoof and is a member of the Vanderhoof Chamber of Commerce. In-person meetings are standard for Vanderhoof businesses, and the Time & Money Audit — a $497 in-person review of where hours and dollars leak out of your admin work — was built specifically for businesses in this area."),
            ("How much does a small business website cost in Vanderhoof?",
             "Websites start at $800 for a single page and $1,500 for a typical 5–8 page local business site, usually live in 2–4 weeks. Every project is quoted in writing before work begins. The $1,000 AI Visibility Audit checks whether an existing business appears in ChatGPT, Perplexity, and Google AI Overviews. The $497 Time & Money Audit is a separate, in-person service focused on admin efficiency rather than web presence. All prices are in Canadian dollars."),
            ("My customers all know me already. Why would I need a website?",
             "Word of mouth still works in Vanderhoof, and a website doesn't replace it. What a website does is capture the customers word of mouth misses: people who just moved to town, people searching from Fraser Lake or Fort St. James, and the growing number of people who ask an AI assistant for a recommendation before they ask a neighbour."),
            ("What areas around Vanderhoof do you serve?",
             "Vanderhoof, Fort St. James, Fraser Lake, Burns Lake, Prince George, Quesnel, and the surrounding Northern BC communities. In-person visits are routine along the Highway 16 corridor; web design and AI visibility work can be done from anywhere."),
        ],
    },
    {
        "slug": "web-design-fort-st-james",
        "city": "Fort St. James",
        "region": "BC",
        "eyebrow": "Fort St. James, BC · Websites &amp; AI Visibility",
        "h1": "Web Design in Fort St. James — Get Found Before Visitors Arrive",
        "hero_sub": "Half your potential customers are deciding where to eat, stay, and hire before they ever reach Stuart Lake. If your business isn't in that search, you never get the chance to impress them.",
        "title": "Web Design Fort St. James, BC | Gentoolink Web Services",
        "desc": "Website design and AI search visibility for Fort St. James businesses. Built for a town where visitors search before they arrive. Sites from $1,500. Vanderhoof-based, in person.",
        "keywords": "web design Fort St. James, website designer Fort St James BC, small business website Fort St. James, Stuart Lake tourism website, AI visibility Fort St. James",
        "local_h2": "In a visitor town, the search happens before the drive.",
        "local_body": [
            "Fort St. James has something most small towns don't: a steady flow of people who are not from here. Visitors coming for Stuart Lake, for the national historic site, for fishing and boating in the summer, and the rotating crews that come through for forestry and mining work.",
            "Those people do not ask a neighbour where to eat. They search — increasingly by asking an AI assistant something like \"where should I eat in Fort St. James\" or \"is there a mechanic in Fort St. James\" — and they do it from a truck somewhere on Highway 27 before they arrive. Whatever comes back is the shortlist. If your business isn't in it, you were never in the running.",
            "This is the cheapest kind of visibility to win, because the competition in a town this size is thin. A properly built site with correct structured data and a complete Google Business Profile can become the default answer for your category here, and stay that way.",
        ],
        "hook": "Small town, small competition. That cuts both ways — and right now it's in your favour.",
        "travel": "Fort St. James is about 45 minutes north of Vanderhoof on Highway 27. In-person visits are straightforward, including for the Time &amp; Money Audit.",
        "faqs": [
            ("Do you serve businesses in Fort St. James?",
             "Yes. Fort St. James is about 45 minutes north of Vanderhoof on Highway 27, and it's part of Gentoolink Web Services' regular in-person service area. That includes both web design work and the $497 in-person Time & Money Audit."),
            ("Is a website worth it for a business in a town this size?",
             "In a visitor town, usually yes — and for a different reason than in a city. Fort St. James draws people who aren't local: Stuart Lake visitors, tourists heading to the national historic site, and work crews passing through. Those people search before they arrive, and a business with no web presence is invisible to all of them."),
            ("How much does a website cost in Fort St. James?",
             "Websites start at $800 for a single page and $1,500 for a typical 5–8 page local business site, usually live in 2–4 weeks. Every project is quoted in writing before work begins. The $1,000 AI Visibility Audit checks whether an existing business shows up in ChatGPT, Perplexity, and Google AI Overviews. All prices are in Canadian dollars."),
            ("How hard is it to rank for searches in Fort St. James?",
             "Considerably easier than in Prince George. In a town this size there are often only a handful of businesses in any given category, and most have incomplete or missing structured data. That makes it realistic to become the default AI and search answer for your category here — and to hold that position."),
        ],
    },
    {
        "slug": "web-design-fraser-lake",
        "city": "Fraser Lake",
        "region": "BC",
        "eyebrow": "Fraser Lake, BC · Websites &amp; AI Visibility",
        "h1": "Web Design in Fraser Lake — Don't Lose the Job to a Prince George Search Result",
        "hero_sub": "When someone in Fraser Lake searches for what you do, the results often fill up with businesses an hour away. A properly built local site fixes that.",
        "title": "Web Design Fraser Lake, BC | Gentoolink Web Services",
        "desc": "Website design and AI search visibility for Fraser Lake businesses. Stop losing local searches to out-of-town competitors. Sites from $1,500. Vanderhoof-based, in person.",
        "keywords": "web design Fraser Lake, website designer Fraser Lake BC, small business website Fraser Lake, Highway 16 web design, AI visibility Fraser Lake",
        "local_h2": "The problem isn't your competitors in town. It's the ones an hour away.",
        "local_body": [
            "Fraser Lake is small enough that most business owners here don't think of themselves as having a search problem. And in terms of local rivals, they usually don't — there may only be one or two other businesses in the category for miles.",
            "The competition is coming from somewhere else. When a Fraser Lake resident searches for a service, or when someone asks an AI assistant for a recommendation, the answer frequently skews toward Vanderhoof, Burns Lake, or Prince George — simply because those businesses have websites with clear location signals and yours doesn't. The work leaves town, and nobody in town ever sees that it happened.",
            "Fixing this is not complicated. It takes a real page that says plainly what you do and where you do it, structured data that states your service area in a form machines can read, and a Google Business Profile that matches. In a village-sized market, that is often enough to take back the top spot outright.",
        ],
        "hook": "You can't win a search you don't appear in. That's the whole problem, and it's fixable.",
        "travel": "Fraser Lake is about 40 minutes west of Vanderhoof on Highway 16. In-person visits are easy to arrange.",
        "faqs": [
            ("Do you build websites for Fraser Lake businesses?",
             "Yes. Fraser Lake is about 40 minutes west of Vanderhoof on Highway 16 and is part of Gentoolink Web Services' regular service area, including in-person visits and the $497 Time & Money Audit."),
            ("Why do out-of-town businesses outrank me in local searches?",
             "Because they've given search engines and AI tools clearer signals about who they serve. A business in Prince George with proper structured data listing its service area will often outrank a Fraser Lake business with no website at all — even for a Fraser Lake customer. The fix is to publish those same signals for your own business."),
            ("How much does a website cost in Fraser Lake?",
             "Websites start at $800 for a single page and $1,500 for a typical 5–8 page local business site, usually live in 2–4 weeks. Every project is quoted in writing before work begins. The $1,000 AI Visibility Audit checks whether an existing business appears in ChatGPT, Perplexity, and Google AI Overviews. All prices are in Canadian dollars."),
            ("Is it realistic for a small Fraser Lake business to rank first?",
             "Yes, more so than in a larger centre. Search competition scales with the number of businesses publishing good signals, and in Fraser Lake that number is very low. A well-built page with correct structured data frequently takes the top local position within a few months."),
        ],
    },
    {
        "slug": "web-design-burns-lake",
        "city": "Burns Lake",
        "region": "BC",
        "eyebrow": "Burns Lake, BC · Websites &amp; AI Visibility",
        "h1": "Web Design in Burns Lake — Built for the Lakes District",
        "hero_sub": "Burns Lake pulls in visitors from well beyond the village — riders, anglers, and travellers along Highway 16. Being findable to them is a different job than being known in town.",
        "title": "Web Design Burns Lake, BC | Gentoolink Web Services",
        "desc": "Website design and AI search visibility for Burns Lake and Lakes District businesses. Built to capture visitor and regional search. Sites from $1,500. Northern BC based.",
        "keywords": "web design Burns Lake, website designer Burns Lake BC, small business website Burns Lake, Lakes District web design, AI visibility Burns Lake",
        "local_h2": "Burns Lake's reach is bigger than its population.",
        "local_body": [
            "Burns Lake serves the Lakes District, and it draws people for reasons that have nothing to do with living here — mountain biking, lake access, fishing, and the steady traffic that Highway 16 carries through the middle of town.",
            "That means two very different audiences. Locals, who mostly already know you, and visitors and regional customers, who have no idea you exist and will find you the same way they find everything else: by searching, or by asking an AI assistant on the drive in. The second group is the one a website earns its money on.",
            "For businesses that see seasonal swings — and in the Lakes District most do — that visibility compounds. A site that is properly structured gets recommended year-round, including during the months when you'd otherwise be waiting for the phone to ring.",
        ],
        "hook": "The people who already know you aren't the ones searching for you.",
        "travel": "Burns Lake is about an hour and 15 minutes west of Vanderhoof on Highway 16. In-person visits can be arranged; most web work is remote.",
        "faqs": [
            ("Do you serve Burns Lake and the Lakes District?",
             "Yes. Burns Lake is about an hour and 15 minutes west of Vanderhoof on Highway 16. Web design and AI visibility work is done remotely, and in-person visits — including the $497 Time & Money Audit — can be arranged."),
            ("How much does a website cost in Burns Lake?",
             "Websites start at $800 for a single page and $1,500 for a typical 5–8 page local business site, usually live in 2–4 weeks. Every project is quoted in writing before work begins. The $1,000 AI Visibility Audit checks whether an existing business appears in ChatGPT, Perplexity, and Google AI Overviews. All prices are in Canadian dollars."),
            ("Can a website help with seasonal business?",
             "It's one of the clearer benefits. Seasonal businesses lose visibility in their off months because nothing is reminding search engines they exist. A properly structured site with current content and an accurate Google Business Profile keeps a business appearing in search and AI recommendations year-round, which shortens the ramp when the season turns."),
            ("Do you work with tourism and recreation businesses?",
             "Yes. Visitor-facing businesses benefit most from AI search visibility, because their customers are overwhelmingly people who aren't local and who research before they travel. That's exactly the search behaviour structured data and a complete Google Business Profile are built to capture."),
        ],
    },
    {
        "slug": "web-design-quesnel",
        "city": "Quesnel",
        "region": "BC",
        "eyebrow": "Quesnel, BC · Websites &amp; AI Visibility",
        "h1": "Web Design in Quesnel — For Locals and the Highway 97 Traffic",
        "hero_sub": "Quesnel gets two kinds of customers: the ones who live here, and the ones passing through on the Gold Rush Trail. A good site is built to catch both.",
        "title": "Web Design Quesnel, BC | Gentoolink Web Services",
        "desc": "Website design and AI search visibility for Quesnel and Cariboo businesses. Built for local trade and Highway 97 visitor traffic. Sites from $1,500. Northern BC based.",
        "keywords": "web design Quesnel, website designer Quesnel BC, small business website Quesnel, Cariboo web design, AI visibility Quesnel",
        "local_h2": "Two audiences, one website, and most sites only serve one.",
        "local_body": [
            "Quesnel sits on Highway 97 with the Cariboo to the south and Prince George to the north, and it carries genuine through-traffic — people heading to Barkerville and along the Gold Rush Trail, plus the regular commercial movement between the north and the Interior.",
            "Most Quesnel business websites are written entirely for people who already know the town. They assume you know where the business is, what it's near, and what it's called locally. To a visitor — or to an AI assistant answering a visitor's question — that site says almost nothing useful, and it gets passed over for one that does.",
            "Serving both audiences isn't a matter of writing twice as much. It's a matter of making the basics explicit: what you do, exactly where you are, when you're open, and who you serve — stated clearly on the page and encoded in structured data underneath it.",
        ],
        "hook": "Write for the customer who's never been here, and you keep the one who has.",
        "travel": "Quesnel is roughly two hours south of Vanderhoof via Prince George. Web and AI visibility work is done remotely; in-person visits can be scheduled.",
        "faqs": [
            ("Do you build websites for Quesnel businesses?",
             "Yes. Gentoolink Web Services works with businesses throughout Northern BC and the Cariboo, including Quesnel. Web design and AI visibility work is done remotely, and in-person visits can be scheduled."),
            ("How much does a website cost in Quesnel?",
             "Websites start at $800 for a single page and $1,500 for a typical 5–8 page local business site, usually live in 2–4 weeks. Every project is quoted in writing before work begins. The $1,000 AI Visibility Audit checks whether an existing business shows up in ChatGPT, Perplexity, and Google AI Overviews. All prices are in Canadian dollars."),
            ("How do I get found by visitors passing through on Highway 97?",
             "By making the basics explicit rather than assuming local knowledge: your category, your exact location, your hours, and your service area — stated plainly on the page and encoded in structured data. Visitors and the AI assistants they ask both rely on those signals, because neither has the local context a resident would."),
            ("Do you travel to Quesnel for in-person work?",
             "Quesnel is roughly two hours south of Vanderhoof via Prince George, so in-person visits are arranged rather than routine. Website design, AI visibility audits, and implementation work don't require an in-person visit."),
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Industry pages
# ─────────────────────────────────────────────────────────────────────────────

INDUSTRIES = [
    {
        "slug": "restaurant-website-design",
        "industry": "Restaurants",
        "demo_name": "The Copper Kettle",
        "demo_url": "https://gentoolink.github.io/gentoolink-demo-sites/copper-kettle/",
        "eyebrow": "Restaurant Websites",
        "h1": "Restaurant Websites That Show the Menu and the Hours",
        "hero_sub": "The two things every diner wants are the two things most restaurant sites bury. Yours won't.",
        "title": "Restaurant Website Design | Gentoolink Web Services",
        "desc": "Website design for restaurants and cafés in Northern BC. Menu, hours, and specials front and centre — plus the structured data that gets you into AI recommendations. From $1,500.",
        "keywords": "restaurant website design, cafe website design, menu website, restaurant web design BC, restaurant SEO Northern BC",
        "problem_h2": "What people actually want from a restaurant website.",
        "problem": [
            "Two things, almost always: what's on the menu, and whether you're open right now. Everything else — the story, the photos, the chef's philosophy — matters only after those two questions are answered.",
            "Most restaurant sites get this backwards. The menu is a PDF that won't open properly on a phone, the hours are in an image, and the specials haven't changed since two summers ago. All three of those problems also make you invisible to AI assistants, because a PDF menu and an image of your hours contain nothing a machine can read.",
        ],
        "features": [
            ("Menu that works on a phone", "Real text, not a PDF download. Loads instantly, readable one-handed, and machine-readable so AI tools can answer questions about what you serve."),
            ("Hours that are actually correct", "Marked up with structured data so Google and AI assistants can state whether you're open right now — including holiday hours."),
            ("Specials you can change yourself", "Weekly features shouldn't require a developer. Update by email and the page updates."),
            ("Built for \"where should I eat\" searches", "Cuisine type, price range, location, and dietary options encoded so you appear when someone asks an AI assistant for a recommendation."),
        ],
        "faqs": [
            ("How much does a restaurant website cost?",
             "Restaurant websites from Gentoolink Web Services start at $1,500 for a typical 5–8 page site and are usually live in 2–4 weeks. That includes a mobile-friendly menu, hours, location, and the structured data needed to appear in Google and AI search results. All prices are in Canadian dollars."),
            ("Can I update my menu and specials myself?",
             "Yes. Menu items, prices, and weekly specials can be updated by sending an email — there's no CMS to learn and no login to remember. Changes go live the same day."),
            ("Why shouldn't my menu be a PDF?",
             "PDFs are difficult to read on phones, slow to load, and effectively invisible to AI assistants. When someone asks ChatGPT whether your restaurant has vegetarian options, it can only answer if your menu exists as readable text on the page. A PDF menu means the answer is 'I don't know.'"),
            ("Will my restaurant show up when someone asks AI where to eat?",
             "That's what the structured data is for. Cuisine type, price range, hours, location, and dietary options are encoded in a format AI assistants read directly. Without it, you're relying on the assistant guessing from unstructured text — which usually means it recommends a competitor instead."),
        ],
    },
    {
        "slug": "plumber-website-design",
        "industry": "Plumbers",
        "demo_name": "Precision Plumbing",
        "demo_url": "https://gentoolink.github.io/gentoolink-demo-sites/plumber/",
        "eyebrow": "Plumbing Websites",
        "h1": "Plumber Websites Built to Get the Phone Ringing",
        "hero_sub": "Nobody browses for a plumber. They have a problem right now, they search, and they call the first business that looks like it can help.",
        "title": "Plumber Website Design | Gentoolink Web Services",
        "desc": "Website design for plumbers and plumbing contractors in Northern BC. Built for emergency searches, service areas, and AI recommendations. From $1,500.",
        "keywords": "plumber website design, plumbing website, plumbing contractor web design, trades website BC, plumber SEO Northern BC",
        "problem_h2": "Plumbing searches are urgent. Your site has about four seconds.",
        "problem": [
            "A burst pipe is not a considered purchase. The customer searches, glances at two or three results, and calls whichever one makes it obvious that they handle this, they serve this town, and they can come today.",
            "Most plumbing sites fail at least one of those. The phone number isn't tappable on a phone. The service area is vague or missing. There's no indication whether emergency calls are answered. Every one of those gaps is also a gap in what AI assistants can tell someone who asks for a plumber in your town.",
        ],
        "features": [
            ("Tap-to-call above the fold", "The number is the primary action on every page, tappable on mobile, not buried in a contact form."),
            ("Service area stated plainly", "Every town you cover, listed on the page and encoded in structured data so you appear in searches for each one."),
            ("Emergency availability made obvious", "If you take after-hours calls, that's the single highest-value fact on your site. It gets said clearly."),
            ("Services listed individually", "Drain cleaning, water heaters, repiping, frozen lines — each named, because that's how people search and how AI tools match."),
        ],
        "faqs": [
            ("How much does a plumber website cost?",
             "Plumbing websites from Gentoolink Web Services start at $1,500 for a typical 5–8 page site and are usually live in 2–4 weeks. That includes tap-to-call, a full service list, service area markup, and the structured data needed to appear in Google and AI search results. All prices are in Canadian dollars."),
            ("How do I show up when someone searches for an emergency plumber?",
             "Three things matter most: stating explicitly that you handle emergency and after-hours calls, listing every town in your service area in a machine-readable form, and having a complete Google Business Profile. Most plumbing sites do none of the three, which is why the results are usually easy to take."),
            ("Should I list every town I serve?",
             "Yes — and not just as a sentence. Service areas encoded as structured data let search engines and AI assistants match your business to searches in each specific town. A plumber in Vanderhoof who properly lists Fort St. James and Fraser Lake will appear for searches in all three."),
            ("Will this help me show up in ChatGPT?",
             "It's the main point. When someone asks an AI assistant for a plumber in a specific town, the assistant needs to know your trade, your service area, and your availability in a readable form. The $1,000 AI Visibility Audit checks whether that's currently true for your business."),
        ],
    },
    {
        "slug": "electrician-website-design",
        "industry": "Electricians",
        "demo_name": "Current Electric",
        "demo_url": "https://gentoolink.github.io/gentoolink-demo-sites/electrician/",
        "eyebrow": "Electrical Contractor Websites",
        "h1": "Electrician Websites That Win Both Kinds of Work",
        "hero_sub": "Residential service calls and commercial contracts get found in completely different ways. Most electrical sites are built for only one.",
        "title": "Electrician Website Design | Gentoolink Web Services",
        "desc": "Website design for electricians and electrical contractors in Northern BC. Built for residential service calls and commercial bids alike. From $1,500.",
        "keywords": "electrician website design, electrical contractor website, trades website BC, electrician SEO Northern BC, commercial electrical website",
        "problem_h2": "A homeowner and a general contractor are not looking for the same thing.",
        "problem": [
            "The homeowner with a dead outlet wants to know you're licensed, you're local, and you'll pick up the phone. The GC pricing a commercial job wants to know your certifications, your capacity, and whether you've done work at that scale before.",
            "Most electrical websites pick one audience and quietly lose the other. The fix isn't two websites — it's a site organised so both visitors find their answer in the first few seconds, with the credentials and project types spelled out in a form that search engines and AI tools can also read.",
        ],
        "features": [
            ("Licensing and certification up front", "The first thing both audiences check. Stated plainly, not hidden in an About page."),
            ("Residential and commercial paths", "Clear routes for both, so neither visitor has to guess whether you handle their kind of work."),
            ("Project types named specifically", "Panel upgrades, service changes, generator installs, tenant improvements — named individually, because that's how people search."),
            ("Service area and response time", "Which towns you cover and how fast you get there, encoded so AI assistants can answer both questions."),
        ],
        "faqs": [
            ("How much does an electrician website cost?",
             "Electrical contractor websites from Gentoolink Web Services start at $1,500 for a typical 5–8 page site and are usually live in 2–4 weeks. That includes licensing details, a full service list, service area markup, and structured data for Google and AI search. All prices are in Canadian dollars."),
            ("Should my site target residential or commercial work?",
             "Both, but on separate paths. A homeowner with a dead outlet and a general contractor pricing a tenant improvement need completely different information. One site can serve both if it's organised so each visitor reaches their answer immediately, rather than forcing them through content written for the other."),
            ("What should an electrical contractor list on their website?",
             "Licensing and certifications, the specific project types you handle, your service area by town, and whether you take emergency calls. Each of those is both what customers check and what AI assistants need in order to recommend you for a specific job."),
            ("How do I get found for commercial electrical work?",
             "Name the project types and scales you've worked at, explicitly. General contractors and AI tools both search by specific capability — 'three-phase', 'service upgrade', 'tenant improvement' — not by generic terms like 'electrical services'. Sites that only use generic language don't match those searches."),
        ],
    },
    {
        "slug": "pizza-shop-website-design",
        "industry": "Pizza Shops",
        "demo_name": "Mama Rosa's Pizza",
        "demo_url": "https://gentoolink.github.io/gentoolink-demo-sites/pizzashop/",
        "eyebrow": "Pizza &amp; Fast-Casual Websites",
        "h1": "Pizza Shop Websites Built for the Order, Not the Browse",
        "hero_sub": "Someone deciding on dinner gives you about ten seconds. Menu, price, phone number, done.",
        "title": "Pizza Shop Website Design | Gentoolink Web Services",
        "desc": "Website design for pizzerias and fast-casual restaurants in Northern BC. Fast menus, clear pricing, tap-to-order. Plus AI search visibility. From $1,500.",
        "keywords": "pizza shop website design, pizzeria website, takeout website design, fast casual restaurant website, pizza SEO Northern BC",
        "problem_h2": "Takeout decisions are made fast, usually on a phone, usually hungry.",
        "problem": [
            "There's no browsing phase. Someone wants dinner, they check two or three places, and they order from whichever one made it easiest. A menu that takes six seconds to load has already lost.",
            "The other half of the problem is that a lot of pizza shops have effectively outsourced their web presence to delivery platforms — which take a cut of every order and own the customer relationship. Your own site is the one channel where the whole ticket is yours.",
        ],
        "features": [
            ("Menu and prices load instantly", "No PDF, no app, no loading spinner. Text on a page, readable in one thumb-scroll."),
            ("Tap to order", "Phone number as the primary action, plus links to whatever ordering system you already use."),
            ("Specials and deals up front", "Wing night, family bundles, lunch specials — the things that actually decide the order."),
            ("Findable by craving, not just by name", "Cuisine, dietary options, and price range encoded so you appear when someone asks an AI assistant where to get pizza nearby."),
        ],
        "faqs": [
            ("How much does a pizza shop website cost?",
             "Pizzeria and fast-casual websites from Gentoolink Web Services start at $1,500 for a typical 5–8 page site and are usually live in 2–4 weeks. That includes a fast mobile menu, pricing, tap-to-call ordering, and structured data for Google and AI search. All prices are in Canadian dollars."),
            ("Do I still need a website if I'm on delivery apps?",
             "Delivery platforms take a percentage of every order and own the customer relationship — you don't get the contact details or the repeat business directly. Your own site is the one channel where the full ticket is yours. Most shops keep both, but drive customers toward the site."),
            ("Can customers order directly from the site?",
             "The site links to whatever ordering system you already use, and makes the phone number a one-tap action. There's no need to replace a system that works; the goal is to remove the steps between someone deciding they want pizza and placing the order."),
            ("How do I show up when someone asks AI where to get pizza?",
             "Cuisine type, location, hours, price range, and dietary options need to be encoded as structured data rather than only appearing as text or images. That's what lets an AI assistant confidently include you when someone asks for pizza nearby. The $1,000 AI Visibility Audit checks whether yours is set up correctly."),
        ],
    },
    {
        "slug": "church-website-design",
        "industry": "Churches",
        "demo_name": "Vanderhoof Christian Church",
        "demo_url": "https://gentoolink.github.io/gentoolink-demo-sites/church/",
        "eyebrow": "Church &amp; Community Websites",
        "h1": "Church Websites for the Person Deciding Whether to Walk In",
        "hero_sub": "Your members already know the service times. The website is for the family that just moved to town and is nervous about visiting.",
        "title": "Church Website Design | Gentoolink Web Services",
        "desc": "Website design for churches and community organizations in Northern BC. Service times, events, and a welcoming first impression for newcomers. From $1,500.",
        "keywords": "church website design, ministry website, community organization website, church web design BC, non-profit website Northern BC",
        "problem_h2": "The website's real job is answering a newcomer's quiet questions.",
        "problem": [
            "What time is the service. How long does it run. What do people wear. Is there anything for my kids. Will someone make a fuss over me if I slip in the back.",
            "Almost nobody asks those out loud, and almost no church website answers them. Instead the homepage leads with a mission statement and a newsletter archive — useful to people already inside, invisible to the person sitting in a parked car deciding whether to come in.",
        ],
        "features": [
            ("Service times, unmissable", "Front and centre on every page, marked up so Google and AI assistants can answer 'what time is the service' directly."),
            ("Written for a first-time visitor", "What to expect, what people wear, where to park, what happens with kids — the questions nobody asks out loud."),
            ("Events people can actually find", "Structured event data so your calendar shows up in search rather than living in a PDF bulletin."),
            ("Updatable without a volunteer web team", "Service changes, special events, and cancellations updated by email — no login, no training."),
        ],
        "faqs": [
            ("How much does a church website cost?",
             "Church and community organization websites from Gentoolink Web Services start at $1,500 for a typical 5–8 page site and are usually live in 2–4 weeks. That includes service times, event listings, and the structured data that lets search engines and AI assistants answer questions about your congregation. All prices are in Canadian dollars."),
            ("What should a church website include?",
             "Service times above everything else, followed by what a first-time visitor can expect — dress, parking, length of service, children's programs. Most church sites lead with a mission statement, which serves existing members but tells a newcomer nothing about whether they'd be comfortable walking in."),
            ("Can volunteers update the site?",
             "Updates are made by sending an email — no CMS login, no training session, and nothing that breaks when the volunteer who set it up moves away. Service changes and event cancellations can go live the same day."),
            ("Will our service times show up in Google and AI search?",
             "If they're marked up correctly, yes. Service times encoded as structured data can be returned directly when someone searches or asks an AI assistant what time a church's service starts. Times that only appear inside an image or a PDF bulletin cannot."),
        ],
    },
    {
        "slug": "auto-repair-website-design",
        "industry": "Auto Repair Shops",
        "demo_name": "Vanderhoof Auto Care",
        "demo_url": "https://gentoolink.github.io/gentoolink-demo-sites/auto-repair/",
        "eyebrow": "Auto Repair Websites",
        "h1": "Auto Repair Websites Built on the Thing You Actually Sell: Trust",
        "hero_sub": "Nobody enjoys picking a mechanic. They're choosing who to trust with an expensive problem they can't verify themselves.",
        "title": "Auto Repair Website Design | Gentoolink Web Services",
        "desc": "Website design for auto repair shops and mechanics in Northern BC. Built to establish trust, list services, and capture urgent searches. From $1,500.",
        "keywords": "auto repair website design, mechanic website, auto shop web design, car repair website BC, automotive SEO Northern BC",
        "problem_h2": "Every customer arrives slightly suspicious. That's the starting position.",
        "problem": [
            "People know they can't evaluate the work. They can't tell whether the repair was necessary or whether the price was fair, and most have a story about a shop that took advantage of that. So they look for signals: how long you've been here, whether real people work here, whether the pricing is explained rather than quoted mysteriously.",
            "A website that shows the shop, names the people, and explains what a given job involves does more selling than any list of services. And the same specifics — makes serviced, certifications, warranty terms — are what let an AI assistant recommend you when someone asks for a mechanic in your town.",
        ],
        "features": [
            ("Real photos of the real shop", "Stock images of a generic garage signal the opposite of what you want. Yours should look like yours."),
            ("The people, by name", "Who owns it, who works there, how long they've been doing it. This is the trust signal that converts."),
            ("Services and makes named specifically", "Brakes, diagnostics, tires, fleet work, which makes you specialise in — because that's how people search."),
            ("Hours, location, and how fast you can get them in", "Encoded so AI assistants can answer 'is there a mechanic open in town' without guessing."),
        ],
        "faqs": [
            ("How much does an auto repair website cost?",
             "Auto shop websites from Gentoolink Web Services start at $1,500 for a typical 5–8 page site and are usually live in 2–4 weeks. That includes your service list, shop photos, hours, location, and the structured data needed for Google and AI search results. All prices are in Canadian dollars."),
            ("What makes an auto repair website convert?",
             "Trust signals, more than anything else. Real photos of the actual shop, the names and experience of the people working there, and plain explanations of what common jobs involve. Customers can't evaluate the mechanical work, so they evaluate everything around it."),
            ("Should I list prices on my website?",
             "Full price lists rarely work for repair, since diagnosis drives the cost. What does work is explaining how pricing is determined — diagnostic fees, shop rate, and how estimates are handled. That addresses the fear of being taken advantage of, which is the real objection."),
            ("How do I show up when someone searches for a mechanic nearby?",
             "Hours, location, services, and the makes you work on all need to be in a machine-readable form, backed by a complete Google Business Profile. Someone stranded with a breakdown asks an AI assistant for a nearby shop, and the assistant can only suggest businesses whose details it can actually read."),
        ],
    },
    {
        "slug": "dentist-website-design",
        "industry": "Dental Practices",
        "demo_name": "Vanderhoof Family Dental",
        "demo_url": "https://gentoolink.github.io/gentoolink-demo-sites/dentist/",
        "eyebrow": "Dental &amp; Medical Practice Websites",
        "h1": "Dental Websites Built Around the Two Questions Every Patient Has",
        "hero_sub": "Are you accepting new patients, and do you take my insurance? Everything else is secondary.",
        "title": "Dentist Website Design | Gentoolink Web Services",
        "desc": "Website design for dental practices and clinics in Northern BC. Built for new patient bookings, insurance questions, and anxious first-timers. From $1,500.",
        "keywords": "dentist website design, dental practice website, clinic web design, medical practice website BC, dental SEO Northern BC",
        "problem_h2": "New patients screen you before they ever call.",
        "problem": [
            "Two questions decide whether the phone rings: are you taking new patients, and will my coverage work here. A site that doesn't answer both immediately loses people who would have booked.",
            "Underneath that sits anxiety. A meaningful share of adults avoid the dentist entirely because of it, and they are reading your site looking for evidence that this will be handled gently. Practices that address that directly — plainly, without making it clinical — book patients that competitors never hear from.",
        ],
        "features": [
            ("\"Accepting new patients\" stated clearly", "The single highest-value sentence on a practice website. It belongs where nobody can miss it."),
            ("Insurance and payment answered up front", "Which plans you work with and how direct billing is handled — before someone has to phone and ask."),
            ("Written for anxious patients", "Sedation options, what a first visit involves, and how long it takes. Said plainly, not clinically."),
            ("Bookings and hours machine-readable", "Hours, location, and services encoded so AI assistants can answer patient questions and point people to you."),
        ],
        "faqs": [
            ("How much does a dental practice website cost?",
             "Dental and clinic websites from Gentoolink Web Services start at $1,500 for a typical 5–8 page site and are usually live in 2–4 weeks. That includes new patient information, insurance details, hours, and the structured data needed for Google and AI search results. All prices are in Canadian dollars."),
            ("What should a dental website say first?",
             "Whether you're accepting new patients, and which insurance plans you work with. Those two questions decide whether a prospective patient calls at all. Practices routinely bury both below a welcome message and lose bookings to a competitor who stated them plainly."),
            ("How do I attract patients who avoid the dentist?",
             "Address the anxiety directly on the site. Explain what a first visit actually involves, how long it takes, what sedation or comfort options exist, and that a gap in care won't be met with judgment. Anxious patients read carefully before booking, and most practice websites give them nothing to go on."),
            ("Will my practice show up in AI search results?",
             "Only if your hours, location, services, and new-patient status are published in a machine-readable form and your Google Business Profile is complete and consistent. The $1,000 AI Visibility Audit checks each of those and reports what's missing."),
        ],
    },
    {
        "slug": "salon-website-design",
        "industry": "Salons &amp; Spas",
        "demo_name": "The Velvet Chair Salon",
        "demo_url": "https://gentoolink.github.io/gentoolink-demo-sites/salon/",
        "eyebrow": "Salon &amp; Beauty Websites",
        "h1": "Salon Websites Where the Work Speaks and the Booking Is One Tap",
        "hero_sub": "Clients choose a stylist by looking. Then they book — or they don't, depending on how many steps you put in the way.",
        "title": "Salon Website Design | Gentoolink Web Services",
        "desc": "Website design for hair salons, spas, and beauty businesses in Northern BC. Gallery-led, one-tap booking, and AI search visibility. From $1,500.",
        "keywords": "salon website design, hair salon website, spa website design, beauty business website BC, salon SEO Northern BC",
        "problem_h2": "This is a visual business with mostly non-visual websites.",
        "problem": [
            "Nobody picks a stylist from a bulleted service list. They look at work — colour, cuts, the general feel of the place — and decide whether it matches what they want. A site with no gallery is asking clients to take a risk they don't need to take.",
            "The second failure is the booking step. Clients decide in the moment, usually on a phone, often in the evening. If booking means calling during business hours, a meaningful share of those decisions evaporate before morning.",
        ],
        "features": [
            ("Gallery-led layout", "Your actual work, sized properly, loading fast. The single biggest factor in whether someone books."),
            ("One-tap booking", "Links straight into whatever booking system you use, or tap-to-call. No form, no waiting for a callback."),
            ("Services and pricing ranges", "Cut, colour, extensions, treatments — with honest ranges, so nobody is surprised at the chair."),
            ("Stylists with their own specialties", "Named, with what each one is known for, so clients can request the right person."),
        ],
        "faqs": [
            ("How much does a salon website cost?",
             "Salon and spa websites from Gentoolink Web Services start at $1,500 for a typical 5–8 page site and are usually live in 2–4 weeks. That includes a work gallery, service list, booking links, and the structured data needed for Google and AI search. All prices are in Canadian dollars."),
            ("Does my salon website need a gallery?",
             "It's the most important element on the page. Clients choose a stylist visually — they want to see colour work and cuts before they trust someone with their hair. A service list without images asks people to take a risk, and many won't."),
            ("Should I list my prices?",
             "Ranges work better than either exact prices or no prices at all. Ranges set expectations, filter out mismatched enquiries, and remove the awkwardness of asking. Salons that publish nothing tend to field more price-shopping calls, not fewer."),
            ("Can the site connect to my booking system?",
             "Yes. The site links directly into whatever system you already use, so there's nothing to migrate. The goal is removing steps between deciding and booking — most clients decide in the evening, and anything that requires calling during business hours loses a share of them."),
        ],
    },
    {
        "slug": "landscaping-website-design",
        "industry": "Landscapers",
        "demo_name": "Northern Terrain Landscaping",
        "demo_url": "https://gentoolink.github.io/gentoolink-demo-sites/landscaper/",
        "eyebrow": "Landscaping &amp; Outdoor Websites",
        "h1": "Landscaping Websites That Work Through the Whole Season",
        "hero_sub": "Your work is visual and your year is seasonal. A portfolio and a site that stays visible in the off months solve both.",
        "title": "Landscaping Website Design | Gentoolink Web Services",
        "desc": "Website design for landscapers and outdoor contractors in Northern BC. Portfolio-led, seasonal service listings, and year-round AI search visibility. From $1,500.",
        "keywords": "landscaping website design, landscaper website, lawn care website, outdoor contractor web design BC, landscaping SEO Northern BC",
        "problem_h2": "Before-and-after photos sell landscaping. Nothing else comes close.",
        "problem": [
            "A homeowner considering a few thousand dollars of yard work wants to see a yard like theirs that you've already transformed. A description of your services does not do that job, and no amount of good copywriting substitutes for the photo.",
            "The seasonal side is the other half. In Northern BC the work compresses into a short window, and most landscaping sites go quiet the rest of the year — which means search engines and AI tools quietly deprioritise them. By the time spring arrives, you're rebuilding visibility instead of taking bookings.",
        ],
        "features": [
            ("Before-and-after portfolio", "Organised by project type, sized to load fast. This is what closes the job."),
            ("Seasonal services, all listed", "Spring cleanup, irrigation, hardscaping, snow removal — the winter services are what keep you visible year-round."),
            ("Service area by town", "Encoded so you appear in searches for each community you'll actually drive to."),
            ("Quote requests that capture the details", "Property size, project type, and timeline gathered up front, so you're not making three calls to price one job."),
        ],
        "faqs": [
            ("How much does a landscaping website cost?",
             "Landscaping and outdoor contractor websites from Gentoolink Web Services start at $1,500 for a typical 5–8 page site and are usually live in 2–4 weeks. That includes a project portfolio, seasonal service listings, service area markup, and structured data for Google and AI search. All prices are in Canadian dollars."),
            ("What matters most on a landscaping website?",
             "Before-and-after photographs, organised by project type. Homeowners spending several thousand dollars want to see a property similar to theirs that you've already transformed. No written description does that job, which is why portfolio-led sites consistently outperform service-list sites."),
            ("How do I stay visible during the off season?",
             "By listing the services you offer year-round — snow removal, planning consultations, winter pruning — rather than letting the site go quiet. Search engines and AI tools deprioritise businesses that appear seasonally inactive, so a site that stops updating in October is rebuilding its position every spring."),
            ("Should I list the towns I serve?",
             "Yes, individually and in machine-readable form. A landscaper based in Vanderhoof who properly lists Fort St. James, Fraser Lake, and Prince George will appear in searches for all four. A vague 'serving Northern BC' matches far fewer searches than the specific town names."),
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Standalone service pages
# ─────────────────────────────────────────────────────────────────────────────

SERVICES = [
    {
        "slug": "google-business-profile-management",
        "name": "Google Business Profile Management",
        "service_type": "Google Business Profile Optimization",
        "title": "Google Business Profile Management | Gentoolink Web Services",
        "desc": "Google Business Profile tune-ups and ongoing management for Northern BC businesses. The single biggest lever in local search and AI recommendations. $250 tune-up, $150/mo managed.",
        "keywords": "Google Business Profile management, GBP optimization, Google Business Profile help Prince George, local SEO Northern BC, Google Maps listing",
        "eyebrow": "Google Business Profile · Local Visibility",
        "h1": "Your Google Business Profile Is Doing More Work Than Your Website",
        "hero_sub": "It is the first thing a local customer sees, the thing Google Maps ranks, and one of the strongest signals an AI assistant uses to decide who to recommend. Most are claimed once and never touched again.",
        "hero_trust": "Tune-up $250, one-time. Ongoing management $150/month. No contract.",
        "cta_label": "Get My Profile Tuned Up",
        "low_price": "250",
        "problem_h2": "Claimed in 2019, never opened since.",
        "problem": [
            "That is the state of most local business profiles. The hours are wrong at Christmas, the phone number is the old one, there are three photos from a flip phone, the category is vaguely close but not right, and the last four reviews have no reply.",
            "Every one of those is a ranking factor. Google reads profile completeness, category accuracy, photo recency, and review responsiveness as signals of whether a business is active and worth showing. A neglected profile gets quietly demoted in the map pack, which is where most local searches actually end.",
            "It matters twice over now. AI assistants lean heavily on Google Business Profile data when someone asks for a local recommendation, because it is structured, verified, and current in a way most small business websites are not. An incomplete profile means the assistant has less to go on, and it recommends whoever gave it more.",
        ],
        "hook": "This is the cheapest ranking work available to a local business. It is also the most commonly skipped.",
        "features_h2": "What the tune-up covers.",
        "features": [
            ("Categories and services", "Primary and secondary categories chosen against what customers actually search, plus every service listed individually rather than lumped into one description."),
            ("NAP consistency", "Name, address, and phone matched exactly across your profile, your website, and your schema markup. Mismatches quietly suppress local rankings."),
            ("Hours, including the awkward ones", "Regular hours, holiday hours, and seasonal changes set properly so Google can state whether you are open right now."),
            ("Photos and products", "Current photos, correctly sized and geotagged, plus products or services populated where your category supports it."),
            ("Reviews and Q&A", "Existing reviews replied to, and the Q&A section seeded with the questions customers actually ask instead of left blank."),
            ("Posts and updates", "Set up so the profile shows recent activity, which is a live signal to both Google and AI assistants that the business is operating."),
        ],
        "tables": [
            {
                "label": "Pricing",
                "h2": "Two ways to do this.",
                "intro": "Most businesses start with the one-time tune-up and add ongoing management only if they want the posting and review work handled for them.",
                "rows": [
                    ("Google Business Profile tune-up", "$250", "One-time. Full audit and cleanup of categories, NAP, hours, photos, services, and Q&A."),
                    ("Ongoing profile management", "$150/mo", "Monthly posts, review monitoring and replies, hours and seasonal updates, performance reporting."),
                ],
            },
        ],
        "faqs": [
            ("What does a Google Business Profile tune-up include?",
             "A full audit and cleanup: primary and secondary category selection, every service listed individually, name/address/phone consistency across the profile and website, regular and holiday hours, current photos, products or services populated, replies to existing reviews, and a seeded Q&A section. The tune-up is $250 CAD, one-time."),
            ("Why does my Google Business Profile matter for AI search?",
             "AI assistants rely heavily on Google Business Profile data when answering local recommendation questions, because it is structured, verified, and current in a way most small business websites are not. When someone asks an assistant for a plumber or a dentist in a specific town, an incomplete profile gives it less to work with, so it recommends a business that supplied more."),
            ("Do I need ongoing management, or is a one-time tune-up enough?",
             "For many businesses a one-time tune-up is enough, particularly if your hours and services rarely change. Ongoing management at $150/month makes sense if you get steady reviews that need replies, run seasonal hours, or want regular posts keeping the profile visibly active. Start with the tune-up and add management only if you want it."),
            ("Will this help me show up in the Google Maps pack?",
             "It is the main lever. The map pack weighs profile completeness, category accuracy, proximity, review volume and recency, and how responsive the business appears. Proximity cannot be changed, but everything else on that list is exactly what the tune-up addresses."),
            ("Can you manage a profile for a business outside Northern BC?",
             "Yes. Google Business Profile work is done remotely and does not require an in-person visit, so it works for businesses anywhere in Canada. The in-person services, like the Time & Money Audit, are the ones limited to the Northern BC service area."),
        ],
        "cta_h2": "Find out what your profile is missing.",
        "cta_body": "Send me your business name and I will look at your Google Business Profile and tell you what is incomplete — categories, hours, photos, review replies, the lot. No charge for the look.",
        "cta_btn": "Check My Profile",
    },
    {
        "slug": "ai-phone-receptionist",
        "name": "AI Phone Receptionist",
        "service_type": "AI Phone Answering Service",
        "title": "AI Phone Receptionist for Small Business | Gentoolink Web Services",
        "desc": "An AI receptionist that answers every call, takes the details, and texts you the message. Built for trades and small businesses that lose jobs to voicemail. $500 setup, $249/month.",
        "keywords": "AI phone receptionist, AI answering service small business, virtual receptionist BC, never miss a call trades, automated phone answering Northern BC",
        "eyebrow": "AI Phone Receptionist · Never Miss a Call",
        "h1": "The Job Went to Whoever Answered the Phone",
        "hero_sub": "You were under a sink, on a roof, or driving. It rang out. They called the next name on the list and never called back — and you never knew it happened.",
        "hero_trust": "$500 setup, $249/month. Answers 24/7, texts you every message. Cancel anytime.",
        "cta_label": "Set Up My Receptionist",
        "low_price": "500",
        "problem_h2": "Voicemail is not a safety net. It is where leads go to die.",
        "problem": [
            "Most people calling a trade or a small business will not leave a voicemail. They hang up and dial the next result. You never see the missed call as a lost job, because nothing about it looks like a loss — it looks like a number you did not recognise.",
            "The awkward part is that the calls you miss are not spread evenly. They cluster exactly when you are busiest: mid-job, mid-drive, mid-season. The better the work is going, the more of it you are quietly turning away.",
            "Hiring a receptionist for this does not pencil out for a small operation, and answering services are expensive and generic. An AI receptionist sits in the gap: it picks up on the first ring every time, sounds normal, gets the caller's name, number, and what they need, and texts it to you before you have put the wrench down.",
        ],
        "hook": "It does not need to be better than you on the phone. It needs to be better than ringing out.",
        "features_h2": "What it actually does.",
        "features": [
            ("Answers on the first ring, always", "No hold music, no queue. It picks up at 2pm on a Tuesday and 9pm on a Sunday, in the same voice."),
            ("Takes the details that matter", "Name, callback number, what they need, and how urgent it is. Configured around the questions your trade actually needs answered."),
            ("Texts you immediately", "The full message arrives as a text the moment the call ends, so you can decide whether it is worth stopping for."),
            ("Answers the questions it can", "Hours, service area, whether you handle a given job, roughly how booking works. The routine questions stop interrupting you."),
            ("Books or routes as configured", "It can push callers to your booking link, take a callback slot, or flag genuine emergencies so those reach you differently."),
            ("Sounds like a person, not a phone tree", "No menus, no press-one-for-service. Callers speak normally and it responds normally."),
        ],
        "tables": [
            {
                "label": "Pricing",
                "h2": "What it costs.",
                "intro": "One setup fee to configure it around your business, then a flat monthly rate. No per-minute billing and no contract.",
                "rows": [
                    ("AI phone receptionist — setup", "$500", "One-time. Voice, script, questions, routing rules, and integration with your existing number."),
                    ("AI phone receptionist — monthly", "$249/mo", "Ongoing service, 24/7 answering, message delivery, and adjustments as your business changes."),
                ],
            },
        ],
        "faqs": [
            ("How much does an AI phone receptionist cost?",
             "Setup is $500 CAD one-time, which covers configuring the voice, the script, the questions it asks, routing rules, and integration with your existing phone number. Ongoing service is $249 CAD per month, flat, with no per-minute charges and no contract."),
            ("Do I have to change my phone number?",
             "No. The receptionist works with your existing number. Calls are forwarded to it, either on every call or only when you do not pick up within a set number of rings, which is the more common setup."),
            ("Will callers know they are talking to an AI?",
             "It is not disguised as a human, and it should not be. In practice most callers do not mind, because the alternative they are comparing it to is voicemail. What they care about is that someone picked up and their message reached you."),
            ("What happens with emergency calls?",
             "Urgent calls can be flagged and routed differently — forwarded straight through to your cell, sent as a priority text, or escalated to a second number. The rules are set during setup around what counts as an emergency in your trade."),
            ("What if it cannot answer a caller's question?",
             "It takes the details and tells the caller you will follow up, which is the correct outcome. It is configured to be straightforward about what it does not know rather than guessing, because a wrong answer about pricing or availability costs more than a callback."),
        ],
        "cta_h2": "Stop losing jobs to a ringing phone.",
        "cta_body": "Tell me roughly how many calls you miss in a week and what your average job is worth, and I will tell you honestly whether this pays for itself. For some businesses it does not — I would rather say so.",
        "cta_btn": "See If It Pays Off",
    },
    {
        "slug": "website-hosting-care-plans",
        "name": "Website Hosting and Care Plans",
        "service_type": "Website Hosting and Maintenance",
        "title": "Website Hosting & Care Plans | Gentoolink Web Services",
        "desc": "Managed hosting, backups, security monitoring, and a real person to email when you need a change. Plans from $25/month for Northern BC businesses.",
        "keywords": "website hosting Northern BC, website maintenance plan, website care plan BC, managed hosting small business, website updates Prince George",
        "eyebrow": "Hosting &amp; Care Plans",
        "h1": "Someone to Email When the Site Needs Changing",
        "hero_sub": "Most small business websites are built once and then quietly abandoned — no backups, no updates, and nobody to call when the hours change or something breaks.",
        "hero_trust": "Hosting from $25/month. Care plans from $40/month, including edits. No lock-in.",
        "cta_label": "Get on a Care Plan",
        "low_price": "25",
        "problem_h2": "The site was finished. Then nothing happened to it for four years.",
        "problem": [
            "This is the normal life cycle of a small business website. It launches, it looks good, and then the person who built it moves on. The hours go stale, the seasonal banner from two summers ago is still up, and nobody has taken a backup since launch.",
            "The failure mode is rarely dramatic. It is a price that has been wrong for eight months, a contact form that quietly stopped delivering, or a certificate that expired on a long weekend. Small things, but each one is a customer who did not get through.",
            "The other half is friction. When changing a phone number means finding an old email thread and hoping someone replies, most owners simply do not bother — and the site drifts further from the truth every month.",
        ],
        "hook": "A website that is wrong is worse than one that is plain. Keeping it true is the cheap part.",
        "features_h2": "What is actually handled.",
        "features": [
            ("Managed hosting", "Fast, monitored hosting with SSL kept current. You are not administering a server or renewing a certificate at midnight."),
            ("Backups that get tested", "Regular automated backups, and a restore path that has actually been checked rather than assumed."),
            ("Security monitoring", "Uptime and integrity monitoring, so a problem gets caught before a customer finds it for you."),
            ("Edits by email", "Send the change you want in plain English. No CMS login, no ticket system, no training session."),
            ("Someone who knows your site", "The same person every time, who already knows how your site is built and does not need it re-explained."),
        ],
        "tables": [
            {
                "label": "Plans",
                "h2": "Hosting and care plans.",
                "intro": "Hosting alone keeps the site online. A care plan adds a set allowance of edits so small changes stop being a project.",
                "rows": [
                    ("Managed hosting — static sites", "$25/mo", "For low-maintenance sites that change rarely."),
                    ("Managed hosting — dynamic sites", "$75/mo", "For sites with frequent updates, bookings, or a store."),
                    ("Security monitoring add-on", "$15/mo", "Added to either hosting tier."),
                    ("Lean Care Plan", "$40/mo", "Hosting, backups, security, plus 2 small edits per quarter."),
                    ("Growth Care Plan", "$85/mo", "Hosting plus a monthly edit allowance and priority turnaround."),
                ],
            },
            {
                "label": "One-off changes",
                "h2": "Not on a plan? Changes are priced individually.",
                "intro": "Every change is quoted in writing before any work starts. These are starting points.",
                "rows": [
                    ("Small edit", "$50", "Text or image swap, updating hours or prices."),
                    ("New page", "$150", "Matching your existing design."),
                    ("New section or feature", "$250", "Form, gallery, or booking widget."),
                    ("DNS or domain change", "$50", "Including moves between providers."),
                    ("Larger functionality", "$500", "Store, member area, or redesign."),
                    ("Rush turnaround", "+25%", "Completed within 48 hours."),
                ],
            },
            {
                "label": "Bundles",
                "h2": "Or bundle it with your local visibility work.",
                "intro": "These combine a care plan with the Google Business Profile work most local businesses need anyway.",
                "rows": [
                    ("Foundation", "$300 + $40/mo", "Google Business Profile tune-up plus the Lean Care Plan."),
                    ("Complete", "$1,050 + $644/mo", "Foundation upgraded to the Growth Care Plan, plus an AI customer service assistant and ongoing local visibility management."),
                ],
            },
        ],
        "faqs": [
            ("How much does website hosting cost?",
             "Managed hosting starts at $25 CAD per month for static, low-maintenance sites and $75 per month for dynamic sites with frequent updates or a store. Security monitoring can be added for $15 per month. Care plans, which bundle hosting with an allowance of edits, start at $40 per month."),
            ("What is the difference between hosting and a care plan?",
             "Hosting keeps the site online, backed up, and secure. A care plan adds a set allowance of content changes — the Lean Care Plan includes 2 small edits per quarter at $40/month, and the Growth Care Plan includes a monthly allowance with priority turnaround at $85/month. If you rarely change anything, hosting alone is enough."),
            ("What counts as a small edit?",
             "Swapping text or an image, updating your hours, or changing a price. Larger work — a new page, a new section or feature, or new functionality like a store — is quoted separately, starting at $150, $250, and $500 respectively. Everything is quoted in writing before work begins."),
            ("Do I have to sign a contract?",
             "No. Hosting and care plans are month to month and can be cancelled at any time. If you leave, the site is yours and it can be moved to another host."),
            ("Can you take over hosting for a site someone else built?",
             "Usually yes, depending on how it was built. Static and standard small business sites migrate easily. It is worth a look first, because occasionally a site is tied to a proprietary platform that cannot be moved without rebuilding it."),
        ],
        "cta_h2": "Tell me what your site is running on.",
        "cta_body": "I will tell you what it would take to move it, what it would cost to keep, and whether a care plan is worth it for how often you actually change things. If hosting alone is enough for you, I will say that.",
        "cta_btn": "Ask About Hosting",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def faq_schema(page_id, faqs):
    return {
        "@type": "FAQPage",
        "@id": f"{page_id}#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def breadcrumb(name, url):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": name, "item": url},
        ],
    }


def faq_html(faqs):
    """Renders the FAQ block, matching the .objections-list pattern used site-wide."""
    rows = []
    for q, a in faqs:
        rows.append(
            f"""      <div class="objection">
        <p class="objection-q">{q}</p>
        <p class="objection-a">{a}</p>
      </div>"""
        )
    return "\n\n".join(rows)


def footer_areas(current_slug):
    links = []
    for c in CITIES:
        if c["slug"] == current_slug:
            links.append(
                f'        <span class="footer-area-current">{c["city"]}</span>'
            )
        else:
            links.append(
                f'        <a href="{c["slug"]}.html">{c["city"]}</a>'
            )
    return "\n".join(links)


def render(shell_vars, body, slug):
    out = SHELL
    for key, val in shell_vars.items():
        out = out.replace("{{" + key + "}}", val)
    out = out.replace("{{BODY}}", body)
    out = out.replace("{{FOOTER_AREAS}}", footer_areas(slug))
    return out


def write(slug, html):
    path = os.path.join(ROOT, f"{slug}.html")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print(f"  wrote {slug}.html")


# ─────────────────────────────────────────────────────────────────────────────
# City page builder
# ─────────────────────────────────────────────────────────────────────────────


def build_city(c):
    slug = c["slug"]
    url = f"{SITE}/{slug}.html"
    city = c["city"]

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": url,
                "url": url,
                "name": f"Web Design in {city}, BC — Gentoolink Web Services",
                "description": c["desc"],
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": f"{SITE}/#organization"},
                "inLanguage": "en-CA",
                "breadcrumb": breadcrumb(f"Web Design {city}", url),
                "mainEntity": {"@id": f"{url}#faq"},
            },
            {
                "@type": "Service",
                "@id": f"{url}#service",
                "name": f"Website Design and AI Visibility in {city}, BC",
                "description": (
                    f"Small business website design, AI search visibility audits, and "
                    f"Google Business Profile optimization for businesses in {city}, "
                    f"British Columbia. Provided by Gentoolink Web Services of Vanderhoof, BC."
                ),
                "provider": {"@id": f"{SITE}/#organization"},
                "serviceType": "Website Design and AI Search Visibility",
                "areaServed": {
                    "@type": "City",
                    "name": city,
                    "containedInPlace": {
                        "@type": "AdministrativeArea",
                        "name": "British Columbia",
                    },
                },
                "offers": {
                    "@type": "AggregateOffer",
                    "lowPrice": "800",
                    "highPrice": "2000",
                    "priceCurrency": "CAD",
                    "offerCount": 3,
                    "availability": "https://schema.org/InStock",
                    "url": url,
                },
            },
            faq_schema(url, c["faqs"]),
        ],
    }

    local_paras = "\n".join(f'    <p class="lead">{p}</p>' for p in c["local_body"])

    body = f"""
<!-- ─── Hero ─────────────────────────────────────────────── -->
<section id="hero">
  <div class="container">
    <div class="hero-grid">
      <div class="hero-copy">
        <div class="hero-eyebrow">{c["eyebrow"]}</div>
        <h1 class="gradient-text">{c["h1"]}</h1>
        <p class="hero-sub">{c["hero_sub"]}</p>
        <div class="hero-cta-row">
          <a href="contact.html" class="btn-primary">Get a Free Spot-Check</a>
        </div>
        <p class="hero-trust">Websites from $800. AI Visibility Audit $1,000, delivered in 24 hours. Based in Vanderhoof, BC.</p>
      </div>
      <div class="agent-console">
        <div class="console-header">
          <span class="console-dot red"></span>
          <span class="console-dot yellow"></span>
          <span class="console-dot green"></span>
          <span class="console-title">visibility-scan — {city.lower().replace(". ", "-").replace(" ", "-")}</span>
        </div>
        <div class="console-body">
          <div class="agent-row">
            <div class="agent-header">
              <span class="agent-name"><span class="agent-dot amber"></span>Google ranking</span>
              <span class="agent-status status-building">PAGE 1</span>
            </div>
            <span class="agent-detail">the part most businesses already pay for</span>
          </div>
          <div class="agent-row">
            <div class="agent-header">
              <span class="agent-name"><span class="agent-dot amber"></span>ChatGPT mention</span>
              <span class="agent-status status-building">NOT FOUND</span>
            </div>
            <span class="agent-detail">asked for a recommendation in {city} — named someone else</span>
          </div>
          <div class="agent-row">
            <div class="agent-header">
              <span class="agent-name"><span class="agent-dot amber"></span>Structured data</span>
              <span class="agent-status status-building">MISSING</span>
            </div>
            <span class="agent-detail">no machine-readable location or service area</span>
          </div>
          <div class="agent-row">
            <div class="agent-header">
              <span class="agent-name"><span class="agent-dot green"></span>The fix</span>
              <span class="agent-status status-active">24 HRS</span>
            </div>
            <span class="agent-detail">audit first, so you know before you spend</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ─── Local context ─────────────────────────────────────── -->
<section id="local">
  <div class="container">
    <div class="section-label">{city}, British Columbia</div>
    <h2>{c["local_h2"]}</h2>
{local_paras}
    <p class="hook">{c["hook"]}</p>
  </div>
</section>

<!-- ─── Services ──────────────────────────────────────────── -->
<section id="services" style="background: var(--bg-card);">
  <div class="container">
    <div class="section-label">What I Do for {city} Businesses</div>
    <h2>Three ways in. Start wherever it hurts.</h2>

    <div class="services-grid" style="margin-top: 40px;">

      <div class="service-card">
        <div class="service-icon"><i class="fa-solid fa-globe"></i></div>
        <div class="service-tag">From $800</div>
        <h3>Website Design &amp; Build</h3>
        <p>A complete small business website, built mobile-first with the structured data baked in from the start. Domain and DNS setup included, and you update it forever by sending an email — no CMS, no login.</p>
        <ul class="service-features">
          <li>Landing page, single page — from $800</li>
          <li>Local business site, 5–8 pages — from $1,500</li>
          <li>Product launch site — from $2,000</li>
          <li>Store +$500 · logo +$500 · copywriting +$300</li>
        </ul>
        <a href="templates.html" class="post-read-more">See example designs →</a>
      </div>

      <div class="service-card">
        <div class="service-icon"><i class="fa-solid fa-magnifying-glass-chart"></i></div>
        <div class="service-tag">$1,000</div>
        <h3>AI Visibility Audit</h3>
        <p>Find out whether your {city} business actually appears when someone asks ChatGPT, Perplexity, or Google AI for a recommendation in your category. Delivered as a plain-English PDF within 24 hours.</p>
        <ul class="service-features">
          <li>Tested against the real AI platforms</li>
          <li>Bing indexing, schema, and Google Business Profile checked</li>
          <li>Includes a competitive comparison</li>
        </ul>
        <a href="services.html" class="post-read-more">What's included →</a>
      </div>

      <div class="service-card">
        <div class="service-icon"><i class="fa-solid fa-stopwatch"></i></div>
        <div class="service-tag">$497 · In person</div>
        <h3>Time &amp; Money Audit</h3>
        <p>Not a web problem — an office one. I visit your business, follow the paperwork, and put real numbers on where hours and dollars leak out of quoting, invoicing, and follow-ups.</p>
        <ul class="service-features">
          <li>Done in person, in your business</li>
          <li>Written plan, fixes ranked by impact</li>
          <li>Fee credited toward the fixes</li>
        </ul>
        <a href="time-money-audit.html" class="post-read-more">How it works →</a>
      </div>

    </div>

    <p class="pricing-note" style="margin-top: 28px;">These are starting points, not final numbers — every project is scoped and quoted in writing before any work begins, and typical builds run 2–4 weeks. {c["travel"]}</p>
  </div>
</section>

<!-- ─── FAQ ───────────────────────────────────────────────── -->
<section id="faq">
  <div class="container">
    <div class="section-label">Common Questions</div>
    <h2>What {city} owners ask.</h2>
    <div class="objections-list">

{faq_html(c["faqs"])}

    </div>
  </div>
</section>

<!-- ─── Final CTA ─────────────────────────────────────────── -->
<section id="cta" style="background: var(--bg-card);">
  <div class="container">
    <div class="cta-center">
      <h2>Find out where you stand in {city}.</h2>
      <p class="lead">I'll run a free spot-check: I ask the AI assistants what a customer would ask, in your category, in {city} — and tell you whether your name comes up. No charge, no obligation.</p>
      <a href="contact.html" class="btn-primary" style="font-size: 17px; padding: 16px 36px; margin-top: 12px; display: inline-block;">Get My Free Spot-Check</a>
      <p style="margin-top: 20px; font-size: 14px; color: var(--text-subtle);">Or email <a href="mailto:ken@gentoolinkwebservices.com">ken@gentoolinkwebservices.com</a> · call or text 604-218-7290</p>
    </div>
  </div>
</section>
"""

    shell_vars = {
        "TITLE": c["title"],
        "DESC": c["desc"],
        "KEYWORDS": c["keywords"],
        "CANON": url,
        "OGTITLE": f"Web Design in {city}, BC — Gentoolink Web Services",
        "OGDESC": c["desc"],
        "OGIMG": OG_IMG,
        "SCHEMA": json.dumps(schema, indent=2, ensure_ascii=False),
        "FOOTER_TAG": f"Websites and AI visibility for {city}. <span>Built in Northern BC.</span>",
    }

    write(slug, render(shell_vars, body, slug))


# ─────────────────────────────────────────────────────────────────────────────
# Industry page builder
# ─────────────────────────────────────────────────────────────────────────────


def build_industry(ind):
    slug = ind["slug"]
    url = f"{SITE}/{slug}.html"
    industry = ind["industry"]

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": url,
                "url": url,
                "name": f"{industry} Website Design — Gentoolink Web Services",
                "description": ind["desc"],
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": f"{SITE}/#organization"},
                "inLanguage": "en-CA",
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "name": "Website Templates",
                            "item": f"{SITE}/templates.html",
                        },
                        {"@type": "ListItem", "position": 3, "name": industry, "item": url},
                    ],
                },
                "mainEntity": {"@id": f"{url}#faq"},
            },
            {
                "@type": "Service",
                "@id": f"{url}#service",
                "name": f"Website Design for {industry}",
                "description": ind["desc"],
                "provider": {"@id": f"{SITE}/#organization"},
                "serviceType": "Website Design",
                "areaServed": {"@type": "AdministrativeArea", "name": "British Columbia"},
                "offers": {
                    "@type": "Offer",
                    "price": "1500",
                    "priceCurrency": "CAD",
                    "availability": "https://schema.org/InStock",
                    "url": url,
                },
            },
            faq_schema(url, ind["faqs"]),
        ],
    }

    problem_paras = "\n".join(f'    <p class="lead">{p}</p>' for p in ind["problem"])

    feature_cards = "\n\n".join(
        f"""      <div class="audit-section">
        <h4>{title}</h4>
        <p style="font-size: 15px; color: var(--text-muted); line-height: 1.7; margin: 0;">{desc}</p>
      </div>"""
        for title, desc in ind["features"]
    )

    body = f"""
<!-- ─── Hero ─────────────────────────────────────────────── -->
<section id="hero">
  <div class="container">
    <div class="hero-grid">
      <div class="hero-copy">
        <div class="hero-eyebrow">{ind["eyebrow"]}</div>
        <h1 class="gradient-text">{ind["h1"]}</h1>
        <p class="hero-sub">{ind["hero_sub"]}</p>
        <div class="hero-cta-row">
          <a href="{ind["demo_url"]}" target="_blank" rel="noopener" class="btn-primary">View the Live Demo →</a>
        </div>
        <p class="hero-trust">From $1,500 for a typical 5&ndash;8 page site, usually live in 2&ndash;4 weeks. Structured data included so AI assistants can actually read your site.</p>
      </div>
    </div>
  </div>
</section>

<!-- ─── Problem ───────────────────────────────────────────── -->
<section id="problem">
  <div class="container">
    <div class="section-label">The Problem</div>
    <h2>{ind["problem_h2"]}</h2>
{problem_paras}
  </div>
</section>

<!-- ─── What's included ───────────────────────────────────── -->
<section id="included" style="background: var(--bg-card);">
  <div class="container">
    <div class="section-label">What You Get</div>
    <h2>Built around how your customers actually decide.</h2>
    <div class="audit-grid" style="margin-top: 32px;">

{feature_cards}

    </div>
  </div>
</section>

<!-- ─── Demo ──────────────────────────────────────────────── -->
<section id="demo">
  <div class="container">
    <div class="section-label">Live Demo</div>
    <h2>{ind["demo_name"]}</h2>
    <p class="lead">A complete, working example site for this industry. Click through it — the menus work, the pages are real. If you like the direction, yours gets built the same way with your content, your photos, and your colours.</p>
    <div style="display: flex; gap: 14px; flex-wrap: wrap; margin-top: 28px;">
      <a href="{ind["demo_url"]}" target="_blank" rel="noopener" class="btn-primary">Open the {ind["demo_name"]} Demo →</a>
      <a href="templates.html" class="btn-secondary">See All Nine Templates</a>
    </div>
  </div>
</section>

<!-- ─── FAQ ───────────────────────────────────────────────── -->
<section id="faq" style="background: var(--bg-card);">
  <div class="container">
    <div class="section-label">Common Questions</div>
    <h2>What owners ask before they order.</h2>
    <div class="objections-list">

{faq_html(ind["faqs"])}

    </div>
  </div>
</section>

<!-- ─── Final CTA ─────────────────────────────────────────── -->
<section id="cta">
  <div class="container">
    <div class="cta-center">
      <h2>Want one like it?</h2>
      <p class="lead">Tell me about your business and I'll come back with what your site would look like and exactly what it costs. No deposit, no pressure — and if a new site isn't what you need, I'll tell you that too.</p>
      <a href="contact.html" class="btn-primary" style="font-size: 17px; padding: 16px 36px; margin-top: 12px; display: inline-block;">Start My Website</a>
      <p style="margin-top: 20px; font-size: 14px; color: var(--text-subtle);">Or email <a href="mailto:ken@gentoolinkwebservices.com">ken@gentoolinkwebservices.com</a> · call or text 604-218-7290</p>
    </div>
  </div>
</section>
"""

    shell_vars = {
        "TITLE": ind["title"],
        "DESC": ind["desc"],
        "KEYWORDS": ind["keywords"],
        "CANON": url,
        "OGTITLE": f"{industry} Website Design | Gentoolink Web Services",
        "OGDESC": ind["desc"],
        "OGIMG": OG_IMG,
        "SCHEMA": json.dumps(schema, indent=2, ensure_ascii=False),
        "FOOTER_TAG": f"Websites for {industry.lower()}. <span>Built in Northern BC.</span>",
    }

    write(slug, render(shell_vars, body, slug))


# ─────────────────────────────────────────────────────────────────────────────

def build_service(s):
    slug = s["slug"]
    url = f"{SITE}/{slug}.html"

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": url,
                "url": url,
                "name": f'{s["name"]} — Gentoolink Web Services',
                "description": s["desc"],
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": f"{SITE}/#organization"},
                "inLanguage": "en-CA",
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                        {"@type": "ListItem", "position": 2, "name": "Services",
                         "item": f"{SITE}/services.html"},
                        {"@type": "ListItem", "position": 3, "name": s["name"], "item": url},
                    ],
                },
                "mainEntity": {"@id": f"{url}#faq"},
            },
            {
                "@type": "Service",
                "@id": f"{url}#service",
                "name": s["name"],
                "description": s["desc"],
                "provider": {"@id": f"{SITE}/#organization"},
                "serviceType": s["service_type"],
                "areaServed": [
                    {"@type": "AdministrativeArea", "name": "British Columbia"},
                    {"@type": "Country", "name": "Canada"},
                ],
                "offers": {
                    "@type": "Offer",
                    "price": s["low_price"],
                    "priceCurrency": "CAD",
                    "availability": "https://schema.org/InStock",
                    "url": url,
                },
            },
            faq_schema(url, s["faqs"]),
        ],
    }

    problem_paras = "\n".join(f'    <p class="lead">{p}</p>' for p in s["problem"])

    feature_cards = "\n\n".join(
        f"""      <div class="audit-section">
        <h4>{title}</h4>
        <p style="font-size: 15px; color: var(--text-muted); line-height: 1.7; margin: 0;">{desc}</p>
      </div>"""
        for title, desc in s["features"]
    )

    tables = []
    for idx, t in enumerate(s["tables"]):
        rows = "\n".join(
            f"""          <tr>
            <td class="td-product">{name}</td>
            <td class="td-price">{price}</td>
            <td class="td-note">{note}</td>
          </tr>"""
            for name, price, note in t["rows"]
        )
        bg = ' style="background: var(--bg-card);"' if idx % 2 == 0 else ""
        tables.append(f"""
<section id="pricing-{idx}"{bg}>
  <div class="container">
    <div class="section-label">{t["label"]}</div>
    <h2>{t["h2"]}</h2>
    <p class="lead">{t["intro"]}</p>
    <table class="pricing-table">
      <thead>
        <tr><th scope="col">Service</th><th scope="col">Starting at</th><th scope="col">What it covers</th></tr>
      </thead>
      <tbody>
{rows}
      </tbody>
    </table>
    <p class="pricing-note">Every project is scoped to your business. You get a firm, fixed price in writing before any work begins, and nothing starts without your sign-off. We never bill by the hour.</p>
  </div>
</section>""")

    body = f"""
<!-- ─── Hero ─────────────────────────────────────────────── -->
<section id="hero">
  <div class="container">
    <div class="hero-grid">
      <div class="hero-copy">
        <div class="hero-eyebrow">{s["eyebrow"]}</div>
        <h1 class="gradient-text">{s["h1"]}</h1>
        <p class="hero-sub">{s["hero_sub"]}</p>
        <div class="hero-cta-row">
          <a href="contact.html" class="btn-primary">{s["cta_label"]}</a>
        </div>
        <p class="hero-trust">{s["hero_trust"]}</p>
      </div>
    </div>
  </div>
</section>

<!-- ─── Problem ───────────────────────────────────────────── -->
<section id="problem">
  <div class="container">
    <div class="section-label">The Problem</div>
    <h2>{s["problem_h2"]}</h2>
{problem_paras}
    <p class="hook">{s["hook"]}</p>
  </div>
</section>

<!-- ─── What's included ───────────────────────────────────── -->
<section id="included" style="background: var(--bg-card);">
  <div class="container">
    <div class="section-label">What You Get</div>
    <h2>{s["features_h2"]}</h2>
    <div class="audit-grid" style="margin-top: 32px;">

{feature_cards}

    </div>
  </div>
</section>
{"".join(tables)}

<!-- ─── FAQ ───────────────────────────────────────────────── -->
<section id="faq">
  <div class="container">
    <div class="section-label">Common Questions</div>
    <h2>What owners ask.</h2>
    <div class="objections-list">

{faq_html(s["faqs"])}

    </div>
  </div>
</section>

<!-- ─── Final CTA ─────────────────────────────────────────── -->
<section id="cta" style="background: var(--bg-card);">
  <div class="container">
    <div class="cta-center">
      <h2>{s["cta_h2"]}</h2>
      <p class="lead">{s["cta_body"]}</p>
      <a href="contact.html" class="btn-primary" style="font-size: 17px; padding: 16px 36px; margin-top: 12px; display: inline-block;">{s["cta_btn"]}</a>
      <p style="margin-top: 20px; font-size: 14px; color: var(--text-subtle);">Or email <a href="mailto:ken@gentoolinkwebservices.com">ken@gentoolinkwebservices.com</a> · call or text 604-218-7290</p>
    </div>
  </div>
</section>
"""

    shell_vars = {
        "TITLE": s["title"],
        "DESC": s["desc"],
        "KEYWORDS": s["keywords"],
        "CANON": url,
        "OGTITLE": f'{s["name"]} | Gentoolink Web Services',
        "OGDESC": s["desc"],
        "OGIMG": OG_IMG,
        "SCHEMA": json.dumps(schema, indent=2, ensure_ascii=False),
        "FOOTER_TAG": f'{s["name"]}. <span>Built in Northern BC.</span>',
    }

    write(slug, render(shell_vars, body, slug))


def main():
    print("Building city pages...")
    for c in CITIES:
        build_city(c)
    print("Building industry pages...")
    for i in INDUSTRIES:
        build_industry(i)
    print("Building service pages...")
    for s in SERVICES:
        build_service(s)
    total = len(CITIES) + len(INDUSTRIES) + len(SERVICES)
    print(f"\nDone. {total} pages generated.")


if __name__ == "__main__":
    main()
