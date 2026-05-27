---
title: "What Glean’s Knowledge Graph Approach Reveals About Enterprise AI Search"
slug: "enterprise-ai-agents-knowledge-layer-beyond-rag"
description: "An analysis of Glean’s knowledge graph approach to enterprise AI search, and what it reveals about retrieval, permissions, relationships, approvals, and operational state beyond vector RAG."
author: "Max"
site: "rmax.ai"
section: "notes"
type: "technical-note"
status: "published"
date: "2026-05-27"
updated: "2026-05-27"
tags: ["enterprise-ai", "ai-agents", "knowledge-graphs", "graph-rag", "enterprise-search", "ontology", "ai-governance"]
reading_time: "14–16 min"
canonical_url: "https://rmax.ai/notes/enterprise-ai-agents-knowledge-layer-beyond-rag/"
license: "CC BY 4.0"
---

# What Glean’s Knowledge Graph Approach Reveals About Enterprise AI Search

## Abstract

This note uses Glean’s knowledge graph framing as a concrete lens on enterprise AI search. The core lesson is that search and RAG are useful but insufficient for serious enterprise workflows, because those workflows depend on relationships, permissions, approvals, provenance, and operational state. Glean’s approach is valuable not merely as product positioning, but because it exposes a broader architectural point: enterprise AI search becomes more useful when it resolves organizational reality into governed entities, relationships, and outcomes rather than retrieving disconnected text alone.

## Source framing

The main source for this note is Glean’s *Working AI: Knowledge Graph* conversation with Rob Stetts, supported by Glean’s published material on enterprise search and knowledge graphs, plus background references on RAG, GraphRAG, ontologies, provenance, and authorization.

The goal here is not to restate Glean’s product narrative. It is to use Glean’s framing as a practical case study for a broader systems question: what kind of retrieval and knowledge architecture enterprise AI search needs when the task is not only answering questions, but helping agents and operators work over governed organizational state.

## Search is necessary, but it is not organizational understanding

Most enterprise AI adoption begins with search: connect Slack, Drive, Jira, GitHub, Confluence, and internal documentation, then allow an assistant to answer questions over that material. This is useful. It is also only the first layer.

Search can retrieve documents. Retrieval-augmented generation can ground an answer in relevant text. But enterprise work is rarely a document lookup problem. It is a problem of relationships, permissions, ownership, policy, state, and outcomes.

For many questions, search is sufficient:

- What does the expense policy say about international travel?
- Find the design document for a specific service.
- Summarize the incident review from last week.
- Which documents mention Project X?

These are retrieval problems. The answer is contained in one document or a small group of related passages.

Enterprise agents face a different class of questions:

- What is blocking Project X, and who owns each dependency?
- Which engineering work this quarter did not contribute to an agreed objective?
- Why is this merchant onboarding case stalled?
- Is this agent allowed to make this change, or does it require approval?
- What evidence justified a previous operational decision, and what was the outcome?

These are not merely search problems. They are relationship and state problems.

An agent investigating why a workflow is blocked does not merely need the right paragraph in a document. It needs to know which case is affected, which policy governs it, which approval is missing, who may grant it, which evidence supports the decision, and whether it is authorized to propose or execute the next step.

An enterprise agent that cannot resolve these connections will either remain a document summarizer or begin guessing across incomplete context. Neither is enough for serious operational work.

## The knowledge layer: turning artifacts into organizational reality

A knowledge layer sits between enterprise systems and the agents that use them. Its purpose is not simply to index content, but to convert fragmented artifacts into canonical, permission-aware, and traceable organizational concepts.

A project may appear as:

- an epic in Jira;
- a repository in GitHub;
- a roadmap objective in a planning document;
- a Slack channel;
- an owner in the employee directory;
- a service in an internal catalogue;
- an incident record in an operations system.

A search engine can retrieve each artifact. A knowledge layer identifies that these artifacts refer to the same operational reality.

