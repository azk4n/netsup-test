import axios from 'axios'

const CSRF_COOKIE_NAME = 'csrftoken'
const CSRF_HEADER_NAME = 'X-CSRFToken'

axios.defaults.baseURL = 'http://localhost:5000'
// axios.defaults.baseURL = 'http://157.230.7.236/'

const Session = axios.create({
  xsrfCookieName: CSRF_COOKIE_NAME,
  xsrfHeaderName: CSRF_HEADER_NAME
})

export default Session
