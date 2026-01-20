# Plataforma de Gestão de Vagas e Capacitação Profissional

## 👥 Equipe
- **Antônio Pereira da Luz Neto** – GitHub: [netoo-444](https://github.com/netoo-444)  
- **Diogo Gomes Figueiredo** – GitHub: [fgrdiogo](https://github.com/fgrdiogo)  
- **Manoel Junio Duarte da Silva** – GitHub: [Junio404](https://github.com/Junio404)

---

## 🎯 Descrição do Domínio

A plataforma integra **colocação profissional** e **desenvolvimento de carreira** em um único ambiente.  
Ela conecta candidatos a vagas e cursos, eliminando a separação entre buscar emprego e adquirir as habilidades exigidas pelo mercado.

O sistema atua de forma **ativa**, sugerindo oportunidades personalizadas e permitindo que vagas tenham **pré-requisitos**, como a conclusão de cursos oferecidos na própria plataforma.

---

## 👤 Atores do Sistema

- **Candidatos**: Buscam vagas e trilhas de capacitação.  
- **Empresas**: Publicam vagas de emprego e cursos corporativos.  
- **Instituições de Ensino**: Oferecem cursos de capacitação geral.

---

## 🔄 Dinâmica Principal

- Oportunidades podem ser **Vagas de Emprego** ou **Cursos de Capacitação**.  
- Vagas podem exigir cursos como pré-requisito.  
- O sistema sugere combinações inteligentes entre perfil, vagas e cursos.

---

## 🧠 Justificativa da Complexidade

A complexidade do sistema se baseia em quatro pilares:

1. **Identidades Múltiplas e Polimorfismo**  
   Três tipos de usuários com comportamentos distintos, tratados por herança e polimorfismo.

2. **Motor de Recomendação (Strategy)**  
   Algoritmos de compatibilidade variáveis, aplicando o padrão *Strategy*.

3. **Gestão de Estados (State)**  
   Controle rigoroso do ciclo de vida das oportunidades (Ex: Aberta → Em Análise → Preenchida).

4. **Arquitetura Robusta**  
   Separação entre domínio e persistência, com injeção de dependência e regras de negócio bem definidas.

---

## 🧩 Hierarquias Principais

### 📁 Organização
Classe base: `Organizacao` (abstrata)  
Subclasses: `Empresa`, `InstituicaoEnsino`

- `Empresa`: pode publicar **Vagas de Emprego** e **Cursos**  
- `InstituicaoEnsino`: publica apenas **Cursos**

---

### 📁 Oportunidades
Classe base: `Oportunidade` (abstrata)  
Subclasses: `VagaEmprego`, `CursoCapacitacao`

- `VagaEmprego`: inicia fluxo de recrutamento  
- `CursoCapacitacao`: executa fluxo de matrícula

---

## 🛠️ Padrões de Projeto

- **State** → Controle de estados de vagas e candidaturas  
- **Strategy** → Algoritmos de compatibilidade e recomendação

---

## 📐 Princípios SOLID Aplicados

- **SRP** – Cada classe tem uma única responsabilidade  
- **OCP** – Extensível sem modificar código existente  
- **LSP** – Subclasses substituem classes base corretamente  
- **DIP** – Dependência em abstrações com injeção de dependência

---

📌 *Este projeto visa criar uma plataforma inteligente, extensível e orientada a objetos para unir capacitação e empregabilidade de forma eficiente.*
