/* global chrome, GHJP */
(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const enabledEl = $("enabled");
  const loggingEl = $("loggingEnabled");
  const statusEl = $("status");

  function setStatus(text) {
    statusEl.textContent = text;
    if (!text) return;
    window.setTimeout(() => {
      if (statusEl.textContent === text) statusEl.textContent = "";
    }, 1200);
  }

  async function refresh() {
    const s = await GHJP.getSyncSettings();
    enabledEl.checked = Boolean(s.enabled);
    loggingEl.checked = Boolean(s.loggingEnabled);
  }

  enabledEl.addEventListener("change", async () => {
    await GHJP.setSyncSettings({ enabled: enabledEl.checked });
    setStatus(enabledEl.checked ? "日本語化: ON" : "日本語化: OFF");
  });

  loggingEl.addEventListener("change", async () => {
    await GHJP.setSyncSettings({ loggingEnabled: loggingEl.checked });
    setStatus(loggingEl.checked ? "ログ収集: ON" : "ログ収集: OFF");
  });

  async function copy(text) {
    await navigator.clipboard.writeText(text);
    setStatus("コピーしました");
  }

  document.getElementById("copyJson").addEventListener("click", async () => {
    const { unknownLog } = await GHJP.getUnknownLogLocal();
    await copy(JSON.stringify(unknownLog, null, 2));
  });

  document.getElementById("openOptions").addEventListener("click", async () => {
    await chrome.runtime.openOptionsPage();
    window.close();
  });

  document.getElementById("copyCsv").addEventListener("click", async () => {
    const { unknownLog } = await GHJP.getUnknownLogLocal();
    await copy(GHJP.toCsv(unknownLog));
  });

  document.getElementById("clearLog").addEventListener("click", async () => {
    await GHJP.clearUnknownLogLocal();
    setStatus("ログを消去しました");
  });

  refresh().catch(() => setStatus("読み込みに失敗しました"));
})();
