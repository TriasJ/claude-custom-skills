#!/usr/bin/env node
/**
 * Hook: Auth Health Check (PreToolUse)
 * Matcher: mcp__notebooklm-mcp__.*
 *
 * Lightweight check that reminds Claude to verify auth status
 * on the first NotebookLM MCP tool call in a session.
 * Does NOT block — only injects a systemMessage.
 * Skips auth tools to avoid recursion.
 */

const AUTH_TOOLS = [
  'mcp__notebooklm-mcp__refresh_auth',
  'mcp__notebooklm-mcp__save_auth_tokens',
  'mcp__notebooklm-mcp__server_info'
];

let input = '';
process.stdin.on('data', (chunk) => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const toolName = data.tool_name || '';

    // Skip auth tools to avoid recursion
    if (AUTH_TOOLS.includes(toolName)) {
      process.stdout.write(JSON.stringify({
        decision: 'approve',
        suppressOutput: true
      }));
      return;
    }

    // For all other NotebookLM MCP tools, add a gentle reminder
    process.stdout.write(JSON.stringify({
      decision: 'approve',
      systemMessage: 'NotebookLM MCP tool invoked. If you encounter auth errors (401/403), run refresh_auth() first, then retry. If that fails, instruct the user to run "nlm login" in their terminal.',
      suppressOutput: true
    }));
  } catch (e) {
    process.stdout.write(JSON.stringify({
      decision: 'approve',
      suppressOutput: true
    }));
  }
});
