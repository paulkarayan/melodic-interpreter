const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('http://localhost:8000/harmony.html');

  // Select simple_chord_changes from dropdown
  await page.selectOption('#harmony-select', 'simple_chord_changes');

  // Click Generate Transformation
  await page.click('button:has-text("Generate Transformation")');

  // Wait for response
  await page.waitForTimeout(3000);

  // Take screenshot
  await page.screenshot({ path: '/tmp/harmony-simple-chords-result.png', fullPage: true });

  // Check for errors
  const errorVisible = await page.locator('#error-output').isVisible();
  if (errorVisible) {
    const errorText = await page.locator('#error-message').textContent();
    console.log('ERROR:', errorText);
  }

  // Check console logs
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));

  await browser.close();
})();
