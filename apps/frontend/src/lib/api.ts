import axios from 'axios'

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface HealthResponse {
  status: string
}

export interface YouTubeVideo {
  video_id: string
  title: string
  description: string
  channel_title: string
  published_at: string
  thumbnail: string
  duration: string
  duration_iso: string
  view_count: number
  like_count: number
  comment_count: number
}

export interface YouTubeSearchResponse {
  query: string
  count: number
  next_page_token: string | null
  results: YouTubeVideo[]
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await api.get<HealthResponse>('/health')

  return response.data
}

export async function searchYouTube(
  query: string,
  maxResults = 10,
  pageToken?: string,
): Promise<YouTubeSearchResponse> {
  const response = await api.get<YouTubeSearchResponse>(
    '/api/youtube/search',
    {
      params: {
        q: query,
        max_results: maxResults,
        ...(pageToken ? { page_token: pageToken } : {}),
      },
    },
  )

  return response.data
}

export default api