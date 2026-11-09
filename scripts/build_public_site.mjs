import {readdir, lstat, mkdir, copyFile, rm} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const projectRoot=fileURLToPath(new URL('../',import.meta.url));
const directories=['astrology','driving-school','downloads','regional','vikri','.well-known'];
const rootFiles=['index.html','404.html','_redirects','_headers','robots.txt','sitemap.xml'];
const privateExtensions=new Set(['.md','.py','.mjs','.map']);
const maximumFileSize=25*1024*1024;

export async function buildPublicSite(sourceRoot=projectRoot) {
  const root=path.resolve(sourceRoot);
  const output=path.resolve(root,'public');
  if(path.dirname(output)!==root) throw new Error('Invalid public output directory.');
  const files=[];
  async function collect(relative,required=false) {
    const source=path.join(root,relative);
    let entry;
    try { entry=await lstat(source); }
    catch(error) { if(error.code==='ENOENT'&&!required) return; throw error; }
    if(entry.isSymbolicLink()) throw new Error('Public files must not be symbolic links: '+relative);
    if(entry.isDirectory()) {
      for(const name of (await readdir(source)).sort()) {
        if(name.startsWith('.')||privateExtensions.has(path.extname(name))) continue;
        await collect(path.join(relative,name));
      }
    } else if(entry.isFile()) {
      if(entry.size>maximumFileSize) throw new Error('Public file exceeds the Pages 25 MiB limit: '+relative);
      files.push(relative);
    }
  }
  for(const name of rootFiles) await collect(name,['index.html','404.html','_redirects'].includes(name));
  for(const name of directories) await collect(name);
  try { if((await lstat(output)).isSymbolicLink()) throw new Error('Public output must not be a symbolic link.'); }
  catch(error) { if(error.code!=='ENOENT') throw error; }
  // The only removal target is the checked public directory inside this source root.
  await rm(output,{recursive:true,force:true});
  await mkdir(output,{recursive:true});
  for(const relative of files) {
    const target=path.join(output,relative);
    await mkdir(path.dirname(target),{recursive:true});
    await copyFile(path.join(root,relative),target);
  }
  return {output,files:files.map(name=>name.split(path.sep).join('/'))};
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  const result=await buildPublicSite();
  console.log(JSON.stringify({output:result.output,publicFiles:result.files.length}));
}
