# Task Manager website

A static documentation page with a sticky table of contents. No npm install or build step needed.

## Preview locally

From the repository root:

```bash
python3 -m http.server 4173 --directory website
```

Open http://localhost:4173.

## Deploy on Vercel

Push these files to GitHub, import this repository into Vercel, and choose:

| Setting | Value |
| --- | --- |
| Root Directory | `website` |
| Framework Preset | `Other` |
| Build Command | Leave empty |
| Output Directory | `.` |

Then click **Deploy**. No environment variables are needed. The included
`vercel.json` sets the framework, build command, and output directory. Set the
Root Directory in Vercel so that it deploys only the website.

[Vercel configuration reference](https://vercel.com/docs/project-configuration/vercel-json)

## Edit the page

- `index.html` — copy, sections, package and repository links.
- `styles.css` — charcoal background, orange accents, and article typography.
- `script.js` — active-section navigation, mobile contents menu, and copy buttons.
- `assets/` — favicon and terminal previews.

The three SVG previews contain real CLI output from isolated demo data with a
fixed sample date. They are text-based renders, not photographs of a terminal.
Regenerate them from the repository root after changing the CLI:

```bash
python3 scripts/render_website_previews.py
```

Copy buttons use the Clipboard API, available on HTTPS deployments and localhost.
If copying is unavailable, the page asks the visitor to copy the visible command
manually. The default installation instructions and links work without JavaScript.
