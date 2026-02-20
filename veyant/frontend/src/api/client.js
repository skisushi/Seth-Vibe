const BASE = '/api'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`)
  return data
}

// Travelers
export const getTravelers       = ()         => request('/travelers')
export const getTraveler        = (id)       => request(`/travelers/${id}`)
export const createTraveler     = (body)     => request('/travelers', { method: 'POST', body: JSON.stringify(body) })

// Trips
export const getTrips           = (travelerId) => request(`/travelers/${travelerId}/trips`)
export const createTrip         = (body)        => request('/trips', { method: 'POST', body: JSON.stringify(body) })

// Preferences
export const getPreferences     = (travelerId) => request(`/travelers/${travelerId}/preferences`)

// Destinations
export const getDestinations    = ()         => request('/destinations')

// Seed
export const seedDatabase       = ()         => request('/seed', { method: 'POST' })
