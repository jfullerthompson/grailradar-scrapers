from fastapi import FastAPI
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get("/psa/{cert}")
def get_psa(cert: str):

    url = f"https://www.psacard.com/cert/{cert}"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # 👈 IMPORTANT (test first)
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900}
        )

        page = context.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("p.text-display5", timeout=60000)

        title = page.locator("p.text-display5").first.inner_text()
        image = page.locator("img[itemprop='contentUrl']").first.get_attribute("src")

        browser.close()

    return {
        "cert_number": cert,
        "title": title,
        "image_front": image
    }
