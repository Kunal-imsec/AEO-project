import { useState } from 'react'
import InputForm from './components/InputForm.jsx'
import ReportCard from './components/ReportCard.jsx'

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-12">
      {/* Page header */}
      <header className="mx-auto mb-10 max-w-3xl text-center">
        <div className="mb-3 inline-flex items-center gap-2 rounded-full bg-indigo-50 px-4 py-1.5 text-xs font-semibold uppercase tracking-widest text-indigo-600 ring-1 ring-indigo-100">
          AI Engine Optimization
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight text-gray-900">
          AEO Diagnostic Tool
        </h1>
        <p className="mt-3 text-base text-gray-500">
          Measure how visible your brand is across ChatGPT, Claude, and Gemini — and get actionable tips to improve.
        </p>
      </header>

      <main className="mx-auto max-w-3xl space-y-8">
        <InputForm onResult={setResult} onLoading={setLoading} />

        {loading && (
          <div
            id="loading-overlay"
            className="flex flex-col items-center gap-3 rounded-2xl bg-white p-12 shadow-md"
          >
            <svg
              className="h-10 w-10 animate-spin text-indigo-500"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            <p className="text-sm font-medium text-gray-500">
              Querying ChatGPT, Claude & Gemini… this may take 15–30 seconds.
            </p>
          </div>
        )}

        {!loading && result && <ReportCard report={result} />}
      </main>

      <footer className="mx-auto mt-16 max-w-3xl border-t border-gray-200 pt-6 text-center text-xs text-gray-400">
        AEO Diagnostic Tool · Phase 5
      </footer>
    </div>
  )
}
