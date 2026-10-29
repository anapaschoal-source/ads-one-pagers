// Senha nas páginas protegidas do hub (Vercel Routing Middleware, roda antes dos arquivos estáticos).
// Cada pasta protegida tem sua variável de ambiente com a senha (não fica no repositório).
// Quem acerta a senha recebe um cookie válido por 30 dias, só para aquela pasta.
const PROTEGIDAS = {
  'jota-ud03yuez': 'SENHA_JOTA',
};

export const config = {
  matcher: ['/jota-ud03yuez', '/jota-ud03yuez/:path*'],
};

async function hash(t) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t));
  return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, '0')).join('');
}

function pagina(erro) {
  const html = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Goomer Ads</title><meta name="robots" content="noindex">
<style>
*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0A0044;color:#fff;font-family:Manrope,system-ui,-apple-system,sans-serif;padding:16px}
form{width:min(380px,100%);display:grid;gap:14px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:28px}
h1{margin:0;font-size:22px}p{margin:0;color:rgba(255,255,255,.7);font-size:14px}
input{font:600 16px inherit;padding:12px 14px;border-radius:12px;border:1px solid rgba(255,255,255,.3);background:#06002B;color:#fff}
button{font:800 15px inherit;padding:12px;border:0;border-radius:999px;background:#BDE249;color:#0A0044;cursor:pointer}
.e{color:#FF8A8A;font-weight:700}
</style></head><body><form method="post"><h1>Goomer Ads</h1><p>Este material é protegido. Digite a senha para continuar.</p>
${erro ? '<p class="e">Senha incorreta. Tente de novo.</p>' : ''}
<label for="senha" style="font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase">Senha</label>
<input id="senha" name="senha" type="password" autocomplete="current-password" required autofocus>
<button type="submit">Entrar</button></form></body></html>`;
  return new Response(html, { status: 200, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } });
}

export default async function middleware(req) {
  const url = new URL(req.url);
  const pasta = url.pathname.split('/')[1];
  const env = PROTEGIDAS[pasta];
  if (!env) return;
  const senha = process.env[env];
  if (!senha) return new Response('Material indisponível no momento.', { status: 503 });
  const token = await hash(senha + '|goomer-ads|' + pasta);
  const nome = 'ga_' + pasta.replace(/[^a-z0-9]/gi, '');
  const cookies = (req.headers.get('cookie') || '').split(/;\s*/);
  if (cookies.includes(nome + '=' + token)) return;
  if (req.method === 'POST') {
    const f = await req.formData().catch(() => null);
    if (f && f.get('senha') === senha) {
      return new Response(null, {
        status: 303,
        headers: {
          location: url.pathname + url.search,
          'set-cookie': `${nome}=${token}; Path=/${pasta}; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax`,
          'cache-control': 'no-store',
        },
      });
    }
    return pagina(true);
  }
  return pagina(false);
}
