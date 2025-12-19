/* global GHJP */
(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);

  const els = {
    enabled: $("enabled"),
    loggingEnabled: $("loggingEnabled"),
    ariaLabel: $("ariaLabel"),
    title: $("title"),
    placeholder: $("placeholder"),
    excludeSelectors: $("excludeSelectors"),
    logMaxEntries: $("logMaxEntries"),
    logMinLen: $("logMinLen"),
    logMaxLen: $("logMaxLen"),
    userDictionary: $("userDictionary"),
    save: $("save"),
    reload: $("reload"),
    filterType: $("filterType"),
    filterUrl: $("filterUrl"),
    sort: $("sort"),
    exportJson: $("exportJson"),
    exportCsv: $("exportCsv"),
    copyTemplate: $("copyTemplate"),
    clearLog: $("clearLog"),
    logView: $("logView"),
    status: $("status")
  };

  let lastUnknownLog = [];

  function setStatus(text) {
    els.status.textContent = text;
    if (!text) return;
    window.setTimeout(() => {
      if (els.status.textContent === text) els.status.textContent = "";
    }, 1400);
  }

  function download(filename, content, mime) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  function applyLogView() {
    const type = els.filterType.value;
    const urlPart = els.filterUrl.value.trim();
    const sort = els.sort.value;

    let rows = Array.from(lastUnknownLog);

    if (type) rows = rows.filter((r) => r.type === type);
    if (urlPart) rows = rows.filter((r) => (r.url || "").includes(urlPart));

    if (sort === "freq") {
      rows.sort((a, b) => (b.count || 0) - (a.count || 0));
    } else {
      rows.sort((a, b) => (b.lastSeenAt || 0) - (a.lastSeenAt || 0));
    }

    els.logView.value = JSON.stringify(rows, null, 2);
  }

  async function refreshAll() {
    const s = await GHJP.getSyncSettings();

    els.enabled.checked = Boolean(s.enabled);
    els.loggingEnabled.checked = Boolean(s.loggingEnabled);

    els.ariaLabel.checked = Boolean(s.translateAttributes?.ariaLabel);
    els.title.checked = Boolean(s.translateAttributes?.title);
    els.placeholder.checked = Boolean(s.translateAttributes?.placeholder);

    els.excludeSelectors.value = s.excludeSelectors ?? "";

    els.logMaxEntries.value = String(s.logMaxEntries ?? 2000);
    els.logMinLen.value = String(s.logMinLen ?? 2);
    els.logMaxLen.value = String(s.logMaxLen ?? 80);

    els.userDictionary.value = JSON.stringify(s.userDictionary ?? {}, null, 2);

    const local = await GHJP.getUnknownLogLocal();
    lastUnknownLog = local.unknownLog;
    applyLogView();
  }

  async function saveSettings() {
    let userDict = {};
    try {
      userDict = JSON.parse(els.userDictionary.value || "{}");
      if (userDict == null || typeof userDict !== "object" || Array.isArray(userDict)) {
        throw new Error("userDictionary must be object");
      }
    } catch {
      setStatus("ユーザー辞書(JSON)の形式が不正です");
      return;
    }

    await GHJP.setSyncSettings({
      enabled: els.enabled.checked,
      loggingEnabled: els.loggingEnabled.checked,
      translateAttributes: {
        ariaLabel: els.ariaLabel.checked,
        title: els.title.checked,
        placeholder: els.placeholder.checked
      },
      excludeSelectors: els.excludeSelectors.value,
      logMaxEntries: Number(els.logMaxEntries.value),
      logMinLen: Number(els.logMinLen.value),
      logMaxLen: Number(els.logMaxLen.value),
      userDictionary: userDict
    });

    setStatus("保存しました");
  }

  // bindings
  els.save.addEventListener("click", () => saveSettings().catch(() => setStatus("保存に失敗しました")));
  els.reload.addEventListener("click", () => refreshAll().catch(() => setStatus("再読み込みに失敗しました")));

  for (const key of ["enabled", "loggingEnabled", "ariaLabel", "title", "placeholder"]) {
    els[key].addEventListener("change", () => saveSettings().catch(() => setStatus("保存に失敗しました")));
  }

  els.excludeSelectors.addEventListener("change", () => saveSettings().catch(() => setStatus("保存に失敗しました")));
  for (const key of ["logMaxEntries", "logMinLen", "logMaxLen"]) {
    els[key].addEventListener("change", () => saveSettings().catch(() => setStatus("保存に失敗しました")));
  }

  els.filterType.addEventListener("change", applyLogView);
  els.filterUrl.addEventListener("input", applyLogView);
  els.sort.addEventListener("change", applyLogView);

  els.exportJson.addEventListener("click", async () => {
    const { unknownLog } = await GHJP.getUnknownLogLocal();
    download("ghjp-unknown-log.json", JSON.stringify(unknownLog, null, 2), "application/json");
  });

  els.exportCsv.addEventListener("click", async () => {
    const { unknownLog } = await GHJP.getUnknownLogLocal();
    download("ghjp-unknown-log.csv", GHJP.toCsv(unknownLog), "text/csv");
  });

  els.copyTemplate.addEventListener("click", async () => {
    const { unknownLog } = await GHJP.getUnknownLogLocal();
    const template = {};
    for (const r of unknownLog) {
      if (!r?.text) continue;
      template[r.text] = "";
    }
    await navigator.clipboard.writeText(JSON.stringify(template, null, 2));
    setStatus("テンプレをコピーしました");
  });

  els.clearLog.addEventListener("click", async () => {
    await GHJP.clearUnknownLogLocal();
    setStatus("ログを消去しました");
    await refreshAll();
  });

  refreshAll().catch(() => setStatus("読み込みに失敗しました"));
})();
