---
name: MOHAPX-V-IT
description: Spacious agency typography and an original orange crown for a personal engineering portfolio.
colors:
  dark-accent: "hsl(33 88% 56%)"
  dark-accent-hover: "hsl(33 78% 74%)"
  dark-accent-active: "hsl(24 88% 48%)"
  dark-bg: "#09090C"
  dark-bg-secondary: "#0D0D12"
  dark-surface: "#19191E"
  dark-text: "#ECECF1"
  dark-muted: "#A9A8B3"
  dark-line: "rgba(236,236,241,.17)"
  dark-button-text: "#151218"
  light-accent: "hsl(27 86% 36%)"
  light-accent-hover: "hsl(24 80% 27%)"
  light-accent-active: "hsl(20 84% 33%)"
  light-bg: "#F4F2EE"
  light-bg-secondary: "#FCFBF9"
  light-surface: "#E8E5E0"
  light-text: "#17161C"
  light-muted: "#57555F"
  light-line: "rgba(18,16,12,.2)"
typography:
  display:
    fontFamily: "Manrope, system-ui, sans-serif"
    fontSize: "clamp(52px, 7.5vw, 112px)"
    fontWeight: 650
    lineHeight: 1.03
    letterSpacing: "-.04em"
  headline:
    fontFamily: "Manrope, system-ui, sans-serif"
    fontSize: "clamp(34px, 4.5vw, 68px)"
    fontWeight: 550
    lineHeight: 1.12
    letterSpacing: "-.035em"
  title:
    fontFamily: "Manrope, system-ui, sans-serif"
    fontSize: "25px"
    fontWeight: 650
    lineHeight: 1.3
    letterSpacing: "-.02em"
  body:
    fontFamily: "Manrope, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.7
  intro:
    fontFamily: "Manrope, system-ui, sans-serif"
    fontSize: "18px"
    lineHeight: 1.65
  button:
    fontFamily: "Manrope, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 750
  text-link:
    fontFamily: "Manrope, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 650
  metadata:
    fontFamily: "Manrope, system-ui, sans-serif"
    fontSize: "12px"
  wordmark:
    fontFamily: "Unbounded, Manrope, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 650
    lineHeight: 1.4
    letterSpacing: "-.025em"
rounded:
  square: "0"
spacing:
  gutter: "clamp(20px, 4vw, 64px)"
  gutter-mobile: "22px"
  gap-small: "18px"
  gap: "24px"
  pad: "26px"
  pad-large: "32px"
  gap-large: "34px"
  section-intro-gap: "54px"
  section-mobile: "64px"
  section: "112px"
components:
  button-primary:
    backgroundColor: "{colors.dark-accent}"
    textColor: "{colors.dark-button-text}"
    typography: "{typography.button}"
    rounded: "{rounded.square}"
    padding: "15px 23px"
    height: "54px minimum"
  button-primary-hover:
    backgroundColor: "{colors.dark-accent-hover}"
  button-primary-active:
    backgroundColor: "{colors.dark-accent-active}"
  button-primary-light:
    backgroundColor: "{colors.light-accent}"
    textColor: "{colors.light-bg-secondary}"
    typography: "{typography.button}"
    rounded: "{rounded.square}"
    padding: "15px 23px"
    height: "54px minimum"
  text-link:
    typography: "{typography.text-link}"
    height: "44px minimum"
  input:
    backgroundColor: "{colors.dark-bg}"
    textColor: "{colors.dark-text}"
    typography: "{typography.body}"
    rounded: "{rounded.square}"
    padding: "12px 14px"
    height: "50px minimum"
  workflow-container:
    backgroundColor: "{colors.dark-surface}"
    rounded: "{rounded.square}"
    padding: "34px 32px 32px"
  calculator-form:
    backgroundColor: "{colors.dark-surface}"
    rounded: "{rounded.square}"
    padding: "32px"
---

# Design System: MOHAPX-V-IT

