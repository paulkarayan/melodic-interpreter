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

  console.log('\nChecking DOM for full-tune elements...');
  const fullTuneElements = await page.$$('[id^="full-tune-"]');
  console.log('Found', fullTuneElements.length, 'full-tune elements');

  for (let i = 0; i < fullTuneElements.length; i++) {
    const id = await fullTuneElements[i].getAttribute('id');
    const innerHTML = await fullTuneElements[i].innerHTML();
    const hasContent = innerHTML.trim().length > 0;
    const boundingBox = await fullTuneElements[i].boundingBox();
    console.log(`  ${id}: ${hasContent ? 'HAS CONTENT' : 'EMPTY'} (${innerHTML.length} chars)`);
    console.log(`    BoundingBox: ${JSON.stringify(boundingBox)}`);

    // Check if SVG is inside
    const svgCount = await fullTuneElements[i].locator('svg').count();
    console.log(`    SVG elements: ${svgCount}`);
  }

  console.log('\nDone.');
  await browser.close();
})();
