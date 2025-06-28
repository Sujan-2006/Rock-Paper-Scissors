import pyrebase
firebaseConfig = {
  "apiKey": "AIzaSyBgsdZ_rn42e6vvpX6rGS1OivEtNWDgqdE",
  "authDomain": "rockpaperscissor-db3f2.firebaseapp.com",
  "databaseURL": "https://rockpaperscissor-db3f2-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "rockpaperscissor-db3f2",
  "storageBucket": "rockpaperscissor-db3f2.firebasestorage.app",
  "messagingSenderId": "700641582387",
  "appId": "1:700641582387:web:27ff785387537fe750b246",
  "measurementId": "G-RVNZCQHN65"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()