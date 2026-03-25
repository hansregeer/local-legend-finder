import { useState, useEffect } from 'react'

interface User {
  id: number
  username: string
  firstname: string
  lastname: string
  is_mock?: boolean
}

interface Activity {
  id: number
  name: string
  distance: number
  moving_time: number
  type: string
  start_date: string
  is_mock?: boolean
}

function App() {
  const [user, setUser] = useState<User | null>(null)
  const [activities, setActivities] = useState<Activity[]>([])
  const [loading, setLoading] = useState(false)
  const [syncing, setSyncing] = useState(false)

  useEffect(() => {
    fetchUser()
    fetchActivities()
  }, [])

  const fetchUser = async () => {
    try {
      const response = await fetch('/api/user')
      const data = await response.json()
      setUser(data)
    } catch (error) {
      console.error('Failed to fetch user:', error)
    }
  }

  const fetchActivities = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/activities')
      const data = await response.json()
      setActivities(data)
    } catch (error) {
      console.error('Failed to fetch activities:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStravaAuth = async () => {
    try {
      const response = await fetch('/api/auth/strava')
      const data = await response.json()
      window.location.href = data.authorization_url
    } catch (error) {
      console.error('Failed to initiate Strava auth:', error)
    }
  }

  const handleSyncActivities = async () => {
    setSyncing(true)
    try {
      const response = await fetch('/api/sync-activities', { method: 'POST' })
      const data = await response.json()
      alert(`Synced ${data.synced} activities${data.is_mock ? ' (mock data)' : ''}`)
      fetchActivities()
    } catch (error) {
      console.error('Failed to sync activities:', error)
    } finally {
      setSyncing(false)
    }
  }

  const formatDistance = (meters: number) => {
    return (meters / 1000).toFixed(2) + ' km'
  }

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-gradient-to-r from-strava-orange to-strava-dark text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
          <h1 className="text-4xl font-bold mb-2">🏆 Local Legend Finder</h1>
          <p className="text-lg opacity-90">Track your Strava activities and find local legends</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* User Section */}
        <div className="mb-8">
          {user ? (
            <div className="bg-white rounded-xl shadow-md p-6 mb-4">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <h2 className="text-2xl font-semibold text-gray-800">
                  Welcome, {user.firstname || user.username}!
                </h2>
                {user.is_mock && (
                  <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-semibold">
                    Demo Mode
                  </span>
                )}
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-md p-6 mb-4">
              <h2 className="text-2xl font-semibold text-gray-800 mb-2">Welcome!</h2>
              <p className="text-gray-600">Connect your Strava account to get started</p>
            </div>
          )}

          <div className="flex gap-4 flex-wrap">
            <button
              onClick={handleStravaAuth}
              className="px-6 py-3 bg-strava-orange hover:bg-strava-dark text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
            >
              {user?.is_mock === false ? 'Reconnect' : 'Connect'} Strava
            </button>
            <button
              onClick={handleSyncActivities}
              disabled={syncing}
              className="px-6 py-3 bg-gray-700 hover:bg-gray-800 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {syncing ? 'Syncing...' : 'Sync Activities'}
            </button>
          </div>
        </div>

        {/* Activities Section */}
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Recent Activities</h2>
          {loading ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">Loading activities...</p>
            </div>
          ) : activities.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {activities.map((activity) => (
                <div
                  key={activity.id}
                  className="bg-white rounded-xl shadow-md p-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-200"
                >
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-semibold text-gray-800 flex-1 mr-2">
                      {activity.name}
                    </h3>
                    <span className="px-3 py-1 bg-strava-orange text-white text-sm font-semibold rounded-full whitespace-nowrap">
                      {activity.type}
                    </span>
                  </div>

                  <div className="flex gap-6 mb-4">
                    <div className="flex flex-col">
                      <span className="text-sm text-gray-500 mb-1">Distance</span>
                      <span className="text-xl font-semibold text-gray-800">
                        {formatDistance(activity.distance)}
                      </span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-sm text-gray-500 mb-1">Time</span>
                      <span className="text-xl font-semibold text-gray-800">
                        {formatTime(activity.moving_time)}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <p className="text-sm text-gray-500">
                      {new Date(activity.start_date).toLocaleDateString()}
                    </p>
                    {activity.is_mock && (
                      <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full">
                        Sample Data
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-md p-12 text-center">
              <p className="text-gray-500 text-lg">
                No activities yet. Sync your Strava activities to get started!
              </p>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center">
          <p className="text-gray-500 text-sm">Local Legend Finder v1.0.0 - MVP</p>
        </div>
      </footer>
    </div>
  )
}

export default App
