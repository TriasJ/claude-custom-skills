<batch_processing>
<objective>
Process large knowledge bases efficiently with parallel processing, progress tracking, and error handling.
</objective>

<batch_processor>
```python
import asyncio
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Optional
import logging

@dataclass
class ProcessingResult:
    """Result of processing a single file or batch."""
    source: str
    success: bool
    output_path: Optional[str] = None
    error: Optional[str] = None
    stats: Optional[dict] = None

class BatchProcessor:
    """Process multiple knowledge base files efficiently."""

    def __init__(self, max_workers: int = 4, chunk_size: int = 10):
        self.max_workers = max_workers
        self.chunk_size = chunk_size
        self.logger = logging.getLogger(__name__)

    def process_directory(
        self,
        input_dir: str,
        output_dir: str,
        extensions: List[str] = None,
        recursive: bool = True
    ) -> List[ProcessingResult]:
        """Process all matching files in directory."""
        if extensions is None:
            extensions = ['.md', '.txt', '.rst']

        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Gather files
        files = []
        for ext in extensions:
            pattern = f'**/*{ext}' if recursive else f'*{ext}'
            files.extend(input_path.glob(pattern))

        self.logger.info(f"Found {len(files)} files to process")

        # Process in batches
        results = []
        for i in range(0, len(files), self.chunk_size):
            chunk = files[i:i + self.chunk_size]
            chunk_results = self._process_chunk(chunk, output_path)
            results.extend(chunk_results)

            # Progress update
            processed = min(i + self.chunk_size, len(files))
            self.logger.info(f"Processed {processed}/{len(files)} files")

        return results

    def _process_chunk(
        self,
        files: List[Path],
        output_dir: Path
    ) -> List[ProcessingResult]:
        """Process a chunk of files in parallel."""
        results = []

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    self._process_single_file,
                    f,
                    output_dir
                ): f for f in files
            }

            for future in as_completed(futures):
                source_file = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(ProcessingResult(
                        source=str(source_file),
                        success=False,
                        error=str(e)
                    ))

        return results

    def _process_single_file(
        self,
        file_path: Path,
        output_dir: Path
    ) -> ProcessingResult:
        """Process a single file to XML."""
        try:
            # Read content
            content = file_path.read_text(encoding='utf-8')

            # Detect type and convert
            doc_type = detect_document_type([{'content': content}])
            structure = extract_structure([{'content': content, 'path': str(file_path)}], doc_type)
            xml_output = generate_xml(structure, doc_type)

            # Write output
            output_file = output_dir / f"{file_path.stem}.xml"
            output_file.write_text(xml_output, encoding='utf-8')

            return ProcessingResult(
                source=str(file_path),
                success=True,
                output_path=str(output_file),
                stats={
                    'input_size': len(content),
                    'output_size': len(xml_output),
                    'doc_type': doc_type
                }
            )

        except Exception as e:
            return ProcessingResult(
                source=str(file_path),
                success=False,
                error=str(e)
            )
```
</batch_processor>

<grouped_processing>
Process related files together (e.g., all slides of a presentation):