## 21st.dev effects, October 2026

The home page adds four effects adapted to the existing buildless architecture:
curved, sliced open-source project covers; animated paths behind the hero;
orange conic-gradient button edges; and a large, cropped halftone footer
wordmark with pointer springs and a click wave. Buttons use 32px corners as
an intentional exception to the original square primary button token.
Existing copy, crown geometry, project disclosure and local fonts remain.
The GitHub section follows the existing ruled layout and uses real dated data,
orange activity levels and keyboard-accessible day exploration. The month grid
scrolls inside its own container on small screens. Motion respects the system
preference and a dedicated effects pause button; canvas rendering sleeps offscreen
and after the springs settle. Journal and calculator do not load the effects.

## Overview

**Creative North Star: "The Engineer's Agency"**

The shipped home page and calculator combine the spacious agency composition of the user-pinned Comblock reference with MOHAPX-V-IT's existing orange palette and crown. Large Manrope headings, asymmetric columns, restrained surfaces and ruled editorial rows give the work room to speak. The crown provides the main expressive object; the content below uses clear reading order and native controls.

The identity retains its own geometry and wordmark. Manrope carries the interface and narrative; Unbounded remains in the brand lockup. Both font families are self-hosted. Dark and light are complete theme pairs, and Russian and English share the same structure. This record covers the redesigned home page and calculator shell. The journal and its article pages intentionally retain the frozen legacy design; they are not examples of this system.

The portfolio is positioned as AI Forward Deployed Engineering: the compact header reads “AI FDE / Full-stack”, while the about section expands the title. Cases connect customer needs, stakeholder alignment, engineering, rollout and observed results. Historical job titles remain factual; Salvim is still recorded as AI Engineer / Full-stack with internal customers. The visual system and crown are unchanged by this content update.

**Key Characteristics:**

- Large, tightly spaced Manrope headlines with generous section intervals.
- Orange emphasis against near-black or warm paper neutrals.
- Clipped brand geometry, square surfaces and fine horizontal rules.
- Editorial project disclosures rather than a repeated card grid.
- One metallic crown object, with user-controlled and preference-aware motion.

## Colors

Orange is the single interface accent; dark charcoal and warm paper provide two complete neutral contexts. Frontmatter retains the source CSS formats and owns the exact values.

### Primary

- **Crown Orange:** `dark-accent` marks the final hero line, links, buttons, results, employer names and expert workflow step. `dark-accent-hover` and `dark-accent-active` are control states.
- **Burnt Orange:** the corresponding light accent family is darker for use against warm paper. Treat it as the same role in the light theme, rather than an additional accent.

### Neutral

- **Near Black / Warm Paper:** the background pair is the page ground. The secondary background pair defines the wide principle section and supplies the light button text.
- **Charcoal / Warm Stone:** the surface pair groups the header controls, workflow, calculator form and verdict.
- **Pale Ink / Deep Ink:** the text pair carries primary copy and headings. The muted pair carries explanations and metadata.
- **Fine Rules:** the translucent line pair separates rows, sections and fields; its opacity belongs to the active theme.

**The Paired Theme Rule.** Switch the entire accent, ground, surface, text and divider family together. New surfaces inherit the existing CSS variables and persisted theme state.

## Typography

**Display Font:** Manrope, with system-ui and sans-serif fallbacks.

**Body Font:** Manrope, with the same fallbacks.

**Brand Font:** Unbounded, with the body stack as fallback.

**Character:** The hierarchy comes from scale, weight and tight headline spacing. Body copy and metadata stay calm; the wordmark supplies a separate identity voice without becoming the display face.

### Hierarchy

