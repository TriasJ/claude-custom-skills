# PowerPoint Templates Reference

Complete definitions for all 8 aesthetic templates with parameterized code snippets.

## CRITICAL - Coordinate System

**All templates in this file use WIDESCREEN (16:9) layout:**
- Layout dimensions: **10 inches wide × 5.625 inches tall**
- All coordinates (x, y, w, h) are in **INCHES**, NOT percentages
- All template coordinates are designed for widescreen and must be used with: `pptx.layout = 'LAYOUT_16x9';`
- Ensure all custom shapes fit: `x + w ≤ 10` and `y + h ≤ 5.625`

## Template 1: Corporate Blue

**Professional, clean, business-ready**

**Colors:**
- Primary: Navy Blue `#003366`
- Secondary: Light Blue `#4472C4`
- Background: White `#FFFFFF`
- Text: Dark Gray `#333333`
- Accent: Gray `#666666`

**Fonts:** Arial, Calibri

**Best for:** Business presentations, quarterly reviews, corporate training, investor decks

**Master Slide Definitions:**

```javascript
function createCorporateBlueTemplate(pptx, options = {}) {
  const colors = {
    primary: options.primaryColor || '003366',
    secondary: options.secondaryColor || '4472C4',
    background: options.backgroundColor || 'FFFFFF',
    text: options.textColor || '333333',
    accent: options.accentColor || '666666'
  };

  const logoPath = options.logoPath || null;
  const companyName = options.companyName || 'Company Name';

  // Title Slide Master
  pptx.defineSlideMaster({
    title: 'CORPORATE_TITLE',
    background: { color: colors.background },
    objects: [
      // Logo (if provided)
      ...(logoPath ? [{
        image: {
          path: logoPath,
          x: 0.5,
          y: 0.3,
          w: 1.5,
          h: 0.5
        }
      }] : []),
      // Title placeholder
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.5,
            y: 2.5,
            w: 9,
            h: 1.5,
            fontSize: 44,
            bold: true,
            color: colors.primary,
            align: 'center',
            valign: 'middle'
          },
          text: 'Click to add title'
        }
      },
      // Subtitle placeholder
      {
        placeholder: {
          options: {
            name: 'subtitle',
            type: 'body',
            x: 0.5,
            y: 4.2,
            w: 9,
            h: 0.6,
            fontSize: 20,
            color: colors.secondary,
            align: 'center'
          },
          text: 'Click to add subtitle'
        }
      },
      // Footer line
      {
        line: {
          x: 0.5,
          y: 6.8,
          w: 9,
          h: 0,
          line: { color: colors.secondary, width: 2 }
        }
      },
      // Footer text
      {
        text: {
          text: `© 2024 ${companyName}`,
          options: {
            x: 0.5,
            y: 7,
            w: 9,
            h: 0.3,
            fontSize: 10,
            color: colors.accent,
            align: 'center'
          }
        }
      }
    ],
    slideNumber: {
      x: 9,
      y: 7,
      fontSize: 10,
      color: colors.accent
    }
  });

  // Content Slide Master
  pptx.defineSlideMaster({
    title: 'CORPORATE_CONTENT',
    background: { color: colors.background },
    objects: [
      // Small logo
      ...(logoPath ? [{
        image: {
          path: logoPath,
          x: 0.5,
          y: 0.3,
          w: 1,
          h: 0.35
        }
      }] : []),
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.5,
            y: 1,
            w: 9,
            h: 0.6,
            fontSize: 28,
            bold: true,
            color: colors.primary
          },
          text: 'Slide Title'
        }
      },
      // Divider line
      {
        line: {
          x: 0.5,
          y: 1.7,
          w: 9,
          h: 0,
          line: { color: colors.secondary, width: 1 }
        }
      },
      // Footer
      {
        text: {
          text: companyName,
          options: {
            x: 0.5,
            y: 7,
            w: 8,
            h: 0.3,
            fontSize: 10,
            color: colors.accent,
            align: 'left'
          }
        }
      }
    ],
    slideNumber: {
      x: 9,
      y: 7,
      fontSize: 10,
      color: colors.accent
    }
  });

  // Section Header Master
  pptx.defineSlideMaster({
    title: 'CORPORATE_SECTION',
    background: { color: colors.primary },
    objects: [
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 1,
            y: 2.5,
            w: 8,
            h: 1.5,
            fontSize: 40,
            bold: true,
            color: 'FFFFFF',
            align: 'center',
            valign: 'middle'
          }
        }
      }
    ]
  });

  return {
    name: 'Corporate Blue',
    colors,
    chartColors: [colors.secondary, colors.primary, colors.accent, 'ED7D31', 'A5A5A5']
  };
}
```

## Template 2: Modern Gradient

**Contemporary, eye-catching, creative**

