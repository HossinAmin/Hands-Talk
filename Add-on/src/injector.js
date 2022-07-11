const host = document.createElement('aside')
const shadow = host.attachShadow({mode:'closed'})
const script = document.createElement('script')
script.src = chrome.runtime.getURL('script.js')
shadow.append(script)
document.body.append(host)

// Content script which injects the script:
chrome.extension.onMessage.addListener(function(message) {
  if (message.from === 'meet-gp') {
    postMessage({extensionMessage: message}, '*');
  }
});
// Thanks to Rob Wu (github.com/Rob--W) for fixing this
