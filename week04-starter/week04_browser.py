"""Selenium tools and screenshot observations for a fixed local practice page."""
from io import BytesIO
from pathlib import Path
from PIL import Image
from smolagents import tool

ROOT = Path(__file__).resolve().parent


class BrowserSession:
    def __init__(self):
        from selenium import webdriver
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1000,950")
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(20)
        self.sequence = 0
        self.tools = self._make_tools()

    def _make_tools(self):
        @tool
        def open_venue() -> str:
            """Open the supplied local fictional venue page in Chrome."""
            self.driver.get((ROOT / "assets/venue.html").as_uri())
            return "Opened local venue page; inspect the screenshot observation."

        @tool
        def show_access_details() -> str:
            """Click the local page's Show access details button."""
            from selenium.webdriver.common.by import By
            expected = (ROOT / "assets/venue.html").as_uri()
            if self.driver.current_url != expected:
                raise ValueError("Call open_venue first")
            self.driver.find_element(By.TAG_NAME, "button").click()
            return "Clicked Show access details; inspect the new screenshot observation."
        return [open_venue, show_access_details]

    def capture(self, step, agent):
        """Add the actual browser screenshot after each action, retaining only the latest."""
        from smolagents.memory import ActionStep
        if not isinstance(step, ActionStep):
            return
        for previous in agent.memory.steps:
            if isinstance(previous, ActionStep):
                previous.observations_images = None
        image = Image.open(BytesIO(self.driver.get_screenshot_as_png())).convert("RGB")
        output = ROOT / "outputs"
        output.mkdir(exist_ok=True)
        self.sequence += 1
        image.save(output / f"browser-{self.sequence:02d}.png")
        step.observations_images = [image.copy()]
        step.observations = (step.observations or "") + "\nBrowser URL: " + self.driver.current_url

    def close(self):
        self.driver.quit()
