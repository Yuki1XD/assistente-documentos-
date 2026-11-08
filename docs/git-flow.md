# Fluxo Git recomendado

1. Criar `main` como branch estável.
2. Criar `develop` a partir de `main`.
3. Para cada Issue, criar uma branch a partir de `develop`, por exemplo:
   `feature/03-health-endpoint`.
4. Fazer commits pequenos com Conventional Commits:
   `feat: adiciona endpoint de saúde`
   `docs: adiciona casos de uso`
   `test: adiciona teste do health check`
5. Abrir Pull Request da feature para `develop`, revisar e integrar.
6. Quando uma versão estiver validada, abrir PR de `develop` para `main`.
7. Criar tag anotada:
   `git tag -a v0.1.0 -m "Versão inicial"`
8. Enviar a tag:
   `git push origin v0.1.0`

Não faça commits diretamente em `main`. Substitua `N` pelo número real da Issue no texto `Closes #N` do Pull Request.
