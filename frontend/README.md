# Frontend

React 19 + TypeScript + Vite single-page app, styled with Tailwind CSS v4.
See the [root README](../README.md) for setup instructions.

```bash
npm install
npm run dev     # http://localhost:5173
npm run lint
npm run build
```

In development the Vite server proxies `/api` to the backend at `API_PROXY_TARGET` (default `http://localhost:8000`), so no CORS setup is needed. See `.env.example` for calling a backend on another origin.
