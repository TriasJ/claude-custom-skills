# Citation Formatting for Biomedical Presentations

<recommended_format>
<overview>
For MARP presentations, use a numbered citation system for cleaner slides.
</overview>

<in_text_citations>
```markdown
TMS demonstrates efficacy in treatment-resistant depression.[1,2]

Meta-analysis shows response rates of 45-60%.[3]

Multiple mechanisms may contribute to therapeutic effects.[4-6]
```
</in_text_citations>

<reference_list_format>
**Standard journal article**:
```
1. Author1 LastName, Author2 LastName, Author3 LastName, et al. Article title. Journal Name. Year;Volume(Issue):StartPage-EndPage. PMID: 12345678
```

**Example**:
```
1. George MS, Lisanby SH, Avery D, et al. Daily left prefrontal transcranial magnetic stimulation therapy for major depressive disorder: a sham-controlled randomized trial. Arch Gen Psychiatry. 2010;67(5):507-516. PMID: 20439832
```

**With DOI**:
```
2. Fitzgerald PB, Fountain S, Daskalakis ZJ. A comprehensive review of the effects of rTMS on motor cortical excitability and inhibition. Clin Neurophysiol. 2006;117(12):2584-2596. doi:10.1016/j.clinph.2006.06.712
```

**Review article**:
```
3. Lefaucheur JP, Aleman A, Baeken C, et al. Evidence-based guidelines on the therapeutic use of repetitive transcranial magnetic stimulation (rTMS): An update (2014-2018). Clin Neurophysiol. 2020;131(2):474-528. PMID: 31901449
```
</reference_list_format>
</recommended_format>

<alternative_format>
<overview>
Use author-year system when presentation style requires narrative citations.
</overview>

<in_text_citations>
```markdown
George et al. (2010) demonstrated efficacy in treatment-resistant depression.

Response rates vary (Fitzgerald et al., 2006; Lefaucheur et al., 2020).
```
</in_text_citations>

<reference_list_format>
```
George, M.S., Lisanby, S.H., Avery, D., et al. (2010). Daily left prefrontal transcranial magnetic stimulation therapy for major depressive disorder. Archives of General Psychiatry, 67(5), 507-516.
```
</reference_list_format>
</alternative_format>

<citation_styles_by_context>
<clinical_education>
**Use**: Numbered system
**Placement**: Footer or slide bottom
**Detail level**: Author et al., Journal abbreviation, Year

```markdown
---
# Treatment Response Rates

- First-line: 45-60% response[1]
- Treatment-resistant: 30-40% response[2,3]

<div style="font-size: 16px; margin-top: 50px;">

1. George et al. Arch Gen Psychiatry. 2010
2. O'Reardon et al. Biol Psychiatry. 2007
3. Carpenter et al. Depress Anxiety. 2012

</div>
---
```
</clinical_education>

<research_seminars>
**Use**: Author-year or numbered
**Placement**: Inline or footer
**Detail level**: Full citation
</research_seminars>

<literature_reviews>
**Use**: Numbered with full details
**Placement**: Dedicated reference slides
**Detail level**: Complete citation with PMID/DOI
</literature_reviews>
</citation_styles_by_context>

<pubmed_citation_extraction>
**Standard format**:
```
LastName InitialInitial, LastName InitialInitial. Title. Journal. Year Mon;Volume(Issue):Pages. PMID: ########
```

**Example extraction**:
```
PMID: 20439832
Title: Daily left prefrontal transcranial magnetic stimulation...
Authors: George MS, Lisanby SH, Avery D, et al.
Journal: Arch Gen Psychiatry
Date: 2010 May;67(5):507-16

Formatted:
George MS, Lisanby SH, Avery D, et al. Daily left prefrontal transcranial magnetic stimulation therapy for major depressive disorder: a sham-controlled randomized trial. Arch Gen Psychiatry. 2010;67(5):507-516. PMID: 20439832
```
</pubmed_citation_extraction>

<citation_management>
<footer_citations>
```markdown
---
footer: 'Smith et al. 2023 | Jones et al. 2022'
---
```
</footer_citations>

<inline_citations>
Bottom of slide:

```markdown
---
# Slide Title

Content here

<div style="font-size: 14px; position: absolute; bottom: 20px;">

**References**: 1. Smith et al. Nature 2023. 2. Jones et al. Science 2022.

</div>
---
```
</inline_citations>

<dedicated_reference_slides>
Place at end of presentation:

```markdown
---
# References

<div style="font-size: 16px; column-count: 2;">

1. Author1 et al. Journal1. 2023;vol:pages.
2. Author2 et al. Journal2. 2022;vol:pages.
3. Author3 et al. Journal3. 2021;vol:pages.
4. Author4 et al. Journal4. 2020;vol:pages.
[... continue ...]

</div>
---
```
</dedicated_reference_slides>
</citation_management>

<image_citations>
<figures_from_publications>
```markdown
![w:600px](image.png)

<div style="font-size: 14px; text-align: center;">

**Figure 3**. Electric field distribution by TMS coil type.
*Adapted from* Deng et al. Brain Stimulation. 2013;6(1):1-13.

</div>
```
</figures_from_publications>

<original_figures>
```markdown
![w:600px](custom_diagram.png)

<div style="font-size: 14px; text-align: center;">

**Figure**. Mechanism of action pathway. Created based on data from Smith et al. 2023[1] and Jones et al. 2022.[2]

</div>
```
</original_figures>
</image_citations>

<journal_abbreviations>
| Full Name | Abbreviation |
|-----------|-------------|
| Archives of General Psychiatry | Arch Gen Psychiatry |
| Biological Psychiatry | Biol Psychiatry |
| Brain Stimulation | Brain Stimul |
| Clinical Neurophysiology | Clin Neurophysiol |
| Journal of Clinical Psychiatry | J Clin Psychiatry |
| Nature Neuroscience | Nat Neurosci |
| NeuroImage | Neuroimage |
| Proceedings of the National Academy of Sciences | Proc Natl Acad Sci USA |
| The Journal of Neuroscience | J Neurosci |
</journal_abbreviations>

<marp_formatting_tips>
<superscript_citations>
```markdown
Treatment shows efficacy<sup>1,2</sup> with minimal side effects<sup>3</sup>.
```
</superscript_citations>

<compact_reference_list>
```markdown
<div style="font-size: 12px; line-height: 1.2;">

References: [1] Author1 2023 [2] Author2 2022 [3] Author3 2021

</div>
```
</compact_reference_list>

<color_coded_citations>
```markdown
<span style="color: #0066cc;">[1]</span>
```
</color_coded_citations>
</marp_formatting_tips>

<best_practices>
1. ✅ **Be consistent**: Choose one format and stick to it
2. ✅ **Cite primary sources**: Original research > review articles when possible
3. ✅ **Include PMID**: Makes verification easy
4. ✅ **Limit per slide**: 3-5 citations max per slide for readability
5. ✅ **Group related citations**: [1-3] instead of [1],[2],[3]
6. ✅ **Verify accuracy**: Double-check author names, years, journals
7. ✅ **Use et al. appropriately**: After 3rd author
8. ✅ **Keep reference slide readable**: Font ≥14pt
</best_practices>

<common_errors>
❌ Missing journal name
❌ Incorrect year
❌ Incomplete author list without "et al."
❌ Missing PMID or DOI
❌ Inconsistent format across slides
❌ Citations too small to read
❌ No citation for reproduced figures
❌ Outdated references when recent data available
</common_errors>
