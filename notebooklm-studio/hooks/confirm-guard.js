#!/usr/bin/env node
/**
 * Hook: Confirm Guard (PreToolUse)
 * Matcher: mcp__notebooklm-mcp__studio_create|mcp__notebooklm-mcp__notebook_delete|mcp__notebooklm-mcp__source_delete|mcp__notebooklm-mcp__studio_delete
 *
 * Ensures destructive/creation operations have confirm=True and warns
 * Claude to get user confirmation before proceeding.
 */

const DESTRUCTIVE_TOOLS = [
  'mcp__notebooklm-mcp__notebook_delete',
  'mcp__notebooklm-mcp__source_delete',
  'mcp__notebooklm-mcp__studio_delete'
];

let input = '';
process.stdin.on('data', (chunk) => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const toolName = data.tool_name || '';
    const toolInput = data.tool_input || {};
    const isDestructive = DESTRUCTIVE_TOOLS.includes(toolName);
    const isStudioCreate = toolName === 'mcp__notebooklm-mcp__studio_create';

    // Check if confirm is properly set
    if (toolInput.confirm === true) {
      // Confirm is set — approve
      process.stdout.write(JSON.stringify({
        decision: 'approve',
        reason: 'confirm=True is set, proceeding.',
        suppressOutput: true
      }));
    } else if (isDestructive) {
      // Destructive operation without confirm — block
      process.stdout.write(JSON.stringify({
        decision: 'block',
        reason: `BLOCKED: ${toolName} requires confirm=True. You MUST get explicit user confirmation before setting confirm=True on destructive operations (delete).`
      }));
    } else if (isStudioCreate) {
      // Studio create without confirm — remind
      process.stdout.write(JSON.stringify({
        decision: 'block',
        reason: 'BLOCKED: studio_create requires confirm=True. Ask the user to confirm the artifact type and settings before proceeding.'
      }));
    } else {
      // Unknown tool matched — approve by default
      process.stdout.write(JSON.stringify({
        decision: 'approve',
        suppressOutput: true
      }));
    }
  } catch (e) {
    // Parse error — don't block
    process.stdout.write(JSON.stringify({
      decision: 'approve',
      suppressOutput: true
    }));
  }
});
