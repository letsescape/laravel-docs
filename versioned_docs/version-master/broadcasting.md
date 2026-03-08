# 브로드캐스팅 (Broadcasting)

- [소개](#introduction)
- [빠른 시작](#quickstart)
- [서버 사이드 설치](#server-side-installation)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [클라이언트 사이드 설치](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [개념 개요](#concept-overview)
    - [예제 애플리케이션 사용하기](#using-example-application)
- [브로드캐스트 이벤트 정의하기](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스팅과 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 인가 처리](#authorizing-channels)
    - [인가 콜백 정의하기](#defining-authorization-callbacks)
    - [채널 클래스 정의하기](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [다른 사용자에게만 브로드캐스팅](#only-to-others)
    - [커넥션 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
    - [브로드캐스트 예외 구제하기](#rescuing-broadcasts)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널 떠나기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
    - [React 또는 Vue 사용하기](#using-react-or-vue)
- [프레젠스 채널](#presence-channels)
    - [프레젠스 채널 인가하기](#authorizing-presence-channels)
    - [프레젠스 채널 참여하기](#joining-presence-channels)
    - [프레젠스 채널로 브로드캐스팅](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림(Notifications)](#notifications)

<a name="introduction"></a>
## 소개 (Introduction)

현대적인 웹 애플리케이션에서는 WebSocket을 사용해 실시간으로 갱신되는 사용자 인터페이스를 구현하는 일이 많습니다. 서버에서 데이터가 변경되면, 클라이언트는 WebSocket 연결을 통해 메시지를 즉시 전달받아 처리할 수 있습니다. WebSocket은 UI의 데이터 변경 사항을 반영하기 위해 서버에 지속적으로 폴링하는 것보다 훨씬 효율적입니다.

예를 들어, 애플리케이션에서 사용자의 데이터를 CSV 파일로 내보내어 이메일로 전달하는 기능이 있다고 가정해봅니다. 하지만, 이 CSV 파일을 생성하는 데 수 분이 걸리기 때문에 이 작업을 [큐에 등록된 작업](/docs/master/queues)에서 처리합니다. CSV 파일이 생성되어 사용자에게 메일로 전송되면, 우리는 `App\Events\UserDataExported` 이벤트를 브로드캐스팅해서 애플리케이션의 JavaScript에서 이를 받을 수 있습니다. 이벤트가 수신되면 사용자는 페이지를 새로 고치지 않고도 CSV 파일이 전송되었다는 메시지를 볼 수 있습니다.

이런 기능을 쉽게 구현할 수 있도록 Laravel은 서버 사이드의 [이벤트](/docs/master/events)를 WebSocket 연결을 통해 "브로드캐스트"하는 기능을 제공합니다. 이벤트 브로드캐스트를 사용하면 서버와 프론트엔드(JavaScript) 애플리케이션 양쪽에서 같은 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다: 클라이언트는 프론트엔드에서 이름이 지정된 채널에 연결하고, Laravel 애플리케이션에서는 백엔드에서 이 채널로 이벤트를 브로드캐스트합니다. 브로드캐스트되는 이벤트에는 프론트엔드에 제공하고 싶은 어떠한 데이터도 포함시킬 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

Laravel은 기본적으로 세 가지 서버 사이드 브로드캐스팅 드라이버를 제공합니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com).

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전에 [이벤트와 리스너](/docs/master/events)에 대한 Laravel 문서를 먼저 읽으시길 바랍니다.

<a name="quickstart"></a>
## 빠른 시작 (Quickstart)

기본적으로, 새로운 Laravel 애플리케이션에서는 브로드캐스팅이 활성화되어 있지 않습니다. `install:broadcasting` Artisan 명령어를 사용해 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령어는 사용할 이벤트 브로드캐스팅 서비스를 선택하도록 안내합니다. 이와 더불어, `config/broadcasting.php` 설정 파일과 애플리케이션의 브로드캐스트 인가(authorization) 라우트 및 콜백을 등록할 수 있는 `routes/channels.php` 파일도 생성합니다.

Laravel은 여러 브로드캐스트 드라이버를 기본 지원합니다: [Laravel Reverb](/docs/master/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅을 위한 `log` 드라이버가 있습니다. 또한, 테스트 중 브로드캐스팅을 사용하지 않을 수 있도록 `null` 드라이버도 포함되어 있습니다. 각각의 드라이버에 대한 설정 예제는 `config/broadcasting.php` 파일에 포함되어 있습니다.

애플리케이션의 모든 브로드캐스트 설정은 `config/broadcasting.php` 파일에 저장됩니다. 만약 이 파일이 없다면, `install:broadcasting` Artisan 명령어 실행 시 자동으로 생성됩니다.

<a name="quickstart-next-steps"></a>
#### 다음 단계

이벤트 브로드캐스팅을 활성화했다면, [브로드캐스트 이벤트 정의](#defining-broadcast-events) 및 [이벤트 리스닝](#listening-for-events) 방법을 배워보세요. 만약 Laravel의 React 또는 Vue [스타터 키트](/docs/master/starter-kits)를 사용 중이라면, Echo의 [useEcho hook](#using-react-or-vue)을 통해 이벤트를 리스닝할 수 있습니다.

> [!NOTE]
> 이벤트를 브로드캐스팅하기 전에, [큐 워커](/docs/master/queues)를 먼저 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐에 등록된 작업을 통해 처리되므로, 브로드캐스팅이 애플리케이션의 응답 시간에 심각한 영향을 주지 않습니다.

<a name="server-side-installation"></a>
## 서버 사이드 설치 (Server Side Installation)

Laravel의 이벤트 브로드캐스팅을 사용하려면, 애플리케이션 내부에서 약간의 설정을 하고, 몇 가지 패키지를 설치해야 합니다.

이벤트 브로드캐스팅은 서버 사이드 브로드캐스트 드라이버가 Laravel 이벤트를 브라우저 클라이언트의 Laravel Echo(JavaScript 라이브러리)로 전달하는 방식으로 이뤄집니다. 걱정하지 마세요. 설치 과정은 단계별로 안내해 드립니다.

<a name="reverb"></a>
### Reverb

Reverb를 이벤트 브로드캐스터로 사용할 때, Laravel의 브로드캐스트 기능을 빠르게 활성화하려면 `install:broadcasting` Artisan 명령어에 `--reverb` 옵션을 추가하여 실행하세요. 이 명령어는 Reverb에 필요한 Composer 및 NPM 패키지를 설치하고, 적절한 환경 변수로 `.env` 파일을 업데이트합니다:

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 명령어를 실행하면 [Laravel Reverb](/docs/master/reverb) 설치를 안내합니다. 물론 Composer 패키지 매니저를 사용하여 직접 Reverb를 설치할 수도 있습니다:

```shell
composer require laravel/reverb
```

패키지 설치 후에는, Reverb의 설치 명령어를 실행해 설정을 배포하고, 필요한 환경 변수를 추가하며, 애플리케이션에서 이벤트 브로드캐스팅을 활성화하세요:

```shell
php artisan reverb:install
```

자세한 Reverb 설치 및 사용 방법은 [Reverb 문서](/docs/master/reverb)에서 확인할 수 있습니다.

<a name="pusher-channels"></a>
### Pusher Channels

Pusher를 이벤트 브로드캐스터로 사용할 때, Laravel의 브로드캐스트를 빠르게 활성화하려면 `install:broadcasting` Artisan 명령어에 `--pusher` 옵션을 추가하여 실행하세요. 이 명령어는 Pusher 인증 정보를 입력받고, Pusher PHP 및 JavaScript SDK 설치, 환경 변수 업데이트까지 처리합니다:

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### 수동 설치

Pusher를 수동으로 지원하려면 Composer 패키지 매니저로 Pusher Channels PHP SDK를 설치하세요:

```shell
composer require pusher/pusher-php-server
```

그 다음, `config/broadcasting.php` 설정 파일에 Pusher Channels 인증 정보를 입력합니다. 이 파일에는 이미 Pusher 설정 예시가 포함되어 있으므로, 키, 시크릿, 애플리케이션 ID만 지정해주면 됩니다. 보통 `.env` 파일에 다음과 같이 입력합니다:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php`의 `pusher` 설정에서는 cluster와 같은 추가 옵션도 지정할 수 있습니다.

애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 설정하세요:

```ini
BROADCAST_CONNECTION=pusher
```

이제 [Laravel Echo 설치 및 설정](#client-side-installation)을 진행할 준비가 되었습니다. Echo는 클라이언트에서 브로드캐스트 이벤트를 수신합니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 문서는 Ably를 "Pusher 호환 모드"로 사용하는 방법을 설명합니다. 하지만, Ably 팀에서는 Ably만의 고유 기능을 활용할 수 있는 브로드캐스터 및 Echo 클라이언트를 별도로 유지·추천하고 있습니다. Ably의 공식 드라이버 사용 방법은 [Ably 라라벨 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 이벤트 브로드캐스터로 사용할 때, 빠르게 Laravel 브로드캐스트 지원을 활성화하려면 `install:broadcasting` Artisan 명령어에 `--ably` 옵션을 추가해서 실행하세요. 이 명령어는 Ably 인증 정보를 입력받고, Ably PHP 및 JavaScript SDK 설치, 그리고 환경 변수 업데이트를 자동으로 처리합니다:

```shell
php artisan install:broadcasting --ably
```

**계속하기 전에, Ably 애플리케이션 설정에서 반드시 Pusher 프로토콜 지원을 활성화해야 합니다. 해당 기능은 Ably 애플리케이션의 "Protocol Adapter Settings" 대시보드에서 변경할 수 있습니다.**

<a name="ably-manual-installation"></a>
#### 수동 설치

Ably 지원을 수동으로 추가하려면 Composer 패키지 매니저로 Ably PHP SDK를 설치하세요:

```shell
composer require ably/ably-php
```

그 다음, `config/broadcasting.php` 설정 파일에서 Ably 인증 정보를 입력하세요. 예제 설정이 이미 포함되어 있으니, 키 값만 지정하면 됩니다. 보통 환경 변수 `ABLY_KEY`를 통해 값을 전달합니다:

```ini
ABLY_KEY=your-ably-key
```

`.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 설정하세요:

```ini
BROADCAST_CONNECTION=ably
```

이제 [Laravel Echo 설치 및 설정](#client-side-installation)을 진행할 준비가 되었습니다.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치 (Client Side Installation)

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스트 드라이버가 브로드캐스트한 이벤트를 구독하고 수신하는 JavaScript 라이브러리입니다.

`install:broadcasting` Artisan 명령어를 통해 Reverb를 설치하면, Echo의 기본 구성과 설정이 자동으로 애플리케이션에 반영됩니다. 하지만 Echo를 직접 수동 설정하고자 한다면 아래 가이드를 참고하세요.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 수동으로 설정하려면, 먼저 `pusher-js` 패키지를 설치해야 합니다. Reverb는 WebSocket 구독 및 메시지 전송을 위하여 Pusher 프로토콜을 사용합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치 후에는 애플리케이션의 JavaScript에서 Echo 인스턴스를 생성할 수 있습니다. 보통 Laravel이 기본 제공하는 `resources/js/bootstrap.js` 파일 하단에 추가하는 것이 좋습니다:

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

애플리케이션 에셋을 빌드하세요:

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` 브로드캐스터는 laravel-echo v1.16.0 이상에서만 지원됩니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스트 드라이버가 브로드캐스트한 이벤트를 구독하고 수신하는 JavaScript 라이브러리입니다.

`install:broadcasting --pusher` Artisan 명령어를 통해 Pusher 및 Echo의 기본 구성과 설정이 자동으로 적용됩니다. 하지만, Echo를 직접 수동 설정하고자 한다면 아래 가이드를 참고하세요.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 수동으로 설정하려면, `laravel-echo`와 `pusher-js` 패키지를 설치해야 합니다. 이 두 패키지는 WebSocket 구독, 채널, 메시징에 Pusher 프로토콜을 사용합니다:

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo가 설치되었다면, 애플리케이션의 `resources/js/bootstrap.js` 파일에서 Echo 인스턴스를 생성합니다:

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

애플리케이션의 `.env` 파일에서 Pusher 환경 변수 값을 올바르게 지정하세요. 만약 아직 없다면, 다음과 같이 추가합니다:

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

Echo 설정을 맞췄다면 애플리케이션 에셋을 빌드합니다:

```shell
npm run build
```

> [!NOTE]
> 애플리케이션의 JavaScript 에셋 빌드에 대해 더 알고 싶다면 [Vite](/docs/master/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

이미 사전에 설정된 Pusher Channels 클라이언트 인스턴스가 있으면 Echo에 `client` 옵션으로 전달할 수 있습니다:

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
### Ably

> [!NOTE]
> 아래 문서는 Ably를 "Pusher 호환 모드"로 사용하는 방법을 설명합니다. 고유한 Ably 드라이버 사용법은 [Ably 라라벨 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스트 드라이버가 브로드캐스트한 이벤트를 구독하고 수신하는 JavaScript 라이브러리입니다.

`install:broadcasting --ably` Artisan 명령어를 통해 Ably 및 Echo의 기본 구성과 설정이 자동으로 적용됩니다. Echo를 직접 수동으로 설정하려면 아래 방법을 참고하세요.

<a name="ably-client-manual-installation"></a>
#### 수동 설치

애플리케이션의 프론트엔드에서 Laravel Echo를 수동 설정하려면, Pusher 프로토콜용 `laravel-echo` 및 `pusher-js` 패키지를 설치하세요:

```shell
npm install --save-dev laravel-echo pusher-js
```

**계속하기 전에, Ably 애플리케이션 설정에서 반드시 Pusher 프로토콜 지원을 활성화하세요. 해당 기능은 "Protocol Adapter Settings" 대시보드에서 설정할 수 있습니다.**

Echo 설치 후에는, `resources/js/bootstrap.js` 파일에서 Echo 인스턴스를 생성하세요:

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

Ably Echo 구성에서 사용되는 `VITE_ABLY_PUBLIC_KEY` 환경 변수값에는 Ably 퍼블릭 키를 입력해야 합니다. Ably 키에서 `:` 문자 앞까지가 퍼블릭 키입니다.

설정을 완료했다면 애플리케이션 에셋을 빌드하세요:

```shell
npm run dev
```

> [!NOTE]
> 자바스크립트 에셋 빌드에 대한 자세한 내용은 [Vite](/docs/master/vite) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

Laravel의 이벤트 브로드캐스팅은 드라이버 기반의 WebSocket 접근 방식으로 서버 사이드 이벤트를 클라이언트 사이드 JavaScript 애플리케이션에 브로드캐스팅할 수 있습니다. 현재 Laravel에서는 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 드라이버를 사용할 수 있습니다. 클라이언트에서는 [Laravel Echo](#client-side-installation) JavaScript 패키지로 간단히 이벤트를 수신할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트됩니다. 채널은 공개(public)나 비공개(private)로 지정할 수 있습니다. 누구나 인증 없이 공개 채널에 구독할 수 있지만, 비공개 채널은 사용자가 해당 채널을 리스닝할 수 있도록 인증 및 인가를 받아야만 구독이 가능합니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용하기

이벤트 브로드캐스팅의 각 요소로 들어가기 전에, 전자상거래 스토어를 예시로 전체적인 흐름을 살펴보겠습니다.

본 애플리케이션에는 사용자가 자신의 주문 배송 상태를 확인할 수 있는 페이지가 있다고 가정하겠습니다. 그리고 애플리케이션에서 배송 상태가 변경되면 `OrderShipmentStatusUpdated` 이벤트가 발생합니다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 주문 정보를 보는 중에는, 페이지를 새로 고치지 않고 상태 변경 알림을 받고 싶을 수 있습니다. 이를 위해서는 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 구현해야 합니다. 이렇게 하면 이벤트가 발생할 때 자동으로 브로드캐스트됩니다:

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

`ShouldBroadcast` 인터페이스를 구현하면 반드시 `broadcastOn` 메서드를 정의해야 합니다. 이 메서드는 이벤트를 브로드캐스트할 채널을 반환해야 합니다. 기본적으로 이벤트 클래스에는 비어있는 `broadcastOn` 메서드 스텁이 생성되어 있으니, 필요한 내용을 채워주면 됩니다. 주문을 생성한 사용자만 상태 알림을 볼 수 있도록, 주문에 연결된 비공개 채널로 브로드캐스트하도록 작성합니다:

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

여러 채널로 이벤트를 브로드캐스트하고 싶다면 `array`를 반환하면 됩니다:

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
#### 채널 인가(Authorization)

비공개 채널을 구독하려면 사용자 인가가 필요합니다. 인가 규칙은 애플리케이션의 `routes/channels.php` 파일에서 정의할 수 있습니다. 예를 들어, 다음 코드에서는 비공개 `orders.1` 채널에 구독을 시도하는 사용자가 실제로 해당 주문의 생성자인지 확인합니다:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널명을 첫 번째 인수로, 사용자가 해당 채널을 리스닝할 수 있는지를 true/false로 반환하는 콜백을 두 번째 인수로 받습니다.

모든 인가 콜백은 현재 인증된 사용자를 첫 번째 인수로 전달받고, 이어서 와일드카드로 지정된 채널 파라미터가 전달됩니다. 예시에서는 `{orderId}` 플레이스홀더를 사용하여 채널 이름의 "ID" 부분을 와일드카드로 처리합니다.

<a name="listening-for-event-broadcasts"></a>
#### 브로드캐스트 이벤트 리스닝

이제 남은 것은 JavaScript 애플리케이션에서 이벤트를 리스닝하는 일입니다. [Laravel Echo](#client-side-installation)를 활용하세요. Echo의 React, Vue hook을 사용하면 쉽게 시작할 수 있고, 기본적으로 이벤트의 public 속성 모두가 브로드캐스트 데이터에 포함됩니다:

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
## 브로드캐스트 이벤트 정의하기 (Defining Broadcast Events)

특정 이벤트를 브로드캐스트하도록 Laravel에 알리려면, 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 모든 Laravel 이벤트 클래스에 이미 `use` 구문을 통해 포함되어 있으므로 쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스를 구현하면 반드시 하나의 메서드, 즉 `broadcastOn`만 구현하면 됩니다. 이 메서드는 이벤트를 브로드캐스트할 채널 혹은 채널의 배열을 반환해야 합니다. 반환값은 `Channel`, `PrivateChannel`, `PresenceChannel` 클래스의 인스턴스여야 합니다. `Channel`은 인증 없이 누구나 구독할 수 있는 공개 채널, `PrivateChannel`과 `PresenceChannel`은 [채널 인가](#authorizing-channels)가 요구되는 비공개 채널입니다:

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

`ShouldBroadcast` 인터페이스를 구현했다면, [이벤트 발생](/docs/master/events)과 동일하게 이벤트를 dispatch만 하면 됩니다. 이벤트가 발생하면 [큐에 등록된 작업](/docs/master/queues)이 자동으로 이벤트를 브로드캐스트해 줍니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트 클래스의 이름을 그대로 브로드캐스트 이벤트 이름으로 사용합니다. 하지만, `broadcastAs` 메서드를 정의하면 원하는 이름으로 커스터마이즈할 수 있습니다:

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

이렇게 커스텀 이름을 사용하면, 리스너 등록 시 이벤트 앞에 `.`(dot) 문자를 붙여야 Echo가 앱의 네임스페이스를 자동으로 추가하지 않게 됩니다:

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트 브로드캐스트 시, public 속성들은 자동으로 직렬화되어 이벤트의 payload로 전송됩니다. 따라서 JavaScript 애플리케이션에서 해당 데이터를 바로 사용할 수 있습니다. 예를 들어, public `$user` 속성이 Eloquent 모델을 담고 있다면 결과 payload는 다음과 같이 전달됩니다:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

보다 상세하게 payload를 제어하려면, 이벤트 클래스에 `broadcastWith` 메서드를 추가해서 브로드캐스트할 데이터 배열을 직접 반환할 수 있습니다:

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
### 브로드캐스트 큐

기본적으로 브로드캐스트 이벤트는 `queue.php`에서 지정한 기본 큐의 기본 커넥션에 저장됩니다. 이벤트 클래스에 `Connection`, `Queue` 속성(Attribute)을 추가해 연결과 큐 이름을 따로 지정할 수 있습니다:

```php
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Queue;

#[Connection('redis')]
#[Queue('default')]
class ServerCreated implements ShouldBroadcast
{
    // ...
}
```

또는, 이벤트 클래스에 `broadcastQueue` 메서드를 구현해 큐 이름만 바꿀 수도 있습니다:

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

만약 기본 큐 드라이버 대신 `sync` 큐로 브로드캐스트하고자 한다면, `ShouldBroadcastNow` 인터페이스를 구현하세요:

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
### 브로드캐스트 조건

특정 조건일 때만 이벤트를 브로드캐스트하고 싶다면, 이벤트 클래스에 `broadcastWhen` 메서드를 추가하세요:

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
#### 브로드캐스팅과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 안에서 브로드캐스트 이벤트를 발생시키면, 큐에서 트랜잭션 커밋 이전에 작업이 처리될 수 있습니다. 이런 경우, 트랜잭션 내에서 변경된 모델이나 레코드가 아직 DB에 반영되지 않아, 큐 작업이 처리될 때 의도하지 않은 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 설정이 `false`일 때, 특정 브로드캐스트 이벤트에 한해 모든 열린 데이터베이스 트랜잭션 커밋 이후에 작업을 실행하려면 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요:

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
> 이런 문제에 대한 우회 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 인가 처리 (Authorizing Channels)

비공개 채널에 구독하려면 현재 인증된 사용자가 해당 채널 청취 권한이 있는지 인가해주어야 합니다. 이 과정은 클라이언트가 채널명을 포함해 Laravel 애플리케이션에 HTTP 요청을 보내고, 서버에서 인가 여부를 판단하는 방식으로 진행됩니다. [Laravel Echo](#client-side-installation)를 사용하면 이 인가 요청이 자동으로 전송됩니다.

브로드캐스팅을 설치하면 Laravel이 `/broadcasting/auth` 라우트를 자동으로 등록합니다. 만약 자동 등록이 실패하면 `/bootstrap/app.php` 파일에서 직접 명시할 수 있습니다:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    channels: __DIR__.'/../routes/channels.php',
    health: '/up',
)
```

<a name="defining-authorization-callbacks"></a>
### 인가 콜백 정의하기

이제 실제로 인증된 사용자가 특정 채널을 리스닝할 권한이 있는지 검사하는 로직을 정의해보겠습니다. 이 코드는 `install:broadcasting` Artisan 명령어로 생성된 `routes/channels.php` 파일에 작성합니다. `Broadcast::channel` 메서드를 사용해 채널 인가 콜백을 등록할 수 있습니다:

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널명과 true/false를 반환하는 콜백을 인수로 받습니다.

콜백에는 인증된 사용자 객체가 첫 번째 인수로, 나머지 와일드카드 파라미터들이 순서대로 전달됩니다. 여기서 `{orderId}`는 채널명에서 와일드카드(플레이스홀더)로 쓰였습니다.

애플리케이션의 브로드캐스트 인가 콜백 목록은 `channel:list` Artisan 명령어로 확인할 수 있습니다:

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 인가 콜백의 모델 바인딩

HTTP 라우트와 마찬가지로 채널 라우트도 암묵적/명시적 [라우트 모델 바인딩](/docs/master/routing#route-model-binding)이 가능합니다. 즉, 문자열이나 숫자 대신 실제 모델 인스턴스를 인수로 받을 수 있습니다:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과 달리 채널 모델 바인딩은 [암묵적 모델 바인딩 범위](/docs/master/routing#implicit-model-binding-scoping)를 지원하지 않습니다. 하지만 대부분의 경우, 한 모델의 기본 키로 범위 지정이 가능하므로 문제가 되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 인가 콜백의 인증

비공개 및 프레젠스 브로드캐스트 채널은 애플리케이션의 기본 인증 가드(guard)를 사용해 인증합니다. 사용자가 인증되지 않았다면, 인가 요청이 자동 거부되고 콜백이 실행되지 않습니다. 필요에 따라 여러 개의 커스텀 가드를 지정할 수도 있습니다:

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의하기

애플리케이션에서 많은 채널을 다루다 보면 `routes/channels.php` 파일이 복잡해질 수 있습니다. 이때는 클로저 대신 채널 클래스를 사용할 수 있습니다. 채널 클래스는 `make:channel` Artisan 명령어로 생성하고, `App/Broadcasting` 디렉토리에 위치합니다.

```shell
php artisan make:channel OrderChannel
```

이제 `routes/channels.php` 파일에 채널을 등록하세요:

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

채널 클래스의 `join` 메서드에 실제 인가 로직을 작성합니다. 또한, 모델 바인딩도 그대로 활용 가능합니다:

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
> Laravel의 다른 클래스처럼, 채널 클래스도 [서비스 컨테이너](/docs/master/container)에 의해 자동으로 해석되므로, 생성자에 의존성을 타입힌트로 선언할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅 (Broadcasting Events)

이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 추가했다면, 이벤트 클래스의 dispatch 메서드를 사용해 이벤트를 단순 발생시키기만 하면 됩니다. 이벤트 디스패처는 이벤트가 `ShouldBroadcast`임을 인식하고 브로드캐스트 처리를 큐에 등록합니다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 다른 사용자에게만 브로드캐스팅

이벤트 브로드캐스팅 사용 시 때로는 현재 사용자 이외의 모든 구독자에게만 이벤트를 브로드캐스팅하고 싶은 경우가 있습니다. 이때는 `broadcast` 헬퍼와 `toOthers` 메서드를 사용하면 됩니다:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

구체적으로 언제 `toOthers`를 사용해야 할지 이해하려면, 예를 들어 할 일 목록 애플리케이션을 생각해보세요. 사용자가 새로운 할 일을 추가할 때 `/task` URL로 요청하여 생성과 동시에 JSON 데이터를 받아 리스트에 추가한다고 가정합니다:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

이때, Task 생성 이벤트도 브로드캐스트했다면, JS 애플리케이션에서 브로드캐스트 이벤트를 수신해 다시 리스트에 할 일을 추가하게 되어, 같은 할 일이 중복으로 표시됩니다. `toOthers` 메서드를 사용하면 현재 사용자(요청을 보낸 브라우저)에는 브로드캐스트가 전달되지 않으므로 중복 문제가 해결됩니다.

> [!WARNING]
> `toOthers` 메서드를 사용하려면 반드시 이벤트에 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트를 추가해야 합니다.

<a name="only-to-others-configuration"></a>
#### 설정 방법

Laravel Echo 인스턴스를 초기화하면, 소켓 ID가 연결에 할당됩니다. 만약 전역 [Axios](https://github.com/axios/axios) 인스턴스를 사용해서 요청을 전송한다면, `X-Socket-ID` 헤더가 자동으로 추가됩니다. `toOthers` 호출 시 Laravel은 이 헤더에서 소켓 ID를 추출하고 해당 연결에는 브로드캐스트하지 않습니다.

전역 Axios를 사용하지 않는다면 모든 요청에 직접 `X-Socket-ID` 헤더를 추가해야 하며, `Echo.socketId` 메서드로 값을 얻을 수 있습니다:

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 커넥션 커스터마이징

여러 브로드캐스팅 커넥션을 사용하는 경우, 기본 브로드캐스터가 아니라 특정 커넥션을 사용하고 싶을 때는 `via` 메서드로 연결을 지정할 수 있습니다:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는, 이벤트 클래스에서 `InteractsWithBroadcasting` 트레이트를 추가하고, 생성자 내에서 `broadcastVia` 메서드로 지정할 수도 있습니다:

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
### 익명 이벤트

간단한 이벤트를 별도의 이벤트 클래스 없이 프론트엔드에 브로드캐스트하고 싶다면, `Broadcast` 파사드를 통한 "익명 이벤트" 브로드캐스트를 활용할 수 있습니다:

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 코드는 다음과 같이 브로드캐스트됩니다:

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

이벤트 이름과 데이터를 `as`, `with` 메서드로 커스터마이즈할 수 있습니다:

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

이 경우 다음과 같이 브로드캐스트됩니다:

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

비공개 또는 프레젠스 채널로 익명 이벤트를 브로드캐스트하려면 `private`, `presence` 메서드를 사용하세요:

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send` 메서드는 이벤트를 [큐](/docs/master/queues)에 등록하여 처리합니다. 즉시 브로드캐스트하고 싶으면 `sendNow`를 사용하면 됩니다:

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 인증된 사용자를 제외한 모든 구독자에게 브로드캐스트하려면 `toOthers` 메서드를 사용하세요:

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
### 브로드캐스트 예외 구제하기

큐 서버에 장애가 있거나 Laravel이 브로드캐스트 중 오류를 만나면 예외가 발생하여, 사용자는 애플리케이션 오류를 볼 수 있습니다. 하지만 이벤트 브로드캐스팅은 핵심 기능이 아닌 부가 기능인 경우가 많으므로, 이런 예외로 인해 사용자 경험이 망가지지 않게 처리할 필요가 있습니다. 이를 위해 이벤트 클래스에 `ShouldRescue` 인터페이스를 구현하세요.

`ShouldRescue`를 구현한 이벤트는 브로드캐스트 처리 중 [rescue 헬퍼 함수](/docs/master/helpers#method-rescue)가 자동 적용됩니다. rescue는 예외를 캐치해서 애플리케이션의 예외 핸들러에 기록만 남기고, 사용자의 애플리케이션 흐름에는 영향을 주지 않습니다:

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
## 브로드캐스트 수신 (Receiving Broadcasts)

<a name="listening-for-events"></a>
### 이벤트 리스닝

[Laravel Echo 설치 및 인스턴스 생성](#client-side-installation)을 마쳤다면 서버에서 브로드캐스트된 이벤트를 리스닝할 준비가 된 것입니다. 먼저 `channel` 메서드를 사용해 채널 인스턴스를 얻고, `listen` 메서드로 원하는 이벤트를 감지하세요:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널에서는 `private` 메서드를 대신 사용하세요. 다수의 이벤트를 하나의 채널에서 연속적으로 감지할 수도 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 리스닝 중지

채널을 [떠나지 않고](#leaving-a-channel)도 특정 이벤트 리스닝만 중지하려면 `stopListening` 메서드를 사용하세요:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### 채널 떠나기

특정 채널에서 나가려면 Echo 인스턴스의 `leaveChannel` 메서드를 호출하세요:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

해당 채널뿐 아니라 연관된 프라이빗, 프레젠스 채널도 함께 나가려면 `leave` 메서드를 사용합니다:

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

예제 코드에서는 이벤트 클래스 이름에 `App\Events` 네임스페이스를 명시하지 않았습니다. 이는 Echo가 기본적으로 이벤트가 `App\Events` 네임스페이스에 있다고 가정하기 때문입니다. 필요하다면 Echo 인스턴스 생성 시 `namespace` 옵션으로 네임스페이스를 직접 지정할 수 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는, Echo로 구독할 때 이벤트 클래스 앞에 `.`(dot)을 붙여 항상 전체 클래스명을 명시하는 것도 가능합니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
### React 또는 Vue 사용하기

Laravel Echo는 React, Vue에서 사용할 수 있는 hook을 제공합니다. 가장 기본적으로는 `useEcho` hook을 통해 비공개 이벤트를 리스닝합니다. 이 hook은 컴포넌트가 언마운트될 때 자동으로 채널을 떠나도록 처리합니다:

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

여러 이벤트를 동시에 리스닝하려면 이벤트명 배열을 전달하면 됩니다:

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

브로드캐스트 이벤트의 데이터 타입도 명시해 타입 안정성과 코드 편의성을 높일 수 있습니다:

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

`useEcho` hook은 자동으로 채널을 떠나도록 처리하지만, 반환값의 함수로 리스닝 일시 정지/시작, 채널 떠나기 등을 직접 제어할 수도 있습니다:

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// 리스닝만 중지...
stopListening();

// 다시 리스닝...
listen();

// 채널 떠나기...
leaveChannel();

// 프라이빗/프레젠스 채널까지 함께 떠나기...
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

// 리스닝만 중지...
stopListening();

// 다시 리스닝...
listen();

// 채널 떠나기...
leaveChannel();

// 프라이빗/프레젠스 채널까지 함께 떠나기...
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>
#### 공개 채널 연결

공개 채널에 연결하려면 `useEchoPublic` hook을 사용하세요:

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
#### 프레젠스 채널 연결

프레젠스 채널에 연결하려면 `useEchoPresence` hook을 사용하세요:

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
#### 연결 상태 확인

`useConnectionStatus` hook을 사용해 WebSocket의 현재 연결 상태를 실시간으로 확인할 수 있습니다. 상태가 바뀔 때마다 값이 자동 갱신됩니다:

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

사용 가능한 상태 값은 아래와 같습니다:

<div class="content-list" markdown="1">

- `connected` - WebSocket 서버에 성공적으로 연결됨
- `connecting` - 초기 연결 시도 중
- `reconnecting` - 연결 해제 후 재연결 시도 중
- `disconnected` - 연결되어 있지 않고 재연결 시도 없음
- `failed` - 연결 실패, 더 이상 재연결하지 않음

</div>

<a name="presence-channels"></a>
## 프레젠스 채널 (Presence Channels)

프레젠스 채널은 비공개 채널의 보안 위에, 누가 채널에 구독 중인지까지 알 수 있는 추가 기능이 제공됩니다. 예를 들어, 같은 페이지를 보거나, 채팅룸에 접속한 사용자를 실시간으로 표시하는 협업 기능이 쉽게 구현됩니다.

<a name="authorizing-presence-channels"></a>
### 프레젠스 채널 인가하기

모든 프레젠스 채널 역시 비공개 채널이므로, [인증 및 인가](#authorizing-channels)가 필요합니다. 이때 인가 콜백에서는 단순히 true를 반환하지 않고, 사용자의 정보를 담은 배열을 반환해야 합니다.

이 콜백에서 반환한 데이터는 프론트엔드의 프레젠스 채널 이벤트 리스너에서 바로 사용할 수 있습니다. 사용자가 접속을 허용받을 수 없다면 false나 null을 반환하세요:

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레젠스 채널 참여하기

Echo의 `join` 메서드로 프레젠스 채널에 참여할 수 있습니다. 반환된 `PresenceChannel` 객체에서는 `listen` 뿐 아니라, `here`, `joining`, `leaving` 이벤트에 구독할 수 있습니다.

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

`here` 콜백은 채널에 성공적으로 입장하면 바로 실행되며, 현재 채널에 구독 중인 다른 사용자의 정보를 배열로 제공합니다. `joining`은 새로운 사용자가 채널에 참여할 때, `leaving`은 사용자가 떠날 때, `error`는 인증 엔드포인트가 200이 아닌 값을 반환하거나 JSON 파싱 문제 발생 시 호출됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레젠스 채널로 브로드캐스팅

프레젠스 채널 역시 공개/비공개 채널과 마찬가지로 이벤트를 수신할 수 있습니다. 예를 들어, 채팅방에서 `NewMessage` 이벤트를 해당 프레젠스 채널로 브로드캐스트하려면, 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel`을 반환하면 됩니다:

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

다른 이벤트들처럼 `broadcast`와 `toOthers` 메서드를 활용해 현재 사용자를 제외한 구독자에게만 브로드캐스트할 수 있습니다:

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

Echo의 `listen` 메서드로 프레젠스 채널에 브로드캐스트된 이벤트를 감지할 수 있습니다:

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
## 모델 브로드캐스팅 (Model Broadcasting)

> [!WARNING]
> 아래의 모델 브로드캐스팅 문서를 읽기 전에, 먼저 Laravel의 일반적인 모델 브로드캐스팅 개념과 수동 이벤트 생성/리스닝 방법을 이해하는 것이 좋습니다.

애플리케이션의 [Eloquent 모델](/docs/master/eloquent)이 생성, 수정, 삭제될 때 이벤트를 브로드캐스트하는 일은 흔하게 발생합니다. 보통 이를 위해 [수동으로 커스텀 이벤트를 정의](/docs/master/eloquent#events)하고 `ShouldBroadcast`를 구현하는 방식을 사용합니다.

하지만, 이벤트를 오직 브로드캐스팅 목적으로만 만든다면 이벤트 클래스를 만드는 것이 번거로울 수 있습니다. 이를 해결하기 위해 Laravel에서는 Eloquent 모델이 상태 변경 시 자동으로 이벤트를 브로드캐스트할 수 있게 해줍니다.

시작하려면, Eloquent 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 추가하고, 모델의 이벤트를 브로드캐스트할 채널을 반환하는 `broadcastOn` 메서드를 정의하세요:

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

이렇게 트레이트와 채널 메서드를 추가하면, 모델 인스턴스가 생성, 수정, 삭제, 휴지통 이동, 복구될 때마다 자동으로 이벤트가 브로드캐스트됩니다.

또한 `broadcastOn` 메서드는 발생한 이벤트의 종류를 나타내는 `$event` 문자열 인수를 받습니다. 값은 `created`, `updated`, `deleted`, `trashed`, `restored` 중 하나입니다. 이를 활용해 이벤트 종류별로 채널 반환값을 다르게 지정할 수 있습니다:

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
#### 모델 브로드캐스트 이벤트 생성 커스터마이징

Laravel의 내부 모델 브로드캐스트 이벤트 생성 방식을 커스터마이즈하고 싶다면, 모델에 `newBroadcastableEvent` 메서드를 정의하세요. 반환값은 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스여야 합니다:

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
### 모델 브로드캐스팅 규칙

<a name="model-broadcasting-channel-conventions"></a>
#### 채널 규칙

앞서 예제에서 `broadcastOn` 메서드는 `Channel` 인스턴스 대신 Eloquent 모델을 반환했습니다. 만약 `broadcastOn`에서 Eloquent 모델 인스턴스를 반환하거나 배열에 포함하면, Laravel은 자동으로 해당 모델 클래스명과 기본 키를 조합해 비공개 채널을 생성합니다.

예를 들어, `App\Models\User` 모델의 `id`가 `1`이면, `Illuminate\Broadcasting\PrivateChannel` 인스턴스의 채널명은 `App.Models.User.1`이 됩니다. 물론 직접 `Channel` 인스턴스를 반환하여 채널명을 완전히 제어할 수도 있습니다:

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

`broadcastOn`에서 채널의 생성자에 모델 인스턴스를 전달하는 것도 가능합니다. 이 경우는 위에서 설명한 모델 채널 규칙이 자동 적용됩니다:

```php
return [new Channel($this->user)];
```

모델의 채널명을 알고 싶다면, 어떤 모델 인스턴스에서든 `broadcastChannel` 메서드를 호출하세요. 예를 들어, `App\Models\User`의 `id`가 `1`하면, 이 메서드는 `App.Models.User.1`을 반환합니다:

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규칙

모델 브로드캐스트 이벤트는 실제 `App\Events` 디렉터리의 이벤트와 연결되어 있지 않으므로, 이벤트명과 페이로드는 규칙에 따라 자동 지정됩니다. Laravel은 "모델 클래스명(네임스페이스 제외)" + "모델 이벤트명" 조합으로 이벤트명을 결정합니다.

예를 들어, `App\Models\Post` 업데이트는 `PostUpdated` 이벤트명이 되어 아래와 같은 페이로드로 클라이언트에 브로드캐스트됩니다:

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

`App\Models\User` 모델 삭제는 `UserDeleted` 이벤트명이 됩니다.

원한다면, `broadcastAs`와 `broadcastWith` 메서드를 모델에 추가해 각 모델 이벤트별로 이벤트명과 페이로드를 지정할 수 있습니다(둘 다 인수로 모델 이벤트명을 받음). `broadcastAs`에서 null을 반환하면 위에서 설명한 기본 규칙이 적용됩니다:

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
### 모델 브로드캐스트 리스닝

`BroadcastsEvents` 트레이트를 모델에 추가하고, `broadcastOn` 메서드를 정의했다면 이제 클라이언트에서 브로드캐스팅된 모델 이벤트를 리스닝할 수 있습니다. 먼저 [이벤트 리스닝 전체 문서](#listening-for-events)를 참고하는 것이 좋습니다.

기본적으로는 `private` 메서드로 채널 인스턴스를 얻고, `listen`으로 특정 이벤트를 감지합니다. 모델 브로드캐스팅 규칙에 따라 채널명을 지정해야 하며, 이벤트명 앞에는 네임스페이스가 없으므로 반드시 `.`(dot)을 붙여야 합니다. 모델 이벤트 페이로드에는 항상 `model` 속성에 모델 데이터가 포함되어 있습니다:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
#### React 또는 Vue에서 모델 브로드캐스트 리스닝

React, Vue 환경에서는 Echo의 `useEchoModel` hook을 사용해 간단히 모델 브로드캐스팅 이벤트를 리스닝할 수 있습니다:

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

타입 안정성과 코드 편의성 강화를 위해 브로드캐스팅 데이터 타입도 지정할 수 있습니다:

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
## 클라이언트 이벤트 (Client Events)

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels) 사용 시, [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings"에서 "Client Events" 옵션을 반드시 활성화해야 클라이언트 이벤트를 전송할 수 있습니다.

때로는 Laravel 애플리케이션을 거치지 않고, 연결된 다른 클라이언트에게만 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 예를 들어, 채팅에서 "입력 중..." 알림처럼 다른 사용자에게 동작을 알려야 할 경우가 그 예입니다.

클라이언트 이벤트 브로드캐스트는 Echo의 `whisper` 메서드를 사용하세요:

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

클라이언트 이벤트 수신은 `listenForWhisper` 메서드로 할 수 있습니다:

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
## 알림 (Notifications)

이벤트 브로드캐스팅과 [알림](/docs/master/notifications)을 결합해, 사용자에게 새로운 알림이 발생할 때마다 페이지 새로 고침 없이 바로 JavaScript 애플리케이션에서 수신할 수 있습니다. 시작하기 전에 [브로드캐스트 알림 채널](/docs/master/notifications#broadcast-notifications) 사용법을 미리 읽어두세요.

알림이 브로드캐스트 채널을 사용하도록 설정했다면, Echo의 `notification` 메서드로 브로드캐스트 이벤트를 리스닝할 수 있습니다. 이때 채널명은 알림의 수신 엔터티 클래스명과 일치해야 합니다:

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

이 예시에서는, `App\Models\User` 인스턴스에 `broadcast` 채널을 통해 전달된 모든 알림을 콜백에서 수신할 수 있습니다. `App.Models.User.{id}` 채널에 대한 인가 콜백은 기본적으로 `routes/channels.php`에 포함되어 있습니다.

<a name="stop-listening-for-notifications"></a>
#### 알림 리스닝 중지

채널을 [떠나지 않고](#leaving-a-channel)도 알림 리스닝만 중지할 수 있습니다. 이때는 `stopListeningForNotification` 메서드를 사용하세요:

```js
const callback = (notification) => {
    console.log(notification.type);
}

// 리스닝 시작...
Echo.private(`App.Models.User.${userId}`)
    .notification(callback);

// 리스닝 중지(콜백은 동일해야 함)...
Echo.private(`App.Models.User.${userId}`)
    .stopListeningForNotification(callback);
```
