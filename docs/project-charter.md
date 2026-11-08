# Project Charter — Assistente Inteligente de Documentos

## 1. Justificativa
Pessoas que estudam ou trabalham precisam consultar documentos extensos para encontrar informações específicas. Fazer isso manualmente pode levar tempo. O sistema pretende facilitar essa tarefa permitindo enviar um documento, gerar um resumo e fazer perguntas sobre o conteúdo.

## 2. Visão do produto
Criar uma API simples que receba documentos PDF ou TXT e ajude o usuário a compreender e localizar informações presentes nesses arquivos, apresentando respostas relacionadas ao conteúdo enviado.

## 3. Objetivos SMART
1. **Até o fim da primeira etapa**, disponibilizar uma API FastAPI com endpoint de saúde e documentação automática acessível pelo navegador.
2. **Até a segunda etapa**, permitir o envio e a validação de arquivos PDF e TXT, rejeitando formatos não aceitos.
3. **Até a terceira etapa**, extrair e armazenar o texto dos documentos enviados.
4. **Até a quarta etapa**, disponibilizar resumo e perguntas e respostas sobre o conteúdo de um documento, com indicação da origem da informação.
5. **Ao final do projeto acadêmico**, documentar requisitos, casos de uso, histórias de usuário e tarefas de desenvolvimento no GitHub.

## 4. Escopo

### Dentro do escopo
- API REST em Python com FastAPI.
- Recebimento de arquivos PDF e TXT.
- Validação de formato e tamanho.
- Extração e armazenamento do texto.
- Geração de resumos por serviço de IA.
- Respostas a perguntas baseadas no documento.
- Documentação e testes básicos.

### Fora do escopo
- Aplicativo mobile.
- Interface web completa.
- Edição de arquivos enviados.
- Suporte inicial a áudio e vídeo.
- Garantia de leitura de PDFs protegidos ou digitalizados sem OCR.
- Treinamento de um modelo próprio de inteligência artificial.

## 5. Stakeholders e público-alvo
- **Usuários:** estudantes, professores e profissionais que consultam documentos.
- **Equipe de desenvolvimento:** responsável por planejar, implementar, testar e documentar o sistema.
- **Professor/avaliador:** acompanha a organização do projeto e verifica as entregas acadêmicas.

## 6. Premissas e restrições
- O usuário terá acesso à internet para utilizar um provedor de IA externo, quando essa integração for implementada.
- O projeto será desenvolvido inicialmente como API.
- O uso de serviços externos poderá depender de limites e chaves de acesso.
- Documentos enviados podem conter informações privadas; o sistema deverá tratar esses arquivos com cuidado.

## 7. Critérios gerais de sucesso
- A API inicia localmente seguindo o README.
- Arquivos aceitos são validados e processados.
- O usuário consegue obter resumo e respostas baseadas no documento.
- A documentação permite entender o objetivo e o funcionamento planejado.
