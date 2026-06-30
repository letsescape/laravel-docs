<!-- # Broadcasting -->
# Broadcasting

- [Introduction](#introduction)
- [Quickstart](#quickstart)
- [Server Side Installation](#server-side-installation)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [Client Side Installation](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [Concept Overview](#concept-overview)
    - [Using an Example Application](#using-example-application)
- [Defining Broadcast Events](#defining-broadcast-events)
    - [Broadcast Name](#broadcast-name)
    - [Broadcast Data](#broadcast-data)
    - [Broadcast Queue](#broadcast-queue)
    - [Broadcast Conditions](#broadcast-conditions)
    - [Broadcasting and Database Transactions](#broadcasting-and-database-transactions)
- [Authorizing Channels](#authorizing-channels)
    - [Defining Authorization Callbacks](#defining-authorization-callbacks)
    - [Defining Channel Classes](#defining-channel-classes)
- [Broadcasting Events](#broadcasting-events)
    - [Only to Others](#only-to-others)
    - [Customizing the Connection](#customizing-the-connection)
    - [Anonymous Events](#anonymous-events)
    - [Rescuing Broadcasts](#rescuing-broadcasts)
- [Receiving Broadcasts](#receiving-broadcasts)
    - [Listening for Events](#listening-for-events)
    - [Leaving a Channel](#leaving-a-channel)
    - [Namespaces](#namespaces)
    - [Using React or Vue](#using-react-or-vue)
- [Presence Channels](#presence-channels)
    - [Authorizing Presence Channels](#authorizing-presence-channels)
    - [Joining Presence Channels](#joining-presence-channels)
    - [Broadcasting to Presence Channels](#broadcasting-to-presence-channels)
- [Model Broadcasting](#model-broadcasting)
    - [Model Broadcasting Conventions](#model-broadcasting-conventions)
    - [Listening for Model Broadcasts](#listening-for-model-broadcasts)
- [Client Events](#client-events)
- [Notifications](#notifications)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In many modern web applications, WebSockets are used to implement realtime, live-updating user interfaces. When some data is updated on the server, a message is typically sent over a WebSocket connection to be handled by the client. WebSockets provide a more efficient alternative to continually polling your application's server for data changes that should be reflected in your UI. -->
많은 최신 웹 애플리케이션에서 WebSocket은 실시간으로 업데이트되는 사용자 인터페이스를 구현하는 데 사용됩니다. 서버에서 일부 데이터가 업데이트되면 일반적으로 클라이언트에서 처리할 메시지가 WebSocket 연결을 통해 전송됩니다. WebSocket은 UI에 반영되어야 하는 데이터 변경 사항에 대해 애플리케이션 서버를 지속적으로 폴링하는 보다 효율적인 대안을 제공합니다.

<!-- For example, imagine your application is able to export a user's data to a CSV file and email it to them. However, creating this CSV file takes several minutes so you choose to create and mail the CSV within a [queued job](/docs/12.x/queues). When the CSV has been created and mailed to the user, we can use event broadcasting to dispatch an `App\Events\UserDataExported` event that is received by our application's JavaScript. Once the event is received, we can display a message to the user that their CSV has been emailed to them without them ever needing to refresh the page. -->
예를 들어, 애플리케이션이 사용자의 데이터를 CSV 파일로 내보내고 이메일로 보낼 수 있다고 가정해 보세요. 그러나 이 CSV 파일을 생성하는 데는 몇 분이 걸리므로 [queued job](/docs/12.x/queues) 내에서 CSV를 생성하여 메일로 보내도록 선택하세요. CSV가 생성되어 사용자에게 메일로 전송되면 애플리케이션의 JavaScript에서 수신한 디스패치 및 `App\Events\UserDataExported` 이벤트에 대한 이벤트 브로드캐스팅을 사용할 수 있습니다. 이벤트가 수신되면 사용자가 페이지를 새로 고칠 필요 없이 CSV가 이메일로 전송되었다는 메시지를 사용자에게 표시할 수 있습니다.

<!-- To assist you in building these types of features, Laravel makes it easy to "broadcast" your server-side Laravel [events](/docs/12.x/events) over a WebSocket connection. Broadcasting your Laravel events allows you to share the same event names and data between your server-side Laravel application and your client-side JavaScript application. -->
이러한 유형의 기능을 구축하는 데 도움을 주기 위해 Laravel을 사용하면 WebSocket 연결을 통해 서버측 Laravel [events](/docs/12.x/events)를 쉽게 "브로드캐스트"할 수 있습니다. Laravel 이벤트를 브로드캐스트하면 서버 측 Laravel 애플리케이션과 클라이언트 측 JavaScript 애플리케이션 간에 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

<!-- The core concepts behind broadcasting are simple: clients connect to named channels on the frontend, while your Laravel application broadcasts events to these channels on the backend. These events can contain any additional data you wish to make available to the frontend. -->
브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트는 프론트엔드의 명명된 채널에 연결하고, Laravel 애플리케이션은 백엔드의 이러한 채널에 이벤트를 브로드캐스트합니다. 이러한 이벤트에는 프론트엔드에서 사용할 수 있도록 하려는 추가 데이터가 포함될 수 있습니다.

<a name="supported-drivers"></a>
<!-- #### Supported Drivers -->
#### Supported Drivers

<!-- By default, Laravel includes three server-side broadcasting drivers for you to choose from: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), and [Ably](https://ably.com). -->
기본적으로 Laravel에는 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels) 및 [Ably](https://ably.com) 중에서 선택할 수 있는 세 가지 서버 측 브로드캐스트 드라이버가 포함되어 있습니다.

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전에 [events and listeners](/docs/12.x/events)에 대한 Laravel 설명서를 읽어보세요.

<a name="quickstart"></a>
<!-- ## Quickstart -->
## Quickstart

<!-- By default, broadcasting is not enabled in new Laravel applications. You may enable broadcasting using the `install:broadcasting` Artisan command: -->
기본적으로 새로운 Laravel 애플리케이션에서는 브로드캐스팅이 활성화되지 않습니다. `install:broadcasting` Artisan 명령을 사용하여 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan install:broadcasting
```

<!-- The `install:broadcasting` command will prompt you for which event broadcasting service you would like to use. In addition, it will create the `config/broadcasting.php` configuration file and the `routes/channels.php` file where you may register your application's broadcast authorization routes and callbacks. -->
`install:broadcasting` 명령은 사용하려는 이벤트 브로드캐스팅 서비스를 묻는 메시지를 표시합니다. 또한 애플리케이션의 브로드캐스트 인가 라우트 및 콜백을 등록할 수 있는 `config/broadcasting.php` 구성 파일과 `routes/channels.php` 파일을 생성합니다.

<!-- Laravel supports several broadcast drivers out of the box: [Laravel Reverb](/docs/12.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), and a `log` driver for local development and debugging. Additionally, a `null` driver is included which allows you to disable broadcasting during testing. A configuration example is included for each of these drivers in the `config/broadcasting.php` configuration file. -->
Laravel는 기본적으로 여러 브로드캐스트 드라이버를 지원합니다. [Laravel Reverb](/docs/12.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 및 로컬 개발을 위한 `log` 드라이버 디버깅. 또한 테스트 시 브로드캐스팅을 비활성화할 수 있는 `null` 드라이버가 포함되어 있습니다. `config/broadcasting.php` 구성 파일에는 이러한 각 드라이버에 대한 구성 예가 포함되어 있습니다.

<!-- All of your application's event broadcasting configuration is stored in the `config/broadcasting.php` configuration file. Don't worry if this file does not exist in your application; it will be created when you run the `install:broadcasting` Artisan command. -->
애플리케이션의 모든 이벤트 브로드캐스팅 구성은 `config/broadcasting.php` 구성 파일에 저장됩니다. 이 파일이 애플리케이션에 존재하지 않더라도 걱정하지 마세요. `install:broadcasting` Artisan 명령을 실행할 때 생성됩니다.

<a name="quickstart-next-steps"></a>
<!-- #### Next Steps -->
#### Next Steps

<!-- Once you have enabled event broadcasting, you're ready to learn more about [defining broadcast events](#defining-broadcast-events) and [listening for events](#listening-for-events). If you're using Laravel's React or Vue [starter kits](/docs/12.x/starter-kits), you may listen for events using Echo's [useEcho hook](#using-react-or-vue). -->
이벤트 브로드캐스팅을 활성화하면 [defining broadcast events](#defining-broadcast-events) 및 [listening for events](#listening-for-events)에 대해 자세히 알아볼 수 있습니다. Laravel의 React 또는 Vue [starter kits](/docs/12.x/starter-kits)를 사용하는 경우 Echo의 [useEcho hook](#using-react-or-vue)를 사용하여 이벤트를 수신할 수 있습니다.

> [!NOTE]
> 이벤트를 브로드캐스트하기 전에 먼저 [queue worker](/docs/12.x/queues)를 구성하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐 작업을 통해 수행되므로 애플리케이션의 응답 시간은 브로드캐스트되는 이벤트로 인해 심각한 영향을 받지 않습니다.

<a name="server-side-installation"></a>
<!-- ## Server Side Installation -->
## Server Side Installation

<!-- To get started using Laravel's event broadcasting, we need to do some configuration within the Laravel application as well as install a few packages. -->
Laravel의 이벤트 브로드캐스팅 사용을 시작하려면 Laravel 애플리케이션 내에서 일부 구성을 수행하고 몇 가지 패키지를 설치해야 합니다.

<!-- Event broadcasting is accomplished by a server-side broadcasting driver that broadcasts your Laravel events so that Laravel Echo (a JavaScript library) can receive them within the browser client. Don't worry - we'll walk through each part of the installation process step-by-step. -->
이벤트 브로드캐스팅은 Laravel Echo(JavaScript 라이브러리)가 브라우저 클라이언트 내에서 수신할 수 있도록 Laravel 이벤트를 브로드캐스트하는 서버 측 브로드캐스트 드라이버에 의해 수행됩니다. 걱정하지 마세요. 설치 과정의 각 부분을 단계별로 안내해 드리겠습니다.

<a name="reverb"></a>
<!-- ### Reverb -->
### Reverb

<!-- To quickly enable support for Laravel's broadcasting features while using Reverb as your event broadcaster, invoke the `install:broadcasting` Artisan command with the `--reverb` option. This Artisan command will install Reverb's required Composer and NPM packages and update your application's `.env` file with the appropriate variables: -->
Reverb를 이벤트 브로드캐스터로 사용하는 동안 Laravel의 브로드캐스팅 기능에 대한 지원을 빠르게 활성화하려면 `--reverb` 옵션과 함께 `install:broadcasting` Artisan 명령을 호출하십시오. 이 Artisan 명령은 Reverb의 필수 Composer 및 NPM 패키지를 설치하고 애플리케이션의 `.env` 파일을 적절한 변수로 업데이트합니다.

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- When running the `install:broadcasting` command, you will be prompted to install [Laravel Reverb](/docs/12.x/reverb). Of course, you may also install Reverb manually using the Composer package manager: -->
`install:broadcasting` 명령을 실행하면 [Laravel Reverb](/docs/12.x/reverb)를 설치하라는 메시지가 표시됩니다. 물론 Composer 패키지 관리자를 사용하여 Reverb를 수동으로 설치할 수도 있습니다.

```shell
composer require laravel/reverb
```

<!-- Once the package is installed, you may run Reverb's installation command to publish the configuration, add Reverb's required environment variables, and enable event broadcasting in your application: -->
패키지가 설치되면 Reverb의 설치 명령을 실행하여 구성을 게시하고 Reverb의 필수 환경 변수를 추가하고 애플리케이션에서 이벤트 브로드캐스팅을 활성화할 수 있습니다.

```shell
php artisan reverb:install
```

<!-- You can find detailed Reverb installation and usage instructions in the [Reverb documentation](/docs/12.x/reverb). -->
[Reverb documentation](/docs/12.x/reverb)에서 자세한 Reverb 설치 및 사용 지침을 확인할 수 있습니다.

<a name="pusher-channels"></a>
<!-- ### Pusher Channels -->
### Pusher Channels

<!-- To quickly enable support for Laravel's broadcasting features while using Pusher as your event broadcaster, invoke the `install:broadcasting` Artisan command with the `--pusher` option. This Artisan command will prompt you for your Pusher credentials, install the Pusher PHP and JavaScript SDKs, and update your application's `.env` file with the appropriate variables: -->
Pusher를 이벤트 브로드캐스터로 사용하는 동안 Laravel의 브로드캐스팅 기능에 대한 지원을 빠르게 활성화하려면 `--pusher` 옵션과 함께 `install:broadcasting` Artisan 명령을 호출하세요. 이 Artisan 명령은 Pusher 자격 증명을 묻는 메시지를 표시하고, Pusher PHP 및 JavaScript SDK를 설치하고, 애플리케이션의 `.env` 파일을 적절한 변수로 업데이트합니다.

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- To install Pusher support manually, you should install the Pusher Channels PHP SDK using the Composer package manager: -->
푸셔 지원을 수동으로 설치하려면 Composer 패키지 관리자를 사용하여 푸셔 채널 PHP SDK를 설치해야 합니다.

```shell
composer require pusher/pusher-php-server
```

<!-- Next, you should configure your Pusher Channels credentials in the `config/broadcasting.php` configuration file. An example Pusher Channels configuration is already included in this file, allowing you to quickly specify your key, secret, and application ID. Typically, you should configure your Pusher Channels credentials in your application's `.env` file: -->
다음으로 `config/broadcasting.php` 구성 파일에서 푸셔 채널 자격 증명을 구성해야 합니다. 푸셔 채널 구성 예시가 이 파일에 이미 포함되어 있어 키, 비밀 및 애플리케이션 ID를 빠르게 지정할 수 있습니다. 일반적으로 애플리케이션의 `.env` 파일에서 푸셔 채널 자격 증명을 구성해야 합니다.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

<!-- The `config/broadcasting.php` file's `pusher` configuration also allows you to specify additional `options` that are supported by Channels, such as the cluster. -->
`config/broadcasting.php` 파일의 `pusher` 구성을 사용하면 클러스터와 같은 채널에서 지원되는 추가 `options`를 지정할 수도 있습니다.

<!-- Then, set the `BROADCAST_CONNECTION` environment variable to `pusher` in your application's `.env` file: -->
그런 다음 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 설정합니다.

```ini
BROADCAST_CONNECTION=pusher
```

<!-- Finally, you are ready to install and configure [Laravel Echo](#client-side-installation), which will receive the broadcast events on the client-side. -->
마지막으로 클라이언트 측에서 브로드캐스트 이벤트를 수신하는 [Laravel Echo](#client-side-installation)를 설치하고 구성할 준비가 되었습니다.

<a name="ably"></a>
<!-- ### Ably -->
### Ably

> [!NOTE]
> 아래 문서에서는 "푸셔 호환성" 모드에서 Ably를 사용하는 방법을 설명합니다. 그러나 Ably 팀은 Ably가 제공하는 고유한 기능을 활용할 수 있는 브로드캐스터와 Echo 클라이언트를 권장하고 유지 관리합니다. Ably에서 유지 관리하는 드라이버 사용에 대한 자세한 내용은 [consult Ably's Laravel broadcaster documentation](https://github.com/ably/laravel-broadcaster)하세요.

<!-- To quickly enable support for Laravel's broadcasting features while using [Ably](https://ably.com) as your event broadcaster, invoke the `install:broadcasting` Artisan command with the `--ably` option. This Artisan command will prompt you for your Ably credentials, install the Ably PHP and JavaScript SDKs, and update your application's `.env` file with the appropriate variables: -->
[Ably](https://ably.com)를 이벤트 브로드캐스터로 사용하는 동안 Laravel의 브로드캐스팅 기능에 대한 지원을 빠르게 활성화하려면 `--ably` 옵션과 함께 `install:broadcasting` Artisan 명령을 호출하세요. 이 Artisan 명령은 Ably 자격 증명을 묻는 메시지를 표시하고, Ably PHP 및 JavaScript SDK를 설치하고, 애플리케이션의 `.env` 파일을 적절한 변수로 업데이트합니다.

```shell
php artisan install:broadcasting --ably
```

<!-- **Before continuing, you should enable Pusher protocol support in your Ably application settings. You may enable this feature within the "Protocol Adapter Settings" portion of your Ably application's settings dashboard.** -->
**계속하기 전에 Ably 애플리케이션 설정에서 푸셔 프로토콜 지원을 활성화해야 합니다. Ably 애플리케이션 설정 대시보드의 "프로토콜 어댑터 설정" 부분에서 이 기능을 활성화할 수 있습니다.**

<a name="ably-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- To install Ably support manually, you should install the Ably PHP SDK using the Composer package manager: -->
Ably 지원을 수동으로 설치하려면 Composer 패키지 관리자를 사용하여 Ably PHP SDK를 설치해야 합니다.

```shell
composer require ably/ably-php
```

<!-- Next, you should configure your Ably credentials in the `config/broadcasting.php` configuration file. An example Ably configuration is already included in this file, allowing you to quickly specify your key. Typically, this value should be set via the `ABLY_KEY` [environment variable](/docs/12.x/configuration#environment-configuration): -->
다음으로 `config/broadcasting.php` 구성 파일에서 Ably 자격 증명을 구성해야 합니다. 이 파일에는 Ably 구성 예시가 이미 포함되어 있어 키를 빠르게 지정할 수 있습니다. 일반적으로 이 값은 `ABLY_KEY` [environment variable](/docs/12.x/configuration#environment-configuration)를 통해 설정되어야 합니다.

```ini
ABLY_KEY=your-ably-key
```

<!-- Then, set the `BROADCAST_CONNECTION` environment variable to `ably` in your application's `.env` file: -->
그런 다음 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 설정합니다.

```ini
BROADCAST_CONNECTION=ably
```

<!-- Finally, you are ready to install and configure [Laravel Echo](#client-side-installation), which will receive the broadcast events on the client-side. -->
마지막으로 클라이언트 측에서 브로드캐스트 이벤트를 수신하는 [Laravel Echo](#client-side-installation)를 설치하고 구성할 준비가 되었습니다.

<a name="client-side-installation"></a>
<!-- ## Client Side Installation -->
## Client Side Installation

<a name="client-reverb"></a>
<!-- ### Reverb -->
### Reverb

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. -->
[Laravel Echo](https://github.com/laravel/echo)는 채널을 구독하고 서버 측 브로드캐스트 드라이버에서 브로드캐스트하는 이벤트를 수신하기 쉽게 해주는 JavaScript 라이브러리입니다.

<!-- When installing Laravel Reverb via the `install:broadcasting` Artisan command, Reverb and Echo's scaffolding and configuration will be injected into your application automatically. However, if you wish to manually configure Laravel Echo, you may do so by following the instructions below. -->
`install:broadcasting` Artisan 명령을 통해 Laravel Reverb를 설치하면 Reverb와 Echo의 스캐폴딩 및 구성이 자동으로 애플리케이션에 주입됩니다. 그러나 Laravel Echo를 수동으로 구성하려면 아래 지침을 따르면 됩니다.

<a name="reverb-client-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- To manually configure Laravel Echo for your application's frontend, first install the `pusher-js` package since Reverb utilizes the Pusher protocol for WebSocket subscriptions, channels, and messages: -->
애플리케이션의 프론트엔드에 대해 Laravel Echo를 수동으로 구성하려면 먼저 `pusher-js` 패키지를 설치하십시오. Reverb는 WebSocket 구독, 채널 및 메시지에 대해 Pusher 프로토콜을 사용하기 때문입니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's JavaScript. A great place to do this is at the bottom of the `resources/js/bootstrap.js` file that is included with the Laravel framework: -->
Echo가 설치되면 애플리케이션의 JavaScript에 새로운 Echo 인스턴스를 생성할 준비가 된 것입니다. 이를 수행하기 가장 좋은 위치는 Laravel 프레임워크에 포함된 `resources/js/bootstrap.js` 파일의 하단입니다.

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT ?? 80,
    wssPort: import.meta.env.VITE_REVERB_PORT ?? 443,
    forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

<!-- Next, you should compile your application's assets: -->
다음으로 애플리케이션 자산을 컴파일해야 합니다.

```shell
npm run build
```

> [!WARNING]
> Laravel Echo `reverb` 브로드캐스터에는 laravel-echo v1.16.0+가 필요합니다.

<a name="client-pusher-channels"></a>
<!-- ### Pusher Channels -->
### Pusher Channels

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. -->
[Laravel Echo](https://github.com/laravel/echo)는 채널을 구독하고 서버 측 브로드캐스트 드라이버에서 브로드캐스트하는 이벤트를 수신하기 쉽게 해주는 JavaScript 라이브러리입니다.

<!-- When installing broadcasting support via the `install:broadcasting --pusher` Artisan command, Pusher and Echo's scaffolding and configuration will be injected into your application automatically. However, if you wish to manually configure Laravel Echo, you may do so by following the instructions below. -->
`install:broadcasting --pusher` Artisan 명령을 통해 브로드캐스팅 지원을 설치하면 Pusher와 Echo의 스캐폴딩 및 구성이 자동으로 애플리케이션에 주입됩니다. 그러나 Laravel Echo를 수동으로 구성하려면 아래 지침을 따르면 됩니다.

<a name="pusher-client-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- To manually configure Laravel Echo for your application's frontend, first install the `laravel-echo` and `pusher-js` packages which utilize the Pusher protocol for WebSocket subscriptions, channels, and messages: -->
애플리케이션의 프론트엔드에 대해 Laravel Echo를 수동으로 구성하려면 먼저 WebSocket 구독, 채널 및 메시지에 대해 Pusher 프로토콜을 활용하는 `laravel-echo` 및 `pusher-js` 패키지를 설치하십시오.

```shell
npm install --save-dev laravel-echo pusher-js
```

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's `resources/js/bootstrap.js` file: -->
Echo가 설치되면 애플리케이션의 `resources/js/bootstrap.js` 파일에 새로운 Echo 인스턴스를 생성할 준비가 된 것입니다.

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    forceTLS: true
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

<!-- Next, you should define the appropriate values for the Pusher environment variables in your application's `.env` file. If these variables do not already exist in your `.env` file, you should add them: -->
다음으로, 애플리케이션의 `.env` 파일에서 Pusher 환경 변수에 대한 적절한 값을 정의해야 합니다. 이러한 변수가 `.env` 파일에 아직 없으면 추가해야 합니다.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"

VITE_APP_NAME="${APP_NAME}"
VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_HOST="${PUSHER_HOST}"
VITE_PUSHER_PORT="${PUSHER_PORT}"
VITE_PUSHER_SCHEME="${PUSHER_SCHEME}"
VITE_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"
```

<!-- Once you have adjusted the Echo configuration according to your application's needs, you may compile your application's assets: -->
애플리케이션의 필요에 따라 Echo 구성을 조정한 후에는 애플리케이션의 자산을 컴파일할 수 있습니다.

```shell
npm run build
```

> [!NOTE]
> 애플리케이션의 JavaScript 자산 컴파일에 대한 자세한 내용은 [Vite](/docs/12.x/vite) 문서를 참조하세요.

<a name="using-an-existing-client-instance"></a>
<!-- #### Using an Existing Client Instance -->
#### Using an Existing Client Instance

<!-- If you already have a pre-configured Pusher Channels client instance that you would like Echo to utilize, you may pass it to Echo via the `client` configuration option: -->
Echo가 활용하려는 사전 구성된 푸셔 채널 클라이언트 인스턴스가 이미 있는 경우 `client` 구성 옵션을 통해 이를 Echo에 전달할 수 있습니다.

```js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

const options = {
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY
}

window.Echo = new Echo({
    ...options,
    client: new Pusher(options.key, options)
});
```

<a name="client-ably"></a>
<!-- ### Ably -->
### Ably

> [!NOTE]
> 아래 문서에서는 "푸셔 호환성" 모드에서 Ably를 사용하는 방법을 설명합니다. 그러나 Ably 팀은 Ably가 제공하는 고유한 기능을 활용할 수 있는 브로드캐스터와 Echo 클라이언트를 권장하고 유지 관리합니다. Ably에서 유지 관리하는 드라이버 사용에 대한 자세한 내용은 [consult Ably's Laravel broadcaster documentation](https://github.com/ably/laravel-broadcaster)하세요.

<!-- [Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver. -->
[Laravel Echo](https://github.com/laravel/echo)는 채널을 구독하고 서버 측 브로드캐스트 드라이버에서 브로드캐스트하는 이벤트를 수신하기 쉽게 해주는 JavaScript 라이브러리입니다.

<!-- When installing broadcasting support via the `install:broadcasting --ably` Artisan command, Ably and Echo's scaffolding and configuration will be injected into your application automatically. However, if you wish to manually configure Laravel Echo, you may do so by following the instructions below. -->
`install:broadcasting --ably` Artisan 명령을 통해 브로드캐스팅 지원을 설치하면 Ably 및 Echo의 스캐폴딩 및 구성이 자동으로 애플리케이션에 주입됩니다. 그러나 Laravel Echo를 수동으로 구성하려면 아래 지침을 따르면 됩니다.

<a name="ably-client-manual-installation"></a>
<!-- #### Manual Installation -->
#### Manual Installation

<!-- To manually configure Laravel Echo for your application's frontend, first install the `laravel-echo` and `pusher-js` packages which utilize the Pusher protocol for WebSocket subscriptions, channels, and messages: -->
애플리케이션의 프론트엔드에 대해 Laravel Echo를 수동으로 구성하려면 먼저 WebSocket 구독, 채널 및 메시지에 대해 Pusher 프로토콜을 활용하는 `laravel-echo` 및 `pusher-js` 패키지를 설치하십시오.

```shell
npm install --save-dev laravel-echo pusher-js
```

<!-- **Before continuing, you should enable Pusher protocol support in your Ably application settings. You may enable this feature within the "Protocol Adapter Settings" portion of your Ably application's settings dashboard.** -->
**계속하기 전에 Ably 애플리케이션 설정에서 푸셔 프로토콜 지원을 활성화해야 합니다. Ably 애플리케이션 설정 대시보드의 "프로토콜 어댑터 설정" 부분에서 이 기능을 활성화할 수 있습니다.**

<!-- Once Echo is installed, you are ready to create a fresh Echo instance in your application's `resources/js/bootstrap.js` file: -->
Echo가 설치되면 애플리케이션의 `resources/js/bootstrap.js` 파일에 새로운 Echo 인스턴스를 생성할 준비가 된 것입니다.

```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    wsHost: 'realtime-pusher.ably.io',
    wsPort: 443,
    disableStats: true,
    encrypted: true,
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

<!-- You may have noticed our Ably Echo configuration references a `VITE_ABLY_PUBLIC_KEY` environment variable. This variable's value should be your Ably public key. Your public key is the portion of your Ably key that occurs before the `:` character. -->
Ably Echo 구성이 `VITE_ABLY_PUBLIC_KEY` 환경 변수를 참조하는 것을 확인하셨을 것입니다. 이 변수의 값은 Ably 공개 키여야 합니다. 공개 키는 `:` 문자 앞에 나오는 Ably 키 부분입니다.

<!-- Once you have adjusted the Echo configuration according to your needs, you may compile your application's assets: -->
필요에 따라 Echo 구성을 조정한 후에는 애플리케이션 자산을 컴파일할 수 있습니다.

```shell
npm run dev
```

> [!NOTE]
> 애플리케이션의 JavaScript 자산 컴파일에 대한 자세한 내용은 [Vite](/docs/12.x/vite) 문서를 참조하세요.

<a name="concept-overview"></a>
<!-- ## Concept Overview -->
## Concept Overview

<!-- Laravel's event broadcasting allows you to broadcast your server-side Laravel events to your client-side JavaScript application using a driver-based approach to WebSockets. Currently, Laravel ships with [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), and [Ably](https://ably.com) drivers. The events may be easily consumed on the client-side using the [Laravel Echo](#client-side-installation) JavaScript package. -->
Laravel의 이벤트 브로드캐스팅을 사용하면 WebSocket에 대한 드라이버 기반 접근 방식을 사용하여 서버 측 Laravel 이벤트를 클라이언트 측 JavaScript 애플리케이션에 브로드캐스트할 수 있습니다. 현재 Laravel는 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels) 및 [Ably](https://ably.com) 드라이버와 함께 제공됩니다. 이벤트는 [Laravel Echo](#client-side-installation) JavaScript 패키지를 사용하여 클라이언트 측에서 쉽게 사용할 수 있습니다.

<!-- Events are broadcast over "channels", which may be specified as public or private. Any visitor to your application may subscribe to a public channel without any authentication or authorization; however, in order to subscribe to a private channel, a user must be authenticated and authorized to listen on that channel. -->
이벤트는 공개 또는 비공개로 지정될 수 있는 "채널"을 통해 브로드캐스트됩니다. 애플리케이션을 방문하는 모든 방문자는 인증이나 인가 없이 공개 채널을 구독할 수 있습니다. 그러나 비공개 채널을 구독하려면 사용자가 해당 채널을 수신할 수 있도록 인증 및 인가를 받아야 합니다.

<a name="using-example-application"></a>
<!-- ### Using an Example Application -->
### Using an Example Application

<!-- Before diving into each component of event broadcasting, let's take a high level overview using an e-commerce store as an example. -->
이벤트 브로드캐스팅의 각 구성요소를 살펴보기 전에 전자상거래 상점을 예로 들어 높은 수준의 개요를 살펴보겠습니다.

<!-- In our application, let's assume we have a page that allows users to view the shipping status for their orders. Let's also assume that an `OrderShipmentStatusUpdated` event is fired when a shipping status update is processed by the application: -->
우리 애플리케이션에는 사용자가 주문의 배송 상태를 확인할 수 있는 페이지가 있다고 가정해 보겠습니다. 또한 애플리케이션에서 배송 상태 업데이트를 처리할 때 `OrderShipmentStatusUpdated` 이벤트가 실행된다고 가정해 보겠습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
<!-- #### The `ShouldBroadcast` Interface -->
#### The `ShouldBroadcast` Interface

<!-- When a user is viewing one of their orders, we don't want them to have to refresh the page to view status updates. Instead, we want to broadcast the updates to the application as they are created. So, we need to mark the `OrderShipmentStatusUpdated` event with the `ShouldBroadcast` interface. This will instruct Laravel to broadcast the event when it is fired: -->
사용자가 주문 중 하나를 볼 때 상태 업데이트를 확인하기 위해 페이지를 새로 고칠 필요가 없습니다. 대신, 업데이트가 생성될 때 애플리케이션에 업데이트를 브로드캐스트하려고 합니다. 따라서 `OrderShipmentStatusUpdated` 이벤트를 `ShouldBroadcast` 인터페이스로 표시해야 합니다. 이는 Laravel가 실행될 때 이벤트를 브로드캐스트하도록 지시합니다.

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    /**
     * The order instance.
     *
     * @var \App\Models\Order
     */
    public $order;
}
```

<!-- The `ShouldBroadcast` interface requires our event to define a `broadcastOn` method. This method is responsible for returning the channels that the event should broadcast on. An empty stub of this method is already defined on generated event classes, so we only need to fill in its details. We only want the creator of the order to be able to view status updates, so we will broadcast the event on a private channel that is tied to the order: -->
`ShouldBroadcast` 인터페이스는 이벤트에 `broadcastOn` 메서드를 정의할 것을 요구합니다. 이 메서드는 이벤트가 브로드캐스트해야 하는 채널을 반환하는 역할을 합니다. 이 메서드의 빈 스텁은 생성된 이벤트 클래스에 이미 정의되어 있으므로 세부 내용만 채우면 됩니다. 주문 생성자만 상태 업데이트를 볼 수 있도록 하기 위해, 주문과 연결된 비공개 채널에서 이벤트를 브로드캐스트합니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channel the event should broadcast on.
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

<!-- If you wish the event to broadcast on multiple channels, you may return an `array` instead: -->
이벤트를 여러 채널로 브로드캐스트하려면 대신 `array`를 반환하면 됩니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels the event should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PrivateChannel('orders.'.$this->order->id),
        // ...
    ];
}
```

<a name="example-application-authorizing-channels"></a>
<!-- #### Authorizing Channels -->
#### Authorizing Channels

<!-- Remember, users must be authorized to listen on private channels. We may define our channel authorization rules in our application's `routes/channels.php` file. In this example, we need to verify that any user attempting to listen on the private `orders.1` channel is actually the creator of the order: -->
사용자는 비공개 채널을 수신하기 위해 인가를 받아야 합니다. 애플리케이션의 `routes/channels.php` 파일에서 채널 인가 규칙을 정의할 수 있습니다. 이 예에서는 비공개 `orders.1` 채널에서 수신을 시도하는 모든 사용자가 실제로 주문을 생성한 사람인지 확인해야 합니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

<!-- The `channel` method accepts two arguments: the name of the channel and a callback which returns `true` or `false` indicating whether the user is authorized to listen on the channel. -->
`channel` 메서드는 채널 이름과 사용자가 채널에서 수신할 수 있는 권한이 있는지 여부를 나타내는 `true` 또는 `false`를 반환하는 콜백이라는 두 가지 인수를 허용합니다.

<!-- All authorization callbacks receive the currently authenticated user as their first argument and any additional wildcard parameters as their subsequent arguments. In this example, we are using the `{orderId}` placeholder to indicate that the "ID" portion of the channel name is a wildcard. -->
모든 인가 콜백은 현재 인증된 사용자를 첫 번째 인수로 받고 추가 와일드카드 매개변수를 후속 인수로 받습니다. 이 예에서는 `{orderId}` 자리 표시자를 사용하여 채널 이름의 "ID" 부분이 와일드카드임을 나타냅니다.

<a name="listening-for-event-broadcasts"></a>
<!-- #### Listening for Event Broadcasts -->
#### Listening for Event Broadcasts

<!-- Next, all that remains is to listen for the event in our JavaScript application. We can do this using [Laravel Echo](#client-side-installation). Laravel Echo's built-in React and Vue hooks make it simple to get started, and, by default, all of the event's public properties will be included on the broadcast event: -->
다음으로 남은 것은 JavaScript 애플리케이션에서 이벤트를 수신하는 것입니다. [Laravel Echo](#client-side-installation)를 사용하여 이 작업을 수행할 수 있습니다. Laravel Echo에 내장된 React 및 Vue 후크를 사용하면 쉽게 시작할 수 있으며 기본적으로 이벤트의 모든 공개 속성은 브로드캐스트 이벤트에 포함됩니다.

```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

<a name="defining-broadcast-events"></a>
<!-- ## Defining Broadcast Events -->
## Defining Broadcast Events

<!-- To inform Laravel that a given event should be broadcast, you must implement the `Illuminate\Contracts\Broadcasting\ShouldBroadcast` interface on the event class. This interface is already imported into all event classes generated by the framework so you may easily add it to any of your events. -->
지정된 이벤트가 브로드캐스트되어야 함을 Laravel에 알리려면 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 이미 프레임워크에서 생성된 모든 이벤트 클래스로 가져왔으므로 이벤트에 쉽게 추가할 수 있습니다.

<!-- The `ShouldBroadcast` interface requires you to implement a single method: `broadcastOn`. The `broadcastOn` method should return a channel or array of channels that the event should broadcast on. The channels should be instances of `Channel`, `PrivateChannel`, or `PresenceChannel`. Instances of `Channel` represent public channels that any user may subscribe to, while `PrivateChannels` and `PresenceChannels` represent private channels that require [channel authorization](#authorizing-channels): -->
`ShouldBroadcast` 인터페이스를 사용하려면 `broadcastOn`라는 단일 메서드를 구현해야 합니다. `broadcastOn` 메서드는 이벤트가 브로드캐스트해야 하는 채널 또는 채널 배열을 반환해야 합니다. 채널은 `Channel`, `PrivateChannel` 또는 `PresenceChannel`의 인스턴스여야 합니다. `Channel` 인스턴스는 모든 사용자가 구독할 수 있는 공개 채널을 나타내는 반면, `PrivateChannels` 및 `PresenceChannels`는 [channel authorization](#authorizing-channels)이 필요한 비공개 채널을 나타냅니다.

```php
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
     * Create a new event instance.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('user.'.$this->user->id),
        ];
    }
}
```

<!-- After implementing the `ShouldBroadcast` interface, you only need to [fire the event](/docs/12.x/events) as you normally would. Once the event has been fired, a [queued job](/docs/12.x/queues) will automatically broadcast the event using your specified broadcast driver. -->
`ShouldBroadcast` 인터페이스를 구현한 후에는 평소처럼 [fire the event](/docs/12.x/events)하기만 하면 됩니다. 이벤트가 실행되면 [queued job](/docs/12.x/queues)가 지정된 브로드캐스트 드라이버를 사용하여 자동으로 이벤트를 브로드캐스트합니다.

<a name="broadcast-name"></a>
<!-- ### Broadcast Name -->
### Broadcast Name

<!-- By default, Laravel will broadcast the event using the event's class name. However, you may customize the broadcast name by defining a `broadcastAs` method on the event: -->
기본적으로 Laravel는 이벤트의 클래스 이름을 사용하여 이벤트를 브로드캐스트합니다. 그러나 이벤트에 `broadcastAs` 메서드를 정의하여 브로드캐스트 이름을 사용자 지정할 수 있습니다.

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

<!-- If you customize the broadcast name using the `broadcastAs` method, you should make sure to register your listener with a leading `.` character. This will instruct Echo to not prepend the application's namespace to the event: -->
`broadcastAs` 메서드를 사용하여 브로드캐스트 이름을 사용자 지정하는 경우 선행 `.` 문자로 리스너를 등록해야 합니다. 이렇게 하면 Echo가 애플리케이션의 네임스페이스를 이벤트 앞에 추가하지 않도록 지시합니다.

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
<!-- ### Broadcast Data -->
### Broadcast Data

<!-- When an event is broadcast, all of its `public` properties are automatically serialized and broadcast as the event's payload, allowing you to access any of its public data from your JavaScript application. So, for example, if your event has a single public `$user` property that contains an Eloquent model, the event's broadcast payload would be: -->
이벤트가 브로드캐스트되면 모든 `public` 속성이 자동으로 직렬화되고 이벤트의 페이로드로 브로드캐스트되므로 JavaScript 애플리케이션에서 공개 데이터에 액세스할 수 있습니다. 예를 들어 이벤트에 Eloquent 모델을 포함하는 단일 공개 `$user` 속성이 있는 경우 이벤트의 브로드캐스트 페이로드는 다음과 같습니다.

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

<!-- However, if you wish to have more fine-grained control over your broadcast payload, you may add a `broadcastWith` method to your event. This method should return the array of data that you wish to broadcast as the event payload: -->
그러나 브로드캐스트 페이로드를 보다 세밀하게 제어하려면 이벤트에 `broadcastWith` 메서드를 추가할 수 있습니다. 이 메서드는 이벤트 페이로드로 브로드캐스트하려는 데이터 배열을 반환해야 합니다.

```php
/**
 * Get the data to broadcast.
 *
 * @return array<string, mixed>
 */
public function broadcastWith(): array
{
    return ['id' => $this->user->id];
}
```

<a name="broadcast-queue"></a>
<!-- ### Broadcast Queue -->
### Broadcast Queue

<!-- By default, each broadcast event is placed on the default queue for the default queue connection specified in your `queue.php` configuration file. You may customize the queue connection and name used by the broadcaster by defining `connection` and `queue` properties on your event class: -->
기본적으로 각 브로드캐스트 이벤트는 `queue.php` 구성 파일에 지정된 기본 큐 연결에 대한 기본 큐에 배치됩니다. 이벤트 클래스에 `connection` 및 `queue` 속성을 정의하여 브로드캐스터에서 사용하는 큐 연결 및 이름을 사용자 지정할 수 있습니다.

```php
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
또는 이벤트에 `broadcastQueue` 메서드를 정의하여 큐 이름을 사용자 지정할 수도 있습니다.

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

<!-- If you would like to broadcast your event using the `sync` queue instead of the default queue driver, you can implement the `ShouldBroadcastNow` interface instead of `ShouldBroadcast`: -->
기본 큐 드라이버 대신 `sync` 큐를 사용하여 이벤트를 브로드캐스팅하려는 경우 `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현할 수 있습니다.

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    // ...
}
```

<a name="broadcast-conditions"></a>
<!-- ### Broadcast Conditions -->
### Broadcast Conditions

<!-- Sometimes you want to broadcast your event only if a given condition is true. You may define these conditions by adding a `broadcastWhen` method to your event class: -->
때때로 주어진 조건이 참인 경우에만 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 이벤트 클래스에 `broadcastWhen` 메서드를 추가하여 이러한 조건을 정의할 수 있습니다.

```php
/**
 * Determine if this event should broadcast.
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
<!-- #### Broadcasting and Database Transactions -->
#### Broadcasting and Database Transactions

<!-- When broadcast events are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your event depends on these models, unexpected errors can occur when the job that broadcasts the event is processed. -->
브로드캐스트 이벤트가 데이터베이스 트랜잭션 내의 디스패치인 경우 데이터베이스 트랜잭션이 커밋되기 전에 큐에 의해 처리될 수 있습니다. 이런 일이 발생하면 데이터베이스 트랜잭션 중에 모델 또는 데이터베이스 레코드에 대해 수행한 업데이트가 아직 데이터베이스에 반영되지 않을 수 있습니다. 또한 트랜잭션 내에서 생성된 모델 또는 데이터베이스 레코드가 데이터베이스에 존재하지 않을 수도 있습니다. 이벤트가 이러한 모델에 의존하는 경우 이벤트를 브로드캐스트하는 작업이 처리될 때 예기치 않은 오류가 발생할 수 있습니다.

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular broadcast event should be dispatched after all open database transactions have been committed by implementing the `ShouldDispatchAfterCommit` interface on the event class: -->
큐 연결의 `after_commit` 구성 옵션이 `false`로 설정된 경우에도 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현하여 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 후에도 특정 브로드캐스트 이벤트가 디스패치여야 함을 나타낼 수 있습니다.

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast, ShouldDispatchAfterCommit
{
    use SerializesModels;
}
```

> [!NOTE]
> 이러한 문제를 해결하는 방법에 대해 자세히 알아보려면 [queued jobs and database transactions](/docs/12.x/queues#jobs-and-database-transactions)에 관한 설명서를 검토하세요.

<a name="authorizing-channels"></a>
<!-- ## Authorizing Channels -->
## Authorizing Channels

<!-- Private channels require you to authorize that the currently authenticated user can actually listen on the channel. This is accomplished by making an HTTP request to your Laravel application with the channel name and allowing your application to determine if the user can listen on that channel. When using [Laravel Echo](#client-side-installation), the HTTP request to authorize subscriptions to private channels will be made automatically. -->
비공개 채널에서는 현재 인증된 사용자가 실제로 채널을 수신할 수 있도록 인가해야 합니다. 이는 채널 이름을 포함한 HTTP 요청을 Laravel 애플리케이션에 보내고, 애플리케이션이 사용자가 해당 채널을 수신할 수 있는지 여부를 결정하는 방식으로 수행됩니다. [Laravel Echo](#client-side-installation)를 사용하면 비공개 채널 구독을 인가하는 HTTP 요청이 자동으로 이루어집니다.

<!-- When broadcasting is installed Laravel attempts to automatically register the `/broadcasting/auth` route to handle authorization requests. If Laravel fails to automatically register these routes, you may register them manually in your application's `/bootstrap/app.php` file: -->
브로드캐스트가 설치되면 Laravel는 인가 요청을 처리하기 위해 `/broadcasting/auth` 라우트를 자동으로 등록하려고 시도합니다. Laravel가 이러한 라우트를 자동으로 등록하지 못하는 경우 애플리케이션의 `/bootstrap/app.php` 파일에 수동으로 등록할 수 있습니다.

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    channels: __DIR__.'/../routes/channels.php',
    health: '/up',
)
```

<a name="defining-authorization-callbacks"></a>
<!-- ### Defining Authorization Callbacks -->
### Defining Authorization Callbacks

<!-- Next, we need to define the logic that will actually determine if the currently authenticated user can listen to a given channel. This is done in the `routes/channels.php` file that was created by the `install:broadcasting` Artisan command. In this file, you may use the `Broadcast::channel` method to register channel authorization callbacks: -->
다음으로, 현재 인증된 사용자가 특정 채널을 수신할 수 있는지 실제로 결정하는 로직을 정의해야 합니다. 이는 `install:broadcasting` Artisan 명령으로 생성된 `routes/channels.php` 파일에서 수행됩니다. 이 파일에서는 `Broadcast::channel` 메서드를 사용하여 채널 인가 콜백을 등록할 수 있습니다.

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

<!-- The `channel` method accepts two arguments: the name of the channel and a callback which returns `true` or `false` indicating whether the user is authorized to listen on the channel. -->
`channel` 메서드는 채널 이름과 사용자가 채널에서 수신할 수 있는 권한이 있는지 여부를 나타내는 `true` 또는 `false`를 반환하는 콜백이라는 두 가지 인수를 허용합니다.

<!-- All authorization callbacks receive the currently authenticated user as their first argument and any additional wildcard parameters as their subsequent arguments. In this example, we are using the `{orderId}` placeholder to indicate that the "ID" portion of the channel name is a wildcard. -->
모든 인가 콜백은 현재 인증된 사용자를 첫 번째 인수로 받고 추가 와일드카드 매개변수를 후속 인수로 받습니다. 이 예에서는 `{orderId}` 자리 표시자를 사용하여 채널 이름의 "ID" 부분이 와일드카드임을 나타냅니다.

<!-- You may view a list of your application's broadcast authorization callbacks using the `channel:list` Artisan command: -->
`channel:list` Artisan 명령을 사용하여 애플리케이션의 브로드캐스트 인가 콜백 목록을 확인할 수 있습니다.

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
<!-- #### Authorization Callback Model Binding -->
#### Authorization Callback Model Binding

<!-- Just like HTTP routes, channel routes may also take advantage of implicit and explicit [route model binding](/docs/12.x/routing#route-model-binding). For example, instead of receiving a string or numeric order ID, you may request an actual `Order` model instance: -->
HTTP 라우트와 마찬가지로 채널 라우트도 암시적 및 명시적 [route model binding](/docs/12.x/routing#route-model-binding)을 활용할 수 있습니다. 예를 들어 문자열이나 숫자로 된 주문 ID를 받는 대신 실제 `Order` 모델 인스턴스를 요청할 수 있습니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과 달리 채널 모델 바인딩은 자동 [implicit model binding scoping](/docs/12.x/routing#implicit-model-binding-scoping)을 지원하지 않습니다. 그러나 대부분의 채널은 단일 모델의 고유한 기본 키를 기반으로 범위가 지정될 수 있으므로 이는 거의 문제가 되지 않습니다.

<a name="authorization-callback-authentication"></a>
<!-- #### Authorization Callback Authentication -->
#### Authorization Callback Authentication

<!-- Private and presence broadcast channels authenticate the current user via your application's default authentication guard. If the user is not authenticated, channel authorization is automatically denied and the authorization callback is never executed. However, you may assign multiple, custom guards that should authenticate the incoming request if necessary: -->
비공개 및 프레즌스 브로드캐스트 채널은 애플리케이션의 기본 인증 가드를 통해 현재 사용자를 인증합니다. 사용자가 인증되지 않으면 채널 인가가 자동으로 거부되고 인가 콜백이 실행되지 않습니다. 그러나 필요한 경우 수신 요청을 인증해야 하는 여러 커스텀 가드를 할당할 수 있습니다.

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
<!-- ### Defining Channel Classes -->
### Defining Channel Classes

<!-- If your application is consuming many different channels, your `routes/channels.php` file could become bulky. So, instead of using closures to authorize channels, you may use channel classes. To generate a channel class, use the `make:channel` Artisan command. This command will place a new channel class in the `App/Broadcasting` directory. -->
애플리케이션이 다양한 채널을 사용하는 경우 `routes/channels.php` 파일이 커질 수 있습니다. 따라서 채널을 인가하기 위해 클로저를 사용하는 대신 채널 클래스를 사용할 수 있습니다. 채널 클래스를 생성하려면 `make:channel` Artisan 명령을 사용하십시오. 이 명령은 `App/Broadcasting` 디렉토리에 새 채널 클래스를 배치합니다.

```shell
php artisan make:channel OrderChannel
```

<!-- Next, register your channel in your `routes/channels.php` file: -->
다음으로 `routes/channels.php` 파일에 채널을 등록하세요.

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

<!-- Finally, you may place the authorization logic for your channel in the channel class' `join` method. This `join` method will house the same logic you would have typically placed in your channel authorization closure. You may also take advantage of channel model binding: -->
마지막으로 채널 클래스의 `join` 메서드에 채널에 대한 인가 로직을 배치할 수 있습니다. 이 `join` 메서드에는 일반적으로 채널 인가 클로저에 배치하는 것과 동일한 로직이 포함됩니다. 채널 모델 바인딩을 활용할 수도 있습니다.

```php
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * Create a new channel instance.
     */
    public function __construct() {}

    /**
     * Authenticate the user's access to the channel.
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]
> Laravel의 다른 많은 클래스와 마찬가지로 채널 클래스는 [service container](/docs/12.x/container)에 의해 자동으로 확인됩니다. 따라서 생성자에서 채널에 필요한 종속성을 유형 힌트로 지정할 수 있습니다.

<a name="broadcasting-events"></a>
<!-- ## Broadcasting Events -->
## Broadcasting Events

<!-- Once you have defined an event and marked it with the `ShouldBroadcast` interface, you only need to fire the event using the event's dispatch method. The event dispatcher will notice that the event is marked with the `ShouldBroadcast` interface and will queue the event for broadcasting: -->
이벤트를 정의하고 `ShouldBroadcast` 인터페이스로 표시한 후에는 이벤트의 디스패치 메서드를 사용하여 이벤트를 실행하기만 하면 됩니다. 이벤트 디스패처는 이벤트가 `ShouldBroadcast` 인터페이스로 표시되어 있음을 확인하고 브로드캐스팅을 위해 이벤트를 큐에 넣습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
<!-- ### Only to Others -->
### Only to Others

<!-- When building an application that utilizes event broadcasting, you may occasionally need to broadcast an event to all subscribers to a given channel except for the current user. You may accomplish this using the `broadcast` helper and the `toOthers` method: -->
이벤트 브로드캐스팅을 활용하는 애플리케이션을 구축할 때 때때로 현재 사용자를 제외한 특정 채널의 모든 구독자에게 이벤트를 브로드캐스트해야 할 수도 있습니다. `broadcast` 도우미와 `toOthers` 메서드를 사용하여 이 작업을 수행할 수 있습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

<!-- To better understand when you may want to use the `toOthers` method, let's imagine a task list application where a user may create a new task by entering a task name. To create a task, your application might make a request to a `/task` URL which broadcasts the task's creation and returns a JSON representation of the new task. When your JavaScript application receives the response from the end-point, it might directly insert the new task into its task list like so: -->
`toOthers` 메서드를 사용하려는 경우를 더 잘 이해하기 위해 사용자가 작업 이름을 입력하여 새 작업을 생성할 수 있는 작업 목록 애플리케이션을 상상해 보겠습니다. 작업을 생성하기 위해 애플리케이션은 작업 생성을 브로드캐스트하고 새 작업의 JSON 표현을 반환하는 `/task` URL에 요청할 수 있습니다. JavaScript 애플리케이션이 엔드포인트로부터 응답을 받으면 다음과 같이 새 작업을 작업 목록에 직접 삽입할 수 있습니다.

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

<!-- However, remember that we also broadcast the task's creation. If your JavaScript application is also listening for this event in order to add tasks to the task list, you will have duplicate tasks in your list: one from the end-point and one from the broadcast. You may solve this by using the `toOthers` method to instruct the broadcaster to not broadcast the event to the current user. -->
그러나 작업 생성도 브로드캐스트된다는 점을 기억하세요. JavaScript 애플리케이션이 작업 목록에 작업을 추가하기 위해 이 이벤트도 수신하는 경우 목록에 중복된 작업이 있게 됩니다. 하나는 엔드포인트에서, 다른 하나는 브로드캐스트에서 발생합니다. `toOthers` 메서드를 사용하여 브로드캐스터에 현재 사용자에게 이벤트를 브로드캐스트하지 않도록 지시하면 이 문제를 해결할 수 있습니다.

> [!WARNING]
> 이벤트는 `toOthers` 메서드를 호출하려면 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 사용해야 합니다.

<a name="only-to-others-configuration"></a>
<!-- #### Configuration -->
#### Configuration

<!-- When you initialize a Laravel Echo instance, a socket ID is assigned to the connection. If you are using a global [Axios](https://github.com/axios/axios) instance to make HTTP requests from your JavaScript application, the socket ID will automatically be attached to every outgoing request as an `X-Socket-ID` header. Then, when you call the `toOthers` method, Laravel will extract the socket ID from the header and instruct the broadcaster to not broadcast to any connections with that socket ID. -->
Laravel Echo 인스턴스를 초기화하면 소켓 ID가 연결에 할당됩니다. 전역 [Axios](https://github.com/axios/axios) 인스턴스를 사용하여 JavaScript 애플리케이션에서 HTTP 요청을 생성하는 경우 소켓 ID는 모든 나가는 요청에 `X-Socket-ID` 헤더로 자동 첨부됩니다. 그런 다음 `toOthers` 메서드를 호출하면 Laravel는 헤더에서 소켓 ID를 추출하고 해당 소켓 ID가 있는 연결에는 브로드캐스트하지 않도록 브로드캐스터에 지시합니다.

<!-- If you are not using a global Axios instance, you will need to manually configure your JavaScript application to send the `X-Socket-ID` header with all outgoing requests. You may retrieve the socket ID using the `Echo.socketId` method: -->
글로벌 Axios 인스턴스를 사용하지 않는 경우 모든 나가는 요청과 함께 `X-Socket-ID` 헤더를 보내도록 JavaScript 애플리케이션을 수동으로 구성해야 합니다. `Echo.socketId` 메서드를 사용하여 소켓 ID를 검색할 수 있습니다:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
<!-- ### Customizing the Connection -->
### Customizing the Connection

<!-- If your application interacts with multiple broadcast connections and you want to broadcast an event using a broadcaster other than your default, you may specify which connection to push an event to using the `via` method: -->
애플리케이션이 여러 브로드캐스트 연결과 상호 작용하고 기본 브로드캐스터가 아닌 다른 브로드캐스터를 사용하여 이벤트를 브로드캐스트하려는 경우 `via` 메서드를 사용하여 이벤트를 푸시할 연결을 지정할 수 있습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

<!-- Alternatively, you may specify the event's broadcast connection by calling the `broadcastVia` method within the event's constructor. However, before doing so, you should ensure that the event class uses the `InteractsWithBroadcasting` trait: -->
또는 이벤트 생성자 내에서 `broadcastVia` 메서드를 호출하여 이벤트의 브로드캐스트 연결을 지정할 수도 있습니다. 그러나 그렇게 하기 전에 이벤트 클래스가 `InteractsWithBroadcasting` 트레이트를 사용하는지 확인해야 합니다.

```php
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
     */
    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```

<a name="anonymous-events"></a>
<!-- ### Anonymous Events -->
### Anonymous Events

<!-- Sometimes, you may want to broadcast a simple event to your application's frontend without creating a dedicated event class. To accommodate this, the `Broadcast` facade allows you to broadcast "anonymous events": -->
때로는 전용 이벤트 클래스를 만들지 않고 간단한 이벤트를 애플리케이션의 프론트엔드에 브로드캐스팅하고 싶을 수도 있습니다. 이를 수용하기 위해 `Broadcast` 파사드를 사용하면 "익명 이벤트"를 브로드캐스트할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->send();
```

<!-- The example above will broadcast the following event: -->
위의 예에서는 다음 이벤트를 브로드캐스트합니다.

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

<!-- Using the `as` and `with` methods, you may customize the event's name and data: -->
`as` 및 `with` 메서드를 사용하면 이벤트의 이름과 데이터를 사용자 지정할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

<!-- The example above will broadcast an event like the following: -->
위의 예는 다음과 같이 이벤트를 브로드캐스트합니다.

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

<!-- If you would like to broadcast the anonymous event on a private or presence channel, you may utilize the `private` and `presence` methods: -->
비공개 또는 프레즌스 채널에서 익명 이벤트를 브로드캐스트하려면 `private` 및 `presence` 메서드를 활용할 수 있습니다.

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

<!-- Broadcasting an anonymous event using the `send` method dispatches the event to your application's [queue](/docs/12.x/queues) for processing. However, if you would like to broadcast the event immediately, you may use the `sendNow` method: -->
`send` 메서드를 사용하면 익명 이벤트가 애플리케이션의 [queue](/docs/12.x/queues)에 디스패치되어 처리됩니다. 이벤트를 즉시 브로드캐스트하려면 `sendNow` 메서드를 사용할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

<!-- To broadcast the event to all channel subscribers except the currently authenticated user, you can invoke the `toOthers` method: -->
현재 인증된 사용자를 제외한 모든 채널 구독자에게 이벤트를 브로드캐스트하려면 `toOthers` 메서드를 호출하면 됩니다.

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
<!-- ### Rescuing Broadcasts -->
### Rescuing Broadcasts

<!-- When your application's queue server is unavailable or Laravel encounters an error while broadcasting an event, an exception is thrown that typically causes the end user to see an application error. Since event broadcasting is often supplementary to your application's core functionality, you can prevent these exceptions from disrupting the user experience by implementing the `ShouldRescue` interface on your events. -->
애플리케이션의 큐 서버를 사용할 수 없거나 이벤트를 브로드캐스트하는 동안 Laravel에 오류가 발생하면 일반적으로 최종 사용자에게 애플리케이션 오류가 표시되는 예외가 발생합니다. 이벤트 브로드캐스팅은 애플리케이션의 핵심 기능을 보완하는 경우가 많으므로 이벤트에 `ShouldRescue` 인터페이스를 구현하여 이러한 예외로 인해 사용자 경험이 중단되는 것을 방지할 수 있습니다.

<!-- Events that implement the `ShouldRescue` interface automatically utilize Laravel's [rescue helper function](/docs/12.x/helpers#method-rescue) during broadcast attempts. This helper catches any exceptions, reports them to your application's exception handler for logging, and allows the application to continue executing normally without interrupting the user's workflow: -->
`ShouldRescue` 인터페이스를 구현하는 이벤트는 브로드캐스트 시도 중에 Laravel의 [rescue helper function](/docs/12.x/helpers#method-rescue)을 자동으로 활용합니다. 이 도우미는 모든 예외를 포착하고 이를 애플리케이션의 예외 처리기에 기록하여 보고하며 사용자의 작업 흐름을 방해하지 않고 애플리케이션이 정상적으로 계속 실행될 수 있도록 합니다.

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Broadcasting\ShouldRescue;

class ServerCreated implements ShouldBroadcast, ShouldRescue
{
    // ...
}
```

<a name="receiving-broadcasts"></a>
<!-- ## Receiving Broadcasts -->
## Receiving Broadcasts

<a name="listening-for-events"></a>
<!-- ### Listening for Events -->
### Listening for Events

<!-- Once you have [installed and instantiated Laravel Echo](#client-side-installation), you are ready to start listening for events that are broadcast from your Laravel application. First, use the `channel` method to retrieve an instance of a channel, then call the `listen` method to listen for a specified event: -->
[installed and instantiated Laravel Echo](#client-side-installation)하고 나면 Laravel 애플리케이션에서 브로드캐스트되는 이벤트를 수신할 준비가 된 것입니다. 먼저 `channel` 메서드를 사용하여 채널의 인스턴스를 검색한 다음 `listen` 메서드를 호출하여 지정된 이벤트를 수신합니다.

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

<!-- If you would like to listen for events on a private channel, use the `private` method instead. You may continue to chain calls to the `listen` method to listen for multiple events on a single channel: -->
비공개 채널에서 이벤트를 수신하려면 대신 `private` 메서드를 사용하세요. 단일 채널에서 여러 이벤트를 수신하기 위해 계속해서 `listen` 메서드에 대한 호출을 연결할 수 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
<!-- #### Stop Listening for Events -->
#### Stop Listening for Events

<!-- If you would like to stop listening to a given event without [leaving the channel](#leaving-a-channel), you may use the `stopListening` method: -->
[leaving the channel](#leaving-a-channel) 않고 특정 이벤트 수신을 중지하려면 `stopListening` 메서드를 사용할 수 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
<!-- ### Leaving a Channel -->
### Leaving a Channel

<!-- To leave a channel, you may call the `leaveChannel` method on your Echo instance: -->
채널을 나가려면 Echo 인스턴스에서 `leaveChannel` 메서드를 호출하면 됩니다.

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

<!-- If you would like to leave a channel and also its associated private and presence channels, you may call the `leave` method: -->
채널과 관련 비공개 및 프레즌스 채널을 종료하려면 `leave` 메서드를 호출하면 됩니다.

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
<!-- ### Namespaces -->
### Namespaces

<!-- You may have noticed in the examples above that we did not specify the full `App\Events` namespace for the event classes. This is because Echo will automatically assume the events are located in the `App\Events` namespace. However, you may configure the root namespace when you instantiate Echo by passing a `namespace` configuration option: -->
위의 예에서 이벤트 클래스에 대해 전체 `App\Events` 네임스페이스를 지정하지 않았음을 알 수 있습니다. 이는 Echo가 자동으로 이벤트가 `App\Events` 네임스페이스에 있다고 가정하기 때문입니다. 그러나 `namespace` 구성 옵션을 전달하여 Echo를 인스턴스화할 때 루트 네임스페이스를 구성할 수 있습니다.

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

<!-- Alternatively, you may prefix event classes with a `.` when subscribing to them using Echo. This will allow you to always specify the fully-qualified class name: -->
또는 Echo를 사용하여 구독할 때 이벤트 클래스 앞에 `.`를 붙일 수도 있습니다. 이렇게 하면 항상 정규화된 클래스 이름을 지정할 수 있습니다.

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
<!-- ### Using React or Vue -->
### Using React or Vue

<!-- Laravel Echo includes React and Vue hooks that make it painless to listen for events. To get started, invoke the `useEcho` hook, which is used to listen for private events. The `useEcho` hook will automatically leave channels when the consuming component is unmounted: -->
Laravel Echo에는 이벤트를 쉽게 수신할 수 있게 해주는 React 및 Vue 후크가 포함되어 있습니다. 시작하려면 비공개 이벤트를 수신하는 데 사용되는 `useEcho` 후크를 호출하십시오. `useEcho` 후크는 소비 컴포넌트가 마운트 해제되면 자동으로 채널을 종료합니다.

```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

<!-- You may listen to multiple events by providing an array of events to `useEcho`: -->
`useEcho`에 이벤트 배열을 제공하여 여러 이벤트를 수신할 수 있습니다.

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

<!-- You may also specify the shape of the broadcast event payload data, providing greater type safety and editing convenience: -->
또한 브로드캐스트 이벤트 페이로드 데이터의 모양을 지정하여 유형 안전성과 편집 편의성을 높일 수도 있습니다.

```ts
type OrderData = {
    order: {
        id: number;
        user: {
            id: number;
            name: string;
        };
        created_at: string;
    };
};

useEcho<OrderData>(`orders.${orderId}`, "OrderShipmentStatusUpdated", (e) => {
    console.log(e.order.id);
    console.log(e.order.user.id);
});
```

<!-- The `useEcho` hook will automatically leave channels when the consuming component is unmounted; however, you may utilize the returned functions to manually stop / start listening to channels programmatically when necessary: -->
`useEcho` 후크는 소비 컴포넌트가 마운트 해제되면 자동으로 채널을 종료합니다. 그러나 필요한 경우 반환된 함수를 활용하여 프로그래밍 방식으로 채널 수신을 수동으로 중지/시작할 수 있습니다.

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>
<!-- #### Connecting to Public Channels -->
#### Connecting to Public Channels

<!-- To connect to a public channel, you may use the `useEchoPublic` hook: -->
공개 채널에 연결하려면 `useEchoPublic` 후크를 사용할 수 있습니다.

```js tab=React
import { useEchoPublic } from "@laravel/echo-react";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPublic } from "@laravel/echo-vue";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connecting-to-presence-channels"></a>
<!-- #### Connecting to Presence Channels -->
#### Connecting to Presence Channels

<!-- To connect to a presence channel, you may use the `useEchoPresence` hook: -->
프레즌스 채널에 연결하려면 `useEchoPresence` 후크를 사용할 수 있습니다.

```js tab=React
import { useEchoPresence } from "@laravel/echo-react";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPresence } from "@laravel/echo-vue";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connection-status"></a>
<!-- #### Connection Status -->
#### Connection Status

<!-- You may retrieve the current WebSocket connection status using the `useConnectionStatus` hook, which provides reactive status that automatically updates when the connection state changes: -->
연결 상태가 변경되면 자동으로 업데이트되는 반응 상태를 제공하는 `useConnectionStatus` 후크를 사용하여 현재 WebSocket 연결 상태를 검색할 수 있습니다.

```js tab=React
import { useConnectionStatus } from "@laravel/echo-react";

function ConnectionIndicator() {
    const status = useConnectionStatus();

    return <div>Connection: {status}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useConnectionStatus } from "@laravel/echo-vue";

const status = useConnectionStatus();
</script>

<template>
    <div>Connection: {{ status }}</div>
</template>
```

<!-- The possible status values are: -->
가능한 상태 값은 다음과 같습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `connected` - Successfully connected to the WebSocket server.
- `connecting` - Initial connection attempt in progress.
- `reconnecting` - Attempting to reconnect after a disconnection.
- `disconnected` - Not connected and not attempting to reconnect.
- `failed` - Connection failed and won't retry.
-->
- `connected` - WebSocket 서버에 성공적으로 연결되었습니다.
- `connecting` - 초기 연결 시도가 진행 중입니다.
- `reconnecting` - 연결이 끊어진 후 다시 연결을 시도합니다.
- `disconnected` - 연결되지 않았으며 다시 연결을 시도하지 않습니다.
- `failed` - 연결이 실패했으며 다시 시도하지 않습니다.

<!-- </div> -->
</div>

<a name="presence-channels"></a>
<!-- ## Presence Channels -->
## Presence Channels

<!-- Presence channels build on the security of private channels while exposing the additional feature of awareness of who is subscribed to the channel. This makes it easy to build powerful, collaborative application features such as notifying users when another user is viewing the same page or listing the inhabitants of a chat room. -->
프레즌스 채널은 비공개 채널의 보안을 기반으로 구축되는 동시에 채널 구독자를 인식하는 추가 기능을 제공합니다. 이를 통해 다른 사용자가 동일한 페이지를 볼 때 사용자에게 알리거나 채팅방 거주자 목록을 나열하는 등 강력한 협업 애플리케이션 기능을 쉽게 구축할 수 있습니다.

<a name="authorizing-presence-channels"></a>
<!-- ### Authorizing Presence Channels -->
### Authorizing Presence Channels

<!-- All presence channels are also private channels; therefore, users must be [authorized to access them](#authorizing-channels). However, when defining authorization callbacks for presence channels, you will not return `true` if the user is authorized to join the channel. Instead, you should return an array of data about the user. -->
모든 프레즌스 채널은 비공개 채널이기도 합니다. 따라서 사용자는 [authorized to access them](#authorizing-channels)을 받아야 합니다. 그러나 프레즌스 채널에 대한 인가 콜백을 정의할 때 사용자가 채널에 참여할 수 있는 권한이 있으면 `true`를 반환하지 않습니다. 대신 사용자에 대한 데이터 배열을 반환해야 합니다.

<!-- The data returned by the authorization callback will be made available to the presence channel event listeners in your JavaScript application. If the user is not authorized to join the presence channel, you should return `false` or `null`: -->
인가 콜백에서 반환된 데이터는 JavaScript 애플리케이션의 프레즌스 채널 이벤트 리스너에서 사용할 수 있습니다. 사용자가 프레즌스 채널에 참여할 권한이 없는 경우 `false` 또는 `null`를 반환해야 합니다.

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
<!-- ### Joining Presence Channels -->
### Joining Presence Channels

<!-- To join a presence channel, you may use Echo's `join` method. The `join` method will return a `PresenceChannel` implementation which, along with exposing the `listen` method, allows you to subscribe to the `here`, `joining`, and `leaving` events. -->
프레즌스 채널에 참여하려면 Echo의 `join` 메서드를 사용할 수 있습니다. `join` 메서드는 `listen` 메서드와 함께 `here`, `joining` 및 `leaving` 이벤트를 구독할 수 있게 해주는 `PresenceChannel` 구현을 반환합니다.

```js
Echo.join(`chat.${roomId}`)
    .here((users) => {
        // ...
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

<!-- The `here` callback will be executed immediately once the channel is joined successfully, and will receive an array containing the user information for all of the other users currently subscribed to the channel. The `joining` method will be executed when a new user joins a channel, while the `leaving` method will be executed when a user leaves the channel. The `error` method will be executed when the authentication endpoint returns an HTTP status code other than 200 or if there is a problem parsing the returned JSON. -->
`here` 콜백은 채널에 성공적으로 참여하면 즉시 실행되며, 현재 채널에 참여하고 있는 다른 모든 사용자의 정보가 포함된 배열을 수신합니다. `joining` 메서드는 새로운 사용자가 채널에 참여할 때 실행되고, `leaving` 메서드는 사용자가 채널을 떠날 때 실행됩니다. 인증 엔드포인트가 200이 아닌 HTTP 상태 코드를 반환하거나 반환된 JSON을 파싱하는 데 문제가 있는 경우 `error` 메서드가 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>
<!-- ### Broadcasting to Presence Channels -->
### Broadcasting to Presence Channels

<!-- Presence channels may receive events just like public or private channels. Using the example of a chatroom, we may want to broadcast `NewMessage` events to the room's presence channel. To do so, we'll return an instance of `PresenceChannel` from the event's `broadcastOn` method: -->
프레즌스 채널은 공개 또는 비공개 채널과 마찬가지로 이벤트를 수신할 수 있습니다. 채팅방의 예를 사용하여 `NewMessage` 이벤트를 방의 프레즌스 채널에 브로드캐스트할 수 있습니다. 이를 위해 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환합니다.

```php
/**
 * Get the channels the event should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PresenceChannel('chat.'.$this->message->room_id),
    ];
}
```

<!-- As with other events, you may use the `broadcast` helper and the `toOthers` method to exclude the current user from receiving the broadcast: -->
다른 이벤트와 마찬가지로 `broadcast` 도우미와 `toOthers` 메서드를 사용하여 현재 사용자를 브로드캐스트 수신에서 제외할 수 있습니다.

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

<!-- As typical of other types of events, you may listen for events sent to presence channels using Echo's `listen` method: -->
다른 유형의 이벤트와 마찬가지로 Echo의 `listen` 메서드를 사용하여 프레즌스 채널로 전송된 이벤트를 수신할 수 있습니다.

```js
Echo.join(`chat.${roomId}`)
    .here(/* ... */)
    .joining(/* ... */)
    .leaving(/* ... */)
    .listen('NewMessage', (e) => {
        // ...
    });
```

<a name="model-broadcasting"></a>
<!-- ## Model Broadcasting -->
## Model Broadcasting

> [!WARNING]
> 모델 브로드캐스팅에 대한 다음 문서를 읽기 전에 Laravel의 모델 브로드캐스팅 서비스의 일반적인 개념과 브로드캐스트 이벤트를 수동으로 생성하고 수신하는 방법을 숙지하는 것이 좋습니다.

<!-- It is common to broadcast events when your application's [Eloquent models](/docs/12.x/eloquent) are created, updated, or deleted. Of course, this can easily be accomplished by manually [defining custom events for Eloquent model state changes](/docs/12.x/eloquent#events) and marking those events with the `ShouldBroadcast` interface. -->
애플리케이션의 [Eloquent models](/docs/12.x/eloquent)가 생성, 업데이트 또는 삭제될 때 이벤트를 브로드캐스트하는 것이 일반적입니다. 물론 이는 수동으로 [defining custom events for Eloquent model state changes](/docs/12.x/eloquent#events)하고 해당 이벤트를 `ShouldBroadcast` 인터페이스로 표시하여 쉽게 수행할 수 있습니다.

<!-- However, if you are not using these events for any other purposes in your application, it can be cumbersome to create event classes for the sole purpose of broadcasting them. To remedy this, Laravel allows you to indicate that an Eloquent model should automatically broadcast its state changes. -->
그러나 애플리케이션에서 다른 목적으로 이러한 이벤트를 사용하지 않는 경우 이를 브로드캐스팅할 목적으로만 이벤트 클래스를 생성하는 것이 번거로울 수 있습니다. 이 문제를 해결하기 위해 Laravel을 사용하면 Eloquent 모델이 상태 변경 사항을 자동으로 브로드캐스트해야 함을 나타낼 수 있습니다.

<!-- To get started, your Eloquent model should use the `Illuminate\Database\Eloquent\BroadcastsEvents` trait. In addition, the model should define a `broadcastOn` method, which will return an array of channels that the model's events should broadcast on: -->
시작하려면 Eloquent 모델이 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 사용해야 합니다. 또한 모델은 모델의 이벤트가 브로드캐스트해야 하는 채널 배열을 반환하는 `broadcastOn` 메서드를 정의해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Database\Eloquent\BroadcastsEvents;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Post extends Model
{
    use BroadcastsEvents, HasFactory;

    /**
     * Get the user that the post belongs to.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Get the channels that model events should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

<!-- Once your model includes this trait and defines its broadcast channels, it will begin automatically broadcasting events when a model instance is created, updated, deleted, trashed, or restored. -->
모델에 이 트레이트가 포함되고 브로드캐스트 채널을 정의하면 모델 인스턴스가 생성, 업데이트, 삭제, 소프트 삭제 또는 복원될 때 자동으로 이벤트 브로드캐스팅이 시작됩니다.

<!-- In addition, you may have noticed that the `broadcastOn` method receives a string `$event` argument. This argument contains the type of event that has occurred on the model and will have a value of `created`, `updated`, `deleted`, `trashed`, or `restored`. By inspecting the value of this variable, you may determine which channels (if any) the model should broadcast to for a particular event: -->
또한 `broadcastOn` 메서드가 문자열 `$event` 인수를 받는 것을 알 수 있습니다. 이 인수에는 모델에서 발생한 이벤트 유형이 포함되며 값은 `created`, `updated`, `deleted`, `trashed` 또는 `restored`입니다. 이 변수의 값을 검사하여 모델이 특정 이벤트에 대해 브로드캐스트해야 하는 채널(있는 경우)을 결정할 수 있습니다.

```php
/**
 * Get the channels that model events should broadcast on.
 *
 * @return array<string, array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>>
 */
public function broadcastOn(string $event): array
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
경우에 따라 Laravel이 기본 모델 브로드캐스트 이벤트를 생성하는 방식을 사용자 지정하고 싶을 수도 있습니다. Eloquent 모델에 `newBroadcastableEvent` 메서드를 정의하여 이를 수행할 수 있습니다. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다.

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * Create a new broadcastable model event for the model.
 */
protected function newBroadcastableEvent(string $event): BroadcastableModelEventOccurred
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
아시다시피 위의 모델 예제에서 `broadcastOn` 메서드는 `Channel` 인스턴스를 반환하지 않았습니다. 대신 Eloquent 모델이 직접 반환되었습니다. Eloquent 모델 인스턴스가 모델의 `broadcastOn` 메서드에 의해 반환되거나 메서드에 의해 반환된 배열에 포함된 경우, Laravel는 모델의 클래스 이름과 기본 키 식별자를 채널 이름으로 사용하여 모델에 대한 비공개 채널 인스턴스를 자동으로 인스턴스화합니다.

<!-- So, an `App\Models\User` model with an `id` of `1` would be converted into an `Illuminate\Broadcasting\PrivateChannel` instance with a name of `App.Models.User.1`. Of course, in addition to returning Eloquent model instances from your model's `broadcastOn` method, you may return complete `Channel` instances in order to have full control over the model's channel names: -->
따라서 `1`의 `id`가 포함된 `App\Models\User` 모델은 이름이 `App.Models.User.1`인 `Illuminate\Broadcasting\PrivateChannel` 인스턴스로 변환됩니다. 물론 모델의 `broadcastOn` 메서드에서 Eloquent 모델 인스턴스를 반환하는 것 외에도 모델의 채널 이름을 완전히 제어하기 위해 완전한 `Channel` 인스턴스를 반환할 수도 있습니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels that model events should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(string $event): array
{
    return [
        new PrivateChannel('user.'.$this->id)
    ];
}
```

<!-- If you plan to explicitly return a channel instance from your model's `broadcastOn` method, you may pass an Eloquent model instance to the channel's constructor. When doing so, Laravel will use the model channel conventions discussed above to convert the Eloquent model into a channel name string: -->
모델의 `broadcastOn` 메서드에서 채널 인스턴스를 명시적으로 반환하려는 경우 Eloquent 모델 인스턴스를 채널 생성자에 전달할 수 있습니다. 이렇게 하면 Laravel는 위에서 설명한 모델 채널 규칙을 사용하여 Eloquent 모델을 채널 이름 문자열로 변환합니다.

```php
return [new Channel($this->user)];
```

<!-- If you need to determine the channel name of a model, you may call the `broadcastChannel` method on any model instance. For example, this method returns the string `App.Models.User.1` for an `App\Models\User` model with an `id` of `1`: -->
모델의 채널 이름을 확인해야 하는 경우 모델 인스턴스에서 `broadcastChannel` 메서드를 호출할 수 있습니다. 예를 들어, 이 메서드는 `1`의 `id`를 사용하여 `App\Models\User` 모델에 대해 `App.Models.User.1` 문자열을 반환합니다.

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
<!-- #### Event Conventions -->
#### Event Conventions

<!-- Since model broadcast events are not associated with an "actual" event within your application's `App\Events` directory, they are assigned a name and a payload based on conventions. Laravel's convention is to broadcast the event using the class name of the model (not including the namespace) and the name of the model event that triggered the broadcast. -->
모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉터리 내의 "실제" 이벤트와 연결되지 않으므로 규칙에 따라 이름과 페이로드가 할당됩니다. Laravel의 규칙은 모델의 클래스 이름(네임스페이스 제외)과 브로드캐스트를 트리거한 모델 이벤트의 이름을 사용하여 이벤트를 브로드캐스트하는 것입니다.

<!-- So, for example, an update to the `App\Models\Post` model would broadcast an event to your client-side application as `PostUpdated` with the following payload: -->
예를 들어 `App\Models\Post` 모델에 대한 업데이트는 다음 페이로드를 사용하여 이벤트를 클라이언트 측 애플리케이션에 `PostUpdated`로 브로드캐스트합니다.

```json
{
    "model": {
        "id": 1,
        "title": "My first post"
        ...
    },
    ...
    "socket": "someSocketId"
}
```

<!-- The deletion of the `App\Models\User` model would broadcast an event named `UserDeleted`. -->
`App\Models\User` 모델을 삭제하면 `UserDeleted`라는 이벤트가 브로드캐스트됩니다.

<!-- If you would like, you may define a custom broadcast name and payload by adding a `broadcastAs` and `broadcastWith` method to your model. These methods receive the name of the model event / operation that is occurring, allowing you to customize the event's name and payload for each model operation. If `null` is returned from the `broadcastAs` method, Laravel will use the model broadcasting event name conventions discussed above when broadcasting the event: -->
원하는 경우 모델에 `broadcastAs` 및 `broadcastWith` 메서드를 추가하여 커스텀 브로드캐스트 이름과 페이로드를 정의할 수 있습니다. 이러한 메서드는 발생 중인 모델 이벤트 / 작업의 이름을 수신하여 각 모델 작업에 대해 이벤트의 이름과 페이로드를 사용자 지정할 수 있습니다. `null`가 `broadcastAs` 메서드에서 반환되면 Laravel는 이벤트를 브로드캐스트할 때 위에서 설명한 모델 브로드캐스팅 이벤트 이름 규칙을 사용합니다.

```php
/**
 * The model event's broadcast name.
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * Get the data to broadcast for the model.
 *
 * @return array<string, mixed>
 */
public function broadcastWith(string $event): array
{
    return match ($event) {
        'created' => ['title' => $this->title],
        default => ['model' => $this],
    };
}
```

<a name="listening-for-model-broadcasts"></a>
<!-- ### Listening for Model Broadcasts -->
### Listening for Model Broadcasts

<!-- Once you have added the `BroadcastsEvents` trait to your model and defined your model's `broadcastOn` method, you are ready to start listening for broadcasted model events within your client-side application. Before getting started, you may wish to consult the complete documentation on [listening for events](#listening-for-events). -->
모델에 `BroadcastsEvents` 트레이트를 추가하고 모델의 `broadcastOn` 메서드를 정의하면 클라이언트 측 애플리케이션 내에서 브로드캐스트된 모델 이벤트를 수신할 준비가 된 것입니다. 시작하기 전에 [listening for events](#listening-for-events)에 대한 전체 문서를 참조하는 것이 좋습니다.

<!-- First, use the `private` method to retrieve an instance of a channel, then call the `listen` method to listen for a specified event. Typically, the channel name given to the `private` method should correspond to Laravel's [model broadcasting conventions](#model-broadcasting-conventions). -->
먼저 `private` 메서드를 사용하여 채널의 인스턴스를 검색한 다음 `listen` 메서드를 호출하여 지정된 이벤트를 수신합니다. 일반적으로 `private` 메서드에 지정된 채널 이름은 Laravel의 [model broadcasting conventions](#model-broadcasting-conventions)과 일치해야 합니다.

<!-- Once you have obtained a channel instance, you may use the `listen` method to listen for a particular event. Since model broadcast events are not associated with an "actual" event within your application's `App\Events` directory, the [event name](#model-broadcasting-event-conventions) must be prefixed with a `.` to indicate it does not belong to a particular namespace. Each model broadcast event has a `model` property which contains all of the broadcastable properties of the model: -->
채널 인스턴스를 얻은 후에는 `listen` 메서드를 사용하여 특정 이벤트를 수신할 수 있습니다. 모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉터리 내의 "실제" 이벤트와 연결되어 있지 않으므로 [event name](#model-broadcasting-event-conventions) 앞에 `.`가 붙어 특정 네임스페이스에 속하지 않음을 나타내야 합니다. 각 모델 브로드캐스트 이벤트에는 모델의 브로드캐스트 가능한 모든 속성을 포함하는 `model` 속성이 있습니다.

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
<!-- #### Using React or Vue -->
#### Using React or Vue

<!-- If you are using React or Vue, you may use Laravel Echo's included `useEchoModel` hook to easily listen for model broadcasts: -->
React 또는 Vue를 사용하는 경우 Laravel Echo에 포함된 `useEchoModel` 후크를 사용하여 모델 브로드캐스트를 쉽게 수신할 수 있습니다.

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```

<!-- You may also specify the shape of the model event payload data, providing greater type safety and editing convenience: -->
또한 모델 이벤트 페이로드 데이터의 모양을 지정하여 유형 안전성과 편집 편의성을 높일 수도 있습니다.

```ts
type User = {
    id: number;
    name: string;
    email: string;
};

useEchoModel<User, "App.Models.User">("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model.id);
    console.log(e.model.name);
});
```

<a name="client-events"></a>
<!-- ## Client Events -->
## Client Events

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels)을 사용할 때 클라이언트 이벤트를 보내려면 [application dashboard](https://dashboard.pusher.com/)의 "앱 설정" 섹션에서 "클라이언트 이벤트" 옵션을 활성화해야 합니다.

<!-- Sometimes you may wish to broadcast an event to other connected clients without hitting your Laravel application at all. This can be particularly useful for things like "typing" notifications, where you want to alert users of your application that another user is typing a message on a given screen. -->
때로는 Laravel 애플리케이션을 전혀 실행하지 않고 연결된 다른 클라이언트에 이벤트를 브로드캐스트하고 싶을 수도 있습니다. 이는 다른 사용자가 특정 화면에 메시지를 입력하고 있음을 애플리케이션 사용자에게 알리려는 "입력" 알림과 같은 작업에 특히 유용할 수 있습니다.

<!-- To broadcast client events, you may use Echo's `whisper` method: -->
클라이언트 이벤트를 브로드캐스트하려면 Echo의 `whisper` 메서드를 사용할 수 있습니다.

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

<!-- To listen for client events, you may use the `listenForWhisper` method: -->
클라이언트 이벤트를 수신하려면 `listenForWhisper` 메서드를 사용할 수 있습니다.

```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
</script>
```

<a name="notifications"></a>
<!-- ## Notifications -->
## Notifications

<!-- By pairing event broadcasting with [notifications](/docs/12.x/notifications), your JavaScript application may receive new notifications as they occur without needing to refresh the page. Before getting started, be sure to read over the documentation on using [the broadcast notification channel](/docs/12.x/notifications#broadcast-notifications). -->
이벤트 브로드캐스팅을 [notifications](/docs/12.x/notifications)과 페어링하면 JavaScript 애플리케이션이 페이지를 새로 고치지 않고도 새 알림을 받을 수 있습니다. 시작하기 전에 [the broadcast notification channel](/docs/12.x/notifications#broadcast-notifications) 사용에 대한 설명서를 읽어보세요.

<!-- Once you have configured a notification to use the broadcast channel, you may listen for the broadcast events using Echo's `notification` method. Remember, the channel name should match the class name of the entity receiving the notifications: -->
브로드캐스트 채널을 사용하도록 알림을 구성한 후에는 Echo의 `notification` 메서드를 사용하여 브로드캐스트 이벤트를 수신할 수 있습니다. 채널 이름은 알림을 받는 엔터티의 클래스 이름과 일치해야 합니다.

```js tab=JavaScript
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

<!-- In this example, all notifications sent to `App\Models\User` instances via the `broadcast` channel would be received by the callback. A channel authorization callback for the `App.Models.User.{id}` channel is included in your application's `routes/channels.php` file. -->
이 예에서는 `broadcast` 채널을 통해 `App\Models\User` 인스턴스로 전송된 모든 알림이 콜백에 의해 수신됩니다. `App.Models.User.{id}` 채널에 대한 채널 인가 콜백은 애플리케이션의 `routes/channels.php` 파일에 포함되어 있습니다.

<a name="stop-listening-for-notifications"></a>
<!-- #### Stop Listening for Notifications -->
#### Stop Listening for Notifications

<!-- If you would like to stop listening to notifications without [leaving the channel](#leaving-a-channel), you may use the `stopListeningForNotification` method: -->
[leaving the channel](#leaving-a-channel) 않고 알림 수신을 중지하려면 `stopListeningForNotification` 메서드를 사용할 수 있습니다.

```js
const callback = (notification) => {
    console.log(notification.type);
}

// Start listening...
Echo.private(`App.Models.User.${userId}`)
    .notification(callback);

// Stop listening (callback must be the same)...
Echo.private(`App.Models.User.${userId}`)
    .stopListeningForNotification(callback);
```
