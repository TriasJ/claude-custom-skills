# Slide Patterns for reveal.js Presentations

Pre-built, reusable slide patterns that can be quickly customized for any presentation. The skill prompts users before applying patterns to maintain flexibility.

## Content Patterns

### 1. Title + Bullets

**Use for**: Main content slides, key points, agenda items

```html
<section>
  <h2><i class="fas fa-list"></i> Your Title</h2>
  <ul>
    <li class="fragment">First point with auto-reveal</li>
    <li class="fragment">Second point</li>
    <li class="fragment">Third point</li>
    <li class="fragment">Fourth point</li>
  </ul>
  <aside class="notes">
    Speaker notes go here...
  </aside>
</section>
```

### 2. Image + Caption

**Use for**: Visual emphasis, product photos, examples

```html
<section>
  <h2><i class="fas fa-image"></i> Visual Example</h2>
  <div class="image-container">
    <img src="data:image/jpeg;base64,..."
         alt="Description"
         class="bordered-image">
    <div class="image-caption">Photo credit: Source Name</div>
  </div>
  <aside class="notes">
    Image: [Title] from [Source]
  </aside>
</section>
```

### 3. Two Column

**Use for**: Comparisons, before/after, pros/cons

```html
<section>
  <h2><i class="fas fa-columns"></i> Comparison</h2>
  <div class="two-column">
    <div class="column">
      <h3 class="teal-text">Option A</h3>
      <ul>
        <li>Benefit 1</li>
        <li>Benefit 2</li>
        <li>Benefit 3</li>
      </ul>
    </div>
    <div class="column">
      <h3 class="blue-text">Option B</h3>
      <ul>
        <li>Benefit 1</li>
        <li>Benefit 2</li>
        <li>Benefit 3</li>
      </ul>
    </div>
  </div>
</section>
```

### 4. Comparison (Pros/Cons)

**Use for**: Decision-making slides, feature analysis

```html
<section>
  <h2><i class="fas fa-balance-scale"></i> Pros & Cons</h2>
  <div class="two-column">
    <div class="column">
      <h3 style="color: var(--success-color);"><i class="fas fa-check-circle"></i> Pros</h3>
      <ul>
        <li>Advantage 1</li>
        <li>Advantage 2</li>
        <li>Advantage 3</li>
      </ul>
    </div>
    <div class="column">
      <h3 style="color: var(--warning-color);"><i class="fas fa-times-circle"></i> Cons</h3>
      <ul>
        <li>Disadvantage 1</li>
        <li>Disadvantage 2</li>
        <li>Disadvantage 3</li>
      </ul>
    </div>
  </div>
</section>
```

### 5. Quote

**Use for**: Testimonials, inspiring quotes, key messages

```html
<section>
  <div class="quote-container">
    <blockquote class="big-quote">
      "Your powerful quote goes here."
    </blockquote>
    <cite>— Author Name, Title</cite>
  </div>
  <aside class="notes">
    This quote emphasizes our key message about...
  </aside>
</section>
```

## Data Patterns

### 6. Infographic

**Use for**: Statistics, key metrics, visual data

```html
<section>
  <h2><i class="fas fa-chart-pie"></i> Key Statistics</h2>
  <div class="stats-grid">
    <div class="stat-card fragment">
      <div class="stat-icon"><i class="fas fa-rocket"></i></div>
      <div class="stat-number">250%</div>
      <div class="stat-label">Growth Rate</div>
    </div>
    <div class="stat-card fragment">
      <div class="stat-icon"><i class="fas fa-users"></i></div>
      <div class="stat-number">50K+</div>
      <div class="stat-label">Active Users</div>
    </div>
    <div class="stat-card fragment">
      <div class="stat-icon"><i class="fas fa-globe"></i></div>
      <div class="stat-number">120</div>
      <div class="stat-label">Countries</div>
    </div>
    <div class="stat-card fragment">
      <div class="stat-icon"><i class="fas fa-star"></i></div>
      <div class="stat-number">4.8/5</div>
      <div class="stat-label">User Rating</div>
    </div>
  </div>
  <aside class="notes">
    These metrics show our strong market performance...
  </aside>
</section>
```

### 7. Timeline

**Use for**: History, roadmap, project phases

