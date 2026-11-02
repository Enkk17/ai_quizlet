"use client";

import { ChangeEvent, useEffect, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";
type Question = { id: string; question_text: string; options: Record<string, string>; explanation?: string; topic?: string; source_type: string };
type Exam = { id: string; questions: Question[] };

export default function Home() {
  const [overview, setOverview] = useState({ questions_answered: 0, correct_answers: 0, accuracy: 0, due_reviews: 0 });
  const [documents, setDocuments] = useState<{ id: string; filename: string; status: string }[]>([]);
  const [exam, setExam] = useState<Exam | null>(null);
  const [index, setIndex] = useState(0);
  const [message, setMessage] = useState("");

  const refresh = async () => {
    const [stats, docs] = await Promise.all([fetch(`${API}/analytics/overview`), fetch(`${API}/documents`)]);
    setOverview(await stats.json()); setDocuments(await docs.json());
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
  const current = exam?.questions[index];
  return <main>
    <aside><div className="brand">EXAM<span>AI</span></div><nav><a>Dashboard</a><a>Documenti</a><a>Domande</a><a>Simulazioni</a><a>Ripasso</a></nav><small>Local-first · Qwen3 + Ollama</small></aside>
    <section className="content"><header><div><p className="eyebrow">PANORAMICA</p><h1>Buongiorno, studente.</h1><p className="muted">Costruisci una preparazione solida, una risposta alla volta.</p></div><label className="upload">+ Importa documento<input type="file" accept=".pdf,.md,.markdown" onChange={upload} /></label></header>
      {message && <div className="notice">{message}</div>}
      {!exam ? <><div className="metrics"><Metric label="Accuratezza" value={`${overview.accuracy}%`} /><Metric label="Domande svolte" value={overview.questions_answered} /><Metric label="Risposte corrette" value={overview.correct_answers} /><Metric label="Ripassi oggi" value={overview.due_reviews} /></div>
        <div className="grid"><article className="card"><div className="cardHead"><h2>Inizia una simulazione</h2><button onClick={startExam}>Avvia quiz →</button></div><p className="muted">Le domande ufficiali importate vengono corrette in modo deterministico e alimentano i tuoi progressi.</p></article>
        <article className="card"><div className="cardHead"><h2>Documenti recenti</h2><span className="muted">{documents.length} totali</span></div>{documents.length ? documents.slice(0, 5).map(d => <div className="row" key={d.id}><span>{d.filename}</span><b>{d.status}</b></div>) : <p className="empty">Importa un PDF o un Markdown per iniziare.</p>}</article></div>
      </> : <article className="quiz card"><p className="eyebrow">DOMANDA {index + 1} DI {exam.questions.length} · {current?.source_type}</p><h2>{current?.question_text}</h2><div className="options">{Object.entries(current?.options ?? {}).map(([key, text]) => <button key={key} onClick={() => answer(key)}><strong>{key}</strong>{text}</button>)}</div></article>}
    </section>
  </main>;
}
function Metric({ label, value }: { label: string; value: string | number }) { return <div className="metric"><span>{label}</span><strong>{value}</strong></div>; }
