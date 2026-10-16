import bakedScores from "@/data/theme-scores.json";
import type { Theme } from "./useThemeVotes";

export const JUDGE_WEIGHT = 0.5;
export const COMMUNITY_WEIGHT = 0.5;

type BakedScores = {
  updatedAt?: string | null;
  scale?: Record<string, string>;
  judges?: string[];
  scores?: Record<string, { average?: number; count?: number }>;
};

const baked = bakedScores as BakedScores;

export const judgePanel: string[] = baked.judges ?? [];

export const judgeScale: string[] = baked.scale
  ? Object.keys(baked.scale)
      .sort()
      .map((key) => baked.scale?.[key] ?? "")
      .filter(Boolean)
  : [];

export const judgeUpdatedAt: number | null = baked.updatedAt
  ? Date.parse(baked.updatedAt)
  : null;

export function hasJudgeScores(): boolean {
  return Object.keys(baked.scores ?? {}).length > 0;
}

export function judgeAverage(themeId: string): number | null {
  const entry = baked.scores?.[themeId];
  return typeof entry?.average === "number" ? entry.average : null;
}

export type Standing = {
  theme: Theme;
  votes: number;
  communityScore: number;
  judgeScore: number | null;
  finalScore: number;
  rank: number;
};

export function computeStandings(
  themes: Theme[],
  votes: Record<string, number>,
): Standing[] {
  const counts = themes.map((theme) => votes[theme.id] ?? 0);
  const maxVotes = Math.max(1, ...counts);
  const judgesPresent = hasJudgeScores();

  const rows: Standing[] = themes.map((theme) => {
    const themeVotes = votes[theme.id] ?? 0;
    const communityScore = (themeVotes / maxVotes) * 100;
    const judgeScore = judgeAverage(theme.id);
    const finalScore =
      judgesPresent && judgeScore !== null
        ? JUDGE_WEIGHT * judgeScore + COMMUNITY_WEIGHT * communityScore
        : communityScore;

    return {
      theme,
      votes: themeVotes,
      communityScore,
      judgeScore,
      finalScore,
      rank: 0,
    };
  });

  rows.sort(
    (a, b) =>
      b.finalScore - a.finalScore || a.theme.name.localeCompare(b.theme.name),
  );
  rows.forEach((row, index) => {
    row.rank = index + 1;
  });

  return rows;
}