```html
<section>
  <h2><i class="fas fa-timeline"></i> Project Timeline</h2>
  <div class="timeline-container">
    <div class="timeline-item fragment">
      <div class="timeline-marker">Q1</div>
      <div class="timeline-content">
        <h3>Phase 1: Research</h3>
        <p>Market analysis and user interviews</p>
      </div>
    </div>
    <div class="timeline-item fragment">
      <div class="timeline-marker">Q2</div>
      <div class="timeline-content">
        <h3>Phase 2: Design</h3>
        <p>Prototyping and user testing</p>
      </div>
    </div>
    <div class="timeline-item fragment">
      <div class="timeline-marker">Q3</div>
      <div class="timeline-content">
        <h3>Phase 3: Development</h3>
        <p>Building core features</p>
      </div>
    </div>
    <div class="timeline-item fragment">
      <div class="timeline-marker">Q4</div>
      <div class="timeline-content">
        <h3>Phase 4: Launch</h3>
        <p>Public release and marketing</p>
      </div>
    </div>
  </div>
</section>

<style>
.timeline-container {
  margin: 2em 0;
}
.timeline-item {
  display: flex;
  align-items: center;
  margin: 1.5em 0;
  gap: 2em;
}
.timeline-marker {
  flex-shrink: 0;
  width: 4em;
  height: 4em;
  background: linear-gradient(135deg, var(--teal-accent), var(--blue-accent));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #000;
  font-size: 1.2em;
}
.timeline-content {
  flex: 1;
  padding: 1em 1.5em;
  background: rgba(0, 255, 245, 0.05);
  border-left: 3px solid var(--teal-accent);
  border-radius: 8px;
}
.timeline-content h3 {
  margin: 0 0 0.3em 0;
  color: var(--teal-accent);
}
.timeline-content p {
  margin: 0;
  color: #888;
}
</style>
```

### 8. Chart (D3.js)

**Use for**: Data visualization, trends, comparisons

```html
<section>
  <h2><i class="fas fa-chart-line"></i> Sales Growth</h2>
  <div class="fig-container"
       data-file="visualizations/sales-chart.html"
       style="height: 600px;">
  </div>
  <aside class="notes">
    This interactive chart shows our quarterly sales trend.
    Note the significant spike in Q4 due to holiday season.
  </aside>
</section>
```

### 9. Data Grid

**Use for**: Multiple metrics, dashboard view

```html
<section>
  <h2><i class="fas fa-th"></i> Dashboard</h2>
  <div class="data-grid">
    <div class="data-item fragment">
      <span class="data-label">Revenue</span>
      <span class="data-value">$2.4M</span>
      <span class="data-change positive">+18% ↑</span>
    </div>
    <div class="data-item fragment">
      <span class="data-label">Customers</span>
      <span class="data-value">12,543</span>
      <span class="data-change positive">+24% ↑</span>
    </div>
    <div class="data-item fragment">
      <span class="data-label">Churn Rate</span>
      <span class="data-value">3.2%</span>
      <span class="data-change negative">+0.5% ↓</span>
    </div>
    <div class="data-item fragment">
      <span class="data-label">NPS Score</span>
      <span class="data-value">67</span>
      <span class="data-change positive">+5 ↑</span>
    </div>
  </div>
</section>

<style>
.data-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2em;
  margin-top: 2em;
}
.data-item {
  background: rgba(0, 255, 245, 0.05);
  border: 2px solid rgba(0, 255, 245, 0.2);
  border-radius: 8px;
  padding: 2em;
  display: flex;
  flex-direction: column;
  gap: 0.5em;
}
.data-label {
  font-size: 0.9em;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.data-value {
  font-size: 2.5em;
  font-weight: 700;
  color: var(--heading-color);
}
.data-change {
  font-size: 0.9em;
  font-weight: 600;
}
.data-change.positive {
  color: var(--success-color);
}
.data-change.negative {
  color: var(--warning-color);
}
</style>
```

## Special Patterns

### 10. Team Intro

**Use for**: About us, team members, speakers

