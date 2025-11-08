# Static Files Directory

This directory contains the frontend static files for Black Sultan OS.

## Structure

- `index.html` - Main HTML entry point
- `favicon.ico` - Application favicon
- `assets/` - Compiled frontend assets
  - `index-*.js` - JavaScript bundle
  - `index-*.css` - CSS bundle

## Frontend Technology

The frontend is built with:
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Recharts for data visualization

## Development

Frontend source code should be developed separately and compiled into this directory.
The production build artifacts in `assets/` are served by the Flask backend.
