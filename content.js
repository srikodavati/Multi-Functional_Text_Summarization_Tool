chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
    if (request.action === "summarizeArticle") {
      const articleText = extractArticleText();
      const summary = SimpleSummarizer.summarize(articleText);
      alert(summary);
    }
  });
  
  function extractArticleText() {
    // You can improve this function to better extract article text from various websites.
    const articleElement = document.querySelector("article") || document.body;
    return articleElement.innerText;
  }
  