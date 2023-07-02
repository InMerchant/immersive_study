// 이미지 파일 이름 배열
const photoImages = [
  "potato.jpg",
  "sweet potato.jpg",
  "washingmachine.jpg",
  "Squid.jpg",
  "golf.jpg",
  "iron.jpg",
  "camera.jpg",
  "rabbit.jpg",
  "Cotton candy.jpg"
];

// 현재 이미지 인덱스
let currentImageIndex = 0;

window.addEventListener('DOMContentLoaded', (event) => {
  const resultElement = document.querySelector('.result');

  showPhoto(photoImages[currentImageIndex], 1);
  showPhoto(photoImages[currentImageIndex + 1], 2);

  const API = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (API) {
    const recognition = new API();

    recognition.continuous = true;
    recognition.lang = 'en-GB';

    const button = document.querySelector('.speech-recognition');
    const speechResult = document.querySelector('.result');
    const userSpeech = document.querySelector('.user-speech');
    const imageWrapper = document.querySelector('.image-container');

    button.addEventListener('click', () => {
      recognition.start();
      button.textContent = 'Listening...';
    });

    recognition.onresult = (event) => {
      const result = event.results[event.results.length - 1][0].transcript;
      speechResult.textContent = result;
      userSpeech.textContent = `You said: ${result}`; // 사용자가 한 말 출력
      guessPhoto(result);
    };
  }
});


// 이미지 보여주기
function showPhoto(imageUrl, imageIndex) {
  const imageElement = document.getElementById(`photoImage${imageIndex}`);
  if (imageElement) {
    imageElement.src = imageUrl;
  }
}

// 음성과 이미지 비교하여 처리
function guessPhoto(photo) {
  const resultElement = document.querySelector(".result");
  const currentImageName = photoImages[currentImageIndex].toLowerCase();
  const spokenWord = photo.toLowerCase().split(".")[0];
  const imageWrapper = document.querySelector(".image-container");

  if (currentImageName.includes(spokenWord)) {
    resultElement.textContent = "정답입니다! 다음 이미지를 맞춰보세요.";

    const currentImageElement = imageWrapper.children[currentImageIndex];
    const circleElement = document.createElement("div");
    circleElement.classList.add("circle");
    currentImageElement.appendChild(circleElement);

    setTimeout(() => {
      currentImageElement.removeChild(circleElement);
      currentImageIndex++;

      if (currentImageIndex < photoImages.length) {
        showPhoto(photoImages[currentImageIndex], 1);
        showPhoto(photoImages[currentImageIndex + 1], 2);
      } else {
        resultElement.textContent = "더 이상 사진이 없습니다.";
        imageWrapper.style.display = "none";
      }
    }, 5000);
  } else {
    resultElement.textContent = "틀렸습니다. 다른 단어를 시도해보세요.";
  }
}
