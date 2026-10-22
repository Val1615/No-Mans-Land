// A versioned module directory keeps one release's complete import graph together in browser caches.
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const root=new URL('../dist/',import.meta.url),html=fs.readFileSync(new URL('index.html',root),'utf8');
const directory=html.match(/src="(runtime-v\d+)\/app\.js"/)?.[1];if(!directory)throw Error('Versioned runtime entry missing from index.html');
const target=new URL(directory+'/',root);fs.mkdirSync(target,{recursive:true});const files={};
for(const name of fs.readdirSync(root).filter(name=>name.endsWith('.js'))){const data=fs.readFileSync(new URL(name,root));fs.writeFileSync(new URL(name,target),data);files[name]=createHash('sha256').update(data).digest('hex');}
fs.writeFileSync(new URL('manifest.json',target),JSON.stringify({directory,files},null,2)+'\n');console.log(`${directory}: ${Object.keys(files).length} modules packaged`);
