---
name: Lumen Brutalist
colors:
  primary: "#4ECDC4"
  secondary: "#F76132"
  base-white: "#FFFFFF"
  base-black: "#000000"
  success: "#22C55E"
  danger: "#EF4444"
  warning: "#F59E0B"
  info: "#0EA5E9"
typography:
  body:
    fontFamily: Red Hat Mono
    fontSize: 14px
    fontWeight: 400
  navigation:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
border:
  width: 3px
  style: solid
  color: "#000000"
shadow:
  offsetX: 4px
  offsetY: 4px
  blur: 0px
---

# Design System — Lumen

## Overview

A brutalist, high-contrast financial management interface. Bold borders, hard shadows, monospaced typography. Inspired by terminal UIs and early web brutalism.

## Colors

- **Primary** (#4ECDC4 turquoise): CTAs, active states, key interactive elements, headers
- **Secondary** (#F76132 orange): Supporting actions, alerts, scan mode
- **Feedback**: success (#22C55E), danger (#EF4444), warning (#F59E0B), info (#0EA5E9)
- **Base**: White (#FFFFFF) backgrounds, Black (#000000) text and borders

## Typography

- **Primary**: Red Hat Mono (monospaced) for all body text, labels, and UI
- **Navigation**: Inter (sans-serif) for bottom tab labels only
- **Sizes**: 12px–16px range; high contrast, no font smoothing

## Components

- **Buttons**: 3px black border, hard 4px shadow, no border-radius
- **Inputs**: 3px black border, monospaced text, white background
- **Cards**: 3px black border, hard 4px shadow, clear background
- **Status badges**: Colored indicator dot + monospaced label

## Do's and Don'ts

- Do use thick black borders (3px) on all interactive elements
- Do use hard shadows (4px offset, 0 blur) — never blurred shadows
- Don't use rounded corners anywhere
- Don't use gradients or elevated surfaces
- Do maintain high contrast (black on white) for all text
- Do use the primary turquoise sparingly for emphasis
