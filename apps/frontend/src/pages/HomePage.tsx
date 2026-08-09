import { useQuery } from '@tanstack/react-query'
import { Search } from 'lucide-react'

import { getHealth } from '../lib/api'

export function HomePage() {
  const healthQuery = useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
  })

  const backendStatus =
    healthQuery.isLoading
      ? 'Checking backend...'
      : healthQuery.isError
        ? 'Backend unavailable'
        : 'Backend connected'

  return (
    <main className="min-h-screen bg-slate-50">
      <section className="mx-auto flex min-h-screen max-w-6xl flex-col justify-center px-6 py-16">
        <div className="max-w-3xl">
          <span className="inline-flex rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
            Learning Content Recommender
          </span>

          <h1 className="mt-6 text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">
            Find the right learning content.
          </h1>

          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600">
            Search a topic and discover the most suitable YouTube learning
            resources based on quality, depth, difficulty, duration, and
            learning goals.
          </p>

          <div className="mt-8 flex max-w-2xl flex-col gap-3 sm:flex-row">
            <div className="flex flex-1 items-center rounded-xl border border-slate-200 bg-white px-4 shadow-sm">
              <Search className="mr-3 h-5 w-5 text-slate-400" />

              <input
                type="text"
                placeholder="Try: Docker, Python, SQL..."
                className="w-full bg-transparent py-4 text-slate-900 outline-none placeholder:text-slate-400"
              />

              <button
                type="button"
                className="ml-3 rounded-lg bg-slate-900 px-4 py-2 font-semibold text-white transition hover:bg-slate-800"
              >
                Explore
              </button>
            </div>
          </div>

          <div className="mt-6 flex items-center gap-2 text-sm text-slate-500">
            <span
              className={`h-2.5 w-2.5 rounded-full ${
                healthQuery.isError ? 'bg-red-500' : 'bg-green-500'
              }`}
            />

            <span>{backendStatus}</span>
          </div>
        </div>
      </section>
    </main>
  )
}