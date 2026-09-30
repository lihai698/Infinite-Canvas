import re
import unittest
from pathlib import Path


INDEX_HTML = Path(__file__).resolve().parents[1] / "static" / "index.html"


class CompactSidebarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = INDEX_HTML.read_text(encoding="utf-8")

    def test_sidebar_never_expands_on_hover_or_pin(self):
        expanding_rules = re.findall(
            r"\.sidebar(?::hover|\.is-pinned)\s*\{[^}]*width:\s*220px",
            self.html,
            flags=re.S,
        )
        self.assertEqual(expanding_rules, [])

    def test_sidebar_uses_one_floating_tooltip(self):
        self.assertIn('id="sidebarTooltip"', self.html)
        self.assertIn("setupSidebarTooltips", self.html)
        self.assertIn("getBoundingClientRect", self.html)

    def test_navigation_click_handlers_are_preserved(self):
        for page_id in (
            "zimage", "enhance", "klein", "angle", "online",
            "gpt-chat", "canvas", "asset-manager", "api-settings",
            "comfyui-settings",
        ):
            self.assertIn(f"switchUI(this, '{page_id}')", self.html)

    def test_author_section_and_its_social_links_are_removed(self):
        self.assertNotIn('class="author-box"', self.html)
        for url in (
            "https://space.bilibili.com/78652351",
            "https://www.xiaohongshu.com/user/profile/6433c34c000000001a023538",
            "https://www.youtube.com/@%E5%A4%A7%E9%9B%84dx",
            "https://x.com/dx8152?s=21",
        ):
            self.assertNotIn(url, self.html)


if __name__ == "__main__":
    unittest.main()
