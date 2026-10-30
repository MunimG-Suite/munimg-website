# Vikri website

The Regional website uses the Vikri name. The owner approved the 30-10-2026
home page design from the mockup. Its order is: opening section, three steps
for item options, the click table, staff, languages, plans, questions and
support. The opening line is `Fewer clicks. Faster bills.` because it fits
every shop; `Every size. Every colour.` was rejected for not doing so. The page
describes billing for small, non-GST businesses. It offers Android phone and
Windows information; it does not claim tablet availability.

The design uses the approved Vikri logo kit from the ERP repository
(`docs/design/brand/vikri`): navy `#10265B`, saffron `#F29B16`, and the name
pair logo. Saffron is never small text on white, because its contrast is too
low there. Buttons are flat with a 12 px corner. Hindi and Marathi text uses
Noto Sans Devanagari, because Inter has no Devanagari letters.

The two opening screens in `regional/images` are the real `Add item options`
test images from the ERP repository, cropped by a task script. Replace them
with device screenshots when those are available.

At 560 px and below, the home page follows the approved phone design, not the
desktop layout. The staff card comes before the staff list, the Free and First
phone prices sit beside the plan name, the opening section has only the WhatsApp
action, and the help buttons have no icons. Compare any phone change with that
design side by side. A check for overflow alone does not prove a match.

## Click table

The click table uses one rule: every box or button tapped is 1 click, and
typing is not counted. The task is one new item with a name and a sale rate
and 8 types.

- Vikri, counted from the Android source: 11 clicks to add all 8 types, and 10
  clicks to bill them with different quantities.
- Other billing apps, 25+ to add: counted on 30-10-2026 from public help pages,
  not from use of the apps. Swipe 27, Vyapar 25 and myBillBook 32.
- Other billing apps, 18+ to bill: an estimate, because the help pages do not
  show this flow step by step.

The owner chose to publish these numbers on 30-10-2026 before a hands-on phone
test. That test remains open. The page does not name the other apps.

## Pages and contact actions

- `/regional/` is the public product page. It includes plans and a WhatsApp
  link for plan questions.
- `/regional/support/` is the help page used by the Google Play app and by
  Android builds whose distribution is not known. Its only external actions
  are a support WhatsApp draft and a telephone link. The logo does not link
  back to the sales page. It contains no plan, price, purchase or upgrade
  content and no script or redirect to a sales page.
- Both pages display `+91 92 25 25 25 66`. All ten phone digits use the same
  colour and font weight. Spaces separate each pair; the number stays on one
  line. On the support page, a soft saffron background covers only the ten
  phone digits and the `+91` country code has no highlight. The home page shows
  the number in plain white on navy. The telephone and WhatsApp targets remain
  `+919225252566`.
- The root homepage keeps its existing product and download content. Only
  its Regional link label changes to `Vikri`.
- The Vikri top navigation contains `Plans` and `Support`. There is no top
  `Downloads` link.

