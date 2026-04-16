# MinerU Troubleshooting Guide

## Table of Contents
- [Installation Issues](#installation-issues)
- [Model Download Problems](#model-download-problems)
- [Runtime Errors](#runtime-errors)
- [Output Quality Issues](#output-quality-issues)
- [Performance Optimization](#performance-optimization)

---

## Installation Issues

### "mineru command not found"
**Cause**: MinerU not in PATH or not installed correctly.

**Solution**:
```powershell
# Verify installation
pip show mineru

# Reinstall if needed
pip install -U "mineru[all]"

# Check scripts directory in PATH
$env:PATH -split ";" | Select-String "Scripts"
```

### Dependency Conflicts
**Cause**: Conflicting package versions with other installed packages.

**Solution**:
```bash
# Use virtual environment
python -m venv mineru_env
mineru_env\Scripts\activate
pip install "mineru[all]"
```

### CUDA/GPU Not Detected
**Cause**: CUDA toolkit not installed or version mismatch.

**Solution**:
```powershell
# Check CUDA
nvidia-smi

# Use CPU mode instead
mineru -p doc.pdf -o ./output -b pipeline -d cpu
```

---

## Model Download Problems

### Download Fails or Hangs
**Cause**: Network issues, firewall, or HuggingFace rate limits.

**Solutions**:

1. **Use ModelScope instead**:
```powershell
$env:MINERU_MODEL_SOURCE = "modelscope"
mineru-models-download
```

2. **Retry with proxy**:
```powershell
$env:HTTP_PROXY = "http://proxy:port"
$env:HTTPS_PROXY = "http://proxy:port"
mineru-models-download
```

3. **Manual download**: Download models manually from HuggingFace and configure `mineru.json`.

### "Model not found" Error
**Cause**: Models not downloaded or path misconfigured.

**Solution**:
```bash
# Re-download models
mineru-models-download

# Check mineru.json in home directory
type %USERPROFILE%\mineru.json
```

### Insufficient Disk Space
**Cause**: Models require ~5-10GB of space.

**Solution**: Free up disk space or specify custom model directory in `mineru.json`.

---

## Runtime Errors

### "CUDA out of memory"
**Cause**: PDF too large or VRAM insufficient.

**Solutions**:
```bash
# Limit VRAM usage
mineru -p doc.pdf -o ./output -b pipeline --vram 2048

# Use CPU instead
mineru -p doc.pdf -o ./output -b pipeline -d cpu

# Process fewer pages at a time
mineru -p doc.pdf -o ./output -s 0 -e 10
```

### "Killed" or Process Terminates
**Cause**: Out of RAM memory.

**Solutions**:
- Close other applications
- Process document in smaller chunks
- Use remote backend (http-client)

### Empty Output / No Markdown Generated
**Cause**: PDF might be encrypted, corrupted, or image-only without OCR.

**Solutions**:
```bash
# Force OCR method
mineru -p doc.pdf -o ./output -m ocr

# Check if PDF is encrypted
# Use pdf decryption tool first
```

### Unicode/Encoding Errors
**Cause**: Special characters in file paths.

**Solution**: Use paths without special characters or unicode.

---

## Output Quality Issues

### Text Garbled or Wrong Characters
**Cause**: Wrong language setting or OCR needed.

**Solutions**:
```bash
# Specify correct language
mineru -p doc.pdf -o ./output -l en

# Force OCR for scanned documents
mineru -p doc.pdf -o ./output -m ocr -l en
```

### Tables Not Formatted Correctly
**Cause**: Complex table structure or table parsing disabled.

**Solutions**:
```bash
# Ensure table parsing enabled
mineru -p doc.pdf -o ./output -t true

# Use hybrid backend for better accuracy
mineru -p doc.pdf -o ./output -b hybrid-auto-engine
```

### Formulas Not Extracted
**Cause**: Formula parsing disabled or backend doesn't support it.

**Solutions**:
```bash
# Enable formula parsing
mineru -p doc.pdf -o ./output -f true

# Use hybrid backend
mineru -p doc.pdf -o ./output -b hybrid-auto-engine
```

### Images Missing or Low Quality
**Cause**: Images embedded in unusual format.

**Solution**: Check `images/` folder in output. If missing, the PDF may have embedded images in unsupported format.

### Layout Issues
**Cause**: Complex multi-column or unusual layouts.

**Solution**: Use VLM backend for better layout understanding:
```bash
mineru -p doc.pdf -o ./output -b vlm-auto-engine
```

---

## Performance Optimization

### Speed Up Processing

1. **Use GPU**:
```bash
mineru -p doc.pdf -o ./output -b pipeline -d cuda:0
```

2. **Disable unused features**:
```bash
# Skip formulas if not needed
mineru -p doc.pdf -o ./output -f false

# Skip tables if not needed
mineru -p doc.pdf -o ./output -t false
```

3. **Process specific pages only**:
```bash
mineru -p doc.pdf -o ./output -s 0 -e 50
```

### Reduce Memory Usage

1. **Limit VRAM**:
```bash
mineru -p doc.pdf -o ./output --vram 2048
```

2. **Use pipeline backend** (more memory efficient):
```bash
mineru -p doc.pdf -o ./output -b pipeline
```

3. **Process in batches**: Split large PDFs and process sequentially.

---

## Quick Diagnostic Commands

```powershell
# Check MinerU version
mineru --version

# Check GPU status
nvidia-smi

# Check model configuration
type $env:USERPROFILE\mineru.json

# Test with simple PDF
mineru -p test.pdf -o ./test_output -b pipeline -d cpu
```
