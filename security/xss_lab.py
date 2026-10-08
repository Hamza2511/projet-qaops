"""Démonstrateur XSS volontairement vulnérable, accessible uniquement en boucle locale."""
import argparse
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path not in ('/', '/vulnerable', '/fixed'):
            self.send_error(404)
            return
        query = parse_qs(parsed.query).get('q', ['Sara Bennani'])[0]
        fixed = parsed.path == '/fixed'
        value = html.escape(query, quote=True) if fixed else query
        label = 'Corrigé : encodage HTML' if fixed else 'Vulnérable : réflexion HTML brute'
        body = f'''<!doctype html><html lang="fr"><meta charset="utf-8">
        <title>QAOps | Laboratoire XSS local</title>
        <style>body{{font:18px system-ui;max-width:850px;margin:50px auto;padding:25px;background:#f3f7fa;color:#183244}}main{{padding:30px;background:white;border-top:6px solid #008b91}}code{{overflow-wrap:anywhere}}.notice{{background:#fff1c7;padding:12px}}input{{padding:10px;width:70%}}button{{padding:10px}}</style>
        <main><h1>Laboratoire XSS local</h1><p class="notice">Démonstrateur pédagogique isolé. Ne pas déployer sur Internet.</p>
        <h2>{label}</h2><form><label>Nom de l’étudiant : <input name="q" value=""></label><button>Afficher</button></form>
        <p id="result">Étudiant : {value}</p><p id="execution">Le JavaScript injecté n’a pas été exécuté.</p>
        <p><a href="/vulnerable?q=Sara">Version vulnérable</a> · <a href="/fixed?q=Sara">Version corrigée</a></p>
        <p>Correctif : html.escape(query, quote=True), puis CSP restrictive en défense complémentaire.</p></main></html>'''.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        if fixed:
            self.send_header('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=18094)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'QAOps XSS lab: http://127.0.0.1:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
