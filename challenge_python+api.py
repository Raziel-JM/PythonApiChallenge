import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Función para obtener las credenciales desde el archivo
def get_spotify_credentials():
    with open('credentials.txt') as f:
        credentials = f.read().splitlines()
        client_id = credentials[0]
        client_secret = credentials[1]
    return client_id, client_secret

# Función para buscar y mostrar las canciones más populares de un artista
def buscar_canciones_populares(artist_name):
    client_id, client_secret = get_spotify_credentials()

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                               client_secret=client_secret))

    results = sp.search(q=artist_name, type='artist', limit=1)
    
    if not results['artists']['items']:
        print(f"No se encontró información para el artista {artist_name}")
        return

    artist_id = results['artists']['items'][0]['id']
    top_tracks = sp.artist_top_tracks(artist_id)

    print(f"\nLas 10 canciones más populares de {artist_name} en Spotify son:\n")
    for idx, track in enumerate(top_tracks['tracks']):
        print(f"{idx + 1}. {track['name']} - Popularidad: {track['popularity']}")

    return top_tracks['tracks']

# Función para gestionar la lista de reproducción
def gestionar_lista_reproduccion(tracks):
    lista_reproduccion = []

    while True:
        try:
            seleccion = int(input("\nIngrese el número de la canción que desea agregar (1-10), "
                                   "o 0 para salir: "))

            if seleccion == 0:
                break
            elif 1 <= seleccion <= 10:
                cancion_seleccionada = tracks[seleccion - 1]
                lista_reproduccion.append(cancion_seleccionada)
                print(f"\nCanción agregada: {cancion_seleccionada['name']}")
            else:
                print("Por favor, ingrese un número válido (1-10).")

        except ValueError:
            print("Por favor, ingrese un número entero.")

    return lista_reproduccion

# Función para calcular la duración total de la lista de reproducción
def calcular_duracion_total(lista_reproduccion):
    duracion_total = sum(track['duration_ms'] for track in lista_reproduccion)
    duracion_total_minutos = duracion_total / 60000
    return duracion_total_minutos

# Función principal
def main():
    artist_name = input("Ingrese el nombre del artista: ")
    top_tracks = buscar_canciones_populares(artist_name)

    if top_tracks:
        lista_reproduccion = gestionar_lista_reproduccion(top_tracks)
        
        if len(lista_reproduccion) >= 2:
            duracion_total = calcular_duracion_total(lista_reproduccion)
            print(f"\nDuración total de la lista de reproducción: {duracion_total:.2f} minutos")

if __name__ == "__main__":
    main()

