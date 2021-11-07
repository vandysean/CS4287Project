// constants
const URL = 'http://35.153.43.136:8000/auth/user/stream';
const USERNAME = document.getElementById("username").value;
const APP = document.getElementById("app").value;
const RATE = 10;
const SECONDS = 1000;
const ALLOWED_TIME = 15;

// stream elements
var stream = document.getElementById( "stream" );
var capture = document.getElementById( "capture" );
var cameraStream = null;
capture.width = stream.width / 3;
capture.height = stream.height / 3;

// instructions and progress bar
var instructions = document.getElementById('instructions');
var progressBar = document.getElementById('progress-bar')
const PROGRESS_BAR_MAX_WIDTH = document.getElementById('progress-bar-container').width;

var isAuthenticated = false;
var timeoutOccurred = false;

async function updateProgressBar() {
	const maxTimeElapsed = ALLOWED_TIME * SECONDS;
	const startTime = Date.now();

	while (Date.now() - startTime <= maxTimeElapsed) {
		let percentWidth = 100 * ((Date.now() - startTime) / maxTimeElapsed);
		if (percentWidth > 100) {
			percentWidth = 100;
		}

		progressBar.style.width = Math.round(percentWidth) + "%";
	}
}

async function handleSuccess() {
	if (!timeoutOccurred) {
		isAuthenticated = true;
		instructions.style.color = "#4bb543";
		instructions.innerHTML = "Successfully authenticated " + USERNAME + "!";

		setTimeout(() => {
			const successLink = document.getElementById("success-url");
			successLink.click()
		}, 2 * SECONDS)
	}
}

async function handleFailure() {
	if (!isAuthenticated) {
		timeoutOccurred = true;
		instructions.style.color = "#fc100d";
		instructions.innerHTML = "Authentication unsuccessful";

		setTimeout(() => {
			const failureLink = document.getElementById("failure-url");
			failureLink.click()
		}, 2 * SECONDS)
	}
}

async function sendFrameToServer() {
	body = {
		uri: capture.toDataURL( "image/png" ),
		username: USERNAME,
		app: APP
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
		const responseStatus = responseJson['status'];

		return responseStatus
	} catch (err) {
		console.log(err);
		return 'ongoing'
	}
}

async function kickoffStream() {
	for (let i = 1; cameraStream != null; ++i) {
		if (i % RATE === 0) {
			const responseStatus = await sendFrameToServer();

			if (responseStatus === 'success') {
				await handleSuccess()
			} else if (responseStatus !== 'ongoing') {
				console.log('ERROR: ' + responseStatus)
			}
		}
	}
}

async function kickoffBackgroundProcesses() {
	setTimeout(() => {
		instructions.innerHTML = "Stream starting in 3";

		setTimeout(() => {
			instructions.innerHTML += ", 2";

			setTimeout(() => {
				instructions.innerHTML += ", 1...";

				setTimeout(() => {
					instructions.innerHTML = "Authentication in progress...";

					kickoffStream();
					updateProgressBar();
					setTimeout(handleFailure, ALLOWED_TIME * SECONDS);

				}, 1 * SECONDS);

			}, 1 * SECONDS);

		}, 1 * SECONDS);

	}, 2 * SECONDS)
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

			kickoffBackgroundProcesses()
		})
		.catch(function(err) {

			console.log("Unable to access camera: " + err);
		});
	} else if (cameraStream !== null) {
		console.log("")
	} else {
		alert('Your browser does not support media devices.');
		return;
	}
}

startStreaming()
