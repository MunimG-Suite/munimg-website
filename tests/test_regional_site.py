"""Check the public-page and app-support boundaries without extra packages."""

import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import parse_qs, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PAGES = (ROOT / "regional/index.html", ROOT / "regional/support/index.html")
PHONE = "+919225252566"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.tags = []
        self.text = []
        self.phone_text = []
        self.in_phone = False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == "a" and "contact-number" in attrs.get("class", "").split():
            self.in_phone = True

    def handle_endtag(self, tag):
        if tag == "a":
            self.in_phone = False

    def handle_data(self, data):
        self.text.append(data)
        if self.in_phone:
            self.phone_text.append(data)

    def elements(self, tag):
        return [attrs for name, attrs in self.tags if name == tag]


class RegionalSiteTest(unittest.TestCase):
    def test_stylesheet_version_matches_current_content(self):
        stylesheet = ROOT / "regional/styles.css"
        version = hashlib.sha256(stylesheet.read_text(encoding="utf-8").encode()).hexdigest()[:12]
        for path in PAGES:
            local_styles = [urlsplit(link["href"]) for link in Page(path).elements("link")
                            if link.get("rel") == "stylesheet"
                            and urlsplit(link["href"]).path == "/regional/styles.css"]
            self.assertEqual(len(local_styles), 1)
            self.assertEqual(parse_qs(local_styles[0].query), {"v": [version]})

    def test_app_support_cannot_lead_to_sales(self):
        page = Page(PAGES[1])
        allowed = {
            "#main",
            "tel:" + PHONE,
            "https://wa.me/919225252566?text=Hello%2C%20I%20need%20help%20with%20Vikri.",
        }
        self.assertEqual({a["href"] for a in page.elements("a")}, allowed)
        self.assertNotRegex(" ".join(page.text).lower(), r"₹|\b(?:plans?|prices?|buy|purchase|subscribe|checkout|upgrade)\b")
        for forbidden_tag in ("script", "iframe", "form"):
            self.assertFalse(page.elements(forbidden_tag), forbidden_tag)
        self.assertFalse([a for a in page.elements("meta") if a.get("http-equiv", "").lower() == "refresh"])

    def test_contact_links_use_the_confirmed_number(self):
        for path in PAGES:
            page = Page(path)
            phone_links = 0
            for link in page.elements("a"):
                href = link["href"]
                if href.startswith("tel:"):
                    self.assertEqual(href, "tel:" + PHONE)
                    phone_links += 1
                if urlsplit(href).hostname == "wa.me":
                    self.assertEqual(urlsplit(href).path, "/919225252566")
                    self.assertIn("text", parse_qs(urlsplit(href).query))
            self.assertGreaterEqual(phone_links, 2)
            self.assertEqual("".join(page.phone_text), "+91 92 25 25 25 66")

    def test_unreleased_apps_are_announced_without_download_controls(self):
        page = Page(PAGES[0])
        self.assertFalse(page.elements("button"))
        self.assertEqual(" ".join(page.text).count("Coming soon on Android and Windows"), 1)
        for link in page.elements("a"):
            self.assertNotRegex(link["href"], r"(?i)\.(apk|aab|msi|exe)(?:\?|$)|play\.google\.com")

    def test_plans_keep_the_five_public_prices(self):
        text = " ".join(Page(PAGES[0]).text)
        for price in ("₹0", "₹999", "₹1,999", "₹2,999", "₹3,999"):
            self.assertIn(price, text)

    def test_click_table_shows_vikri_counts_and_the_counting_rule(self):
        page = Page(PAGES[0])
        text = " ".join(page.text)
        self.assertEqual(len(page.elements("table")), 1)
        for phrase in ("Clicks to add all 8 types", "Clicks to bill all 8 types",
                       "Every box or button you tap is 1 click."):
            self.assertIn(phrase, text)

    def test_local_links_assets_and_fragments_exist(self):
        for path in PAGES:
            page = Page(path)
            ids = [attrs["id"] for _, attrs in page.tags if "id" in attrs]
            self.assertEqual(len(ids), len(set(ids)), "Duplicate IDs")
            for tag, attrs in page.tags:
                href = attrs.get("href") or attrs.get("src")
                if not href:
                    continue
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                if not url.path:
                    self.assertIn(url.fragment, ids)
                    continue
                target = ROOT / url.path.lstrip("/") if url.path.startswith("/") else path.parent / url.path
                if target.is_dir():
                    target /= "index.html"
                self.assertTrue(target.is_file(), f"Missing {href} in {path}")
                if tag == "use":
                    icon_ids = {element.get("id") for element in ET.parse(target).iter()}
                    self.assertIn(url.fragment, icon_ids)

    def test_visible_copy_has_no_removed_claims_or_preview_text(self):
        for path in PAGES:
            text = " ".join(Page(path).text)
            self.assertNotRegex(text.lower(), r"\b(?:tablet|b2b|b2c|mockup|preview|todo|fastest)\b|formerly|munimg erp regional")

    def test_pages_have_one_heading_and_their_own_canonical_url(self):
        for path, suffix in zip(PAGES, ("/regional/", "/regional/support/")):
            page = Page(path)
            self.assertEqual(len(page.elements("h1")), 1)
            self.assertEqual(len(page.elements("main")), 1)
            canonicals = [link["href"] for link in page.elements("link") if link.get("rel") == "canonical"]
            self.assertEqual(canonicals, ["https://munimg.net" + suffix])


if __name__ == "__main__":
    unittest.main()