```python
def process_grouped_files(
    input_dir: str,
    output_dir: str,
    group_by: str = 'directory'
) -> List[ProcessingResult]:
    """Process files in groups for better synthesis."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Group files
    if group_by == 'directory':
        groups = group_by_directory(input_path)
    elif group_by == 'prefix':
        groups = group_by_filename_prefix(input_path)
    elif group_by == 'pattern':
        groups = group_by_pattern(input_path)
    else:
        groups = {'all': list(input_path.rglob('*.*'))}

    results = []
    for group_name, files in groups.items():
        result = process_file_group(files, output_path, group_name)
        results.append(result)

    return results

def group_by_directory(root: Path) -> dict:
    """Group files by their parent directory."""
    groups = {}
    for file in root.rglob('*'):
        if file.is_file() and file.suffix in ['.md', '.txt', '.rst']:
            dir_name = file.parent.name
            if dir_name not in groups:
                groups[dir_name] = []
            groups[dir_name].append(file)
    return groups

def group_by_filename_prefix(root: Path) -> dict:
    """Group files by common prefix (e.g., 'chapter-01', 'chapter-02')."""
    import re
    groups = {}

    for file in root.rglob('*'):
        if file.is_file():
            # Extract prefix (letters before numbers)
            match = re.match(r'^([a-zA-Z-]+)', file.stem)
            if match:
                prefix = match.group(1).rstrip('-')
                if prefix not in groups:
                    groups[prefix] = []
                groups[prefix].append(file)

    return groups

def process_file_group(
    files: List[Path],
    output_dir: Path,
    group_name: str
) -> ProcessingResult:
    """Process a group of related files into single XML."""
    try:
        # Read all files in group
        file_contents = []
        for f in sorted(files):
            content = f.read_text(encoding='utf-8')
            file_contents.append({
                'path': str(f),
                'name': f.name,
                'content': content
            })

        # Detect type from combined content
        doc_type = detect_document_type(file_contents)

        # Extract and synthesize
        structure = extract_structure(file_contents, doc_type)
        synthesized = synthesize_content(structure)

        # Generate combined XML
        xml_output = generate_xml(synthesized, doc_type)

        # Write output
        output_file = output_dir / f"{group_name}.xml"
        output_file.write_text(xml_output, encoding='utf-8')

        return ProcessingResult(
            source=group_name,
            success=True,
            output_path=str(output_file),
            stats={
                'file_count': len(files),
                'doc_type': doc_type
            }
        )

    except Exception as e:
        return ProcessingResult(
            source=group_name,
            success=False,
            error=str(e)
        )
```
</grouped_processing>

<progress_tracking>
```python
from tqdm import tqdm
from datetime import datetime
import json

class ProgressTracker:
    """Track and report batch processing progress."""

    def __init__(self, total: int, log_file: str = None):
        self.total = total
        self.processed = 0
        self.succeeded = 0
        self.failed = 0
        self.start_time = datetime.now()
        self.log_file = log_file
        self.progress_bar = tqdm(total=total, desc="Processing")

    def update(self, result: ProcessingResult):
        """Update progress with result."""
        self.processed += 1
        if result.success:
            self.succeeded += 1
        else:
            self.failed += 1

        self.progress_bar.update(1)

        if self.log_file:
            self._log_result(result)

    def _log_result(self, result: ProcessingResult):
        """Log result to file."""
        with open(self.log_file, 'a') as f:
            f.write(json.dumps({
                'timestamp': datetime.now().isoformat(),
                'source': result.source,
                'success': result.success,
                'output': result.output_path,
                'error': result.error
            }) + '\n')

    def summary(self) -> dict:
        """Get processing summary."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return {
            'total': self.total,
            'processed': self.processed,
            'succeeded': self.succeeded,
            'failed': self.failed,
            'success_rate': self.succeeded / max(self.processed, 1),
            'elapsed_seconds': elapsed,
            'files_per_second': self.processed / max(elapsed, 1)
        }

    def close(self):
        """Close progress bar and print summary."""
        self.progress_bar.close()
        summary = self.summary()
        print(f"\nProcessing complete:")
        print(f"  Succeeded: {summary['succeeded']}/{summary['total']}")
        print(f"  Failed: {summary['failed']}")
        print(f"  Time: {summary['elapsed_seconds']:.1f}s")
        print(f"  Rate: {summary['files_per_second']:.1f} files/sec")
```
</progress_tracking>

