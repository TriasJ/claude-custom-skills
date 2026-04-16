# Advanced Open-i Biomedical Image Search

## Overview

Open-i is the National Library of Medicine's biomedical image search engine that indexes images from PubMed Central and other medical image collections. The enhanced Open-i integration provides sophisticated filtering and retrieval capabilities.

## What is Open-i?

Open-i (https://openi.nlm.nih.gov/) provides:
- **Millions of biomedical images** from open-access literature
- **Rich metadata** including captions, abstracts, and MeSH terms
- **Multiple collections** (PMC, clinical images, MedPix)
- **Advanced filtering** by modality, specialty, and type
- **High-quality images** suitable for presentations

## Enhanced Features

Our advanced Open-i integration adds:

✅ **Modality Filtering**: CT, MRI, X-ray, ultrasound, PET, microscopy, etc.
✅ **Specialty Filtering**: Cardiology, neurology, oncology, psychiatry, etc.
✅ **Image Type Filtering**: Diagnostic, illustration, chart, photograph
✅ **Collection Filtering**: PMC, clinical images, MedPix, Indiana Network
✅ **Date Range Filtering**: Year-based publication filters
✅ **Metadata Export**: JSON/CSV formats
✅ **Library Generation**: Creates skill-compatible image_library.json

## Usage

### Basic Search

```bash
python scripts/openi_advanced_search.py \
  --query "brain MRI glioblastoma" \
  --max-results 10 \
  --download \
  --create-library
```

### Search with Modality Filter

```bash
# Find MRI images only
python scripts/openi_advanced_search.py \
  --query "brain tumor" \
  --modality mri \
  --max-results 15
```

### Search with Multiple Filters

```bash
# CT scans in oncology from recent years
python scripts/openi_advanced_search.py \
  --query "lung cancer staging" \
  --modality ct \
  --specialty oncology \
  --year-from 2020 \
  --download \
  --output ./lung_cancer_images
```

### Search for Illustrations/Diagrams

```bash
# Find diagrams and illustrations (not clinical images)
python scripts/openi_advanced_search.py \
  --query "TMS coil mechanism" \
  --image-type illustration \
  --max-results 10 \
  --download
```

## Available Filters

### Image Modalities

| Filter Code | Description |
|-------------|-------------|
| `ct` | CT Scan |
| `mri` | MRI |
| `xray` | X-Ray |
| `ultrasound` | Ultrasound |
| `pet` | PET Scan |
| `microscopy` | Microscopy |
| `photograph` | Clinical Photograph |
| `illustration` | Illustration/Diagram |
| `graph` | Graph/Chart |

**List all**: `python scripts/openi_advanced_search.py --list-modalities`

### Clinical Specialties

| Filter Code | Description |
|-------------|-------------|
| `cardiology` | Cardiology |
| `neurology` | Neurology |
| `oncology` | Oncology |
| `psychiatry` | Psychiatry |
| `radiology` | Radiology |
| `surgery` | Surgery |
| `pathology` | Pathology |
| `dermatology` | Dermatology |

**List all**: `python scripts/openi_advanced_search.py --list-specialties`

### Collections

| Filter Code | Description |
|-------------|-------------|
| `pmc` | PubMed Central |
| `clinical` | Clinical Images |
| `medpix` | MedPix Collection |
| `indiana` | Indiana Network |

### Image Types

Common values:
- `diagnostic` - Clinical diagnostic images
- `illustration` - Diagrams and illustrations
- `photograph` - Clinical photographs
- `chart` - Charts and graphs
- `microscopy` - Microscopy images

## Command-Line Options

### Required
- `--query`, `-q`: Search query string

### Search Options
- `--max-results`, `-n`: Maximum results (default: 20)
- `--sort`: Sort by `relevance` (default) or `date`

### Filter Options
- `--modality`, `-m`: Image modality (ct, mri, xray, etc.)
- `--specialty`, `-s`: Clinical specialty
- `--image-type`, `-t`: Type of image
- `--collection`, `-c`: Source collection
- `--year-from`: Start year for date range
- `--year-to`: End year for date range

### Output Options
- `--output`, `-o`: Output directory (default: ./openi_images)
- `--download`: Download images
- `--thumbnail`: Download thumbnails instead of full images
- `--create-library`: Create image_library.json
- `--export-metadata`: Export metadata as `json` or `csv`

## Examples by Use Case

### 1. Neuroimaging Research

```bash
# MRI images of brain tumors from last 5 years
python scripts/openi_advanced_search.py \
  --query "brain tumor MRI" \
  --modality mri \
  --specialty neurology \
  --year-from 2020 \
  --max-results 20 \
  --download \
  --create-library \
  --output ./brain_tumor_mri
```

### 2. Clinical Education

```bash
# Diagnostic images for cardiology residents
python scripts/openi_advanced_search.py \
  --query "myocardial infarction diagnosis" \
  --specialty cardiology \
  --image-type diagnostic \
  --max-results 15 \
  --download \
  --create-library
```

### 3. Mechanism Illustrations

```bash
# Diagrams for mechanism slides
python scripts/openi_advanced_search.py \
  --query "synaptic plasticity mechanism" \
  --image-type illustration \
  --max-results 10 \
  --download \
  --output ./mechanism_diagrams
```

### 4. Pathology Images

```bash
# Microscopy images for pathology presentation
python scripts/openi_advanced_search.py \
  --query "adenocarcinoma histology" \
  --modality microscopy \
  --specialty pathology \
  --max-results 20 \
  --download
```

### 5. Surgical Techniques

```bash
# Surgical procedure photographs
python scripts/openi_advanced_search.py \
  --query "laparoscopic cholecystectomy technique" \
  --specialty surgery \
  --image-type photograph \
  --max-results 10 \
  --download
```

### 6. Quick Browse (No Download)

```bash
# Just search and view metadata
python scripts/openi_advanced_search.py \
  --query "TMS coil types" \
  --max-results 10
```

## Output Structure

### Search Results Display

```
================================================================================
SEARCH RESULTS
================================================================================

1. Comparison of TMS coil configurations
   Article: Electric field depth-focality tradeoff in TMS
   Journal: Brain Stimulation (2013)
   Modality: illustration
   Type: figure
   PMCID: PMC3579268
   Caption: Figure showing different TMS coil designs and their electric...

2. H-coil penetration characteristics
   Article: Deep transcranial magnetic stimulation
   Journal: Clinical Neurophysiology (2014)
   ...
```

### Downloaded Files

```
openi_images/
├── openi_PMC3579268_Fig2.jpg
├── openi_PMC4123456_Fig1.jpg
├── openi_PMC5234567_Fig3A.jpg
├── image_library.json
└── openi_metadata.json
```

### Image Library Format

```json
{
  "image_id": "PMC3579268/Fig2",
  "filename": "openi_PMC3579268_Fig2.jpg",
  "path": "/full/path/to/openi_images/openi_PMC3579268_Fig2.jpg",
  "source_document": "PMC3579268.pdf",
  "document_title": "Electric field depth-focality tradeoff...",
  "caption": "Figure showing comparison of TMS coil configurations...",
  "modality": "illustration",
  "image_type": "figure",
  "keywords": ["TMS", "coil", "electric field"],
  "journal": "Brain Stimulation",
  "year": "2013",
  "collection": "pmc"
}
```

## Integration with Presentations

### In Workflow

```bash
# Step 1: Search and download images
python scripts/openi_advanced_search.py \
  --query "TMS coil types" \
  --modality illustration \
  --download \
  --create-library \
  --output ./tms_images

# Step 2: Use in presentation
# The generated image_library.json can be used with:
python scripts/image_sourcer.py \
  ./tms_images/image_library.json \
  "coil design" \
  --max-results 3
```

### Automatic Integration

When Claude creates presentations:

1. **Identify image needs** per subtopic
2. **Run Open-i search** with appropriate filters
3. **Download matched images**
4. **Insert in presentation** with proper citations

## Query Tips

### Effective Query Construction

**Good Queries**:
- Specific: "glioblastoma MRI FLAIR sequence"
- Technical: "figure-8 coil focality characteristics"
- Anatomical: "prefrontal cortex activation fMRI"

**Poor Queries**:
- Too broad: "brain"
- Too vague: "medical image"
- Non-specific: "disease"

### Using Filters Effectively

1. **Start broad, then filter**: Search first, then add modality/specialty
2. **Combine modality + specialty**: More targeted results
3. **Use date range for recent evidence**: `--year-from 2020`
4. **Image type for presentation style**: `illustration` vs `diagnostic`

## Advantages Over Simple Search

| Feature | Basic Search | Advanced Open-i |
|---------|--------------|-----------------|
| Modality filtering | ❌ | ✅ CT, MRI, X-ray, etc. |
| Specialty filtering | ❌ | ✅ By medical field |
| Image type selection | ❌ | ✅ Diagnostic vs illustration |
| Collection filtering | ❌ | ✅ PMC, clinical, MedPix |
| Date range | ❌ | ✅ Year-based filtering |
| Metadata export | ❌ | ✅ JSON/CSV export |
| Structured data | Basic | ✅ Rich metadata |

## Metadata Fields

Each image includes:

**Core Fields**:
- `uid`: Unique image identifier
- `title`: Image title
- `caption`: Full figure caption
- `image_url`: Full-size image URL
- `thumbnail_url`: Thumbnail URL

**Source Fields**:
- `pmcid`: PubMed Central ID
- `article_title`: Source article title
- `journal`: Publication journal
- `year`: Publication year
- `authors`: Article authors
- `abstract`: Article abstract (truncated)

**Classification Fields**:
- `image_type`: Type classification
- `modality`: Imaging modality
- `collection`: Source collection
- `mesh_terms`: Medical Subject Headings

## Rate Limiting

The script includes automatic rate limiting:
- 0.5 second delay between downloads
- Respects API limits
- Graceful error handling

## Error Handling

The script handles:
- Network errors
- Malformed responses
- Missing images
- API timeouts

Failed downloads are reported but don't stop the process.

## Best Practices

### 1. Use Specific Filters

```bash
# Better
--query "brain" --modality mri --specialty neurology

# Than
--query "brain MRI neurology"
```

Filters are more reliable than relying on text matching.

### 2. Download Selectively

Preview results first (no `--download`), then download with refined query.

### 3. Organize by Topic

```bash
# Separate directories per subtopic
--output ./coil_types
--output ./penetration_depth
--output ./clinical_protocols
```

### 4. Export Metadata

Always use `--export-metadata json` to keep searchable records.

### 5. Create Library

Use `--create-library` for integration with presentation workflow.

## Troubleshooting

### No Results Found

**Solutions**:
- Broaden query (remove specific terms)
- Remove some filters
- Try alternative terminology
- Check spelling of medical terms

### Images Not Downloading

**Solutions**:
- Check network connection
- Try `--thumbnail` for faster downloads
- Reduce `--max-results`
- Check output directory permissions

### Wrong Image Types

**Solutions**:
- Add `--image-type illustration` for diagrams
- Add `--modality` filter for specific imaging
- Refine query with more specific terms

## Comparison with Other Tools

### vs. pmc_contextual_fetcher.py

**Open-i Advanced Search**:
- ✅ Pre-indexed images (faster)
- ✅ Multiple collections beyond PMC
- ✅ Rich filtering options
- ❌ No contextual matching
- ❌ No relevance scoring per subtopic

**Contextual Fetcher**:
- ✅ Semantic matching to subtopics
- ✅ Relevance scoring
- ✅ Context-aware selection
- ❌ PMC only
- ❌ Slower (article-by-article)

**Use Open-i when**:
- Need specific modality (MRI, CT, etc.)
- Want illustrations/diagrams
- Need clinical photographs
- Speed is priority

**Use Contextual Fetcher when**:
- Have multiple distinct subtopics
- Need semantic matching
- Want relevance scoring
- Educational coherence is priority

### vs. pmc_image_fetcher.py

**Open-i Advanced** is superior:
- ✅ Pre-indexed (faster)
- ✅ Advanced filters
- ✅ Multiple collections
- ✅ Rich metadata
- ✅ Better structured data

## API Information

Based on Open-i API at https://openi.nlm.nih.gov/services

**Endpoint**: `https://openi.nlm.nih.gov/api/search`

**Parameters**:
- `query`: Search string
- `rows`: Number of results
- `start`: Pagination offset
- `sort`: relevance or date

**Response Format**: JSON with image metadata and URLs

## Summary

The enhanced Open-i integration provides:

1. **Powerful filtering** by modality, specialty, type, collection
2. **Fast results** from pre-indexed database
3. **Rich metadata** for proper citation
4. **Library generation** for workflow integration
5. **Export capabilities** for data management

Perfect for finding specific types of biomedical images quickly with proper filtering and organization.
