# Aliya Wedding Static Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a responsive static Aliya Wedding Organizer website with three switchable frontend modes and simple Python server scripts.

**Architecture:** The site is a no-build static app. `index.html` owns semantic markup, `src/css/styles.css` owns visual systems and responsive behavior, `src/data/site.js` owns editable content, and `src/js/app.js` owns rendering and interaction.

**Tech Stack:** HTML5, CSS with Tailwind-like utilities and shadcn/Magic UI/Aceternity-inspired components, vanilla JavaScript, Python static server, Git Bash shell scripts.

## Global Constraints

- Run locally with `./start.sh` and `./stop.sh`.
- No Docker.
- Python is used only as a local static server.
- No emoji or emoticon characters in visible UI or source copy.
- Mobile first responsive layout for phone, tablet, laptop, desktop, and ultra-wide.
- Include three frontend modes: Luxury Editorial, Cinematic Romantic, Modern Booking.
- Include scroll reveal, scroll parallax, floating animation, smooth hover transitions, and sticky decorative overlays.
- Include folders for images, videos, music, overlays, compressed assets, CSS, JS, components, data, and tools.
- Keep decorative overlays non-blocking with `pointer-events: none`.

---

### Task 1: Runtime And Folder Structure

**Files:**
- Create/modify: `server.py`
- Create/modify: `start.sh`
- Create/modify: `stop.sh`
- Create/modify: asset and source folders

**Interfaces:**
- Produces: `server.py --host 127.0.0.1 --port 8000`
- Produces: `.server.pid` created by `start.sh` and consumed by `stop.sh`

- [ ] **Step 1: Create folders**

Run:

```bash
mkdir -p assets/images/hero assets/images/gallery assets/images/testimonials assets/images/packages
mkdir -p assets/videos assets/music assets/overlays/flowers assets/overlays/rings assets/overlays/ribbons assets/overlays/ornaments assets/compressed
mkdir -p src/css src/js src/components src/data tools
```

- [ ] **Step 2: Implement Python static server**

Write `server.py` with `ThreadingHTTPServer`, local binding, command arguments, and no caching for HTML.

- [ ] **Step 3: Implement run scripts**

Write `start.sh` to start `server.py`, write `.server.pid`, and print `http://127.0.0.1:8000`.

Write `stop.sh` to read `.server.pid`, stop the server process, and remove the pid file.

- [ ] **Step 4: Verify runtime**

Run:

```bash
./start.sh
./stop.sh
```

Expected: server starts and stops without Docker.

### Task 2: Site Data

**Files:**
- Create: `src/data/site.js`

**Interfaces:**
- Produces: `window.ALIYA_SITE_DATA`
- Consumes: no previous task output

- [ ] **Step 1: Create content data**

Define brand, links, packages, why items, gallery items, testimonials, process steps, and FAQ entries.

- [ ] **Step 2: Verify data loads**

Expected: browser console can read `window.ALIYA_SITE_DATA.brand.name`.

### Task 3: Semantic HTML Shell

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: `src/data/site.js`
- Consumes: `src/css/styles.css`
- Consumes: `src/js/app.js`
- Produces: DOM targets with IDs used by `app.js`

- [ ] **Step 1: Build document shell**

Create semantic sections for header, hero, about, packages, why, gallery, testimonials, process, FAQ, contact, footer, mode switcher, modal, and sticky WhatsApp CTA.

- [ ] **Step 2: Add accessible static fallbacks**

Include meaningful headings, CTA links, and noscript-safe core content.

### Task 4: Visual System And Three Modes

**Files:**
- Create: `src/css/styles.css`

**Interfaces:**
- Consumes: `body[data-mode="luxury"]`, `body[data-mode="cinematic"]`, and `body[data-mode="booking"]`
- Produces: responsive layout and component styles

- [ ] **Step 1: Add design tokens**

Define CSS variables for each mode: background, text, muted text, gold, rose, panel, border, and shadow.

- [ ] **Step 2: Add component styling**

Style buttons, cards, nav, package grid, gallery, testimonials, timeline, accordion, modal, and contact.

- [ ] **Step 3: Add responsive behavior**

Implement mobile first breakpoints for navigation, grids, hero, overlays, and timeline.

- [ ] **Step 4: Add animation rules**

Implement reveal states, floating overlays, parallax-safe transforms, hover states, modal transitions, and reduced-motion overrides.

### Task 5: App Interaction

**Files:**
- Create: `src/js/app.js`

**Interfaces:**
- Consumes: `window.ALIYA_SITE_DATA`
- Consumes: DOM targets from `index.html`
- Produces: rendered cards, mode switching, parallax, reveal, gallery modal, testimonial slider, FAQ accordion

- [ ] **Step 1: Render dynamic sections**

Render packages, why items, gallery items, testimonials, process steps, and FAQs from `window.ALIYA_SITE_DATA`.

- [ ] **Step 2: Implement mode switcher**

Save selected mode to `localStorage` as `aliya-mode`; apply it to `body.dataset.mode`.

- [ ] **Step 3: Implement scroll interactions**

Use `IntersectionObserver` for reveal and `requestAnimationFrame` for parallax.

- [ ] **Step 4: Implement interactive components**

Add gallery modal, testimonial slider, mobile nav toggle, and FAQ accordion.

### Task 6: Asset Compression Helper

**Files:**
- Create: `tools/compress_assets.py`

**Interfaces:**
- Produces: CLI helper `python tools/compress_assets.py`
- Consumes: local `assets/` folders

- [ ] **Step 1: Implement helper**

Scan common media folders, compress images to WebP if Pillow is installed, and print ffmpeg commands for videos and music if ffmpeg is available.

- [ ] **Step 2: Verify fallback**

Run:

```bash
python tools/compress_assets.py
```

Expected: helper reports available compression actions without crashing.

### Task 7: Verification

**Files:**
- Modify as needed based on failures

**Interfaces:**
- Consumes: all previous tasks

- [ ] **Step 1: Run server**

Run:

```bash
./start.sh
```

Expected: `http://127.0.0.1:8000` is available.

- [ ] **Step 2: Inspect files for forbidden visible emoji/emoticons**

Run a text scan over `index.html`, `src/`, and `tools/`.

- [ ] **Step 3: Verify responsive layout**

Open the local page and check phone, tablet, laptop, and desktop widths.

- [ ] **Step 4: Stop server**

Run:

```bash
./stop.sh
```

Expected: process stops and `.server.pid` is removed.
