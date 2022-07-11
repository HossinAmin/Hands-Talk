(async function meet_gp() {
	'use strict'

	// Create preview video
	const video = document.createElement('video')
	video.setAttribute('playsinline', '')
	video.setAttribute('autoplay', '')
	video.setAttribute('muted', '')

	
	var img = document.createElement("img")
	// img.style.width = "300px"
	// img.style.height = "300px"
	// img.style.position = "absolute"
	// img.style.zIndex = 60000
	// document.body.append(img)

	// Configs
	// Text config
	const text = []

	// Video config
	const fps = 10

	// Request config
	//const useText = false;


	// Create canvases
	const canvases = Object.fromEntries(['buffer','pure', 'display'].map(name => {
		const element = document.createElement('canvas')
		const context = element.getContext('2d')
		return [name, {
			element,
			context
		}]
	}))

	let task = 0
	let listen = false

	// Injected script script
	addEventListener('message', function(event) {
		if (event.data && event.data.extensionMessage && event.data.extensionMessage.action) {
				listen = event.data.extensionMessage.action === 'start'
		}
	});

	function buildRequest(imgBlob) {
		const fd = new FormData()
		fd.append('field-name', imgBlob, 'image-filename.png')
		return new Request('http://127.0.0.1:5000/Rx_frame', {
        method: 'POST',
        body: fd
      })
	}


	// Send image and get image
	function setImageAfterProcessing(ctx,width,height){

		canvases.buffer.context.canvas.toBlob((blob) => {

			const req = buildRequest(blob)
			fetch(req)
				.then(response => response.blob())
				.then(function(myBlob){
					console.log(myBlob.size)
					img.src = URL.createObjectURL(myBlob)
					img.onload = function() {
						canvases.display.context.clearRect(0,0,width,height)
						canvases.display.context.drawImage(img,0,0)
					}

				}).catch(err => console.error("Fetch Error: ", err))
    	})
  	}

	function draw(width, height) {
		const fill = [0, 0, width, height]
		const { context } = canvases.buffer
		
		context.clearRect(...fill)

		 if (video.srcObject){
			// TODO: Remove this line and uncomment the above
			context.drawImage(video, 0, 0, width, height)

		} else {
			// Draw preview stripes if video doesn't exist
			'18, 100%, 68%; -10,100%,80%; 5, 90%, 72%; 48, 100%, 75%; 36, 100%, 70%; 20, 90%, 70%'
			.split(';')
				.forEach((color, index) => {
					context.fillStyle = `hsl(${color})`
					context.fillRect(index * width / 6, 0, width / 6, height)
				})
		}

	if(listen){		

			setImageAfterProcessing(context,width,height)

		}
		else{
			canvases.display.context.clearRect(0,0,width,height)
			canvases.display.context.drawImage(canvases.buffer.element, 0, 0)	
		}

	}

	class MeetMediaStream extends MediaStream {

		constructor(old_stream) {
			// Copy original stream settings
			super(old_stream)
			video.srcObject = old_stream

			const { width, height } = old_stream.getVideoTracks()[0].getSettings()
			Object.values(canvases).forEach(canvas => {
				canvas.element.width = width
				canvas.element.height = height
			})
			// Amp: for values that can range from 0 to +infinity, amp**value does the mapping.
			clearInterval(task)
			task = setInterval(draw, 1000/fps, width, height)
			const new_stream = canvases.display.element.captureStream(fps)
			new_stream.addEventListener('inactive', () => {
				old_stream.getTracks().forEach(track => track.stop())
				canvases.display.context.clearRect(...fill)
				video.srcObject = null
			})
			return new_stream
		}
	}

	MediaDevices.prototype.old_getUserMedia = MediaDevices.prototype.getUserMedia
	MediaDevices.prototype.getUserMedia = async constraints =>
		(constraints && constraints.video && !constraints.audio) ?
		new MeetMediaStream(await navigator.mediaDevices.old_getUserMedia(constraints)) :
		navigator.mediaDevices.old_getUserMedia(constraints)
})()