<div class="mermaid">
flowchart LR
    J["Jira epic<br/>EPIC-421"] --> P["Project<br/>Merchant Risk Refresh"]
    G["GitHub repo<br/>risk-workflows"] --> P
    O["Roadmap objective<br/>Reduce manual review latency"] --> P
    S["Slack channel"] --> P
    D["Employee directory owner"] --> P
    C["Service catalogue entry"] --> P
    I["Incident record"] --> P
    P --> A["Blocking approval<br/>A-184"]
    P --> Pol["Governing policy<br/>Enhanced Risk Review"]
    P --> E["Evidence bundle<br/>documents, case history, reviewer notes"]
</div>

Instead of retrieving disconnected snippets, the system can resolve one operational object with the relationships that matter around it.

This is a fundamental change in what an agent can do. It no longer has to reconstruct the organization from scattered text on every invocation. It can operate over stable concepts: cases, workflows, owners, policies, decisions, and outcomes.

The knowledge layer needs more than entity names. Each fact must carry properties that determine whether the agent may trust or expose it:

- source and provenance;
- timestamp and freshness;
- validity interval and supersession state;
- confidence or verification status;
- access-control scope;
- whether the fact was human-asserted, system-generated, or model-extracted.

Without these properties, an enterprise graph becomes an impressive-looking source of stale or unsafe assumptions.

## Knowledge graphs solve multi-hop enterprise questions

A knowledge graph encodes entities and the relationships between them. In the enterprise context, entities are not only people and documents. They are workflows, cases, objectives, policies, approvals, code changes, incidents, decisions, and business outcomes.

The basic value of a graph is simple: it makes relationships traversable.

Consider a question such as:

> Why is this customer onboarding workflow delayed, and what needs to happen next?

A standard RAG system may retrieve a few semantically similar documents and ask the language model to infer the rest. A graph-backed system can traverse a connected path instead:

<div class="mermaid">
flowchart LR
    Customer["Customer"] -->|has_onboarding_case| Case["Onboarding case"]
    Case -->|governed_by| Policy["Policy"]
    Case -->|requires| Approval["Approval"]
    Approval -->|currently_waiting_on| Reviewer["Reviewer role"]
    Case -->|supported_by| Evidence["Evidence documents"]
    Approval -->|permits_after_approval| Action["Account activation action"]
</div>

The language model is still useful. It can explain the situation, produce a summary, draft a recommendation, or prepare an approval request. But the core organizational joins no longer depend on the model guessing correctly from loosely related chunks.

This matters because enterprise questions are often inherently multi-hop. A project status question may require linking objectives to tasks, tasks to code changes, code changes to incidents, and incidents back to unplanned work. A procurement question may require linking a purchase request to a policy threshold, vendor classification, budget owner, and approval chain. A support escalation may require linking a customer, contract, product incident, service owner, and remediation decision.

Graph-based retrieval shifts part of this reasoning from runtime prompt construction into a maintained organizational model. That can reduce repeated search loops, improve evidence quality, and make the path behind an answer inspectable.

But it also creates a responsibility: the graph must be kept fresh, permission-aware, and contestable. A graph is not automatically ground truth merely because it is structured.

## Ontologies are the missing discipline behind enterprise graphs

A graph without an ontology is only a collection of connections. An ontology gives those connections consistent business meaning.

If one team models an owner as the engineer who last touched a repository, another models it as the accountable product lead, and another models it as the approval authority, an agent cannot reliably reason about ownership. The words look similar while the operational meaning differs.

An ontology defines the entity types, relationship types, and constraints that matter within a workflow domain.

For a governed enterprise workflow, a minimal ontology might look like this:

