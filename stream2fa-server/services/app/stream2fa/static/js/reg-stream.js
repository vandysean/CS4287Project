// constants
const URL = 'http://35.153.43.136:8000/register/user/stream';
const USERNAME = document.getElementById("username").value;
const RATE = 10;
const SECONDS = 1000;
const ALLOWED_TIME = 20;

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

var maxNumEncodingsSaved = -1;

var isRegistered = false;
var registrationFailed = false;
var timeoutOccurred = false;

function streamIsOver() {
	return isRegistered || registrationFailed || timeoutOccurred;
}

async function updateProgressBar(numEncodingsSaved) {	
	let percentWidth = Math.round(100 * (numEncodingsSaved / maxNumEncodingsSaved))
	if (percentWidth > 100) {
		percentWidth = 100;
	}

	progressBar.style.width = percentWidth + "%";
}

async function handleSuccess() {
	if (!timeoutOccurred && !registrationFailed) {
		isRegistered = true;
		instructions.style.color = "#4bb543";
		instructions.innerHTML = "Successfully registered " + USERNAME + "!";
		progressBar.style.backgroundColor = "#4bb543";

		setTimeout(() => {
			const successLink = document.getElementById("success-url");
			successLink.click()
		}, 1 * SECONDS)
	}
}

async function handleFailure() {
	if (!isRegistered && !timeoutOccurred) {
		registrationFailed = true;
		instructions.style.color = "#fc100d";
		instructions.innerHTML = "Registration unsuccessful";

		progressBar.style.backgroundColor = "#fc100d";

		setTimeout(() => {
			const failureLink = document.getElementById("failure-url");
			failureLink.click()
		}, 1 * SECONDS)
	}
}

async function handleTimeout() {
	if (!isRegistered && !registrationFailed) {
		timeoutOccurred = true;
		instructions.style.color = "#fc100d";
		instructions.innerHTML = "Registration timed out";

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

		return responseJson;
	} catch (err) {
		console.log(err);
		return 'ongoing'
	}
}

async function kickoffStream() {
	const startTime = Date.now();
	const endTime = startTime + ALLOWED_TIME * SECONDS

	for (let i = 1; !streamIsOver() && cameraStream != null; ++i) {
		if (Date.now() > endTime) {
			await handleTimeout()
		}

		if (i % RATE === 0) {
			ctx.drawImage(stream, 0, 0, capture.width, capture.height);
			const uri = capture.toDataURL('image/png');

			const responseJson = await sendFrameToServer(uri);

			const responseStatus = responseJson['status'];
			const numEncodingsSaved = responseJson['encodings_saved'];
			if (maxNumEncodingsSaved < 0) {
				maxNumEncodingsSaved = responseJson['max_encodings_saved'];
			}

			await updateProgressBar(numEncodingsSaved);

			if (responseStatus === 'complete' || numEncodingsSaved >= maxNumEncodingsSaved) {
				await handleSuccess();
			} else if (responseStatus === 'failed') {
				await handleFailure();
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

			instructions.innerHTML = "Registration in progress, remain close to camera...<br>Make sure only you are in frame";
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
