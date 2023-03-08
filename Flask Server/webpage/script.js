const video = document.getElementById("video");
const inputCanvas = document.getElementById("input-canvas");
const inputCanvasCTX = inputCanvas.getContext("2d");
const drawCanvas = document.getElementById("over-video-canv");
const ctx = drawCanvas.getContext("2d");

// gloable variable to revice data
let data = {};

// function declaration
function openWebCam() {
  navigator.mediaDevices
    .getUserMedia({
      video: true,
      audio: false,
    })
    .then((stream) => {
      // Changing the source of video to current stream.
      video.srcObject = stream;
      video.addEventListener("loadedmetadata", () => {
        video.play();
      });
    })
    .catch(alert);
}

function putFrame() {
  // setting canvas
  inputCanvas.width = video.videoWidth;
  inputCanvas.height = video.videoHeight;
  drawCanvas.width = video.videoWidth;
  drawCanvas.height = video.videoHeight;

  // draw webcam frames on canvas
  inputCanvasCTX.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);

  // turn frame into a blob to be send to server
  inputCanvas.toBlob((blob) => {
    //This code runs AFTER the Blob is extracted
    let fd = new FormData();
    fd.append("field-name", blob, "image-filename.png");
    // making request
    let req = new Request("http://127.0.0.1:5000/Rx_frame", {
      method: "POST",
      body: fd,
      mode: "cors",
    });

    // Sending request
    fetch(req).then((res) => {
      res.json().then((json) => {
        data = json;
        console.log(json);
      });

      // check if res is not empyt
      if (Object.keys(data).length > 0) {
        drawRect(data);
      }
    });
  });
}

function drawRect(data) {
  inputCanvasCTX.lineWidth = "2";
  inputCanvasCTX.strokeStyle = "red";
  inputCanvasCTX.rect(
    data.corrdinates.x_min - 10,
    data.corrdinates.y_min - 5,
    Math.abs(data.corrdinates.x_max - data.corrdinates.x_min) + 10,
    Math.abs(data.corrdinates.y_max - data.corrdinates.y_min) + 5
  );

  inputCanvasCTX.stroke();
}

// main code
openWebCam();
setInterval(putFrame, 100);
