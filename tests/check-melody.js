const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Listen for console messages - capture all args
  page.on('console', msg => {
    const type = msg.type();
    const text = msg.text();
    console.log(`[${type.toUpperCase()}]`, text);
  });

  page.on('pageerror', error => {
    console.log('[PAGE ERROR]', error.message);
    console.log(error.stack);
  });

  console.log('Loading page...');
  const response = await page.goto('http://localhost:8000/melody.html');
  console.log('Response status:', response.status());
  await page.waitForLoadState('networkidle');

  console.log('\nPage title:', await page.title());
  console.log('Page URL:', page.url());

  // Check if button exists
  const buttonExists = await page.locator('button:has-text("Generate Variation")').count();
  console.log('Generate button exists:', buttonExists > 0);

  if (buttonExists === 0) {
    console.log('\nPage content snippet:');
    const bodyText = await page.locator('body').textContent();
    console.log(bodyText.substring(0, 500));
    await page.screenshot({ path: '/tmp/melody-error.png', fullPage: true });
    console.log('Saved error screenshot to /tmp/melody-error.png');
    await browser.close();
    return;
  }

  console.log('\nClicking Generate Variation...');
  await page.click('button:has-text("Generate Variation")');

  // Wait for the variation to render
  await page.waitForTimeout(8000);

  console.log('\nTaking screenshot...');
  await page.screenshot({ path: '/tmp/melody-with-variation.png', fullPage: true });

  console.log('\nChecking variations...');

  // Get all variation sections
  const variations = await page.$$('.variation');
  console.log('Found', variations.length, 'variation sections');

  for (let i = 0; i < Math.min(3, variations.length); i++) {
    const variation = variations[i];

    // Get the description
    const descText = await variation.$eval('.description', el => el.textContent);
    console.log(`\nVariation ${i + 1}: ${descText}`);

    // Take a focused screenshot of this variation
    const bbox = await variation.boundingBox();
    if (bbox) {
      await page.screenshot({
        path: `/tmp/variation-${i + 1}.png`,
        clip: {
          x: bbox.x,
          y: bbox.y,
          width: Math.min(bbox.width, 1200),
          height: Math.min(bbox.height, 800)
        }
      });
      console.log(`  Screenshot saved to /tmp/variation-${i + 1}.png`);
    }

    // Check for highlighted bars in full tune
    const svg = await variation.$('svg');
    if (svg) {
      // Count yellow rectangles
      const rects = await variation.$$eval('rect[fill="#ffeb3b"]', rects => rects.length);
      console.log(`  Yellow highlight rectangles: ${rects}`);

      // Check for "Varied" text
      const variedTexts = await variation.$$eval('text', texts =>
        texts.filter(t => t.textContent.includes('Varied')).length
      );
      console.log(`  "Varied" text elements: ${variedTexts}`);
    }
  }

  console.log('\nDone.');
  await browser.close();
})();
