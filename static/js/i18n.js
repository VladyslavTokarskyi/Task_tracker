let translations = {};

async function loadLanguage(lang) {
  const res = await fetch(`/static/i18n/${lang}.json`);
  translations = await res.json();
  applyTranslations();
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    let text = translations[key] || key;

    if (el.dataset.i18nVars) {
      const vars = JSON.parse(el.dataset.i18nVars);
      Object.keys(vars).forEach((v) => {
        text = text.replace(`{{${v}}}`, vars[v]);
      });
    }

    el.textContent = text;
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.dataset.i18nPlaceholder;
    el.placeholder = translations[key] || key;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (window.APP_CONTEXT?.lang) {
    loadLanguage(window.APP_CONTEXT.lang);
  }
});
