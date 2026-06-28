# Aliya Wedding Organizer Static Site Design

## Goal

Build a premium static website for Aliya Wedding Organizer as a branding, portfolio, service package, and lead generation channel. The main conversion path is WhatsApp consultation.

The website will run locally with Python as a static server and simple Git Bash scripts:

- `./start.sh`
- `./stop.sh`

No Docker is used.

## Brand And Content

Brand:

- Aliya Wedding Organizer
- WhatsApp: `+62 896-3743-1865`
- Instagram: `@aliyatazkiaa_`
- Maps: `https://maps.app.goo.gl/WJvTm61HaXCupswC6`
- GitHub target: `https://github.com/AlAfif19/wedding`

Tone:

- Elegant
- Romantic
- Premium
- Editorial
- Trustworthy

No emoji or emoticon characters will be used in the source text or visible UI.

## Frontend Modes

The site will include three visual modes in one codebase. Users can switch modes from an in-page style switcher.

### Mode 1: Luxury Editorial

This is the default mode. It uses ivory, cream, champagne gold, rose gold, serif headings, soft shadows, and large floral overlays. It prioritizes a premium first impression and follows the supplied mockup direction.

Best for:

- Brand trust
- Premium wedding organizer positioning
- Elegant portfolio presentation

### Mode 2: Cinematic Romantic

This mode makes visuals more immersive with deeper contrast, larger media blocks, stronger scroll storytelling, and a more emotional gallery flow. It is designed for photo and video-heavy presentation while staying lightweight through lazy loading and compressed assets.

Best for:

- Portfolio storytelling
- Wedding video/photo showcase
- Emotional engagement

### Mode 3: Modern Booking

This mode makes the layout more direct and conversion-focused. Packages, process, FAQ, WhatsApp CTA, Instagram, and Maps receive stronger hierarchy. Decorative overlays remain present but quieter.

Best for:

- Fast scanning
- Booking consultation
- Clear package comparison

## Page Structure

The first version will include these sections:

1. Header and navigation
2. Hero with CTA, contact shortcuts, parallax media, and floating overlay ornament
3. About Aliya
4. Package cards: Silver, Gold, Platinum
5. Why Choose Us
6. Gallery with image/video placeholders, masonry layout, and modal preview
7. Testimonials with slider behavior
8. Process timeline: Consultation, Planning, Preparation, Wedding Day, After Event
9. FAQ accordion
10. Contact section with WhatsApp, Instagram, and Maps CTA
11. Footer
12. Sticky WhatsApp action
13. Fixed decorative overlay layer

## Interaction And Animation

Animations will be implemented with plain JavaScript and CSS patterns inspired by Motion.dev, Magic UI, Aceternity UI, and shadcn/ui styling. Because this is a static HTML project, external component libraries will be represented as design patterns rather than installed React components.

Required animation behavior:

- Scroll reveal with IntersectionObserver
- Hero parallax based on scroll position
- Floating floral overlay motion
- Smooth hover and press states
- Gallery modal transitions
- Testimonial auto slide
- FAQ accordion expand/collapse
- Reduced-motion support through `prefers-reduced-motion`

## Asset Strategy

Folder structure:

```text
assets/
  images/
    hero/
    gallery/
    testimonials/
    packages/
  videos/
  music/
  overlays/
    flowers/
    rings/
    ribbons/
    ornaments/
  compressed/
src/
  css/
  js/
  components/
  data/
tools/
  compress_assets.py
```

The implementation will include generated placeholder assets or CSS visual placeholders if real assets are not available locally. Any real images, videos, music, or overlays added later should be compressed into `assets/compressed/` before production use.

`tools/compress_assets.py` will provide a local helper for:

- WebP image compression when Pillow is available
- MP4 compression guidance when ffmpeg is available
- MP3 compression guidance when ffmpeg is available
- Safe fallback messages when optional tools are missing

## Overlay Layer

The site will include fixed overlay decoration on a high visual layer. The overlay must:

- Stay pointer-events none so it does not block clicks
- Appear at page edges on desktop
- Scale down on tablet and mobile
- Avoid covering important text and CTA buttons
- Create the impression of floral or wedding ornaments emerging from the screen

Large full-section ornaments can be added per mode, but they must remain responsive and not break reading flow.

## Technical Architecture

Files:

- `index.html`: semantic page markup
- `src/css/styles.css`: Tailwind-like utility styling plus custom component styles
- `src/js/app.js`: mode switcher, scroll reveal, parallax, slider, modal, FAQ
- `src/data/site.js`: packages, testimonials, gallery, FAQ, contact data
- `server.py`: Python static server
- `start.sh`: starts Python server from Git Bash
- `stop.sh`: stops server process created by `start.sh`
- `tools/compress_assets.py`: asset compression helper

The project will remain static and deployable to Vercel, Netlify, VPS, or GitHub Pages-style hosting.

## Responsive Design

Approach:

- Mobile first
- Tablet, laptop, desktop, and ultra-wide breakpoints
- Navigation collapses on mobile
- Cards stack on mobile and become grids on wider screens
- Gallery shifts from single column to masonry-like grid
- Timeline becomes vertical on mobile and horizontal on larger screens
- Overlay scale is controlled per breakpoint

## Performance Requirements

Target:

- Lighthouse score above 90
- First load under 3 seconds for local optimized assets
- Lazy-loaded media
- No heavy runtime framework
- CSS and JavaScript kept small

Performance tactics:

- Use `loading="lazy"` for below-the-fold images
- Use compressed WebP assets where possible
- Avoid layout shifts with stable image aspect ratios
- Use transform and opacity for animations
- Respect reduced motion settings

## Accessibility And UX

Required:

- Semantic sections and headings
- Keyboard-accessible buttons, modal, FAQ, and navigation
- Visible focus states
- Sufficient contrast on text and buttons
- Alt text for images
- CTA links with clear labels
- No decorative asset should block interaction

## Testing And Verification

Before completion, verify:

- `./start.sh` starts the site
- `./stop.sh` stops the server
- Page loads in browser at the printed local URL
- Mobile, tablet, laptop, and large desktop layouts are usable
- Three visual modes can be switched
- WhatsApp, Instagram, and Maps links are correct
- No emoji or emoticon characters are present in visible content
- No console-breaking JavaScript errors

## Open Decisions

The first implementation will use placeholders for real portfolio media unless local assets are provided. The structure will make it easy to replace placeholders with compressed production photos, videos, music, and transparent overlays later.
