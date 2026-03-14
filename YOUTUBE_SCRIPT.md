# YouTube Video Script: CRF Annotation MCP Server

**Target Length:** 6-8 minutes  
**Target Audience:** Clinical programmers, SDTM mappers, AI-curious pharma professionals  
**Tone:** Professional but approachable, demo-focused

---

## 📺 Video Structure

**[0:00-0:30]** Hook + Problem  
**[0:30-1:00]** Solution Introduction  
**[1:00-4:00]** Live Demo (The Wow Moment)  
**[4:00-5:30]** How It Works + Setup  
**[5:30-6:00]** GitHub + Call to Action

---

## 🎬 SCRIPT

### [0:00-0:30] HOOK + PROBLEM

**[Screen: You scrolling through a massive PDF CRF with hundreds of comments]**

> **You (voiceover):**  
> "Picture this: It's Friday afternoon. Your project manager asks, 'Which CRF pages cover adverse events?'"
>
> **[Still scrolling through PDF]**
>
> "You open the 200-page annotated CRF PDF. You start clicking through comment after comment. Demographics... Labs... Vital Signs..."
>
> **[Exasperated expression]**
>
> "An hour later, you finally have the answer."
>
> **[Cut to camera]**
>
> "There's a better way. Let me show you."

**[Title card appears]**

**CRF Annotation MCP**  
*Query SDTM Annotations with AI*

---

### [0:30-1:00] SOLUTION INTRODUCTION

**[Screen: You talking to camera]**

> "I built a tool that lets you query SDTM annotations from annotated CRF PDFs using natural language."
>
> "Instead of manually hunting through a PDF, you ask Claude — or any AI assistant that supports the Model Context Protocol."
>
> **[Quick cuts showing questions appearing:]**
> - "Show me all DM annotations"
> - "What's on page 15?"
> - "Search for adverse event variables"
>
> "And it automatically knows about SDTM domain relationships. When you ask for DM, it includes SUPPDM."
>
> "Let me show you how it works."

---

### [1:00-4:00] LIVE DEMO (THE WOW MOMENT)

**[Screen: Claude Desktop open, split screen with annotated CRF PDF on the side]**

> **"Okay, here's a real annotated CRF. 180 pages. SDTM annotations in the comments."**

**[Show the PDF briefly — lots of pages, lots of annotations]**

---

**DEMO 1: Query by Domain**

> **"Let's say I need all the Demographics annotations. I'll ask Claude:"**

**[Type in Claude Desktop:]**  
`"Show me all DM domain annotations"`

**[Claude responds with:]**

```
Found 4 annotations:

DM.USUBJID - Page 1 - Subject ID
DM.RFSTDTC - Page 1 - Study start date
DM.BRTHDTC - Page 2 - Date of birth
SUPPDM.RACE2 - Page 2 - Secondary race
```

> **"Notice — it automatically included SUPPDM. It knows SDTM domain relationships."**

---

**DEMO 2: Query by Page**

> **"Now let's say I need to know what's annotated on page 15."**

**[Type:]**  
`"What domains are annotated on page 15?"`

**[Claude responds:]**

```
Page 15 contains 3 annotations:

AE.AETERM - Adverse event term
AE.AESTDTC - AE start date
AE.AESER - Serious AE flag
```

> **"Instant answer. No scrolling. No hunting."**

---

**DEMO 3: Free-Text Search**

> **"What if I need all date-related variables across the entire CRF?"**

**[Type:]**  
`"Search for annotations containing 'date'"`

**[Claude responds:]**

```
Found 5 annotations:

DM.RFSTDTC - Page 1 - Study start date
DM.BRTHDTC - Page 2 - Date of birth
AE.AESTDTC - Page 15 - AE start date
AE.AEENDTC - Page 16 - AE end date
VS.VSDTC - Page 10 - Vital signs date
```

> **"Five seconds. No manual search."**

---

**DEMO 4: List All Domains**

> **"Or maybe I just want an overview of all domains in the CRF."**

**[Type:]**  
`"List all SDTM domains in this CRF"`

**[Claude responds:]**

```
SDTM Domains in CRF:

• DM (has SUPP): 3 annotations, 3 variables, pages 1, 2
• AE: 5 annotations, 5 variables, pages 15-18
• VS: 4 annotations, 4 variables, pages 10-12
• LB: 8 annotations, 8 variables, pages 20-25
```

> **"Complete summary. Instantly."**

**[Cut back to camera]**

> **"This is the difference between spending an hour hunting... and getting your answer in five seconds."**

---

### [4:00-5:30] HOW IT WORKS + SETUP

**[Screen: Architecture diagram or code editor]**

> **"So how does this work?"**
>
> **"It's built on the Model Context Protocol — MCP — which is an open standard for connecting AI assistants to external tools."**
>
> **[Show diagram: Annotated CRF PDF → Parser → MCP Server → Claude Desktop]**
>
> "Here's the flow:"
>
> **1. The parser extracts annotations from your PDF**  
> It looks for patterns like `DM.USUBJID` or `SUPPDM.RACE2` in PDF comments.
>
> **2. The query engine indexes them**  
> By domain, by page, by variable name. And it understands SDTM relationships.
>
> **3. The MCP server exposes tools**  
> Claude — or any MCP client — can call these tools with natural language.
>
> **[Show quick setup steps on screen]**
>
> "Setting it up is straightforward:"
>
> ```bash
> # Clone the repo
> git clone https://github.com/vikasgaddu1/crf-annotation-mcp.git
> 
> # Install dependencies
> cd crf-annotation-mcp
> uv pip install -e .
> 
> # Configure Claude Desktop
> # Point it at your annotated CRF PDF
> ```
>
> **[Show the Claude Desktop config snippet]**
>
> "Add this to your Claude Desktop config, point it at your PDF, and you're ready to go."
>
> **[Cut back to camera]**
>
> "Full setup guide is in the README. Takes about 5 minutes."

