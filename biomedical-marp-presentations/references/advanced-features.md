# Advanced MARP Features

## Overview

This guide covers advanced MARP (Markdown Presentation Ecosystem) features beyond basic slides. These features enable sophisticated layouts, visual effects, and presentation enhancements.

## Custom Slide Classes

MARP provides built-in slide classes that modify slide appearance and behavior.

### Lead Class

Centers content and increases text size for emphasis.

**Syntax**:
```markdown
<!-- _class: lead -->

# Big Centered Message

Perfect for section dividers or key takeaways
```

**Use cases**:
- Section transitions
- Key conclusions
- Dramatic reveals
- Question slides

**Example**:
```markdown
<!-- _class: lead -->

# Question

What is the mechanism of rapid antidepressant action?
```

### Invert Class

Inverts slide colors (background ↔ foreground).

**Syntax**:
```markdown
<!-- _class: invert -->

# Dark Slide

White text on dark background
```

**Use cases**:
- Visual variety
- Emphasizing specific slides
- Dark theme compatibility
- Eye rest in bright rooms

**Example**:
```markdown
<!-- _class: invert -->

# Clinical Pearl

Always check for contraindications before TMS treatment
```

### Explanatory Class

Custom class for detailed content slides (defined in skill themes).

**Syntax**:
```markdown
<!-- _class: explanatory -->

# Deep Dive: NMDA Receptor Function

[Detailed paragraphs explaining complex mechanism...]
```

**Use cases**:
- Complex mechanisms
- Detailed pathophysiology
- In-depth literature review
- Technical deep dives

**Characteristics**:
- Allows 1-2 paragraphs (150-250 words)
- Smaller font for more text
- Still includes visuals
- Has key takeaway box

### Combining Classes

Multiple classes can be combined:

```markdown
<!-- _class: lead invert -->

# Centered Dark Slide

Combines lead and invert effects
```

## Background Images

MARP supports various background image configurations.

### Full Background

```markdown
![bg](image.jpg)

# Slide Title

Text appears over the background image
```

**Best for**:
- Title slides with contextual imagery
- Section dividers
- Emotional impact

**Tips**:
- Use semi-transparent overlays for text readability
- Choose images with clear areas for text
- Avoid busy backgrounds

### Background Fitting Options

**Fit to slide**:
```markdown
![bg fit](image.jpg)
```
Scales image to fit without cropping.

**Cover (default)**:
```markdown
![bg](image.jpg)
```
Fills entire slide, may crop edges.

**Contain**:
```markdown
![bg contain](image.jpg)
```
Shows entire image with possible borders.

### Positioned Backgrounds

**Left half**:
```markdown
![bg left](image.jpg)

# Content on Right

Text appears on right side
```

**Right half**:
```markdown
![bg right](image.jpg)

# Content on Left

Text appears on left side
```

**Custom width**:
```markdown
![bg right:40%](image.jpg)

Image takes 40% of width on right
```

### Multiple Backgrounds

Stack multiple background images:

```markdown
![bg](background.jpg)
![bg opacity:.3](overlay.png)

# Layered Backgrounds
```

**Use opacity to blend**:
```markdown
![bg brightness:.5](dark-image.jpg)
![bg opacity:.7](pattern.png)
```

### Background Filters

Apply CSS filters to backgrounds:

```markdown
<!-- Darken for text readability -->
![bg brightness:.4](image.jpg)

<!-- Blur for subtle effect -->
![bg blur:3px](image.jpg)

<!-- Grayscale for professional look -->
![bg grayscale:1](image.jpg)

<!-- Sepia for vintage feel -->
![bg sepia:.8](image.jpg)
```

## Speaker Notes

Add notes visible only to presenter.

**Syntax**:
```markdown
# Slide Title

Content visible to audience

<!--
These are speaker notes
- Remind myself to emphasize X
- Mention upcoming study
- Timing: 2 minutes on this slide
-->
```

**Best practices**:
- Keep notes concise
- Include timing estimates
- Add emphasis reminders
- Note transitions

**Example**:
```markdown
# TMS Efficacy Data

Meta-analysis shows response rate of 50-60%<sup>1</sup>

<!--
SPEAKER NOTES:
- Emphasize this is for rTMS, not single-session
- Mention FDA approval in 2008
- Compare to 30% for resistant depression with meds alone
- Timing: 3 minutes
- Transition: "Now let's look at the mechanism..."
-->
```

## Pagination and Footers

### Page Numbers

Enable pagination in frontmatter:

```yaml
---
marp: true
paginate: true
---
```

**Skip pagination on specific slides**:
```markdown
<!-- _paginate: false -->

# Title Slide

No page number on this slide
```

### Custom Footers

