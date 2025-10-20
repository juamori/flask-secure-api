# 🛡️ RIPD — Sprint 4  
## Projeto: InvestmentAdvisor Secure API  
**Disciplina:** Cybersecurity  
**Autora:** Julia Amorim  
**Data:** Outubro/2025  

---

## 🎯 1. Objetivo do Relatório  
Este Relatório de Impacto à Proteção de Dados (RIPD) apresenta as medidas de **segurança da informação**, **privacidade** e **conformidade com a LGPD** implementadas na *InvestmentAdvisor Secure API*.  
O foco desta sprint foi garantir práticas seguras de desenvolvimento (SSDLC), auditoria de consentimento e automação de testes e análises de segurança.

---

## 🔐 2. Controles Implementados  

### 2.1. Autenticação e Autorização  
- **JWT (JSON Web Token):** autenticação baseada em token com expiração configurável.  
- **Senhas protegidas com hash (Werkzeug / bcrypt)**.  
- **Rotas protegidas:** endpoints sensíveis exigem token válido (`/protected`).  
- **Erros tratados com mensagens seguras (sem exposição de dados internos).**

### 2.2. Conformidade com LGPD  
- Implementado endpoint `/consent` que registra o **consentimento explícito do usuário**.  
- Os logs são armazenados em arquivo `consent.log` no formato JSON, contendo:
  - `user_id`  
  - `policy_version`  
  - `timestamp`  
  - `ip` (quando aplicável)
- O log é auditável e não sobrescreve registros (append-only).  
- O teste automatizado `test_consent_endpoint_creates_log` comprova o funcionamento do controle.

### 2.3. Testes Automatizados (Pytest)  
- **Cobertura de testes de segurança e LGPD:**
  - `test_register_login_protected`: fluxo completo de registro, login e acesso autenticado.  
  - `test_login_invalid_password`: verificação de erro em credenciais inválidas.  
  - `test_protected_route_no_token`: acesso negado sem token.  
  - `test_consent_endpoint_creates_log`: validação da criação de logs de consentimento.  
- Todos os testes **executados com sucesso (`pytest -v`)**.  
- Banco de dados isolado em memória (`sqlite:///:memory:`) durante testes.

---

## 🧰 3. Pipeline de Segurança (CI/CD)  

### 3.1. SAST — Semgrep  
- Configurado arquivo `semgrep.yml` com regras de **análise estática** de código-fonte:  
  - Verificação de uso de funções inseguras (`eval`, `os.system`, etc.).  
  - Checagem de manipulação segura de dados sensíveis.  
- Executado via GitHub Actions em `.github/workflows/main-pipeline.yml`.  
- Saída registrada em `semgrep-report.json`.

### 3.2. SCA — pip-audit  
- Auditoria automatizada de vulnerabilidades em dependências Python.  
- Comando utilizado:
  ```bash
  pip-audit --format json > pip-audit-report.json

### 3.3. DAST — OWASP ZAP (opcional)
- Etapa configurável para execução de varredura dinâmica com OWASP ZAP no container de teste.
- Evidências de segurança podem ser exportadas em zap-report.html.

---

### 📂 4. Estrutura de Logs e Evidências

| Tipo de Evidência     | Arquivo / Ferramenta    | Descrição                          |
| --------------------- | ----------------------- | ---------------------------------- |
| Logs de Consentimento | `consent.log`           | Registro LGPD em formato JSON      |
| Testes Automatizados  | `pytest`                | Validação funcional e de segurança |
| SAST Report           | `semgrep-report.json`   | Análise estática de código         |
| SCA Report            | `pip-audit-report.json` | Auditoria de dependências          |
| DAST Report           | `zap-report.html`       | Varredura dinâmica (opcional)      |

---

### ⚙️ 5. Práticas SSDLC Adotadas

- Validação e sanitização de entradas de usuários.
- Uso de variáveis de ambiente para credenciais e segredos.
- Logging seguro sem exposição de informações sensíveis.
- Criação de testes automatizados como parte da pipeline.
- Princípio do menor privilégio aplicado no Dockerfile (USER nonroot).
- Adoção de controle de versão seguro (sem commits com chaves/segredos).

---
### 🧩 6. Riscos Residuais e Melhorias Futuras

- Implementar encriptação em repouso para dados sensíveis (em banco).
- Integrar ferramenta de secret scanning no CI.
- Adicionar autenticação multifator em endpoints administrativos.
- Expandir o módulo de consentimento para revogação e anonimização de dados.

---

### ✅ 7. Conclusão

A InvestmentAdvisor Secure API cumpre os requisitos da Sprint 4 de Cybersecurity, apresentando:

- Controles de segurança e privacidade em conformidade com a LGPD;
- Testes automatizados para autenticação e consentimento;
- Pipeline de segurança funcional com SAST e SCA;
- Evidências auditáveis e documentação técnica do ciclo SSDLC.

        Status: ✔️ Conformidade alcançada — projeto seguro, testado e auditável.