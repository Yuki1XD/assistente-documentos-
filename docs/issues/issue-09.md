# Configurar banco de dados

**Labels sugeridas:** `setup, feature, priority: high`

## Descrição
Preparar conexão com PostgreSQL e configuração por variáveis de ambiente.

## Critérios de aceitação
- [ ] Credenciais não ficam no código.
- [ ] Conexão pode ser configurada por ambiente.
- [ ] Falha de conexão gera erro tratado.

## Rastreabilidade
RF06, RNF05

## Definition of Done
- [ ] Código revisado.
- [ ] Testes relevantes executados.
- [ ] Documentação atualizada, quando necessário.
- [ ] Pull Request aberto para `develop`.
- [ ] Pull Request referencia esta Issue com `Closes #N`.
