const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    const responseDiv = document.getElementById('response');
    // const stopButton = document.getElementById('stopButton');

    // Start recognition automatically
    recognition.start();

    recognition.onresult = (event) => {
        const transcript = event.results[event.results.length - 1][0].transcript; 
        responseDiv.innerHTML = `You said: ${transcript}`;
        console.log(`Recognized text: ${transcript}`);

        // Send recognized command to Python Eel
        eel.process_command(transcript)(function(response) {
            responseDiv.innerHTML += `<br>Response from AI: ${response}`;
            // Restart recognition after AI response
            recognition.start();
        });
    };

    recognition.onerror = (event) => {
        responseDiv.innerHTML = `Error occurred: ${event.error}`;
        console.error(`Error: ${event.error}`);
    };

    recognition.onend = () => {
        console.log('Recognition ended. Restarting...');
        responseDiv.innerHTML += '<br>Listening stopped. Restarting...';
        recognition.start(); 
    };

    stopButton.addEventListener('click', () => {
        recognition.stop();
        responseDiv.innerHTML += '<br>Listening stopped.';
    });
} else {
    console.error('Speech recognition not supported in this browser.');
}
