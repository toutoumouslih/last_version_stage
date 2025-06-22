import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import type { ProxyOptions } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path: string) => path,
        configure: (proxy: any, _options: ProxyOptions) => {
          proxy.on('error', (err: Error) => {
            // eslint-disable-next-line no-console
            console.error('proxy error', err);
          });
          proxy.on('proxyReq', (_proxyReq: any, req: any) => {
            // eslint-disable-next-line no-console
            console.log('Sending Request to:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes: any, req: any) => {
            // eslint-disable-next-line no-console
            console.log('Received Response:', proxyRes.statusCode, req.url);
          });
        },
      },
    },
  },
})