- **Display:** the three-line opening uses the frontmatter display role; the contact heading grows to a larger clamp. At mobile width the opening becomes `clamp(32px, 7.95vw, 59px)` with a more open line height (1.1).
- **Headline:** section headings use the frontmatter headline role. The about heading and calculator title have larger contextual variants. Mobile section headings use (36px) and line height (1.15).
- **Title:** project and experience titles use the title role; featured work is larger. Mobile project disclosure titles use (21px).
- **Body:** the base role becomes (15px / 1.65) at mobile width. Expanded project paragraphs use (17px / 1.65) on desktop. Long project and experience descriptions have observed limits around (72–75ch).
- **Intro:** section explanations use the intro role, generally bounded to (760px). The hero introduction uses the same size with line height (1.6).
- **Label:** metadata and text-only tags use the metadata role. Button and text-link roles keep actions distinct without uppercase interface copy.
- **Wordmark:** Unbounded is reserved for the header and footer lockups; its compact responsive sizes are local to those lockups.

**The Brand Voice Rule.** Use Manrope for large statements and reading; reserve Unbounded for the identity lockup.

## Layout

The main content and header share a maximum width (1536px) and fluid side gutters from the frontmatter. Major sections use a top rule and the section spacing role. The desktop page uses unequal columns and deliberately different alignments: narrative beside portrait, project explanation beside workflow, dates beside experience, and categories beside stack entries. Project disclosures indent their body to (33%) on desktop.

At widths up to (1100px), section padding contracts to (88px), columns tighten and header proportions shrink. At (760px), the page uses the mobile gutter and section spacing roles; most content grids become one column, project body indentation disappears, and the hero crown moves into the normal reading flow between headline and introduction. Below (360px), gutters contract to (16px). At wide screens from (1600px), the hero receives more vertical room. A separate desktop rule for heights up to (800px) fits the opening, crown and introduction to a short viewport.

The calculator reuses the shell but favors operation: a form column capped at (420px), a results column, and a gap (7%). These become one column at (900px). Results retain a two-column internal grid. The result region is sticky on wider screens and becomes static with the one-column layout.

**The Editorial Row Rule.** Use horizontal separators and aligned information for repeated projects, experience and tools. Preserve native disclosures and the established mobile reading order.

## Elevation & Depth

Content surfaces are flat, with depth supplied by neutral tone changes and fine rules. The dropdown menu alone uses a diffuse shadow (`0 24px 48px -20px rgba(0,0,0,.38)`) to sit above the document. The 3D crown is the expressive depth element: its orange metallic face and lighter edge material use local studio lighting. These material colors are scene values, not extra interface accent tokens.

**The Object Depth Rule.** Keep recurring content flat; concentrate physical depth in the original crown and functional menu overlay.

## Shapes

Buttons, fields and content surfaces use square corners. The brand block has clipped left corners (18px on desktop); on mobile, the combined header carries a smaller version of the same cut (14px). The crown preserves the original polygon and detached rounded base. Its geometry is an identity exception to the square interface surfaces, not a reusable card shape.

Tags and stack items are plain text separated by spacing. Existing class names suggesting pills do not imply rounded chip containers.

## Components

### Buttons

Primary actions are square orange blocks with dark text in the dark theme and pale text in the light theme. The arrow and label are separated by a generous gap (32px). Hover changes the accent state and moves the SVG arrow (4px); active uses the deep accent state. Calculator actions use the same square silhouette, with a bordered ghost variant. Keyboard focus uses an accent outline (2px) offset (5px); disabled buttons reduce opacity (.5).

### Text Links and Tags

Text links have an SVG arrow, a gap (24px), a minimum target height (44px), and accent hover. Project tags and stack items remain text, wrapping through flex layout without decorative containers.

### Cards / Containers

The project workflow, calculator form and verdict group related information with the surface color and no border radius or content shadow. Other repeated records remain ruled rows. The workflow uses ordered text steps and down-facing SVG arrows, highlighting its expert step in orange.

### Inputs / Fields

Calculator number fields use the page ground inside the surface-colored form, square corners, a fine border, body typography and a minimum height (50px). Labels sit above the field and hints below. Focus changes the border to the accent. The calculator override removes the legacy field glow and outline, so the shipped field focus treatment is its border change; do not describe a ring that the cascade does not render.

