import cv2
from fer import FER
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='',   #Enter your client_id
                                               client_secret='', #Enter your client_secret
                                               redirect_uri='', #Enter your redirect_uri.
                                               scope='user-modify-playback-state'))


def get_playlist_url(emotion_data):
    #use any desired Spotity Playlists according to thier respective emotions.
    happy_playlist_uri = "https://open.spotify.com/playlist/2gSHA2hK9utrPK6ldtJgws"
    sad_playlist_uri = "https://open.spotify.com/playlist/1ERdXeiTQ8CixFdXV2t1oD"
    angry_playlist_uri = "https://open.spotify.com/playlist/609gQW5ztNwAkKnoZplkao"

    if emotion_data == "happy":
        return happy_playlist_uri
    elif emotion_data == "sad":
        return sad_playlist_uri
    elif emotion_data == "angry":
        return angry_playlist_uri
    else:
        return "No playlist available for this emotion."


def play_music_based_on_emotion(emotion_data):
    playlist_uri = get_playlist_url(emotion_data)
    print(f"You can listen to the {emotion_data} music playlist here: {playlist_uri}")


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    detector = FER()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.putText(frame, "Press 'C' to Capture Image", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'Q' to Quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow('Video Capture', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            emotion_data = detector.top_emotion(frame)
            if emotion_data:
                emotion_label, score = emotion_data
                print(f"Detected Emotion: {emotion_label} with confidence: {score:.2f}")
                play_music_based_on_emotion(emotion_label)

            cv2.imshow('Emotion Detected', frame)
            cv2.waitKey(2000)

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
