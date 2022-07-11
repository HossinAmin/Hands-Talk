(function() {
  function sendAction(action) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {action: action, from: 'meet-gp'});
    });
  }
  const btn = document.getElementById("listener-button");
      btn.addEventListener("click", () => {
        const isStarted = btn.innerText === "Start";
        if (isStarted) {
          btn.innerText = "Stop";
          btn.style.backgroundColor = "red";
          sendAction("start");
        } else {
          btn.innerText = "Start";
          btn.style.backgroundColor = "teal";
          sendAction("stop");
        }
      });
})()