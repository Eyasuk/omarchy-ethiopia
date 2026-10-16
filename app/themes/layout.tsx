import type { Metadata } from "next";
import themesData from "../../data/themes.json";

const themeCount = themesData.length;

export const metadata: Metadata = {
  title: "Ethiopian Theme Competition",
  description: `Vote for your favourite Ethiopian Omarchy theme. ${themeCount} community-built themes competing for a 10,000 ETB prize pool, ranked live by community votes.`,
  openGraph: {
    title: "Ethiopian Theme Competition",
    description: `Vote for your favourite Ethiopian Omarchy theme — ${themeCount} community-built themes ranked live by community votes.`,
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Ethiopian Theme Competition",
    description: `Vote for your favourite Ethiopian Omarchy theme — ${themeCount} community-built themes ranked live by community votes.`,
  },
};

export default function ThemesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
