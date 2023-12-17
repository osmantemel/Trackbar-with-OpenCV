import cv2
import numpy as np

# Kamera bağlantısını başlat
cap = cv2.VideoCapture(0)

# 'nothing' fonksiyonunu tanımla (bu fonksiyon şu anki uygulamada kullanılmıyor)
def nothing(x):
    pass

# Ayarlar penceresini oluştur ve boyutunu ayarla
cv2.namedWindow("trackbar")
cv2.resizeWindow("trackbar", 500, 500)

# Alt renk sınırları için izleme çubuklarını oluştur
cv2.createTrackbar("lower-H", "trackbar", 0, 180, nothing)
cv2.createTrackbar("lower-S", "trackbar", 0, 255, nothing)
cv2.createTrackbar("lower-V", "trackbar", 0, 255, nothing)

# Üst renk sınırları için izleme çubuklarını oluştur
cv2.createTrackbar("upper-H", "trackbar", 0, 180, nothing)
cv2.createTrackbar("upper-S", "trackbar", 0, 255, nothing)
cv2.createTrackbar("upper-V", "trackbar", 0, 255, nothing)

# İlk değerleri üst sınırlara ayarla
cv2.setTrackbarPos("upper-H", "trackbar", 180)
cv2.setTrackbarPos("upper-S", "trackbar", 255)
cv2.setTrackbarPos("upper-V", "trackbar", 255)

# Sonuçları göstermek için bir pencere oluştur
cv2.namedWindow("result")

while True:
    # Kameradan bir çerçeve al
    ret, frame = cap.read()
    
    # Çerçeveyi yatay olarak çevir
    frame = cv2.flip(frame, 1)
    
    # Çerçeveyi HSV renk uzayına dönüştür
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Alt renk sınırları için izleme çubuklarından değerleri al
    lower_h = cv2.getTrackbarPos("lower-H", "trackbar")
    lower_s = cv2.getTrackbarPos("lower-S", "trackbar")
    lower_v = cv2.getTrackbarPos("lower-V", "trackbar")

    # Üst renk sınırları için izleme çubuklarından değerleri al
    upper_h = cv2.getTrackbarPos("upper-H", "trackbar")
    upper_s = cv2.getTrackbarPos("upper-S", "trackbar")
    upper_v = cv2.getTrackbarPos("upper-V", "trackbar")

    # Alt ve üst renk sınırlarını belirle
    lower_color = np.array([lower_h, lower_s, lower_v])
    upper_color = np.array([upper_h, upper_s, upper_v])

    # Renk sınırları arasındaki renkleri içeren maskeyi oluştur
    mask = cv2.inRange(frame_hsv, lower_color, upper_color)

    # Maskeyi orijinal çerçeve üzerine uygula
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Orijinal çerçeve ve maskeyi yatay olarak birleştir
    combined = np.hstack((frame, result))

    # Sonuçları göster
    cv2.imshow("result", combined)

    # 'q' tuşuna basılırsa döngüden çık
    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

# Kamera bağlantısını kapat
cap.release()

# Tüm pencereleri kapat
cv2.destroyAllWindows()
