import { useState, useEffect, useCallback } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getTraveler, getTrips, getPreferences } from '../api/client'
import AddTripModal from './AddTripModal'

// ─── Helpers ──────────────────────────────────────────────────────────────

const AVATAR_COLORS = [
  '#2563eb', '#7c3aed', '#db2777', '#059669',
  '#d97706', '#dc2626', '#0891b2', '#65a30d',
]
function avatarColor(name = '') {
  return AVATAR_COLORS[name.charCodeAt(0) % AVATAR_COLORS.length]
}
function initials(name = '') {
  return name.split(' ').map((w) => w[0]).join('').slice(0, 2).toUpperCase()
}
function formatDate(str) {
  if (!str) return '—'
  return new Date(str + 'T00:00:00').toLocaleDateString(undefined, {
    month: 'short', day: 'numeric', year: 'numeric',
  })
}
function capitalize(str = '') {
  return str.charAt(0).toUpperCase() + str.slice(1)
}

// ─── Preferences cards ─────────────────────────────────────────────────────

function PreferencesSection({ prefs }) {
  if (!prefs) return null

  const countries = prefs.countries_visited
    ? prefs.countries_visited.split(',').map((c) => c.trim())
    : []
  const travelTypes = prefs.travel_types
    ? prefs.travel_types.split(',').map((t) => capitalize(t.trim()))
    : []
  const accommodations = prefs.accommodation_types
    ? prefs.accommodation_types.split(',').map((a) => capitalize(a.trim()))
    : []

  return (
    <>
      <div className="section-header">
        <h2 className="section-title">Travel Profile</h2>
      </div>
      <div className="prefs-grid">
        <div className="card pref-card">
          <div className="pref-card__label">Total trips</div>
          <div className="pref-card__value">{prefs.total_trips ?? '0'}</div>
          <div className="pref-card__sub">across all destinations</div>
        </div>

        <div className="card pref-card">
          <div className="pref-card__label">Avg duration</div>
          <div className="pref-card__value">{prefs.avg_trip_duration_days ?? '—'}</div>
          <div className="pref-card__sub">days per trip</div>
        </div>

        <div className="card pref-card">
          <div className="pref-card__label">Countries</div>
          <div className="pref-card__value">{countries.length}</div>
          <div className="pref-card__sub">{countries.join(', ') || '—'}</div>
        </div>

        <div className="card pref-card">
          <div className="pref-card__label">Travel styles</div>
          <div className="pref-card__value" style={{ fontSize: '1.1rem', paddingTop: '6px' }}>
            {travelTypes.join(' · ') || '—'}
          </div>
          <div className="pref-card__sub">preferred types</div>
        </div>

        <div className="card pref-card">
          <div className="pref-card__label">Stays in</div>
          <div className="pref-card__value" style={{ fontSize: '1.1rem', paddingTop: '6px' }}>
            {accommodations.join(' · ') || '—'}
          </div>
          <div className="pref-card__sub">accommodation types</div>
        </div>
      </div>
    </>
  )
}

// ─── Trip card ─────────────────────────────────────────────────────────────

function TripCard({ trip }) {
  const dest = [trip.city, trip.country].filter(Boolean).join(', ')

  return (
    <div className="card trip-card">
      <div className="trip-card__top">
        <div>
          <div className="trip-card__dest">{dest || trip.country}</div>
          <div className="trip-card__dates">
            {formatDate(trip.start_date)} – {formatDate(trip.end_date)}
          </div>
        </div>
        <div className="trip-card__duration">
          {trip.duration_days ?? '?'} {trip.duration_days === 1 ? 'day' : 'days'}
        </div>
      </div>

      <div className="trip-card__badges">
        {trip.travel_type && (
          <span className="badge badge-blue">{capitalize(trip.travel_type)}</span>
        )}
        {trip.accommodation_type && (
          <span className="badge badge-amber">{capitalize(trip.accommodation_type)}</span>
        )}
        {trip.region && (
          <span className="badge badge-green">{trip.region}</span>
        )}
      </div>

      {trip.notes && (
        <div className="trip-card__notes">"{trip.notes}"</div>
      )}
    </div>
  )
}

// ─── Main component ─────────────────────────────────────────────────────────

export default function TravelerDetail() {
  const { id } = useParams()
  const [traveler, setTraveler] = useState(null)
  const [trips, setTrips] = useState([])
  const [prefs, setPrefs] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showModal, setShowModal] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const [t, tr, p] = await Promise.all([
        getTraveler(id),
        getTrips(id),
        getPreferences(id).catch(() => null),
      ])
      setTraveler(t)
      setTrips(tr)
      setPrefs(p)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [id])

  useEffect(() => { load() }, [load])

  const handleTripCreated = () => {
    // Refresh trips + preferences after adding
    load()
  }

  if (loading) return (
    <div className="container">
      <div className="loading-state">Loading…</div>
    </div>
  )

  if (error) return (
    <div className="container">
      <div style={{ paddingTop: 32 }}>
        <div className="error-banner">{error}</div>
        <Link to="/" className="back-link">← Back to travelers</Link>
      </div>
    </div>
  )

  return (
    <div className="container">
      {/* Back nav */}
      <div style={{ paddingTop: 24 }}>
        <Link to="/" className="back-link">← All travelers</Link>
      </div>

      {/* Traveler header */}
      <div className="page-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div
            className="avatar"
            style={{ width: 56, height: 56, fontSize: '1.3rem', background: avatarColor(traveler?.name) }}
          >
            {initials(traveler?.name)}
          </div>
          <div>
            <h1 className="page-title">{traveler?.name}</h1>
            <p className="page-subtitle">{traveler?.email}</p>
          </div>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          + Add Trip
        </button>
      </div>

      {/* Preferences */}
      <PreferencesSection prefs={prefs} />

      {/* Trips */}
      <div className="section-header">
        <h2 className="section-title">
          Trip History
          <span style={{ fontWeight: 400, color: 'var(--text-muted)', marginLeft: 8, fontSize: '0.9rem' }}>
            ({trips.length})
          </span>
        </h2>
      </div>

      {trips.length === 0 ? (
        <div className="card empty-state">
          <div className="empty-state__icon">✈</div>
          <div className="empty-state__title">No trips yet</div>
          <div className="empty-state__body">
            Click <strong>+ Add Trip</strong> to log this traveler's first journey.
          </div>
        </div>
      ) : (
        <div className="trip-list">
          {trips.map((trip) => (
            <TripCard key={trip.id} trip={trip} />
          ))}
        </div>
      )}

      {showModal && (
        <AddTripModal
          travelerId={Number(id)}
          onClose={() => setShowModal(false)}
          onCreated={handleTripCreated}
        />
      )}
    </div>
  )
}
