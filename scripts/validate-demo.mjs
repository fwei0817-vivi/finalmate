import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const htmlPath = path.join(root, 'skills', 'notes', 'examples', 'class_demo.html');
const html = await readFile(htmlPath, 'utf8');

const failures = [];

for (const placeholder of ['{{TITLE}}', '{{MD_CONTENT_JSON}}', '{{UI_LABELS_JSON}}']) {
  if (html.includes(placeholder)) failures.push(`Unreplaced placeholder: ${placeholder}`);
}

function getJsonScript(id) {
  const re = new RegExp(`<script[^>]+id="${id}"[^>]*>([\\s\\S]*?)<\\/script>`);
  const match = html.match(re);
  if (!match) {
    failures.push(`Missing JSON script: ${id}`);
    return null;
  }
  try {
    return JSON.parse(match[1]);
  } catch (err) {
    failures.push(`Invalid JSON in ${id}: ${err.message}`);
    return null;
  }
}

const markdown = getJsonScript('content-json');
getJsonScript('ui-labels-json');

if (typeof markdown === 'string') {
  for (const needle of ['```quiz', '```mermaid', '<!-- cheatsheet:start -->']) {
    if (!markdown.includes(needle)) failures.push(`Demo markdown missing ${needle}`);
  }
}

for (const needle of [
  'function getAssessState()',
  'saved.hash === sourceHash',
  'function sectionId(h3, index)',
  '[sourceHash, index, h2Text, h3Text]'
]) {
  if (!html.includes(needle)) failures.push(`Assessment state regression guard missing: ${needle}`);
}
if (html.includes('hashStr(h3Text).substring')) {
  failures.push('Assessment section ids are based only on H3 text');
}

const scriptRe = /<script(?![^>]+\bsrc=)(?![^>]+type="application\/json")[^>]*>([\s\S]*?)<\/script>/g;
let scriptIndex = 0;
for (const match of html.matchAll(scriptRe)) {
  scriptIndex += 1;
  try {
    new Function(match[1]);
  } catch (err) {
    failures.push(`Inline script ${scriptIndex} has a syntax error: ${err.message}`);
  }
}

if (failures.length) {
  console.error(failures.map(f => `- ${f}`).join('\n'));
  process.exit(1);
}

console.log('Demo validation passed');