<div class="mermaid">
erDiagram
    PERSON }o--o{ TEAM : MEMBER_OF
    TEAM ||--o{ WORKFLOW : OWNS
    WORKFLOW ||--o{ CASE : INSTANCE_OF
    WORKFLOW }o--|| POLICY : GOVERNED_BY
    CASE ||--o{ EVIDENCE : SUPPORTED_BY
    CASE ||--o{ APPROVAL : REQUIRES
    APPROVAL }o--|| PERSON : GRANTED_BY
    DECISION }o--o{ EVIDENCE : BASED_ON
    ACTION }o--|| APPROVAL : AUTHORIZED_BY
    OUTCOME }o--|| ACTION : RESULT_OF
</div>

This is not an attempt to model the whole company in advance. That would be slow, brittle, and likely fail. The practical approach is workflow-first ontology design: model one high-value operational domain, validate that the relationships support useful agent behavior, then expand only where reuse is proven.

For enterprise agents, ontology work is architecture work. It determines what the system can safely answer, what it can check before proposing actions, and what evidence it can preserve after a workflow completes.

## Authorization must exist inside the knowledge model

In consumer search, a relationship in a graph can often be treated as public information. Inside an enterprise, even the existence of a relationship may be sensitive.

An agent does not need to quote a confidential document to leak information. It may leak that an employee is connected to an investigation, that a customer account is under risk review, or that a confidential project depends on an unreleased product decision.

This makes security a property of facts and relationships, not merely documents.

<div class="mermaid">
flowchart TD
    Fact["Fact<br/>Case A → requires approval → Risk Lead"] --> Meta["Attached metadata<br/>source, ACL, validity, provenance, sensitivity, policy scope"]
    Meta --> Retrieve{"Requester and agent authorized to retrieve the fact?"}
    Retrieve -- No --> Deny["Do not reveal fact or relationship"]
    Retrieve -- Yes --> Output{"May the agent summarize or infer from it?"}
    Output -- No --> Constrain["Constrain or suppress output"]
    Output -- Yes --> Act{"May the agent propose or execute an action?"}
    Act -- Approval required --> Human["Route to human approval"]
    Act -- Allowed --> Audit["Execute with audit trail and attribution"]
</div>

Glean describes this as extending graph triples with an additional metadata field so access constraints can be attached directly to individual facts. The broader architectural principle is more important than the specific storage model: retrieval must not expose graph facts unless the requesting user and the acting agent are allowed to see them.

Even that is not sufficient on its own. Agents synthesize conclusions across retrieved facts. A safe enterprise architecture also needs policy enforcement at the output and action layers:

- Is the user allowed to see the underlying evidence?
- Is the agent permitted to summarize the inferred conclusion?
- Can the agent propose a write action?
- Does the write require human approval?
- Was the eventual execution recorded and attributable?

This is where a knowledge layer meets an agent gateway. The graph describes relevant organizational state. The gateway enforces what agents are permitted to retrieve, infer, propose, and execute.

## From knowledge retrieval to organizational state

The most interesting application of a knowledge graph is not better chat. It is the ability to expose patterns in the way an organization operates.

In a Glean example, an internal agent used relationships between objectives and engineering activity to analyze progress against OKRs. The system highlighted a large amount of work that was not linked to declared objectives. Investigation reportedly showed that engineers were spending substantial effort on problems caused by database growth. The team paused feature work to address the underlying system issue.

The important insight is not that a graph can generate a status update. It is that graph-connected evidence can identify the gap between declared organizational intent and actual operational effort.

This creates a richer category of enterprise agent capability:

| Capability | Document-centric assistant | Knowledge-layer agent |
| --- | --- | --- |
| Status reporting | Summarizes written updates | Traces work, dependencies, and outcomes |
| Incident analysis | Retrieves postmortems | Connects incidents, services, changes, and owners |
| Governance | Summarizes policies | Checks policies, permissions, and approval state |
| Decision preparation | Summarizes source documents | Produces evidence paths and identifies missing controls |
| Strategic review | Finds planning artifacts | Detects orphaned work, blocked objectives, and systemic overhead |

This is where enterprise agents become operational systems rather than intelligent search boxes.

A mature knowledge layer can preserve durable organizational state:

<div class="mermaid">
flowchart LR
    Case["Case"] --> Decision["Decision"]
    Decision --> Evidence["Evidence"]
    Evidence --> Approval["Approval"]
    Approval --> Execution["Execution"]
    Execution --> Outcome["Outcome"]
</div>

This should not become a dump of agent reasoning traces. Internal chain-of-thought and every tool call are not institutional knowledge. The graph should preserve validated facts, decisions, approvals, and outcomes that future agents and humans need to understand the organization’s history and current state.

## The hard problems cannot be hand-waved away

Knowledge graphs are powerful, but they do not make enterprise AI reliable by default.

First, a graph is not objective merely because it is structured. An engineering task that lacks an explicit link to an OKR may be waste, or it may be essential resilience work that was never correctly categorized. A model that treats missing links as proof of low value will produce managerial fiction with the appearance of precision.

Second, graph construction shifts complexity rather than eliminating it. Entity resolution, relationship extraction, permission synchronization, temporal correctness, and schema evolution are difficult continuous engineering problems. Runtime token reduction is useful, but it does not by itself justify the total system cost.

Third, access-controlled retrieval does not fully solve information leakage. An agent may combine allowed facts into a sensitive inference. Enterprise systems must evaluate both unauthorized retrieval and unauthorized conclusions.

Finally, operational graphs can drift into employee surveillance. Their best use is to identify workflow friction, hidden dependencies, and system-level failure patterns. Their most dangerous use is to pretend that visible activity graphs are complete measures of individual contribution.

The discipline is clear: use graphs to make processes legible and decisions accountable, not to replace judgment with dashboards.

## A reference architecture for enterprise agents

The enterprise agent stack is not simply model plus tools. It is a governed runtime grounded in organizational knowledge.

<div class="mermaid">
flowchart TD
    A["Enterprise systems<br/>Slack, Drive, Jira, GitHub, CRM, ERP"] --> B["Connectors and identity sync"]
    B --> C["Permission-aware knowledge layer<br/>documents, entities, provenance, ACLs, temporal state"]
    C --> D["Ontology and knowledge graph<br/>workflows, cases, policies, decisions, outcomes"]
    D --> E["Retrieval plane<br/>semantic search, graph traversal, citations"]
    E --> F["Agent runtime<br/>plan, interpret, propose, evaluate"]
    F --> G["Governed action gateway<br/>policy checks, approvals, audit, execution"]
    G --> H["Validated outcomes"]
    H --> D
</div>

Each layer answers a different enterprise requirement:

- Search finds information.
- RAG grounds generated answers.
- The knowledge layer resolves identity, permissions, freshness, and provenance.
- The graph represents relationships and operational state.
- Ontologies ensure those relationships have stable meaning.
- The agent runtime interprets context and prepares work.
- The action gateway constrains autonomy through policy, approvals, and audit.
- Outcome capture allows the organization to learn from validated execution.

The model is not the system. The system is the governed environment within which the model can resolve organizational reality and act without exceeding authority.

## The real thesis: enterprise agents need a knowledge control plane

RAG is a retrieval pattern. Enterprise autonomy requires a control plane.

An enterprise knowledge control plane would be responsible for:

- resolving business entities across fragmented systems;
- expressing relationships through workflow-specific ontologies;
- preserving provenance and temporal state;
- enforcing fact-level permissions;
- supporting graph traversal for multi-hop operational questions;
- binding proposed actions to policies and approvals;
- recording validated decisions and outcomes for future reasoning.

This changes how enterprise agents should be evaluated. The question is not simply whether an assistant can answer questions accurately. The stronger questions are:

- Can it identify the correct operational object across systems?
- Can it explain the evidence path behind a conclusion?
- Can it respect permissions not only for documents, but for inferred relationships?
- Can it identify missing approvals before an action is attempted?
- Can it record a durable outcome without polluting institutional memory with unverified model output?

The enterprise agent is only as intelligent as the organizational reality it can safely resolve into entities, relationships, policies, and outcomes.

That reality is not contained in the language model. It must be engineered around it.

## Research direction: building a small proof of the knowledge control plane

A useful prototype does not require modelling an entire enterprise. It requires one realistic workflow in which search alone is clearly insufficient.

A small research implementation could model a governed workflow such as a merchant risk escalation, support incident remediation, or internal access request:

<div class="mermaid">
flowchart LR
    User["User"] --> Role["Role"]
    Role --> Workflow["Workflow"]
    Workflow --> Case["Case"]
    Case --> Evidence["Evidence"]
    Evidence --> Proposed["Proposed action"]
    Proposed --> Approval["Approval"]
    Approval --> Outcome["Outcome"]
</div>

The prototype should compare four approaches:

1. semantic search over documents;
2. vector RAG with citations;
3. graph-assisted retrieval;
4. graph-assisted retrieval with permissions, approval state, and outcome recording.

A benchmark of cross-system questions can test when each architecture fails:

- direct policy lookup;
- multi-hop ownership resolution;
- missing approval detection;
- unauthorized evidence access;
- time-sensitive workflow state;
- reconstruction of a prior decision from evidence and outcome records.

The evaluation should measure correctness, evidence quality, permission failures, inference leakage, latency, and token consumption.

This is the practical research frontier for enterprise AI agents: not another chatbot over company documents, but a minimal governed system capable of reasoning over organizational state and acting only through accountable boundaries.

## Conclusion

What Glean’s knowledge graph approach makes clear is that enterprise AI search is not only about better retrieval quality. It is about whether the system can represent enough organizational structure to answer multi-hop questions, respect permissions at the fact level, expose evidence paths, and connect search results to governed action.

Search gives access to company information. RAG gives grounded text. A knowledge graph adds traversable relationships. Ontologies stabilize the meaning of those relationships. Permission-aware provenance makes them safer to expose. Policy and approvals make downstream action governable. Outcome capture makes the system capable of learning from execution rather than only from documents.

Even if one does not adopt Glean’s exact implementation, the architectural lesson holds: enterprise AI search becomes substantially more valuable when it operates over organizational state instead of over semantically similar passages alone.

## References

### Core source

- Glean. *Working AI: Knowledge Graph*. Interview with Rob Stetts. <https://www.youtube.com/watch?v=MsZUIi97ynk>

### Enterprise search and enterprise knowledge layers

- Glean. *The Glean Knowledge Graph: How It Powers Enterprise Search and Generative AI*. <https://www.glean.com/resources/guides/glean-knowledge-graph>
- Glean. *Hybrid Search vs. RAG and Vector Search: Key Differences*. 2024. <https://www.glean.com/blog/hybrid-vs-rag-vector>
- Glean. *How Knowledge Graphs Work and Why They Are the Key to Enterprise AI Agents*. 2025. <https://www.glean.com/blog/knowledge-graph-agentic-engine>

### RAG and GraphRAG

- Lewis, Patrick, et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS, 2020. <https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html>
- Edge, Darren, et al. *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. Microsoft Research, 2024. <https://arxiv.org/abs/2404.16130>
- Microsoft Research. *GraphRAG Documentation*. <https://microsoft.github.io/graphrag/>
- Microsoft Research. *Project GraphRAG Publications*. <https://www.microsoft.com/en-us/research/project/graphrag/publications/>

### Knowledge graphs

- Hogan, Aidan, et al. *Knowledge Graphs*. ACM Computing Surveys, 54(4), 2021. <https://dl.acm.org/doi/10.1145/3447772>
- Jarnac, Lucas, et al. *Uncertainty Management in the Construction of Knowledge Graphs*. Transactions on Graph Data and Knowledge, 2025. <https://drops.dagstuhl.de/entities/document/10.4230/TGDK.3.1.3>

### Ontologies and semantic modelling

- Noy, Natalya F., and Deborah L. McGuinness. *Ontology Development 101: A Guide to Creating Your First Ontology*. Stanford Knowledge Systems Laboratory, 2001. <https://protege.stanford.edu/publications/ontology_development/ontology101.pdf>
- W3C. *RDF 1.2 Concepts and Abstract Data Model*. 2026. <https://www.w3.org/TR/rdf12-concepts/>
- W3C. *OWL 2 Web Ontology Language Primer*. 2012. <https://www.w3.org/TR/owl2-primer/>
- W3C. *OWL 2 Web Ontology Language Document Overview*. 2012. <https://www.w3.org/TR/owl2-overview/>

### Provenance, authorization, and permission-aware facts

- W3C. *PROV-O: The PROV Ontology*. 2013. <https://www.w3.org/TR/prov-o/>
- Pang, Ruoming, et al. *Zanzibar: Google’s Consistent, Global Authorization System*. USENIX Annual Technical Conference, 2019. <https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/>

### Governed enterprise agents

- NIST. *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. 2023. <https://www.nist.gov/itl/ai-risk-management-framework>
- NIST. *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)*. 2024. <https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf>
- Singapore Infocomm Media Development Authority. *Model AI Governance Framework for Agentic AI*. 2026. <https://www.imda.gov.sg/about-imda/emerging-technologies-and-research/artificial-intelligence>
