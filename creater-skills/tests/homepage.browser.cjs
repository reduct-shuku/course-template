// Run against a running preview: HOMEPAGE_URL=http://127.0.0.1:5173 node creater-skills/tests/homepage.browser.cjs
const assert = require('node:assert/strict');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async () => {
  const browser = await chromium.launch({ headless: true, ...(process.env.BROWSER_PATH ? { executablePath: process.env.BROWSER_PATH } : {}), args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(process.env.HOMEPAGE_URL || 'http://127.0.0.1:5173', { waitUntil: 'networkidle' });
    await page.getByRole('heading', { name: /下一次理解，从这里开始/ }).waitFor();
    const cards = page.locator('.sd-library-card');
    const count = await cards.count();
    assert.ok(count > 0, 'Registered courses must be visible');
    const first = cards.first();
    const title = await first.locator('h2').innerText();
    await page.getByRole('searchbox').fill('no-course-matches-8fae57');
    assert.equal(await cards.count(), 0);
    await page.getByRole('button', { name: '浏览全部课程' }).click();
    assert.equal(await cards.count(), count);
    await page.getByRole('searchbox').fill(title);
    assert.ok(await cards.count() > 0);
    await page.getByRole('button', { name: '清空搜索' }).click();
    await first.getByRole('button', { name: `收藏${title}`, exact: true }).click();
    await page.getByRole('button', { name: /我的收藏/ }).click();
    assert.equal(await cards.count(), 1);
    await page.reload({ waitUntil: 'networkidle' });
    assert.equal(await page.getByRole('button', { name: `取消收藏${title}`, exact: true }).count(), 1);
    await cards.first().locator('h2 button').click();
    const dialog = page.getByRole('dialog');
    await dialog.waitFor({ state: 'visible' });
    assert.equal(await dialog.locator('h2').innerText(), title);
    const selfStudy = await dialog.getByRole('link', { name: '自学互动模式', exact: true }).getAttribute('href');
    assert.ok(selfStudy && selfStudy.includes('/modules/'));
    const teaching = dialog.getByRole('link', { name: '教学展示模式', exact: true });
    if (await teaching.count()) assert.ok((await teaching.getAttribute('href')).includes('deck='));
    await page.keyboard.press('Escape');
    await dialog.waitFor({ state: 'hidden' });
    for (const width of [1600, 390]) {
      await page.setViewportSize({ width, height: 900 });
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `No overflow at ${width}`);
    }
    // Old or corrupted preferences must not make the homepage blank.
    await page.evaluate(() => localStorage.setItem('scenedeck:saved-courses', '{}'));
    await page.reload({ waitUntil: 'networkidle' });
    await page.getByRole('heading', { name: /下一次理解，从这里开始/ }).waitFor();
    assert.equal(errors.length, 0, errors.join('\n'));
    if (process.env.HOMEPAGE_SCREENSHOT) {
      await page.setViewportSize({ width: 1600, height: 900 });
      await page.screenshot({ path: process.env.HOMEPAGE_SCREENSHOT, fullPage: true });
    }
    console.log('PASS: course listing, search/reset, bookmarks/persistence, directory/mode links, dismissal, mobile layout and invalid storage');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