**Colors:**
- Primary: Purple `#6B46C1`
- Secondary: Pink `#EC4899`
- Background: White `#FFFFFF`
- Text: Dark Gray `#2D3748`
- Accent: Light Purple `#9F7AEA`

**Fonts:** Sans-serif, modern (Helvetica, Arial)

**Best for:** Product launches, marketing pitches, creative showcases, startup decks

```javascript
function createModernGradientTemplate(pptx, options = {}) {
  const colors = {
    primary: options.primaryColor || '6B46C1',
    secondary: options.secondaryColor || 'EC4899',
    background: options.backgroundColor || 'FFFFFF',
    text: options.textColor || '2D3748',
    accent: options.accentColor || '9F7AEA'
  };

  // Title Slide with Gradient Background
  pptx.defineSlideMaster({
    title: 'MODERN_TITLE',
    background: { color: colors.primary },
    objects: [
      // Gradient overlay (using shape)
      {
        rect: {
          x: 0,
          y: 0,
          w: 10,
          h: 7.5,
          fill: {
            type: 'solid',
            color: colors.primary,
            transparency: 10
          }
        }
      },
      // Title placeholder
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 1,
            y: 2,
            w: 8,
            h: 2,
            fontSize: 54,
            bold: true,
            color: 'FFFFFF',
            align: 'left',
            valign: 'top'
          }
        }
      },
      // Subtitle
      {
        placeholder: {
          options: {
            name: 'subtitle',
            type: 'body',
            x: 1,
            y: 4.5,
            w: 8,
            h: 0.8,
            fontSize: 24,
            color: 'FFFFFF',
            align: 'left'
          }
        }
      },
      // Accent shape
      {
        rect: {
          x: 0,
          y: 7,
          w: 10,
          h: 0.5,
          fill: { color: colors.secondary }
        }
      }
    ]
  });

  // Content Slide
  pptx.defineSlideMaster({
    title: 'MODERN_CONTENT',
    background: { color: colors.background },
    objects: [
      // Colored accent bar
      {
        rect: {
          x: 0,
          y: 0,
          w: 0.15,
          h: 7.5,
          fill: { color: colors.primary }
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.5,
            y: 0.5,
            w: 9,
            h: 0.8,
            fontSize: 32,
            bold: true,
            color: colors.primary
          }
        }
      }
    ],
    slideNumber: {
      x: 9,
      y: 7,
      fontSize: 10,
      color: colors.text
    }
  });

  // Image Slide (full-bleed)
  pptx.defineSlideMaster({
    title: 'MODERN_IMAGE',
    background: { color: 'FFFFFF' },
    objects: [
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.5,
            y: 6,
            w: 9,
            h: 0.8,
            fontSize: 28,
            bold: true,
            color: 'FFFFFF',
            fill: { color: colors.primary, transparency: 20 }
          }
        }
      }
    ]
  });

  return {
    name: 'Modern Gradient',
    colors,
    chartColors: [colors.primary, colors.secondary, colors.accent, 'F59E0B', '10B981']
  };
}
```

## Template 3: Academic Classic

**Traditional, scholarly, formal**

**Colors:**
- Primary: Burgundy `#800020`
- Secondary: Gold `#FFD700`
- Background: Cream `#F5F5DC`
- Text: Black `#000000`
- Accent: Dark Gold `#B8860B`

**Fonts:** Georgia, Times New Roman

**Best for:** Research presentations, academic conferences, educational content, formal lectures

