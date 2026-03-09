# SKILLUP — Plataforma de Gestão de Vagas e Capacitação Profissional

Repositório da disciplina de Programação Orientada a Objetos. O projeto implementa uma plataforma em Python para conectar candidatos, empresas e instituições de ensino em um único ambiente de empregabilidade e formação profissional.

## 👥 Equipe

- **Antônio Pereira da Luz Neto** – GitHub: [netoo-444](https://github.com/netoo-444)
- **Diogo Gomes Figueiredo** – GitHub: [fgrdiogo](https://github.com/fgrdiogo)
- **Manoel Junio Duarte da Silva** – GitHub: [Junio404](https://github.com/Junio404)

---

## 📝 Descrição Geral e Objetivo do Projeto

O **SkillUp** é um sistema orientado a objetos para **gestão de vagas, candidaturas, cursos e desenvolvimento de competências**. A proposta central do projeto é unir dois problemas normalmente separados:

1. a busca por oportunidades profissionais;  
2. a capacitação necessária para alcançar essas oportunidades.

Na prática, a plataforma permite que:

- **candidatos** mantenham perfil, currículo, competências, inscrições e candidaturas;
- **empresas** publiquem vagas e visualizem candidatos;
- **instituições de ensino** publiquem cursos e gerenciem áreas de ensino;
- o sistema faça **buscas e recomendações** de vagas e cursos com base no perfil do usuário.

O objetivo do projeto é aplicar conceitos de **POO, separação em camadas, regras de negócio, persistência em JSON, testes automatizados e arquitetura desacoplada**.

---

## 🎯 O que o sistema faz

- Cadastro e login de candidatos, empresas e instituições;
- gerenciamento de perfil e currículo do candidato;
- gerenciamento de competências do candidato;
- cadastro e busca de vagas CLT e de estágio;
- cadastro e gerenciamento de cursos EAD e presenciais;
- inscrições em cursos e candidaturas em vagas;
- associação de competências a cursos e requisitos a vagas;
- recomendação de vagas e cursos;
- persistência em arquivos JSON;
- execução por fluxos de menu em terminal;
- suíte de testes unitários, de services e de fluxos.

---

## 🧱 Entidades do Domínio

Esta seção resume o papel de cada entidade da pasta `src/dominio`.

### `EntidadePublicadora`
Classe abstrata base para organizações que publicam oportunidades. Centraliza `id`, `nome` e `cnpj`, além do contrato de validação para publicação.

### `Candidato`
Representa o usuário que busca oportunidades. Armazena dados cadastrais, áreas de interesse, nível de formação, localidade e currículo. Também concentra regras de edição de perfil e currículo.

### `Empresa`
Representa a organização que publica vagas. Armazena nome, CNPJ e porte, além da regra de limite de publicações conforme o tamanho da empresa.

### `InstituicaoEnsino`
Representa instituições que ofertam cursos. Controla credenciamento, modalidades aceitas, dados cadastrais e autorização para publicação de cursos.

### `AreaEnsino`
Representa uma área temática de ensino, como Tecnologia, Saúde ou Administração.

### `InstituicaoAreaEnsino`
Entidade de vínculo entre uma instituição e uma área de ensino. Permite mapear quais áreas cada instituição atende.

### `Competencia`
Representa uma habilidade do catálogo do sistema, como Python, Comunicação ou Banco de Dados.

### `CompetenciaCandidato`
Relaciona um candidato a uma competência específica, incluindo o nível atual de domínio (`iniciante`, `intermediario`, `avancado`).

### `Curso`
Classe abstrata base dos cursos. Define dados comuns, como nome, área, carga horária, capacidade, prazo de inscrição e estado de publicação.

### `CursoEAD`
Especialização de `Curso` para ensino remoto. Mantém a URL da plataforma e força a modalidade remota.

### `CursoPresencial`
Especialização de `Curso` para ensino presencial. Mantém a localidade e força a modalidade presencial.

### `CursoCompetencia`
Relaciona um curso a uma competência ofertada, definindo o nível que o curso confere ao aluno ao ser concluído.

### `Vaga`
Classe abstrata base das vagas. Define título, descrição, área, modalidade, tipo, requisitos e status de publicação.

### `VagaCLT`
Especialização de `Vaga` para oportunidades de emprego CLT. Armazena salário base e localidade.

### `VagaEstagio`
Especialização de `Vaga` para oportunidades de estágio. Armazena bolsa auxílio, instituição conveniada e localidade.

### `RequisitoVaga`
Relaciona uma vaga a uma competência exigida, com nível mínimo e obrigatoriedade.

### `Candidatura`
Representa a candidatura de um candidato a uma vaga. Controla data e status do processo seletivo.

### `InscricaoCurso`
Representa a inscrição de um candidato em um curso. Controla data da inscrição e status acadêmico da matrícula.

### `Validators`
O arquivo `validators.py` concentra validadores reutilizáveis do domínio, como CPF, CNPJ, email, níveis, prazos, localidade e tipos básicos, mantendo modularização e reutilização de código bem padronizadas.

---

## ⚙️ Clonagem do Repositório, Ambiente Virtual e Execução com Poetry

Esta seção mostra o passo a passo para preparar o projeto localmente e executar tanto os testes quanto o fluxo principal.

### Pré-requisitos

- Python 3.11 ou superior instalado;
- Git instalado;
- acesso ao terminal (PowerShell, CMD ou Git Bash).

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/<seu-usuario-ou-organizacao>/SkillUp.git
```

### 2️⃣ Entrar na pasta do projeto Python

```bash
cd SkillUp/skillup_project
```

### 3️⃣ Criar o ambiente virtual

```bash
python -m venv .venv
```

### 4️⃣ Ativar o ambiente virtual no Windows

```powershell
.venv\Scripts\activate
```

Após a ativação, o terminal deve exibir algo como:

```powershell
(.venv)
```

### 5️⃣ Instalar Poetry e pytest

Com o ambiente virtual ativado, instale o Poetry e o pytest:

```bash
pip install poetry pytest
```

### 6️⃣ Instalar o projeto com Poetry

```bash
poetry install
```

### 7️⃣ Executar todos os testes com Poetry

```bash
poetry run pytest tests/ -v
```

### 8️⃣ Executar apenas um grupo de testes

#### Testes de domínio

```bash
poetry run pytest tests/teste_dominio/ -v
```

#### Testes de services

```bash
poetry run pytest tests/test_services/ -v
```

#### Testes de fluxos

```bash
poetry run pytest tests/test_fluxos/ -v
```
### Executar um teste específico

```bash
poetry run pytest tests/teste_dominio/test_candidato.py -v
```

### 9️⃣ Executar o fluxo principal da aplicação

```bash
poetry run python main.py
```

Ao iniciar, o sistema abre o menu principal em modo terminal, com opções para candidato, empresa e instituição de ensino.

### 🔟 Resumo rápido de comandos

```bash
git clone https://github.com/<seu-usuario-ou-organizacao>/SkillUp.git
cd SkillUp/skillup_project
python -m venv .venv
.venv\Scripts\activate
pip install poetry pytest
poetry install
poetry run pytest tests/ -v
poetry run python main.py
```

---

## 📁 Estrutura do Diretório

```text
SkillUp/
├── README.md                      # Documentação principal do repositório
├── diagrams/                      # Diagramas, imagens e materiais visuais do projeto
└── skillup_project/               # Projeto Python executável
    ├── README.md                  # Documentação local do pacote Python
    ├── main.py                    # Ponto de entrada principal da aplicação em terminal
    ├── pyproject.toml             # Configuração do Poetry
    ├── poetry.lock                # Lockfile das dependências resolvidas
    ├── src/                       # Código-fonte do sistema
    │   ├── aplicacao/             # Fluxos de navegação CLI para candidato, empresa, instituição e admins
    │   ├── data/                  # Arquivos JSON usados como persistência local
    │   ├── dominio/               # Entidades, enums, validadores e mapeadores do negócio
    │   ├── interfaces/            # Contratos/abstrações usados pelas camadas
    │   ├── repositorios/          # Repositórios JSON e operações de persistência
    │   └── services/              # Casos de uso, regras de negócio aplicadas e orquestração
    └── tests/                     # Testes automatizados
        ├── teste_dominio/         # Testes unitários das entidades e validadores
        ├── test_services/         # Testes dos services e integrações com mocks
        └── test_fluxos/           # Testes dos fluxos de menus e interação CLI
```

### O que cada pasta contém

#### `diagrams/`
Contém diagramas UML, MER, rascunhos e materiais visuais usados para modelagem e apresentação do sistema.

#### `skillup_project/src/aplicacao/`
Contém os fluxos de interação em terminal. É aqui que ficam os menus para candidato, empresa, instituição e backoffice administrativo.

#### `skillup_project/src/data/`
Contém arquivos JSON de persistência local. Esses arquivos armazenam dados como candidatos, empresas, instituições e vínculos do sistema.

#### `skillup_project/src/dominio/`
Contém as entidades do negócio, validadores, enums, regras centrais e mappers de serialização.

#### `skillup_project/src/interfaces/`
Contém contratos e abstrações usados para desacoplar domínio, repositórios e services.

#### `skillup_project/src/repositorios/`
Contém os repositórios responsáveis por leitura e escrita dos dados em JSON, além de consultas específicas.

#### `skillup_project/src/services/`
Contém os casos de uso e as regras de negócio aplicadas sobre o domínio, como cadastro, busca, filtros, controle de status, recomendações e validações de unicidade.

#### `skillup_project/tests/teste_dominio/`
Contém testes unitários das entidades de domínio, validadores e regras centrais.

#### `skillup_project/tests/test_services/`
Contém testes da camada de serviços, garantindo fluxos de negócio, integração entre objetos e uso de repositórios.

#### `skillup_project/tests/test_fluxos/`
Contém testes dos fluxos CLI, menus, autenticação e navegação principal do sistema.

---

## 🧪 Exemplos de Uso

### Exemplo 1 — Executar o sistema principal

```bash
poetry run python main.py
```

Saída esperada no terminal:

```text
============================================================
                 BEM-VINDO AO SKILLUP
      Plataforma de Gestão de Vagas e Capacitação
============================================================

Escolha seu perfil na plataforma:

  1. Candidato
  2. Empresa
  3. Instituição de Ensino
  4. Sair
```



### Exemplo 2 — Fluxo básico de candidato

1. iniciar o sistema com `poetry run python main.py`;  
2. escolher a opção `1. Candidato`;  
3. fazer cadastro ou login;  
4. acessar menus de vagas, cursos, candidaturas, competências e perfil;  
5. editar currículo, áreas de interesse e dados pessoais.

### Exemplo 3 — Fluxo básico de empresa

1. iniciar o sistema com `poetry run python main.py`;  
2. escolher a opção `2. Empresa`;  
3. fazer cadastro ou login;  
4. acessar o menu de candidaturas;  
5. visualizar candidatos de uma vaga e consultar currículos por ID.

### Exemplo 4 — Fluxo básico de instituição

1. iniciar o sistema com `poetry run python main.py`;  
2. escolher a opção `3. Instituição de Ensino`;  
3. fazer cadastro ou login;  
4. acessar os menus disponíveis para gestão institucional e cursos.

---

## 🏗️ Arquitetura e Boas Práticas Aplicadas

- **Programação Orientada a Objetos** com entidades e regras no domínio;
- **separação por camadas**: domínio, services, repositórios e aplicação;
- **Repository Pattern** para persistência desacoplada;
- **State** → Controle de estados de vagas e candidaturas;  
- **Strategy** → Algoritmos de compatibilidade e recomendação;
- **Domain drive development** → Criação do sistema como um todo baseado nas entidades de domínio;
- **injeção de dependência** nas entidades e services;
- **persistência local em JSON** para simplificar execução e testes;
- **testes automatizados** para domínio, services e fluxos;
- **regras de negócio centralizadas** nas entidades e nos services;
- **SRP** → Cada classe tem uma única responsabilidade;  
- **OCP** → Extensível sem modificar código existente;  
- **LSP** → Subclasses substituem classes base corretamente;  
- **DIP** → Dependência em abstrações com injeção de dependência;

---

## ✅ Observações Finais

- O projeto é executado em terminal e não depende de banco relacional externo.
- A persistência é feita por arquivos JSON na pasta `src/data`.
- O fluxo principal está em `skillup_project/main.py`.
- O projeto possui cobertura automatizada para domínio, services e fluxos.

Se desejar, o próximo passo pode ser adicionar ao README uma seção extra com:

- requisitos funcionais e regras de negócio resumidas;
- tecnologias utilizadas;
- diagrama de classes;
- diagrama de casos de uso.
