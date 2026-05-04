import { useEffect, useRef, useState } from 'react'

/* ─── Grade config ─────────────────────────────────────────────────── */
const GRADE_STYLES = {
  A: { badge: 'bg-emerald-500 text-white shadow-emerald-200', label: 'Excellent' },
  B: { badge: 'bg-blue-500 text-white shadow-blue-200', label: 'Good' },
  C: { badge: 'bg-yellow-500 text-white shadow-yellow-200', label: 'Average' },
  D: { badge: 'bg-orange-500 text-white shadow-orange-200', label: 'Below Average' },
  F: { badge: 'bg-red-500 text-white shadow-red-200', label: 'Poor' },
}

/* ─── Engine config ─────────────────────────────────────────────────── */
const ENGINE_LABELS = {
  openai: 'ChatGPT',
  claude: 'Claude',
  gemini: 'Gemini',
}

const ENGINE_DOTS = {
  openai: 'bg-green-500',
  claude: 'bg-orange-500',
  gemini: 'bg-blue-500',
}

/* ─── Rank pill config ──────────────────────────────────────────────── */
const RANK_PILL = {
  high: 'bg-emerald-100 text-emerald-700',
  medium: 'bg-yellow-100 text-yellow-700',
  low: 'bg-red-100 text-red-700',
}

const RANK_BAR = {
  high: 'bg-emerald-500',
  medium: 'bg-yellow-400',
  low: 'bg-red-500',
}

/* ─── GradeBadge ────────────────────────────────────────────────────── */
function GradeBadge({ grade }) {
  const style = GRADE_STYLES[grade] ?? GRADE_STYLES['F']
  return (
    <span
      id="grade-badge"
      className={`inline-flex h-20 w-20 items-center justify-center rounded-full text-4xl font-bold shadow-lg ${style.badge}`}
    >
      {grade}
    </span>
  )
}

/* ─── ScoreBar with animated fill ───────────────────────────────────── */
function ScoreBar({ score }) {
  const pct = Math.round(score)
  const barColor = pct > 70 ? 'bg-green-500' : pct > 40 ? 'bg-yellow-400' : 'bg-red-500'
  const [width, setWidth] = useState(0)

  useEffect(() => {
    // Delay slightly so CSS transition fires after mount
    const t = setTimeout(() => setWidth(pct), 80)
    return () => clearTimeout(t)
  }, [pct])

  return (
    <div className="w-full">
      <div className="mb-1 flex justify-between text-xs text-gray-500">
        <span>AI Visibility Score</span>
        <span className="font-semibold text-gray-700">{pct} / 100</span>
      </div>
      <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200">
        <div
          id="score-bar"
          className={`h-3 rounded-full ${barColor}`}
          style={{ width: `${width}%`, transition: 'width 1s ease-out' }}
        />
      </div>
    </div>
  )
}

