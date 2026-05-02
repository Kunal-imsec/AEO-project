const GRADE_STYLES = {
  A: { badge: 'bg-green-100 text-green-800 ring-green-300', dot: 'bg-green-500' },
  B: { badge: 'bg-blue-100 text-blue-800 ring-blue-300', dot: 'bg-blue-500' },
  C: { badge: 'bg-yellow-100 text-yellow-800 ring-yellow-300', dot: 'bg-yellow-500' },
  D: { badge: 'bg-orange-100 text-orange-800 ring-orange-300', dot: 'bg-orange-500' },
  F: { badge: 'bg-red-100 text-red-800 ring-red-300', dot: 'bg-red-500' },
}

const ENGINE_LABELS = {
  openai: 'ChatGPT (OpenAI)',
  claude: 'Claude (Anthropic)',
  gemini: 'Gemini (Google)',
}

function GradeBadge({ grade }) {
  const style = GRADE_STYLES[grade] ?? GRADE_STYLES['F']
  return (
    <span
      id="grade-badge"
      className={`inline-flex h-20 w-20 items-center justify-center rounded-full text-4xl font-bold ring-4 ${style.badge}`}
    >
      {grade}
    </span>
  )
}

function ScoreBar({ score }) {
  const pct = Math.round(score)
  const color =
    pct >= 70 ? 'bg-green-500' : pct >= 50 ? 'bg-blue-500' : pct >= 30 ? 'bg-yellow-500' : 'bg-red-500'
  return (
    <div className="w-full">
      <div className="mb-1 flex justify-between text-xs text-gray-500">
        <span>AI Visibility Score</span>
        <span className="font-semibold text-gray-700">{pct}%</span>
      </div>
      <div className="h-3 w-full overflow-hidden rounded-full bg-gray-200">
        <div
          id="score-bar"
          className={`h-3 rounded-full transition-all duration-700 ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

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
            return (
              <tr key={key} className="hover:bg-gray-50 transition-colors">
                <td className="whitespace-nowrap px-4 py-3 font-medium text-gray-800">
                  {ENGINE_LABELS[key] ?? key}
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-20 overflow-hidden rounded-full bg-gray-200">
                      <div
                        className="h-2 rounded-full bg-indigo-500"
                        style={{ width: `${mentionPct}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-600">{mentionPct}%</span>
                  </div>
                </td>
                <td className="whitespace-nowrap px-4 py-3 text-gray-600">{data.rank ?? '—'}</td>
                <td className="px-4 py-3 text-gray-600">{data.tip ?? '—'}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function CompetitorsList({ competitors }) {
  if (!competitors || competitors.length === 0) {
    return <p className="text-sm text-gray-400 italic">No competitors identified.</p>
  }
  return (
    <ul id="competitors-list" className="flex flex-wrap gap-2">
      {competitors.map((c, i) => (
        <li
          key={i}
          className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700 ring-1 ring-gray-200"
        >
          {c}
        </li>
      ))}
    </ul>
  )
}

export default function ReportCard({ report }) {
  if (!report) return null

  const { product, brand, overall_score, grade, queries_used, engines, top_competitors, summary } = report
  const gradeStyle = GRADE_STYLES[grade] ?? GRADE_STYLES['F']

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
    </div>
  )
}
