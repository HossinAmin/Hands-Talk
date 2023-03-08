const video = document.getElementById("video");
const outputCanvas = document.getElementById("input-canvas");
const outputCanvasCTX = outputCanvas.getContext("2d");

let previousState = {
  x: undefined,
  y: undefined,
};

let currentState = {
  x: undefined,
  y: undefined,
};

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

  // turn frame into a blob to be send to server
  outputCanvas.toBlob((blob) => {
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
        // check if res is not empyt
        currentState = json;
      });
    });
  });
}

requestAnimationFrame(drawRect);

function drawRect() {
  outputCanvas.width = video.videoWidth;
  outputCanvas.height = video.videoHeight;

  // draw webcam frames on canvas
  outputCanvasCTX.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
  const { coordinates } = currentState;

  let xDelta = Math.abs(coordinates?.x_min || 0 - previousState.x || 0);
  let yDelta = Math.abs(coordinates?.y_min || 0 - previousState.y || 0);
  let stepSize = (xDelta + yDelta) / 20;

  let xTrace = xDelta / stepSize;
  let yTrace = yDelta / stepSize;

  outputCanvasCTX.lineWidth = "2";
  outputCanvasCTX.strokeStyle = "red";
  outputCanvasCTX.rect(
    previousState.x - 10 + xTrace,
    previousState.y - 5 + yTrace,
    Math.abs(coordinates?.x_max - coordinates?.x_min) + 10,
    Math.abs(coordinates?.y_max - coordinates?.y_min) + 5
  );
  outputCanvasCTX.stroke();

  previousState = {
    x: coordinates?.x_min,
    y: coordinates?.y_min,
  };

  requestAnimationFrame(drawRect);
}

// main code
openWebCam();
setInterval(putFrame, 100);
// setInterval(drawRect, 100);
