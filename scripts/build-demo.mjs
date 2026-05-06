import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const skillDir = path.join(root, 'skills', 'notes');
const mdPath = path.join(skillDir, 'examples', 'class_demo.md');
const htmlPath = path.join(skillDir, 'examples', 'class_demo.html');
const templatePath = path.join(skillDir, 'template.html');

const markdown = await readFile(mdPath, 'utf8');
const template = await readFile(templatePath, 'utf8');
const titleMatch = markdown.match(/^#\s+(.+)$/m);
const title = titleMatch ? titleMatch[1].trim() : 'Study Notes Demo';
const labels = {};

const html = template
  .replaceAll('{{TITLE}}', title)
  .replace('{{MD_CONTENT_JSON}}', JSON.stringify(markdown).replace(/<\//g, '<\\/'))
  .replace('{{UI_LABELS_JSON}}', JSON.stringify(labels).replace(/<\//g, '<\\/'));

await writeFile(htmlPath, html);
console.log(`Wrote ${path.relative(root, htmlPath)}`);

