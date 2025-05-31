function changeSpeed(speed) {
    let video = document.querySelector("iframe");
    video.contentWindow.postMessage(JSON.stringify({
        event: "command",
        func: "setPlaybackRate",
        args: [speed]
    }), "*");
}

// Save search history
function saveSearch(query) {
    let searches = JSON.parse(localStorage.getItem("searchHistory")) || [];
    if (!searches.includes(query)) {
        searches.push(query);
        localStorage.setItem("searchHistory", JSON.stringify(searches));
    }
}

// Load search history
window.onload = function() {
    let searches = JSON.parse(localStorage.getItem("searchHistory")) || [];
    let historyList = document.getElementById("searchHistory");
    searches.forEach(search => {
        let item = document.createElement("li");
        item.textContent = search;
        historyList.appendChild(item);
    });
}