**Global footer** (all slides):
```yaml
---
marp: true
footer: 'Author Name | Institution | Date'
---
```

**Per-slide footer**:
```markdown
<!-- _footer: 'Special footer for this slide' -->

# Slide Title
```

**Remove footer on specific slide**:
```markdown
<!-- _footer: '' -->

# Clean Slide
```

### Footer Formatting

Footers support markdown:

```yaml
---
footer: '**TMS Overview** | *Dr. Smith* | January 2025'
---
```

## Advanced Layouts

### Multi-Column Layouts

**Two columns**:
```markdown
<div class="columns">
<div>

## Left Column

Content here

</div>
<div>

## Right Column

Content here

</div>
</div>
```

**Three columns**:
```markdown
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
<div>

Column 1

</div>
<div>

Column 2

</div>
<div>

Column 3

</div>
</div>
```

**Asymmetric columns** (1/3 + 2/3):
```markdown
<div style="display: grid; grid-template-columns: 1fr 2fr; gap: 20px;">
<div>

Narrow column

</div>
<div>

Wide column

</div>
</div>
```

### Grid Layouts

**2x2 image grid**:
```markdown
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">

![w:400px](image1.jpg)
![w:400px](image2.jpg)
![w:400px](image3.jpg)
![w:400px](image4.jpg)

</div>
```

**Gallery layout**:
```markdown
<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">

![h:200px](image1.jpg)
![h:200px](image2.jpg)
![h:200px](image3.jpg)

</div>
```

## Advanced Image Techniques

### Image Size Control

**Width control**:
```markdown
![w:600px](image.jpg)   # 600 pixels wide
![w:80%](image.jpg)     # 80% of slide width
```

**Height control**:
```markdown
![h:400px](image.jpg)   # 400 pixels tall
![h:60%](image.jpg)     # 60% of slide height
```

**Both dimensions**:
```markdown
![w:600px h:400px](image.jpg)
```

### Image Positioning

**Floating right**:
```markdown
<img src="image.jpg" alt="Description" style="float: right; width: 400px; margin-left: 20px;">

Text wraps around the image on the left side...
```

**Centered**:
```markdown
<div style="text-align: center;">

![w:600px](image.jpg)

</div>
```

**Side by side**:
```markdown
<div style="display: flex; gap: 20px; justify-content: center;">

![w:400px](image1.jpg)
![w:400px](image2.jpg)

</div>
```

### Image with Caption Box

```markdown
<figure style="text-align: center;">

![w:600px](brain-scan.jpg)

<figcaption style="font-size: 16px; color: #666; margin-top: 10px; padding: 10px; background: #f5f5f5; border-left: 4px solid #2C5F8D;">

**Figure 1**. DLPFC activation during TMS stimulation.
*Source*: Smith et al. Nature Neuroscience. 2024.<sup>1</sup>

</figcaption>
</figure>
```

## Slide Transitions and Animations

MARP has limited animation support, but you can use CSS:

### Fade In Effect

```markdown
<div style="animation: fadein 2s;">

# Content Fades In

</div>

<style>
@keyframes fadein {
    from { opacity: 0; }
    to { opacity: 1; }
}
</style>
```

### Slide-In Effect

```markdown
<div style="animation: slidein 1s;">

Content slides in from left

</div>

<style>
@keyframes slidein {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}
</style>
```

**Note**: Use animations sparingly in scientific presentations. They can distract from content.

## Scoped Styles

Apply custom CSS to specific slides:

**Slide-specific style**:
```markdown
<!-- _class: custom-slide -->

# Special Slide

<style scoped>
.custom-slide {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}
</style>
```

**All slides in section**:
```markdown
<style>
section {
    font-size: 28px;
}
</style>
```

## HTML and CSS Integration

### Custom Boxes

**Highlight box**:
```markdown
<div style="background: #FFF3CD; padding: 20px; border-left: 5px solid #FFA500; margin: 20px 0;">

⚠️ **Important**: Always check contraindications before TMS treatment

</div>
```

**Key takeaway box**:
```markdown
<div style="background: #D1ECF1; padding: 20px; border-radius: 8px; border: 2px solid #0C5460;">

💡 **Key Takeaway**: TMS demonstrates significant efficacy for treatment-resistant depression

</div>
```

**Clinical pearl box**:
```markdown
<div style="background: #E7F3E7; padding: 20px; border-left: 5px solid #28A745;">

🔬 **Clinical Pearl**: Response typically emerges after 10-15 sessions

</div>
```

### Progressive Disclosure

Reveal content in stages (requires presenter mode):

```markdown
# Main Point

<div>

First point (always visible)

</div>

<!-- _class: fragment -->

Second point (revealed on click)

<!-- _class: fragment -->

Third point (revealed on second click)
```

