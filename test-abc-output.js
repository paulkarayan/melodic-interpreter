const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  let transformedAbc = '';

  page.on('console', msg => {
    const text = msg.text();
    if (text.includes('transformed_abc:')) {
      console.log('FULL RESPONSE:', text);
    }
  });

  await page.goto('http://localhost:8000/harmony.html');
  await page.selectOption('#harmony-select', 'simple_chord_changes');
  await page.click('button:has-text("Generate Transformation")');

  console.log('Waiting for response...');
  await page.waitForTimeout(8000);

  // Get the transformed ABC from the page's variationAbcs
  const abc = await page.evaluate(() => {
    return window.variationAbcs ? window.variationAbcs['full-transformation'] : 'not found';
  });

  console.log('\n=== TRANSFORMED ABC ===');
  console.log(abc);
  console.log('======================\n');

  await browser.close();
})();
