import type { Metadata } from "next";
import themesData from "../../data/themes.json";

const themeCount = themesData.length;

export const metadata: Metadata = {
  title: `${themeCount} Themes`,
  description: `Discover ${themeCount} community themes for Omarchy Linux shared by the Ethiopian Omarchy community. Customize your desktop with new visual styles.`,
  openGraph: {
    title: `${themeCount} Omarchy Themes`,
    description: `Discover ${themeCount} community themes for Omarchy Linux shared by the Ethiopian Omarchy community.`,
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: `${themeCount} Omarchy Themes`,
    description: `Discover ${themeCount} community themes for Omarchy Linux shared by the Ethiopian Omarchy community.`,
  },
};

export default function ThemesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
