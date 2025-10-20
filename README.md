# Flask Secure Auth API (DevSecOps Example)

Projeto de exemplo para a disciplina de Segurança da Informação.
Inclui:
- API Flask simples com autenticação (registro / login / token JWT)
- Dockerfile + docker-compose para execução local
- GitHub Actions CI com etapas de SAST (Semgrep), SCA (pip-audit), DAST (OWASP ZAP) e testes
- Exemplos de configuração e relatórios

## Estrutura
- app/
  - main.py
  - auth.py
  - models.py
  - requirements.txt
- tests/
  - test_auth.py
- .github/workflows/
  - ci.yml
  - sast.yml
  - sca.yml
  - dast.yml
- Dockerfile
- docker-compose.yml
- semgrep.yml

## Como usar localmente
1. Construir e rodar com docker-compose:
   ```bash
   docker-compose up --build
   ```
2. API estará em http://localhost:5000
3. Endpoints principais:
   - POST /register  { "username", "password" }
   - POST /login     { "username", "password" } -> returns access token
   - GET /protected  (Authorization: Bearer <token>)

## Observações sobre CI/CD
- Semgrep é usado em `sast.yml` com configuração semgrep.yml.
- pip-audit gera relatório de dependências em `sca.yml`.
- OWASP ZAP Ageção (baseline) é usada em `dast.yml` após iniciar a aplicação em containers.

## Autoria 
- Julia Amorim RM99609
- Lana Leite RM551143
- Matheus Cavasini RM97722