```html
<section>
  <h2><i class="fas fa-users"></i> Meet the Team</h2>
  <div class="team-grid">
    <div class="team-member fragment">
      <img src="data:image/jpeg;base64,..."
           alt="Team Member"
           class="team-photo">
      <h3>Jane Doe</h3>
      <p class="team-role">CEO & Founder</p>
      <p class="team-bio">15 years in tech innovation</p>
    </div>
    <div class="team-member fragment">
      <img src="data:image/jpeg;base64,..."
           alt="Team Member"
           class="team-photo">
      <h3>John Smith</h3>
      <p class="team-role">CTO</p>
      <p class="team-bio">Expert in scalable systems</p>
    </div>
    <!-- Add more team members -->
  </div>
</section>

<style>
.team-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2em;
  margin-top: 2em;
}
.team-member {
  text-align: center;
  padding: 1.5em;
  background: rgba(0, 255, 245, 0.05);
  border-radius: 8px;
  border: 2px solid rgba(0, 255, 245, 0.2);
  transition: all 0.3s;
}
.team-member:hover {
  transform: translateY(-5px);
  border-color: var(--teal-accent);
}
.team-photo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 1em;
  border: 3px solid var(--teal-accent);
}
.team-member h3 {
  margin: 0.5em 0 0.2em;
  color: var(--heading-color);
}
.team-role {
  color: var(--teal-accent);
  font-weight: 600;
  margin: 0;
}
.team-bio {
  font-size: 0.8em;
  color: #888;
  margin: 0.5em 0 0;
}
</style>
```

### 11. Process Flow

**Use for**: Workflows, step-by-step guides, methodologies

```html
<section>
  <h2><i class="fas fa-diagram-project"></i> Our Process</h2>
  <div class="process-flow">
    <div class="process-step fragment">
      <div class="step-number">1</div>
      <h3>Discover</h3>
      <p>Understand needs</p>
    </div>
    <div class="process-arrow fragment">→</div>
    <div class="process-step fragment">
      <div class="step-number">2</div>
      <h3>Design</h3>
      <p>Create solutions</p>
    </div>
    <div class="process-arrow fragment">→</div>
    <div class="process-step fragment">
      <div class="step-number">3</div>
      <h3>Develop</h3>
      <p>Build product</p>
    </div>
    <div class="process-arrow fragment">→</div>
    <div class="process-step fragment">
      <div class="step-number">4</div>
      <h3>Deliver</h3>
      <p>Launch & iterate</p>
    </div>
  </div>
</section>
```

### 12. Full Background

**Use for**: Section breaks, dramatic emphasis

```html
<section data-background-image="data:image/jpeg;base64,..."
         data-background-opacity="0.3">
  <div class="overlay-content">
    <h1 class="shadow-text">Section Title</h1>
    <p class="shadow-text subtitle">Beautiful background with overlaid text</p>
  </div>
  <aside class="notes">
    Image: [Title] from [Source]
  </aside>
</section>
```

### 13. Video Background

**Use for**: Product demos, dynamic intros, atmosphere

```html
<section data-background-video="videos/background.mp4"
         data-background-video-loop
         data-background-video-muted
         data-background-opacity="0.5">
  <div class="overlay-content">
    <h2 class="shadow-text">Video Background</h2>
    <p class="shadow-text">Looping video creates dynamic atmosphere</p>
  </div>
</section>
```

## Using Patterns in the Skill

When the skill creates presentations, it:

1. **Prompts user**: "Would you like to use pre-built slide patterns?"
2. **If yes**: "Which patterns work best for your content?"
   - Shows list of patterns with use cases
   - User selects relevant patterns
3. **Generates slides**: Using selected patterns with user's content
4. **Maintains flexibility**: User can always customize further

This gives you the **best of both worlds**:
- Speed of pre-built patterns
- Flexibility to customize as needed

## Customization Tips

1. **Colors**: Replace teal/blue accents with your brand colors
2. **Icons**: Use Font Awesome or custom SVG icons
3. **Spacing**: Adjust grid gaps and padding for your content
4. **Animations**: Modify fragment timing and transition effects
5. **Fonts**: Update CSS variables for different typography

## Pattern Selection Guide

| Content Type | Recommended Pattern |
|--------------|---------------------|
| Key points | Title + Bullets |
| Statistics | Infographic or Data Grid |
| Comparison | Two Column or Pros/Cons |
| History/Roadmap | Timeline |
| Team introduction | Team Intro |
| Process explanation | Process Flow |
| Testimonial | Quote |
| Visual example | Image + Caption |
| Section break | Full Background |
| Data trends | Chart (D3.js) |
| Product demo | Video Background |

## Resources

- All patterns work with Quantum Dark and other templates
- Patterns are responsive and mobile-friendly
- Fragment animations included by default
- Speaker notes templates provided
- Accessibility features included (ARIA labels, alt text)

---

**Tip**: Mix and match patterns throughout your presentation for visual variety while maintaining consistency.
