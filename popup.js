let isSummary = false;
let summaryText = "";
document.addEventListener("DOMContentLoaded", () => {
  const summarizeButton = document.getElementById("summarize");
  const summaryContainer = document.getElementById("summary");
  const tagContainer = document.getElementById("tags");
  const numSentencesInput = document.getElementById("num-sentences");
  const sentimentContainer = document.getElementById("sentiment-container");
  const copyCitationButton = document.getElementById("copy-citation");
  const copySummaryButton = document.getElementById("copy-summary");
  const resultsContainer = document.getElementById("results");
  const numSentences = document.getElementById('num-sentences');
  const targetLang = document.getElementById("language-selection");

  copyCitationButton.classList.add("hidden");
  copySummaryButton.classList.add("hidden");

  numSentences.addEventListener('input', function () {
    if (parseInt(this.value) > 10) {
      this.value = 10;
    }
  });
  summarizeButton.addEventListener("click", async () => {
    const numSentences = numSentencesInput.value;
    const target_lang = targetLang.value;
    const activeTab = await getActiveTab();
    summaryContainer.innerText = "";
    const loadingIcon = document.getElementById("loading-icon");
    loadingIcon.style.display = "inline-block";
    const result = await chrome.scripting.executeScript({
      target: { tabId: activeTab.id },
      func: summarize,
      args: [numSentences, target_lang],
    });
    loadingIcon.style.display = "none";
    resultsContainer.classList.remove("hidden");
    if (result[0].result) {
      summaryText = result[0].result["summary"] || "Summary not available";
      summaryContainer.innerText = summaryText;
      isSummary = true;

      // Show the "Copy Citation" and "Copy Summary" buttons
      copyCitationButton.classList.remove("hidden");
      copySummaryButton.classList.remove("hidden");

      tagContainer.innerHTML = "";
      const tags = result[0].result["tags"] || [];
      if (tags.length == 0) {
        tagContainer.innerHTML = "Tags not available";
      }
      tags.forEach(tag => {
        const chip = document.createElement("span");
        chip.className = "chip";
        chip.innerText = tag;
        tagContainer.appendChild(chip);
      });
      const sentiment =result[0].result["sentiment"];
      sentimentContainer.className = ""; 
      switch (sentiment) {
        case 1:
          sentimentContainer.innerText = "\u263A"; 
          sentimentContainer.style.color = "green";
          break;
        case 0:
          sentimentContainer.innerText = "\uD83D\uDE10";; 
          break;
    
        case -1:
          sentimentContainer.innerText = "\u2639"; 
          sentimentContainer.style.color = "Red";
          break;

        default:
          sentimentContainer.innerText = "Sentiment not available";
          sentimentContainer.style.color = ""; 
          break;
      }
      copyCitationButton.addEventListener("click", () => {
        const citation = `Citation: ${activeTab.title}. Retrieved from ${activeTab.url}`;
        navigator.clipboard.writeText(citation).then(() => {
          const originalButton = copyCitationButton.innerText;
          copyCitationButton.innerText = "Copied!";
          setTimeout(() => {
            copyCitationButton.innerText = originalButton;
          }, 2000);
        }, () => {
          alert("Failed to copy citation!");
        });
      });    
    }
      else {
        summaryContainer.innerText = "Summary not available";
        tagContainer.innerText = "Tags not available";
        sentimentContainer.innerText = "Sentiment not available";
        copyCitationButton.classList.add("hidden");
        copySummaryButton.classList.add("hidden");
      }
    });
  
    copySummaryButton.addEventListener("click", () => {
      if (isSummary) {
        navigator.clipboard.writeText(summaryText).then(() => {
          const originalButton = copySummaryButton.innerText;
          copySummaryButton.innerText = "Copied!";
          setTimeout(() => {
            copySummaryButton.innerText = originalButton;
          }, 2000);
        }, () => {
          alert("Failed to copy summary.");
        });
      } else {
        alert("No summary available to copy.");
      }
    });
  });
  
  async function getActiveTab() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab;
  }
  
  async function summarize(numSentences, targetLang) {
    const message = window.location.href;
    const data = { message: message, numSentences: numSentences, targetLang: targetLang };
    try {
      const response = await fetch("http://localhost:8000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Accept-Charset": "utf-8"
        },
        body: JSON.stringify(data),
      });
  
      const result = await response.json();
      return result;
    } catch (error) {
      console.error(error);
    }
  }
  
