/* global chrome, GHJP */
(() => {
  "use strict";

  const TRANSLATED_TEXT_NODES_LIMIT = 5000;

  let settings = null;
  let bundledDictionary = null;
  let dictionaryNorm = new Map();

  let excludeMatcher = () => false;

  const translatedTextOriginal = new WeakMap();
  const translatedTextNodes = new Set();

  let observer = null;
  let pendingRoots = new Set();
  let flushTimer = null;

  // unknown log cache (local)
  let unknownLog = [];
  let unknownIndex = new Set();
  let unknownKeyToEntry = new Map();
  let unknownSaveTimer = null;

  function compileExcludeMatcher(selectors) {
    const s = (selectors ?? "").trim();
    if (!s) return () => false;
    try {
      return (el) => {
        if (!el || el.nodeType !== Node.ELEMENT_NODE) return false;
        return Boolean(el.closest(s));
      };
    } catch {
      return () => false;
    }
  }

  function buildNormalizedDictionaryMap(dict) {
    const m = new Map();
    for (const [k, v] of Object.entries(dict || {})) {
      const nk = GHJP.normalizeText(k);
      if (!nk) continue;
      if (typeof v !== "string") continue;
      m.set(nk, v);
    }
    return m;
  }

  function mergeDictionaries(bundled, user) {
    return {
      ...(bundled || {}),
      ...(user || {})
    };
  }

  function shouldSkipElement(el) {
    if (!el) return true;
    const tag = el.tagName;
    if (!tag) return false;
    const t = tag.toLowerCase();
    if (t === "script" || t === "style" || t === "noscript") return true;
    return false;
  }

  function preserveOuterWhitespace(original, replaced) {
    const prefix = (original.match(/^\s*/)?.[0]) ?? "";
    const suffix = (original.match(/\s*$/)?.[0]) ?? "";
    return `${prefix}${replaced}${suffix}`;
  }

  function translateTextNode(node) {
    if (!settings?.enabled) return;
    if (!node || node.nodeType !== Node.TEXT_NODE) return;

    const parent = node.parentElement;
    if (!parent) return;
    if (shouldSkipElement(parent)) return;

    const parentTag = parent.tagName?.toLowerCase?.() ?? "";
    if (parentTag === "textarea" || parentTag === "input") return;

    if (excludeMatcher(parent)) return;

    const originalText = node.nodeValue;
    if (!originalText) return;

    const normalized = GHJP.normalizeText(originalText);
    if (!normalized) return;

    const translated = dictionaryNorm.get(normalized);
    if (translated == null) {
      maybeCollectUnknown(normalized, "textNode", parent);
      return;
    }

    if (translatedTextOriginal.has(node)) {
      const prevOriginal = translatedTextOriginal.get(node);
      const prevTranslated = prevOriginal ? dictionaryNorm.get(GHJP.normalizeText(prevOriginal)) : null;
      if (prevOriginal && prevTranslated != null) {
        const expected = preserveOuterWhitespace(prevOriginal, prevTranslated);
        if (node.nodeValue === expected) return;
      }
      translatedTextOriginal.delete(node);
      translatedTextNodes.delete(node);
    }

    const nextText = preserveOuterWhitespace(originalText, translated);
    if (nextText === originalText) return;

    translatedTextOriginal.set(node, originalText);
    node.nodeValue = nextText;

    if (translatedTextNodes.size < TRANSLATED_TEXT_NODES_LIMIT) {
      translatedTextNodes.add(node);
    }
  }

  function translateAttribute(el, attr, type) {
    if (!settings?.enabled) return;
    if (!el || el.nodeType !== Node.ELEMENT_NODE) return;
    if (shouldSkipElement(el)) return;
    if (excludeMatcher(el)) return;

    const value = el.getAttribute(attr);
    if (value == null) return;

    const normalized = GHJP.normalizeText(value);
    if (!normalized) return;

    const translated = dictionaryNorm.get(normalized);
    if (translated == null) {
      maybeCollectUnknown(normalized, type, el);
      return;
    }

    const dataKey = `ghjpOrig_${attr.replace(/-/g, "_")}`;
    if (el.dataset[dataKey] != null) {
      const prevOriginal = el.dataset[dataKey];
      const prevTranslated = prevOriginal ? dictionaryNorm.get(GHJP.normalizeText(prevOriginal)) : null;
      if (prevOriginal && prevTranslated != null) {
        const expected = preserveOuterWhitespace(prevOriginal, prevTranslated);
        if (el.getAttribute(attr) === expected) return;
      }
      delete el.dataset[dataKey];
    }

    const nextValue = preserveOuterWhitespace(value, translated);
    if (nextValue === value) return;

    el.dataset[dataKey] = value;
    el.setAttribute(attr, nextValue);
  }

  function translateTree(root) {
    if (!settings?.enabled) return;
    if (!root) return;

    if (root.nodeType === Node.TEXT_NODE) {
      translateTextNode(root);
      return;
    }

    const nodeRoot = root.nodeType === Node.ELEMENT_NODE ? root : root.parentElement;
    if (nodeRoot && excludeMatcher(nodeRoot)) return;

    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => {
        if (!n || n.nodeType !== Node.TEXT_NODE) return NodeFilter.FILTER_REJECT;
        const p = n.parentElement;
        if (!p) return NodeFilter.FILTER_REJECT;
        if (shouldSkipElement(p)) return NodeFilter.FILTER_REJECT;

        const tag = p.tagName?.toLowerCase?.() ?? "";
        if (tag === "textarea" || tag === "input") return NodeFilter.FILTER_REJECT;

        if (excludeMatcher(p)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });

    let n;
    while ((n = walker.nextNode())) {
      translateTextNode(n);
    }

    const rootEl = root.nodeType === Node.ELEMENT_NODE ? root : root.parentElement;

    if (settings.translateAttributes?.ariaLabel) {
      if (rootEl?.hasAttribute?.("aria-label")) translateAttribute(rootEl, "aria-label", "aria-label");
      for (const el of root.querySelectorAll?.("[aria-label]") ?? []) {
        translateAttribute(el, "aria-label", "aria-label");
      }
    }
    if (settings.translateAttributes?.title) {
      if (rootEl?.hasAttribute?.("title")) translateAttribute(rootEl, "title", "title");
      for (const el of root.querySelectorAll?.("[title]") ?? []) {
        translateAttribute(el, "title", "title");
      }
    }
    if (settings.translateAttributes?.placeholder) {
      if (rootEl?.hasAttribute?.("placeholder")) translateAttribute(rootEl, "placeholder", "placeholder");
      for (const el of root.querySelectorAll?.("[placeholder]") ?? []) {
        translateAttribute(el, "placeholder", "placeholder");
      }
    }
  }

  function revertTranslations() {
    for (const node of translatedTextNodes) {
      if (!node?.isConnected) continue;
      const original = translatedTextOriginal.get(node);
      if (original == null) continue;
      node.nodeValue = original;
      translatedTextOriginal.delete(node);
    }
    translatedTextNodes.clear();

    // attributes
    const attrs = ["aria-label", "title", "placeholder"];
    for (const attr of attrs) {
      const dataKey = `ghjpOrig_${attr.replace(/-/g, "_")}`;
      for (const el of document.querySelectorAll(`[${attr}]`)) {
        const original = el.dataset[dataKey];
        if (original != null) {
          el.setAttribute(attr, original);
          delete el.dataset[dataKey];
        }
      }
    }
  }

  function scheduleTranslate(root) {
    if (!settings?.enabled) return;
    if (!root) return;
    pendingRoots.add(root);
    if (flushTimer) return;
    flushTimer = window.setTimeout(() => {
      flushTimer = null;
      const roots = Array.from(pendingRoots);
      pendingRoots = new Set();
      for (const r of roots) translateTree(r);
    }, 120);
  }

  function observeDom() {
    if (observer) observer.disconnect();

    const attributeFilter = [];
    if (settings.translateAttributes?.ariaLabel) attributeFilter.push("aria-label");
    if (settings.translateAttributes?.title) attributeFilter.push("title");
    if (settings.translateAttributes?.placeholder) attributeFilter.push("placeholder");

    observer = new MutationObserver((mutations) => {
      if (!settings?.enabled) return;

      for (const m of mutations) {
        if (m.type === "childList") {
          for (const added of m.addedNodes) {
            if (added.nodeType === Node.ELEMENT_NODE || added.nodeType === Node.TEXT_NODE) {
              scheduleTranslate(added);
            }
          }
        } else if (m.type === "attributes") {
          const el = m.target;
          if (el && el.nodeType === Node.ELEMENT_NODE) {
            scheduleTranslate(el);
          }
        }
      }
    });

    observer.observe(document.documentElement, {
      childList: true,
      subtree: true,
      attributes: attributeFilter.length > 0,
      attributeFilter: attributeFilter.length > 0 ? attributeFilter : undefined
    });
  }

  function hookHistory() {
    const onUrlChange = () => {
      if (!settings?.enabled) return;
      scheduleTranslate(document.body || document.documentElement);
    };

    const wrap = (fnName) => {
      const orig = history[fnName];
      if (typeof orig !== "function") return;
      history[fnName] = function (...args) {
        const r = orig.apply(this, args);
        window.dispatchEvent(new Event("ghjp:urlchange"));
        return r;
      };
    };

    wrap("pushState");
    wrap("replaceState");

    window.addEventListener("popstate", () => window.dispatchEvent(new Event("ghjp:urlchange")));
    window.addEventListener("ghjp:urlchange", onUrlChange);
  }

  function buildHint(el) {
    if (!el || el.nodeType !== Node.ELEMENT_NODE) return "";
    const tag = el.tagName?.toLowerCase?.() ?? "";
    const cls = (el.className && typeof el.className === "string") ? el.className.trim() : "";
    const clsShort = cls ? cls.split(/\s+/).slice(0, 3).join(".") : "";
    return clsShort ? `${tag}.${clsShort}` : tag;
  }

  function maybeCollectUnknown(normalizedText, type, elForHint) {
    if (!settings?.loggingEnabled) return;
    if (!GHJP.looksLikeUiText(normalizedText, settings.logMinLen, settings.logMaxLen)) return;

    const key = `${type}\n${normalizedText}`;
    const now = Date.now();
    const url = GHJP.sanitizeUrl(location.href);

    const existing = unknownKeyToEntry.get(key);
    if (existing) {
      existing.lastSeenAt = now;
      existing.count = (existing.count || 1) + 1;
      scheduleUnknownSave();
      return;
    }

    if (unknownIndex.has(key)) return;

    const entry = {
      text: normalizedText,
      type,
      url,
      firstSeenAt: now,
      lastSeenAt: now,
      count: 1,
      hint: buildHint(elForHint)
    };

    unknownIndex.add(key);
    unknownKeyToEntry.set(key, entry);
    unknownLog.unshift(entry);

    const max = Number(settings.logMaxEntries) || 2000;
    if (unknownLog.length > max) {
      const removed = unknownLog.splice(max);
      for (const r of removed) {
        const rk = `${r.type}\n${r.text}`;
        unknownIndex.delete(rk);
        unknownKeyToEntry.delete(rk);
      }
    }

    scheduleUnknownSave();
  }

  function scheduleUnknownSave() {
    if (unknownSaveTimer) return;
    unknownSaveTimer = window.setTimeout(async () => {
      unknownSaveTimer = null;
      const indexObj = {};
      for (const k of unknownIndex) indexObj[k] = true;
      try {
        await chrome.storage.local.set({ unknownLog, unknownLogIndex: indexObj });
      } catch {
        // storage.local失敗時は安全側でログ収集を止める
        settings.loggingEnabled = false;
      }
    }, 800);
  }

  async function loadUnknownCache() {
    const local = await GHJP.getUnknownLogLocal();
    unknownLog = local.unknownLog;
    unknownIndex = new Set(Object.keys(local.unknownLogIndex || {}));
    unknownKeyToEntry = new Map();
    for (const e of unknownLog) {
      if (!e?.text || !e?.type) continue;
      unknownKeyToEntry.set(`${e.type}\n${e.text}`, e);
    }
  }

  async function reloadDictionaryAndSettings() {
    const nextSettings = await GHJP.getSyncSettings();

    if (!bundledDictionary) {
      bundledDictionary = await GHJP.loadBundledDictionary();
    }

    settings = nextSettings;
    excludeMatcher = compileExcludeMatcher(settings.excludeSelectors);

    const merged = mergeDictionaries(bundledDictionary, settings.userDictionary);
    dictionaryNorm = buildNormalizedDictionaryMap(merged);
  }

  async function start() {
    await reloadDictionaryAndSettings();
    await loadUnknownCache();

    hookHistory();

    if (settings.enabled) {
      observeDom();
      translateTree(document.body || document.documentElement);
    }

    chrome.storage.onChanged.addListener(async (changes, area) => {
      if (area !== "sync") return;

      const enabledBefore = settings?.enabled;
      await reloadDictionaryAndSettings();

      if (enabledBefore && !settings.enabled) {
        if (observer) observer.disconnect();
        revertTranslations();
        return;
      }

      if (!enabledBefore && settings.enabled) {
        observeDom();
      } else if (enabledBefore && settings.enabled) {
        observeDom();
      }

      if (settings.enabled) {
        scheduleTranslate(document.body || document.documentElement);
      }
    });
  }

  start().catch(() => {
    // 辞書ロード失敗などの致命エラー時は翻訳を止める
  });
})();