```javascript
function createAcademicClassicTemplate(pptx, options = {}) {
  const colors = {
    primary: options.primaryColor || '800020',
    secondary: options.secondaryColor || 'FFD700',
    background: options.backgroundColor || 'F5F5DC',
    text: options.textColor || '000000',
    accent: options.accentColor || 'B8860B'
  };

  const institution = options.institution || 'Institution Name';

  // Title Slide
  pptx.defineSlideMaster({
    title: 'ACADEMIC_TITLE',
    background: { color: colors.background },
    objects: [
      // Border frame
      {
        rect: {
          x: 0.3,
          y: 0.3,
          w: 9.4,
          h: 6.9,
          fill: { type: 'none' },
          line: { color: colors.primary, width: 3 }
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 1,
            y: 2,
            w: 8,
            h: 1.5,
            fontSize: 40,
            bold: true,
            color: colors.primary,
            align: 'center',
            fontFace: 'Georgia'
          }
        }
      },
      // Subtitle
      {
        placeholder: {
          options: {
            name: 'subtitle',
            type: 'body',
            x: 1,
            y: 3.8,
            w: 8,
            h: 0.6,
            fontSize: 20,
            color: colors.text,
            align: 'center',
            fontFace: 'Georgia'
          }
        }
      },
      // Institution name
      {
        text: {
          text: institution,
          options: {
            x: 1,
            y: 6.5,
            w: 8,
            h: 0.4,
            fontSize: 14,
            color: colors.primary,
            align: 'center',
            fontFace: 'Georgia',
            italic: true
          }
        }
      }
    ]
  });

  // Content Slide (Two-Column Layout)
  pptx.defineSlideMaster({
    title: 'ACADEMIC_CONTENT',
    background: { color: colors.background },
    objects: [
      // Header bar
      {
        rect: {
          x: 0,
          y: 0,
          w: 10,
          h: 0.8,
          fill: { color: colors.primary }
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.5,
            y: 0.15,
            w: 9,
            h: 0.5,
            fontSize: 26,
            bold: true,
            color: 'FFFFFF',
            fontFace: 'Georgia'
          }
        }
      },
      // Footer line
      {
        line: {
          x: 0.5,
          y: 7,
          w: 9,
          h: 0,
          line: { color: colors.accent, width: 1 }
        }
      }
    ],
    slideNumber: {
      x: 9,
      y: 7.2,
      fontSize: 10,
      color: colors.text
    }
  });

  return {
    name: 'Academic Classic',
    colors,
    chartColors: [colors.primary, colors.accent, '8B4513', '2F4F4F', '696969']
  };
}
```

## Template 4: Creative Pop

**Bold, colorful, energetic**

**Colors:**
- Primary: Orange `#FF6B35`
- Secondary: Teal `#00D9C0`
- Tertiary: Yellow `#FFE66D`
- Accent: Purple `#7B2CBF`
- Background: White `#FFFFFF`

**Fonts:** Poppins, Roboto, Arial

**Best for:** Creative pitches, youth-oriented content, innovation showcases, design portfolios

```javascript
function createCreativePopTemplate(pptx, options = {}) {
  const colors = {
    primary: options.primaryColor || 'FF6B35',
    secondary: options.secondaryColor || '00D9C0',
    tertiary: options.tertiaryColor || 'FFE66D',
    accent: options.accentColor || '7B2CBF',
    background: options.backgroundColor || 'FFFFFF'
  };

  // Title Slide
  pptx.defineSlideMaster({
    title: 'CREATIVE_TITLE',
    background: { color: colors.background },
    objects: [
      // Colorful shapes for decoration
      {
        ellipse: {
          x: -1,
          y: -0.5,
          w: 3,
          h: 3,
          fill: { color: colors.primary, transparency: 70 }
        }
      },
      {
        ellipse: {
          x: 8,
          y: 5.5,
          w: 2.5,
          h: 2.5,
          fill: { color: colors.secondary, transparency: 70 }
        }
      },
      {
        rect: {
          x: 0.3,
          y: 6,
          w: 1.2,
          h: 1.2,
          fill: { color: colors.tertiary, transparency: 70 },
          rotate: 15
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 1.5,
            y: 2,
            w: 7,
            h: 2,
            fontSize: 52,
            bold: true,
            color: colors.accent,
            align: 'left'
          }
        }
      },
      // Subtitle
      {
        placeholder: {
          options: {
            name: 'subtitle',
            type: 'body',
            x: 1.5,
            y: 4.3,
            w: 7,
            h: 0.8,
            fontSize: 22,
            color: colors.primary,
            align: 'left'
          }
        }
      }
    ]
  });

  // Content Slide
  pptx.defineSlideMaster({
    title: 'CREATIVE_CONTENT',
    background: { color: colors.background },
    objects: [
      // Accent shapes
      {
        rect: {
          x: 0,
          y: 0,
          w: 0.5,
          h: 1.5,
          fill: { color: colors.primary }
        }
      },
      {
        ellipse: {
          x: 9,
          y: 0.2,
          w: 0.8,
          h: 0.8,
          fill: { color: colors.secondary, transparency: 60 }
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.8,
            y: 0.4,
            w: 8,
            h: 0.7,
            fontSize: 32,
            bold: true,
            color: colors.accent
          }
        }
      }
    ],
    slideNumber: {
      x: 0.5,
      y: 7,
      fontSize: 11,
      color: colors.accent,
      bold: true
    }
  });

  return {
    name: 'Creative Pop',
    colors,
    chartColors: [colors.primary, colors.secondary, colors.tertiary, colors.accent, 'E63946']
  };
}
```

## Template 5: Minimal White

**Clean, simple, elegant**

**Colors:**
- Primary: Black `#000000`
- Secondary: Light Gray `#F5F5F5`
- Accent: Blue `#0088CC`
- Text: Dark Gray `#333333`
- Background: White `#FFFFFF`

**Fonts:** Helvetica, Arial

**Best for:** Portfolio presentations, minimalist brands, design showcases, tech products

