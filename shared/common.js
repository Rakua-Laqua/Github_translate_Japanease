/* global chrome */
(() => {
  "use strict";

  const DEFAULT_SYNC_SETTINGS = {
    enabled: true,
    loggingEnabled: true,
    translateAttributes: {
      ariaLabel: true,
      title: true,
      placeholder: true
    },
    excludeSelectors: "pre, code, .markdown-body",
    logMaxEntries: 2000,
    logMinLen: 2,
    logMaxLen: 80,
    userDictionary: {}
  };

  function deepMerge(base, override) {
    if (override == null) return structuredClone(base);
    if (typeof base !== "object" || base === null) return override;
    if (Array.isArray(base)) return Array.isArray(override) ? override : structuredClone(base);

    const out = { ...base };
    for (const [k, v] of Object.entries(override)) {
      if (v && typeof v === "object" && !Array.isArray(v) && base[k] && typeof base[k] === "object") {
        out[k] = deepMerge(base[k], v);
      } else {
        out[k] = v;
      }
    }
    return out;
  }

  function normalizeText(text) {
    if (typeof text !== "string") return "";
    return text.trim().replace(/\s+/g, " ");
  }

  function sanitizeUrl(url) {
    try {
      const u = new URL(url);
      return `${u.origin}${u.pathname}`;
    } catch {
      return "";
    }
  }

  function looksLikeUiText(text, minLen, maxLen) {
    if (!text) return false;
    if (text.includes("\n")) return false;
    if (text.length < minLen || text.length > maxLen) return false;

    if (!/[A-Za-z]/.test(text)) return false;

    if (/https?:\/\//i.test(text)) return false;
    if (/\bwww\./i.test(text)) return false;
    if (/\b[a-f0-9]{7,40}\b/i.test(text)) return false;

    if (/[{}<>;$=]/.test(text)) return false;

    return true;
  }

  async function getSyncSettings() {
    const raw = await chrome.storage.sync.get(DEFAULT_SYNC_SETTINGS);
    return deepMerge(DEFAULT_SYNC_SETTINGS, raw);
  }

  async function setSyncSettings(patch) {
    const current = await getSyncSettings();
    const next = deepMerge(current, patch);
    await chrome.storage.sync.set(next);
    return next;
  }

  async function loadBundledDictionary() {
    const url = chrome.runtime.getURL("data/dictionary.json");
    const resp = await fetch(url, { cache: "no-store" });
    if (!resp.ok) throw new Error(`dictionary load failed: ${resp.status}`);
    const json = await resp.json();
    return json && typeof json === "object" ? json : {};
  }

  async function getUnknownLogLocal() {
    const { unknownLog = [], unknownLogIndex = {} } = await chrome.storage.local.get([
      "unknownLog",
      "unknownLogIndex"
    ]);
    return {
      unknownLog: Array.isArray(unknownLog) ? unknownLog : [],
      unknownLogIndex: unknownLogIndex && typeof unknownLogIndex === "object" ? unknownLogIndex : {}
    };
  }

  async function clearUnknownLogLocal() {
    await chrome.storage.local.set({ unknownLog: [], unknownLogIndex: {} });
  }

  function toCsv(rows) {
    const header = ["text", "type", "url", "firstSeenAt", "lastSeenAt", "count", "hint"];
    const escape = (v) => {
      const s = String(v ?? "");
      const needs = /[\",\n\r]/.test(s);
      const q = s.replace(/\"/g, '""');
      return needs ? `"${q}"` : q;
    };

    const lines = [header.join(",")];
    for (const r of rows) {
      lines.push(
        header
          .map((k) => escape(r[k]))
          .join(",")
      );
    }
    return lines.join("\n");
  }

  // expose
  self.GHJP = {
    DEFAULT_SYNC_SETTINGS,
    deepMerge,
    normalizeText,
    sanitizeUrl,
    looksLikeUiText,
    getSyncSettings,
    setSyncSettings,
    loadBundledDictionary,
    getUnknownLogLocal,
    clearUnknownLogLocal,
    toCsv
  };
})();
