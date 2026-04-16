---
name: convert-knowledge-to-xml
description: Parse and convert knowledge bases (.md, .txt, text files) into structured XML documents with intelligent content synthesis. Use when converting documentation, presentations, journal articles, or mixed text files into hierarchical XML, or when the user needs to organize knowledge into structured data.
---

<objective>
Transform unstructured or semi-structured text files into logically organized XML documents. This skill detects document types, synthesizes related content, and produces hierarchical XML that preserves semantic meaning while improving organization.
</objective>

<quick_start>
<basic_workflow>
1. **Analyze input files**: Read all source files and detect their document type
2. **Extract semantic structure**: Identify headings, sections, key concepts
3. **Synthesize content**: Merge related sections, deduplicate, organize hierarchically
4. **Generate XML**: Output well-formed XML with appropriate schema

```python
# Basic conversion pattern
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom

def convert_to_xml(input_path: str, output_path: str):
    """Convert text files to structured XML."""
    files = gather_files(input_path)
    doc_type = detect_document_type(files)
    structure = extract_structure(files, doc_type)
    synthesized = synthesize_content(structure)
    xml_output = generate_xml(synthesized, doc_type)
    write_xml(xml_output, output_path)
```
</basic_workflow>

<supported_formats>
- **Markdown** (.md): Parses headings, lists, code blocks, links
- **Plain text** (.txt): Detects implicit structure via whitespace and patterns
- **reStructuredText** (.rst): Handles directives and section markers
- **Other text**: Analyzes patterns to infer structure
</supported_formats>
</quick_start>

<document_type_detection>
<presentation_patterns>
Indicators that content is a presentation:
- Sequential "Slide X" or numbered sections
- Short bullet points with minimal prose
- Repeated header patterns
- Title + bullets structure

Synthesis strategy: **Merge slides by topic**, combine related bullet points, create hierarchical topic structure.
</presentation_patterns>

<journal_article_patterns>
Indicators that content is a journal article:
- IMRaD structure (Introduction, Methods, Results, Discussion)
- Abstract at beginning
- References/Bibliography section
- Academic language patterns, citations

Synthesis strategy: **Map to standard sections** (abstract, introduction, methods, results, discussion, conclusions, references).
</journal_article_patterns>

<documentation_patterns>
Indicators that content is technical documentation:
- API references, code examples
- Installation/setup sections
- Hierarchical heading structure
- Cross-references between sections

Synthesis strategy: **Preserve hierarchy**, group by functional area, link related concepts.
</documentation_patterns>

<mixed_content_patterns>
When document type is unclear:
- Analyze heading frequency and depth
- Check for consistent structural markers
- Default to hierarchical organization by topic
- Preserve original section boundaries when uncertain
</mixed_content_patterns>
</document_type_detection>

<xml_schema_templates>
<presentation_schema>
```xml
<?xml version="1.0" encoding="UTF-8"?>
<knowledge-base type="presentation" source="{source_files}">
  <metadata>
    <title>{extracted_title}</title>
    <topics>{topic_list}</topics>
    <created>{timestamp}</created>
  </metadata>
  <content>
    <topic id="topic-1" name="{topic_name}">
      <summary>{synthesized_summary}</summary>
      <points>
        <point importance="high">{merged_point}</point>
        <point importance="medium">{merged_point}</point>
      </points>
      <sources>
        <source file="{filename}" slide="{slide_num}"/>
      </sources>
    </topic>
  </content>
</knowledge-base>
```
</presentation_schema>

<journal_article_schema>
```xml
<?xml version="1.0" encoding="UTF-8"?>
<knowledge-base type="journal-article" source="{source_files}">
  <metadata>
    <title>{title}</title>
    <authors>{authors}</authors>
    <date>{publication_date}</date>
    <doi>{doi_if_present}</doi>
  </metadata>
  <content>
    <abstract>{abstract_text}</abstract>
    <introduction>
      <background>{background}</background>
      <objectives>{objectives}</objectives>
    </introduction>
    <methods>
      <design>{study_design}</design>
      <procedures>{procedures}</procedures>
    </methods>
    <results>
      <finding id="f1">{key_finding}</finding>
    </results>
    <discussion>
      <interpretation>{interpretation}</interpretation>
      <limitations>{limitations}</limitations>
    </discussion>
    <conclusions>{conclusions}</conclusions>
    <references>
      <reference id="ref1">{citation}</reference>
    </references>
  </content>
</knowledge-base>
```
</journal_article_schema>