```javascript
function createMinimalWhiteTemplate(pptx, options = {}) {
  const colors = {
    primary: options.primaryColor || '000000',
    secondary: options.secondaryColor || 'F5F5F5',
    accent: options.accentColor || '0088CC',
    text: options.textColor || '333333',
    background: options.backgroundColor || 'FFFFFF'
  };

  // Title Slide
  pptx.defineSlideMaster({
    title: 'MINIMAL_TITLE',
    background: { color: colors.background },
    objects: [
      // Single accent line
      {
        line: {
          x: 2,
          y: 3,
          w: 6,
          h: 0,
          line: { color: colors.accent, width: 3 }
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 2,
            y: 3.5,
            w: 6,
            h: 1.2,
            fontSize: 48,
            bold: false,
            color: colors.primary,
            align: 'left',
            fontFace: 'Helvetica'
          }
        }
      },
      // Subtitle
      {
        placeholder: {
          options: {
            name: 'subtitle',
            type: 'body',
            x: 2,
            y: 5,
            w: 6,
            h: 0.5,
            fontSize: 18,
            color: colors.text,
            align: 'left',
            fontFace: 'Helvetica'
          }
        }
      }
    ]
  });

  // Content Slide
  pptx.defineSlideMaster({
    title: 'MINIMAL_CONTENT',
    background: { color: colors.background },
    objects: [
      // Minimal accent
      {
        rect: {
          x: 0.5,
          y: 0.5,
          w: 0.05,
          h: 0.5,
          fill: { color: colors.accent }
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.8,
            y: 0.5,
            w: 8.7,
            h: 0.5,
            fontSize: 28,
            bold: false,
            color: colors.primary,
            fontFace: 'Helvetica'
          }
        }
      }
    ],
    slideNumber: {
      x: 9,
      y: 7,
      fontSize: 9,
      color: colors.text
    }
  });

  // Image Slide (large image with minimal text)
  pptx.defineSlideMaster({
    title: 'MINIMAL_IMAGE',
    background: { color: colors.background },
    objects: [
      {
        placeholder: {
          options: {
            name: 'caption',
            type: 'body',
            x: 0.5,
            y: 6.5,
            w: 9,
            h: 0.5,
            fontSize: 14,
            color: colors.text,
            align: 'center',
            fontFace: 'Helvetica'
          }
        }
      }
    ]
  });

  return {
    name: 'Minimal White',
    colors,
    chartColors: [colors.accent, colors.primary, '95A5A6', '3498DB', 'E74C3C']
  };
}
```

## Using Templates

**Quick template application:**

```javascript
// Select and apply template
const template = createCorporateBlueTemplate(pptx, {
  logoPath: './images/logo.png',
  companyName: 'Acme Corp',
  primaryColor: '003366'
});

// Use master slides
const titleSlide = pptx.addSlide({ masterName: 'CORPORATE_TITLE' });
titleSlide.addText('Annual Report 2024', { placeholder: 'title' });
titleSlide.addText('Financial Review', { placeholder: 'subtitle' });

const contentSlide = pptx.addSlide({ masterName: 'CORPORATE_CONTENT' });
contentSlide.addText('Q4 Results', { placeholder: 'title' });

// Use template colors for charts
contentSlide.addChart(pptx.ChartType.bar, chartData, {
  chartColors: template.chartColors,
  ...
});
```

**Customization:**

All template functions accept an options object for customization:
- `primaryColor`, `secondaryColor`, `backgroundColor`, etc.
- `logoPath`: Path to logo image
- `companyName` or `institution`: Organization name
- `fontFace`: Override default fonts

**Template selection helper:**

```javascript
function selectTemplate(templateName, options = {}) {
  const templates = {
    'corporate-blue': createCorporateBlueTemplate,
    'modern-gradient': createModernGradientTemplate,
    'academic-classic': createAcademicClassicTemplate,
    'creative-pop': createCreativePopTemplate,
    'minimal-white': createMinimalWhiteTemplate
  };

  return templates[templateName](pptx, options);
}

// Usage
const template = selectTemplate('corporate-blue', {
  logoPath: './logo.png',
  companyName: 'Acme Corp'
});
```

## Template 6: Neumorphic Soft UI

**Soft, tactile, modern 3D appearance**

**Colors:**
- Primary: Soft Gray `#E0E5EC`
- Secondary: Light Gray `#F0F5FA`
- Shadow Dark: `#A8B1C1`
- Shadow Light: White `#FFFFFF`
- Accent: Soft Blue `#6B8EBF`
- Text: Dark Gray `#4A5568`

**Fonts:** Poppins, Inter, System-UI

**Best for:** Modern tech products, UI/UX showcases, app presentations, SaaS platforms

