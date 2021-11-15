// constants
const URL = 'http://35.153.43.136:8000/auth/user/stream';
const USERNAME = document.getElementById("username").value;
const RATE = 10;
const SECONDS = 1000;
const ALLOWED_TIME = 20;
const NUM_SUCCESSFUL_NEEDED = 15;

// stream elements
var stream = document.getElementById("stream");
var capture = document.getElementById("capture");
var ctx = capture.getContext('2d');
var cameraStream = null;

capture.width = stream.width;
capture.height = stream.height;

// instructions and progress bar
var instructions = document.getElementById('instructions');
var progressBar = document.getElementById('progress-bar');

var isAuthenticated = false;
var timeoutOccurred = false;

function streamIsOver() {
	return isAuthenticated || timeoutOccurred;
}

async function updateProgressBar(numSuccess) {	
	let percentWidth = Math.round(100 * (numSuccess / NUM_SUCCESSFUL_NEEDED))
	if (percentWidth > 100) {
		percentWidth = 100;
	}

	progressBar.style.width = percentWidth + "%";
}

async function handleSuccess() {
	if (!timeoutOccurred) {
		isAuthenticated = true;
		instructions.style.color = "#4bb543";
		instructions.innerHTML = "Successfully authenticated " + USERNAME + "!";
		progressBar.style.backgroundColor = "#4bb543";

		setTimeout(() => {
			const successLink = document.getElementById("success-url");
			successLink.click()
		}, 1 * SECONDS)
	}
}

async function handleFailure() {
	if (!isAuthenticated) {
		timeoutOccurred = true;
		instructions.style.color = "#fc100d";
		instructions.innerHTML = "Authentication unsuccessful";

		progressBar.style.backgroundColor = "#fc100d";

		setTimeout(() => {
			const failureLink = document.getElementById("failure-url");
			failureLink.click()
		}, 1 * SECONDS)
	}
}

async function sendFrameToServer(uri) {
	const body = {
		uri: uri,
		username: USERNAME
	};

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
		
		const responseJson = await response.json();

		return responseJson['status'];
	} catch (err) {
		console.log(err);
		return 'ongoing'
	}
}

async function kickoffStream() {
	const startTime = Date.now();
	const endTime = startTime + ALLOWED_TIME * SECONDS;
	var numSuccess = 0;

	for (let i = 1; !streamIsOver() && cameraStream != null; ++i) {
		if (Date.now() > endTime) {
			await handleFailure()
		}

		if (i % RATE === 0) {
			ctx.drawImage(stream, 0, 0, capture.width, capture.height);
			const uri = capture.toDataURL('image/png');

			const responseStatus = await sendFrameToServer(uri);
			
			if (responseStatus === 'success') {
				++numSuccess;
				await updateProgressBar(numSuccess);

				if (numSuccess >= NUM_SUCCESSFUL_NEEDED) {
					await handleSuccess();
				}
			} else if (responseStatus !== 'ongoing') {
				console.log('ERROR: ' + responseStatus);
			}
		}
	}
}

// Start Streaming
async function startStreaming() {

	var mediaSupport = 'mediaDevices' in navigator;

	if (mediaSupport && null === cameraStream) {

		navigator.mediaDevices.getUserMedia({ video: true })
		.then(function(mediaStream){
			cameraStream = mediaStream;

			stream.srcObject = mediaStream;

			stream.play();

			instructions.innerHTML = "Authentication in progress...<br>Make sure your face is close to the camera"
			kickoffStream();
		})
		.catch(function(err) {
			console.log("Unable to access camera: " + err);
		});
	} else if (!mediaSupport) {
		instructions.innerHTML = 'Your browser does not support media devices';
		setTimeout(() => {
			const failureLink = document.getElementById("failure-url");
			failureLink.click()
		}, 2 * SECONDS)
	}
}

startStreaming();
