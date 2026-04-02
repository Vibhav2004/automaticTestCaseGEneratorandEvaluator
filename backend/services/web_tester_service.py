import asyncio
from playwright.async_api import async_playwright
import time

async def run_web_test(url: str):
    tasks = []
    
    async with async_playwright() as p:
        # Launch browser (headless for speed)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Task 1: Navigation
            start_time = time.time()
            try:
                await page.goto(url, wait_until="networkidle", timeout=15000)
                duration = round(time.time() - start_time, 2)
                tasks.append({
                    "action": "navigation",
                    "target": url,
                    "status": "passed",
                    "message": f"Successfully loaded page in {duration}s",
                    "timestamp": time.time()
                })
            except Exception as e:
                tasks.append({
                    "action": "navigation",
                    "target": url,
                    "status": "failed",
                    "message": f"Navigation failed: {str(e)}",
                    "timestamp": time.time()
                })
                return tasks # Stop if navigation fails
            
            # Task 2: Scrolling
            try:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1) # Wait for animations/dynamic content
                await page.evaluate("window.scrollTo(0, 0)")
                tasks.append({
                    "action": "scrolling",
                    "target": "full_page",
                    "status": "passed",
                    "message": "Successfully scrolled through the entire page and back.",
                    "timestamp": time.time()
                })
            except Exception as e:
                 tasks.append({
                    "action": "scrolling",
                    "target": "full_page",
                    "status": "failed",
                    "message": f"Scrolling error: {str(e)}",
                    "timestamp": time.time()
                })

            # Task 3: Interactive Elements Discovery & Testing
            # Find all buttons and links
            buttons = await page.query_selector_all("button, input[type='button'], input[type='submit']")
            links = await page.query_selector_all("a[href]")
            
            # Test some buttons (limit to first 3 to avoid infinite loops/destructive actions)
            for i, button in enumerate(buttons[:3]):
                name = await button.inner_text() or await button.get_attribute("name") or f"Button {i+1}"
                try:
                    # Check if visible and enabled
                    if await button.is_visible() and await button.is_enabled():
                        # We use simple hover/click check (don't actually follow links if they navigate away)
                        await button.hover(timeout=1000)
                        tasks.append({
                            "action": "interaction",
                            "target": name,
                            "status": "passed",
                            "message": f"Verified '{name}' is interactive and visible.",
                            "timestamp": time.time()
                        })
                    else:
                         tasks.append({
                            "action": "interaction",
                            "target": name,
                            "status": "failed",
                            "message": f"Button '{name}' is not visible or disabled.",
                            "timestamp": time.time()
                        })
                except Exception as e:
                     tasks.append({
                        "action": "interaction",
                        "target": name,
                        "status": "failed",
                        "message": f"Error interacting with '{name}': {str(e)}",
                        "timestamp": time.time()
                    })

            # Task 4: Forms (Discovery)
            forms = await page.query_selector_all("form")
            if forms:
                tasks.append({
                    "action": "discovery",
                    "target": f"{len(forms)} Forms Found",
                    "status": "passed",
                    "message": f"Detected {len(forms)} form(s) on the page ready for data input test.",
                    "timestamp": time.time()
                })
            else:
                 tasks.append({
                    "action": "discovery",
                    "target": "Forms",
                    "status": "passed",
                    "message": "No forms detected on the landing page.",
                    "timestamp": time.time()
                })

            # Task 5: Accessibility/SEO Check
            h1 = await page.query_selector("h1")
            status = "passed" if h1 else "warning"
            message = f"Found H1: {await h1.inner_text()}" if h1 else "Missing H1 tag (SEO risk)"
            tasks.append({
                "action": "seo_check",
                "target": "H1 Header",
                "status": status,
                "message": message,
                "timestamp": time.time()
            })

            return tasks

        finally:
            await browser.close()