**Key Features:** Soft shadows create embossed/extruded appearance, minimal color contrast, almost tactile feel

```javascript
function createNeumorphicSoftUITemplate(pptx, options = {}) {
  const colors = {
    primary: options.primaryColor || 'E0E5EC',
    secondary: options.secondaryColor || 'F0F5FA',
    shadowDark: options.shadowDark || 'A8B1C1',
    shadowLight: options.shadowLight || 'FFFFFF',
    accent: options.accentColor || '6B8EBF',
    text: options.textColor || '4A5568',
    background: options.backgroundColor || 'E0E5EC'
  };

  // Title Slide - Neumorphic Style
  pptx.defineSlideMaster({
    title: 'NEUMORPHIC_TITLE',
    background: { color: colors.background },
    objects: [
      // Soft shadow effect - dark shadow (bottom right)
      {
        rect: {
          x: 2.1,
          y: 2.6,
          w: 5.8,
          h: 2.3,
          fill: { color: colors.shadowDark, transparency: 30 },
          line: { type: 'none' }
        }
      },
      // Light shadow (top left)
      {
        rect: {
          x: 1.9,
          y: 2.4,
          w: 5.8,
          h: 2.3,
          fill: { color: colors.shadowLight, transparency: 90 },
          line: { type: 'none' }
        }
      },
      // Main card (neumorphic element)
      {
        rect: {
          x: 2,
          y: 2.5,
          w: 5.8,
          h: 2.3,
          fill: { color: colors.background },
          line: { type: 'none' }
        }
      },
      // Title placeholder
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 2.2,
            y: 2.8,
            w: 5.4,
            h: 1.2,
            fontSize: 44,
            bold: true,
            color: colors.text,
            align: 'center',
            valign: 'middle',
            fontFace: 'Poppins'
          },
          text: 'Click to add title'
        }
      },
      // Subtitle
      {
        placeholder: {
          options: {
            name: 'subtitle',
            type: 'body',
            x: 2.2,
            y: 4.1,
            w: 5.4,
            h: 0.5,
            fontSize: 18,
            color: colors.accent,
            align: 'center',
            fontFace: 'Poppins'
          },
          text: 'Click to add subtitle'
        }
      },
      // Floating accent elements (soft circles)
      {
        ellipse: {
          x: 0.8,
          y: 1.2,
          w: 0.8,
          h: 0.8,
          fill: { color: colors.accent, transparency: 80 },
          line: { type: 'none' }
        }
      },
      {
        ellipse: {
          x: 8.5,
          y: 5.8,
          w: 1,
          h: 1,
          fill: { color: colors.accent, transparency: 80 },
          line: { type: 'none' }
        }
      }
    ]
  });

  // Content Slide - Neumorphic Cards
  pptx.defineSlideMaster({
    title: 'NEUMORPHIC_CONTENT',
    background: { color: colors.background },
    objects: [
      // Title card with soft shadows
      // Dark shadow
      {
        rect: {
          x: 0.6,
          y: 0.6,
          w: 8.8,
          h: 0.7,
          fill: { color: colors.shadowDark, transparency: 30 },
          line: { type: 'none' }
        }
      },
      // Light shadow
      {
        rect: {
          x: 0.4,
          y: 0.4,
          w: 8.8,
          h: 0.7,
          fill: { color: colors.shadowLight, transparency: 90 },
          line: { type: 'none' }
        }
      },
      // Main title card
      {
        rect: {
          x: 0.5,
          y: 0.5,
          w: 8.8,
          h: 0.7,
          fill: { color: colors.background },
          line: { type: 'none' }
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.7,
            y: 0.55,
            w: 8.4,
            h: 0.6,
            fontSize: 28,
            bold: true,
            color: colors.text,
            fontFace: 'Poppins'
          }
        }
      },
      // Soft divider
      {
        line: {
          x: 0.5,
          y: 1.35,
          w: 8.8,
          h: 0,
          line: { color: colors.shadowDark, width: 1, transparency: 50 }
        }
      }
    ],
    slideNumber: {
      x: 9,
      y: 7,
      fontSize: 10,
      color: colors.accent
    }
  });

  // Section Header - Large Neumorphic Card
  pptx.defineSlideMaster({
    title: 'NEUMORPHIC_SECTION',
    background: { color: colors.background },
    objects: [
      // Large centered neumorphic card
      // Dark shadow
      {
        rect: {
          x: 1.6,
          y: 2.6,
          w: 6.8,
          h: 2.3,
          fill: { color: colors.shadowDark, transparency: 30 },
          line: { type: 'none' }
        }
      },
      // Light shadow
      {
        rect: {
          x: 1.4,
          y: 2.4,
          w: 6.8,
          h: 2.3,
          fill: { color: colors.shadowLight, transparency: 90 },
          line: { type: 'none' }
        }
      },
      // Main card
      {
        rect: {
          x: 1.5,
          y: 2.5,
          w: 6.8,
          h: 2.3,
          fill: { color: colors.background },
          line: { type: 'none' }
        }
      },
      // Section title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 1.7,
            y: 3,
            w: 6.4,
            h: 1.3,
            fontSize: 40,
            bold: true,
            color: colors.accent,
            align: 'center',
            valign: 'middle',
            fontFace: 'Poppins'
          }
        }
      }
    ]
  });

  return {
    name: 'Neumorphic Soft UI',
    colors,
    chartColors: [colors.accent, '8BA3C7', '5A7BA6', '9FB8D3', '7496BB']
  };
}
```

