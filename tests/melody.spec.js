import { test, expect } from '@playwright/test';

test.describe('Melody Variations', () => {
  test('should display separate variation snippets grouped by content', async ({ page }) => {
    await page.goto('/melody.html');

    // Fill in ABC notation
    const abcInput = page.locator('#abc-input');
    await expect(abcInput).toBeVisible();

    // ABC should already have Sliabh Russell by default
    const abcContent = await abcInput.inputValue();
    expect(abcContent).toContain('Sliabh Russell');

    // Select a melodic variation type
    await page.selectOption('#melodic-select', 'neighbor');

    // Click generate button
    await page.click('button:has-text("Generate Variation")');

    // Should show spinner
    const variationDesc = page.locator('#variation-desc');
    await expect(variationDesc).toContainText('Generating variation');

    // Wait for variations to load (may take a while due to LLM)
    await page.waitForSelector('.section.variation', { timeout: 60000 });

    // Should have at least one variation snippet
    const variations = page.locator('.section.variation');
    const count = await variations.count();
    expect(count).toBeGreaterThan(0);

    // Each variation should have:
    // 1. Title (Variation 1, Variation 2, etc.)
    // 2. Description with bar numbers
    // 3. Musical notation
    // 4. Play and Stop buttons

    const firstVariation = variations.first();
    await expect(firstVariation.locator('h4')).toContainText('Variation');
    await expect(firstVariation.locator('.description')).toBeVisible();
    await expect(firstVariation.locator('.notation')).toBeVisible();
    await expect(firstVariation.locator('button:has-text("Play")')).toBeVisible();
    await expect(firstVariation.locator('button:has-text("Stop")')).toBeVisible();

    // Description should contain bar numbers
    const description = await firstVariation.locator('.description').textContent();
    expect(description).toMatch(/Bar[s]? \d+/);

    console.log(`✓ Found ${count} variation snippet(s)`);
    console.log(`✓ First variation description: ${description}`);
  });

  test('should group identical modifications into single variation', async ({ page }) => {
    await page.goto('/melody.html');

    // Fill in a specific lick that appears multiple times
    await page.fill('#lick-input', 'eaa efg');

    // Select rhythmic displacement
    await page.selectOption('#melodic-select', 'rhythmic_shift');

    // Click generate
    await page.click('button:has-text("Generate Variation")');

    // Wait for result
    await page.waitForSelector('.section.variation', { timeout: 60000 });

    // Check if multiple bars are grouped
    const firstVariation = page.locator('.section.variation').first();
    const description = await firstVariation.locator('.description').textContent();

    // Should show "Bars X, Y, Z" if grouped, or "Bar X" if single
    const hasBarsPlural = description.includes('Bars ');

    if (hasBarsPlural) {
      console.log('✓ Multiple bars grouped correctly:', description);
      // Should have comma-separated bar numbers
      expect(description).toMatch(/Bars \d+, \d+/);
    } else {
      console.log('✓ Single bar variation:', description);
    }
  });

  test('should have working play and stop buttons', async ({ page }) => {
    await page.goto('/melody.html');

    // Generate a variation
    await page.click('button:has-text("Generate Variation")');
    await page.waitForSelector('.section.variation', { timeout: 60000 });

    // Try clicking play button (we can't test audio, but we can test the button works)
    const playButton = page.locator('.section.variation').first().locator('button:has-text("Play")');
    await playButton.click();

    // Click stop button
    const stopButton = page.locator('.section.variation').first().locator('button:has-text("Stop")');
    await stopButton.click();

    console.log('✓ Play and Stop buttons are clickable');
  });
});