/* ─── EnginesTable ──────────────────────────────────────────────────── */
function EnginesTable({ engines }) {
  const rows = Object.entries(engines)
  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200">
      <table id="engines-table" className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-gray-50">
          <tr>
            {['Engine', 'Mention Rate', 'Rank', 'Tip'].map((h) => (
              <th
                key={h}
                className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500"
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100 bg-white">
          {rows.map(([key, data]) => {
            const mentionPct = Math.round((data.mention_rate ?? 0) * 100)
            const rank = (data.rank ?? 'low').toLowerCase()
            const rankClass = RANK_PILL[rank] ?? RANK_PILL['low']
            const barClass = RANK_BAR[rank] ?? RANK_BAR['low']
            const dotClass = ENGINE_DOTS[key] ?? 'bg-gray-400'

            return (
              <tr key={key} className="hover:bg-gray-50 transition-colors">
                {/* Engine name + dot */}
                <td className="whitespace-nowrap px-4 py-3 font-medium text-gray-800">
                  <div className="flex items-center gap-2">
                    <span className={`inline-block h-2.5 w-2.5 rounded-full ${dotClass}`} />
                    {ENGINE_LABELS[key] ?? key}
                  </div>
                </td>
                {/* Mention rate bar */}
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-20 overflow-hidden rounded-full bg-gray-200">
                      <div
                        className={`h-2 rounded-full ${barClass}`}
                        style={{ width: `${mentionPct}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-600">{mentionPct}%</span>
                  </div>
                </td>
                {/* Rank pill */}
                <td className="whitespace-nowrap px-4 py-3">
                  <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium capitalize ${rankClass}`}>
                    {data.rank ?? '—'}
                  </span>
                </td>
                {/* Tip */}
                <td className="px-4 py-3 text-gray-600">{data.tip ?? '—'}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

/* ─── CompetitorsList ───────────────────────────────────────────────── */
function CompetitorsList({ competitors }) {
  if (!competitors || competitors.length === 0) {
    return <p className="text-sm text-gray-400 italic">No competitors identified.</p>
  }
  return (
    <ul id="competitors-list" className="flex flex-wrap gap-3">
      {competitors.map((c, i) =>
        i === 0 ? (
          /* First = trophy card */
          <li
            key={i}
            className="flex flex-col items-center rounded-xl border border-yellow-200 bg-yellow-50 px-4 py-2 shadow-sm"
          >
            <span className="mb-0.5 text-xs font-semibold text-yellow-600">🏆 Top Competitor</span>
            <span className="text-sm font-bold text-gray-800">{c}</span>
          </li>
        ) : (
          /* Others = bordered pill */
          <li
            key={i}
            className="flex items-center rounded-full border border-gray-200 bg-white px-3 py-1.5 text-xs font-medium text-gray-700 shadow-sm"
          >
            {c}
          </li>
        )
      )}
    </ul>
  )
}

/* ─── WhatToDoNext ──────────────────────────────────────────────────── */
function WhatToDoNext({ category }) {
  const cat = category || 'your category'
  const actions = [
    {
      icon: '🖊️',
      text: `Update your listing title to include ${cat} keywords`,
    },
    {
      icon: '📸',
      text: 'Add lifestyle images showing your product in use',
    },
    {
      icon: '⭐',
      text: 'Gather more reviews — AI engines favor well-reviewed products',
    },
  ]
  return (
    <ol className="space-y-3">
      {actions.map((action, i) => (
        <li key={i} className="flex items-start gap-3">
          <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-xs font-bold text-indigo-600">
            {i + 1}
          </span>
          <span className="text-sm text-gray-600">
            <span className="mr-1.5">{action.icon}</span>
            {action.text}
          </span>
        </li>
      ))}
    </ol>
  )
}

/* ─── ReportCard (main export) ──────────────────────────────────────── */
export default function ReportCard({ report, onReset }) {
  if (!report) return null

  const { product, brand, overall_score, grade, queries_used, engines, top_competitors, summary, category } = report

  return (
    <div id="report-card" className="space-y-6">
      {/* Header */}
      <div className="rounded-2xl bg-white shadow-md p-8">
        <div className="flex flex-col items-center gap-4 sm:flex-row sm:items-start">
          <GradeBadge grade={grade} />
          <div className="flex-1 text-center sm:text-left">
            <h2 className="text-2xl font-bold text-gray-900">
              {brand}{' '}
              <span className="font-normal text-gray-500">— {product}</span>
            </h2>
            <p className="mt-1 text-sm text-gray-500">AEO Diagnostic Report</p>
            <div className="mt-4">
              <ScoreBar score={overall_score} />
            </div>
          </div>
        </div>
      </div>

      {/* Engine Breakdown */}
      <div className="rounded-2xl bg-white shadow-md p-8">
        <h3 className="mb-4 text-base font-semibold text-gray-800">Engine Breakdown</h3>
        <EnginesTable engines={engines} />
      </div>

      {/* Queries Used */}
      {queries_used && queries_used.length > 0 && (
        <div className="rounded-2xl bg-white shadow-md p-8">
          <h3 className="mb-3 text-base font-semibold text-gray-800">Queries Used</h3>
          <ol id="queries-list" className="list-decimal list-inside space-y-1.5 text-sm text-gray-600">
            {queries_used.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ol>
        </div>
      )}

      {/* Top Competitors */}
      <div className="rounded-2xl bg-white shadow-md p-8">
        <h3 className="mb-3 text-base font-semibold text-gray-800">Top Competitors Mentioned</h3>
        <CompetitorsList competitors={top_competitors} />
      </div>

      {/* Summary */}
      <div className="rounded-2xl bg-white shadow-md p-8">
        <h3 className="mb-2 text-base font-semibold text-gray-800">Summary</h3>
        <p id="summary-text" className="text-sm leading-relaxed text-gray-600">
          {summary}
        </p>
      </div>

      {/* What To Do Next */}
      <div className="rounded-2xl bg-white shadow-md p-8">
        <h3 className="mb-4 text-base font-semibold text-gray-800">What To Do Next</h3>
        <WhatToDoNext category={category} />
      </div>

      {/* Run Another Diagnosis */}
      <div className="flex justify-center pb-4">
        <button
          id="reset-btn"
          onClick={onReset}
          className="rounded-lg border border-indigo-300 bg-white px-6 py-2.5 text-sm font-semibold text-indigo-600 shadow-sm transition hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2"
        >
          ↩ Run Another Diagnosis
        </button>
      </div>
    </div>
  )
}
