const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  // Capture console messages
  page.on('console', msg => console.log('BROWSER:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));

  await page.goto('http://localhost:8000/harmony.html');

  // Select trick_chord_changes from dropdown
  await page.selectOption('#harmony-select', 'trick_chord_changes');

  // Click Generate Transformation
  await page.click('button:has-text("Generate Transformation")');

  // Wait for response (AI can take a while)
  console.log('Waiting for trick chord transformation...');
  await page.waitForTimeout(10000);

  // Take screenshot
  await page.screenshot({ path: '/tmp/harmony-trick-chords-result.png', fullPage: true });

  // Check for errors
  const errorVisible = await page.locator('#error-output').isVisible();
  if (errorVisible) {
    const errorText = await page.locator('#error-message').textContent();
    console.log('ERROR VISIBLE:', errorText);
  }

  // Check output section
  const outputVisible = await page.locator('#output-section').isVisible();
  console.log('Output section visible:', outputVisible);

  await browser.close();
})();
