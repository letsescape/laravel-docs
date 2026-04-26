# 브로드캐스팅 (Broadcasting)

- [소개](#introduction)
- [빠른 시작](#quickstart)
- [서버 측 설치](#server-side-installation)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
- [클라이언트 측 설치](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
- [개념 개요](#concept-overview)
    - [예제 애플리케이션 사용](#using-example-application)
- [브로드캐스트 이벤트 정의](#defining-broadcast-events)
    - [브로드캐스트 이름](#broadcast-name)
    - [브로드캐스트 데이터](#broadcast-data)
    - [브로드캐스트 큐](#broadcast-queue)
    - [브로드캐스트 조건](#broadcast-conditions)
    - [브로드캐스팅과 데이터베이스 트랜잭션](#broadcasting-and-database-transactions)
- [채널 인가](#authorizing-channels)
    - [인가 콜백 정의](#defining-authorization-callbacks)
    - [채널 클래스 정의](#defining-channel-classes)
- [이벤트 브로드캐스팅](#broadcasting-events)
    - [다른 사용자에게만](#only-to-others)
    - [연결 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
    - [브로드캐스트 복구](#rescuing-broadcasts)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널 떠나기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
    - [React, Vue 또는 Svelte 사용](#using-react-or-vue)
- [Presence 채널](#presence-channels)
    - [Presence 채널 인가](#authorizing-presence-channels)
    - [Presence 채널 참여](#joining-presence-channels)
    - [Presence 채널로 브로드캐스팅](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림](#notifications)

<a name="introduction"></a>
## 소개 (Introduction)

많은 현대 웹 애플리케이션에서는 실시간으로 계속 업데이트되는 사용자 인터페이스를 구현하기 위해 WebSocket을 사용합니다. 서버에서 어떤 데이터가 업데이트되면, 일반적으로 클라이언트가 처리할 수 있도록 WebSocket 연결을 통해 메시지가 전송됩니다. WebSocket은 UI에 반영되어야 하는 데이터 변경 사항을 확인하기 위해 애플리케이션 서버를 계속 폴링하는 방식보다 더 효율적인 대안을 제공합니다.

예를 들어, 애플리케이션이 사용자의 데이터를 CSV 파일로 내보내고 이메일로 보낼 수 있다고 가정해 보겠습니다. 하지만 이 CSV 파일을 만드는 데 몇 분이 걸리기 때문에, CSV 생성과 발송을 [큐 작업](/docs/13.x/queues) 안에서 처리하기로 선택합니다. CSV가 생성되어 사용자에게 이메일로 전송되면, 이벤트 브로드캐스팅을 사용해 `App\Events\UserDataExported` 이벤트를 디스패치할 수 있으며, 이 이벤트는 애플리케이션의 JavaScript에서 수신됩니다. 이벤트를 수신하면 사용자가 페이지를 새로고침하지 않아도 CSV가 이메일로 전송되었다는 메시지를 표시할 수 있습니다.

이러한 기능을 쉽게 만들 수 있도록 Laravel은 서버 측 Laravel [이벤트](/docs/13.x/events)를 WebSocket 연결을 통해 "브로드캐스트"하기 쉽게 해줍니다. Laravel 이벤트를 브로드캐스트하면 서버 측 Laravel 애플리케이션과 클라이언트 측 JavaScript 애플리케이션 사이에서 동일한 이벤트 이름과 데이터를 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 단순합니다. 클라이언트는 프론트엔드에서 이름이 있는 채널에 연결하고, Laravel 애플리케이션은 백엔드에서 이 채널들로 이벤트를 브로드캐스트합니다. 이러한 이벤트에는 프론트엔드에서 사용할 수 있도록 원하는 추가 데이터를 포함할 수 있습니다.

<a name="supported-drivers"></a>
#### 지원 드라이버

기본적으로 Laravel은 선택할 수 있는 세 가지 서버 측 브로드캐스팅 드라이버를 포함합니다. [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com)입니다.

> [!NOTE]
> 이벤트 브로드캐스팅을 살펴보기 전에 Laravel의 [이벤트와 리스너](/docs/13.x/events) 문서를 먼저 읽어보시기 바랍니다.

<a name="quickstart"></a>
## 빠른 시작 (Quickstart)

기본적으로 새 Laravel 애플리케이션에서는 브로드캐스팅이 활성화되어 있지 않습니다. `install:broadcasting` Artisan 명령어를 사용해 브로드캐스팅을 활성화할 수 있습니다.

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령어는 사용할 이벤트 브로드캐스팅 서비스를 묻습니다. 또한 `config/broadcasting.php` 설정 파일과, 애플리케이션의 브로드캐스트 인가 라우트 및 콜백을 등록할 수 있는 `routes/channels.php` 파일을 생성합니다.

Laravel은 기본적으로 여러 브로드캐스트 드라이버를 지원합니다. [Laravel Reverb](/docs/13.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅을 위한 `log` 드라이버가 있습니다. 또한 테스트 중 브로드캐스팅을 비활성화할 수 있는 `null` 드라이버도 포함되어 있습니다. `config/broadcasting.php` 설정 파일에는 이러한 각 드라이버에 대한 설정 예제가 포함되어 있습니다.

애플리케이션의 모든 이벤트 브로드캐스팅 설정은 `config/broadcasting.php` 설정 파일에 저장됩니다. 애플리케이션에 이 파일이 없더라도 걱정하지 않아도 됩니다. `install:broadcasting` Artisan 명령어를 실행하면 생성됩니다.

<a name="quickstart-next-steps"></a>
#### 다음 단계

이벤트 브로드캐스팅을 활성화했다면, 이제 [브로드캐스트 이벤트 정의](#defining-broadcast-events)와 [이벤트 리스닝](#listening-for-events)에 대해 더 배울 준비가 된 것입니다. Laravel의 React, Vue 또는 Svelte [스타터 키트](/docs/13.x/starter-kits)를 사용하고 있다면, Echo의 [useEcho 훅](#using-react-or-vue)을 사용해 이벤트를 리스닝할 수 있습니다.

> [!NOTE]
> 이벤트를 브로드캐스트하기 전에 먼저 [큐 워커](/docs/13.x/queues)를 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐 작업을 통해 수행되므로, 이벤트 브로드캐스트로 인해 애플리케이션의 응답 시간이 크게 영향을 받지 않습니다.

<a name="server-side-installation"></a>
## 서버 측 설치 (Server Side Installation)

Laravel의 이벤트 브로드캐스팅을 사용하려면 Laravel 애플리케이션 내부에서 몇 가지 설정을 하고, 몇 가지 패키지를 설치해야 합니다.

이벤트 브로드캐스팅은 서버 측 브로드캐스팅 드라이버가 Laravel 이벤트를 브로드캐스트하고, Laravel Echo(JavaScript 라이브러리)가 브라우저 클라이언트 안에서 이를 수신하는 방식으로 이루어집니다. 걱정하지 않아도 됩니다. 설치 과정의 각 부분을 단계별로 살펴보겠습니다.

<a name="reverb"></a>
### Reverb

Reverb를 이벤트 브로드캐스터로 사용하면서 Laravel의 브로드캐스팅 기능 지원을 빠르게 활성화하려면, `--reverb` 옵션과 함께 `install:broadcasting` Artisan 명령어를 실행하세요. 이 Artisan 명령어는 Reverb에 필요한 Composer 및 NPM 패키지를 설치하고, 애플리케이션의 `.env` 파일에 적절한 변수를 추가합니다.

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 명령어를 실행하면 [Laravel Reverb](/docs/13.x/reverb)를 설치할 것인지 묻게 됩니다. 물론 Composer 패키지 관리자를 사용해 Reverb를 수동으로 설치할 수도 있습니다.

```shell
composer require laravel/reverb
```

패키지가 설치되면 Reverb의 설치 명령어를 실행해 설정을 게시하고, Reverb에 필요한 환경 변수를 추가하며, 애플리케이션에서 이벤트 브로드캐스팅을 활성화할 수 있습니다.

```shell
php artisan reverb:install
```

자세한 Reverb 설치 및 사용 방법은 [Reverb 문서](/docs/13.x/reverb)에서 확인할 수 있습니다.

<a name="pusher-channels"></a>
### Pusher Channels

Pusher를 이벤트 브로드캐스터로 사용하면서 Laravel의 브로드캐스팅 기능 지원을 빠르게 활성화하려면, `--pusher` 옵션과 함께 `install:broadcasting` Artisan 명령어를 실행하세요. 이 Artisan 명령어는 Pusher 인증 정보를 묻고, Pusher PHP 및 JavaScript SDK를 설치하며, 애플리케이션의 `.env` 파일에 적절한 변수를 추가합니다.

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### 수동 설치

Pusher 지원을 수동으로 설치하려면 Composer 패키지 관리자를 사용해 Pusher Channels PHP SDK를 설치해야 합니다.

```shell
composer require pusher/pusher-php-server
```

다음으로 `config/broadcasting.php` 설정 파일에서 Pusher Channels 인증 정보를 설정해야 합니다. 이 파일에는 Pusher Channels 설정 예제가 이미 포함되어 있어 key, secret, application ID를 빠르게 지정할 수 있습니다. 일반적으로 Pusher Channels 인증 정보는 애플리케이션의 `.env` 파일에서 설정해야 합니다.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php` 파일의 `pusher` 설정에서는 cluster와 같이 Channels에서 지원하는 추가 `options`도 지정할 수 있습니다.

그런 다음 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 설정합니다.

```ini
BROADCAST_CONNECTION=pusher
```

마지막으로 클라이언트 측에서 브로드캐스트 이벤트를 수신할 [Laravel Echo](#client-side-installation)를 설치하고 설정할 준비가 되었습니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 문서는 Ably를 "Pusher compatibility" 모드로 사용하는 방법을 설명합니다. 하지만 Ably 팀은 Ably가 제공하는 고유한 기능을 활용할 수 있는 브로드캐스터와 Echo 클라이언트를 권장하며 유지보수하고 있습니다. Ably가 유지보수하는 드라이버 사용에 대한 자세한 내용은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 이벤트 브로드캐스터로 사용하면서 Laravel의 브로드캐스팅 기능 지원을 빠르게 활성화하려면, `--ably` 옵션과 함께 `install:broadcasting` Artisan 명령어를 실행하세요. 이 Artisan 명령어는 Ably 인증 정보를 묻고, Ably PHP 및 JavaScript SDK를 설치하며, 애플리케이션의 `.env` 파일에 적절한 변수를 추가합니다.

```shell
php artisan install:broadcasting --ably
```

**계속 진행하기 전에 Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다. 이 기능은 Ably 애플리케이션 설정 대시보드의 "Protocol Adapter Settings" 영역에서 활성화할 수 있습니다.**

<a name="ably-manual-installation"></a>
#### 수동 설치

Ably 지원을 수동으로 설치하려면 Composer 패키지 관리자를 사용해 Ably PHP SDK를 설치해야 합니다.

```shell
composer require ably/ably-php
```

다음으로 `config/broadcasting.php` 설정 파일에서 Ably 인증 정보를 설정해야 합니다. 이 파일에는 Ably 설정 예제가 이미 포함되어 있어 key를 빠르게 지정할 수 있습니다. 일반적으로 이 값은 `ABLY_KEY` [환경 변수](/docs/13.x/configuration#environment-configuration)를 통해 설정해야 합니다.

```ini
ABLY_KEY=your-ably-key
```

그런 다음 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 설정합니다.

```ini
BROADCAST_CONNECTION=ably
```

마지막으로 클라이언트 측에서 브로드캐스트 이벤트를 수신할 [Laravel Echo](#client-side-installation)를 설치하고 설정할 준비가 되었습니다.

<a name="client-side-installation"></a>
## 클라이언트 측 설치 (Client Side Installation)

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 채널을 구독하고 서버 측 브로드캐스팅 드라이버가 브로드캐스트한 이벤트를 손쉽게 리스닝할 수 있게 해주는 JavaScript 라이브러리입니다.

`install:broadcasting` Artisan 명령어를 통해 Laravel Reverb를 설치하면 Reverb와 Echo의 스캐폴딩 및 설정이 애플리케이션에 자동으로 삽입됩니다. 하지만 Laravel Echo를 수동으로 설정하고 싶다면 아래 지침을 따르면 됩니다.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

애플리케이션 프론트엔드에서 Laravel Echo를 수동으로 설정하려면, Reverb가 WebSocket 구독, 채널, 메시지에 Pusher 프로토콜을 사용하므로 먼저 `pusher-js` 패키지를 설치합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo가 설치되면 애플리케이션의 JavaScript에서 새 Echo 인스턴스를 만들 준비가 됩니다. 이를 작성하기 좋은 위치는 Laravel 프레임워크에 포함된 `resources/js/bootstrap.js` 파일의 하단입니다.

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

```js tab=Svelte
import { configureEcho } from "@laravel/echo-svelte";

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

다음으로 애플리케이션의 에셋을 컴파일해야 합니다.

```shell
npm run build
```

> [!WARNING]
> Laravel Echo `reverb` 브로드캐스터에는 laravel-echo v1.16.0 이상이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 채널을 구독하고 서버 측 브로드캐스팅 드라이버가 브로드캐스트한 이벤트를 손쉽게 리스닝할 수 있게 해주는 JavaScript 라이브러리입니다.

`install:broadcasting --pusher` Artisan 명령어를 통해 브로드캐스팅 지원을 설치하면 Pusher와 Echo의 스캐폴딩 및 설정이 애플리케이션에 자동으로 삽입됩니다. 하지만 Laravel Echo를 수동으로 설정하고 싶다면 아래 지침을 따르면 됩니다.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

애플리케이션 프론트엔드에서 Laravel Echo를 수동으로 설정하려면, WebSocket 구독, 채널, 메시지에 Pusher 프로토콜을 사용하는 `laravel-echo` 및 `pusher-js` 패키지를 먼저 설치합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo가 설치되면 애플리케이션의 `resources/js/bootstrap.js` 파일에서 새 Echo 인스턴스를 만들 준비가 됩니다.

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

```js tab=Svelte
import { configureEcho } from "@laravel/echo-svelte";

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

다음으로 애플리케이션의 `.env` 파일에서 Pusher 환경 변수에 적절한 값을 정의해야 합니다. 이러한 변수가 `.env` 파일에 아직 없다면 추가해야 합니다.

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

애플리케이션의 필요에 맞게 Echo 설정을 조정한 후에는 애플리케이션의 에셋을 컴파일할 수 있습니다.

```shell
npm run build
```

> [!NOTE]
> 애플리케이션의 JavaScript 에셋 컴파일에 대해 더 알아보려면 [Vite](/docs/13.x/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용

Echo가 사용하기를 원하는, 미리 설정된 Pusher Channels 클라이언트 인스턴스가 이미 있다면 `client` 설정 옵션을 통해 Echo에 전달할 수 있습니다.

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
> 아래 문서는 Ably를 "Pusher compatibility" 모드로 사용하는 방법을 설명합니다. 하지만 Ably 팀은 Ably가 제공하는 고유한 기능을 활용할 수 있는 브로드캐스터와 Echo 클라이언트를 권장하고 유지 관리합니다. Ably가 유지 관리하는 드라이버 사용에 대한 자세한 내용은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참조하십시오.

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스팅 드라이버가 브로드캐스트하는 이벤트를 채널에 구독하고 수신하는 작업을 간단하게 만들어 주는 JavaScript 라이브러리입니다.

`install:broadcasting --ably` Artisan 명령어로 브로드캐스팅 지원을 설치하면 Ably와 Echo의 스캐폴딩 및 설정이 애플리케이션에 자동으로 주입됩니다. 하지만 Laravel Echo를 직접 설정하려면 아래 지침을 따를 수 있습니다.

<a name="ably-client-manual-installation"></a>
#### 수동 설치

애플리케이션의 프론트엔드에서 Laravel Echo를 직접 설정하려면, 먼저 WebSocket 구독, 채널, 메시지에 Pusher 프로토콜을 사용하는 `laravel-echo`와 `pusher-js` 패키지를 설치합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

**계속하기 전에 Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다. 이 기능은 Ably 애플리케이션 설정 대시보드의 "Protocol Adapter Settings" 영역에서 활성화할 수 있습니다.**

Echo가 설치되면 애플리케이션의 `resources/js/bootstrap.js` 파일에서 새 Echo 인스턴스를 생성할 준비가 된 것입니다.

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

```js tab=Svelte
import { configureEcho } from "@laravel/echo-svelte";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

위의 Ably Echo 설정이 `VITE_ABLY_PUBLIC_KEY` 환경 변수를 참조한다는 점을 눈치챘을 수 있습니다. 이 변수의 값은 Ably 공개 키여야 합니다. 공개 키는 Ably 키에서 `:` 문자 앞에 오는 부분입니다.

필요에 맞게 Echo 설정을 조정한 후 애플리케이션의 에셋을 컴파일할 수 있습니다.

```shell
npm run dev
```

> [!NOTE]
> 애플리케이션의 JavaScript 에셋 컴파일에 대해 더 알아보려면 [Vite](/docs/13.x/vite) 문서를 참조하십시오.

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

Laravel의 이벤트 브로드캐스팅을 사용하면 WebSocket에 대한 드라이버 기반 접근 방식을 통해 서버 측 Laravel 이벤트를 클라이언트 측 JavaScript 애플리케이션으로 브로드캐스트할 수 있습니다. 현재 Laravel은 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 드라이버를 제공합니다. 이벤트는 클라이언트 측에서 [Laravel Echo](#client-side-installation) JavaScript 패키지를 사용해 쉽게 소비할 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트되며, 채널은 public 또는 private으로 지정할 수 있습니다. 애플리케이션 방문자는 인증이나 인가 없이 public 채널을 구독할 수 있습니다. 하지만 private 채널을 구독하려면 사용자가 인증되어 있어야 하며, 해당 채널을 수신할 수 있도록 인가되어야 합니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 사용

이벤트 브로드캐스팅의 각 구성 요소를 자세히 살펴보기 전에, 전자상거래 스토어를 예로 들어 높은 수준에서 개요를 살펴보겠습니다.

애플리케이션에 사용자가 주문의 배송 상태를 확인할 수 있는 페이지가 있다고 가정해 보겠습니다. 또한 애플리케이션에서 배송 상태 업데이트가 처리될 때 `OrderShipmentStatusUpdated` 이벤트가 발생한다고 가정해 보겠습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 자신의 주문 중 하나를 보고 있을 때, 상태 업데이트를 확인하기 위해 페이지를 새로고침하게 만들고 싶지는 않습니다. 대신 업데이트가 생성되는 즉시 애플리케이션으로 브로드캐스트하고 싶습니다. 따라서 `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 표시해야 합니다. 이렇게 하면 이벤트가 발생할 때 Laravel이 해당 이벤트를 브로드캐스트하도록 지시합니다.

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

`ShouldBroadcast` 인터페이스는 이벤트가 `broadcastOn` 메서드를 정의하도록 요구합니다. 이 메서드는 이벤트가 브로드캐스트될 채널을 반환하는 역할을 합니다. 생성된 이벤트 클래스에는 이 메서드의 빈 스텁이 이미 정의되어 있으므로 세부 내용만 채우면 됩니다. 주문 생성자만 상태 업데이트를 볼 수 있어야 하므로, 주문에 연결된 private 채널에서 이벤트를 브로드캐스트하겠습니다.

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

이벤트를 여러 채널에 브로드캐스트하려면 대신 `array`를 반환할 수 있습니다.

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
#### 채널 인가

사용자는 private 채널을 수신하려면 반드시 인가되어야 한다는 점을 기억하십시오. 채널 인가 규칙은 애플리케이션의 `routes/channels.php` 파일에 정의할 수 있습니다. 이 예제에서는 private `orders.1` 채널을 수신하려는 사용자가 실제로 해당 주문의 생성자인지 확인해야 합니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 개의 인수를 받습니다. 하나는 채널 이름이고, 다른 하나는 사용자가 해당 채널을 수신할 권한이 있는지 여부를 나타내는 `true` 또는 `false`를 반환하는 콜백입니다.

모든 인가 콜백은 첫 번째 인수로 현재 인증된 사용자를 받고, 그 뒤의 인수로 추가 와일드카드 매개변수를 받습니다. 이 예제에서는 채널 이름의 "ID" 부분이 와일드카드임을 나타내기 위해 `{orderId}` 플레이스홀더를 사용하고 있습니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 브로드캐스트 수신

다음으로 남은 일은 JavaScript 애플리케이션에서 이벤트를 수신하는 것입니다. [Laravel Echo](#client-side-installation)를 사용해 이를 수행할 수 있습니다. Laravel Echo의 기본 제공 React, Vue, Svelte 훅을 사용하면 쉽게 시작할 수 있으며, 기본적으로 이벤트의 모든 public 속성이 브로드캐스트 이벤트에 포함됩니다.

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

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

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
## 브로드캐스트 이벤트 정의 (Defining Broadcast Events)

특정 이벤트를 브로드캐스트해야 한다는 것을 Laravel에 알리려면 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크가 생성하는 모든 이벤트 클래스에 이미 임포트되어 있으므로, 여러분의 이벤트에 쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 하나의 메서드인 `broadcastOn`을 구현하도록 요구합니다. `broadcastOn` 메서드는 이벤트가 브로드캐스트될 채널 또는 채널 배열을 반환해야 합니다. 채널은 `Channel`, `PrivateChannel`, 또는 `PresenceChannel`의 인스턴스여야 합니다. `Channel` 인스턴스는 모든 사용자가 구독할 수 있는 public 채널을 나타내며, `PrivateChannels`와 `PresenceChannels`는 [채널 인가](#authorizing-channels)가 필요한 private 채널을 나타냅니다.

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

`ShouldBroadcast` 인터페이스를 구현한 후에는 평소처럼 [이벤트를 발생](/docs/13.x/events)시키기만 하면 됩니다. 이벤트가 발생하면 [queued job](/docs/13.x/queues)이 지정한 브로드캐스트 드라이버를 사용해 이벤트를 자동으로 브로드캐스트합니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트의 클래스 이름을 사용해 이벤트를 브로드캐스트합니다. 하지만 이벤트에 `broadcastAs` 메서드를 정의하여 브로드캐스트 이름을 사용자 지정할 수 있습니다.

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

`broadcastAs` 메서드를 사용해 브로드캐스트 이름을 사용자 지정하는 경우, 리스너를 등록할 때 앞에 `.` 문자를 붙여야 합니다. 이렇게 하면 Echo가 애플리케이션의 네임스페이스를 이벤트 앞에 추가하지 않도록 지시합니다.

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트될 때 모든 `public` 속성은 자동으로 직렬화되어 이벤트의 payload로 브로드캐스트됩니다. 따라서 JavaScript 애플리케이션에서 해당 public 데이터에 접근할 수 있습니다. 예를 들어 이벤트에 Eloquent 모델을 담고 있는 하나의 public `$user` 속성이 있다면, 이벤트의 브로드캐스트 payload는 다음과 같습니다.

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

하지만 브로드캐스트 payload를 더 세밀하게 제어하고 싶다면 이벤트에 `broadcastWith` 메서드를 추가할 수 있습니다. 이 메서드는 이벤트 payload로 브로드캐스트하려는 데이터 배열을 반환해야 합니다.

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

기본적으로 각 브로드캐스트 이벤트는 `queue.php` 설정 파일에 지정된 기본 큐 연결의 기본 큐에 배치됩니다. 이벤트 클래스에 `Connection` 및 `Queue` 속성을 사용하여 브로드캐스터가 사용하는 큐 연결과 이름을 사용자 지정할 수 있습니다.

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

또는 이벤트에 `broadcastQueue` 메서드를 정의하여 큐 이름을 사용자 지정할 수 있습니다.

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

기본 큐 드라이버 대신 `sync` 큐를 사용해 이벤트를 브로드캐스트하려면 `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현할 수 있습니다.

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

때로는 특정 조건이 참일 때만 이벤트를 브로드캐스트하고 싶을 수 있습니다. 이벤트 클래스에 `broadcastWhen` 메서드를 추가하여 이러한 조건을 정의할 수 있습니다.

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

브로드캐스트 이벤트가 데이터베이스 트랜잭션 안에서 디스패치되면, 데이터베이스 트랜잭션이 커밋되기 전에 큐가 해당 이벤트를 처리할 수 있습니다. 이런 경우 데이터베이스 트랜잭션 중에 모델이나 데이터베이스 레코드에 적용한 업데이트가 아직 데이터베이스에 반영되지 않았을 수 있습니다. 또한 트랜잭션 안에서 생성된 모델이나 데이터베이스 레코드가 데이터베이스에 아직 존재하지 않을 수도 있습니다. 이벤트가 이러한 모델에 의존한다면, 이벤트를 브로드캐스트하는 job이 처리될 때 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정 옵션이 `false`로 설정되어 있더라도, 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하여 특정 브로드캐스트 이벤트가 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 후 디스패치되어야 함을 나타낼 수 있습니다.

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
> 이러한 문제를 우회하는 방법을 더 알아보려면 [큐에 들어간 작업과 데이터베이스 트랜잭션](/docs/13.x/queues#jobs-and-database-transactions) 관련 문서를 확인하세요.

<a name="authorizing-channels"></a>
## 채널 인가 (Authorizing Channels)

비공개 채널은 현재 인증된 사용자가 실제로 해당 채널을 수신할 수 있는지 인가해야 합니다. 이는 채널 이름과 함께 Laravel 애플리케이션에 HTTP 요청을 보내고, 애플리케이션이 사용자가 해당 채널을 수신할 수 있는지 판단하도록 하여 처리합니다. [Laravel Echo](#client-side-installation)를 사용하는 경우, 비공개 채널 구독을 인가하기 위한 HTTP 요청은 자동으로 전송됩니다.

브로드캐스팅이 설치되면 Laravel은 인가 요청을 처리하기 위해 `/broadcasting/auth` 라우트를 자동으로 등록하려고 시도합니다. Laravel이 이러한 라우트를 자동으로 등록하지 못하는 경우, 애플리케이션의 `/bootstrap/app.php` 파일에서 수동으로 등록할 수 있습니다.

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    channels: __DIR__.'/../routes/channels.php',
    health: '/up',
)
```

<a name="defining-authorization-callbacks"></a>
### 인가 콜백 정의

다음으로, 현재 인증된 사용자가 특정 채널을 수신할 수 있는지 실제로 판단하는 로직을 정의해야 합니다. 이 작업은 `install:broadcasting` Artisan 명령어로 생성된 `routes/channels.php` 파일에서 수행합니다. 이 파일에서는 `Broadcast::channel` 메서드를 사용하여 채널 인가 콜백을 등록할 수 있습니다.

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 두 개의 인수를 받습니다. 하나는 채널 이름이고, 다른 하나는 사용자가 해당 채널을 수신할 수 있도록 인가되었는지를 나타내는 `true` 또는 `false`를 반환하는 콜백입니다.

모든 인가 콜백은 첫 번째 인수로 현재 인증된 사용자를 받고, 그 뒤의 인수로 추가 와일드카드 매개변수를 받습니다. 이 예제에서는 채널 이름의 "ID" 부분이 와일드카드임을 나타내기 위해 `{orderId}` 플레이스홀더를 사용합니다.

애플리케이션의 브로드캐스트 인가 콜백 목록은 `channel:list` Artisan 명령어로 확인할 수 있습니다.

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 인가 콜백 모델 바인딩

HTTP 라우트와 마찬가지로, 채널 라우트도 암묵적 및 명시적 [라우트 모델 바인딩](/docs/13.x/routing#route-model-binding)을 활용할 수 있습니다. 예를 들어 문자열이나 숫자 형태의 주문 ID를 받는 대신, 실제 `Order` 모델 인스턴스를 요청할 수 있습니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과 달리, 채널 모델 바인딩은 자동 [암묵적 모델 바인딩 범위 지정](/docs/13.x/routing#implicit-model-binding-scoping)을 지원하지 않습니다. 하지만 대부분의 채널은 단일 모델의 고유한 기본 키를 기준으로 범위를 지정할 수 있으므로, 실제로 문제가 되는 경우는 드뭅니다.

<a name="authorization-callback-authentication"></a>
#### 인가 콜백 인증

비공개 및 프레즌스 브로드캐스트 채널은 애플리케이션의 기본 인증 가드를 통해 현재 사용자를 인증합니다. 사용자가 인증되지 않은 경우 채널 인가는 자동으로 거부되며, 인가 콜백은 실행되지 않습니다. 하지만 필요한 경우 들어오는 요청을 인증해야 하는 여러 개의 커스텀 가드를 지정할 수 있습니다.

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의

애플리케이션이 여러 채널을 사용한다면 `routes/channels.php` 파일이 커질 수 있습니다. 따라서 클로저를 사용하여 채널을 인가하는 대신 채널 클래스를 사용할 수 있습니다. 채널 클래스를 생성하려면 `make:channel` Artisan 명령어를 사용하세요. 이 명령어는 `App/Broadcasting` 디렉터리에 새 채널 클래스를 생성합니다.

```shell
php artisan make:channel OrderChannel
```

다음으로, `routes/channels.php` 파일에 채널을 등록합니다.

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

마지막으로, 채널 클래스의 `join` 메서드에 채널 인가 로직을 배치할 수 있습니다. 이 `join` 메서드에는 일반적으로 채널 인가 클로저에 작성했을 로직과 동일한 로직이 들어갑니다. 채널 모델 바인딩도 활용할 수 있습니다.

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
> Laravel의 다른 많은 클래스와 마찬가지로, 채널 클래스도 [서비스 컨테이너](/docs/13.x/container)에 의해 자동으로 resolve됩니다. 따라서 채널에 필요한 의존성을 생성자에서 타입 힌트로 지정할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅 (Broadcasting Events)

이벤트를 정의하고 `ShouldBroadcast` 인터페이스를 지정했다면, 이제 이벤트의 dispatch 메서드를 사용해 이벤트를 발생시키기만 하면 됩니다. 이벤트 디스패처는 해당 이벤트에 `ShouldBroadcast` 인터페이스가 지정되어 있음을 감지하고, 브로드캐스팅을 위해 이벤트를 큐에 넣습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### 다른 사용자에게만

이벤트 브로드캐스팅을 사용하는 애플리케이션을 만들다 보면, 현재 사용자를 제외하고 특정 채널의 모든 구독자에게 이벤트를 브로드캐스트해야 할 때가 있습니다. 이는 `broadcast` 헬퍼와 `toOthers` 메서드를 사용하여 처리할 수 있습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

`toOthers` 메서드를 언제 사용하면 좋은지 더 잘 이해하기 위해, 사용자가 작업 이름을 입력하여 새 작업을 만들 수 있는 작업 목록 애플리케이션을 생각해 보겠습니다. 작업을 만들기 위해 애플리케이션은 `/task` URL로 요청을 보낼 수 있으며, 이 요청은 작업 생성 사실을 브로드캐스트하고 새 작업의 JSON 표현을 반환합니다. JavaScript 애플리케이션이 엔드포인트의 응답을 받으면 다음과 같이 새 작업을 작업 목록에 직접 추가할 수 있습니다.

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

하지만 작업 생성 사실도 함께 브로드캐스트한다는 점을 기억해야 합니다. JavaScript 애플리케이션이 작업 목록에 작업을 추가하기 위해 이 이벤트도 수신하고 있다면, 목록에 작업이 중복으로 들어갑니다. 하나는 엔드포인트에서 온 것이고, 다른 하나는 브로드캐스트에서 온 것입니다. 이 문제는 `toOthers` 메서드를 사용하여 브로드캐스터에게 현재 사용자에게는 이벤트를 브로드캐스트하지 말라고 지시함으로써 해결할 수 있습니다.

> [!WARNING]
> `toOthers` 메서드를 호출하려면 이벤트에서 `Illuminate\Broadcasting\InteractsWithSockets` trait을 사용해야 합니다.

<a name="only-to-others-configuration"></a>
#### 설정

Laravel Echo 인스턴스를 초기화하면 연결에 소켓 ID가 할당됩니다. JavaScript 애플리케이션에서 HTTP 요청을 보내기 위해 전역 [Axios](https://github.com/axios/axios) 인스턴스를 사용하고 있다면, 소켓 ID는 모든 발신 요청에 `X-Socket-ID` 헤더로 자동 첨부됩니다. 그런 다음 `toOthers` 메서드를 호출하면 Laravel은 헤더에서 소켓 ID를 추출하고, 해당 소켓 ID를 가진 연결에는 브로드캐스트하지 않도록 브로드캐스터에 지시합니다.

전역 Axios 인스턴스를 사용하지 않는 경우, 모든 발신 요청에 `X-Socket-ID` 헤더를 보내도록 JavaScript 애플리케이션을 수동으로 설정해야 합니다. 소켓 ID는 `Echo.socketId` 메서드를 사용하여 가져올 수 있습니다.

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 연결 커스터마이징

애플리케이션이 여러 브로드캐스트 연결과 상호작용하고 있으며 기본 브로드캐스터가 아닌 다른 브로드캐스터를 사용해 이벤트를 브로드캐스트하려는 경우, `via` 메서드를 사용하여 이벤트를 보낼 연결을 지정할 수 있습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는 이벤트의 생성자 안에서 `broadcastVia` 메서드를 호출하여 이벤트의 브로드캐스트 연결을 지정할 수도 있습니다. 다만 그렇게 하기 전에, 이벤트 클래스가 `InteractsWithBroadcasting` trait을 사용하는지 확인해야 합니다.

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

때로는 전용 이벤트 클래스를 만들지 않고 애플리케이션의 프런트엔드에 간단한 이벤트를 브로드캐스트하고 싶을 수 있습니다. 이를 위해 `Broadcast` 파사드는 "익명 이벤트"를 브로드캐스트할 수 있도록 해줍니다.

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 예제는 다음 이벤트를 브로드캐스트합니다.

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

`as` 및 `with` 메서드를 사용하면 이벤트 이름과 데이터를 커스터마이징할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

위 예제는 다음과 같은 이벤트를 브로드캐스트합니다.

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

비공개 또는 프레즌스 채널에서 익명 이벤트를 브로드캐스트하려면 `private` 및 `presence` 메서드를 사용할 수 있습니다.

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send` 메서드를 사용하여 익명 이벤트를 브로드캐스트하면, 이벤트가 처리를 위해 애플리케이션의 [큐](/docs/13.x/queues)로 디스패치됩니다. 하지만 이벤트를 즉시 브로드캐스트하고 싶다면 `sendNow` 메서드를 사용할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 인증된 사용자를 제외한 모든 채널 구독자에게 이벤트를 브로드캐스트하려면 `toOthers` 메서드를 호출하면 됩니다.

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
### 브로드캐스트 복구

애플리케이션의 큐 서버를 사용할 수 없거나 Laravel이 이벤트를 브로드캐스트하는 중 오류를 만나면, 보통 최종 사용자가 애플리케이션 오류를 보게 만드는 예외가 발생합니다. 이벤트 브로드캐스팅은 애플리케이션의 핵심 기능을 보조하는 경우가 많기 때문에, 이벤트에 `ShouldRescue` 인터페이스를 구현하여 이러한 예외가 사용자 경험을 방해하지 않도록 할 수 있습니다.

`ShouldRescue` 인터페이스를 구현한 이벤트는 브로드캐스트를 시도하는 동안 Laravel의 [rescue 헬퍼 함수](/docs/13.x/helpers#method-rescue)를 자동으로 사용합니다. 이 헬퍼는 모든 예외를 잡고, 로깅을 위해 애플리케이션의 예외 핸들러에 보고하며, 사용자의 작업 흐름을 중단하지 않고 애플리케이션이 정상적으로 계속 실행되도록 합니다.

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
### 이벤트 수신

[Laravel Echo를 설치하고 인스턴스를 생성](#client-side-installation)했다면, 이제 Laravel 애플리케이션에서 브로드캐스트되는 이벤트를 수신할 준비가 된 것입니다. 먼저 `channel` 메서드를 사용하여 채널 인스턴스를 가져온 다음, `listen` 메서드를 호출하여 지정한 이벤트를 수신합니다.

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널의 이벤트를 수신하려면 대신 `private` 메서드를 사용하세요. 하나의 채널에서 여러 이벤트를 수신하려면 `listen` 메서드 호출을 계속 체이닝할 수 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 수신 중지

[채널을 떠나지 않고](#leaving-a-channel) 특정 이벤트 수신만 중지하려면 `stopListening` 메서드를 사용할 수 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### 채널 떠나기

채널을 떠나려면 Echo 인스턴스에서 `leaveChannel` 메서드를 호출하면 됩니다.

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널과 그에 연결된 비공개 및 프레즌스 채널까지 함께 떠나려면 `leave` 메서드를 호출하면 됩니다.

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
### 네임스페이스

위 예제에서 이벤트 클래스에 전체 `App\Events` 네임스페이스를 지정하지 않았다는 점을 눈치챘을 수 있습니다. 이는 Echo가 이벤트가 `App\Events` 네임스페이스에 있다고 자동으로 가정하기 때문입니다. 하지만 Echo 인스턴스를 생성할 때 `namespace` 설정 옵션을 전달하여 루트 네임스페이스를 설정할 수 있습니다.

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

또는 Echo를 사용하여 이벤트를 구독할 때 이벤트 클래스 앞에 `.`를 붙일 수 있습니다. 이렇게 하면 항상 완전한 클래스명을 지정할 수 있습니다.

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
### React, Vue 또는 Svelte 사용

Laravel Echo에는 이벤트 수신을 쉽게 해주는 React, Vue 및 Svelte 훅이 포함되어 있습니다. 시작하려면 비공개 이벤트를 수신하는 데 사용되는 `useEcho` 훅을 호출하세요. `useEcho` 훅은 이를 사용하는 컴포넌트가 언마운트될 때 자동으로 채널을 떠납니다.

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

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

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

브로드캐스트 이벤트 페이로드 데이터의 형태도 지정할 수 있으며, 이를 통해 더 높은 타입 안정성과 편집 편의성을 얻을 수 있습니다.

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

`useEcho` 훅은 이를 사용하는 컴포넌트가 언마운트될 때 자동으로 채널에서 나갑니다. 하지만 필요한 경우 반환된 함수를 사용해 프로그래밍 방식으로 채널 수신을 수동으로 중지하거나 다시 시작할 수 있습니다.

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

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

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
#### 공개 채널에 연결하기

공개 채널에 연결하려면 `useEchoPublic` 훅을 사용할 수 있습니다.

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

```svelte tab=Svelte
<script>
import { useEchoPublic } from "@laravel/echo-svelte";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connecting-to-presence-channels"></a>
#### 프레즌스 채널에 연결하기

프레즌스 채널에 연결하려면 `useEchoPresence` 훅을 사용할 수 있습니다.

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

```svelte tab=Svelte
<script>
import { useEchoPresence } from "@laravel/echo-svelte";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connection-status"></a>
#### 연결 상태

`useConnectionStatus` 훅을 사용하면 현재 WebSocket 연결 상태를 가져올 수 있습니다. 이 훅은 연결 상태가 변경될 때 자동으로 업데이트되는 반응형 상태를 제공합니다.

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

```svelte tab=Svelte
<script>
import { useConnectionStatus } from "@laravel/echo-svelte";

const status = useConnectionStatus();
</script>

<div>Connection: {status()}</div>
```

가능한 상태 값은 다음과 같습니다.

<div class="content-list" markdown="1">

- `connected` - WebSocket 서버에 성공적으로 연결되었습니다.
- `connecting` - 초기 연결 시도가 진행 중입니다.
- `reconnecting` - 연결이 끊어진 후 다시 연결을 시도하는 중입니다.
- `disconnected` - 연결되어 있지 않으며 다시 연결을 시도하고 있지도 않습니다.
- `failed` - 연결에 실패했으며 다시 시도하지 않습니다.

</div>

<a name="presence-channels"></a>
## 프레즌스 채널 (Presence Channels)

프레즌스 채널은 비공개 채널의 보안 위에, 해당 채널을 구독 중인 사용자가 누구인지 알 수 있는 추가 기능을 제공합니다. 이를 통해 다른 사용자가 같은 페이지를 보고 있을 때 알림을 표시하거나 채팅방에 있는 사용자를 나열하는 등 강력한 협업형 애플리케이션 기능을 쉽게 만들 수 있습니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 인가하기

모든 프레즌스 채널은 비공개 채널이기도 합니다. 따라서 사용자는 해당 채널에 접근하도록 [인가되어야 합니다](#authorizing-channels). 하지만 프레즌스 채널의 인가 콜백을 정의할 때는 사용자가 채널에 참여할 수 있더라도 `true`를 반환하지 않습니다. 대신 사용자에 대한 데이터 배열을 반환해야 합니다.

인가 콜백이 반환한 데이터는 JavaScript 애플리케이션의 프레즌스 채널 이벤트 리스너에서 사용할 수 있게 됩니다. 사용자가 프레즌스 채널에 참여할 권한이 없다면 `false` 또는 `null`을 반환해야 합니다.

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레즌스 채널 참여하기

프레즌스 채널에 참여하려면 Echo의 `join` 메서드를 사용할 수 있습니다. `join` 메서드는 `PresenceChannel` 구현체를 반환하며, 이 구현체는 `listen` 메서드를 제공하는 것과 함께 `here`, `joining`, `leaving` 이벤트를 구독할 수 있게 해 줍니다.

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

`here` 콜백은 채널 참여가 성공적으로 완료되면 즉시 실행되며, 현재 채널을 구독 중인 다른 모든 사용자의 정보가 담긴 배열을 받습니다. `joining` 메서드는 새 사용자가 채널에 참여할 때 실행되고, `leaving` 메서드는 사용자가 채널을 떠날 때 실행됩니다. `error` 메서드는 인증 엔드포인트가 200이 아닌 HTTP 상태 코드를 반환하거나 반환된 JSON을 파싱하는 데 문제가 있을 때 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널로 브로드캐스트하기

프레즌스 채널도 공개 채널이나 비공개 채널처럼 이벤트를 받을 수 있습니다. 채팅방 예시를 사용해 보면, 방의 프레즌스 채널로 `NewMessage` 이벤트를 브로드캐스트하고 싶을 수 있습니다. 이렇게 하려면 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel` 인스턴스를 반환합니다.

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

다른 이벤트와 마찬가지로 `broadcast` 헬퍼와 `toOthers` 메서드를 사용하여 현재 사용자가 브로드캐스트를 받지 않도록 제외할 수 있습니다.

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

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
## 모델 브로드캐스팅 (Model Broadcasting)

> [!WARNING]
> 모델 브로드캐스팅에 대한 다음 문서를 읽기 전에, Laravel의 모델 브로드캐스팅 서비스에 대한 일반적인 개념과 브로드캐스트 이벤트를 수동으로 만들고 수신하는 방법을 먼저 익히는 것을 권장합니다.

애플리케이션의 [Eloquent 모델](/docs/13.x/eloquent)이 생성, 수정, 삭제될 때 이벤트를 브로드캐스트하는 것은 흔한 일입니다. 물론 이는 [Eloquent 모델 상태 변경에 대한 사용자 정의 이벤트를 정의](/docs/13.x/eloquent#events)하고 해당 이벤트에 `ShouldBroadcast` 인터페이스를 표시하여 쉽게 구현할 수 있습니다.

하지만 애플리케이션에서 이러한 이벤트를 다른 용도로 사용하지 않는다면, 오직 브로드캐스트만을 위해 이벤트 클래스를 만드는 일은 번거로울 수 있습니다. 이를 해결하기 위해 Laravel은 Eloquent 모델이 자신의 상태 변경을 자동으로 브로드캐스트하도록 지정할 수 있게 해 줍니다.

시작하려면 Eloquent 모델에서 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 사용해야 합니다. 또한 모델은 모델의 이벤트가 브로드캐스트되어야 할 채널 배열을 반환하는 `broadcastOn` 메서드를 정의해야 합니다.

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

모델에 이 트레이트를 포함하고 브로드캐스트 채널을 정의하면, 모델 인스턴스가 생성, 수정, 삭제, 휴지통 이동, 복원될 때 자동으로 이벤트 브로드캐스트를 시작합니다.

또한 `broadcastOn` 메서드가 문자열 `$event` 인수를 받는다는 점을 보았을 것입니다. 이 인수에는 모델에서 발생한 이벤트 유형이 들어 있으며, 값은 `created`, `updated`, `deleted`, `trashed`, `restored` 중 하나입니다. 이 변수의 값을 확인하여 특정 이벤트에 대해 모델이 어떤 채널로 브로드캐스트해야 하는지, 또는 브로드캐스트하지 않아야 하는지를 결정할 수 있습니다.

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
#### 모델 브로드캐스팅 이벤트 생성 커스터마이징

때때로 Laravel이 내부 모델 브로드캐스팅 이벤트를 생성하는 방식을 커스터마이징하고 싶을 수 있습니다. Eloquent 모델에 `newBroadcastableEvent` 메서드를 정의하면 이를 구현할 수 있습니다. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다.

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

위 모델 예시에서 `broadcastOn` 메서드가 `Channel` 인스턴스를 반환하지 않았다는 점을 보았을 것입니다. 대신 Eloquent 모델이 직접 반환되었습니다. 모델의 `broadcastOn` 메서드가 Eloquent 모델 인스턴스를 반환하거나, 메서드가 반환한 배열에 Eloquent 모델 인스턴스가 포함되어 있다면, Laravel은 모델의 클래스명과 기본 키 식별자를 채널 이름으로 사용하여 해당 모델에 대한 비공개 채널 인스턴스를 자동으로 생성합니다.
따라서 `id`가 `1`인 `App\Models\User` 모델은 이름이 `App.Models.User.1`인 `Illuminate\Broadcasting\PrivateChannel` 인스턴스로 변환됩니다. 물론 모델의 `broadcastOn` 메서드에서 Eloquent 모델 인스턴스를 반환하는 것 외에도, 모델의 채널 이름을 완전히 제어하기 위해 완전한 `Channel` 인스턴스를 반환할 수도 있습니다.

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

모델의 `broadcastOn` 메서드에서 채널 인스턴스를 명시적으로 반환하려는 경우, 채널 생성자에 Eloquent 모델 인스턴스를 전달할 수 있습니다. 이렇게 하면 Laravel은 앞에서 설명한 모델 채널 규칙을 사용하여 Eloquent 모델을 채널 이름 문자열로 변환합니다.

```php
return [new Channel($this->user)];
```

모델의 채널 이름을 확인해야 하는 경우, 어떤 모델 인스턴스에서든 `broadcastChannel` 메서드를 호출할 수 있습니다. 예를 들어, 이 메서드는 `id`가 `1`인 `App\Models\User` 모델에 대해 문자열 `App.Models.User.1`을 반환합니다.

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규칙

모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉터리에 있는 "실제" 이벤트와 연결되지 않으므로, 규칙에 따라 이름과 페이로드가 지정됩니다. Laravel의 규칙은 모델의 클래스 이름(네임스페이스 제외)과 브로드캐스트를 트리거한 모델 이벤트 이름을 사용하여 이벤트를 브로드캐스트하는 것입니다.

예를 들어 `App\Models\Post` 모델이 업데이트되면, 다음 페이로드와 함께 `PostUpdated`라는 이벤트가 클라이언트 측 애플리케이션으로 브로드캐스트됩니다.

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

`App\Models\User` 모델이 삭제되면 `UserDeleted`라는 이름의 이벤트가 브로드캐스트됩니다.

원한다면 모델에 `broadcastAs` 및 `broadcastWith` 메서드를 추가하여 사용자 정의 브로드캐스트 이름과 페이로드를 정의할 수 있습니다. 이 메서드들은 현재 발생 중인 모델 이벤트 / 작업의 이름을 전달받으므로, 각 모델 작업에 맞게 이벤트 이름과 페이로드를 사용자 정의할 수 있습니다. `broadcastAs` 메서드가 `null`을 반환하면, Laravel은 이벤트를 브로드캐스트할 때 앞에서 설명한 모델 브로드캐스팅 이벤트 이름 규칙을 사용합니다.

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
### 모델 브로드캐스트 수신하기

모델에 `BroadcastsEvents` 트레이트를 추가하고 모델의 `broadcastOn` 메서드를 정의했다면, 이제 클라이언트 측 애플리케이션에서 브로드캐스트된 모델 이벤트를 수신할 준비가 된 것입니다. 시작하기 전에 [이벤트 수신하기](#listening-for-events)에 대한 전체 문서를 참고하면 좋습니다.

먼저 `private` 메서드를 사용해 채널 인스턴스를 가져온 다음, `listen` 메서드를 호출하여 지정한 이벤트를 수신합니다. 일반적으로 `private` 메서드에 전달하는 채널 이름은 Laravel의 [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)을 따라야 합니다.

채널 인스턴스를 얻은 뒤에는 `listen` 메서드를 사용해 특정 이벤트를 수신할 수 있습니다. 모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉터리에 있는 "실제" 이벤트와 연결되지 않으므로, 특정 네임스페이스에 속하지 않음을 나타내기 위해 [이벤트 이름](#model-broadcasting-event-conventions) 앞에 `.`를 붙여야 합니다. 각 모델 브로드캐스트 이벤트에는 모델에서 브로드캐스트 가능한 모든 속성을 담고 있는 `model` 속성이 있습니다.

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
#### React, Vue 또는 Svelte 사용하기

React, Vue 또는 Svelte를 사용한다면 Laravel Echo에 포함된 `useEchoModel` 훅을 사용해 모델 브로드캐스트를 쉽게 수신할 수 있습니다.

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

```svelte tab=Svelte
<script>
import { useEchoModel } from "@laravel/echo-svelte";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```

모델 이벤트 페이로드 데이터의 형태를 지정하여 더 높은 타입 안정성과 편리한 편집 환경을 제공할 수도 있습니다.

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
> [Pusher Channels](https://pusher.com/channels)를 사용할 때 클라이언트 이벤트를 보내려면 [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings" 섹션에서 "Client Events" 옵션을 활성화해야 합니다.

때로는 Laravel 애플리케이션을 전혀 거치지 않고 연결된 다른 클라이언트에 이벤트를 브로드캐스트하고 싶을 수 있습니다. 예를 들어 특정 화면에서 다른 사용자가 메시지를 입력하고 있음을 애플리케이션 사용자에게 알리는 "입력 중" 알림 같은 기능에 특히 유용합니다.

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

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

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

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

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

이벤트 브로드캐스팅과 [알림](/docs/13.x/notifications)을 함께 사용하면, JavaScript 애플리케이션은 페이지를 새로고침하지 않아도 새 알림이 발생하는 즉시 받을 수 있습니다. 시작하기 전에 [브로드캐스트 알림 채널](/docs/13.x/notifications#broadcast-notifications) 사용에 대한 문서를 반드시 읽어보시기 바랍니다.

브로드캐스트 채널을 사용하도록 알림을 설정했다면, Echo의 `notification` 메서드를 사용해 브로드캐스트 이벤트를 수신할 수 있습니다. 채널 이름은 알림을 받는 엔티티의 클래스 이름과 일치해야 한다는 점을 기억하세요.

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

```svelte tab=Svelte
<script>
import { useEchoModel } from "@laravel/echo-svelte";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

이 예제에서는 `broadcast` 채널을 통해 `App\Models\User` 인스턴스로 전송된 모든 알림이 콜백에서 수신됩니다. `App.Models.User.{id}` 채널에 대한 채널 인가 콜백은 애플리케이션의 `routes/channels.php` 파일에 포함되어 있습니다.

<a name="stop-listening-for-notifications"></a>
#### 알림 수신 중지하기

[채널을 떠나지](#leaving-a-channel) 않고 알림 수신을 중지하려면 `stopListeningForNotification` 메서드를 사용할 수 있습니다.

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
