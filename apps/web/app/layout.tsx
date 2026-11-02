import type { ReactNode } from "react";
import "./globals.css";

export default function Layout({ children }: { children: ReactNode }) {
  return <html lang="it"><body>{children}</body></html>;
}
