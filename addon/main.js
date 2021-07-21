window.onload = () => {
    console.log('window loaded');
    main();
};

function main() {
  const nodesToIgnore = new Set(["PRE"]);
  // sklp pre and under pre element, get Nodes
  const nodes = collectNodes();
  // console.log(nodes)
  for (const node of nodes) {
    // skip if node is not textNode
    if (node.nodeType !== Node.TEXT_NODE) {
      continue;
    }
    // skip text node with blank + newline only element
    if (/^\s+$/.test(node.textContent)) {
      continue;
    }
    processNode(node);
  }
}

function collectNodes() {
  const container = document.querySelector(".content")
  const r = [];
  let n;
  const walker = document.createTreeWalker(container, NodeFilter.SHOW_ALL, {
    acceptNode: function(node) {
      // console.log(node.parentNode.nodeName)
      if (/PRE/.test(node.nodeName)) {
        return NodeFilter.FILTER_REJECT
      }
      return NodeFilter.FILTER_ACCEPT
    }
  }, false);
  while ((n = walker.nextNode())) {
    // console.log(n)
    r.push(n);
  }
  return r;
}

function lookupWord(word) {
    const stem = word2stem[word.toLowerCase()];
    if (!stem) {
      return "";
    }
    const meaning = dic[stem];
    if (!meaning) {
      return "";
    }
    return meaning;
}

function processNode(node) {
  const fragment = document.createDocumentFragment();
  const words = node.textContent.split(/\s+/)
  words.forEach((word) => {
    const span = document.createElement("span");
    span.textContent = word;
    fragment.appendChild(span);
    fragment.appendChild(document.createTextNode(" "));

    const trimmedWord = word.replace(/['",.:;]/g, '');
    const meaning = lookupWord(trimmedWord);
    if (!meaning) {
      return;
    }
    span.className = "word";
    const tooltip = document.createElement("div");
    tooltip.textContent = meaning;
    tooltip.className = "word-translation";
    span.appendChild(tooltip);
  });
  if (fragment.children.length > 0 && fragment.lastChild.textContent === " ") {
    fragment.removeChild(fragment.lastChild);
  }
  // workaround to avoid making h2 > pre and h3 > pre
  if (node.parentNode.nodeName == "H2" || node.parentNode.nodeName == "H3") {
    // wrap by div
    const div = document.createElement("div");
    div.appendChild(fragment);
    node.parentNode.replaceChild(div, node);
  } else {
    node.parentNode.replaceChild(fragment, node);
  }
}
