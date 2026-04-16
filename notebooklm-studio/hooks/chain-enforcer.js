#!/usr/bin/env node
/**
 * Hook: Chain Enforcer (PostToolUse)
 * Matcher: mcp__notebooklm-mcp__studio_create
 *
 * After studio_create completes, injects a systemMessage reminding Claude
 * to follow the complete create -> poll -> download chain.
 */

let input = '';
process.stdin.on('data', (chunk) => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const toolOutput = data.tool_output || '';
    const toolInput = data.tool_input || {};
    const artifactType = toolInput.artifact_type || 'artifact';
    const notebookId = toolInput.notebook_id || '';

    // Check if creation was successful (output should contain success indicators)
    const outputStr = typeof toolOutput === 'string' ? toolOutput : JSON.stringify(toolOutput);
    const isSuccess = !outputStr.toLowerCase().includes('error') && !outputStr.toLowerCase().includes('failed');

    if (isSuccess) {
      process.stdout.write(JSON.stringify({
        systemMessage: [
          `Artifact creation initiated (type: ${artifactType}, notebook: ${notebookId}).`,
          'You MUST now complete the chain:',
          `1. Poll: studio_status(notebook_id="${notebookId}") — repeat every 30s until status is "completed" or "failed"`,
          '2. If completed: download_artifact() to ~/Downloads/notebooklm/{notebook-name}/{type}-{date}.{ext}',
          '3. If failed: retry ONCE with identical parameters. If second attempt fails, report the error.',
          'Do NOT skip any step. Do NOT stop without downloading the completed artifact.'
        ].join('\n')
      }));
    } else {
      process.stdout.write(JSON.stringify({
        systemMessage: [
          `Studio creation may have failed for ${artifactType}.`,
          'Check studio_status to confirm. If failed, retry ONCE with the same parameters.',
          'If second attempt also fails, report the error to the user with troubleshooting steps.'
        ].join('\n')
      }));
    }
  } catch (e) {
    // Parse error — still inject chain reminder
    process.stdout.write(JSON.stringify({
      systemMessage: 'Studio artifact created. Remember: poll studio_status until complete, then download_artifact.'
    }));
  }
});
