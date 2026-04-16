<custom_schemas>
<objective>
Define project-specific XML schemas for specialized knowledge base structures beyond the built-in templates.
</objective>

<creating_custom_schema>
<step_1>
**Define your document structure**

Identify the key elements your knowledge base needs:
- What metadata is essential?
- What content sections exist?
- How do sections relate to each other?
- What attributes describe elements?
</step_1>

<step_2>
**Create XSD schema file**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <!-- Root element -->
  <xs:element name="knowledge-base">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="metadata" type="MetadataType"/>
        <xs:element name="content" type="ContentType"/>
      </xs:sequence>
      <xs:attribute name="type" type="xs:string" use="required"/>
      <xs:attribute name="version" type="xs:string" default="1.0"/>
    </xs:complexType>
  </xs:element>

  <!-- Metadata type -->
  <xs:complexType name="MetadataType">
    <xs:sequence>
      <xs:element name="title" type="xs:string"/>
      <xs:element name="created" type="xs:dateTime"/>
      <xs:any minOccurs="0" maxOccurs="unbounded" processContents="lax"/>
    </xs:sequence>
  </xs:complexType>

  <!-- Content type - customize for your needs -->
  <xs:complexType name="ContentType">
    <xs:sequence>
      <xs:element name="section" type="SectionType" maxOccurs="unbounded"/>
    </xs:sequence>
  </xs:complexType>

  <!-- Section type -->
  <xs:complexType name="SectionType">
    <xs:sequence>
      <xs:element name="heading" type="xs:string"/>
      <xs:element name="body" type="xs:string" minOccurs="0"/>
      <xs:element name="section" type="SectionType" minOccurs="0" maxOccurs="unbounded"/>
    </xs:sequence>
    <xs:attribute name="id" type="xs:ID" use="required"/>
    <xs:attribute name="level" type="xs:integer"/>
  </xs:complexType>

</xs:schema>
```
</step_2>

<step_3>
**Implement schema-specific generator**

```python
def generate_custom_xml(structure: dict, schema_config: dict) -> ET.Element:
    """Generate XML based on custom schema configuration."""
    root = ET.Element(schema_config['root_element'])

    for attr, value in schema_config.get('root_attributes', {}).items():
        root.set(attr, value)

    # Build according to schema structure
    for element_config in schema_config['elements']:
        build_element(root, structure, element_config)

    return root

def build_element(parent: ET.Element, data: dict, config: dict):
    """Recursively build elements from config."""
    tag = config['tag']
    source_key = config.get('source', tag)

    if source_key not in data:
        if config.get('required', False):
            raise ValueError(f"Missing required field: {source_key}")
        return

    elem = ET.SubElement(parent, tag)

    # Set attributes
    for attr_config in config.get('attributes', []):
        attr_name = attr_config['name']
        attr_source = attr_config.get('source', attr_name)
        if attr_source in data:
            elem.set(attr_name, str(data[attr_source]))

    # Set content or children
    if 'children' in config:
        for child_config in config['children']:
            build_element(elem, data.get(source_key, {}), child_config)
    else:
        elem.text = str(data[source_key])
```
</step_3>
</creating_custom_schema>

<schema_examples>
<meeting_notes_schema>
```xml
<?xml version="1.0" encoding="UTF-8"?>
<knowledge-base type="meeting-notes">
  <metadata>
    <title>Weekly Team Sync</title>
    <date>2024-01-15</date>
    <attendees>
      <attendee role="facilitator">Alice</attendee>
      <attendee>Bob</attendee>
    </attendees>
  </metadata>
  <content>
    <agenda-item id="ai-1" status="discussed">
      <topic>Q1 Planning</topic>
      <discussion>{summary}</discussion>
      <decisions>
        <decision owner="Alice" due="2024-01-20">{decision}</decision>
      </decisions>
      <action-items>
        <action owner="Bob" priority="high">{action}</action>
      </action-items>
    </agenda-item>
  </content>
</knowledge-base>
```
</meeting_notes_schema>

<code_review_schema>
```xml
<?xml version="1.0" encoding="UTF-8"?>
<knowledge-base type="code-review">
  <metadata>
    <repository>{repo}</repository>
    <pull-request>{pr_number}</pull-request>
    <reviewer>{reviewer}</reviewer>
  </metadata>
  <content>
    <file path="{file_path}">
      <comment line="{line}" severity="warning">
        <issue>{issue_description}</issue>
        <suggestion>{suggestion}</suggestion>
      </comment>
    </file>
    <summary>
      <approved>{true/false}</approved>
      <blocking-issues>{count}</blocking-issues>
    </summary>
  </content>
</knowledge-base>
```
</code_review_schema>

<research_notes_schema>
```xml
<?xml version="1.0" encoding="UTF-8"?>
<knowledge-base type="research-notes">
  <metadata>
    <project>{project_name}</project>
    <researcher>{name}</researcher>
    <date-range from="{start}" to="{end}"/>
  </metadata>
  <content>
    <hypothesis id="h1">
      <statement>{hypothesis}</statement>
      <evidence>
        <observation date="{date}" source="{source}">
          {observation}
        </observation>
      </evidence>
      <status>{confirmed/refuted/pending}</status>
    </hypothesis>
    <insights>
      <insight relates-to="h1" confidence="high">
        {insight_text}
      </insight>
    </insights>
  </content>
</knowledge-base>
```
</research_notes_schema>
</schema_examples>

<schema_configuration_file>
Create a JSON configuration to define custom schemas programmatically:

```json
{
  "schema_name": "project-requirements",
  "root_element": "knowledge-base",
  "root_attributes": {
    "type": "requirements",
    "version": "1.0"
  },
  "elements": [
    {
      "tag": "metadata",
      "children": [
        {"tag": "title", "source": "project_name", "required": true},
        {"tag": "version", "source": "version"},
        {"tag": "stakeholders", "source": "stakeholders", "is_list": true}
      ]
    },
    {
      "tag": "content",
      "children": [
        {
          "tag": "requirement",
          "source": "requirements",
          "is_list": true,
          "attributes": [
            {"name": "id", "source": "req_id"},
            {"name": "priority", "source": "priority"}
          ],
          "children": [
            {"tag": "description", "source": "description"},
            {"tag": "acceptance-criteria", "source": "criteria"}
          ]
        }
      ]
    }
  ]
}
```
</schema_configuration_file>

<validation_with_custom_schema>
```python
def validate_against_custom_schema(xml_string: str, schema_path: str) -> tuple:
    """Validate XML against custom XSD schema."""
    from lxml import etree

    errors = []

    try:
        doc = etree.fromstring(xml_string.encode())

        with open(schema_path, 'r') as f:
            schema_doc = etree.parse(f)
        schema = etree.XMLSchema(schema_doc)

        if not schema.validate(doc):
            for error in schema.error_log:
                errors.append({
                    'line': error.line,
                    'message': error.message,
                    'type': error.type_name
                })

        return len(errors) == 0, errors

    except Exception as e:
        return False, [{'message': str(e)}]
```
</validation_with_custom_schema>
</custom_schemas>
