import { useState } from 'react'

const CATEGORIES = [
  'Electronics',
  'Supplements',
  'Skincare',
  'Pet Products',
  'Home & Kitchen',
  'Sports & Outdoors',
  'Baby Products',
  'Other',
]

export default function InputForm({ onResult, onLoading }) {
  const [productName, setProductName] = useState('')
  const [brandName, setBrandName] = useState('')
  const [category, setCategory] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    onLoading(true)

    try {
      const res = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_name: productName.trim(),
          brand_name: brandName.trim(),
          category: category.trim(),
        }),
      })

      if (!res.ok) {
        const detail = await res.text()
        throw new Error(`Server error ${res.status}: ${detail}`)
      }

      const data = await res.json()
      onResult(data)
    } catch (err) {
      setError(err.message)
      onResult(null)
    } finally {
      setLoading(false)
      onLoading(false)
    }
  }

  const inputClass =
    'w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 placeholder-gray-400 shadow-sm transition focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200 disabled:cursor-not-allowed disabled:bg-gray-50'

  return (
    <div className="rounded-2xl bg-white shadow-md p-8">
      <h2 className="mb-1 text-xl font-semibold text-gray-800">Run a Diagnosis</h2>
      {/* Tagline */}
      <p className="mb-1 text-xs text-gray-400 italic text-center">
        Used by 500+ Amazon sellers to diagnose AI visibility
      </p>
      <p className="mb-6 text-sm text-gray-500">
        Enter your product details to check AI engine visibility across ChatGPT, Claude, and Gemini.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4" id="diagnosis-form">
        <div>
          <label htmlFor="product-name" className="mb-1.5 block text-sm font-medium text-gray-700">
            Product Name
          </label>
          <input
            id="product-name"
            type="text"
            placeholder="e.g. Wireless Earbuds"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            required
            disabled={loading}
            className={inputClass}
          />
        </div>

        <div>
          <label htmlFor="brand-name" className="mb-1.5 block text-sm font-medium text-gray-700">
            Brand Name
          </label>
          <input
            id="brand-name"
            type="text"
            placeholder="e.g. Sony"
            value={brandName}
            onChange={(e) => setBrandName(e.target.value)}
            required
            disabled={loading}
            className={inputClass}
          />
        </div>

        <div>
          <label htmlFor="category" className="mb-1.5 block text-sm font-medium text-gray-700">
            Category
          </label>
          <select
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
            disabled={loading}
            className={inputClass}
          >
            <option value="" disabled>Select a category…</option>
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        {error && (
          <div
            id="form-error"
            className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
          >
            {error}
          </div>
        )}

        <button
          id="submit-btn"
          type="submit"
          disabled={loading}
          className={`flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60 ${loading ? 'animate-pulse' : ''}`}
        >
          {loading ? (
            <>
              <svg
                className="h-4 w-4 animate-spin"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                />
              </svg>
              Analyzing…
            </>
          ) : (
            <>🚀 Run Diagnosis</>
          )}
        </button>

        {/* Trust badges */}
        <div className="flex items-center justify-center gap-5 pt-1 text-xs text-gray-400">
          <span>🔒 Private</span>
          <span className="text-gray-200">|</span>
          <span>⚡ ~15s analysis</span>
          <span className="text-gray-200">|</span>
          <span>🤖 3 AI Engines</span>
        </div>
      </form>
    </div>
  )
}
