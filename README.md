<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/header-light.svg">
  <img alt="Samui — .NET 8 APIs on the back, React and Next.js on the front" src="assets/header-light.svg" width="100%">
</picture>

</div>

## About

Full-stack developer, mostly on **B2B products**: multi-tenant APIs in .NET and the interfaces that consume them.

I care about architecture that survives its second year — real boundaries between layers, typed contracts between back and front, and tests that fail for the right reason. Most of what I ship is private client work, so this profile is about *how* I build more than *what* is public.

## Stack

|  |  |
| --- | --- |
| **Backend** | C# · .NET 8 · ASP.NET Core · EF Core |
| **Architecture** | Clean Architecture · CQRS with MediatR · Result pattern (`ErrorOr`) · FluentValidation |
| **Data** | PostgreSQL · MySQL · Redis · S3 / MinIO |
| **Frontend** | TypeScript · Next.js 14 · React 18 · Tailwind · Radix / shadcn-ui |
| **Client state** | TanStack Query · Zustand · Zod · React Hook Form |
| **Testing** | xUnit · FluentAssertions · Moq · Vitest · Playwright |
| **Infra** | Docker · Cloudflare Workers (OpenNext) · Hangfire · JWT |

## How I build

- **Layers that mean something.** Domain, Application, Infrastructure and API are separate projects, not folders with good intentions.
- **Expected failures are values, not exceptions.** `ErrorOr<T>` all the way up, so the compiler keeps track of what can go wrong.
- **Contract first.** The OpenAPI spec generates the frontend client, so a breaking backend change breaks the build — not production.
- **Two kinds of tests.** Fast unit tests around the domain, integration tests for anything that touches a database.
- **Boring infrastructure.** Background jobs, object storage and caching solved with tools that already work.

## Currently

Building a **multi-tenant white-label SaaS** (.NET 8 + EF Core, background jobs, S3 storage, PDF generation) and a **Next.js 14 app on Cloudflare Workers** with i18n and an end-to-end Playwright suite.

<!-- Stats: a instancia publica do github-readme-stats estava em 503 e o perfil
     ainda nao tem repo publico com codigo, entao os cards mostrariam zero.
     Para religar, basta descomentar este bloco.

## Stats

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=SamuiArashi&show_icons=true&hide_border=true&hide_title=true&include_all_commits=true&count_private=true&theme=github_dark">
  <img alt="GitHub stats" src="https://github-readme-stats.vercel.app/api?username=SamuiArashi&show_icons=true&hide_border=true&hide_title=true&include_all_commits=true&count_private=true" height="150">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=SamuiArashi&layout=compact&hide_border=true&hide_title=true&langs_count=8&theme=github_dark">
  <img alt="Top languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=SamuiArashi&layout=compact&hide_border=true&hide_title=true&langs_count=8" height="150">
</picture>

</div>
-->

## Contact

[![Email](https://img.shields.io/badge/Email-0969da?style=for-the-badge&logoColor=white)](mailto:harlananjos@ai.facilitavitae.com.br)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/harlan-anjos-16a257286/)

---

<details>
<summary><b>🇧🇷 Em português</b></summary>

<br>

### Sobre

Desenvolvedor full-stack, principalmente em **produtos B2B**: APIs multi-tenant em .NET e as interfaces que consomem essas APIs.

Me importo com arquitetura que sobrevive ao segundo ano — fronteiras reais entre camadas, contratos tipados entre back e front, e testes que quebram pelo motivo certo. A maior parte do que eu entrego é trabalho privado para clientes, então este perfil fala mais de *como* eu construo do que do que está público.

### Stack

|  |  |
| --- | --- |
| **Backend** | C# · .NET 8 · ASP.NET Core · EF Core |
| **Arquitetura** | Clean Architecture · CQRS com MediatR · Result pattern (`ErrorOr`) · FluentValidation |
| **Dados** | PostgreSQL · MySQL · Redis · S3 / MinIO |
| **Frontend** | TypeScript · Next.js 14 · React 18 · Tailwind · Radix / shadcn-ui |
| **Estado no cliente** | TanStack Query · Zustand · Zod · React Hook Form |
| **Testes** | xUnit · FluentAssertions · Moq · Vitest · Playwright |
| **Infra** | Docker · Cloudflare Workers (OpenNext) · Hangfire · JWT |

### Como eu construo

- **Camadas que significam alguma coisa.** Domain, Application, Infrastructure e API são projetos separados, não pastas com boas intenções.
- **Falha esperada é valor, não exceção.** `ErrorOr<T>` até o topo, para o compilador lembrar o que pode dar errado.
- **Contrato primeiro.** A spec OpenAPI gera o client do frontend — mudança quebrando no backend quebra o build, não a produção.
- **Dois tipos de teste.** Teste unitário rápido no domínio, teste de integração em tudo que encosta no banco.
- **Infra sem graça.** Jobs em background, storage de objeto e cache resolvidos com ferramenta que já funciona.

### Agora

Construindo um **SaaS white-label multi-tenant** (.NET 8 + EF Core, jobs em background, storage S3, geração de PDF) e um **app Next.js 14 na Cloudflare Workers**, com i18n e suíte end-to-end em Playwright.

</details>