<documentation_schema>
```xml
<?xml version="1.0" encoding="UTF-8"?>
<knowledge-base type="documentation" source="{source_files}">
  <metadata>
    <title>{title}</title>
    <version>{version}</version>
    <created>{timestamp}</created>
  </metadata>
  <content>
    <section id="sec-1" name="{section_name}">
      <description>{section_description}</description>
      <subsections>
        <subsection id="sub-1" name="{subsection_name}">
          <content>{content}</content>
          <code-examples>
            <example language="{lang}">{code}</example>
          </code-examples>
        </subsection>
      </subsections>
    </section>
  </content>
  <index>
    <term name="{term}" refs="sec-1,sub-1"/>
  </index>
</knowledge-base>
```
</documentation_schema>

<generic_schema>
```xml
<?xml version="1.0" encoding="UTF-8"?>
<knowledge-base type="generic" source="{source_files}">
  <metadata>
    <title>{inferred_title}</title>
    <created>{timestamp}</created>
  </metadata>
  <content>
    <section id="sec-{n}" level="{depth}">
      <heading>{heading}</heading>
      <body>{content}</body>
      <children>
        <!-- nested sections -->
      </children>
    </section>
  </content>
</knowledge-base>
```
</generic_schema>
</xml_schema_templates>

<synthesis_algorithms>
<topic_clustering>
For presentations and mixed content:

1. Extract all headings/titles
2. Compute semantic similarity (using word overlap, TF-IDF, or embeddings)
3. Cluster related sections
4. Merge content within clusters
5. Generate synthesized summaries

```python
def cluster_by_topic(sections: list) -> dict:
    """Group sections by semantic similarity."""
    from collections import defaultdict

    # Extract keywords from each section
    keywords = {s['id']: extract_keywords(s['content']) for s in sections}

    # Build similarity matrix
    clusters = defaultdict(list)
    for section in sections:
        topic = find_best_matching_topic(section, keywords)
        clusters[topic].append(section)

    return dict(clusters)

def synthesize_cluster(sections: list) -> dict:
    """Merge related sections into coherent content."""
    # Deduplicate similar points
    unique_points = deduplicate(extract_all_points(sections))
    # Order by importance/frequency
    ranked_points = rank_by_importance(unique_points)
    # Generate summary
    summary = generate_summary(ranked_points)

    return {
        'summary': summary,
        'points': ranked_points,
        'sources': [s['source'] for s in sections]
    }
```
</topic_clustering>

<imrad_extraction>
For journal articles:

```python
def extract_imrad_structure(content: str) -> dict:
    """Extract IMRaD structure from article text."""
    sections = {
        'abstract': extract_section(content, ['abstract', 'summary']),
        'introduction': extract_section(content, ['introduction', 'background']),
        'methods': extract_section(content, ['methods', 'methodology', 'materials']),
        'results': extract_section(content, ['results', 'findings']),
        'discussion': extract_section(content, ['discussion', 'interpretation']),
        'conclusions': extract_section(content, ['conclusion', 'conclusions']),
        'references': extract_references(content)
    }
    return sections

def clarify_section(section_name: str, content: str) -> dict:
    """Break section into semantic sub-components."""
    if section_name == 'introduction':
        return {
            'background': extract_background(content),
            'objectives': extract_objectives(content),
            'hypotheses': extract_hypotheses(content)
        }
    elif section_name == 'methods':
        return {
            'design': extract_study_design(content),
            'participants': extract_participants(content),
            'procedures': extract_procedures(content),
            'analysis': extract_analysis_methods(content)
        }
    # ... similar for other sections
```
</imrad_extraction>

<hierarchy_building>
For documentation and generic content:

```python
def build_hierarchy(content: str) -> ET.Element:
    """Build XML hierarchy from heading structure."""
    root = ET.Element('content')
    stack = [(root, 0)]  # (element, depth)

    for line in content.split('\n'):
        heading_match = detect_heading(line)
        if heading_match:
            level = heading_match['level']
            text = heading_match['text']

            # Pop stack to find parent
            while stack and stack[-1][1] >= level:
                stack.pop()

            parent = stack[-1][0]
            section = ET.SubElement(parent, 'section')
            section.set('id', generate_id(text))
            section.set('level', str(level))

            heading_elem = ET.SubElement(section, 'heading')
            heading_elem.text = text

            stack.append((section, level))
        else:
            # Add content to current section
            current = stack[-1][0]
            body = current.find('body')
            if body is None:
                body = ET.SubElement(current, 'body')
            body.text = (body.text or '') + line + '\n'

    return root
```
</hierarchy_building>
</synthesis_algorithms>

<workflow>
<step_1>
**Gather and analyze files**

