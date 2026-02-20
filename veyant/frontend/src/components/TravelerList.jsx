import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getTravelers, getPreferences, seedDatabase } from '../api/client'
import AddTravelerModal from './AddTravelerModal'

// Deterministic color per traveler based on name initial
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

function TravelerCard({ traveler, prefs, onClick }) {
  return (
    <div className="card traveler-card" onClick={onClick} role="button" tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}>
      <div className="traveler-card__header">
        <div className="avatar" style={{ background: avatarColor(traveler.name) }}>
          {initials(traveler.name)}
        </div>
        <div>
          <div className="traveler-card__name">{traveler.name}</div>
          <div className="traveler-card__email">{traveler.email}</div>
        </div>
      </div>

      <div className="traveler-card__stats">
        <div className="stat-item">
          <div className="stat-item__value">{prefs?.total_trips ?? '—'}</div>
          <div className="stat-item__label">Trips</div>
        </div>
        <div className="stat-item">
          <div className="stat-item__value">
            {prefs?.avg_trip_duration_days ?? '—'}
          </div>
          <div className="stat-item__label">Avg days</div>
        </div>
        <div className="stat-item">
          <div className="stat-item__value">
            {prefs?.countries_visited
              ? prefs.countries_visited.split(',').length
              : '—'}
          </div>
          <div className="stat-item__label">Countries</div>
        </div>
      </div>
    </div>
  )
}

export default function TravelerList() {
  const navigate = useNavigate()
  const [travelers, setTravelers] = useState([])
  const [prefsMap, setPrefsMap] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [seeding, setSeeding] = useState(false)
  const [seedMsg, setSeedMsg] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const list = await getTravelers()
      setTravelers(list)
      // Load preferences for all travelers in parallel
      const entries = await Promise.all(
        list.map((t) =>
          getPreferences(t.id)
            .then((p) => [t.id, p])
            .catch(() => [t.id, null])
        )
      )
      setPrefsMap(Object.fromEntries(entries))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const handleCreated = (traveler) => {
    setTravelers((prev) => [traveler, ...prev])
  }

  const handleSeed = async () => {
    setSeeding(true)
    setSeedMsg('')
    try {
      await seedDatabase()
      setSeedMsg('Sample data loaded!')
      await load()
    } catch (err) {
      setSeedMsg(err.message)
    } finally {
      setSeeding(false)
    }
  }

  return (
    <div className="container">
      <div className="page-header">
        <div className="page-header__text">
          <h1 className="page-title">Travelers</h1>
          <p className="page-subtitle">
            {loading ? 'Loading…' : `${travelers.length} traveler${travelers.length !== 1 ? 's' : ''} tracked`}
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          + Add Traveler
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {!loading && travelers.length === 0 && (
        <div className="seed-banner">
          <div className="seed-banner__text">
            <strong>No travelers yet</strong>
            <span>Load sample data to see the app in action.</span>
          </div>
          <button className="btn btn-primary btn-sm" onClick={handleSeed} disabled={seeding}>
            {seeding ? 'Loading…' : 'Load Sample Data'}
          </button>
          {seedMsg && <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{seedMsg}</span>}
        </div>
      )}

      {loading ? (
        <div className="loading-state">Loading travelers…</div>
      ) : (
        <div className="traveler-grid">
          {travelers.map((t) => (
            <TravelerCard
              key={t.id}
              traveler={t}
              prefs={prefsMap[t.id]}
              onClick={() => navigate(`/travelers/${t.id}`)}
            />
          ))}
        </div>
      )}

      {showModal && (
        <AddTravelerModal
          onClose={() => setShowModal(false)}
          onCreated={handleCreated}
        />
      )}
    </div>
  )
}
