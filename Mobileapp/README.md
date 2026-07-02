# Jacu — Aplicativo de controle

Código de funcionamento do aplicativo de controle e monitoramento do robô
agrícola Jacu. Desenvolvido em React Native (Expo), é responsável pela
interface entre o operador e o robô: painel de status, controle manual e
visualização do talhão.

## Funcionalidades

### Painel
Tela inicial com o status geral do robô: nível de bateria, modo de operação
(autônomo/manual), área do talhão já coberta e histórico de eventos/alertas
recentes.

### Controle Manual
Permite assumir o controle direto do robô: liga/desliga do motor, seleção
de velocidade, joystick virtual para direção e botão de parada de
emergência. Inclui também o painel de câmeras (frontal, traseira, esquerda
e direita) para apoiar manobras, especialmente em marcha à ré.

### Mapa do Talhão
Visualização das fileiras já percorridas, posição atual do robô,
coordenadas e tempo de operação.

## Câmeras

As câmeras são transmitidas por dispositivos conectados à mesma rede local
do robô, via streaming de vídeo sobre Wi-Fi. Para configurar:

1. No dispositivo que servirá de câmera, inicie a transmissão de vídeo
   (ex: pelo app IP Webcam, no caso de um celular Android) e anote o
   endereço gerado — algo como `http://192.168.0.15:8080/video`.
2. No app, na tela de Controle Manual, toque no ícone de engrenagem ao
   lado das abas de câmera.
3. Cole o endereço no campo correspondente ao ângulo (Frontal, Traseira,
   Esquerda ou Direita) e salve.

Todos os dispositivos precisam estar na mesma rede local para que a
transmissão funcione.

## Como rodar

Pré-requisitos: Node.js instalado e o app Expo Go no celular de testes.

```bash
npm install
npx expo install --fix
npx expo start
```

Escaneie o QR code exibido no terminal com o Expo Go (Android) ou a câmera
nativa do iPhone.

## Estrutura do projeto

```
jacu-app/
├── App.js                      # navegação em abas
├── src/
│   ├── theme.js                 # cores e tipografia
│   ├── components/
│   │   ├── RadialGauge.js       # indicador circular (bateria)
│   │   ├── StatusPill.js        # indicador de conexão
│   │   ├── Card.js              # cartão padrão de conteúdo
│   │   ├── TopoBackground.js    # textura de fundo
│   │   ├── Joystick.js          # joystick virtual de direção
│   │   ├── CameraFeed.js        # exibição de vídeo ao vivo por câmera
│   │   └── CameraSettingsModal.js # configuração dos endereços de câmera
│   ├── hooks/
│   │   └── useCameraFeeds.js    # persistência dos endereços de câmera
│   └── screens/
│       ├── DashboardScreen.js
│       ├── ControlScreen.js
│       └── FieldMapScreen.js
```

## Telemetria

Os valores de bateria, coordenadas, área coberta e histórico de eventos
são definidos localmente na interface. Quando a comunicação com os
sensores do robô (via ROS2/Raspberry Pi) estiver definida, esses pontos
devem ser substituídos por leituras em tempo real, mantendo a mesma
estrutura de tela.

## Integração com ROS2 / Raspberry Pi

A comunicação entre este aplicativo e o robô ainda depende da definição de
uma ponte de comunicação (rosbridge via WebSocket, MQTT, ou uma API REST
customizada rodando no Raspberry Pi). Assim que essa decisão for tomada
pelo time, os dados fixos das telas e os comandos do joystick/motor devem
ser conectados aos tópicos ou endpoints correspondentes.
