import speech_recognition as sr
from fuzzywuzzy import process


# To add your own voice commands just write a function
# with any name and then add it to the if chain in the
# while True loop down below.
# Good design I know
def play_example(song):
    # Songs could come from a specific folder, e.g.
    # `os.listdir('songs')`
    example_songs = [
        'Dmitri Shostakovich - Waltz No. 2',
        'XI - Blue Zenith',
        'Popeda - Lihaa ja perunaa'
    ]

    if not song:
        # Someone said "play" and nothing else
        best_match = choice(examples_songs)
    else:
        # Fuzzy match all the titles and take the closest one
        best_match = process.ExtractOne(song_title, example_songs)
    # You could actually do something with that information here
    print('Best match from examples songs: ', best_match)


rec = sr.Recognizer()

with sr.Microphone() as mic:
    rec.adjust_for_ambient_noise(mic)

    while True:
        audio = rec.listen(mic)

        try:
            command = rec.recognize_sphinx(audio)
            command, _, rest = command.partition(' ')

            if command == 'play':
                play_example(rest)
        except sr.UnknownValueError:
            # Couldn't recognize audio
            pass