### Navigation

The sticky header separates the crown-and-wordmark block, grouped language/theme/menu controls and desktop contact action. The dropdown has two link columns on desktop and one on mobile; mobile hides the separate contact button and the menu text label. Its button exposes expanded state. Escape closes the menu and returns focus; outside click, focus leaving the header and link activation also close it. Theme and language persist using the existing local-storage keys.

### Project Disclosures

Native `details` and `summary` provide expansion and keyboard behavior. Metadata precedes the title; a drawn plus becomes a minus when open. Hovered and open titles take the accent color. Mobile retains the plus control and hides its descriptive text while expanding the body at full width.

### Crown

One Three.js group assembles extruded versions of the existing crown body and base into a single rotating identity object. The renderer uses self-hosted Three.js (0.180.0), an authored local environment, and no external HDRI. Rotation completes a turn in about (28s), with a small secondary tilt. Pause/resume is available after a successful mount; reduced motion starts it paused. Rendering pauses when offscreen or when the document is hidden. A static SVG remains the fallback if modules, WebGL or its context are unavailable. The sidecar previews this fallback, not a second 3D implementation.

## Do's and Don'ts

### Do:

- **Do** retain the original orange theme roles and crown geometry.
- **Do** use the shared self-hosted fonts, theme variables and persisted language/theme controls.
- **Do** keep repeated portfolio records as readable ruled rows with native disclosures.
- **Do** carry the mobile reading order and preference-aware crown motion onto related surfaces.
- **Do** use SVG or drawn geometry for interface icons, following the redesigned header and project controls.

### Don't:

- **Don't** turn plain text tags or stack items into a new pill system.
- **Don't** extend the clipped brand silhouette into every content container.
- **Don't** infer current design tokens from the frozen journal or legacy stylesheet embedded in the calculator; the current cascade is authoritative.
- **Don't** inherit legacy calculator glyph icons or hidden terminal-style eyebrows as a house style. They remain non-canonical legacy details.
- **Don't** substitute a different crown, copied reference identity or additional interface accent family.
## Interactive motion

The original rotating crown remains the focal motion. The navigation uses interruptible opacity and translate animations (300 ms entrance, 180 ms exit). Project rows and calculator FAQs retain native details as a no-script fallback; progressively enhanced grid disclosures follow natural content height (360 ms opening, 240 ms closing), including language and viewport changes. Closing content becomes inert immediately. Buttons have a small press response and directional arrows; theme colours transition for 280 ms. Reduced-motion preferences disable these transitions and settle any animation already in progress. Reading sections stay visible and still.

## Current home page: MOHAPX / Fieldwork

The current home page supersedes the original agency composition while retaining
the MOHAPX crown, Manrope, warm accent and two themes. Dark: charcoal-green
#111210 with warm white #f1f0e9 and apricot #ff9459. Light: paper #f4f2eb with
ink #20221b and burnt orange #b74b17. JetBrains Mono is reserved for small
engineering annotations; Manrope carries readable content. The orange contact
panel closes the narrative. No scroll hijacking, autoplay video or cursor replacement.

The portrait is an editorial print with an annotation and small crown seal.
The three selected cases pair a short business explanation with authored process
diagrams, not fake screenshots. Project filters preserve native detail disclosure.
A restrained spotlight, a four-stage scroll rail, tiny magnetic CTA movement and
brief heading reveals are adapted from the selected 21st.dev sources.
The motion toggle covers the crown, card band, calendar reveal and heading motion.

Default spacing is 100px per major section, 64px on mobile. Main content is
limited to 1400px including gutters. Header exposes primary destinations on
desktop; the full menu remains keyboard accessible. Deep history is disclosed
on request so the main journey is substantially shorter. The previous token
block documents the shared calculator shell, not the current portfolio overrides.
