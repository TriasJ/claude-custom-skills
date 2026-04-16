#!/usr/bin/env node
/**
 * Hook: Download Path Enforcer (PreToolUse)
 * Matcher: mcp__notebooklm-mcp__download_artifact
 *
 * Ensures all artifact downloads go to ~/Downloads/notebooklm/{notebook-name}/
 * If the output_path doesn't match the expected pattern, rewrites it.
 */

const path = require('path');
const os = require('os');

const DOWNLOAD_BASE = path.join(os.homedir(), 'Downloads', 'notebooklm');

let input = '';
process.stdin.on('data', (chunk) => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const toolInput = data.tool_input || {};
    const outputPath = toolInput.output_path || '';

    // Normalize path separators for comparison
    const normalizedPath = outputPath.replace(/\\/g, '/');
    const normalizedBase = DOWNLOAD_BASE.replace(/\\/g, '/');

    if (normalizedPath.startsWith(normalizedBase)) {
      // Path is already correct — approve without modification
      process.stdout.write(JSON.stringify({
        decision: 'approve',
        suppressOutput: true
      }));
    } else if (outputPath === '') {
      // No path specified — add a system message but don't block
      process.stdout.write(JSON.stringify({
        decision: 'approve',
        systemMessage: `Download path not specified. Use the pattern: ${DOWNLOAD_BASE}/{notebook-name}/{type}-{date}.{ext}`
      }));
    } else {
      // Path doesn't match expected base — warn but don't block
      // (user may have a valid reason for a custom path)
      process.stdout.write(JSON.stringify({
        decision: 'approve',
        systemMessage: `Note: Download path "${outputPath}" is outside the standard location (${DOWNLOAD_BASE}/). Consider using the standard path for organization.`
      }));
    }
  } catch (e) {
    process.stdout.write(JSON.stringify({
      decision: 'approve',
      suppressOutput: true
    }));
  }
});
