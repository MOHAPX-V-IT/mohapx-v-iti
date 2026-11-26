import * as React from "react";
import { createRoot } from "react-dom/client";
import { WarpCarousel, type WarpCard } from "./ui/warp-carousel";

type Language = "ru" | "en";
type Role = {
  html: string;
  mark: string;
  company: Record<Language, string>;
  title: Record<Language, string>;
  date: Record<Language, string>;
};

const section = document.getElementById("path");
const originals = section ? Array.from(section.querySelectorAll<HTMLElement>(":scope > article.resume-role")) : [];

function languageText(element: Element | null, language: Language): string {
  if (!element) return "";
  const localized = element.querySelector(`.${language}`);
  return (localized?.textContent || element.textContent || "").replace(/\s+/g, " ").trim();
}

const roles: Role[] = originals.map((original) => {
  const meta = original.querySelector(".resume-role-meta");
  const date = meta?.querySelector(".resume-date") || null;
  const company = meta?.querySelector("h3") || null;
  const title = meta?.querySelector("p:not(.resume-date)") || null;
  const copy = original.cloneNode(true) as HTMLElement;
  copy.removeAttribute("id");
  copy.querySelectorAll("[id]").forEach((element) => element.removeAttribute("id"));
  return {
    html: copy.innerHTML,
    mark: original.dataset.mark || "",
    company: { ru: languageText(company, "ru"), en: languageText(company, "en") },
    title: { ru: languageText(title, "ru"), en: languageText(title, "en") },
    date: { ru: languageText(date, "ru"), en: languageText(date, "en") },
  };
});

const palettes = [
  ["#213b36", "#0d211e", "#153027", "#668257"],
  ["#57311f", "#25160f", "#492817", "#b9753a"],
  ["#203e4b", "#14272e", "#244957", "#5d93a0"],
  ["#3b4224", "#1c2213", "#414b29", "#8d9b48"],
  ["#343d58", "#161d30", "#273c50", "#60829f"],
  ["#4d3d23", "#262012", "#59452a", "#ac965c"],
  ["#254846", "#142c30", "#30574f", "#75a09b"],
  ["#47362c", "#211b18", "#563b2b", "#b98663"],
  ["#534c20", "#25220f", "#4e471f", "#b3a249"],
];

function readAppearance() {
  const style = getComputedStyle(document.body);
  return {
    language: document.documentElement.lang === "en" ? "en" as Language : "ru" as Language,
    background: style.getPropertyValue("--bg").trim() || "#111210",
  };
}

class ExperienceBoundary extends React.Component<React.PropsWithChildren, { failed: boolean }> {
  state = { failed: false };
  static getDerivedStateFromError() { return { failed: true }; }
  componentDidCatch(error: Error) {
    originals.forEach((role) => { role.hidden = false; });
    section?.classList.remove("experience-enhanced");
    console.warn("Experience carousel: showing the readable list instead.", error.message);
  }
  render() { return this.state.failed ? null : this.props.children; }
}

function Experience() {
  const [appearance, setAppearance] = React.useState(readAppearance);
  const [index, setIndex] = React.useState(0);
  const [ready, setReady] = React.useState(false);
  const [listMode, setListMode] = React.useState(false);
  const language = appearance.language;
  const current = roles[index];
  const readyCallback = React.useCallback(() => setReady(true), []);
  const choose = React.useCallback((next: number) => setIndex((next + roles.length) % roles.length), []);

  React.useEffect(() => {
    const observer = new MutationObserver(() => setAppearance(readAppearance()));
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ["lang", "data-theme"] });
    return () => observer.disconnect();
  }, []);

  React.useEffect(() => {
    if (!ready) return;
    originals.forEach((role) => { role.hidden = !listMode; });
    section?.classList.add("experience-enhanced");
    return () => {
      originals.forEach((role) => { role.hidden = false; });
      section?.classList.remove("experience-enhanced");
    };
  }, [ready, listMode]);

  const cards = React.useMemo<WarpCard[]>(() => roles.map((role, item) => ({
    title: `${role.company[language]}\n${role.title[language]}`,
    value: role.mark || role.company[language].slice(0, 2),
    footer: role.date[language],
    detail: "ring",
    mesh: palettes[item % palettes.length],
    numeral: ["#fff3dc", "#d4c7ad"],
    accent: "#f1b66d",
    glow: "#95613d",
  })), [language]);

  return <div className="experience-browser" data-ready={ready ? "true" : "false"}>
    <div className="experience-toolbar">
      <p className="experience-intro">{language === "ru" ? "Команды, задачи и мой вклад." : "Teams, challenges and my contribution."}</p>
      <button type="button" className="experience-view-toggle" aria-pressed={listMode} onClick={() => setListMode((value) => !value)}>
        {language === "ru" ? (listMode ? "Смотреть карточки" : "Показать списком") : (listMode ? "Show cards" : "Show as a list")}
      </button>
    </div>
    <div className="experience-presentation" hidden={listMode}>
      <div className="experience-stage-column">
        <WarpCarousel cards={cards} index={index} onIndexChange={choose} autoplay={false} step={1}
          background={appearance.background} font='"Manrope", system-ui, sans-serif' warp={0.8}
          onReady={readyCallback} ariaLabel={language === "ru" ? "Места работы: используйте стрелки влево и вправо или перетаскивайте карточки" : "Work experience: use the left and right arrow keys or drag the cards"}
          className="experience-warp-stage" style={{ minHeight: 300, aspectRatio: "6 / 5" }} />
        <div className="experience-controls" aria-label={language === "ru" ? "Навигация по опыту" : "Experience navigation"}>
          <button type="button" onClick={() => choose(index - 1)} aria-label={language === "ru" ? "Предыдущее место работы" : "Previous role"}>{language === "ru" ? "Назад" : "Previous"}</button>
          <span className="experience-position" aria-hidden="true">{String(index + 1).padStart(2, "0")} <span>/ {String(roles.length).padStart(2, "0")}</span></span>
          <button type="button" onClick={() => choose(index + 1)} aria-label={language === "ru" ? "Следующее место работы" : "Next role"}>{language === "ru" ? "Далее" : "Next"}</button>
        </div>
      </div>
      <div className="experience-reading-column">
        <article className="experience-current" id="experience-current" aria-label={current.company[language]}
          // Only existing, repository-owned resume markup is cloned into this island.
          dangerouslySetInnerHTML={{ __html: current.html }} />
        <p className="experience-selection" role="status" aria-live="polite" aria-atomic="true">
          {language === "ru" ? "Выбрано: " : "Selected: "}{current.company[language]}
        </p>
      </div>
    </div>
    <div className="experience-employers" hidden={listMode} aria-label={language === "ru" ? "Выбрать место работы" : "Choose a role"}>
      {roles.map((role, item) => <button type="button" key={item} aria-current={item === index ? "true" : undefined}
        aria-controls="experience-current" onClick={() => choose(item)}>
        {role.company[language]}
      </button>)}
    </div>
  </div>;
}

if (section && originals.length) {
  const root = document.createElement("div");
  root.id = "experience-warp";
  section.querySelector(":scope > h2")?.after(root);
  createRoot(root).render(<ExperienceBoundary><Experience /></ExperienceBoundary>);
}
