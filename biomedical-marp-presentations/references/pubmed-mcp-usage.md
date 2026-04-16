# Using PubMed MCP for Biomedical Presentations

<overview>
When creating biomedical MARP presentations, ALWAYS prioritize using PubMed MCP (Model Context Protocol) if it's available. MCP provides structured, reliable, and direct access to PubMed data, making it superior to web scraping or generic search.
</overview>

<checking_mcp_availability>
At the start of your workflow, check if PubMed MCP tools are available:
- Look for PubMed-specific tools in your available tools list
- Common tool names might include: `pubmed_search`, `fetch_article`, `get_abstract`, etc.
- If available, you'll see them listed alongside other tools like `web_search`
</checking_mcp_availability>

<why_prioritize_mcp>
<advantages>
✅ **Structured Data**: Returns formatted metadata (PMID, DOI, authors, journal, etc.)
✅ **Direct Access**: No need to parse web pages or search results
✅ **Reliability**: Consistent data format and availability
✅ **Efficiency**: Faster than web scraping
✅ **Completeness**: Access to abstracts, MeSH terms, citation data
✅ **API Compliance**: Follows NCBI usage guidelines automatically
</advantages>

<web_search_limitations>
❌ Requires parsing search result snippets
❌ May miss relevant articles
❌ Less structured data extraction
❌ Slower multi-step process
❌ Potential rate limiting issues
</web_search_limitations>
</why_prioritize_mcp>

<mcp_workflow>
<step_1_search_strategy>
Use MCP to search PubMed with well-constructed queries:

**For Topic Overviews**:
```
Search: "[topic] AND (review[Publication Type] OR systematic review[Publication Type])"
Example: "transcranial magnetic stimulation AND review[Publication Type]"
```

**For Specific Evidence**:
```
Search: "[specific question] AND (randomized controlled trial[Publication Type] OR meta-analysis[Publication Type])"
Example: "TMS treatment resistant depression AND randomized controlled trial[Publication Type]"
```

**For Clinical Guidelines**:
```
Search: "[topic] AND (guideline[Publication Type] OR consensus[Title/Abstract])"
Example: "TMS safety AND guideline[Publication Type]"
```
</step_1_search_strategy>

<step_2_retrieve_data>
For each relevant article found, retrieve:
- **PMID**: For citation and reference tracking
- **Title**: For slide titles and references
- **Authors**: For citation formatting
- **Abstract**: For extracting key findings
- **Journal**: For citation formatting
- **Publication Date**: For recency and citation
- **DOI**: For digital links
- **MeSH Terms**: For understanding article focus
</step_2_retrieve_data>

<step_3_extract_information>
From abstracts and metadata, extract:
- Main findings and conclusions
- Study design and sample size
- Statistical significance (p-values, confidence intervals)
- Clinical implications
- Limitations
</step_3_extract_information>

<step_4_format_citations>
Use the structured data from MCP to format citations:

**Numbered Style** (Preferred for MARP):
```
Author LastName et al. Title. Journal. Year;Volume(Issue):Pages. PMID: 12345678
```

**Example**:
```
George MS et al. Daily left prefrontal transcranial magnetic stimulation therapy for major depressive disorder. Arch Gen Psychiatry. 2010;67(5):507-516. PMID: 20439832
```
</step_4_format_citations>
</mcp_workflow>

<common_search_patterns>
<background_research>
```
Topic: "neuroplasticity mechanisms"
Query: "neuroplasticity AND (review[PT] OR mechanisms[Title])"
Purpose: Foundational knowledge for introduction slides
```
</background_research>

<evidence_synthesis>
```
Topic: "treatment efficacy"
Query: "[intervention] AND [condition] AND (randomized controlled trial[PT] OR meta-analysis[PT])"
Purpose: Evidence slides with statistics
```
</evidence_synthesis>

<clinical_guidelines>
```
Topic: "practice recommendations"
Query: "[procedure] AND (practice guideline[PT] OR guideline[TI])"
Purpose: Clinical application slides
```
</clinical_guidelines>

<safety_information>
```
Topic: "adverse effects"
Query: "[intervention] AND (adverse effects[MeSH] OR safety[Title/Abstract])"
Purpose: Safety and contraindication slides
```
</safety_information>

<mechanism_studies>
```
Topic: "biological mechanisms"
Query: "[topic] AND (mechanism[Title/Abstract] OR pathophysiology[MeSH])"
Purpose: Mechanistic explanatory slides
```
</mechanism_studies>
</common_search_patterns>

