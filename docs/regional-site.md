# Vikri website

The Regional website uses the Vikri name. The approved design uses a light
background, two short feature lists, app downloads and support at the top,
and the free and four annual paid plans below. It describes a khatabook for
small, non-GST businesses. It offers Android phone and Windows information;
it does not claim tablet availability.

## Pages and contact actions

- `/regional/` is the public product page. It includes plans and a WhatsApp
  link for plan questions.
- `/regional/support/` is the help page used by the Google Play app and by
  Android builds whose distribution is not known. Its only external actions
  are a support WhatsApp draft and a telephone link. The logo does not link
  back to the sales page. It contains no plan, price, purchase or upgrade
  content and no script or redirect to a sales page.
- Both pages use `+91 9225252566`. The middle `252525` has a stronger font
  weight and green colour. The ten-digit number has no spaces or boxes.
- The root homepage keeps its existing product and download content. Only
  its Regional link label changes to `Vikri`.

The support boundary follows the app's existing website-link contract and
[Google Play's payments guidance](https://support.google.com/googleplay/android-developer/answer/10281818).
Support conversations must remain help-only when reached through the app.
The page layout alone does not establish Google Play approval.

## Downloads and legal pages

The owner requested download placeholders on 30-10-2026. Both download buttons
are disabled and say `Coming soon`. No APK, installer or store URL is invented.
Replace each placeholder with a real link when that release is approved.

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
- The number's middle digits use weight 700; the other digits use weight 400.
  The browser displayed the full number without spaces between its ten digits.

These checks do not prove a hosted deployment, Google Play approval, a real
phone call, WhatsApp message delivery, physical-device accessibility or app
release readiness. No app package was built or uploaded.

## Rollback

Revert the website change commit if the deployed pages fail their checks. The
change does not touch app data, account records, release files or ERP source.
The prior Regional page can then be served by the existing hosting workflow.
