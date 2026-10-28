# Visão Artificial — API Central (Nuvem)

> Este repositório faz parte do ecossistema **Visão Artificial**. Ele atua como o núcleo de comunicação e roteamento. Para ver as outras pontas, consulte os repositórios da [API Local de IA](https://github.com/Thurzinfs/vision-artificial-local) e do [Aplicativo Mobile (Flutter)](https://github.com/Thurzinfs/vision-artificial-mobile).

---

## Sobre, Motivo e Objetivo

### O Problema (O Desafio)
Em sistemas de visão computacional distribuídos em tempo real (envolvendo hardware de captura, processamento pesado de inteligência artificial e aplicativos móveis de acessibilidade), um dos maiores gargalos é o **roteamento e a sincronização de dados**. Sem uma central robusta, a comunicação entre dispositivos de borda, servidores de IA e clientes finais torna-se instável, lenta e difícil de escalar.

### A Solução e o Objetivo da API Central
Esta API em nuvem atua como o **diretor de tráfego** do ecossistema. O seu objetivo é intermediar de forma assíncrona e assíncrona o fluxo de dados em tempo real:
1. **Recebimento:** Coleta os frames enviados pelo hardware via **MQTT**.
2. **Encaminhamento:** Disponibiliza esses dados para a **API Local de IA** processar.
3. **Distribuição:** Recebe os resultados processados e os encaminha via **WebSocket** para o **Aplicativo Mobile**, garantindo uma comunicação rápida, limpa e desacoplada.

---

## Resumo do Ecossistema

Para que o projeto funcione em harmonia, a arquitetura é dividida em três frentes independentes:

| Componente | Repositório | Papel Principal |
|---|---|---|
| **Hardware** | *(Repositório Externo)* | Captura o ambiente e transmite os dados brutos. |
| **API Central (Nuvem)** | *Este repositório* | Gerencia rotas, conexões MQTT/WebSocket e distribui os dados. |
| **API Local de IA** | [Link] | Processa as imagens através de modelos de visão computacional. |
| **App Mobile** | [Link] | Consome os dados e os converte em acessibilidade por voz (TTS). |

---
---

## Método

O fluxo de comunicação implementado é:

1. A API conecta-se ao broker MQTT e assina o tópico configurado em `BROKER_TOPIC`.
2. Ao receber uma mensagem, extrai o identificador UUID do dispositivo do último segmento do tópico e encaminha os bytes do frame ao caso de uso de processamento.
3. O caso de uso envia o frame ao cliente local conectado pelo WebSocket. A mensagem binária enviada é composta pelos 16 bytes do UUID seguidos pelos bytes do frame.
4. Aplicações conectam-se ao WebSocket associado ao dispositivo. Quando um cliente local envia à API um texto JSON com o campo `device`, o payload é encaminhado às aplicações conectadas para esse UUID.

---

### Interfaces disponíveis

| Interface | Caminho/Configuração | Uso |
| --- | --- | --- |
| MQTT | `BROKER_HOST` e `BROKER_TOPIC` | Receber frames; o tópico da mensagem deve terminar com o UUID do dispositivo. |
| WebSocket local | `/ws/local/{client}` | Conectar um cliente local usando seu UUID. |
| WebSocket da aplicação | `/ws/app/{device}` | Conectar uma aplicação ao dispositivo usando seu UUID. |

O `root_path` configurado pela aplicação é `/api/v1`. Em ambientes com proxy reverso, configure o encaminhamento para considerar esse prefixo.

---

## Tecnologia

- **Python 3.12+** e **asyncio** para execução assíncrona.
- **FastAPI** para a aplicação e os endpoints WebSocket.
- **aiomqtt** para a conexão assíncrona ao broker MQTT.
- **dotenv** para carregar configurações de ambiente.
- **uv** para gerenciamento e sincronização das dependências, com `uv.lock`.
- **Docker** com imagem multi-stage baseada em `python:3.12-slim`.

---

## Arquitetura

O código é dividido por responsabilidades, seguindo uma organização em camadas:

```text
app/
├── api/
│   ├── dependencies/  # Construção e injeção de dependências
│   └── handlers/      # Endpoints e integração com FastAPI
├── application/
│   └── use_cases/     # Fluxos de processamento de frames e resultados
├── domain/
│   ├── contracts/     # Contratos dos adaptadores
│   └── entities/      # Entidades do domínio
└── infrastructure/
    └── adapters/      # Implementações MQTT e WebSocket
config/
└── settings.py        # Configuração por variáveis de ambiente
```

Em tempo de execução, a aplicação cria os adaptadores MQTT e WebSocket, inicia o listener MQTT no ciclo de vida do FastAPI e usa os casos de uso para encaminhar mensagens. Os contratos do domínio isolam os casos de uso das implementações concretas dos adaptadores.

---

## Boas práticas e princípios

- Separação de responsabilidades entre API, aplicação, domínio e infraestrutura.
- Contratos abstratos para os adaptadores de comunicação.
- Injeção de dependências nos handlers e casos de uso.
- Configuração externa por variáveis de ambiente, sem exigir valores fixos no código.
- Uso de UUID para associar conexões aos dispositivos.
- Imagem Docker multi-stage e execução do processo como usuário não privilegiado.

---

## Roadmap e estado atual

### Feito

- [x] Inicialização da API FastAPI com ciclo de vida assíncrono.
- [x] Conexão e assinatura de tópico MQTT configurável.
- [x] Encaminhamento de frames recebidos para clientes locais conectados via WebSocket.
- [x] WebSockets separados para clientes locais e aplicações, associados a UUIDs.
- [x] Encaminhamento de payloads de resultados para aplicações conectadas ao dispositivo.
- [x] Configuração do broker e do tópico por variáveis de ambiente.
- [x] Empacotamento da aplicação em Docker.

### Próximas evoluções sugeridas

- [ ] Adicionar testes automatizados para os casos de uso e adaptadores.
- [ ] Documentar e validar formalmente o formato dos frames e dos resultados.
- [ ] Adicionar autenticação e autorização às conexões.
- [ ] Melhorar logs, métricas e monitoramento do broker e das conexões.
- [ ] Definir e documentar o processo de implantação na nuvem.

As próximas evoluções são sugestões; não estão implementadas no estado atual do repositório.

---

## Executar localmente

1. Copie `.env.example` para `.env` e preencha as configurações do broker:

   ```env
   BROKER_HOST=seu-host-mqtt
   BROKER_TOPIC=seu-topico
   ```

2. Sincronize as dependências e inicie a API:

   ```bash
   uv sync
   uv run uvicorn main:app --reload
   ```

---

## Executar com Docker

Com o arquivo `.env` preenchido, construa e execute a imagem:

```bash
docker build -t cloud-visao-artificial .
docker run --env-file .env -p 8000:8000 cloud-visao-artificial
```

---

## Contato

- **Autor** — Arthur França Silva
- **E-mail** — arthurfranca.dev@gmail.com
- **GitHub** — [@Thurzinfs](https://github.com/Thurzinfs)

---

<div align="center">
  Desenvolvido com ❤️ por <a href="https://github.com/Thurzinfs">Arthur França Silva</a>
</div>