<error_recovery>
```python
class RecoverableBatchProcessor(BatchProcessor):
    """Batch processor with checkpoint and recovery support."""

    def __init__(self, checkpoint_file: str = '.batch_checkpoint.json', **kwargs):
        super().__init__(**kwargs)
        self.checkpoint_file = checkpoint_file

    def process_with_recovery(
        self,
        input_dir: str,
        output_dir: str,
        **kwargs
    ) -> List[ProcessingResult]:
        """Process with automatic checkpoint and recovery."""
        # Load checkpoint if exists
        completed = self._load_checkpoint()

        # Get all files
        all_files = self._gather_files(input_dir, **kwargs)

        # Filter out completed
        pending = [f for f in all_files if str(f) not in completed]

        self.logger.info(f"Resuming: {len(completed)} done, {len(pending)} pending")

        results = []
        for file in pending:
            result = self._process_single_file(file, Path(output_dir))
            results.append(result)

            # Save checkpoint after each file
            completed.add(str(file))
            self._save_checkpoint(completed)

        # Clean up checkpoint on success
        if all(r.success for r in results):
            self._clear_checkpoint()

        return results

    def _load_checkpoint(self) -> set:
        """Load completed files from checkpoint."""
        try:
            with open(self.checkpoint_file, 'r') as f:
                data = json.load(f)
                return set(data.get('completed', []))
        except FileNotFoundError:
            return set()

    def _save_checkpoint(self, completed: set):
        """Save checkpoint."""
        with open(self.checkpoint_file, 'w') as f:
            json.dump({'completed': list(completed)}, f)

    def _clear_checkpoint(self):
        """Remove checkpoint file."""
        Path(self.checkpoint_file).unlink(missing_ok=True)
```
</error_recovery>

<memory_efficient_processing>
For very large files that don't fit in memory:

```python
def process_large_file_streaming(
    input_path: str,
    output_path: str,
    chunk_lines: int = 1000
) -> ProcessingResult:
    """Process large file in streaming chunks."""
    from lxml.etree import Element, SubElement, tostring

    root = Element('knowledge-base')
    root.set('type', 'large-document')
    content = SubElement(root, 'content')

    current_section = None
    line_buffer = []

    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            # Detect section boundaries
            if is_section_header(line):
                # Flush buffer to current section
                if current_section is not None and line_buffer:
                    body = SubElement(current_section, 'body')
                    body.text = '\n'.join(line_buffer)
                    line_buffer = []

                # Start new section
                current_section = SubElement(content, 'section')
                current_section.set('id', f'sec-{line_num}')
                heading = SubElement(current_section, 'heading')
                heading.text = line.strip()
            else:
                line_buffer.append(line.rstrip())

            # Periodic flush for memory management
            if len(line_buffer) >= chunk_lines:
                if current_section is not None:
                    body = current_section.find('body')
                    if body is None:
                        body = SubElement(current_section, 'body')
                        body.text = ''
                    body.text += '\n'.join(line_buffer) + '\n'
                    line_buffer = []

    # Final flush
    if current_section is not None and line_buffer:
        body = current_section.find('body')
        if body is None:
            body = SubElement(current_section, 'body')
            body.text = ''
        body.text += '\n'.join(line_buffer)

    # Write output
    with open(output_path, 'wb') as f:
        f.write(tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

    return ProcessingResult(
        source=input_path,
        success=True,
        output_path=output_path
    )
```
</memory_efficient_processing>

<cli_interface>
```python
#!/usr/bin/env python3
"""CLI for batch knowledge base conversion."""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Convert knowledge bases to structured XML'
    )
    parser.add_argument('input', help='Input file or directory')
    parser.add_argument('output', help='Output directory')
    parser.add_argument('--recursive', '-r', action='store_true',
                        help='Process directories recursively')
    parser.add_argument('--workers', '-w', type=int, default=4,
                        help='Number of parallel workers')
    parser.add_argument('--group-by', choices=['directory', 'prefix', 'none'],
                        default='none', help='How to group related files')
    parser.add_argument('--resume', action='store_true',
                        help='Resume from checkpoint')
    parser.add_argument('--log', help='Log file path')
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()

    # Configure logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Run processor
    if args.resume:
        processor = RecoverableBatchProcessor(max_workers=args.workers)
        results = processor.process_with_recovery(args.input, args.output)
    elif args.group_by != 'none':
        results = process_grouped_files(args.input, args.output, args.group_by)
    else:
        processor = BatchProcessor(max_workers=args.workers)
        results = processor.process_directory(
            args.input, args.output, recursive=args.recursive
        )

    # Report results
    succeeded = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)

    print(f"\nResults: {succeeded} succeeded, {failed} failed")

    if failed > 0:
        print("\nFailed files:")
        for r in results:
            if not r.success:
                print(f"  {r.source}: {r.error}")
        sys.exit(1)

if __name__ == '__main__':
    main()
```
</cli_interface>
</batch_processing>
