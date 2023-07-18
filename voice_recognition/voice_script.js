// 이미지 파일 이름 배열
const photoImages = [
  "세탁기.jpg",
  "오징어.jpg",
  "골프.jpg",
  "다리미.jpg",
  "카메라.jpg",
  "토끼.jpg",
  "솜사탕.jpg"
];

const API = window.SpeechRecognition || window.webkitSpeechRecognition;

if (API) {
  const recognition = new API();

  recognition.continuous = true;
  recognition.lang = 'ko-kr';
  let filename1 = '감자';
  let filename2 = '고구마';

  const button = document.querySelector('.speech-recognition');
  const speechResult = document.querySelector('.result');
  const photo1 = document.querySelector('#photo1');
  const photo2 = document.querySelector('#photo2');
  const message1 = document.querySelector('#message1');
  const message2 = document.querySelector('#message2');
  const usedImages = [];

  button.addEventListener('click', () => {
    recognition.start();
    button.textContent = 'Listening...';
  });

  recognition.onresult = (event) => {
    const results = event.results;

    for (let i = 0; i < results.length; i++) {
      const transcript = results[i][0].transcript;
      speechResult.textContent = transcript;

      if (transcript.includes(filename1)&& !transcript.includes(filename2)) {
        changephoto1();
      }
      if (transcript.includes(filename2)&& !transcript.includes(filename1)) {
        changephoto2();
      }
    }
  };

  function changephoto1() {
    const availableImages = photoImages.filter((path) => !usedImages.includes(path));
    if (availableImages.length > 0) {
        const image = availableImages[Math.floor(Math.random() * availableImages.length)];
        filename1 = extractFileName(image);
        photo1.src = image;
        usedImages.push(image);
        message1.textContent = '';
        circle1.style.display = 'block';
        setTimeout(() => {
          circle1.style.display = 'none';
        }, 3000); 
      }
      else {
        photo1.style.display='none'
        message1.textContent = '이미지가 끝났습니다.';
      }
  }
  function changephoto2() {
    const availableImages = photoImages.filter((path) => !usedImages.includes(path));
    if (availableImages.length > 0) {
        const image = availableImages[Math.floor(Math.random() * availableImages.length)];
        filename2 = extractFileName(image);
        photo2.src = image;
        usedImages.push(image);
        message2.textContent = '';
        circle2.style.display = 'block';
        setTimeout(() => {
          circle2.style.display = 'none';
        }, 3000); 
    }
      else {
        photo2.style.display='none'
        message2.textContent = '이미지가 끝났습니다.';
      }
  }
  function extractFileName(photoImages) {
    return photoImages.match(/(.+)\./)[1];
  }
}
