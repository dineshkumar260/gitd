function startDictation() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "hi-IN"; // Hindi demo
        recognition.start();
        recognition.onresult = function(e) {
            document.getElementById('name').value = e.results[0][0].transcript;
            recognition.stop();
        };
        recognition.onerror = function(e) {
            recognition.stop();
        }
    }
}