```python
from pathlib import Path

def gather_files(input_path: str, extensions: list = None) -> list:
    """Collect all text files from path."""
    if extensions is None:
        extensions = ['.md', '.txt', '.rst', '.text']

    path = Path(input_path)
    files = []

    if path.is_file():
        files.append(path)
    else:
        for ext in extensions:
            files.extend(path.rglob(f'*{ext}'))

    return sorted(files, key=lambda f: f.name)

def read_file_content(file_path: Path) -> dict:
    """Read file with metadata."""
    content = file_path.read_text(encoding='utf-8')
    return {
        'path': str(file_path),
        'name': file_path.name,
        'content': content,
        'extension': file_path.suffix
    }
```
</step_1>

<step_2>
**Detect document type**

```python
def detect_document_type(files: list) -> str:
    """Analyze files to determine document type."""
    combined_content = '\n'.join(f['content'] for f in files)

    # Check for presentation patterns
    if is_presentation(combined_content):
        return 'presentation'

    # Check for journal article patterns
    if is_journal_article(combined_content):
        return 'journal-article'

    # Check for documentation patterns
    if is_documentation(combined_content):
        return 'documentation'

    return 'generic'

def is_presentation(content: str) -> bool:
    """Check for presentation indicators."""
    patterns = [
        r'slide\s*\d+',
        r'^#{1,2}\s+\d+\.',  # Numbered slides
        r'^\s*[-*]\s+',  # Heavy bullet usage
    ]
    # Count matches, threshold for classification
    ...

def is_journal_article(content: str) -> bool:
    """Check for IMRaD structure."""
    required_sections = ['abstract', 'introduction', 'method', 'result', 'discussion']
    found = sum(1 for s in required_sections if s in content.lower())
    return found >= 3
```
</step_2>

<step_3>
**Extract and synthesize**

Apply appropriate synthesis algorithm based on document type:
- Presentations: Topic clustering + point merging
- Journal articles: IMRaD extraction + section clarification
- Documentation: Hierarchy building + cross-referencing
- Generic: Hierarchical organization by headings
</step_3>

<step_4>
**Generate XML output**

```python
def generate_xml(structure: dict, doc_type: str) -> str:
    """Generate well-formed XML from structure."""
    root = ET.Element('knowledge-base')
    root.set('type', doc_type)
    root.set('source', structure.get('source', 'unknown'))

    # Add metadata
    metadata = ET.SubElement(root, 'metadata')
    for key, value in structure.get('metadata', {}).items():
        elem = ET.SubElement(metadata, key)
        elem.text = str(value)

    # Add content based on doc_type
    content = ET.SubElement(root, 'content')
    populate_content(content, structure['content'], doc_type)

    # Pretty print
    return prettify_xml(root)

def prettify_xml(elem: ET.Element) -> str:
    """Return pretty-printed XML string."""
    rough = ET.tostring(elem, encoding='unicode')
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent='  ')

def write_xml(xml_string: str, output_path: str):
    """Write XML to file."""
    Path(output_path).write_text(xml_string, encoding='utf-8')
```
</step_4>
</workflow>

<advanced_features>
**Custom schemas**: See [references/custom-schemas.md](references/custom-schemas.md) for defining project-specific XML structures.

**Batch processing**: See [references/batch-processing.md](references/batch-processing.md) for handling large knowledge bases.

**Semantic analysis**: For deeper content synthesis, integrate with NLP libraries or LLM APIs for:
- Key phrase extraction
- Automatic summarization
- Entity recognition
- Relationship mapping
</advanced_features>

<validation>
<xml_validation>
```python
from lxml import etree

def validate_xml(xml_string: str, schema_path: str = None) -> bool:
    """Validate XML structure and optionally against XSD schema."""
    try:
        doc = etree.fromstring(xml_string.encode())

        if schema_path:
            with open(schema_path, 'r') as f:
                schema_doc = etree.parse(f)
            schema = etree.XMLSchema(schema_doc)
            schema.assertValid(doc)

        return True
    except etree.XMLSyntaxError as e:
        print(f"XML syntax error: {e}")
        return False
    except etree.DocumentInvalid as e:
        print(f"Schema validation error: {e}")
        return False
```
</xml_validation>

<content_validation>
- Verify all source files are represented in output
- Check that hierarchy depth matches source structure
- Validate cross-references resolve correctly
- Ensure no content loss during synthesis
</content_validation>
</validation>

<success_criteria>
- **Valid XML**: Output passes XML syntax validation
- **Complete coverage**: All source content represented in output
- **Correct type detection**: Document type matches source characteristics
- **Logical hierarchy**: Structure reflects semantic organization
- **Meaningful synthesis**: Related content merged, not just concatenated
- **Preserved semantics**: Key information retained after synthesis
</success_criteria>

<anti_patterns>
- **Flat dumping**: Converting without structure analysis
- **Over-synthesis**: Losing important distinctions between related content
- **Type misclassification**: Applying wrong schema to content
- **Broken hierarchy**: Inconsistent nesting levels
- **Silent data loss**: Dropping content without indication
</anti_patterns>