## Template 7: Modern Tech (Dark Mode with Neon)

**Futuristic, high-tech, contemporary**

**Colors:**
- Primary: Dark Navy `#0A1929`
- Secondary: Darker Navy `#0D1B2A`
- Accent: Neon Blue `#00D9FF`
- Secondary Accent: Neon Purple `#A855F7`
- Text: White `#FFFFFF`
- Muted: Gray `#8B949E`

**Fonts:** JetBrains Mono, Roboto Mono, Consolas, Arial

**Best for:** Tech startups, software launches, developer presentations, AI/ML products, cybersecurity

**Key Features:** Dark backgrounds, vibrant neon accents, grid patterns, tech aesthetic

```javascript
function createModernTechTemplate(pptx, options = {}) {
  const colors = {
    primary: options.primaryColor || '0A1929',
    secondary: options.secondaryColor || '0D1B2A',
    accent: options.accentColor || '00D9FF',
    accentSecondary: options.accentSecondary || 'A855F7',
    text: options.textColor || 'FFFFFF',
    muted: options.mutedColor || '8B949E',
    background: options.backgroundColor || '0A1929'
  };

  // Title Slide - Tech Grid Background
  pptx.defineSlideMaster({
    title: 'TECH_TITLE',
    background: { color: colors.primary },
    objects: [
      // Grid pattern simulation (use lines)
      ...[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(i => ({
        line: {
          x: i,
          y: 0,
          w: 0,
          h: 7.5,
          line: { color: colors.muted, width: 0.5, transparency: 85 }
        }
      })),
      ...[0, 1, 2, 3, 4, 5, 6, 7].map(i => ({
        line: {
          x: 0,
          y: i,
          w: 10,
          h: 0,
          line: { color: colors.muted, width: 0.5, transparency: 85 }
        }
      })),
      // Neon accent line (top)
      {
        line: {
          x: 0,
          y: 0.05,
          w: 10,
          h: 0,
          line: { color: colors.accent, width: 2, glow: { size: 8, color: colors.accent, transparency: 50 } }
        }
      },
      // Neon accent shape (corner)
      {
        rect: {
          x: 0,
          y: 0,
          w: 0.15,
          h: 7.5,
          fill: { color: colors.accent },
          glow: { size: 10, color: colors.accent, transparency: 60 }
        }
      },
      // Title with glow effect
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 1.5,
            y: 2,
            w: 7,
            h: 2,
            fontSize: 54,
            bold: true,
            color: colors.text,
            align: 'left',
            fontFace: 'Arial'
          },
          text: 'PRESENTATION TITLE'
        }
      },
      // Neon line under title
      {
        line: {
          x: 1.5,
          y: 4.1,
          w: 4,
          h: 0,
          line: { color: colors.accent, width: 3 }
        }
      },
      // Subtitle
      {
        placeholder: {
          options: {
            name: 'subtitle',
            type: 'body',
            x: 1.5,
            y: 4.5,
            w: 7,
            h: 0.8,
            fontSize: 20,
            color: colors.muted,
            align: 'left'
          },
          text: 'Subtitle text'
        }
      },
      // Tech accent elements
      {
        rect: {
          x: 8.5,
          y: 6.5,
          w: 1,
          h: 0.7,
          fill: { type: 'none' },
          line: { color: colors.accentSecondary, width: 2 }
        }
      }
    ]
  });

  // Content Slide - Clean Dark Mode
  pptx.defineSlideMaster({
    title: 'TECH_CONTENT',
    background: { color: colors.primary },
    objects: [
      // Neon accent bar (left)
      {
        rect: {
          x: 0,
          y: 0,
          w: 0.08,
          h: 7.5,
          fill: { color: colors.accent }
        }
      },
      // Title area with subtle glow
      {
        rect: {
          x: 0.3,
          y: 0.4,
          w: 9.4,
          h: 0.8,
          fill: { color: colors.secondary },
          line: { color: colors.accent, width: 1 }
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.5,
            y: 0.5,
            w: 9,
            h: 0.6,
            fontSize: 30,
            bold: true,
            color: colors.accent,
            fontFace: 'Arial'
          }
        }
      },
      // Corner accent
      {
        rect: {
          x: 9,
          y: 0.4,
          w: 0.7,
          h: 0.8,
          fill: { color: colors.accentSecondary }
        }
      }
    ],
    slideNumber: {
      x: 0.3,
      y: 7.1,
      fontSize: 10,
      color: colors.muted
    }
  });

  // Section Header - Full Neon Impact
  pptx.defineSlideMaster({
    title: 'TECH_SECTION',
    background: { color: colors.secondary },
    objects: [
      // Diagonal neon line
      {
        line: {
          x: 0,
          y: 3.75,
          w: 10,
          h: 0,
          line: { color: colors.accent, width: 4 }
        }
      },
      // Second accent line
      {
        line: {
          x: 0,
          y: 3.9,
          w: 10,
          h: 0,
          line: { color: colors.accentSecondary, width: 2, transparency: 60 }
        }
      },
      // Section title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 1,
            y: 2.5,
            w: 8,
            h: 1,
            fontSize: 48,
            bold: true,
            color: colors.text,
            align: 'left',
            valign: 'top',
            fontFace: 'Arial'
          }
        }
      }
    ]
  });

  return {
    name: 'Modern Tech',
    colors,
    chartColors: [colors.accent, colors.accentSecondary, '10B981', 'F59E0B', 'EF4444']
  };
}
```

