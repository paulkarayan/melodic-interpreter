const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  page.on('console', msg => console.log('BROWSER:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

  await page.goto('http://localhost:8000/reharmonize.html');

  // Click Analyze button
  await page.click('button:has-text("Analyze Chords")');

  console.log('Waiting for analysis...');
  await page.waitForTimeout(3000);

  // Take screenshot
  await page.screenshot({ path: '/tmp/reharmonize-result.png', fullPage: true });

  // Check for errors
  const errorVisible = await page.locator('#error-output').isVisible();
  if (errorVisible) {
    const errorText = await page.locator('#error-message').textContent();
    console.log('ERROR:', errorText);
  }

  // Check output section
  const outputVisible = await page.locator('#output-section').isVisible();
  console.log('Output visible:', outputVisible);

  await browser.close();
})();
