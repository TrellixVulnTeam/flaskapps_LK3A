import { parseUser, parseStatus } from '../entity_normalizer/entity_normalizer.service.js'
import { RegistrationError, StatusCodeError } from '../errors/errors'
import { map, reduce } from 'lodash'

const MASTODON_LOGIN_URL = '/api/v1/accounts/verify_credentials'
const MASTODON_REGISTRATION_URL = '/api/v1/accounts'
const MASTODON_USER_URL = '/api/v1/accounts'

const TRACKS_UPLOAD_URL = '/api/tracks'
const TRACKS_FETCH_URL = (username, id) => `/api/tracks/${username}/${id}`
const TRACKS_EDIT_URL = (username, id) => `/api/tracks/${username}/${id}`
const TRACKS_DELETE_URL = (username, id) => `/api/tracks/${username}/${id}`
const TRACKS_LOGS_URL = (username, id) => `/api/tracks/${username}/${id}/logs`
const TRACKS_UPDATE_ARTWORK_URL = (username, id) => `/api/tracks/${username}/${id}/artwork`
const TRACKS_RETRY_PROCESSING_URL = (username, id) => `/api/tracks/${username}/${id}/retry_processing`

const ALBUMS_NEW_URL = '/api/albums'
const ALBUMS_FETCH_URL = (username, id) => `/api/albums/${username}/${id}`
const ALBUMS_EDIT_URL = (username, id) => `/api/albums/${username}/${id}`
const ALBUM_REORDER_URL = (username, id) => `/api/albums/${username}/${id}/reorder`
const ALBUMS_DELETE_URL = (username, id) => `/api/albums/${username}/${id}`
const ALBUMS_UPDATE_ARTWORK_URL = (username, id) => `/api/albums/${username}/${id}/artwork`

const ACCOUNT_LOGS_URL = (username, currentPage, perPage) => `/api/users/${username}/logs?page=${currentPage}&page_size=${perPage}`
const ACCOUNT_QUOTA_URL = (username, currentPage, perPage) => `/api/users/${username}/quota?page=${currentPage}&page_size=${perPage}`

const MASTODON_PUBLIC_TIMELINE = '/api/v1/timelines/public'
const MASTODON_USER_HOME_TIMELINE_URL = '/api/v1/timelines/home'
const MASTODON_DIRECT_MESSAGES_TIMELINE_URL = '/api/v1/timelines/direct'
const MASTODON_USER_NOTIFICATIONS_URL = '/api/v1/notifications'
const MASTODON_USER_TIMELINE_URL = id => `/api/v1/accounts/${id}/statuses`
const MASTODON_PROFILE_UPDATE_URL = '/api/v1/accounts/update_credentials'
const MASTODON_USER_RELATIONSHIPS_URL = '/api/v1/accounts/relationships'
const MASTODON_FOLLOW_URL = id => `/api/v1/accounts/${id}/follow`
const MASTODON_UNFOLLOW_URL = id => `/api/v1/accounts/${id}/unfollow`
const MASTODON_FOLLOWING_URL = id => `/api/v1/accounts/${id}/following`
const MASTODON_FOLLOWERS_URL = id => `/api/v1/accounts/${id}/followers`

const REEL2BITS_LICENSES = '/api/reel2bits/licenses'
const REEL2BITS_GENRES = '/api/reel2bits/genres'
const REEL2BITS_TAGS = '/api/reel2bits/tags'
const REEL2BITS_ALBUMS = (username) => `/api/albums/${username}`
const CHANGE_PASSWORD_URL = '/api/reel2bits/change_password'
const RESET_PASSWORD_URL = '/api/reel2bits/reset_password'
const RESET_PASSWORD_URL_TOKEN = (token) => `${RESET_PASSWORD_URL}/${token}`
const REEL2BITS_DRAFTS_TIMELINE = '/api/v1/timelines/drafts'
const REEL2BITS_ALBUMS_TIMELINE = '/api/v1/timelines/albums'
const REEL2BITS_UNPROCESSED_TIMELINE = '/api/v1/timelines/unprocessed'

const oldfetch = window.fetch

const fetch = (url, options) => {
  options = options || {}
  const baseUrl = ''
  const fullUrl = baseUrl + url
  options.credentials = 'same-origin'
  return oldfetch(fullUrl, options)
}

