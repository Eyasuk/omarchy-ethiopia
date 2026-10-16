"use client";

import { useCallback, useEffect, useState } from "react";
import bakedVotes from "@/data/theme-votes.json";

const REPO = "nebiyuelias1/omarchy-ethiopia";
const LABEL = "theme-competition";

const POSITIVE_REACTIONS = ["+1", "heart", "hooray", "rocket", "laugh"] as const;

export type Theme = {
  id: string;
  issue?: number;
  name: string;
  author: string;
  category: string;
  link: string;
  screenshot?: string;
  tags?: string[];
};

export type ThemeVotes = {
  votes: Record<string, number>;
  loading: boolean;
  live: boolean;
  error: string | null;
  updatedAt: number | null;
  refresh: () => void;
};

type Reactions = Record<string, number>;

type BakedVotes = {
  updatedAt?: string;
  votes?: Record<string, number>;
};

const baked = bakedVotes as BakedVotes;
const BAKED_VOTES: Record<string, number> = baked.votes ?? {};
const BAKED_UPDATED_AT: number | null = baked.updatedAt
  ? Date.parse(baked.updatedAt)
  : null;

export function voteIssueUrl(theme: Theme): string | undefined {
  if (typeof theme.issue !== "number") return undefined;
  return `https://github.com/${REPO}/issues/${theme.issue}`;
}

function countVotes(reactions: Reactions): number {
  return POSITIVE_REACTIONS.reduce(
    (total, key) => total + (reactions[key] ?? 0),
    0,
  );
}

async function fetchLiveVotes(
  themes: Theme[],
): Promise<{ votes: Record<string, number>; updatedAt: number }> {
  const res = await fetch(
    `https://api.github.com/repos/${REPO}/issues?state=all&labels=${LABEL}&per_page=100`,
    { headers: { Accept: "application/vnd.github+json" } },
  );
  if (!res.ok) {
    throw new Error(`GitHub returned ${res.status}`);
  }

  const issues = (await res.json()) as Array<{
    number: number;
    pull_request?: unknown;
    reactions?: Reactions;
  }>;

  const byNumber = new Map<number, number>();
  for (const issue of issues) {
    if (issue.pull_request) continue;
    byNumber.set(issue.number, countVotes(issue.reactions ?? {}));
  }
  if (byNumber.size === 0) {
    throw new Error("No theme issues returned");
  }

  const votes: Record<string, number> = {};
  for (const theme of themes) {
    if (typeof theme.issue !== "number") continue;
    votes[theme.id] = byNumber.get(theme.issue) ?? 0;
  }

  return { votes, updatedAt: Date.now() };
}

export function useThemeVotes(themes: Theme[]): ThemeVotes {
  const [votes, setVotes] = useState<Record<string, number>>(BAKED_VOTES);
  const [updatedAt, setUpdatedAt] = useState<number | null>(BAKED_UPDATED_AT);
  const [live, setLive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [nonce, setNonce] = useState(0);

  useEffect(() => {
    let active = true;

    fetchLiveVotes(themes)
      .then((snapshot) => {
        if (!active) return;
        setVotes(snapshot.votes);
        setUpdatedAt(snapshot.updatedAt);
        setLive(true);
        setError(null);
      })
      .catch((err: unknown) => {
        if (!active) return;
        setLive(false);
        setError(
          err instanceof Error ? err.message : "Live votes unavailable",
        );
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [themes, nonce]);

  const refresh = useCallback(() => {
    setLoading(true);
    setNonce((value) => value + 1);
  }, []);

  return { votes, loading, live, error, updatedAt, refresh };
}
