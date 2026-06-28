# Aliya Wedding Organizer

Static premium website for Aliya Wedding Organizer. The site includes three switchable visual modes, responsive mobile-first layout, scroll animation, parallax, gallery preview, FAQ accordion, testimonial slider, and sticky WhatsApp contact.

## Run Locally

Use Git Bash in VS Code:

```bash
./start.sh
```

Open:

```text
http://127.0.0.1:8000
```

Stop the server:

```bash
./stop.sh
```

## Project Structure

```text
assets/
  images/
  videos/
  music/
  overlays/
  compressed/
src/
  css/styles.css
  js/app.js
  data/site.js
tools/
  compress_assets.py
index.html
server.py
start.sh
stop.sh
```

## Visual Modes

- Luxury: premium editorial wedding style.
- Cinema: immersive romantic showcase style.
- Booking: conversion-focused consultation style.

The selected mode is saved in the browser with `localStorage`.

## Edit Content

Most editable content lives in:

```text
src/data/site.js
```

Update packages, gallery, testimonials, process steps, FAQ, WhatsApp, Instagram, and Maps links there.

## Compress Assets

Put original media in `assets/`, then run:

```bash
python tools/compress_assets.py
```

Images are converted to WebP when Pillow is installed:

```bash
python -m pip install pillow
```

For video and music, install `ffmpeg`; the helper will print safe compression commands.

## Deploy

This is a static site. It can be deployed to Vercel, Netlify, GitHub Pages-style hosting, or a VPS static server.

For GitHub:

```bash
git init
git add .
git commit -m "feat: build aliya wedding static site"
git branch -M main
git remote add origin https://github.com/AlAfif19/wedding.git
git push -u origin main
```
