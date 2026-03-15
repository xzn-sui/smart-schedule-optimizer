import { useState, useEffect } from 'react'
import './App.css'

const API = 'http://localhost:8000'
const GRID_START = 8 * 60   // 8:00 AM
const GRID_END = 19 * 60    // 7:00 PM
const PX_PER_MIN = 0.9
const PAGE_SIZE = 10

const DAYS_MAP = { M: 0, T: 1, W: 2, R: 3, F: 4 }
const DAY_LABELS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

const COURSE_COLORS = [
  { bg: '#2b6cb0', text: '#fff' },
  { bg: '#2c7a4b', text: '#fff' },
  { bg: '#c05621', text: '#fff' },
  { bg: '#6b46c1', text: '#fff' },
  { bg: '#b7791f', text: '#fff' },
  { bg: '#2c7873', text: '#fff' },
]

function parseDays(daysStr) {
  return [...daysStr].map(d => DAYS_MAP[d]).filter(d => d !== undefined)
}

function timeToMin(t) {
  const [h, m] = t.split(':').map(Number)
  return h * 60 + m
}

function formatHour(h) {
  if (h === 12) return '12pm'
  if (h > 12) return `${h - 12}pm`
  return `${h}am`
}

function StarRating({ rating }) {
  const color = rating >= 4.0 ? '#2c7a4b' : rating >= 3.0 ? '#b7791f' : '#c53030'
  return <span style={{ color, fontWeight: 600 }}>★ {rating.toFixed(1)}</span>
}

function Timetable({ sections, colorMap }) {
  const gridHeight = (GRID_END - GRID_START) * PX_PER_MIN
  const hours = []
  for (let h = 8; h <= 19; h++) hours.push(h)

  return (
    <div className="timetable">
      {/* Time labels */}
      <div className="time-col">
        <div className="day-header" />
        <div className="day-body" style={{ height: gridHeight }}>
          {hours.map(h => (
            <div
              key={h}
              className="time-label"
              style={{ top: (h * 60 - GRID_START) * PX_PER_MIN }}
            >
              {formatHour(h)}
            </div>
          ))}
        </div>
      </div>

      {/* Day columns */}
      {DAY_LABELS.map((label, dayIdx) => (
        <div key={label} className="day-col">
          <div className="day-header">{label}</div>
          <div className="day-body" style={{ height: gridHeight }}>
            {hours.map(h => (
              <div
                key={h}
                className="hour-line"
                style={{ top: (h * 60 - GRID_START) * PX_PER_MIN }}
              />
            ))}
            {sections
              .filter(s => parseDays(s.days).includes(dayIdx))
              .map(s => {
                const top = (timeToMin(s.start_time) - GRID_START) * PX_PER_MIN
                const height = (timeToMin(s.end_time) - timeToMin(s.start_time)) * PX_PER_MIN
                const color = colorMap[s.course_id] || { bg: '#718096', text: '#fff' }
                return (
                  <div
                    key={s.id}
                    className="section-block"
                    style={{ top, height, backgroundColor: color.bg, color: color.text }}
                  >
                    <div className="section-code">{s.course_id.toUpperCase()}</div>
                    <div className="section-time">{s.start_time}–{s.end_time}</div>
                  </div>
                )
              })}
          </div>
        </div>
      ))}
    </div>
  )
}

export default function App() {
  const [courses, setCourses] = useState([])
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [selected, setSelected] = useState(new Set())
  const [results, setResults] = useState([])
  const [colorMap, setColorMap] = useState({})
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetch(`${API}/courses`)
      .then(res => res.json())
      .then(data => setCourses(data))
      .catch(() => setError('Could not load courses. Is the backend running?'))
  }, [])

  function toggleCourse(code) {
    setSelected(prev => {
      const next = new Set(prev)
      if (next.has(code)) next.delete(code)
      else next.add(code)
      return next
    })
  }

  async function generateSchedules() {
    setError(null)
    setResults([])
    setLoading(true)
    try {
      const res = await fetch(`${API}/generate-schedules`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ courses: Array.from(selected) }),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Unknown error')
      }
      const data = await res.json()

      const map = {}
      Array.from(selected).forEach((code, i) => {
        map[code.toLowerCase()] = COURSE_COLORS[i % COURSE_COLORS.length]
      })
      setColorMap(map)
      setResults(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const filtered = courses.filter(c =>
    c.code.toLowerCase().includes(search.toLowerCase()) ||
    c.name.toLowerCase().includes(search.toLowerCase())
  )
  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const visible = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  return (
    <>
      <div className="header">
        <h1>Smart Schedule Optimizer</h1>
        <p>Select your courses and we'll find the best non-conflicting schedules.</p>
      </div>

      <div className="container">
        <div className="card">
          <h2>Select Courses</h2>

          <input
            className="search-input"
            type="text"
            placeholder="Search by course code or name..."
            value={search}
            onChange={e => { setSearch(e.target.value); setPage(1) }}
          />

          <div className="course-list">
            {courses.length === 0 && !error && <p className="muted">Loading courses...</p>}
            {filtered.length === 0 && courses.length > 0 && (
              <p className="muted">No courses match your search.</p>
            )}
            {visible.map(course => (
              <label
                key={course.id}
                className={`course-item ${selected.has(course.code) ? 'selected' : ''}`}
              >
                <input
                  type="checkbox"
                  checked={selected.has(course.code)}
                  onChange={() => toggleCourse(course.code)}
                />
                <span className="code">{course.code}</span>
                <span className="name">— {course.name}</span>
              </label>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="pagination">
              <button
                className="btn-page"
                onClick={() => setPage(p => p - 1)}
                disabled={page === 1}
              >
                ← Prev
              </button>
              <span className="page-info">Page {page} of {totalPages}</span>
              <button
                className="btn-page"
                onClick={() => setPage(p => p + 1)}
                disabled={page === totalPages}
              >
                Next →
              </button>
            </div>
          )}

          {selected.size > 0 && (
            <p className="selected-summary">
              {selected.size} course{selected.size > 1 ? 's' : ''} selected:{' '}
              {Array.from(selected).join(', ')}
            </p>
          )}

          <button
            className="btn-generate"
            onClick={generateSchedules}
            disabled={selected.size === 0 || loading}
          >
            {loading ? 'Generating...' : 'Generate Schedules'}
          </button>

          {error && <p className="error">{error}</p>}
        </div>

        {results.length > 0 && (
          <div>
            <p className="results-header">{results.length} schedules found</p>
            {results.map((result, i) => (
              <div key={i} className="result-card">
                <div className="result-title">
                  <h3>Option {i + 1}</h3>
                  <span className="score">Score: {result.score}</span>
                </div>

                {/* Side-by-side: timetable + table */}
                <div className="result-body">
                  <div className="result-timetable">
                    <Timetable sections={result.sections} colorMap={colorMap} />
                  </div>
                  <div className="result-table-wrap">
                    <table>
                      <thead>
                        <tr>
                          <th>Course</th>
                          <th>Professor</th>
                          <th>Rating</th>
                          <th>Days</th>
                          <th>Time</th>
                        </tr>
                      </thead>
                      <tbody>
                        {result.sections.map(section => (
                          <tr key={section.id}>
                            <td>
                              <span
                                className="course-badge"
                                style={{ backgroundColor: (colorMap[section.course_id] || {}).bg }}
                              >
                                {section.course_id.toUpperCase()}
                              </span>
                            </td>
                            <td>{section.professor}</td>
                            <td><StarRating rating={section.rating} /></td>
                            <td>{section.days}</td>
                            <td>{section.start_time}–{section.end_time}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  )
}
