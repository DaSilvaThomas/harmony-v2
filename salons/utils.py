import requests
from django.conf import settings

def search_jamendo_tracks(query='popular', limit=10):
    """
    Recherche de morceaux via l'API Jamendo
    """
    url = f"{settings.JAMENDO_API_BASE_URL}/tracks/"
    params = {
        'client_id': settings.JAMENDO_CLIENT_ID,
        'format': 'json',
        'limit': limit,
        'search': query,
        'include': 'musicinfo',
        'audioformat': 'mp32'
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            tracks = []
            for track in data.get('results', []):
                tracks.append({
                    'jamendo_id': track.get('id'),
                    'titre': track.get('name'),
                    'artiste': track.get('artist_name'),
                    'album': track.get('album_name', ''),
                    'cover_url': track.get('album_image', ''),
                    'preview_url': track.get('audio', ''),
                    'duree': track.get('duration', 30)
                })
            return tracks
    except Exception as e:
        print(f"Erreur Jamendo API: {e}")
    
    return []