<decision_tree>
```
START
  ↓
Is PubMed MCP available?
  ↓
YES → Use MCP for ALL PubMed searches
  ↓
  • Search with structured queries
  • Retrieve complete metadata
  • Extract abstracts directly
  • Format citations from PMID
  ↓
NO → Use web_search as fallback
  ↓
  • Search "pubmed [topic]"
  • Parse search results
  • Extract PMIDs from snippets
  • Use citation_formatter.py script
```
</decision_tree>

<best_practices>
<do>
✅ Use MeSH terms for precision
✅ Filter by publication type (review, RCT, meta-analysis)
✅ Limit to recent publications when appropriate (last 5-10 years)
✅ Retrieve abstracts for all cited articles
✅ Extract exact statistics and findings from abstracts
✅ Use PMIDs for all citations
</do>

<dont>
❌ Use vague search terms
❌ Skip abstract retrieval
❌ Cite articles without reading abstracts
❌ Use outdated references when recent data exists
❌ Forget to include PMIDs in citations
❌ Fall back to web_search if MCP is available
</dont>
</best_practices>

<integration_with_presentation>
<introduction_slides>
- MCP Search: Recent reviews (last 3 years)
- Extract: Current state of field, knowledge gaps
</introduction_slides>

<main_content_slides>
- MCP Search: Primary research on specific topics
- Extract: Key findings, methods, sample sizes
</main_content_slides>

<evidence_slides>
- MCP Search: RCTs and meta-analyses
- Extract: Effect sizes, p-values, clinical significance
</evidence_slides>

<explanatory_slides>
- MCP Search: Mechanism studies, reviews
- Extract: Pathophysiology, theoretical frameworks
</explanatory_slides>

<clinical_application_slides>
- MCP Search: Clinical guidelines, practice recommendations
- Extract: Evidence-based protocols, contraindications
</clinical_application_slides>

<references_slide>
- Format: All PMIDs retrieved via MCP
- Include: Complete citations with PMID numbers
</references_slide>
</integration_with_presentation>

<example_workflow>
**Task**: Create presentation on "TMS Coil Types and Stimulation Patterns"

<background_research>
```
MCP Search: "transcranial magnetic stimulation AND coil design AND review[PT]"
Results: 5 recent reviews
Action: Retrieve abstracts, extract coil types mentioned
```
</background_research>

<technical_details>
```
MCP Search: "TMS AND (figure-8 coil OR H-coil OR circular coil)"
Results: 15 research articles
Action: Extract depth penetration, focality data
```
</technical_details>

<clinical_applications>
```
MCP Search: "repetitive transcranial magnetic stimulation AND (protocol OR frequency)"
Results: Meta-analyses on rTMS, iTBS, cTBS
Action: Extract efficacy data, optimal parameters
```
</clinical_applications>

<safety_information>
```
MCP Search: "transcranial magnetic stimulation AND (safety OR adverse effects)"
Results: Safety guidelines and reviews
Action: Extract contraindications, side effects
```
</safety_information>

<citation_formatting>
- Use PMIDs from all MCP retrievals
- Format with numbered system
- Include in references slide
</citation_formatting>
</example_workflow>

<error_handling>
<no_results>
If MCP Search Returns No Results:
1. Broaden search terms
2. Remove restrictive filters
3. Try alternative terminology
4. Consider related MeSH terms
5. As last resort, use web_search for that specific query
</no_results>

<mcp_unavailable>
If MCP Is Unavailable Mid-Session:
1. Complete current MCP queries
2. Document PMIDs already retrieved
3. Switch to web_search for remaining searches
4. Note the methodology change
</mcp_unavailable>
</error_handling>

<quality_checks>
Before finalizing presentation, verify:
- [ ] All factual claims have PubMed citations
- [ ] PMIDs are correct and match content
- [ ] Abstracts were retrieved and reviewed for all citations
- [ ] Statistics and findings are accurately quoted
- [ ] Citations are formatted consistently
- [ ] Most recent relevant research is included
- [ ] MCP was used for all searches (if available)
</quality_checks>

<summary>
**Golden Rule**: If PubMed MCP is available, use it exclusively for literature searches. Only fall back to web_search if MCP is unavailable or returns insufficient results for a specific query.

MCP provides the structured, reliable access to PubMed that ensures scientific accuracy and proper citation in biomedical presentations.
</summary>
