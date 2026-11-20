export const dynamic = 'force-dynamic';

const API = process.env.API_INTERNAL_URL || 'http://api:8000';
const ORG = process.env.DASHBOARD_ORG_ID || 'demo';

// Development only: the API honours these headers only when APP_ENV=development and DEV_AUTH_ENABLED=true.
// Server-side env, never exposed to the browser. Production uses OIDC (backlog item).
function authHeaders(): Record<string, string> {
  if (process.env.DASHBOARD_DEV_AUTH === 'true') {
    return { 'X-Dev-User': 'dashboard-dev', 'X-Dev-Org': ORG, 'X-Dev-Roles': 'organization_owner' };
  }
  return {};
}

type Result<T> = { ok: true; data: T } | { ok: false; status: number };

async function api<T>(path: string): Promise<Result<T>> {
  try {
    const res = await fetch(`${API}/api/v1${path}`, { cache: 'no-store', headers: authHeaders() });
    if (!res.ok) return { ok: false, status: res.status };
    return { ok: true, data: (await res.json()) as T };
  } catch {
    return { ok: false, status: 0 };
  }
}

function explain(status: number): string {
  if (status === 0) return 'API unreachable. Check that the api container is running (docker compose logs api).';
  if (status === 401 || status === 403) return 'API rejected the dashboard identity. For local dev set DEV_AUTH_ENABLED=true (API) and DASHBOARD_DEV_AUTH=true (web).';
  return `API returned HTTP ${status}.`;
}

const DEPARTMENTS = ['Marketing Intelligence', 'Strategy & Brand', 'SEO & SEM', 'Content & Creative', 'Social & Influencer',
  'Demand Generation', 'CRM & Lifecycle', 'E-commerce & Conversion', 'Analytics & BI', 'Marketing Operations'];

export default async function Home() {
  const [a, t, p] = await Promise.all([
    api<any>('/agents'),
    api<any[]>(`/tasks?organization_id=${encodeURIComponent(ORG)}`),
    api<any[]>(`/approvals?organization_id=${encodeURIComponent(ORG)}&status=pending`),
  ]);
  const agents = a.ok ? (Array.isArray(a.data) ? a.data.length : a.data?.agents?.length ?? 0) : 0;
  const tasks = t.ok ? t.data : [];
  const approvals = p.ok ? p.data : [];
  const problems = [a, t, p].filter((r) => !r.ok).map((r) => explain((r as { status: number }).status));

  return (
    <main>
      <header>
        <div><small>HYBRID AI OPERATIONS</small><h1>Marketing Control Center</h1><p>Organization: {ORG} · Multi-brand</p></div>
        <span className="pill">MVP · Development</span>
      </header>
      {problems.length > 0 && (
        <section className="panel"><h2>Connection problem</h2>{Array.from(new Set(problems)).map((m) => <p className="muted" key={m}>{m}</p>)}</section>
      )}
      <section className="cards">
        <article><small>LOGICAL AGENTS</small><strong>{agents || '—'}</strong><p>Registered roles</p></article>
        <article><small>TASKS</small><strong>{t.ok ? tasks.length : '—'}</strong><p>Tracked tasks</p></article>
        <article><small>PENDING APPROVALS</small><strong>{p.ok ? approvals.length : '—'}</strong><p>Human decision required</p></article>
      </section>
      <section className="panel">
        <h2>Department directory</h2>
        <p>10 departments · 1 Director · 10 Department Heads · 45 Specialists</p>
        <div className="grid">{DEPARTMENTS.map((x, i) => <div className="dept" key={x}><b>{String(i + 1).padStart(2, '0')}</b><span>{x}</span><small>Registry enabled</small></div>)}</div>
      </section>
      <section className="panel">
        <h2>Recent tasks</h2>
        {tasks.length === 0
          ? <p className="muted">No tasks yet. Create tasks through the API at <code>/docs</code>.</p>
          : tasks.slice(0, 8).map((x: any) => <div className="task" key={x.id}><b>{x.title}</b><span>{x.status}</span></div>)}
      </section>
      <footer>Approval-gated execution · External actions disabled by default</footer>
    </main>
  );
}