const authHeaders = (accessToken) => {
  if (accessToken) {
    return { Authorization: `Bearer ${accessToken}` }
  } else {
    return {}
  }
}

const promisedRequest = ({ method, url, payload, credentials, headers = {} }, store) => {
  const options = {
    method,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...headers
    }
  }
  if (payload) {
    options.body = JSON.stringify(payload)
  }
  if (credentials) {
    options.headers = {
      ...options.headers,
      ...authHeaders(credentials)
    }
  }
  return fetch(url, options)
    .then((response) => {
      return new Promise((resolve, reject) => response.json()
        .then((json) => {
          if (!response.ok) {
            return reject(new StatusCodeError(response.status, json, { url, options }, response))
          }
          return resolve(json)
        }))
    })
}

/*
 * Parameters needed:
 *  nickname, email, fullname, password, password_confirm
 * Optionals:
 *  bio, homepage, location, token
 */
const register = (userInfo, store) => {
  console.debug('api.service::register', userInfo)
  const { nickname, ...rest } = userInfo
  return fetch(MASTODON_REGISTRATION_URL, {
    method: 'POST',
    headers: {
      ...authHeaders(store.getters.getToken()),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      nickname,
      locale: 'en_US',
      agreement: true,
      ...rest
    })
  })
    .then((response) => {
      if (response.ok) {
        return response.json()
      } else {
        return response.json().then((error) => { throw new RegistrationError(error) })
      }
    })
}

const verifyCredentials = (user, store) => {
  return fetch(MASTODON_LOGIN_URL, {
    headers: authHeaders(user)
  })
    .then((response) => {
      if (response.ok) {
        return response.json()
      } else {
        return {
          error: response
        }
      }
    })
    .then((data) => data.error ? data : parseUser(data))
}

const trackUpload = (trackInfo, store) => {
  const form = new window.FormData()
  form.append('title', trackInfo.title)
  form.append('description', trackInfo.description)
  form.append('album', trackInfo.album)
  form.append('licence', trackInfo.licence)
  form.append('private', trackInfo.private)
  form.append('genre', trackInfo.genre)
  form.append('tags', trackInfo.tags.map(a => a.text))
  // let the files last for dev tools inspection
  if (trackInfo.artwork) {
    let filename = 'blob.invalid'
    if (trackInfo.artwork.type === 'image/jpeg') {
      filename = 'blob.jpg'
    } else if (trackInfo.artwork.type === 'image/png') {
      filename = 'blob.png'
    } else if (trackInfo.artwork.type === 'image/gif') {
      filename = 'blob.gif'
    }
    form.append('artwork', trackInfo.artwork, filename)
  }
  form.append('file', trackInfo.file)

  return fetch(TRACKS_UPLOAD_URL, {
    body: form,
    method: 'POST',
    headers: authHeaders(store.getters.getToken())
  })
    .then((response) => [response.ok, response])
    .then(([ok, response]) => {
      if (ok) {
        return response.json()
      } else {
        return response.json().then((error) => { throw new Error(error.error) })
      }
    })
}

const trackFetch = ({ userId, trackId, credentials }) => {
  const url = TRACKS_FETCH_URL(userId, trackId)

  return fetch(url, { headers: authHeaders(credentials) })
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error fetching track', data)
    })
    .then((data) => data.json())
    .then((data) => parseStatus(data))
}

const trackDelete = ({ userId, trackId, credentials }) => {
  const url = TRACKS_DELETE_URL(userId, trackId)

  return fetch(url, {
    headers: authHeaders(credentials),
    method: 'DELETE'
  })
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error deleting track', data)
    })
    .then((data) => data.json())
}

const trackEdit = ({ userId, trackId, track, credentials }) => {
  // Do that to avoid modifying `track` and bork the vue variable (tags)
  const payload = {
    title: track.title,
    description: track.description,
    album: track.album,
    licence: track.licence,
    private: track.private,
    genre: track.genre,
    tags: track.tags.map(a => a.text)
  }

  return promisedRequest({
    url: TRACKS_EDIT_URL(userId, trackId),
    method: 'PATCH',
    payload: payload,
    credentials: credentials
  }).then((data) => parseStatus(data))
}

const fetchTrackLogs = ({ userId, trackId, credentials }) => {
  const url = TRACKS_LOGS_URL(userId, trackId)

  return fetch(url, { headers: authHeaders(credentials) })
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error fetching track logs', data)
    })
    .then((data) => data.json())
}

