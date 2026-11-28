// Writes tools/texts.json: every name, fact, molecule and home item the app can speak,
// keyed exactly as the app looks up audio clips (e.g. "name/ru/8").
// Usage: node tools/export_texts.mjs
import {readFileSync,writeFileSync} from 'node:fs';
const dir=new URL('..',import.meta.url);
const html=readFileSync(new URL('app.html',dir),'utf8');
const data=html.slice(html.indexOf('/*DATA*/'),html.indexOf('/*ENDDATA*/'));
const texts=new Function(data+';return allTexts()')();
writeFileSync(new URL('tools/texts.json',dir),JSON.stringify(texts,null,1));
console.log(Object.keys(texts).length+' texts written to tools/texts.json');
