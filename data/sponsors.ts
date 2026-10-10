import type { StaticImageData } from "next/image";
import teferLogo from "@/public/assets/partners/tefer-logo-white.png";
import simaLogo from "@/public/assets/partners/sima.png";
import senayGebrePhoto from "@/public/assets/partners/senay-gebre.jpg";

export type SponsorCapability = {
  title: string;
  description: string;
};

export type Sponsor = {
  name: string;
  slug: string;
  tier: "Official Event Partner" | "Lead Sponsor" | "Community Sponsor" | "Supporter";
  href?: string;
  logo: string | StaticImageData;
  avatar?: boolean;
  tagline?: string;
  description?: string;
  overview?: string;
  capabilities?: SponsorCapability[];
  linkLabel?: string;
};

export const sponsors: Sponsor[] = [
  {
    name: "Tefer",
    slug: "tefer",
    tier: "Official Event Partner",
    href: "https://tefer.io/",
    logo: teferLogo,
    tagline: "Developer connectivity, venue operations, and community infrastructure",
    description:
      "Primary event partner supporting developer connectivity, venue operations, and community logistics for Omarchy Ethiopia Meetup 2026.",
    linkLabel: "Visit tefer.io",
  },
  {
    name: "SIMA",
    slug: "sima",
    tier: "Lead Sponsor",
    href: "https://sima.to/pilot",
    logo: simaLogo,
    tagline: "Enterprise Voice AI that answers every call, in your language",
    description:
      "SIMA answers customers' calls in their own language, resolves requests on the spot, and hands off to a person only when it truly needs one.",
    overview:
      "SIMA builds enterprise voice AI tailored for African languages. Teams can learn more at sima.to and join the pilot waitlist to get started.",
    capabilities: [
      {
        title: "Handle inbound calls",
        description:
          "Automate high-volume incoming phone calls with real-time, responsive voice AI speaking native African languages.",
      },
      {
        title: "Handle outbound calls for marketing",
        description:
          "Launch intelligent outbound campaigns for marketing outreach, personalized announcements, and customer engagement.",
      },
      {
        title: "Human hand-off when task is hard",
        description:
          "Resolve requests automatically and route only complex conversations or high-touch tasks to human agents with context preserved.",
      },
      {
        title: "Custom API integration",
        description:
          "Integrate seamlessly into existing CRMs, telecommunication gateways, custom databases, and internal workflows.",
      },
    ],
    linkLabel: "Join SIMA pilot waitlist",
  },
  {
    name: "Tauon Labs",
    slug: "tauonlabs",
    tier: "Lead Sponsor",
    href: "https://tauonlabs.com",
    logo: "/assets/partners/tauonlabs-logo.jpeg",
    tagline: "Product lab building SaaS products and incubating ideas from the ground up",
    description:
      "Tauon Labs is supporting Omarchy Ethiopia Meetup 2026 as a Lead Sponsor to help grow the local tech community and connect with talented builders.",
    overview:
      "Tauon Labs is a product-focused lab building SaaS products and incubating ideas from the ground up. Through this sponsorship, the team is supporting local builders while sharing what they are creating.",
    linkLabel: "Visit tauonlabs.com",
  },
  {
    name: "Senay Gebre",
    slug: "senay-gebre",
    tier: "Supporter",
    href: "https://senay-portfolio.vercel.app/",
    logo: senayGebrePhoto,
    avatar: true,
    tagline: "Senior Mobile Engineer | Flutter & Dart",
    description:
      "Senior Mobile Engineer supporting Omarchy Ethiopia Meetup 2026 as an individual Supporter. He was previously Senior Mobile Technologies Developer at Commercial Bank of Qatar.",
    overview:
      "Senay Gebre is a Senior Mobile Engineer with 6+ years of software development experience, including end-to-end delivery of corporate mobile and internet banking at Commercial Bank of Qatar alongside contributions to its retail digital channels. As CEO and CTO of 888 Software Systems, he architected and built 888 Market from scratch, live on web, Android and iOS, and leads ETH Pass digital identity and e-government platform work.",
    capabilities: [
      {
        title: "Corporate banking delivery",
        description:
          "Led Flutter/Dart delivery for Corporate Internet Banking and Corporate Mobile Banking at Commercial Bank of Qatar, from planning and architecture through testing and production release.",
      },
      {
        title: "Flutter architecture & resilient checkout",
        description:
          "Built 888 Market checkout recovery with durable order intents, idempotent submissions and cart-revision checks, plus shared Flutter packages and server-driven storefronts.",
      },
      {
        title: "Secure native integrations",
        description:
          "Implemented SQLCipher-backed local databases and biometric signing with Android Keystore and iOS Secure Enclave, with unit, widget and buyer-journey tests in CI.",
      },
      {
        title: "Payments, identity & commerce",
        description:
          "Designed a Go modular monolith for inventory, orders and payments with double-entry ledger controls, and leads ETH Pass national digital identity plus ETH Tenant and ETH Police workflows.",
      },
    ],
    linkLabel: "Visit portfolio",
  },
];
