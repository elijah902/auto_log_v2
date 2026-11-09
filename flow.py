import google.oauth2.credentials
import google_auth_oauthlib.flow

# Retrieves the client ID from client_secret.json file. 
flow = google_auth_oauth.flow.Flow.from_client_secrets_file('client_secrets.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets'])

flow.redirect_uri = 'http://localhost:8000'

authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true'
)

return flask.redirect(authorization_url)