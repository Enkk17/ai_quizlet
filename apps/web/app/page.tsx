"use client";

import { ChangeEvent, useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";
type Question = { id: string; question_text: string; options: Record<string, string>; topic?: string; source_type: string };
type Exam = { id: string; questions: Question[] };
type Document = { id: string; filename: string; status: string; total_pages: number };
type Section = "dashboard" | "documents" | "questions" | "analytics" | "reviews";
type Overview = { questions_answered: number; correct_answers: number; accuracy: number; due_reviews: number; topics: { topic: string; accuracy: number; attempts: number }[] };

async function get<T>(path: string): Promise<T> {
  const response = await fetch(`${API}${path}`);
  if (!response.ok) throw new Error((await response.json()).detail ?? "Errore API");
  return response.json();
}

export default function Home() {
  const [section, setSection] = useState<Section>("dashboard");
  const [overview, setOverview] = useState<Overview>({ questions_answered: 0, correct_answers: 0, accuracy: 0, due_reviews: 0, topics: [] });
  const [documents, setDocuments] = useState<Document[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [reviews, setReviews] = useState<{ id: string; topic: string; due_date: string; interval_days: number }[]>([]);
  const [daily, setDaily] = useState<{ day: string; questions: number; accuracy: number }[]>([]);
  const [exam, setExam] = useState<Exam | null>(null);
  const [index, setIndex] = useState(0);
  const [message, setMessage] = useState("");

  const refresh = async () => {
    try {
      const [stats, docs, qs, due, history] = await Promise.all([
        get<typeof overview>("/analytics/overview"), get<Document[]>("/documents"),
        get<Question[]>("/questions"), get<typeof reviews>("/reviews/today"),
        get<typeof daily>("/analytics/daily?days=14"),
      ]);
      setOverview(stats); setDocuments(docs); setQuestions(qs); setReviews(due); setDaily(history);
    } catch (error) { setMessage(error instanceof Error ? error.message : "Errore di caricamento"); }
  };
  useEffect(() => { refresh(); }, []);

  const upload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]; if (!file) return;
    const body = new FormData(); body.append("file", file);
    const response = await fetch(`${API}/documents/upload`, { method: "POST", body });
    setMessage(response.ok ? "Documento importato." : (await response.json()).detail ?? "Errore di importazione");
    refresh();
  };
  const startExam = async () => {
    const response = await fetch(`${API}/exams`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ title: "Sessione rapida", question_count: 5 }) });
    if (response.ok) { setExam(await response.json()); setIndex(0); setMessage(""); } else setMessage((await response.json()).detail);
  };
  const answer = async (option: string) => {
    if (!exam) return;
    await fetch(`${API}/exams/${exam.id}/answer`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question_id: exam.questions[index].id, selected_option: option }) });
    if (index + 1 < exam.questions.length) setIndex(index + 1);
    else { const result = await fetch(`${API}/exams/${exam.id}/finish`, { method: "POST" }); setMessage(`Sessione completata: ${(await result.json()).accuracy}%`); setExam(null); refresh(); }
  };
  const completeReview = async (id: string) => { await fetch(`${API}/reviews/${id}/complete`, { method: "POST" }); refresh(); };
  const current = exam?.questions[index];
  return <main>
    <aside><div className="brand">EXAM<span>AI</span></div><nav>
      {([["dashboard", "Dashboard"], ["documents", "Documenti"], ["questions", "Domande"], ["analytics", "Progressi"], ["reviews", "Ripasso"]] as [Section, string][]).map(([id, label]) => <button className={section === id ? "navActive" : ""} onClick={() => setSection(id)} key={id}>{label}</button>)}
    </nav><small>Local-first · Qwen3 + Ollama</small></aside>
    <section className="content"><header><div><p className="eyebrow">{section.toUpperCase()}</p><h1>{section === "dashboard" ? "Buongiorno, studente." : sectionTitle(section)}</h1><p className="muted">Costruisci una preparazione solida, una risposta alla volta.</p></div><label className="upload">+ Importa documento<input type="file" accept=".pdf,.md,.markdown" onChange={upload} /></label></header>
      {message && <div className="notice">{message}</div>}
      {exam ? <article className="quiz card"><p className="eyebrow">DOMANDA {index + 1} DI {exam.questions.length} · {current?.source_type}</p><h2>{current?.question_text}</h2><div className="options">{Object.entries(current?.options ?? {}).map(([key, text]) => <button key={key} onClick={() => answer(key)}><strong>{key}</strong>{text}</button>)}</div></article> : <SectionView section={section} overview={overview} documents={documents} questions={questions} reviews={reviews} daily={daily} onStart={startExam} onCompleteReview={completeReview} />}
    </section>
  </main>;
}