const trackRetryProcessing = ({ userId, trackId, credentials }) => {
  return promisedRequest({
    url: TRACKS_RETRY_PROCESSING_URL(userId, trackId),
    method: 'POST',
    credentials: credentials
  })
}

const albumReorder = ({ userId, albumId, tracksOrder, credentials }) => {
  return promisedRequest({
    url: ALBUM_REORDER_URL(userId, albumId),
    method: 'PATCH',
    payload: tracksOrder,
    credentials: credentials
  }).then((data) => parseStatus(data))
}

const fetchUser = ({ id, credentials }) => {
  const url = `${MASTODON_USER_URL}/${id}`
  return promisedRequest({ url, credentials })
    .then((data) => parseUser(data))
}

const fetchUserRelationship = ({ id, credentials }) => {
  const url = `${MASTODON_USER_RELATIONSHIPS_URL}/?id=${id}`
  return fetch(url, { headers: authHeaders(credentials) })
    .then((response) => {
      return new Promise((resolve, reject) => response.json()
        .then((json) => {
          if (!response.ok) {
            return reject(new StatusCodeError(response.status, json, { url }, response))
          }
          return resolve(json)
        }))
    })
}

const updateUserSettings = ({ settings, credentials }) => {
  return promisedRequest({
    url: MASTODON_PROFILE_UPDATE_URL,
    method: 'PATCH',
    payload: settings,
    credentials: credentials
  }).then((data) => parseUser(data))
}

const fetchLicenses = () => {
  const url = REEL2BITS_LICENSES

  return fetch(url)
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error fetching licenses', data)
    })
    .then((data) => data.json())
}

const fetchGenres = ({ query = false }) => {
  let url = REEL2BITS_GENRES

  const params = []

  if (query) {
    params.push(['query', query])
  }

  const queryString = map(params, (param) => `${param[0]}=${param[1]}`).join('&')
  url += `?${queryString}`

  return fetch(url)
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error fetching genres', data)
    })
    .then((data) => data.json())
}

const fetchTags = ({ query = false }) => {
  let url = REEL2BITS_TAGS

  const params = []

  if (query) {
    params.push(['query', query])
  }

  const queryString = map(params, (param) => `${param[0]}=${param[1]}`).join('&')
  url += `?${queryString}`

  return fetch(url)
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error fetching tags', data)
    })
    .then((data) => data.json())
}

const fetchUserAlbums = ({ userId, short = false, credentials }) => {
  let url = REEL2BITS_ALBUMS(userId)

  const params = []
  params.push(['short', short])

  const queryString = map(params, (param) => `${param[0]}=${param[1]}`).join('&')
  url += `?${queryString}`

  return fetch(url, { headers: authHeaders(credentials) })
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error fetching albums', data)
    })
    .then((data) => data.json())
}

const albumNew = (albumInfo, store) => {
  const form = new window.FormData()
  form.append('title', albumInfo.title)
  form.append('description', albumInfo.description)
  form.append('private', albumInfo.private)
  form.append('genre', albumInfo.genre)
  form.append('tags', albumInfo.tags.map(a => a.text))
  // let the files last for dev tools inspection
  if (albumInfo.artwork) {
    let filename = 'blob.invalid'
    if (albumInfo.artwork.type === 'image/jpeg') {
      filename = 'blob.jpg'
    } else if (albumInfo.artwork.type === 'image/png') {
      filename = 'blob.png'
    } else if (albumInfo.artwork.type === 'image/gif') {
      filename = 'blob.gif'
    }
    form.append('artwork', albumInfo.artwork, filename)
  }

  return fetch(ALBUMS_NEW_URL, {
    body: form,
    method: 'POST',
    headers: authHeaders(store.getters.getToken())
  })
    .then((response) => [response.ok, response])
    .then(([ok, response]) => {
      if (ok) {
        return response.json()
      } else {
        return response.json().then((error) => { throw new Error(error.error) })
      }
    })
}

const albumFetch = ({ userId, albumId, credentials }) => {
  const url = ALBUMS_FETCH_URL(userId, albumId)

  return fetch(url, { headers: authHeaders(credentials) })
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error fetching album', data)
    })
    .then((data) => data.json())
    .then((data) => parseStatus(data))
}

