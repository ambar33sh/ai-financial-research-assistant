"use client";

import { FormEvent, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

type Citation = { source_name: string; page: number; section?: string; evidence: string };
type Answer = { answer: string; route: string; evidence_strength: string; citations: Citation[] };

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [company, setCompany] = useState("Apple");
  const [year, setYear] = useState("2025");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<Answer | null>(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  async function upload() {
    if (!file) return;
    setLoading(true); setStatus("Indexing document...");
    const data = new FormData();
    data.append("file", file); data.append("company", company); data.append("document_type", "financial_report"); data.append("fiscal_year", year);
    try {
      const response = await fetch(`${API}/documents`, { method: "POST", body: data });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail ?? "Upload failed");
      setStatus(`Indexed ${body.chunks} chunks from ${body.pages} pages.`);
    } catch (error) { setStatus(error instanceof Error ? error.message : "Upload failed"); }
    finally { setLoading(false); }
  }

  async function ask(event: FormEvent) {
    event.preventDefault(); if (!question.trim()) return;
    setLoading(true); setAnswer(null);
    try {
      const response = await fetch(`${API}/ask`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ query: question, company, fiscal_year: Number(year), top_k: 5 }) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail ?? "Question failed");
      setAnswer(body);
    } catch (error) { setStatus(error instanceof Error ? error.message : "Question failed"); }
    finally { setLoading(false); }
  }

  return (
    <div className="shell">
      <header className="topbar"><div className="brand">FinSight <span>AI</span></div><div className="badge">Evidence-grounded financial research</div></header>
      <main className="main">
        <section className="hero"><div className="eyebrow">Financial intelligence workspace</div><h1>Research from the source, not the guess.</h1><p>Upload financial reports, retrieve supporting evidence, and ask questions with page-level citations. Calculations and financial metrics are designed to remain deterministic and auditable.</p></section>
        <div className="grid">
          <section className="card">
            <h2>Document intelligence</h2><p className="muted">PDFs are parsed, chunked with page metadata, embedded and indexed for retrieval.</p>
            <div className="upload"><input className="file" type="file" accept="application/pdf" onChange={e => setFile(e.target.files?.[0] ?? null)} /><div className="row"><input className="input" value={company} onChange={e => setCompany(e.target.value)} placeholder="Company" /><input className="input" value={year} onChange={e => setYear(e.target.value)} placeholder="Fiscal year" /></div><button className="primary" disabled={!file || loading} onClick={upload}>Index PDF</button><p className="muted">{status || "Use annual or quarterly financial reports."}</p></div>
            <div className="stats"><div className="stat"><span className="muted">Retrieval</span><strong>Hybrid</strong></div><div className="stat"><span className="muted">Evidence</span><strong>Cited</strong></div><div className="stat"><span className="muted">Math</span><strong>Deterministic</strong></div></div>
          </section>
          <section className="card">
            <h2>Research assistant</h2><p className="muted">Ask a question about the indexed reports.</p>
            <form onSubmit={ask} className="question"><input className="input" value={question} onChange={e => setQuestion(e.target.value)} placeholder="Why did revenue change? What risks did management mention?" /><button className="primary" disabled={loading || !question.trim()} style={{ marginTop: 10 }}>{loading ? "Working..." : "Ask FinSight"}</button></form>
            {answer && <div className="answer"><div className="badge">Route: {answer.route} · Evidence: {answer.evidence_strength}</div><p>{answer.answer}</p><strong>Sources</strong><div className="sources">{answer.citations.map((c, i) => <div className="source" key={`${c.source_name}-${c.page}-${i}`}><b>{c.source_name}</b> · page {c.page}{c.section ? ` · ${c.section}` : ""}<br />{c.evidence}</div>)}</div></div>}
          </section>
        </div>
      </main>
    </div>
  );
}