function SectionView({ section, overview, documents, questions, reviews, daily, onStart, onCompleteReview }: { section: Section; overview: Overview; documents: Document[]; questions: Question[]; reviews: { id: string; topic: string; due_date: string; interval_days: number }[]; daily: { day: string; questions: number; accuracy: number }[]; onStart: () => void; onCompleteReview: (id: string) => void }) {
  if (section === "documents") return <div className="grid"><article className="card wide"><div className="cardHead"><h2>Documenti caricati</h2><span className="muted">{documents.length} totali</span></div>{documents.length ? documents.map(d => <div className="row" key={d.id}><span>{d.filename}<small>{d.total_pages ? ` · ${d.total_pages} pagine` : ""}</small></span><b>{d.status}</b></div>) : <p className="empty">Nessun documento importato.</p>}</article></div>;
  if (section === "questions") return <div className="grid"><article className="card wide"><div className="cardHead"><h2>Archivio domande</h2><span className="muted">{questions.length} domande</span></div>{questions.map(q => <div className="questionRow" key={q.id}><b>{q.source_type}</b><span>{q.question_text}</span><small>{q.topic}</small></div>)}</article></div>;
  if (section === "reviews") return <div className="grid"><article className="card wide"><h2>Ripassi in scadenza</h2>{reviews.length ? reviews.map(r => <div className="row" key={r.id}><span>{r.topic}<small> · {r.due_date}</small></span><button onClick={() => onCompleteReview(r.id)}>Completa</button></div>) : <p className="empty">Nessun ripasso oggi.</p>}</article></div>;
  if (section === "analytics") return <div className="grid"><article className="card"><h2>Andamento recente</h2>{daily.map(d => <div className="row" key={d.day}><span>{d.day}</span><b>{d.accuracy}% · {d.questions}</b></div>)}</article><article className="card"><h2>Argomenti</h2>{overview.topics.map(t => <div className="row" key={t.topic}><span>{t.topic}</span><b>{t.accuracy}%</b></div>)}</article></div>;
  return <><div className="metrics"><Metric label="Accuratezza" value={`${overview.accuracy}%`} /><Metric label="Domande svolte" value={overview.questions_answered} /><Metric label="Risposte corrette" value={overview.correct_answers} /><Metric label="Ripassi oggi" value={overview.due_reviews} /></div><div className="grid"><article className="card"><div className="cardHead"><h2>Inizia una simulazione</h2><button onClick={onStart}>Avvia quiz →</button></div><p className="muted">Le domande vengono corrette in modo deterministico e alimentano i tuoi progressi.</p></article><article className="card"><div className="cardHead"><h2>Documenti recenti</h2><span className="muted">{documents.length} totali</span></div>{documents.slice(0, 5).map(d => <div className="row" key={d.id}><span>{d.filename}</span><b>{d.status}</b></div>)}</article></div></>;
}
function sectionTitle(section: Section) { return ({ documents: "I tuoi documenti", questions: "Archivio domande", analytics: "I tuoi progressi", reviews: "Ripasso intelligente", dashboard: "Dashboard" })[section]; }
function Metric({ label, value }: { label: string; value: string | number }) { return <div className="metric"><span>{label}</span><strong>{value}</strong></div>; }