const albumDelete = ({ userId, albumId, credentials }) => {
  const url = ALBUMS_DELETE_URL(userId, albumId)

  return fetch(url, {
    headers: authHeaders(credentials),
    method: 'DELETE'
  })
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error deleting album', data)
    })
}

const albumEdit = ({ userId, albumId, album, credentials }) => {
  // Do that to avoid modifying `album` and bork the vue variable (tags)
  const payload = {
    title: album.title,
    description: album.description,
    private: album.private,
    genre: album.genre,
    tags: album.tags.map(a => a.text)
  }

  return promisedRequest({
    url: ALBUMS_EDIT_URL(userId, albumId),
    method: 'PATCH',
    payload: payload,
    credentials: credentials
  }).then((data) => parseStatus(data))
}

const fetchUserLogs = (user, currentPage, perPage, store) => {
  const url = ACCOUNT_LOGS_URL(user, currentPage, perPage)
  const credentials = store.getters.getToken()

  return fetch(url, { headers: authHeaders(credentials) })
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error fetching user logs', data)
    })
    .then((data) => data.json())
}

const fetchUserQuota = (user, currentPage, perPage, store) => {
  const url = ACCOUNT_QUOTA_URL(user, currentPage, perPage)
  const credentials = store.getters.getToken()

  return fetch(url, { headers: authHeaders(credentials) })
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error fetching user quota summary', data)
    })
    .then((data) => data.json())
}

const fetchTimeline = ({
  timeline,
  credentials,
  since = false,
  until = false,
  userId = false,
  tag = false,
  withMuted = false,
  page = 1
}) => {
  const timelineUrls = {
    public: MASTODON_PUBLIC_TIMELINE,
    friends: MASTODON_USER_HOME_TIMELINE_URL,
    dms: MASTODON_DIRECT_MESSAGES_TIMELINE_URL,
    notifications: MASTODON_USER_NOTIFICATIONS_URL,
    publicAndExternal: MASTODON_PUBLIC_TIMELINE,
    user: MASTODON_USER_TIMELINE_URL,
    drafts: REEL2BITS_DRAFTS_TIMELINE,
    albums: REEL2BITS_ALBUMS_TIMELINE,
    unprocessed: REEL2BITS_UNPROCESSED_TIMELINE
  }
  const params = []

  let url = timelineUrls[timeline]

  if (timeline === 'user' || timeline === 'media') {
    url = url(userId)
  }

  if (timeline === 'albums') {
    params.push(['user', userId])
  }

  if (since) {
    params.push(['since_id', since])
  }
  if (until) {
    params.push(['max_id', until])
  }
  if (tag) {
    url = url(tag)
  }
  if (timeline === 'media') {
    params.push(['only_media', 1])
  }
  if (timeline === 'public') {
    params.push(['local', true])
  }
  if (timeline === 'public' || timeline === 'publicAndExternal') {
    params.push(['only_media', false])
  }
  if (page <= 0) {
    params.push(['page', 1])
  } else {
    params.push(['page', page])
  }

  params.push(['count', 5])
  params.push(['with_muted', withMuted])
  params.push(['paginated', true])

  const queryString = map(params, (param) => `${param[0]}=${param[1]}`).join('&')
  url += `?${queryString}`

  return fetch(url, { headers: authHeaders(credentials) })
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error fetching timeline', data)
    })
    .then((data) => data.json())
    .then((data) => {
      data.items = data.items.map(parseStatus)
      return data
    })
}

const changePassword = ({ credentials, password, newPassword, newPasswordConfirmation }) => {
  const form = new FormData()

  form.append('password', password)
  form.append('new_password', newPassword)
  form.append('new_password_confirmation', newPasswordConfirmation)

  return fetch(CHANGE_PASSWORD_URL, {
    body: form,
    method: 'POST',
    headers: authHeaders(credentials)
  })
    .then((response) => response.json())
}

const resetPassword = ({ email }) => {
  const params = { email }
  const query = reduce(params, (acc, v, k) => {
    const encoded = `${k}=${encodeURIComponent(v)}`
    return `${acc}&${encoded}`
  }, '')
  const url = `${RESET_PASSWORD_URL}?${query}`
  return fetch(url, {
    method: 'POST'
  })
}