The support boundary follows the app's existing website-link contract and
[Google Play's payments guidance](https://support.google.com/googleplay/android-developer/answer/10281818).
Support conversations must remain help-only when reached through the app.
The page layout alone does not establish Google Play approval.

## Downloads and legal pages

The approved design replaces the two disabled download buttons with one line:
`Coming soon on Android and Windows`. The main action is a WhatsApp link. No
APK, installer or store URL is invented. Add real download links when each
release is approved.

Privacy, terms and refund links are omitted because no approved public pages
are available in this repository. The Regional app's legal publication gate
remains open. The draft legal documents are not published by this change.

## Implementation and checks

The pages use static HTML, one shared stylesheet and local SVG icons. Navigation,
phone links, WhatsApp links and FAQs do not require JavaScript. No new build
tool or runtime package is required.

From the website checkout, run `python -m unittest discover -s tests -v`.
The checks cover the help-only link boundary, the confirmed contact number,
download placeholders, local assets and links, removed wording, and page
headings/canonical addresses. They do not place a call or send a message.

Before pushing, also run `git diff --check` and inspect the homepage and support
page in a browser at wide and narrow widths. Keep all test output and temporary
files in the task directory on D:.

### Check record — 30-10-2026

The source was checked in an isolated D: checkout on Windows with Python 3.13.

- `python -m unittest discover -s tests -v`: exit 0; 6 tests passed.
- `git diff --check`: exit 0.
- `python D:\CodexWork\MunimG-Suite\munimg-website\vikri-publish-20261030\refresh-website-kb.py`:
  exit 0. This calls the existing suite generator on a website-only snapshot.
  It refreshes the website knowledge pages without writing to other projects.
- `python -m py_compile C:\Users\Admin\Projects\MunimG-Suite\scripts\generate_ai_knowledge_base.py`:
  exit 0, with the bytecode cache redirected to D:.
- Browser checks: homepage at normal desktop width, 390 px and 320 px; support
  at 320 px and normal desktop width. No horizontal overflow was found at the
  narrow widths. Navigation, FAQ expansion and the visible keyboard focus on
  the skip link worked. The support page had only the expected contact links.
- At initial publication, the number's middle digits used weight 700 and the
  other digits used weight 400, with no spaces. The owner later replaced this
  design with equal-weight, two-digit groups as specified above.

These checks do not prove a hosted deployment, Google Play approval, a real
phone call, WhatsApp message delivery, physical-device accessibility or app
release readiness. No app package was built or uploaded.

### Phone spacing and navigation check — 30-10-2026

The owner requested equal styling with `92 25 25 25 66`, and removal of the
top `Downloads` link. Both contact pages use the grouped display. The actual
telephone and WhatsApp targets stay unchanged.

- `python -m unittest discover -s tests -v`: exit 0; all 6 existing tests passed.
- `git diff --check`: exit 0.
- The website-only knowledge-page refresh: exit 0.
- Browser check: the phone digits form one plain text span at weight 400;
  navigation contains only Plans and Support; no horizontal overflow at 320 px.

### Colour, type and button checks - 30-10-2026

- The six existing website tests passed after the final button change:
  `python -m unittest discover -s tests -v`, exit 0.
- `git diff --check`: exit 0.
- Browser checks confirmed the main and support pages had no horizontal
  overflow at a 320 px viewport. The buttons had no clipped text.
- Selected text contrast ratios were 17.02:1 for page text, 6.38:1 for the
  main action, 5.39:1 for support text and 13.21:1 for the phone number.
- The main page buttons showed rounded ends and shadows. The country code
  remained outside the number highlight.
- These checks do not establish full accessibility or physical-device proof.

### Stylesheet cache fix - 30-10-2026

The live server served the new stylesheet, but an existing browser still used
its cached green design after reload. Both pages now include a version in the
stylesheet link. A test compares it with the current CSS content
so future style changes must update that version. Product: Vikri website.
Frequency: 6/10. Severity: 3/10. Score: 18.

### Home page redesign check - 30-10-2026

The source was checked in an isolated D: worktree on Windows with Python 3.13.7.

- `python -m unittest discover -s tests -v`: exit 0; 9 tests passed.
- `git diff --check`: exit 0.
- Browser checks with Edge at 1440, 1000, 390 and 320 px: the page rendered in
  the expected order. At 390 and 320 px there was no horizontal overflow, the
  opening line stayed on two lines and all links were at least 44 px tall.
- The support page was checked at 1440 and 320 px.

These checks do not prove a hosted deployment, a real phone, WhatsApp delivery,
Google Play approval or full accessibility. The click counts were not tested
by hand in any app.

### Phone layout match - 30-10-2026

The first build used the desktop layout at phone width, so it did not match the
approved phone design. Product: Vikri website. Frequency: 10/10. Severity: 3/10.
Score: 30. This change adds phone rules at 560 px and below.

- `python -m unittest discover -s tests -v`: exit 0; 9 tests passed.
- `git diff --check`: exit 0.
- Side-by-side check at 390 px: all 24 headings were within 1 px of the phone
  design. Footer legal links stay out, because those pages do not exist.
- At 320 and 560 px there was no horizontal overflow. At 320 px all links were
  at least 44 px tall.
- Pixel comparison with the live page at 1440 and 800 px: the only change is the
  footer link text, now `Help & Support`.

These checks do not prove a real phone, WhatsApp delivery or full accessibility.

## Rollback

Soft-background follow-up on 30-10-2026: all 6 existing website tests and
`git diff --check` passed (exit 0). Both pages showed the whole number on the
shared light-green surface, with no horizontal overflow at 320 px. Knowledge
pages were checked; this shared CSS change adds no route or structural change.

Revert the website change commit if the deployed pages fail their checks. The
change does not touch app data, account records, release files or ERP source.
The prior Regional page can then be served by the existing hosting workflow.
