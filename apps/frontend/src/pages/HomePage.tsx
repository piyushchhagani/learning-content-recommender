import { Search } from 'lucide-react'

export function HomePage() {
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
            </div>

            <button
              type="button"
              className="rounded-xl bg-slate-900 px-6 py-4 font-semibold text-white transition hover:bg-slate-800"
            >
              Explore
            </button>
          </div>
        </div>
      </section>
    </main>
  )
}