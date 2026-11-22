import * as fs from 'fs';
import * as path from 'path';

function main() {
  const botDir = process.env.MAKEFUN_BOT_DIR || '/bot';
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';

  const srcPath = path.join(botDir, 'POST.json');
  const destPath = path.join(outputDir, 'POST.json');

  if (!fs.existsSync(botDir)) {
    fs.mkdirSync(botDir, { recursive: true });
  }
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  if (fs.existsSync(srcPath)) {
    fs.copyFileSync(srcPath, destPath);
  } else {
    // Fallback default POST.json if not present in botDir
    const defaultPost = { url: "" };
    fs.writeFileSync(destPath, JSON.stringify(defaultPost, null, 2));
  }

  console.log(`Successfully copied POST.json to ${destPath}`);
}

main();