## Template 8: Biological Sciences

**Scientific, natural, academic**

**Colors:**
- Primary: Deep Green `#1B5E20`
- Secondary: Teal `#00796B`
- Tertiary: Sky Blue `#0277BD`
- Accent: Amber `#FF6F00`
- Background: Off-White `#FAFAFA`
- Text: Dark Gray `#212121`

**Fonts:** Lato, Open Sans, Arial

**Best for:** Biology research, medical presentations, ecology, life sciences, academic conferences

**Key Features:** Natural color palette, scientific diagrams, cell/molecular imagery, professional academic look

```javascript
function createBiologicalSciencesTemplate(pptx, options = {}) {
  const colors = {
    primary: options.primaryColor || '1B5E20',
    secondary: options.secondaryColor || '00796B',
    tertiary: options.tertiaryColor || '0277BD',
    accent: options.accentColor || 'FF6F00',
    background: options.backgroundColor || 'FAFAFA',
    text: options.textColor || '212121'
  };

  const institution = options.institution || 'Research Institution';

  // Title Slide - Scientific
  pptx.defineSlideMaster({
    title: 'BIO_TITLE',
    background: { color: colors.background },
    objects: [
      // DNA helix-inspired decorative elements (circles)
      {
        ellipse: {
          x: 0.5,
          y: 1,
          w: 0.3,
          h: 0.3,
          fill: { color: colors.primary, transparency: 30 }
        }
      },
      {
        ellipse: {
          x: 1,
          y: 1.8,
          w: 0.3,
          h: 0.3,
          fill: { color: colors.secondary, transparency: 30 }
        }
      },
      {
        ellipse: {
          x: 0.7,
          y: 2.6,
          w: 0.3,
          h: 0.3,
          fill: { color: colors.tertiary, transparency: 30 }
        }
      },
      {
        ellipse: {
          x: 1.2,
          y: 3.4,
          w: 0.3,
          h: 0.3,
          fill: { color: colors.primary, transparency: 30 }
        }
      },
      // Right side elements
      {
        ellipse: {
          x: 9.2,
          y: 1.5,
          w: 0.3,
          h: 0.3,
          fill: { color: colors.tertiary, transparency: 30 }
        }
      },
      {
        ellipse: {
          x: 8.7,
          y: 2.3,
          w: 0.3,
          h: 0.3,
          fill: { color: colors.secondary, transparency: 30 }
        }
      },
      {
        ellipse: {
          x: 9.0,
          y: 3.1,
          w: 0.3,
          h: 0.3,
          fill: { color: colors.primary, transparency: 30 }
        }
      },
      // Header bar
      {
        rect: {
          x: 0,
          y: 0,
          w: 10,
          h: 0.5,
          fill: { color: colors.primary }
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 2,
            y: 2.5,
            w: 6,
            h: 1.5,
            fontSize: 40,
            bold: true,
            color: colors.primary,
            align: 'center',
            valign: 'middle',
            fontFace: 'Lato'
          },
          text: 'Research Presentation Title'
        }
      },
      // Subtitle
      {
        placeholder: {
          options: {
            name: 'subtitle',
            type: 'body',
            x: 2,
            y: 4.2,
            w: 6,
            h: 0.6,
            fontSize: 18,
            color: colors.secondary,
            align: 'center',
            fontFace: 'Lato'
          },
          text: 'Subtitle or Author Information'
        }
      },
      // Institution footer
      {
        rect: {
          x: 0,
          y: 7,
          w: 10,
          h: 0.5,
          fill: { color: colors.secondary }
        }
      },
      {
        text: {
          text: institution,
          options: {
            x: 0.5,
            y: 7.05,
            w: 9,
            h: 0.4,
            fontSize: 12,
            color: 'FFFFFF',
            align: 'center',
            valign: 'middle',
            fontFace: 'Lato'
          }
        }
      }
    ]
  });

  // Content Slide - Research Layout
  pptx.defineSlideMaster({
    title: 'BIO_CONTENT',
    background: { color: colors.background },
    objects: [
      // Color-coded sidebar
      {
        rect: {
          x: 0,
          y: 0,
          w: 0.25,
          h: 7.5,
          fill: { color: colors.primary }
        }
      },
      // Header section
      {
        rect: {
          x: 0.25,
          y: 0,
          w: 9.75,
          h: 0.9,
          fill: { color: colors.background },
          line: { color: colors.primary, width: 2, type: 'solid' }
        }
      },
      // Title
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.5,
            y: 0.2,
            w: 9,
            h: 0.5,
            fontSize: 26,
            bold: true,
            color: colors.primary,
            fontFace: 'Lato'
          }
        }
      },
      // Decorative molecule circles (small)
      {
        ellipse: {
          x: 9.3,
          y: 0.25,
          w: 0.15,
          h: 0.15,
          fill: { color: colors.secondary }
        }
      },
      {
        ellipse: {
          x: 9.5,
          y: 0.35,
          w: 0.15,
          h: 0.15,
          fill: { color: colors.tertiary }
        }
      },
      {
        ellipse: {
          x: 9.7,
          y: 0.45,
          w: 0.15,
          h: 0.15,
          fill: { color: colors.accent }
        }
      }
    ],
    slideNumber: {
      x: 9.3,
      y: 7.2,
      fontSize: 10,
      color: colors.text
    }
  });

  // Methods/Results Slide - Two Column
  pptx.defineSlideMaster({
    title: 'BIO_TWO_COLUMN',
    background: { color: colors.background },
    objects: [
      // Left column header
      {
        rect: {
          x: 0.5,
          y: 1.5,
          w: 4,
          h: 0.4,
          fill: { color: colors.secondary },
          line: { type: 'none' }
        }
      },
      {
        text: {
          text: 'METHODS',
          options: {
            x: 0.5,
            y: 1.5,
            w: 4,
            h: 0.4,
            fontSize: 14,
            bold: true,
            color: 'FFFFFF',
            align: 'center',
            valign: 'middle'
          }
        }
      },
      // Right column header
      {
        rect: {
          x: 5.5,
          y: 1.5,
          w: 4,
          h: 0.4,
          fill: { color: colors.tertiary },
          line: { type: 'none' }
        }
      },
      {
        text: {
          text: 'RESULTS',
          options: {
            x: 5.5,
            y: 1.5,
            w: 4,
            h: 0.4,
            fontSize: 14,
            bold: true,
            color: 'FFFFFF',
            align: 'center',
            valign: 'middle'
          }
        }
      },
      // Title at top
      {
        placeholder: {
          options: {
            name: 'title',
            type: 'title',
            x: 0.5,
            y: 0.5,
            w: 9,
            h: 0.6,
            fontSize: 28,
            bold: true,
            color: colors.primary,
            fontFace: 'Lato'
          }
        }
      }
    ]
  });

  return {
    name: 'Biological Sciences',
    colors,
    chartColors: [colors.primary, colors.secondary, colors.tertiary, colors.accent, '8BC34A']
  };
}
```

## Updated Template Selection Helper

```javascript
function selectTemplate(templateName, options = {}) {
  const templates = {
    'corporate-blue': createCorporateBlueTemplate,
    'modern-gradient': createModernGradientTemplate,
    'academic-classic': createAcademicClassicTemplate,
    'creative-pop': createCreativePopTemplate,
    'minimal-white': createMinimalWhiteTemplate,
    'neumorphic-soft-ui': createNeumorphicSoftUITemplate,
    'modern-tech': createModernTechTemplate,
    'biological-sciences': createBiologicalSciencesTemplate
  };

  return templates[templateName](pptx, options);
}

// Usage examples
const techTemplate = selectTemplate('modern-tech', {
  accentColor: '00D9FF',
  accentSecondary: 'A855F7'
});

const bioTemplate = selectTemplate('biological-sciences', {
  institution: 'Harvard Medical School',
  primaryColor: '1B5E20'
});

const neuTemplate = selectTemplate('neumorphic-soft-ui', {
  accentColor: '6B8EBF'
});
```
