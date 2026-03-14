# LinkedIn Post: CRF Annotation MCP Server

---

## Version 1: Technical Focus

I just open-sourced a new tool for clinical programmers working with AI assistants.

**CRF Annotation MCP** lets you query SDTM annotations from annotated CRF PDFs using natural language.

Instead of manually scanning a 200-page CRF for domain mappings, you can now ask:
• "Show me all DM annotations" → Returns DM + SUPPDM automatically
• "What's annotated on page 15?" → Lists all domains on that page
• "Search for adverse event variables" → Free-text search across all annotations

It's built on the Model Context Protocol (MCP), so it works with Claude Desktop, Cline, and other AI assistants out of the box.

**Why this matters:**
When you're building specs or mapping studies, you're constantly cross-referencing CRFs, annotations, and SDTM standards. This eliminates the manual lookup.

It complements my earlier annoSDTMCheck project:
• **crf-annotation-mcp** - Query annotations during study setup (AI-assisted)
• **annoSDTMCheck** - Validate annotations against actual datasets (post-mapping)

Built with Python + MCP protocol. MIT licensed.

GitHub: https://github.com/vikasgaddu1/crf-annotation-mcp

#ClinicalProgramming #CDISC #SDTM #AI #OpenSource #MCP

---

## Version 2: Problem-Solution Focus

Ever tried finding a specific SDTM variable annotation in a 200-page CRF PDF?

You're scrolling through Demographics... then Labs... then Adverse Events... clicking through comment after comment.

I got tired of it, so I built something better.

**CRF Annotation MCP** is an AI-powered query tool for annotated CRF PDFs.

Ask questions like:
• "Give me all DM domain annotations" (automatically includes SUPPDM)
• "What domains are on page 15?"
• "Search for all date-related variables"

Works with Claude Desktop, Cline, or any AI assistant that supports MCP.

**The workflow:**
1. Annotate your CRF PDF with SDTM mappings (like you already do)
2. Point the MCP server at your PDF
3. Ask your AI assistant questions about annotations

No more manual hunting. Just ask.

This pairs with my annoSDTMCheck tool:
• **crf-annotation-mcp** - Query annotations while building specs
• **annoSDTMCheck** - Validate annotations against final datasets

Open source. Python-based. Ready to use.

GitHub: https://github.com/vikasgaddu1/crf-annotation-mcp

What do you think? Would this speed up your study startup work?

#ClinicalProgramming #SDTM #CDISC #AI #Automation

---

## Version 3: Story-Based (Most Engaging)

I spent an hour yesterday hunting for SUPPDM annotations in a 180-page CRF.

Page by page. Comment by comment. Building a mental map of where everything was.

There had to be a better way.

So I built one.

**CRF Annotation MCP** - Query SDTM annotations using natural language.

"Show me all DM annotations" → Returns DM.USUBJID, DM.RFSTDTC... and SUPPDM.RACE2.

It automatically knows to include SUPP domains. It can search across pages. It understands domain relationships.

And it works with Claude Desktop right out of the box (or any AI assistant that supports MCP).

**Real use case:**
Your PM asks, "Which CRF pages cover adverse events?"

Before: Open PDF, scan annotations, compile list manually.

Now: Ask Claude, "What pages have AE annotations?" → Instant answer.

This complements my annoSDTMCheck validation tool:
• Use **crf-annotation-mcp** during study setup (query annotations)
• Use **annoSDTMCheck** after mapping (validate against datasets)

Open source. Python. MIT licensed.

GitHub: https://github.com/vikasgaddu1/crf-annotation-mcp

Anyone else tired of manual CRF annotation lookups? What would you use this for?

#ClinicalProgramming #CDISC #SDTM #AI #OpenSource

---

## 📝 Recommendation

**Use Version 3** - It has:
✅ Relatable story opening
✅ Clear problem → solution
✅ Concrete examples
✅ Engagement question at the end
✅ Professional but conversational tone

Post timing: Tuesday or Wednesday morning (8-10 AM EST) for best B2B engagement.
