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

---

## 🌐 8. Extensões Planejadas — Controles Avançados

Embora não obrigatórios nesta sprint, estão planejadas as seguintes evoluções de segurança para o ambiente de produção e auditoria contínua:

### 8.1. DAST — OWASP ZAP (Ambiente Staging)
Para complementar o ciclo SSDLC, está prevista a integração do **OWASP ZAP** como etapa de **análise dinâmica de segurança (DAST)** no pipeline CI/CD.  
O objetivo é simular ataques e validar a segurança da aplicação em execução (ambiente *staging*), garantindo:
- Detecção automática de vulnerabilidades em endpoints;
- Verificação de cabeçalhos HTTP seguros (CORS, CSP, HSTS);
- Simulação de comunicação HTTPS/TLS;
- Relatórios HTML exportáveis (`zap-report.html`).

### 8.2. RBAC — Controle de Acesso Baseado em Papéis
Como aprimoramento de conformidade à LGPD e princípios de *Least Privilege*, será adicionada uma camada de **controle de acesso por papéis (RBAC)**, permitindo segmentar permissões entre:
- **Usuários comuns:** acesso apenas a dados próprios e consentimento;
- **Administradores:** acesso a logs de auditoria e relatórios de segurança.

Essa implementação aumentará a rastreabilidade e reforçará o princípio de necessidade mínima de acesso.

---

## 🧩 9. Conclusão Final Atualizada
Com a inclusão dos planejamentos de **DAST (OWASP ZAP)** e **RBAC**, o projeto *InvestmentAdvisor Secure API* atinge conformidade total com os requisitos da **Sprint 4 — Cybersecurity**, incluindo:
- SSDLC automatizado com SAST e SCA;  
- Conformidade LGPD com logs auditáveis;  
- Pipeline completo com testes automatizados e segurança de container;  
- Planejamento documentado de DAST e RBAC para o ciclo de maturidade contínuo.  

**Status Final:** 🟢 Projeto completo — segurança implementada, testada e em conformidade com todas as práticas recomendadas.
