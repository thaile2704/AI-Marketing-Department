import type { ReactNode } from 'react';
import './style.css';
export const metadata = { title: 'AI Marketing Control Center', description: 'Hybrid AI Marketing Department' };
export default function RootLayout({ children }: { children: ReactNode }) { return <html lang="en"><body>{children}</body></html>; }