const resetPasswordToken = ({ token, password, passwordConfirm }) => {
  const url = RESET_PASSWORD_URL_TOKEN(token)
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      token: token,
      new_password: password,
      new_password_confirmation: passwordConfirm
    })
  })
}

const followUser = ({ id, credentials }) => {
  const url = MASTODON_FOLLOW_URL(id)
  return fetch(url, {
    headers: authHeaders(credentials),
    method: 'POST'
  }).then((data) => data.json())
}

const unfollowUser = ({ id, credentials }) => {
  const url = MASTODON_UNFOLLOW_URL(id)
  return fetch(url, {
    headers: authHeaders(credentials),
    method: 'POST'
  }).then((data) => data.json())
}

const fetchFriends = ({ id, page = 1, limit = 20, credentials }) => {
  let url = MASTODON_FOLLOWING_URL(id)
  const args = [
    page && `page=${page}`,
    limit && `limit=${limit}`
  ].filter(_ => _).join('&')

  url = url + (args ? '?' + args : '')
  return fetch(url, { headers: authHeaders(credentials) })
    .then((data) => data.json())
    .then((data) => {
      data.items = data.items.map(parseUser)
      return data
    })
}

const fetchFollowers = ({ id, page = 1, limit = 20, credentials }) => {
  let url = MASTODON_FOLLOWERS_URL(id)
  const args = [
    page && `page=${page}`,
    limit && `limit=${limit}`
  ].filter(_ => _).join('&')

  url += args ? '?' + args : ''
  return fetch(url, { headers: authHeaders(credentials) })
    .then((data) => data.json())
    .then((data) => {
      data.items = data.items.map(parseUser)
      return data
    })
}

const deleteUser = ({ userId, credentials }) => {
  const headers = authHeaders(credentials)
  return fetch(MASTODON_USER_URL, {
    method: 'DELETE',
    headers: headers
  })
    .then((data) => {
      if (data.ok) {
        return data
      }
      throw new Error('Error queuing user deletion', data)
    })
    .then((data) => data.json())
}

const updateArtwork = ({ kind, objId, userId, picture, credentials }) => {
  let url = null
  if (kind === 'album') {
    url = ALBUMS_UPDATE_ARTWORK_URL(userId, objId)
  } else if (kind === 'track') {
    url = TRACKS_UPDATE_ARTWORK_URL(userId, objId)
  }

  const form = new FormData()
  let filename = 'blob.invalid'
  if (picture.type === 'image/jpeg') {
    filename = 'blob.jpg'
  } else if (picture.type === 'image/png') {
    filename = 'blob.png'
  } else if (picture.type === 'image/gif') {
    filename = 'blob.gif'
  }
  form.append('artwork', picture, filename)

  return fetch(url, {
    headers: authHeaders(credentials),
    method: 'PATCH',
    body: form
  }).then((response) => {
    if (response.ok) {
      return response.json()
    } else {
      return response.json().then((error) => { throw new Error(error.error) })
    }
  })
}

const updateAvatar = ({ credentials, avatar }) => {
  const form = new FormData()

  let filename = 'blob.invalid'
  if (avatar.type === 'image/jpeg') {
    filename = 'blob.jpg'
  } else if (avatar.type === 'image/png') {
    filename = 'blob.png'
  } else if (avatar.type === 'image/gif') {
    filename = 'blob.gif'
  }
  form.append('avatar', avatar, filename)

  return fetch(MASTODON_PROFILE_UPDATE_URL, {
    headers: authHeaders(credentials),
    method: 'PATCH',
    body: form
  }).then((data) => data.json())
    .then((data) => parseUser(data))
}

const apiService = {
  verifyCredentials,
  register,
  fetchUser,
  fetchUserRelationship,
  trackUpload,
  trackDelete,
  trackEdit,
  trackFetch,
  fetchTrackLogs,
  trackRetryProcessing,
  albumNew,
  albumDelete,
  albumFetch,
  albumEdit,
  albumReorder,
  fetchUserLogs,
  fetchUserQuota,
  fetchTimeline,
  fetchLicenses,
  fetchUserAlbums,
  updateUserSettings,
  changePassword,
  resetPassword,
  resetPasswordToken,
  followUser,
  unfollowUser,
  fetchFriends,
  fetchFollowers,
  deleteUser,
  fetchGenres,
  fetchTags,
  updateArtwork,
  updateAvatar
}

export default apiService