---

### [5:30-6:00] WORKFLOW + USE CASES

**[Screen: You talking to camera]**

> **"Here's where this fits in your workflow:"**
>
> **"During study startup:**  
> Use this to query annotations while you're building your mapping specs."
>
> **"After dataset creation:**  
> Switch to my other tool — annoSDTMCheck — to validate those annotations against your actual SDTM datasets."
>
> **"They work together:"**
> - **crf-annotation-mcp** = AI-assisted annotation queries (study setup)
> - **annoSDTMCheck** = Validation against data (post-mapping)

---

### [6:00-6:30] GITHUB + CALL TO ACTION

**[Screen: GitHub repo page]**

> **"This is open source. MIT licensed. Available now on GitHub."**
>
> **[Show URL on screen:]**  
> **github.com/vikasgaddu1/crf-annotation-mcp**
>
> "The README has:"
> - Full setup guide
> - Example queries
> - Configuration for Claude Desktop, Cline, and other MCP clients
>
> **[Cut back to camera]**
>
> "If you work with SDTM annotations, give it a try. Let me know what you think in the comments."
>
> **"And if you found this useful, hit subscribe — I'm building more AI tools for clinical programming."**
>
> **[Smile]**
>
> "Thanks for watching. See you in the next one."

**[End screen with:]**
- GitHub link: github.com/vikasgaddu1/crf-annotation-mcp
- LinkedIn: linkedin.com/in/vikasgaddu
- Subscribe button animation

---

## 🎥 PRODUCTION NOTES

### Visuals Needed

1. **Annotated CRF PDF** (sample/demo file)
   - At least 20-30 pages
   - SDTM annotations visible in comments
   - Include DM, SUPPDM, AE, VS, LB domains

2. **Screen recordings:**
   - Claude Desktop demo (all 4 queries)
   - Quick architecture diagram (simple, clean)
   - GitHub repo page walkthrough

3. **B-roll:**
   - You scrolling through PDF (frustrated)
   - Code snippets appearing on screen
   - Setup steps visually highlighted

### Audio

- Clear voiceover (minimal background noise)
- Optional: Subtle background music (royalty-free)
- Sound effects for:
  - Typing queries
  - Results appearing (subtle "whoosh" or "ping")

### Text Overlays

- Question prompts appearing on screen
- Key phrases highlighted:
  - "Automatically includes SUPPDM"
  - "5 seconds vs 1 hour"
  - "Query with natural language"

### Thumbnails (A/B test these)

**Option A:**
- Split screen: Frustrated person vs Happy person
- Text: "Stop Hunting CRF Annotations"
- Before/After style

**Option B:**
- Claude Desktop screenshot with query results
- Text: "Query SDTM Annotations with AI"
- Clean, professional

**Option C:**
- You pointing at screen
- Big text: "AI for CRF Annotations"
- Red arrow pointing to results

---

## 📊 YouTube Metadata

### Title (A/B Test)

**Option 1:** Query SDTM Annotations with AI | CRF Annotation MCP Demo  
**Option 2:** Stop Manually Searching CRF PDFs | AI-Powered SDTM Queries  
**Option 3:** I Built an AI Tool for Clinical Programmers | CRF Annotation MCP

### Description

```
I spent too many hours hunting for SDTM annotations in massive CRF PDFs. So I built a tool to let AI do it for me.

CRF Annotation MCP is an open-source MCP server that lets you query SDTM annotations from annotated CRF PDFs using natural language.

Ask questions like:
• "Show me all DM annotations" (auto-includes SUPPDM!)
• "What's on page 15?"
• "Search for date variables"

And get instant answers.

🔗 GitHub: https://github.com/vikasgaddu1/crf-annotation-mcp
📖 Full Setup Guide: [link to README]
💼 LinkedIn: https://linkedin.com/in/vikasgaddu

⏱️ Timestamps:
0:00 - The Problem
0:30 - Introducing CRF Annotation MCP
1:00 - Live Demo (Query by Domain)
2:00 - Query by Page
2:40 - Free-Text Search
3:20 - List All Domains
4:00 - How It Works
5:30 - Workflow Integration
6:00 - Open Source + Call to Action

Built with Python, MCP protocol, and PyMuPDF. Works with Claude Desktop, Cline, and other MCP clients.

#ClinicalProgramming #CDISC #SDTM #AI #OpenSource #MCP #Python
```

### Tags

- clinical programming
- sdtm
- cdisc
- ai tools
- model context protocol
- mcp
- claude ai
- python
- open source
- pharmaceutical
- clinical trials
- data standards
- automation
- programming

---

## 🎯 KEY MESSAGES TO EMPHASIZE

1. **The pain is real** - Everyone has wasted hours scrolling through CRF PDFs
2. **Natural language queries** - No coding required, just ask
3. **Domain-aware** - Understands SDTM relationships (DM includes SUPPDM)
4. **Open source** - Free, MIT licensed, ready to use
5. **Complements existing tools** - Works with annoSDTMCheck
6. **5 minutes to set up** - Not complicated

---

## 📈 PROMOTION STRATEGY

**Cross-post to:**
- LinkedIn (with video snippet)
- Twitter (thread with key demo GIFs)
- Reddit (r/datascience, r/bioinformatics)
- CDISC community forums

**Follow-up content:**
- Week 2: "5 Ways to Use CRF Annotation MCP"
- Week 3: "How I Built It" (technical deep-dive)
- Week 4: "Community Contributions" (if any PRs/issues)

---

Ready to film! 🎬
