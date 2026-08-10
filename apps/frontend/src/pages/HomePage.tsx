import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Search } from 'lucide-react'

import { getHealth, searchYouTube } from '../lib/api'

function formatNumber(value: number): string {
  if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(2)}M`
  }

  if (value >= 1_000) {
    return `${(value / 1_000).toFixed(1)}K`
  }

  return value.toString()
}

function decodeHtmlEntities(value: string): string {
  const parser = new DOMParser()
  return parser.parseFromString(value, 'text/html').documentElement.textContent ?? value
}


export function HomePage() {
  const [search, setSearch] = useState('')
  const [submittedQuery, setSubmittedQuery] = useState('')

  const healthQuery = useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
  })

  const searchQuery = useQuery({
    queryKey: ['youtube-search', submittedQuery],
    queryFn: () => searchYouTube(submittedQuery, 10),
    enabled: Boolean(submittedQuery),
  })

  const backendStatus =
    healthQuery.isLoading
      ? 'Checking backend...'
      : healthQuery.isError
        ? 'Backend unavailable'
        : 'Backend connected'

  function handleSearch() {
    const query = search.trim()

    if (!query) {
      return
    }

    setSubmittedQuery(query)
  }

  return (
    <section className="mx-auto flex min-h-screen max-w-6xl flex-col px-6 py-16">
      <div className="max-w-4xl">
        <span className="inline-flex rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
          Learning Content Recommender
        </span>

        <h1 className="mt-6 text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">
          Find the right learning content.
        </h1>

        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-600">
          Search a topic and discover the most suitable YouTube learning
          resources based on quality, depth, difficulty, duration, and
          learning goals.
        </p>

        <div className="mt-8 flex max-w-3xl flex-col gap-3 sm:flex-row">
          <div className="flex flex-1 items-center rounded-xl border border-slate-200 bg-white px-4 shadow-sm">
            <Search className="mr-3 h-5 w-5 shrink-0 text-slate-400" />

            <input
              type="text"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') {
                  handleSearch()
                }
              }}
              placeholder="Try: Docker, Python, SQL..."
              className="w-full bg-transparent py-4 text-slate-900 outline-none placeholder:text-slate-400"
            />

            <button
              type="button"
              onClick={handleSearch}
              className="ml-3 rounded-lg bg-slate-900 px-5 py-3 font-semibold text-white transition hover:bg-slate-800"
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

      {searchQuery.isLoading && (
        <section className="mt-12">
          <p className="text-slate-600">Searching YouTube...</p>
        </section>
      )}

      {searchQuery.isError && (
        <section className="mt-12">
          <p className="text-red-600">
            Unable to search YouTube. Please try again.
          </p>
        </section>
      )}

      {searchQuery.data && (
        <section className="mt-12">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-slate-900">
              Results for "{searchQuery.data.query}"
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              {searchQuery.data.count} videos found
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            {searchQuery.data.results.map((video) => (
              <article
                key={video.video_id}
                className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm transition hover:shadow-md"
              >
                <img
 		 src={video.thumbnail}
  		 alt={decodeHtmlEntities(video.title)}
   		 className="aspect-video w-full object-cover"
		/>

                <div className="p-5">
                  <h3 className="font-semibold leading-6 text-slate-900">
  		     {decodeHtmlEntities(video.title)}
		  </h3>

                  <p className="mt-2 text-sm text-slate-500">
                    {video.channel_title}
                  </p>
		  
		  <div className="mt-3 flex flex-wrap gap-x-3 gap-y-1 text-sm text-slate-500">
  			<span>{video.duration}</span>
  			<span>•</span>
  			<span>{formatNumber(video.view_count)} views</span>
  			<span>•</span>
 		  	<span>{formatNumber(video.like_count)} likes</span>
  			<span>•</span>
  			<span>{formatNumber(video.comment_count)} comments</span>
		  </div>

                  <a
                    href={`https://www.youtube.com/watch?v=${video.video_id}`}
                    target="_blank"
                    rel="noreferrer"
                    className="mt-4 inline-block font-medium text-blue-600 hover:text-blue-700"
                  >
                    Watch on YouTube →
                  </a>
                </div>
              </article>
            ))}
          </div>
        </section>
      )}
    </section>
  )
}