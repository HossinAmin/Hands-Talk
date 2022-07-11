let capFrameButton= document.getElementById("capFrameButton");
let video = document.getElementById("video")

function openWebCam()
{
    navigator.mediaDevices
    .getUserMedia({
      video: true, audio: false,
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



video.addEventListener("timeupdate",(ev)=>{
  
  var inputCanvas = document.getElementById("inputCanvas");

  inputCanvas.width = video.videoWidth;
  inputCanvas.height = video.videoHeight;
  var canvasContext = inputCanvas.getContext("2d");
  canvasContext.drawImage(video, 0, 0,500,500);
  let blob = inputCanvas.toBlob((blob) => {
    //this code runs AFTER the Blob is extracted
    let fd = new FormData();
    fd.append('field-name', blob, 'image-filename.png');
    let req = new Request( 'http://127.0.0.1:5000/Rx_frame', {
        method: 'POST',
        body: fd
    })
    fetch(req)
    .then(response=>response.blob())
    .then(function(myBlob)
    {
      var imgEL = document.getElementById("disImag");
      
      imgEL.src = URL.createObjectURL(myBlob);;
      
    }
    )

  });

  
});

// main code
openWebCam();