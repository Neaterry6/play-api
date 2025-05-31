// ✅ Change YouTube Video Speed
function changeSpeed(speed) {
    let video = document.querySelector("iframe");
    if (video && video.contentWindow) {
        video.contentWindow.postMessage(JSON.stringify({
            event: "command",
            func: "setPlaybackRate",
            args: [speed]
        }), "*");
    } else {
        console.error("❌ Video element not found!");
    }
}

// ✅ Save Search History (Prevents Duplicates)
function saveSearch(query) {
    if (!query.trim()) return;  // Prevent empty searches

    let searches = JSON.parse(localStorage.getItem("searchHistory")) || [];
    if (!searches.includes(query)) {
        searches.push(query);
        localStorage.setItem("searchHistory", JSON.stringify(searches));
    }
}

// ✅ Load Search History on Page Load
document.addEventListener("DOMContentLoaded", function () {
    let searches = JSON.parse(localStorage.getItem("searchHistory")) || [];
    let historyList = document.getElementById("searchHistory");

    if (!historyList) {
        console.error("❌ Search history list element not found!");
        return;
    }

    searches.forEach(search => {
        let item = document.createElement("li");
        item.textContent = search;
        historyList.appendChild(item);
    });
});

// ✅ Clear Search History (Optional Feature)
function clearSearchHistory() {
    localStorage.removeItem("searchHistory");
    location.reload();  // Refresh page to update history list
