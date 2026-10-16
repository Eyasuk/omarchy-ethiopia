"use client";

import Image from "next/image";
import { ExternalLink, RefreshCw, ThumbsUp, Trophy } from "lucide-react";
import type { Theme } from "./useThemeVotes";
import { voteIssueUrl } from "./useThemeVotes";

type ThemeLeaderboardProps = {
  themes: Theme[];
  votes: Record<string, number>;
  loading: boolean;
  live: boolean;
  error: string | null;
  updatedAt: number | null;
  onRefresh: () => void;
};

function rankStyles(rank: number): string {
  if (rank === 1) return "border-tibeb-gold/60 bg-tibeb-gold text-black";
  if (rank === 2) return "border-white/25 bg-white/15 text-white";
  if (rank === 3) return "border-ethiopia-green/50 bg-ethiopia-green/15 text-ethiopia-green";
  return "border-white/15 bg-white/[0.03] text-cream/70";
}

function formatTime(timestamp: number): string {
  return `${new Date(timestamp).toISOString().slice(11, 16)} UTC`;
}

export default function ThemeLeaderboard({
  themes,
  votes,
  loading,
  live,
  error,
  updatedAt,
  onRefresh,
}: ThemeLeaderboardProps) {
  const ranked = [...themes]
    .map((theme) => ({ theme, count: votes[theme.id] ?? 0 }))
    .sort(
      (a, b) => b.count - a.count || a.theme.name.localeCompare(b.theme.name),
    );

  const maxVotes = Math.max(1, ...ranked.map((entry) => entry.count));
  const leader = ranked[0];
  const hasVotes = ranked.some((entry) => entry.count > 0);

  return (
    <section
      id="leaderboard"
      className="mt-12 scroll-mt-20 rounded-2xl border border-white/10 bg-[#0b0c11] p-5 sm:p-7"
    >
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="flex items-center gap-2 text-lg font-bold tracking-tight text-white sm:text-xl">
            <Trophy className="h-5 w-5 text-tibeb-gold" />
            <span>Live Leaderboard</span>
          </h2>
          <p className="mt-1 text-xs text-cream/60 sm:text-sm">
            Community votes via GitHub reactions. React on a theme&apos;s issue
            to move it up.
          </p>
        </div>

        <div className="flex items-center gap-3 font-mono text-[11px]">
          {live ? (
            <span className="inline-flex items-center gap-1.5 rounded-full border border-ethiopia-green/40 bg-ethiopia-green/10 px-3 py-1 font-bold tracking-wider text-ethiopia-green">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-ethiopia-green" />
              LIVE
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 rounded-full border border-white/20 bg-white/[0.03] px-3 py-1 font-bold tracking-wider text-cream/60">
              SYNCED
            </span>
          )}
          {loading ? (
            <span className="text-cream/50">updating…</span>
          ) : updatedAt ? (
            <span className="text-cream/50">{formatTime(updatedAt)}</span>
          ) : null}
          <button
            type="button"
            onClick={onRefresh}
            disabled={loading}
            className="inline-flex items-center gap-1.5 rounded-lg border border-white/15 bg-white/[0.03] px-3 py-1 text-cream/80 transition hover:border-tibeb-gold hover:text-tibeb-gold disabled:cursor-not-allowed disabled:opacity-50"
          >
            <RefreshCw className={`h-3 w-3 ${loading ? "animate-spin" : ""}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {!live && error && (
        <p className="mt-4 rounded-lg border border-tibeb-gold/30 bg-tibeb-gold/5 px-4 py-3 font-mono text-xs text-cream/70">
          Live GitHub votes are unavailable right now, so these are the last
          synced totals
          {updatedAt ? ` (${formatTime(updatedAt)})` : ""}. They refresh
          automatically.
        </p>
      )}

      {leader && hasVotes && (
        <div className="mt-5 rounded-xl border border-tibeb-gold/40 bg-gradient-to-r from-tibeb-gold/15 to-transparent p-4">
          <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-tibeb-gold">
            Currently winning
          </p>
          <div className="mt-2 flex items-baseline gap-3">
            <span className="text-xl font-bold text-white sm:text-2xl">
              {leader.theme.name}
            </span>
            <span className="font-mono text-sm text-cream/60">
              {leader.count} {leader.count === 1 ? "vote" : "votes"}
            </span>
          </div>
        </div>
      )}

      <ol className="mt-5 space-y-2.5">
        {ranked.map(({ theme, count }, index) => {
          const rank = index + 1;
          const issueUrl = voteIssueUrl(theme);
          const width = count > 0 ? Math.max(6, (count / maxVotes) * 100) : 0;

          return (
            <li
              key={theme.id}
              className={`flex flex-wrap items-center gap-3 rounded-xl border p-3 transition sm:gap-4 sm:p-4 ${
                rank === 1
                  ? "border-tibeb-gold/40 bg-[#0e0f14]"
                  : "border-white/10 bg-[#0e0f14]"
              }`}
            >
              <span
                className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border font-mono text-sm font-bold ${rankStyles(rank)}`}
              >
                {rank}
              </span>

              <div className="relative hidden h-11 w-20 shrink-0 overflow-hidden rounded-md bg-[#0b0c11] ring-1 ring-white/10 sm:block">
                {theme.screenshot ? (
                  <Image
                    src={theme.screenshot}
                    alt={`${theme.name} theme screenshot`}
                    fill
                    sizes="80px"
                    className="object-cover"
                  />
                ) : (
                  <span className="flex h-full w-full items-center justify-center font-mono text-base font-bold text-tibeb-gold/30">
                    {theme.name.charAt(0)}
                  </span>
                )}
              </div>

              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-medium text-white">
                  {theme.name}
                </p>
                <p className="truncate font-mono text-[11px] text-cream/50">
                  {theme.author}
                </p>
              </div>

              <div className="flex w-full items-center gap-3 sm:w-auto sm:min-w-[9rem]">
                <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/10">
                  <div
                    className="h-full rounded-full bg-tibeb-gold transition-all duration-500"
                    style={{ width: `${width}%` }}
                  />
                </div>
                <span className="w-20 text-right font-mono text-sm font-bold text-cream">
                  {loading && !(theme.id in votes) ? "…" : `${count}`}
                  <span className="ml-1 text-[11px] font-normal text-cream/50">
                    {count === 1 ? "vote" : "votes"}
                  </span>
                </span>
              </div>

              {issueUrl && (
                <a
                  href={issueUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex shrink-0 items-center gap-1.5 rounded-lg border border-tibeb-gold/40 bg-tibeb-gold/10 px-3 py-2 font-mono text-xs font-bold text-tibeb-gold transition hover:bg-tibeb-gold hover:text-black focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-tibeb-gold"
                >
                  <ThumbsUp className="h-3.5 w-3.5" />
                  <span>Vote</span>
                  <ExternalLink className="h-3 w-3 opacity-60" />
                </a>
              )}
            </li>
          );
        })}
      </ol>

      {ranked.length === 0 && (
        <p className="mt-5 rounded-lg border border-white/10 bg-[#0e0f14] p-6 text-center font-mono text-sm text-cream/60">
          No themes to rank yet.
        </p>
      )}
    </section>
  );
}
