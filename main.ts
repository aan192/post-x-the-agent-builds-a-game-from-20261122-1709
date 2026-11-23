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

  // Read the copied POST.json back and make sure the post URL it carries is
  // a real X/Twitter status address before this entry goes anywhere.
  const copied = JSON.parse(fs.readFileSync(destPath, 'utf8'));
  const postUrl = typeof copied.url === 'string' ? copied.url.trim() : '';
  const statusPattern = /^https?:\/\/(www\.)?(x\.com|twitter\.com)\/[^/]+\/status\/\d+([/?#].*)?$/;
  if (!statusPattern.test(postUrl)) {
    throw new Error(`POST.json post URL is missing or malformed: ${JSON.stringify(copied.url)}`);
  }
  console.log(`Verified X post URL: ${postUrl}`);

  console.log(`Successfully copied POST.json to ${destPath}`);
}

main();
