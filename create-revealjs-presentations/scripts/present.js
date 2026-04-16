#!/usr/bin/env node
/**
 * Reveal.js Presentation Launcher
 *
 * Starts a local HTTP server and opens the presentation in browser.
 * Press 'S' in the presentation to open Speaker View.
 *
 * Usage: node present.js [port] [filename]
 * Default: port 8000, filename index.html
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const PORT = process.argv[2] || 8000;
const HOSTNAME = 'localhost';
const DEFAULT_FILE = process.argv[3] || 'index.html';

// MIME types mapping
const mimeTypes = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.eot': 'application/vnd.ms-fontobject',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.mp3': 'audio/mpeg',
  '.wav': 'audio/wav',
  '.glb': 'model/gltf-binary',
  '.gltf': 'model/gltf+json'
};

// Create HTTP server
const server = http.createServer((req, res) => {
  let filePath = '.' + decodeURIComponent(req.url);
  if (filePath === './') filePath = './' + DEFAULT_FILE;

  const extname = path.extname(filePath).toLowerCase();
  const contentType = mimeTypes[extname] || 'application/octet-stream';

  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end(`<h1>404 Not Found</h1><p>File: ${filePath}</p>`, 'utf-8');
      } else {
        res.writeHead(500);
        res.end('Server error: ' + error.code, 'utf-8');
      }
    } else {
      res.writeHead(200, {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*'
      });
      res.end(content, 'utf-8');
    }
  });
});

// Start server
server.listen(PORT, HOSTNAME, () => {
  const url = `http://${HOSTNAME}:${PORT}`;

  console.log(`
╔════════════════════════════════════════════════════════════╗
║           Reveal.js Presentation Server                    ║
╠════════════════════════════════════════════════════════════╣
║  Server running at: ${url.padEnd(36)} ║
║                                                            ║
║  Opening presentation in browser...                        ║
║                                                            ║
║  PRESENTER VIEW: Press 'S' key in the presentation         ║
║                                                            ║
║  TIP: Put speaker view on laptop, presentation on          ║
║       external display/projector                           ║
║                                                            ║
║  Keyboard Shortcuts:                                       ║
║    S - Speaker view    F - Fullscreen    O - Overview      ║
║    Arrow keys - Navigate    ESC - Exit                     ║
║                                                            ║
║  Press Ctrl+C to stop the server                           ║
╚════════════════════════════════════════════════════════════╝
`);

  // Open browser automatically
  const platform = process.platform;
  let command;

  if (platform === 'win32') {
    command = `start "" "${url}"`;
  } else if (platform === 'darwin') {
    command = `open "${url}"`;
  } else {
    command = `xdg-open "${url}"`;
  }

  exec(command, (error) => {
    if (error) {
      console.log(`Could not auto-open browser. Please visit: ${url}`);
    }
  });
});

// Handle server errors
server.on('error', (error) => {
  if (error.code === 'EADDRINUSE') {
    console.error(`Port ${PORT} is already in use. Try: node present.js ${parseInt(PORT) + 1}`);
  } else {
    console.error('Server error:', error);
  }
  process.exit(1);
});
