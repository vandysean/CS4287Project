// constants
const URL = 'http://35.153.43.136:8000/auth/user/stream'
const USERNAME = document.getElementById("username").value
const APP = document.getElementById("app").value
const RATE = 10
const STREAM_TIME = 15 * 1000 // 10 seconds

// The buttons to start & stop stream and to capture the image
var btnStart = document.getElementById( "btn-start" );
var btnStop = document.getElementById( "btn-stop" );

// The stream & capture
var stream = document.getElementById( "stream" );
var capture = document.getElementById( "capture" );
capture.width = stream.width
capture.height = stream.height
// The video stream
var cameraStream = null;

var SHOULD_STREAM = true

// Attach listeners
btnStart.addEventListener( "click", startStreaming );
btnStop.addEventListener( "click", stopStreaming );

async function sendFrameToServer(num, uri) {
	body = {
		uri: uri,
		username: USERNAME,
		app: APP
	}

	try {
		const response = await fetch(URL, {
			method: 'POST',
			mode: 'cors',
			cache: 'no-cache',
			credentials: 'same-origin',
			headers: {
			'Content-Type': 'application/json',
			'accept': 'application/json'
			},
			redirect: 'follow',
			referrerPolicy: 'no-referrer',
			body: JSON.stringify(body)
		});
		
		const responseText = await response.text();

		console.log(num + ": " + responseText)
	} catch(err) {
		console.log(err)
	}
}

// 12.35 frames/sec on firefox
// 11.2 frames/sec on edge
// 1.55? frames/sec on chrome
// 13.15 on opera
async function streamToServer() {
	for(let i = 1; SHOULD_STREAM && cameraStream != null; ++i) {
		if(i % RATE === 0) {
			await sendFrameToServer(i)
		}
	}
}

async function doStream() {
	for(let i = 1; SHOULD_STREAM && cameraStream != null; ++i) {
		// var ctx = capture.getContext( '2d' );
		// var img = new Image();

		// ctx.drawImage( stream, 0, 0, capture.width, capture.height );
	
		uri = capture.toDataURL( "image/png" );

		// img.src		= uri;
		// img.width	= 320;
        // img.height  = 240;

		// snapshot.innerHTML = '';

		// snapshot.appendChild( img );
		if(i % RATE === 0) {
			await sendFrameToServer(i, uri)
		}
	}
}

// Start Streaming
function startStreaming() {

	var mediaSupport = 'mediaDevices' in navigator;

	if( mediaSupport && null === cameraStream ) {

		navigator.mediaDevices.getUserMedia( { video: true } )
		.then( function( mediaStream ) {
			SHOULD_STREAM = true

			cameraStream = mediaStream;

			stream.srcObject = mediaStream;

			stream.play();

			doStream()

			// streamToServer();

			// setTimeout(() => { SHOULD_STREAM = false; }, STREAM_TIME);
		})
		.catch( function( err ) {

			console.log( "Unable to access camera: " + err );
		});
	} else if(cameraStream !== null) {
		console.log("")
	} else {

		alert( 'Your browser does not support media devices.' );

		return;
	}
}

// Stop Streaming
function stopStreaming() {

	if( null != cameraStream ) {

		var track = cameraStream.getTracks()[ 0 ];

		track.stop();
		stream.load();

		cameraStream = null;
	}
}

function captureSnapshot() {

	if( null != cameraStream ) {

		var ctx = capture.getContext( '2d' );
		var img = new Image();

		ctx.drawImage( stream, 0, 0, capture.width, capture.height );
	
		data = capture.toDataURL( "image/png" );

		img.src		= data;
		img.width	= 320;
        img.height  = 240;

		snapshot.innerHTML = '';

		snapshot.appendChild( img );
	}
}