**Note**: Fragment support varies by MARP engine. Test with your rendering tool.

## Mathematical Equations

MARP supports LaTeX math via KaTeX:

**Inline math**:
```markdown
The formula $E = mc^2$ shows energy-mass equivalence
```

**Display math**:
```markdown
$$
\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

**Biomedical example**:
```markdown
$$
\text{Response Rate} = \frac{\text{Responders}}{\text{Total Treated}} \times 100\%
$$
```

## Code Highlighting

Syntax highlighting for code examples:

**Python**:
````markdown
```python
def calculate_response_rate(responders, total):
    return (responders / total) * 100
```
````

**R (for statistics)**:
````markdown
```r
# Calculate effect size
cohens_d <- (mean1 - mean2) / pooled_sd
```
````

**With line numbers**:
````markdown
```python {.line-numbers}
1 | def analyze_results(data):
2 |     response_rate = calculate_rate(data)
3 |     return response_rate
```
````

## Tables

### Basic Table

```markdown
| Coil Type | Penetration Depth | Focality | Clinical Use |
|-----------|-------------------|----------|--------------|
| Figure-8  | 1.5-2 cm         | High     | Depression   |
| H-coil    | >6 cm            | Low      | Deep targets |
| Circular  | 3-4 cm           | Medium   | Motor cortex |
```

### Styled Table

```markdown
<table style="width: 100%; border-collapse: collapse;">
<thead style="background: #2C5F8D; color: white;">
<tr>
<th style="padding: 12px;">Parameter</th>
<th style="padding: 12px;">rTMS</th>
<th style="padding: 12px;">Theta-Burst</th>
</tr>
</thead>
<tbody>
<tr style="background: #f9f9f9;">
<td style="padding: 10px;">Duration</td>
<td style="padding: 10px;">30-40 min</td>
<td style="padding: 10px;">3-10 min</td>
</tr>
<tr>
<td style="padding: 10px;">Sessions</td>
<td style="padding: 10px;">25-30</td>
<td style="padding: 10px;">10-20</td>
</tr>
</tbody>
</table>
```

### Comparison Table

```markdown
| Feature | Traditional Review | Meta-Analysis |
|---------|-------------------|---------------|
| Evidence Level | ⭐⭐ | ⭐⭐⭐⭐ |
| Statistical Power | Low | High |
| Bias Risk | High | Moderate |
| Time Required | Days | Weeks |
```

## Icons and Symbols

Enhance slides with Unicode symbols:

**Clinical**:
```markdown
✅ Approved
❌ Contraindicated
⚠️ Caution Required
🔬 Research Evidence
💊 Pharmacological
🧠 Neurological
⚡ Electrical Stimulation
📊 Statistical Significance
```

**Status indicators**:
```markdown
✓ Completed
➜ In Progress
○ Planned
★ Important
```

## Slide Size and Aspect Ratio

Configure in frontmatter:

```yaml
---
# 16:9 (default, recommended for modern displays)
size: 16:9

# 4:3 (classic, better for older projectors)
size: 4:3

# Custom dimensions
size: 1280x720
---
```

## Export Options

### PDF Export

Via MARP CLI:
```bash
marp presentation.md --pdf --allow-local-files
```

### HTML Export

```bash
marp presentation.md --html --allow-local-files
```

### PowerPoint Export

```bash
marp presentation.md --pptx --allow-local-files
```

**Note**: PowerPoint export has limited support for custom HTML/CSS.

## Best Practices for Advanced Features

### 1. Performance

- **Minimize animations**: Slow rendering on some systems
- **Optimize images**: Large images slow rendering
- **Limit custom CSS**: Can cause inconsistencies
- **Test rendering**: Preview before presenting

### 2. Compatibility

- **Test on target system**: Features vary by MARP engine
- **Provide fallbacks**: Not all features work in all renderers
- **Use standard features first**: Advanced features when needed
- **Check PDF export**: Some features lost in PDF

### 3. Accessibility

- **Color contrast**: Ensure text readability
- **Alt text**: Include for all images
- **Font size**: Minimum 20pt for body text
- **Clear structure**: Logical heading hierarchy

### 4. Scientific Presentations

- **Subtle effects**: Avoid flashy animations
- **Professional appearance**: Use advanced features to enhance, not distract
- **Data focus**: Let content shine, not effects
- **Consistency**: Apply advanced features uniformly

## Summary

Advanced MARP features enable:
- **Custom layouts** with columns and grids
- **Visual variety** with backgrounds and classes
- **Enhanced readability** with boxes and highlighting
- **Professional polish** with proper styling

Use these features to elevate your biomedical presentations while maintaining scientific professionalism and content focus.
