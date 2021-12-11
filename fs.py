import os
import sqlite3
import mutagen


def __scanDir(cur, path, relativePath='/'):
    if path[-1] != '/':
        path += '/'
    directory = []
    for file in os.scandir(path):
        if file.is_dir():
            folderName = file.name
            directory.append(
                __scanDir(cur, f'{path}/{folderName}', relativePath=f'{relativePath}{folderName}/'))
        else:
            audiofile = mutagen.File(f'{path}{file.name}')

            if audiofile is None:
                continue

            metadata = {
                'name': file.name if 'title' not in audiofile else audiofile['title'][0],
                'artist': 'Unknown artist' if 'artist' not in audiofile else ', '.join(audiofile['artist']),
                'album': 'Unknown album' if 'album' not in audiofile else ', '.join(audiofile['album']),
                'genre': 'Unknown' if 'genre' not in audiofile else ', '.join(audiofile['genre']),
                'date': 'Unknown' if 'date' not in audiofile else ', '.join(audiofile['date'])
            }
            cur.execute(
                '''INSERT OR IGNORE INTO artists (artist_name) VALUES (?)''', (metadata['artist'],))
            cur.execute('''INSERT OR IGNORE INTO albums (album_name, artist_name) VALUES (?, ?)''',
                        (metadata['album'], metadata['artist'],))

            cur.execute('''INSERT OR IGNORE INTO songs (song_name, artist_name, album_name, genre, date, song_file_name) VALUES (?, ?, ?, ?, ?, ?)
            ''', (metadata['name'], metadata['artist'], metadata['album'], metadata['genre'], metadata['date'], relativePath + file.name))
            directory.append(relativePath + file.name)

    return directory


def scanDir(con, cur, path):
  cur = con.cursor()
  cur.execute('''CREATE TABLE IF NOT EXISTS artists
  (artist_id integer primary key, artist_name text, unique(artist_name))
  ''')

  cur.execute('''CREATE TABLE IF NOT EXISTS albums
  (album_id integer primary key, album_name text, artist_name text, unique(album_name))
  ''')

  cur.execute('''CREATE TABLE IF NOT EXISTS songs
                (song_id integer primary key, song_name text, artist_name text, album_name text, genre text, date text, song_file_name text, unique(song_name))''')

  __scanDir(cur, path)

  con.commit()