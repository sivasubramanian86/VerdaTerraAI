# VerdaTerraAI Dashboard

React/Vite dashboard for the VerdaTerraAI civic hygiene command-center and inspector workflows.

## Local Development

```bash
npm install
npm run lint
npm run build
npm run dev
```

## Accessibility Checklist

- Keep visible labels on every report form input.
- Preserve descriptive `alt` text for dashboard imagery.
- Use native buttons, inputs, and selects for keyboard support.
- Do not remove focus outlines.
- Pair status colors with text labels so risk is not color-only.
- Keep `prefers-reduced-motion` support in CSS when adding animations.

## Evaluator Notes

The UI is part of the project evaluation surface. Before submission, run `npm run lint` and `npm run build`, then manually confirm the report workflow can be completed with keyboard navigation and that text remains readable at mobile and desktop widths.
