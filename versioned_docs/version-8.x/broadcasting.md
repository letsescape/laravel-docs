<!-- # Broadcasting -->
# Broadcasting

- [Introduction](#introduction)
- [Server Side Installation](#server-side-installation)
    - [Configuration](#configuration)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
    - [Open Source Alternatives](#open-source-alternatives)
- [Client Side Installation](#client-side-installation)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [Concept Overview](#concept-overview)
    - [Using An Example Application](#using-example-application)
- [Defining Broadcast Events](#defining-broadcast-events)
    - [Broadcast Name](#broadcast-name)
    - [Broadcast Data](#broadcast-data)
    - [Broadcast Queue](#broadcast-queue)
    - [Broadcast Conditions](#broadcast-conditions)
    - [Broadcasting & Database Transactions](#broadcasting-and-database-transactions)
- [Authorizing Channels](#authorizing-channels)
    - [Defining Authorization Routes](#defining-authorization-routes)
    - [Defining Authorization Callbacks](#defining-authorization-callbacks)
    - [Defining Channel Classes](#defining-channel-classes)
- [Broadcasting Events](#broadcasting-events)
    - [Only To Others](#only-to-others)
    - [Customizing The Connection](#customizing-the-connection)
- [Receiving Broadcasts](#receiving-broadcasts)
    - [Listening For Events](#listening-for-events)
    - [Leaving A Channel](#leaving-a-channel)
    - [Namespaces](#namespaces)
- [Presence Channels](#presence-channels)
    - [Authorizing Presence Channels](#authorizing-presence-channels)
    - [Joining Presence Channels](#joining-presence-channels)
    - [Broadcasting To Presence Channels](#broadcasting-to-presence-channels)
- [Model Broadcasting](#model-broadcasting)
    - [Model Broadcasting Conventions](#model-broadcasting-conventions)
    - [Listening For Model Broadcasts](#listening-for-model-broadcasts)
- [Client Events](#client-events)
- [Notifications](#notifications)

<a name="introduction"></a>

<!-- ## Introduction -->
## Introduction

<!-- In many modern web applications, WebSockets are used to implement realtime, live-updating user interfaces. When some data is updated on the server, a message is typically sent over a WebSocket connection to be handled by the client. WebSockets provide a more efficient alternative to continually polling your application's server for data changes that should be reflected in your UI. -->
최근 웹 애플리케이션에서는 실시간(Realtime), 라이브 업데이트 UI를 구현하기 위해 WebSocket을 널리 사용합니다. 서버에서 데이터가 변경되면, 일반적으로 WebSocket 연결을 통해 메시지가 전송되며, 클라이언트는 이를 받아 UI를 즉시 갱신할 수 있습니다. 이러한 방식은 데이터 변경 사항을 확인하기 위해 애플리케이션 서버에 반복적으로 요청(polling)하는 것보다 훨씬 효율적입니다.

<!-- For example, imagine your application is able to export a user's data to a CSV file and email it to them. However, creating this CSV file takes several minutes so you choose to create and mail the CSV within a [queued job](/docs/8.x/queues). When the CSV has been created and mailed to the user, we can use event broadcasting to dispatch a `App\Events\UserDataExported` event that is received by our application's JavaScript. Once the event is received, we can display a message to the user that their CSV has been emailed to them without them ever needing to refresh the page. -->
예를 들어, 여러분의 애플리케이션이 사용자의 데이터를 CSV 파일로 내보내고 해당 파일을 이메일로 발송하는 기능을 제공한다고 가정해보겠습니다. CSV 파일 생성에는 몇 분이 소요될 수 있으므로, 이 작업을 [queued job](/docs/8.x/queues)으로 처리한다고 해봅니다. CSV 파일이 완성되어 사용자의 이메일로 발송되면, 우리는 `App\Events\UserDataExported` 이벤트를 브로드캐스팅하여 애플리케이션의 JavaScript에서 수신하도록 할 수 있습니다. 이 이벤트를 수신하면, 사용자는 페이지를 새로고침하지 않아도 CSV가 이메일로 전송되었다는 안내 메시지를 실시간으로 확인할 수 있습니다.

<!-- To assist you in building these types of features, Laravel makes it easy to "broadcast" your server-side Laravel [events](/docs/8.x/events) over a WebSocket connection. Broadcasting your Laravel events allows you to share the same event names and data between your server-side Laravel application and your client-side JavaScript application. -->
이와 같은 기능을 쉽게 구현할 수 있도록, Laravel은 서버 사이드의 [events](/docs/8.x/events)를 WebSocket 연결을 통해 간단하게 “브로드캐스트”할 수 있는 기능을 제공합니다. Laravel 이벤트를 브로드캐스팅하면 서버 사이드의 Laravel 애플리케이션과 클라이언트 사이드의 JavaScript 애플리케이션 모두에서 동일한 이벤트 이름과 데이터를 손쉽게 공유할 수 있습니다.

<!-- The core concepts behind broadcasting are simple: clients connect to named channels on the frontend, while your Laravel application broadcasts events to these channels on the backend. These events can contain any additional data you wish to make available to the frontend. -->
브로드캐스팅의 핵심 개념은 단순합니다. 클라이언트는 프론트엔드에서 정의된 채널에 접속하고, Laravel 애플리케이션은 백엔드에서 해당 채널로 이벤트를 브로드캐스트합니다. 이 이벤트에는 프론트엔드에서 사용할 수 있도록 원하는 추가 데이터를 포함할 수 있습니다.

<a name="supported-drivers"></a>

<!-- #### Supported Drivers -->
#### Supported Drivers

<!-- By default, Laravel includes two server-side broadcasting drivers for you to choose from: [Pusher Channels](https://pusher.com/channels) and [Ably](https://ably.io). However, community driven packages such as [laravel-websockets](https://beyondco.de/docs/laravel-websockets/getting-started/introduction) and [soketi](https://docs.soketi.app/) provide additional broadcasting drivers that do not require commercial broadcasting providers. -->
Laravel은 기본적으로 두 가지 서버 사이드 브로드캐스팅 드라이버를 제공합니다: [Pusher Channels](https://pusher.com/channels)과 [Ably](https://ably.io)가 이에 해당합니다. 그 외에도, 커뮤니티에서 제공하는 [laravel-websockets](https://beyondco.de/docs/laravel-websockets/getting-started/introduction), [soketi](https://docs.soketi.app/) 등은 상용 브로드캐스팅 서비스에 의존하지 않아도 사용할 수 있는 브로드캐스팅 드라이버를 제공합니다.

> [!TIP]
> 이벤트 브로드캐스팅을 시작하기 전에, Laravel [events and listeners](/docs/8.x/events) 문서를 먼저 읽어보시기 바랍니다.

<a name="server-side-installation"></a>

<!-- ## Server Side Installation -->
## Server Side Installation

<!-- To get started using Laravel's event broadcasting, we need to do some configuration within the Laravel application as well as install a few packages. -->
Laravel의 이벤트 브로드캐스팅을 사용하려면, Laravel 애플리케이션 내에서 몇 가지 설정을 해주고, 일부 패키지를 설치해야 합니다.

<!-- Event broadcasting is accomplished by a server-side broadcasting driver that broadcasts your Laravel events so that Laravel Echo (a JavaScript library) can receive them within the browser client. Don't worry - we'll walk through each part of the installation process step-by-step. -->
이벤트 브로드캐스팅은 서버 사이드 ‘브로드캐스트 드라이버’를 통해 이루어집니다. 이 드라이버가 Laravel 이벤트를 브라우저의 JavaScript 라이브러리인 Laravel Echo에서 수신할 수 있게 브로드캐스트해줍니다. 걱정하지 마세요! 설치 과정은 하나씩 차근차근 안내해드리니 쉽게 따라오실 수 있습니다.

<a name="configuration"></a>

<!-- ### Configuration -->
### Configuration

<!-- All of your application's event broadcasting configuration is stored in the `config/broadcasting.php` configuration file. Laravel supports several broadcast drivers out of the box: [Pusher Channels](https://pusher.com/channels), [Redis](/docs/8.x/redis), and a `log` driver for local development and debugging. Additionally, a `null` driver is included which allows you to totally disable broadcasting during testing. A configuration example is included for each of these drivers in the `config/broadcasting.php` configuration file. -->
애플리케이션의 이벤트 브로드캐스트와 관련된 모든 설정은 `config/broadcasting.php` 설정 파일에 저장됩니다. Laravel은 기본적으로 [Pusher Channels](https://pusher.com/channels), [Redis](/docs/8.x/redis), 그리고 로컬 개발 및 디버깅용 `log` 드라이버 등 여러 브로드캐스트 드라이버를 지원합니다. 또한, 테스트 환경에서 브로드캐스팅을 완전히 비활성화하고 싶을 때 사용할 수 있는 `null` 드라이버도 포함되어 있습니다. 각 드라이버에 대한 설정 예시는 `config/broadcasting.php` 파일에 미리 준비되어 있습니다.

<a name="broadcast-service-provider"></a>

<!-- #### Broadcast Service Provider -->
#### Broadcast Service Provider

<!-- Before broadcasting any events, you will first need to register the `App\Providers\BroadcastServiceProvider`. In new Laravel applications, you only need to uncomment this provider in the `providers` array of your `config/app.php` configuration file. This `BroadcastServiceProvider` contains the code necessary to register the broadcast authorization routes and callbacks. -->
이벤트를 브로드캐스트하기 전에, 먼저 `App\Providers\BroadcastServiceProvider`를 등록해야 합니다. 새로운 Laravel 애플리케이션에서는, 이 프로바이더가 `config/app.php` 파일의 `providers` 배열에 주석 처리되어 있으니 해당 주석만 해제하면 됩니다. 이 `BroadcastServiceProvider`는 브로드캐스트 인가(authorization) 라우트 및 콜백을 등록하는 데 필요한 코드를 포함하고 있습니다.

<a name="queue-configuration"></a>

<!-- #### Queue Configuration -->
#### Queue Configuration

<!-- You will also need to configure and run a [queue worker](/docs/8.x/queues). All event broadcasting is done via queued jobs so that the response time of your application is not seriously affected by events being broadcast. -->
또한, [queue worker](/docs/8.x/queues)를 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐에 등록된 작업(queued job)을 통해 이루어지므로, 이벤트 브로드캐스트로 인해 애플리케이션 응답속도에 영향을 미치지 않게 할 수 있습니다.

<a name="pusher-channels"></a>

<!-- ### Pusher Channels -->
### Pusher Channels

<!-- If you plan to broadcast your events using [Pusher Channels](https://pusher.com/channels), you should install the Pusher Channels PHP SDK using the Composer package manager: -->
이벤트를 [Pusher Channels](https://pusher.com/channels)로 브로드캐스트할 계획이라면, Composer 패키지 매니저를 사용하여 Pusher Channels PHP SDK를 설치해야 합니다:

```
composer require pusher/pusher-php-server
```

<!-- Next, you should configure your Pusher Channels credentials in the `config/broadcasting.php` configuration file. An example Pusher Channels configuration is already included in this file, allowing you to quickly specify your key, secret, and application ID. Typically, these values should be set via the `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`, and `PUSHER_APP_ID` [environment variables](/docs/8.x/configuration#environment-configuration): -->
그 다음, `config/broadcasting.php` 설정 파일에 Pusher Channels 인증 정보를 추가해줍니다. 이 파일에는 이미 Pusher Channels 설정 예시가 포함되어 있으므로, 여러분은 키(key), 시크릿(secret), 애플리케이션 ID만 지정해주면 빠르게 시작할 수 있습니다. 일반적으로 이러한 값들은 `PUSHER_APP_KEY`, `PUSHER_APP_SECRET`, `PUSHER_APP_ID`와 같은 [environment variables](/docs/8.x/configuration#environment-configuration)를 통해 설정합니다:

```
PUSHER_APP_ID=your-pusher-app-id
PUSHER_APP_KEY=your-pusher-key
PUSHER_APP_SECRET=your-pusher-secret
PUSHER_APP_CLUSTER=mt1
```

<!-- The `config/broadcasting.php` file's `pusher` configuration also allows you to specify additional `options` that are supported by Channels, such as the cluster. -->
`config/broadcasting.php` 파일의 `pusher` 설정 내에는 cluster 등 Pusher Channels에서 지원하는 추가 `options`도 지정할 수 있습니다.

<!-- Next, you will need to change your broadcast driver to `pusher` in your `.env` file: -->
설정이 끝나면, `.env` 파일에서 브로드캐스트 드라이버를 `pusher`로 변경해야 합니다:

```
BROADCAST_DRIVER=pusher
```

<!-- Finally, you are ready to install and configure [Laravel Echo](#client-side-installation), which will receive the broadcast events on the client-side. -->
이제 [Laravel Echo](#client-side-installation)를 설치하고 설정하면, 클라이언트에서 브로드캐스트 이벤트를 수신할 준비가 완료됩니다.

<a name="pusher-compatible-open-source-alternatives"></a>

<!-- #### Open Source Pusher Alternatives -->
#### Open Source Pusher Alternatives

<!-- The [laravel-websockets](https://github.com/beyondcode/laravel-websockets) and [soketi](https://docs.soketi.app/) packages provide Pusher compatible WebSocket servers for Laravel. These packages allow you to leverage the full power of Laravel broadcasting without a commercial WebSocket provider. For more information on installing and using these packages, please consult our documentation on [open source alternatives](#open-source-alternatives). -->
[laravel-websockets](https://github.com/beyondcode/laravel-websockets)와 [soketi](https://docs.soketi.app/) 패키지는 Laravel에서 사용할 수 있는 Pusher 호환 WebSocket 서버를 제공합니다. 이 패키지들을 활용하면 상용 WebSocket 서비스 없이도 Laravel 브로드캐스팅의 모든 기능을 자유롭게 사용할 수 있습니다. 설치 및 사용법에 대한 더 자세한 내용은 [open source alternatives](#open-source-alternatives) 문서를 참고하시기 바랍니다.

<a name="ably"></a>

<!-- ### Ably -->
### Ably

<!-- If you plan to broadcast your events using [Ably](https://ably.io), you should install the Ably PHP SDK using the Composer package manager: -->
이벤트를 [Ably](https://ably.io)로 브로드캐스트하려는 경우, Composer 패키지 매니저를 사용해 Ably PHP SDK를 설치해야 합니다:

```
composer require ably/ably-php
```

<!-- Next, you should configure your Ably credentials in the `config/broadcasting.php` configuration file. An example Ably configuration is already included in this file, allowing you to quickly specify your key. Typically, this value should be set via the `ABLY_KEY` [environment variable](/docs/8.x/configuration#environment-configuration): -->
그 다음, `config/broadcasting.php` 설정 파일에 Ably 인증 정보를 추가해야 합니다. 이 파일에도 이미 Ably 설정 예시가 포함되어 있어, key만 빠르게 지정해주면 됩니다. 일반적으로 이 값은 `ABLY_KEY` [environment variable](/docs/8.x/configuration#environment-configuration)로 설정합니다:

```
ABLY_KEY=your-ably-key
```

<!-- Next, you will need to change your broadcast driver to `ably` in your `.env` file: -->
마찬가지로, `.env` 파일에서 브로드캐스트 드라이버를 `ably`로 변경해야 합니다:

```
BROADCAST_DRIVER=ably
```

<!-- Finally, you are ready to install and configure [Laravel Echo](#client-side-installation), which will receive the broadcast events on the client-side. -->
이제 [Laravel Echo](#client-side-installation)를 설치하고 설정하면, 클라이언트에서 브로드캐스트 이벤트를 받을 준비가 완료됩니다.

<a name="open-source-alternatives"></a>

<!-- ### Open Source Alternatives -->
### Open Source Alternatives

<a name="open-source-alternatives-php"></a>

<!-- #### PHP -->
#### PHP

<!-- The [laravel-websockets](https://github.com/beyondcode/laravel-websockets) package is a pure PHP, Pusher compatible WebSocket package for Laravel. This package allows you to leverage the full power of Laravel broadcasting without a commercial WebSocket provider. For more information on installing and using this package, please consult its [official documentation](https://beyondco.de/docs/laravel-websockets). -->
[laravel-websockets](https://github.com/beyondcode/laravel-websockets) 패키지는 Laravel용 순수 PHP로 작성된 Pusher 호환 WebSocket 패키지입니다. 이 패키지를 사용하면 상용 WebSocket 서비스 없이 Laravel 브로드캐스팅의 모든 기능을 자유롭게 활용할 수 있습니다. 설치 및 사용 방법에 대해서는 [official documentation](https://beyondco.de/docs/laravel-websockets)를 참고하세요.

<a name="open-source-alternatives-node"></a>

<!-- #### Node -->
#### Node

<!-- [Soketi](https://github.com/soketi/soketi) is a Node based, Pusher compatible WebSocket server for Laravel. Under the hood, Soketi utilizes µWebSockets.js for extreme scalability and speed. This package allows you to leverage the full power of Laravel broadcasting without a commercial WebSocket provider. For more information on installing and using this package, please consult its [official documentation](https://docs.soketi.app/). -->
[Soketi](https://github.com/soketi/soketi)는 Node 기반, Pusher 호환 WebSocket 서버로 µWebSockets.js를 활용하여 매우 높은 확장성과 속도를 자랑합니다. 이 역시 상용 WebSocket 서비스 없이도 Laravel 브로드캐스팅의 모든 기능을 활용할 수 있습니다. 설치 및 사용법에 대해서는 [official documentation](https://docs.soketi.app/)를 참고하세요.

<a name="client-side-installation"></a>

<!-- ## Client Side Installation -->
## Client Side Installation

<a name="client-pusher-channels"></a>

<!-- ### Pusher Channels -->
### Pusher Channels

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. You may install Echo via the NPM package manager. In this example, we will also install the `pusher-js` package since we will be using the Pusher Channels broadcaster: -->
[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스토가 브로드캐스트하는 이벤트를 손쉽게 구독하고 수신할 수 있게 해주는 JavaScript 라이브러리입니다. Echo는 NPM 패키지 매니저로 설치할 수 있습니다. 여기서는 Pusher Channels 브로드캐스터를 사용할 것이므로, `pusher-js` 패키지도 함께 설치합니다:

```bash
npm install --save-dev laravel-echo pusher-js
```

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's JavaScript. A great place to do this is at the bottom of the `resources/js/bootstrap.js` file that is included with the Laravel framework. By default, an example Echo configuration is already included in this file - you simply need to uncomment it: -->
Echo 설치가 완료되면, 여러분의 애플리케이션 JavaScript에서 새로운 Echo 인스턴스를 생성하면 됩니다. 보통 이는 Laravel 프레임워크에 기본 포함된 `resources/js/bootstrap.js` 파일 하단에 추가하는 것이 가장 좋습니다. 기본적으로 이 파일에는 Echo 설정 예시가 이미 주석 처리되어 있으니, 주석을 해제하기만 하면 됩니다:

```js
import Echo from 'laravel-echo';

window.Pusher = require('pusher-js');

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: process.env.MIX_PUSHER_APP_KEY,
    cluster: process.env.MIX_PUSHER_APP_CLUSTER,
    forceTLS: true
});
```

<!-- Once you have uncommented and adjusted the Echo configuration according to your needs, you may compile your application's assets: -->
Echo 설정을 주석 해제하고, 프로젝트 환경에 맞게 필요한 부분을 조정했다면, 애플리케이션 에셋을 컴파일합니다:

```
npm run dev
```

> [!TIP]
> 애플리케이션의 JavaScript 에셋 컴파일 방법에 대해서는 [Laravel Mix](/docs/8.x/mix) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>

<!-- #### Using An Existing Client Instance -->
#### Using An Existing Client Instance

<!-- If you already have a pre-configured Pusher Channels client instance that you would like Echo to utilize, you may pass it to Echo via the `client` configuration option: -->
이미 사전에 설정된 Pusher Channels 클라이언트 인스턴스가 있다면, Echo에 `client` 설정 옵션으로 전달해 사용할 수 있습니다:

```js
import Echo from 'laravel-echo';

const client = require('pusher-js');

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: 'your-pusher-channels-key',
    client: client
});
```

<a name="client-ably"></a>

<!-- ### Ably -->
### Ably

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. You may install Echo via the NPM package manager. In this example, we will also install the `pusher-js` package. -->
[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스트 드라이버가 브로드캐스트하는 이벤트를 손쉽게 구독하고 수신할 수 있는 JavaScript 라이브러리입니다. Echo는 NPM 패키지 매니저로 설치할 수 있습니다. 이 예제에서도 `pusher-js` 패키지를 함께 설치합니다.

<!-- You may wonder why we would install the `pusher-js` JavaScript library even though we are using Ably to broadcast our events. Thankfully, Ably includes a Pusher compatibility mode which lets us use the Pusher protocol when listening for events in our client-side application: -->
혹시 Ably 전용인데도 불구하고 왜 `pusher-js` JavaScript 라이브러리를 설치해야 하는지 궁금하실 수 있습니다. 다행히도 Ably에는 Pusher 호환 모드가 있어서, 클라이언트 애플리케이션에서 Pusher 프로토콜을 사용해 이벤트를 수신할 수 있도록 해줍니다.

```bash
npm install --save-dev laravel-echo pusher-js
```

<!-- **Before continuing, you should enable Pusher protocol support in your Ably application settings. You may enable this feature within the "Protocol Adapter Settings" portion of your Ably application's settings dashboard.** -->
**계속 진행하기 전에, Ably 애플리케이션 설정의 "Protocol Adapter Settings" 섹션에서 Pusher 프로토콜 지원을 활성화해주셔야 합니다.**

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's JavaScript. A great place to do this is at the bottom of the `resources/js/bootstrap.js` file that is included with the Laravel framework. By default, an example Echo configuration is already included in this file; however, the default configuration in the `bootstrap.js` file is intended for Pusher. You may copy the configuration below to transition your configuration to Ably: -->
Echo 설치가 완료되면, 여러분의 애플리케이션 JavaScript에서 새로운 Echo 인스턴스를 생성합니다. 보통 `resources/js/bootstrap.js` 파일 하단에 추가하는 것이 가장 좋습니다. 이 파일에는 기본적으로 Echo 설정 예제가 포함되어 있지만, `bootstrap.js` 내 기본 설정은 Pusher용이니, 아래 설정처럼 Ably에 맞게 복사해 변경해주면 됩니다:

```js
import Echo from 'laravel-echo';

window.Pusher = require('pusher-js');

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: process.env.MIX_ABLY_PUBLIC_KEY,
    wsHost: 'realtime-pusher.ably.io',
    wsPort: 443,
    disableStats: true,
    encrypted: true,
});
```

<!-- Note that our Ably Echo configuration references a `MIX_ABLY_PUBLIC_KEY` environment variable. This variable's value should be your Ably public key. Your public key is the portion of your Ably key that occurs before the `:` character. -->
참고로, 이 예제의 Ably Echo 설정에서 사용된 `MIX_ABLY_PUBLIC_KEY` 환경 변수 값은 Ably의 public key여야 하며, Ably 전체 키 중 `:` 문자 앞 부분에 해당합니다.

<!-- Once you have uncommented and adjusted the Echo configuration according to your needs, you may compile your application's assets: -->
Echo 설정을 주석 해제하고 프로젝트 환경에 맞게 조정했다면, 다음 명령어로 애플리케이션 에셋을 컴파일할 수 있습니다:

```
npm run dev
```

> [!TIP]
> 애플리케이션의 JavaScript 에셋 컴파일 방법에 대해서는 [Laravel Mix](/docs/8.x/mix) 문서를 참고하세요.

<a name="concept-overview"></a>

<!-- ## Concept Overview -->
## Concept Overview

<!-- Laravel's event broadcasting allows you to broadcast your server-side Laravel events to your client-side JavaScript application using a driver-based approach to WebSockets. Currently, Laravel ships with [Pusher Channels](https://pusher.com/channels) and [Ably](https://ably.io) drivers. The events may be easily consumed on the client-side using the [Laravel Echo](#client-side-installation) JavaScript package. -->
Laravel의 이벤트 브로드캐스팅은 드라이버 기반으로 설계되어 있어, 서버 사이드의 Laravel 이벤트를 클라이언트 사이드 JavaScript 애플리케이션으로 매우 손쉽게 브로드캐스트할 수 있습니다. Laravel에는 기본적으로 [Pusher Channels](https://pusher.com/channels)와 [Ably](https://ably.io) 드라이버가 포함되어 있습니다. 클라이언트에서는 [Laravel Echo](#client-side-installation) JavaScript 패키지를 사용하여 쉽게 이벤트를 수신할 수 있습니다.

<!-- Events are broadcast over "channels", which may be specified as public or private. Any visitor to your application may subscribe to a public channel without any authentication or authorization; however, in order to subscribe to a private channel, a user must be authenticated and authorized to listen on that channel. -->
이벤트는 "채널"을 통해 브로드캐스트됩니다. 채널은 공용(public) 또는 비공용(private)으로 지정할 수 있습니다. 누구나 인증이나 인가 과정 없이 공용 채널에 구독할 수 있지만, 비공용(프라이빗) 채널을 구독하려면 반드시 인증 및 인가를 받아야 합니다.

> [!TIP]
> Pusher의 오픈 소스 대안이 궁금하다면 [open source alternatives](#open-source-alternatives) 문서를 참고하세요.

<a name="using-example-application"></a>

<!-- ### Using An Example Application -->
### Using An Example Application

<!-- Before diving into each component of event broadcasting, let's take a high level overview using an e-commerce store as an example. -->
이벤트 브로드캐스팅의 각 컴포넌트를 본격적으로 살펴보기 전에, 먼저 통합 예시로 개념을 빠르게 훑어보겠습니다. 예로 들어 전자상거래(이커머스) 스토어를 다루는 애플리케이션을 생각해봅시다.

<!-- In our application, let's assume we have a page that allows users to view the shipping status for their orders. Let's also assume that a `OrderShipmentStatusUpdated` event is fired when a shipping status update is processed by the application: -->
이 애플리케이션에는 사용자가 자신의 주문 상태(배송 현황 등)를 볼 수 있는 페이지가 있습니다. 그리고 주문의 발송 상태가 갱신되는 시점에 `OrderShipmentStatusUpdated` 이벤트가 발생한다고 가정해봅니다:

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>

<!-- #### The `ShouldBroadcast` Interface -->
#### The `ShouldBroadcast` Interface

<!-- When a user is viewing one of their orders, we don't want them to have to refresh the page to view status updates. Instead, we want to broadcast the updates to the application as they are created. So, we need to mark the `OrderShipmentStatusUpdated` event with the `ShouldBroadcast` interface. This will instruct Laravel to broadcast the event when it is fired: -->
사용자가 특정 주문을 조회하고 있을 때, 새로고침 없이 배송 상태 업데이트를 실시간으로 받고 싶을 경우가 많습니다. 이를 위해서는, `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스를 구현하면, 이벤트가 발생했을 때 Laravel이 자동으로 해당 이벤트를 브로드캐스트합니다:

```
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    /**
     * The order instance.
     *
     * @var \App\Order
     */
    public $order;
}
```

<!-- The `ShouldBroadcast` interface requires our event to define a `broadcastOn` method. This method is responsible for returning the channels that the event should broadcast on. An empty stub of this method is already defined on generated event classes, so we only need to fill in its details. We only want the creator of the order to be able to view status updates, so we will broadcast the event on a private channel that is tied to the order: -->
`ShouldBroadcast` 인터페이스를 구현하면 반드시 `broadcastOn` 메서드를 정의해야 합니다. 이 메서드는 이벤트를 브로드캐스트할 채널(들)을 반환하는 역할을 합니다. 이벤트 클래스를 생성할 때 이미 비어있는 메서드 틀이 포함되어 있으니, 세부 내용을 채워주기만 하면 됩니다. 여기서는 주문의 생성자만 해당 주문 상태를 볼 수 있어야 하므로, 주문에 연결된 프라이빗 채널에서만 브로드캐스트하도록 합니다:

```
/**
 * Get the channels the event should broadcast on.
 *
 * @return \Illuminate\Broadcasting\PrivateChannel
 */
public function broadcastOn()
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

<a name="example-application-authorizing-channels"></a>

<!-- #### Authorizing Channels -->
#### Authorizing Channels

<!-- Remember, users must be authorized to listen on private channels. We may define our channel authorization rules in our application's `routes/channels.php` file. In this example, we need to verify that any user attempting to listen on the private `orders.1` channel is actually the creator of the order: -->
프라이빗 채널을 수신하려면, 사용자가 해당 채널을 구독할 수 있는 인가를 반드시 받아야 함을 기억하세요. 애플리케이션의 `routes/channels.php` 파일에서 채널 인가 규칙을 정의할 수 있습니다. 아래 예제에서는, 프라이빗 채널인 `orders.1`을 구독하려는 사용자가 실제로 해당 주문의 생성자인지 검증합니다:

```
use App\Models\Order;

Broadcast::channel('orders.{orderId}', function ($user, $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

<!-- The `channel` method accepts two arguments: the name of the channel and a callback which returns `true` or `false` indicating whether the user is authorized to listen on the channel. -->
`channel` 메서드는 두 개의 인수를 받습니다. 채널 이름과, 사용자가 해당 채널을 청취할 권한이 있는지를 나타내는 `true` 또는 `false` 값을 반환하는 콜백입니다.

<!-- All authorization callbacks receive the currently authenticated user as their first argument and any additional wildcard parameters as their subsequent arguments. In this example, we are using the `{orderId}` placeholder to indicate that the "ID" portion of the channel name is a wildcard. -->
모든 인가 콜백은 첫 번째 인수로 현재 인증된 사용자를 받고, 이후 인수로 추가 와일드카드 파라미터를 받습니다. 위 예시에서는 `{orderId}` 플레이스홀더를 사용해 채널 이름의 "ID" 부분이 와일드카드임을 나타냅니다.

<a name="listening-for-event-broadcasts"></a>

<!-- #### Listening For Event Broadcasts -->
#### Listening For Event Broadcasts

<!-- Next, all that remains is to listen for the event in our JavaScript application. We can do this using [Laravel Echo](#client-side-installation). First, we'll use the `private` method to subscribe to the private channel. Then, we may use the `listen` method to listen for the `OrderShipmentStatusUpdated` event. By default, all of the event's public properties will be included on the broadcast event: -->
이제 남은 일은, JavaScript 애플리케이션에서 이 이벤트를 수신하는 것입니다. 이는 [Laravel Echo](#client-side-installation)를 활용하여 간단히 구현할 수 있습니다. 먼저 `private` 메서드로 프라이빗 채널에 구독하고, 이어서 `listen` 메서드를 통해 `OrderShipmentStatusUpdated` 이벤트를 수신합니다. 기본적으로 이벤트의 public 속성은 모두 브로드캐스트 데이터로 전송됩니다:

```js
Echo.private(`orders.${orderId}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order);
    });
```

<a name="defining-broadcast-events"></a>

<!-- ## Defining Broadcast Events -->
## Defining Broadcast Events

<!-- To inform Laravel that a given event should be broadcast, you must implement the `Illuminate\Contracts\Broadcasting\ShouldBroadcast` interface on the event class. This interface is already imported into all event classes generated by the framework so you may easily add it to any of your events. -->
특정 이벤트를 브로드캐스팅해야 함을 Laravel에 알리려면, 해당 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크가 생성하는 모든 이벤트 클래스에서 이미 임포트되어 있으므로, 간단히 implements 키워드만 추가하면 됩니다.

<!-- The `ShouldBroadcast` interface requires you to implement a single method: `broadcastOn`. The `broadcastOn` method should return a channel or array of channels that the event should broadcast on. The channels should be instances of `Channel`, `PrivateChannel`, or `PresenceChannel`. Instances of `Channel` represent public channels that any user may subscribe to, while `PrivateChannels` and `PresenceChannels` represent private channels that require [channel authorization](#authorizing-channels): -->
`ShouldBroadcast` 인터페이스를 구현하면 반드시 하나의 메서드, 즉 `broadcastOn`을 정의해야 합니다. `broadcastOn` 메서드는 이벤트를 브로드캐스트할 채널(또는 채널 배열)을 반환해야 합니다. 여기서 반환하는 채널 객체는 `Channel`, `PrivateChannel`, 또는 `PresenceChannel`의 인스턴스가 되어야 합니다. `Channel`은 누구든 구독할 수 있는 공용 채널을 나타내며, `PrivateChannels`와 `PresenceChannels`는 [channel authorization](#authorizing-channels)가 반드시 필요한 프라이빗 채널을 의미합니다:

```
<?php

namespace App\Events;

use App\Models\User;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast
{
    use SerializesModels;

    /**
     * The user that created the server.
     *
     * @var \App\Models\User
     */
    public $user;

    /**
     * Create a new event instance.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function __construct(User $user)
    {
        $this->user = $user;
    }

    /**
     * Get the channels the event should broadcast on.
     *
     * @return Channel|array
     */
    public function broadcastOn()
    {
        return new PrivateChannel('user.'.$this->user->id);
    }
}
```

<!-- After implementing the `ShouldBroadcast` interface, you only need to [fire the event](/docs/8.x/events) as you normally would. Once the event has been fired, a [queued job](/docs/8.x/queues) will automatically broadcast the event using your specified broadcast driver. -->
`ShouldBroadcast` 인터페이스를 구현했다면, 이제 일반 이벤트와 똑같이 [fire the event](/docs/8.x/events)시키면 됩니다. 이벤트가 발생하면, [queued job](/docs/8.x/queues)을 통해 자동으로 지정한 브로드캐스트 드라이버로 이벤트가 브로드캐스팅됩니다.

<a name="broadcast-name"></a>

<!-- ### Broadcast Name -->
### Broadcast Name

<!-- By default, Laravel will broadcast the event using the event's class name. However, you may customize the broadcast name by defining a `broadcastAs` method on the event: -->
기본적으로 Laravel은 이벤트 클래스의 이름을 그대로 브로드캐스트 이름으로 사용합니다. 하지만, 이벤트의 `broadcastAs` 메서드를 정의하면 브로드캐스트 이름을 커스터마이징할 수 있습니다:

```
/**
 * The event's broadcast name.
 *
 * @return string
 */
public function broadcastAs()
{
    return 'server.created';
}
```

<!-- If you customize the broadcast name using the `broadcastAs` method, you should make sure to register your listener with a leading `.` character. This will instruct Echo to not prepend the application's namespace to the event: -->
`broadcastAs` 메서드를 통해 브로드캐스트 이름을 별도로 지정했다면, 리스너를 등록할 때 앞에 `.`(점) 문자를 붙여야 합니다. 이렇게 하면 Echo가 애플리케이션 네임스페이스를 이벤트 이름 앞에 덧붙이지 않도록 지정할 수 있습니다:

```
.listen('.server.created', function (e) {
    ....
});
```

<a name="broadcast-data"></a>

<!-- ### Broadcast Data -->
### Broadcast Data

<!-- When an event is broadcast, all of its `public` properties are automatically serialized and broadcast as the event's payload, allowing you to access any of its public data from your JavaScript application. So, for example, if your event has a single public `$user` property that contains an Eloquent model, the event's broadcast payload would be: -->
이벤트가 브로드캐스트될 때, 해당 이벤트의 모든 `public` 속성(property)은 자동으로 직렬화되어 브로드캐스트 데이터(payload)에 포함됩니다. 따라서 JavaScript 애플리케이션에서 이 속성값들을 바로 사용할 수 있습니다. 예를 들어, 이벤트에 Eloquent 모델이 담긴 단일 public `$user` 속성 하나만 있다면, 브로드캐스트 데이터는 아래와 같이 구성됩니다:

```
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

<!-- However, if you wish to have more fine-grained control over your broadcast payload, you may add a `broadcastWith` method to your event. This method should return the array of data that you wish to broadcast as the event payload: -->
하지만, 브로드캐스트 데이터(payload)를 더 세밀하게 제어하고 싶다면 이벤트에 `broadcastWith` 메서드를 정의할 수 있습니다. 이 메서드는 이벤트로 브로드캐스트할 데이터를 배열 형태로 반환하면 됩니다:

```
/**
 * Get the data to broadcast.
 *
 * @return array
 */
public function broadcastWith()
{
    return ['id' => $this->user->id];
}
```

<a name="broadcast-queue"></a>

<!-- ### Broadcast Queue -->
### Broadcast Queue

<!-- By default, each broadcast event is placed on the default queue for the default queue connection specified in your `queue.php` configuration file. You may customize the queue connection and name used by the broadcaster by defining `connection` and `queue` properties on your event class: -->
기본적으로 모든 브로드캐스트 이벤트는 `queue.php` 설정 파일에 지정된 기본 큐의 기본 커넥션에 등록됩니다. 브로드캐스터에서 사용할 큐 커넥션과 큐 이름을 이벤트 클래스의 `connection` 및 `queue` 속성을 통해 직접 지정할 수도 있습니다:

```
/**
 * The name of the queue connection to use when broadcasting the event.
 *
 * @var string
 */
public $connection = 'redis';

/**
 * The name of the queue on which to place the broadcasting job.
 *
 * @var string
 */
public $queue = 'default';
```

<!-- Alternatively, you may customize the queue name by defining a `broadcastQueue` method on your event: -->
또는, 이벤트에 `broadcastQueue` 메서드를 정의해 큐 이름을 커스터마이징할 수도 있습니다:

```
/**
 * The name of the queue on which to place the broadcasting job.
 *
 * @return string
 */
public function broadcastQueue()
{
    return 'default';
}
```

<!-- If you would like to broadcast your event using the `sync` queue instead of the default queue driver, you can implement the `ShouldBroadcastNow` interface instead of `ShouldBroadcast`: -->
만약 브로드캐스트 이벤트를 기본 큐 드라이버가 아닌 `sync` 큐를 통해 즉시 처리하고 싶다면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하면 됩니다:

```
<?php

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    //
}
```

<a name="broadcast-conditions"></a>

<!-- ### Broadcast Conditions -->
### Broadcast Conditions

<!-- Sometimes you want to broadcast your event only if a given condition is true. You may define these conditions by adding a `broadcastWhen` method to your event class: -->
특정 상황에서만 이벤트를 브로드캐스트하고 싶을 때는, 이벤트 클래스에 `broadcastWhen` 메서드를 추가하면 됩니다:

```
/**
 * Determine if this event should broadcast.
 *
 * @return bool
 */
public function broadcastWhen()
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>

<!-- #### Broadcasting & Database Transactions -->
#### Broadcasting & Database Transactions

<!-- When broadcast events are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your event depends on these models, unexpected errors can occur when the job that broadcasts the event is processed. -->
데이터베이스 트랜잭션 내부에서 브로드캐스팅 이벤트가 디스패치(dispatch)될 때, 브로드캐스트 작업이 큐에서 실제 트랜잭션 커밋보다 먼저 처리될 수도 있습니다. 이 경우 트랜잭션 중에 변경된 모델이나 DB 레코드가 아직 DB에 반영되지 않았거나, 트랜잭션 내에서 생성된 레코드가 DB에 존재하지 않을 수 있습니다. 만약 브로드캐스트 이벤트가 이런 모델이나 데이터에 의존한다면, 예상치 못한 에러가 발생할 수 있습니다.

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular broadcast event should be dispatched after all open database transactions have been committed by defining an `$afterCommit` property on the event class: -->
만약 큐 커넥션의 `after_commit` 설정이 `false`라면, 이벤트 클래스에 `$afterCommit` 속성을 설정하여 해당 브로드캐스트 작업이 모든 트랜잭션 커밋 이후에 처리되도록 지정할 수 있습니다:

```
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast
{
    use SerializesModels;

    public $afterCommit = true;
}
```

> [!TIP]
> 이러한 문제를 우회하는 방법에 대해 더 자세히 알고 싶다면, [queued jobs and database transactions](/docs/8.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>

<!-- ## Authorizing Channels -->
## Authorizing Channels

<!-- Private channels require you to authorize that the currently authenticated user can actually listen on the channel. This is accomplished by making an HTTP request to your Laravel application with the channel name and allowing your application to determine if the user can listen on that channel. When using [Laravel Echo](#client-side-installation), the HTTP request to authorize subscriptions to private channels will be made automatically; however, you do need to define the proper routes to respond to these requests. -->
프라이빗 채널을 사용하려면, 현재 인증된 사용자가 해당 채널을 실제로 수신(listen)할 수 있는 자격이 있는지 반드시 인가해야 합니다. 이 과정은 채널 이름을 포함한 HTTP 요청을 Laravel 애플리케이션에 보내고, 애플리케이션이 사용자의 구독 권한을 검증하는 방식으로 이루어집니다. [Laravel Echo](#client-side-installation)를 사용할 경우, 프라이빗 채널 구독 인가를 위한 HTTP 요청이 자동으로 전송되지만, 애플리케이션에서 이 요청에 응답할 라우트를 별도로 정의해주어야 합니다.

<a name="defining-authorization-routes"></a>

<!-- ### Defining Authorization Routes -->
### Defining Authorization Routes

<!-- Thankfully, Laravel makes it easy to define the routes to respond to channel authorization requests. In the `App\Providers\BroadcastServiceProvider` included with your Laravel application, you will see a call to the `Broadcast::routes` method. This method will register the `/broadcasting/auth` route to handle authorization requests: -->
Laravel에서는 채널 인가 요청에 응답할 라우트를 매우 쉽게 정의할 수 있습니다. Laravel 애플리케이션에 기본 포함된 `App\Providers\BroadcastServiceProvider`에는 `Broadcast::routes` 메서드가 호출되어 있습니다. 이 메서드는 `/broadcasting/auth` 라우트를 등록해 브로드캐스트 인가 요청을 처리합니다:

```
Broadcast::routes();
```

<!-- The `Broadcast::routes` method will automatically place its routes within the `web` middleware group; however, you may pass an array of route attributes to the method if you would like to customize the assigned attributes: -->
`Broadcast::routes` 메서드는 기본적으로 등록하는 모든 라우트를 `web` 미들웨어 그룹에 포함시킵니다. 만약 라우트 속성을 커스터마이징하고 싶다면, 메서드에 속성(attributes) 배열을 전달할 수도 있습니다:

```
Broadcast::routes($attributes);
```

<a name="customizing-the-authorization-endpoint"></a>

<!-- #### Customizing The Authorization Endpoint -->
#### Customizing The Authorization Endpoint

<!-- By default, Echo will use the `/broadcasting/auth` endpoint to authorize channel access. However, you may specify your own authorization endpoint by passing the `authEndpoint` configuration option to your Echo instance: -->
기본적으로 Echo는 채널 접근 권한을 인가하기 위해 `/broadcasting/auth` 엔드포인트를 사용합니다. 하지만 `authEndpoint` 설정 옵션을 Echo 인스턴스에 전달함으로써 여러분만의 인가 엔드포인트를 사용할 수 있습니다.

```
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    authEndpoint: '/custom/endpoint/auth'
});
```

<a name="customizing-the-authorization-request"></a>

<!-- #### Customizing The Authorization Request -->
#### Customizing The Authorization Request

<!-- You can customize how Laravel Echo performs authorization requests by providing a custom authorizer when initializing Echo: -->
Laravel Echo가 인가 요청을 수행하는 방식을 커스터마이즈하려면 Echo를 초기화할 때 사용자 지정 authorizer를 제공할 수 있습니다.

```
window.Echo = new Echo({
    // ...
    authorizer: (channel, options) => {
        return {
            authorize: (socketId, callback) => {
                axios.post('/api/broadcasting/auth', {
                    socket_id: socketId,
                    channel_name: channel.name
                })
                .then(response => {
                    callback(false, response.data);
                })
                .catch(error => {
                    callback(true, error);
                });
            }
        };
    },
})
```

<a name="defining-authorization-callbacks"></a>

<!-- ### Defining Authorization Callbacks -->
### Defining Authorization Callbacks

<!-- Next, we need to define the logic that will actually determine if the currently authenticated user can listen to a given channel. This is done in the `routes/channels.php` file that is included with your application. In this file, you may use the `Broadcast::channel` method to register channel authorization callbacks: -->
다음으로, 현재 인증된 사용자가 특정 채널을 청취할 권한이 있는지 실제로 판단하는 로직을 정의해야 합니다. 이 로직은 애플리케이션에 기본으로 포함된 `routes/channels.php` 파일에서 작성합니다. 이 파일 내에서, `Broadcast::channel` 메서드를 사용하여 채널 인증 콜백을 등록할 수 있습니다.

```
Broadcast::channel('orders.{orderId}', function ($user, $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

<!-- The `channel` method accepts two arguments: the name of the channel and a callback which returns `true` or `false` indicating whether the user is authorized to listen on the channel. -->
`channel` 메서드는 두 개의 인수를 받습니다. 채널 이름과, 사용자가 해당 채널을 청취할 권한이 있는지를 나타내는 `true` 또는 `false` 값을 반환하는 콜백입니다.

<!-- All authorization callbacks receive the currently authenticated user as their first argument and any additional wildcard parameters as their subsequent arguments. In this example, we are using the `{orderId}` placeholder to indicate that the "ID" portion of the channel name is a wildcard. -->
모든 인증 콜백은 첫 번째 인수로 현재 인증된 사용자를, 그리고 이후 인수로는 와일드카드 파라미터를 받습니다. 이 예제에서는 `{orderId}` 플레이스홀더를 사용하여 채널 이름의 "ID" 부분이 와일드카드임을 나타냅니다.

<a name="authorization-callback-model-binding"></a>

<!-- #### Authorization Callback Model Binding -->
#### Authorization Callback Model Binding

<!-- Just like HTTP routes, channel routes may also take advantage of implicit and explicit [route model binding](/docs/8.x/routing#route-model-binding). For example, instead of receiving a string or numeric order ID, you may request an actual `Order` model instance: -->
HTTP 라우트와 마찬가지로, 채널 라우트에서도 [route model binding](/docs/8.x/routing#route-model-binding)의 명시적 및 암묵적 방식 모두를 활용할 수 있습니다. 예를 들어, 문자열이나 숫자 형태의 주문 ID 대신 실제 `Order` 모델 인스턴스를 받을 수도 있습니다.

```
use App\Models\Order;

Broadcast::channel('orders.{order}', function ($user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!NOTE]
> HTTP 라우트 모델 바인딩과 달리, 채널 모델 바인딩은 자동 [implicit model binding scoping](/docs/8.x/routing#implicit-model-binding-scoping)를 지원하지 않습니다. 하지만 대부분의 경우, 채널은 단일 모델의 고유 기본 키로 범위가 지정되기 때문에 이 점이 문제되는 경우는 드뭅니다.

<a name="authorization-callback-authentication"></a>

<!-- #### Authorization Callback Authentication -->
#### Authorization Callback Authentication

<!-- Private and presence broadcast channels authenticate the current user via your application's default authentication guard. If the user is not authenticated, channel authorization is automatically denied and the authorization callback is never executed. However, you may assign multiple, custom guards that should authenticate the incoming request if necessary: -->
프라이빗 및 프리즌스 브로드캐스트 채널은 애플리케이션의 기본 인증 가드(guard)를 통해 현재 사용자를 인증합니다. 사용자가 인증되지 않았다면 채널 인증은 자동으로 거부되며, 인증 콜백이 실행되지 않습니다. 하지만 필요하다면 여러 개의 커스텀 가드를 지정해서, 해당 요청을 인증 처리하도록 할 수 있습니다.

```
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>

<!-- ### Defining Channel Classes -->
### Defining Channel Classes

<!-- If your application is consuming many different channels, your `routes/channels.php` file could become bulky. So, instead of using closures to authorize channels, you may use channel classes. To generate a channel class, use the `make:channel` Artisan command. This command will place a new channel class in the `App/Broadcasting` directory. -->
애플리케이션이 다양한 채널을 많이 사용한다면 `routes/channels.php` 파일이 복잡해질 수 있습니다. 이럴 때는 클로저 대신 채널 클래스를 사용할 수 있습니다. 채널 클래스를 생성하려면 `make:channel` Artisan 명령어를 사용합니다. 이렇게 하면 `App/Broadcasting` 디렉터리에 새로운 채널 클래스가 생성됩니다.

```
php artisan make:channel OrderChannel
```

<!-- Next, register your channel in your `routes/channels.php` file: -->
다음으로, `routes/channels.php` 파일에서 해당 채널을 등록합니다.

```
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

<!-- Finally, you may place the authorization logic for your channel in the channel class' `join` method. This `join` method will house the same logic you would have typically placed in your channel authorization closure. You may also take advantage of channel model binding: -->
마지막으로, 채널 클래스의 `join` 메서드에 채널 인가 로직을 작성할 수 있습니다. 이 `join` 메서드에는 보통 클로저로 등록하던 동일한 로직을 포함하면 됩니다. 또한 채널 모델 바인딩도 활용할 수 있습니다.

```
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * Create a new channel instance.
     *
     * @return void
     */
    public function __construct()
    {
        //
    }

    /**
     * Authenticate the user's access to the channel.
     *
     * @param  \App\Models\User  $user
     * @param  \App\Models\Order  $order
     * @return array|bool
     */
    public function join(User $user, Order $order)
    {
        return $user->id === $order->user_id;
    }
}
```

> [!TIP]
> Laravel의 여러 클래스와 마찬가지로, 채널 클래스도 [service container](/docs/8.x/container)에 의해 자동으로 resolve됩니다. 따라서 생성자에서 필요한 의존성을 타입 힌트로 명시하면, 자동으로 주입받을 수 있습니다.

<a name="broadcasting-events"></a>

<!-- ## Broadcasting Events -->
## Broadcasting Events

<!-- Once you have defined an event and marked it with the `ShouldBroadcast` interface, you only need to fire the event using the event's dispatch method. The event dispatcher will notice that the event is marked with the `ShouldBroadcast` interface and will queue the event for broadcasting: -->
이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 구현한 후에는, 해당 이벤트의 dispatch 메서드를 사용해 이벤트를 발생시키면 됩니다. 이벤트 디스패처는 이벤트에 `ShouldBroadcast` 인터페이스가 구현되어 있음을 감지하고, 해당 이벤트를 브로드캐스팅 대기열에 추가합니다.

```
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>

<!-- ### Only To Others -->
### Only To Others

<!-- When building an application that utilizes event broadcasting, you may occasionally need to broadcast an event to all subscribers to a given channel except for the current user. You may accomplish this using the `broadcast` helper and the `toOthers` method: -->
이벤트 브로드캐스팅을 사용하는 애플리케이션에서는, 때때로 현재 사용자를 제외한 모두에게 이벤트를 브로드캐스트해야 할 때가 있습니다. 이럴 때는 `broadcast` 헬퍼와 `toOthers` 메서드를 활용할 수 있습니다.

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

<!-- To better understand when you may want to use the `toOthers` method, let's imagine a task list application where a user may create a new task by entering a task name. To create a task, your application might make a request to a `/task` URL which broadcasts the task's creation and returns a JSON representation of the new task. When your JavaScript application receives the response from the end-point, it might directly insert the new task into its task list like so: -->
언제 `toOthers` 메서드를 사용하면 좋은지 이해하기 위해, 할일 목록 애플리케이션을 예로 들어 보겠습니다. 사용자가 새로운 작업을 추가할 때, 애플리케이션에서는 `/task` URL에 요청을 보내 작업 생성을 처리하고, 새 작업의 JSON 데이터를 반환할 수 있습니다. 클라이언트(예: 자바스크립트 앱)는 응답을 받아 작업 목록에 새 작업을 직접 추가할 수 있습니다.

```
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

<!-- However, remember that we also broadcast the task's creation. If your JavaScript application is also listening for this event in order to add tasks to the task list, you will have duplicate tasks in your list: one from the end-point and one from the broadcast. You may solve this by using the `toOthers` method to instruct the broadcaster to not broadcast the event to the current user. -->
하지만 작업 생성 시 이벤트도 브로드캐스트된다면, 자바스크립트 앱이 이벤트를 청취해 또 한 번 작업을 추가할 수 있기 때문에, 같은 작업이 두 번 추가되는 문제가 발생할 수 있습니다. 이런 중복을 방지하려면 `toOthers` 메서드를 사용하여 브로드캐스트 대상에서 현재 사용자를 제외하면 됩니다.

> [!NOTE]
> 이벤트에서 `toOthers` 메서드를 사용하려면, 반드시 해당 이벤트 클래스가 `Illuminate\Broadcasting\InteractsWithSockets` 트레잇을 사용해야 합니다.

<a name="only-to-others-configuration"></a>

<!-- #### Configuration -->
#### Configuration

<!-- When you initialize a Laravel Echo instance, a socket ID is assigned to the connection. If you are using a global [Axios](https://github.com/mzabriskie/axios) instance to make HTTP requests from your JavaScript application, the socket ID will automatically be attached to every outgoing request as a `X-Socket-ID` header. Then, when you call the `toOthers` method, Laravel will extract the socket ID from the header and instruct the broadcaster to not broadcast to any connections with that socket ID. -->
Laravel Echo 인스턴스를 초기화하면, 연결에 socket ID가 부여됩니다. 자바스크립트 애플리케이션에서 [Axios](https://github.com/mzabriskie/axios)와 같은 전역 인스턴스를 사용해 HTTP 요청을 보낼 경우, 각 요청 헤더에 자동으로 `X-Socket-ID` 값이 추가됩니다. 그러면 `toOthers` 메서드는 이 socket ID를 활용해, 해당 ID를 가진 접속자에게는 브로드캐스트를 하지 않도록 지시합니다.

<!-- If you are not using a global Axios instance, you will need to manually configure your JavaScript application to send the `X-Socket-ID` header with all outgoing requests. You may retrieve the socket ID using the `Echo.socketId` method: -->
전역 Axios 인스턴스를 사용하지 않는 경우, 자바스크립트 애플리케이션에서 모든 요청 시 수동으로 `X-Socket-ID` 헤더를 추가해야 합니다. 이때는 `Echo.socketId` 메서드를 사용해 socket ID를 얻을 수 있습니다.

```
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>

<!-- ### Customizing The Connection -->
### Customizing The Connection

<!-- If your application interacts with multiple broadcast connections and you want to broadcast an event using a broadcaster other than your default, you may specify which connection to push an event to using the `via` method: -->
여러 브로드캐스트 커넥션을 사용하는 애플리케이션에서, 기본 브로드캐스터 이외의 브로드캐스터로 이벤트를 전송하려면 `via` 메서드를 사용할 수 있습니다.

```
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

<!-- Alternatively, you may specify the event's broadcast connection by calling the `broadcastVia` method within the event's constructor. However, before doing so, you should ensure that the event class uses the `InteractsWithBroadcasting` trait: -->
또한, 이벤트의 생성자 내부에서 `broadcastVia` 메서드를 호출하여, 이벤트의 브로드캐스트 커넥션을 지정할 수도 있습니다. 이 전에, 이벤트 클래스가 `InteractsWithBroadcasting` 트레잇을 사용하고 있는지 확인해야 합니다.

```
<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithBroadcasting;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    use InteractsWithBroadcasting;

    /**
     * Create a new event instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```

<a name="receiving-broadcasts"></a>

<!-- ## Receiving Broadcasts -->
## Receiving Broadcasts

<a name="listening-for-events"></a>

<!-- ### Listening For Events -->
### Listening For Events

<!-- Once you have [installed and instantiated Laravel Echo](#client-side-installation), you are ready to start listening for events that are broadcast from your Laravel application. First, use the `channel` method to retrieve an instance of a channel, then call the `listen` method to listen for a specified event: -->
[installed and instantiated Laravel Echo](#client-side-installation)했다면, Laravel 애플리케이션에서 브로드캐스트된 이벤트를 청취할 준비가 된 것입니다. 먼저, `channel` 메서드를 사용해 채널 인스턴스를 가져온 뒤, `listen` 메서드를 호출해서 원하는 이벤트를 구독하면 됩니다.

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

<!-- If you would like to listen for events on a private channel, use the `private` method instead. You may continue to chain calls to the `listen` method to listen for multiple events on a single channel: -->
프라이빗 채널의 이벤트를 듣고 싶다면 `private` 메서드를 사용하세요. 여러 이벤트를 하나의 채널에서 연속으로 `listen` 체이닝 방식으로 청취할 수도 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .listen(...)
    .listen(...)
    .listen(...);
```

<a name="stop-listening-for-events"></a>

<!-- #### Stop Listening For Events -->
#### Stop Listening For Events

<!-- If you would like to stop listening to a given event without [leaving the channel](#leaving-a-channel), you may use the `stopListening` method: -->
[leaving the channel](#leaving-a-channel) 없이 특정 이벤트의 청취만 중단하고 싶다면, `stopListening` 메서드를 사용할 수 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated')
```

<a name="leaving-a-channel"></a>

<!-- ### Leaving A Channel -->
### Leaving A Channel

<!-- To leave a channel, you may call the `leaveChannel` method on your Echo instance: -->
채널에서 나가려면 Echo 인스턴스의 `leaveChannel` 메서드를 호출합니다.

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

<!-- If you would like to leave a channel and also its associated private and presence channels, you may call the `leave` method: -->
주어진 채널뿐 아니라 그와 연관된 프라이빗 및 프리즌스 채널 모두에서 나가고 싶을 때는, `leave` 메서드를 사용하세요.

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>

<!-- ### Namespaces -->
### Namespaces

<!-- You may have noticed in the examples above that we did not specify the full `App\Events` namespace for the event classes. This is because Echo will automatically assume the events are located in the `App\Events` namespace. However, you may configure the root namespace when you instantiate Echo by passing a `namespace` configuration option: -->
위 예제들에서 이벤트 클래스의 전체 `App\Events` 네임스페이스를 따로 지정하지 않은 점을 눈치챘을 수도 있습니다. 이는 Echo가 기본적으로 이벤트가 `App\Events` 네임스페이스에 있다고 간주하기 때문입니다. 하지만 Echo를 인스턴스화할 때 `namespace` 옵션을 전달해 루트 네임스페이스를 직접 설정할 수 있습니다.

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

<!-- Alternatively, you may prefix event classes with a `.` when subscribing to them using Echo. This will allow you to always specify the fully-qualified class name: -->
또는, Echo로 이벤트를 구독할 때 이벤트 클래스 앞에 `.`를 붙일 수도 있습니다. 이렇게 하면 항상 정규화된 전체 클래스 이름을 지정할 수 있습니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        //
    });
```

<a name="presence-channels"></a>

<!-- ## Presence Channels -->
## Presence Channels

<!-- Presence channels build on the security of private channels while exposing the additional feature of awareness of who is subscribed to the channel. This makes it easy to build powerful, collaborative application features such as notifying users when another user is viewing the same page or listing the inhabitants of a chat room. -->
프리즌스 채널은 프라이빗 채널의 보안 위에, 채널에 누가 구독 중인지 인지할 수 있는 기능이 더해진 채널입니다. 이를 통해 같은 페이지를 보고 있는 다른 사용자가 누구인지 알리는 기능이나, 채팅방 입장 멤버 목록 등의 강력한 협업 기능을 쉽게 구축할 수 있습니다.

<a name="authorizing-presence-channels"></a>

<!-- ### Authorizing Presence Channels -->
### Authorizing Presence Channels

<!-- All presence channels are also private channels; therefore, users must be [authorized to access them](#authorizing-channels). However, when defining authorization callbacks for presence channels, you will not return `true` if the user is authorized to join the channel. Instead, you should return an array of data about the user. -->
프리즌스 채널은 프라이빗 채널이기도 하므로, 사용자는 반드시 [authorized to access them](#authorizing-channels) 상태여야 합니다. 그러나 프라이빗 채널과 달리, 프리즌스 채널의 인가 콜백에서는 사용자가 채널에 참여할 수 있는 경우 `true`를 반환하는 것이 아니라, 사용자에 대한 데이터를 배열로 반환해야 합니다.

<!-- The data returned by the authorization callback will be made available to the presence channel event listeners in your JavaScript application. If the user is not authorized to join the presence channel, you should return `false` or `null`: -->
이 콜백에서 반환된 데이터는 자바스크립트 애플리케이션의 프리즌스 채널 이벤트 리스너에서 사용할 수 있습니다. 사용자가 채널 참여를 인가받지 못하면, `false` 또는 `null`을 반환하면 됩니다.

```
Broadcast::channel('chat.{roomId}', function ($user, $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>

<!-- ### Joining Presence Channels -->
### Joining Presence Channels

<!-- To join a presence channel, you may use Echo's `join` method. The `join` method will return a `PresenceChannel` implementation which, along with exposing the `listen` method, allows you to subscribe to the `here`, `joining`, and `leaving` events. -->
프리즌스 채널에 참여하려면 Echo의 `join` 메서드를 사용합니다. `join` 메서드는 `PresenceChannel` 구현체를 반환합니다. 이 구현체는 `listen` 메서드뿐 아니라, `here`, `joining`, `leaving` 이벤트 구독 메서드도 함께 제공합니다.

```
Echo.join(`chat.${roomId}`)
    .here((users) => {
        //
    })
    .joining((user) => {
        console.log(user.name);
    })
    .leaving((user) => {
        console.log(user.name);
    })
    .error((error) => {
        console.error(error);
    });
```

<!-- The `here` callback will be executed immediately once the channel is joined successfully, and will receive an array containing the user information for all of the other users currently subscribed to the channel. The `joining` method will be executed when a new user joins a channel, while the `leaving` method will be executed when a user leaves the channel. The `error` method will be executed when the authentication endpoint returns a HTTP status code other than 200 or if there is a problem parsing the returned JSON. -->
`here` 콜백은 채널에 성공적으로 참여하자마자 즉시 실행되며, 현재 채널에 구독 중인 모든 다른 사용자의 정보를 담은 배열을 인자로 받습니다. `joining` 메서드는 새로운 사용자가 채널에 들어올 때 실행되고, `leaving` 메서드는 사용자가 나갈 때 실행됩니다. `error` 메서드는 인증 엔드포인트가 200이 아닌 상태 코드를 반환하거나, 반환된 JSON을 파싱하는 데 문제가 발생할 때 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>

<!-- ### Broadcasting To Presence Channels -->
### Broadcasting To Presence Channels

<!-- Presence channels may receive events just like public or private channels. Using the example of a chatroom, we may want to broadcast `NewMessage` events to the room's presence channel. To do so, we'll return an instance of `PresenceChannel` from the event's `broadcastOn` method: -->
프리즌스 채널도 퍼블릭이나 프라이빗 채널처럼 이벤트를 수신할 수 있습니다. 예를 들어, 채팅방에서 `NewMessage` 이벤트를 해당 방의 프리즌스 채널로 브로드캐스트할 수 있습니다. 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환하면 됩니다.

```
/**
 * Get the channels the event should broadcast on.
 *
 * @return Channel|array
 */
public function broadcastOn()
{
    return new PresenceChannel('room.'.$this->message->room_id);
}
```

<!-- As with other events, you may use the `broadcast` helper and the `toOthers` method to exclude the current user from receiving the broadcast: -->
다른 이벤트와 마찬가지로, `broadcast` 헬퍼와 `toOthers` 메서드를 사용하면 현재 사용자를 브로드캐스트 대상에서 제외할 수 있습니다.

```
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

<!-- As typical of other types of events, you may listen for events sent to presence channels using Echo's `listen` method: -->
다른 종류의 이벤트와 마찬가지로, 프리즌스 채널로 전송된 이벤트를 Echo의 `listen` 메서드로 청취할 수 있습니다.

```
Echo.join(`chat.${roomId}`)
    .here(...)
    .joining(...)
    .leaving(...)
    .listen('NewMessage', (e) => {
        //
    });
```

<a name="model-broadcasting"></a>

<!-- ## Model Broadcasting -->
## Model Broadcasting

> [!NOTE]
> 모델 브로드캐스팅 관련 섹션을 읽기 전에, Laravel의 모델 브로드캐스팅 서비스의 기본 개념과, 브로드캐스트 이벤트를 직접 생성 및 청취하는 방법을 충분히 숙지하시길 권장합니다.

<!-- It is common to broadcast events when your application's [Eloquent models](/docs/8.x/eloquent) are created, updated, or deleted. Of course, this can easily be accomplished by manually [defining custom events for Eloquent model state changes](/docs/8.x/eloquent#events) and marking those events with the `ShouldBroadcast` interface. -->
애플리케이션의 [Eloquent models](/docs/8.x/eloquent)이 생성, 수정, 삭제될 때 이벤트를 브로드캐스트하는 것은 매우 일반적입니다. 물론, 이런 처리를 위해 [defining custom events for Eloquent model state changes](/docs/8.x/eloquent#events)를 직접 정의하고, 이 이벤트에 `ShouldBroadcast` 인터페이스를 구현하는 방식도 사용할 수 있습니다.

<!-- However, if you are not using these events for any other purposes in your application, it can be cumbersome to create event classes for the sole purpose of broadcasting them. To remedy this, Laravel allows you to indicate that an Eloquent model should automatically broadcast its state changes. -->
그렇지만, 다른 용도가 없이 오직 브로드캐스트만을 위해 이벤트 클래스를 만드는 것이 번거로울 수 있습니다. 이를 해결하기 위해, Laravel은 Eloquent 모델이 상태 변화를 자동으로 브로드캐스트할 수 있도록 지원합니다.

<!-- To get started, your Eloquent model should use the `Illuminate\Database\Eloquent\BroadcastsEvents` trait. In addition, the model should define a `broadcastsOn` method, which will return an array of channels that the model's events should broadcast on: -->
우선, Eloquent 모델에서 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레잇을 사용하세요. 그리고 `broadcastsOn` 메서드를 정의해, 모델의 이벤트가 브로드캐스트될 채널 배열을 반환하도록 설정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Database\Eloquent\BroadcastsEvents;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    use BroadcastsEvents, HasFactory;

    /**
     * Get the user that the post belongs to.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Get the channels that model events should broadcast on.
     *
     * @param  string  $event
     * @return \Illuminate\Broadcasting\Channel|array
     */
    public function broadcastOn($event)
    {
        return [$this, $this->user];
    }
}
```

<!-- Once your model includes this trait and defines its broadcast channels, it will begin automatically broadcasting events when a model instance is created, updated, deleted, trashed, or restored. -->
이렇게 트레잇을 추가하고 브로드캐스트 채널을 정의하면, 모델 인스턴스가 생성, 수정, 삭제, 휴지통 이동(trashed), 복원(restored)될 때마다 자동으로 관련 이벤트가 브로드캐스트됩니다.

<!-- In addition, you may have noticed that the `broadcastOn` method receives a string `$event` argument. This argument contains the type of event that has occurred on the model and will have a value of `created`, `updated`, `deleted`, `trashed`, or `restored`. By inspecting the value of this variable, you may determine which channels (if any) the model should broadcast to for a particular event: -->
또한, `broadcastOn` 메서드에 문자열 `$event` 인수가 전달되는 점에 주목해주세요. 이 인수에는 현재 발생한 모델 이벤트의 타입(예: `created`, `updated`, `deleted`, `trashed`, `restored`)이 담깁니다. 이 값을 활용해, 어떤 이벤트에 대해 어떤 채널을 브로드캐스트할지 판단할 수 있습니다.

```php
/**
 * Get the channels that model events should broadcast on.
 *
 * @param  string  $event
 * @return \Illuminate\Broadcasting\Channel|array
 */
public function broadcastOn($event)
{
    return match ($event) {
        'deleted' => [],
        default => [$this, $this->user],
    };
}
```

<a name="customizing-model-broadcasting-event-creation"></a>

<!-- #### Customizing Model Broadcasting Event Creation -->
#### Customizing Model Broadcasting Event Creation

<!-- Occasionally, you may wish to customize how Laravel creates the underlying model broadcasting event. You may accomplish this by defining a `newBroadcastableEvent` method on your Eloquent model. This method should return an `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` instance: -->
때때로 Laravel이 내부적으로 모델 브로드캐스팅 이벤트를 생성하는 방식을 커스터마이즈하고 싶을 수 있습니다. 이럴 때는 Eloquent 모델에 `newBroadcastableEvent` 메서드를 정의할 수 있습니다. 이 메서드는 반드시 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다.

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred

/**
 * Create a new broadcastable model event for the model.
 *
 * @param  string  $event
 * @return \Illuminate\Database\Eloquent\BroadcastableModelEventOccurred
 */
protected function newBroadcastableEvent($event)
{
    return (new BroadcastableModelEventOccurred(
        $this, $event
    ))->dontBroadcastToCurrentUser();
}
```

<a name="model-broadcasting-conventions"></a>

<!-- ### Model Broadcasting Conventions -->
### Model Broadcasting Conventions

<a name="model-broadcasting-channel-conventions"></a>

<!-- #### Channel Conventions -->
#### Channel Conventions

<!-- As you may have noticed, the `broadcastOn` method in the model example above did not return `Channel` instances. Instead, Eloquent models were returned directly. If an Eloquent model instance is returned by your model's `broadcastOn` method (or is contained in an array returned by the method), Laravel will automatically instantiate a private channel instance for the model using the model's class name and primary key identifier as the channel name. -->
앞선 예시에서 모델의 `broadcastOn` 메서드가 `Channel` 인스턴스 대신 Eloquent 모델 인스턴스를 반환한 것을 확인할 수 있습니다. 모델의 `broadcastOn` 메서드에서 Eloquent 모델 인스턴스(혹은 이를 포함하는 배열)를 반환하면, Laravel은 자동으로 모델의 클래스명과 기본 키 식별자를 채널 이름으로 사용해 프라이빗 채널 인스턴스를 생성합니다.

<!-- So, an `App\Models\User` model with an `id` of `1` would be converted into a `Illuminate\Broadcasting\PrivateChannel` instance with a name of `App.Models.User.1`. Of course, in addition to returning Eloquent model instances from your model's `broadcastOn` method, you may return complete `Channel` instances in order to have full control over the model's channel names: -->
예를 들어, `App\Models\User` 모델의 `id`가 `1`이라면, `Illuminate\Broadcasting\PrivateChannel` 인스턴스가 `App.Models.User.1`이라는 이름으로 만들어집니다. 물론, 모델의 `broadcastOn` 메서드에서 Eloquent 모델 대신 직접 `Channel` 인스턴스를 반환해, 채널 이름을 완전히 제어하는 것도 가능합니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels that model events should broadcast on.
 *
 * @param  string  $event
 * @return \Illuminate\Broadcasting\Channel|array
 */
public function broadcastOn($event)
{
    return [new PrivateChannel('user.'.$this->id)];
}
```

<!-- If you plan to explicitly return a channel instance from your model's `broadcastOn` method, you may pass an Eloquent model instance to the channel's constructor. When doing so, Laravel will use the model channel conventions discussed above to convert the Eloquent model into a channel name string: -->
`broadcastOn` 메서드에서 채널 인스턴스를 명시적으로 반환할 계획이라면, 이를 생성할 때 Eloquent 모델 인스턴스를 인수로 전달할 수 있습니다. 이렇게 하면 Laravel은 모델 브로드캐스팅 관례를 사용해, 해당 모델을 채널 이름 문자열로 자동 변환합니다.

```php
return [new Channel($this->user)];
```

<!-- If you need to determine the channel name of a model, you may call the `broadcastChannel` method on any model instance. For example, this method returns the string `App.Models.User.1` for a `App\Models\User` model with an `id` of `1`: -->
모델의 실제 채널 이름이 궁금하다면, 어떤 모델 인스턴스에서도 `broadcastChannel` 메서드를 호출하여 확인할 수 있습니다. 예를 들어, `App\Models\User` 모델의 `id`가 `1`인 경우, 해당 메서드는 `App.Models.User.1` 문자열을 반환합니다.

```php
$user->broadcastChannel()
```

<a name="model-broadcasting-event-conventions"></a>

<!-- #### Event Conventions -->
#### Event Conventions

<!-- Since model broadcast events are not associated with an "actual" event within your application's `App\Events` directory, they are assigned a name and a payload based on conventions. Laravel's convention is to broadcast the event using the class name of the model (not including the namespace) and the name of the model event that triggered the broadcast. -->
모델 브로드캐스트 이벤트는 애플리케이션 `App\Events` 디렉터리에 "실제" 이벤트가 존재하는 것이 아니므로, 관례에 따라 이름과 페이로드가 할당됩니다. Laravel은 모델의 클래스명(네임스페이스 제외)과 해당 이벤트 타입을 조합해 이벤트 이름을 구성합니다.

<!-- So, for example, an update to the `App\Models\Post` model would broadcast an event to your client-side application as `PostUpdated` with the following payload: -->
예를 들어, `App\Models\Post` 모델이 수정되면 클라이언트 애플리케이션에는 `PostUpdated`라는 이름으로 아래와 같은 페이로드가 전송됩니다.

```
{
    "model": {
        "id": 1,
        "title": "My first post"
        ...
    },
    ...
    "socket": "someSocketId",
}
```

<!-- The deletion of the `App\Models\User` model would broadcast an event named `UserDeleted`. -->
`App\Models\User` 모델이 삭제될 경우에는 `UserDeleted` 이벤트 이름이 사용됩니다.

<!-- If you would like, you may define a custom broadcast name and payload by adding a `broadcastAs` and `broadcastWith` method to your model. These methods receive the name of the model event / operation that is occurring, allowing you to customize the event's name and payload for each model operation. If `null` is returned from the `broadcastAs` method, Laravel will use the model broadcasting event name conventions discussed above when broadcasting the event: -->
원한다면, 모델에 `broadcastAs` 및 `broadcastWith` 메서드를 추가해, 브로드캐스트되는 이름과 페이로드를 커스터마이즈할 수 있습니다. 이 메서드는 해당 모델 이벤트/작업의 이름을 인수로 받아, 각 작업 유형별 명칭과 페이로드를 원하는 대로 세밀하게 제어할 수 있습니다. `broadcastAs`에서 `null`을 반환하면, Laravel은 위에 설명한 기본 네이밍 관례를 따릅니다.

```php
/**
 * The model event's broadcast name.
 *
 * @param  string  $event
 * @return string|null
 */
public function broadcastAs($event)
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * Get the data to broadcast for the model.
 *
 * @param  string  $event
 * @return array
 */
public function broadcastWith($event)
{
    return match ($event) {
        'created' => ['title' => $this->title],
        default => ['model' => $this],
    };
}
```

<a name="listening-for-model-broadcasts"></a>

<!-- ### Listening For Model Broadcasts -->
### Listening For Model Broadcasts

<!-- Once you have added the `BroadcastsEvents` trait to your model and defined your model's `broadcastOn` method, you are ready to start listening for broadcasted model events within your client-side application. Before getting started, you may wish to consult the complete documentation on [listening for events](#listening-for-events). -->
모델에 `BroadcastsEvents` 트레잇을 추가하고 `broadcastOn` 메서드를 정의했다면, 이제 클라이언트 애플리케이션에서 브로드캐스트된 모델 이벤트를 청취할 수 있습니다. 시작에 앞서 [listening for events](#listening-for-events)에 대한 전체 문서를 참고하면 좋습니다.

<!-- First, use the `private` method to retrieve an instance of a channel, then call the `listen` method to listen for a specified event. Typically, the channel name given to the `private` method should correspond to Laravel's [model broadcasting conventions](#model-broadcasting-conventions). -->
먼저, `private` 메서드를 사용해 채널 인스턴스를 얻은 다음, `listen` 메서드로 원하는 이벤트를 구독하세요. 일반적으로 `private` 메서드에 지정하는 채널 이름은 Laravel의 [model broadcasting conventions](#model-broadcasting-conventions)를 따라야 합니다.

<!-- Once you have obtained a channel instance, you may use the `listen` method to listen for a particular event. Since model broadcast events are not associated with an "actual" event within your application's `App\Events` directory, the [event name](#model-broadcasting-event-conventions) must be prefixed with a `.` to indicate it does not belong to a particular namespace. Each model broadcast event has a `model` property which contains all of the broadcastable properties of the model: -->
채널 인스턴스를 얻었다면, `listen` 메서드에서 원하는 이벤트를 구독할 수 있습니다. 모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉터리에 실제 이벤트 클래스가 존재하지 않으므로, [event name](#model-broadcasting-event-conventions)에 반드시 `.`(점)을 접두사로 붙여 네임스페이스에 소속되지 않았음을 표시해야 합니다. 각 모델 브로드캐스트 이벤트에는 `model` 속성이 포함되어, 모델의 브로드캐스트 속성 전체가 전달됩니다.

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.PostUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="client-events"></a>

<!-- ## Client Events -->
## Client Events

> [!TIP]
> [Pusher Channels](https://pusher.com/channels)를 사용할 때는, 클라이언트 이벤트를 전송하려면 [application dashboard](https://dashboard.pusher.com/)의 "App Settings" 섹션에서 "Client Events" 옵션을 반드시 활성화해야 합니다.

<!-- Sometimes you may wish to broadcast an event to other connected clients without hitting your Laravel application at all. This can be particularly useful for things like "typing" notifications, where you want to alert users of your application that another user is typing a message on a given screen. -->
때로는 Laravel 애플리케이션 서버를 거치지 않고, 다른 연결된 클라이언트들에게 직접 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 예를 들어, 어떤 사용자가 화면에서 메시지를 입력하고 있다는 사실을 다른 사용자에게 알리는 "입력 중" 알림과 같은 경우에 매우 유용하게 사용할 수 있습니다.

<!-- To broadcast client events, you may use Echo's `whisper` method: -->
클라이언트 이벤트를 브로드캐스트하려면 Echo의 `whisper` 메서드를 사용할 수 있습니다.

```
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

<!-- To listen for client events, you may use the `listenForWhisper` method: -->
클라이언트 이벤트를 수신하려면 `listenForWhisper` 메서드를 사용합니다.

```
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

<a name="notifications"></a>

<!-- ## Notifications -->
## Notifications

<!-- By pairing event broadcasting with [notifications](/docs/8.x/notifications), your JavaScript application may receive new notifications as they occur without needing to refresh the page. Before getting started, be sure to read over the documentation on using [the broadcast notification channel](/docs/8.x/notifications#broadcast-notifications). -->
이벤트 브로드캐스팅을 [notifications](/docs/8.x/notifications) 기능과 연동하면, 자바스크립트 애플리케이션이 페이지를 새로고침하지 않아도 새로운 알림이 도착하면 실시간으로 받아볼 수 있습니다. 시작하기 전에 [the broadcast notification channel](/docs/8.x/notifications#broadcast-notifications) 사용법에 관한 문서를 반드시 먼저 살펴보시기 바랍니다.

<!-- Once you have configured a notification to use the broadcast channel, you may listen for the broadcast events using Echo's `notification` method. Remember, the channel name should match the class name of the entity receiving the notifications: -->
알림이 브로드캐스트 채널을 사용하도록 설정됐다면, Echo의 `notification` 메서드를 사용해 브로드캐스트 알림 이벤트를 수신할 수 있습니다. 이때, 채널 이름은 알림을 받는 엔티티의 클래스명을 기준으로 해야 합니다.

```
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<!-- In this example, all notifications sent to `App\Models\User` instances via the `broadcast` channel would be received by the callback. A channel authorization callback for the `App.Models.User.{id}` channel is included in the default `BroadcastServiceProvider` that ships with the Laravel framework. -->
이 예시에서는, `broadcast` 채널을 통해 `App\Models\User` 인스턴스에 전달되는 모든 알림이 위 콜백에서 받아집니다. Laravel 프레임워크에서는 기본적으로 제공하는 `BroadcastServiceProvider`에 `App.Models.User.{id}` 채널에 대한 채널 인가 콜백이 포함되어 있습니다.
