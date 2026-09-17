const CLASS_ORDER = ["Alegre", "Neutra", "Triste"];
const CLASS_COLOR_VAR = {
  Alegre: "--series-alegre",
  Neutra: "--series-neutra",
  Triste: "--series-triste",
};

const CLASS_ICON = {
  Alegre: "😊",
  Neutra: "😐",
  Triste: "😢",
};

const form = document.getElementById("uploadForm");
const audioInput = document.getElementById("audioInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const dropZone = document.getElementById("dropZone");
const fileNameEl = document.getElementById("fileName");
const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const resultEl = document.getElementById("result");
const winnerNameEl = document.getElementById("winnerName");
const chartEl = document.getElementById("chart");

function showLoading() {
  loadingEl.hidden = false;
  errorEl.hidden = true;
  resultEl.hidden = true;
  analyzeBtn.disabled = true;
}

function hideLoading() {
  loadingEl.hidden = true;
  analyzeBtn.disabled = false;
}

function showError(message) {
  errorEl.textContent = message;
  errorEl.hidden = false;
  resultEl.hidden = true;
}

function renderResult(data) {
  const { predicted_class: predictedClass, probabilities } = data;
  winnerNameEl.textContent = `${CLASS_ICON[predictedClass]} ${predictedClass}`;

  chartEl.innerHTML = "";
  for (const className of CLASS_ORDER) {
    const prob = probabilities[className] ?? 0;
    const pct = Math.round(prob * 1000) / 10;
    const isWinner = className === predictedClass;

    const row = document.createElement("div");
    row.className = "bar-row" + (isWinner ? " is-winner" : "");
    row.title = `${className}: ${pct}%`;

    const label = document.createElement("span");
    label.className = "bar-label";
    label.textContent = className;

    const track = document.createElement("div");
    track.className = "bar-track";
    const fill = document.createElement("div");
    fill.className = "bar-fill";
    fill.style.width = `${pct}%`;
    fill.style.background = `var(${CLASS_COLOR_VAR[className]})`;
    track.appendChild(fill);

    const value = document.createElement("span");
    value.className = "bar-value";
    value.textContent = `${pct}%`;

    row.append(label, track, value);
    chartEl.appendChild(row);
  }

  errorEl.hidden = true;
  resultEl.hidden = false;
}

function updateFileName() {
  const file = audioInput.files[0];
  if (file) {
    fileNameEl.textContent = file.name;
    fileNameEl.hidden = false;
  } else {
    fileNameEl.hidden = true;
  }
}

audioInput.addEventListener("change", updateFileName);

["dragenter", "dragover"].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    event.stopPropagation();
    dropZone.classList.add("is-dragover");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    event.stopPropagation();
    dropZone.classList.remove("is-dragover");
  });
});

dropZone.addEventListener("drop", (event) => {
  const files = event.dataTransfer.files;
  if (files.length > 0) {
    audioInput.files = files;
    updateFileName();
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = audioInput.files[0];
  if (!file) {
    showError("Selecciona un archivo de audio.");
    return;
  }

  showLoading();
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/api/predict", { method: "POST", body: formData });
    const payload = await res.json();
    if (!res.ok) {
      throw new Error(payload.detail || "Error al procesar el audio.");
    }
    renderResult(payload);
  } catch (err) {
    showError(err.message);
  } finally {
    hideLoading();
  }
});
