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
    - [예제 애플리케이션 활용](#using-example-application)
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
    - [Others만을 대상으로 브로드캐스팅](#only-to-others)
    - [커넥션 커스터마이징](#customizing-the-connection)
    - [익명 이벤트](#anonymous-events)
    - [브로드캐스팅 예외 처리](#rescuing-broadcasts)
- [브로드캐스트 수신](#receiving-broadcasts)
    - [이벤트 리스닝](#listening-for-events)
    - [채널 나가기](#leaving-a-channel)
    - [네임스페이스](#namespaces)
    - [React 또는 Vue 사용하기](#using-react-or-vue)
- [프레즌스 채널(Presence Channels)](#presence-channels)
    - [프레즌스 채널 인가](#authorizing-presence-channels)
    - [프레즌스 채널 참여](#joining-presence-channels)
    - [프레즌스 채널에 브로드캐스트](#broadcasting-to-presence-channels)
- [모델 브로드캐스팅](#model-broadcasting)
    - [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)
    - [모델 브로드캐스트 리스닝](#listening-for-model-broadcasts)
- [클라이언트 이벤트](#client-events)
- [알림(Notifications)](#notifications)

<a name="introduction"></a>
## 소개 (Introduction)

현대적인 웹 애플리케이션에서는 WebSocket을 활용하여 실시간으로 갱신되는 사용자 인터페이스를 구현하는 경우가 많습니다. 서버의 일부 데이터가 변경되면, 일반적으로 WebSocket 커넥션을 통해 메시지가 클라이언트로 전송되어 처리됩니다. WebSocket은 주기적으로 애플리케이션 서버에 변경된 데이터를 조회하는 방식보다 훨씬 효율적인 대안입니다.

예를 들어, 사용자의 데이터를 CSV 파일로 내보내고 이메일로 발송하는 기능이 있다고 가정합시다. CSV 파일 생성이 수 분 정도 걸릴 수 있으므로, [큐 작업](/docs/12.x/queues) 내에서 CSV 파일을 생성하고 메일링하도록 선택할 수 있습니다. 그리고 CSV가 생성되어 사용자가 메일을 받은 시점에, `App\Events\UserDataExported` 이벤트를 브로드캐스트하여 자바스크립트에서 감지하도록 할 수 있습니다. 이 이벤트를 받은 후 사용자는 페이지를 새로고침하지 않아도 CSV가 발송되었음을 알 수 있습니다.

이러한 실시간 기능 개발을 돕기 위해, Laravel은 서버 사이드 [이벤트](/docs/12.x/events)를 WebSocket 커넥션을 통해 쉽게 "브로드캐스트"할 수 있도록 지원합니다. Laravel 이벤트를 브로드캐스트하면, 동일한 이벤트 이름과 데이터를 서버/클라이언트 양쪽 애플리케이션에서 공유할 수 있습니다.

브로드캐스팅의 핵심 개념은 간단합니다. 클라이언트는 프론트엔드에서 특정 이름의 채널에 연결하고, 서버의 Laravel 애플리케이션은 백엔드에서 이 채널로 이벤트를 브로드캐스트합니다. 이 이벤트에는 프론트엔드에서 사용하고 싶은 데이터를 자유롭게 포함시킬 수 있습니다.

<a name="supported-drivers"></a>
#### 지원되는 드라이버

Laravel에는 기본적으로 서버 사이드 브로드캐스팅 드라이버가 세 가지 포함되어 있습니다: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com).

> [!NOTE]
> 이벤트 브로드캐스팅을 시작하기 전에, 반드시 [이벤트 & 리스너](/docs/12.x/events) 문서를 먼저 읽어보시기 바랍니다.

<a name="quickstart"></a>
## 빠른 시작 (Quickstart)

기본적으로, 새로 생성한 Laravel 애플리케이션에서는 브로드캐스팅이 활성화되어 있지 않습니다. `install:broadcasting` Artisan 명령어로 브로드캐스팅을 활성화할 수 있습니다.

```shell
php artisan install:broadcasting
```

`install:broadcasting` 명령은 어떤 이벤트 브로드캐스트 서비스를 사용할 것인지 물어봅니다. 또한, `config/broadcasting.php` 설정 파일과 `routes/channels.php` 파일을 생성합니다. 이곳에서 애플리케이션의 브로드캐스트 인가 라우트 및 콜백을 등록할 수 있습니다.

Laravel은 기본적으로 여러 브로드캐스트 드라이버를 지원합니다: [Laravel Reverb](/docs/12.x/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), 그리고 로컬 개발 및 디버깅을 위한 `log` 드라이버가 있습니다. 또한, 테스트 중 브로드캐스팅을 비활성화할 수 있도록 `null` 드라이버도 포함되어 있습니다. 각 드라이버의 설정 예시는 `config/broadcasting.php` 파일에 포함되어 있습니다.

애플리케이션의 모든 브로드캐스팅 관련 설정은 `config/broadcasting.php` 파일에서 관리됩니다. 이 파일이 존재하지 않더라도, `install:broadcasting` 명령을 실행하면 자동으로 생성됩니다.

<a name="quickstart-next-steps"></a>
#### 다음 단계

이벤트 브로드캐스팅을 활성화했다면, 이제 [브로드캐스트 이벤트 정의](#defining-broadcast-events)와 [이벤트 리스닝](#listening-for-events)에 대해 학습할 준비가 완료된 것입니다. Laravel의 React 또는 Vue [스타터 키트](/docs/12.x/starter-kits)를 사용하는 경우, Echo의 [useEcho hook](#using-react-or-vue)으로 손쉽게 이벤트를 수신할 수 있습니다.

> [!NOTE]
> 이벤트를 브로드캐스트하기 전에 반드시 [큐 워커](/docs/12.x/queues)를 먼저 설정하고 실행해야 합니다. 모든 이벤트 브로드캐스팅은 큐 작업을 통해 이루어지므로, 이벤트 브로드캐스팅에 의해 애플리케이션의 응답 시간이 지연되는 일을 방지할 수 있습니다.

<a name="server-side-installation"></a>
## 서버 사이드 설치 (Server Side Installation)

Laravel의 이벤트 브로드캐스팅을 시작하려면, Laravel 애플리케이션 내에서 일부 설정을 진행하고 몇 가지 패키지를 설치해야 합니다.

이벤트 브로드캐스팅은 서버 사이드 브로드캐스트 드라이버가 Laravel 이벤트를 브라우저 내에서 Laravel Echo(자바스크립트 라이브러리)로 전달하는 방식으로 동작합니다. 설치 과정을 단계별로 안내하니 부담 없이 따라오시면 됩니다.

<a name="reverb"></a>
### Reverb

Reverb를 이벤트 브로드캐스트 드라이버로 사용하여 Laravel의 브로드캐스트 기능을 빠르게 활성화하려면, `install:broadcasting` 아티즌 명령에 `--reverb` 옵션을 추가해 실행하세요. 이 명령은 Reverb에 필요한 Composer 및 NPM 패키지를 설치하고, 애플리케이션의 `.env` 파일에 적절한 환경 변수를 추가합니다.

```shell
php artisan install:broadcasting --reverb
```

<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 명령을 실행하면 [Laravel Reverb](/docs/12.x/reverb) 설치를 권장하는 메시지가 나타납니다. 물론, Composer 패키지 매니저를 사용해 Reverb를 수동으로 설치할 수도 있습니다.

```shell
composer require laravel/reverb
```

패키지 설치 후, Reverb의 설치 명령을 실행하면 관련 설정이 퍼블리시되고 환경 변수 추가, 이벤트 브로드캐스팅 활성화 등이 자동으로 진행됩니다.

```shell
php artisan reverb:install
```

자세한 Reverb 설치 및 사용 방법은 [Reverb 공식 문서](/docs/12.x/reverb)에서 확인할 수 있습니다.

<a name="pusher-channels"></a>
### Pusher Channels

Pusher를 이벤트 브로드캐스트 드라이버로 사용할 경우, `install:broadcasting` 아티즌 명령에 `--pusher` 옵션을 추가해 실행합니다. 이 명령은 Pusher 인증 정보를 입력받고, Pusher PHP 및 자바스크립트 SDK를 설치하며, 애플리케이션의 `.env` 파일에 필요한 변수를 추가합니다.

```shell
php artisan install:broadcasting --pusher
```

<a name="pusher-manual-installation"></a>
#### 수동 설치

Pusher 지원을 수동으로 설치하려면 Composer 패키지 매니저를 사용해 Pusher Channels PHP SDK를 설치해야 합니다.

```shell
composer require pusher/pusher-php-server
```

다음으로, `config/broadcasting.php` 설정 파일에 Pusher Channels 인증 정보를 입력해야 합니다. 이 파일에는 이미 Pusher 설정 예시가 포함되어 있어, key, secret, application ID만 빠르게 입력하면 됩니다. 보통 아래와 같이 `.env` 파일에서 Pusher Credentials를 지정합니다.

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```

`config/broadcasting.php` 파일의 `pusher` 설정에서는 클러스터(cluster) 등 추가 옵션도 지정할 수 있습니다.

그리고, `.env` 파일의 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 설정하세요.

```ini
BROADCAST_CONNECTION=pusher
```

이제 [Laravel Echo](#client-side-installation)를 설치 및 구성하면, 클라이언트에서 브로드캐스트 이벤트를 받을 준비가 됩니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 설명은 Ably를 "Pusher 호환" 모드로 사용하는 방법을 다룹니다. Ably 팀에서는 Ably의 고유 기능을 활용할 수 있도록 별도 브로드캐스터 및 Echo 클라이언트를 직접 개발 및 유지관리합니다. 해당 드라이버 사용법은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Ably](https://ably.com)를 브로드캐스트 드라이버로 사용할 때는, `install:broadcasting` 아티즌 명령에 `--ably` 옵션을 추가해 실행합니다. 인증정보 입력, Ably PHP/JS SDK 설치, `.env` 환경 변수 추가가 자동화됩니다.

```shell
php artisan install:broadcasting --ably
```

**계속 진행하기 전, 반드시 Ably 애플리케이션 설정의 "Protocol Adapter Settings"에서 Pusher 프로토콜 지원을 활성화해야 합니다.**

<a name="ably-manual-installation"></a>
#### 수동 설치

수동 설치를 위해 Composer를 사용해 Ably PHP SDK를 설치하세요.

```shell
composer require ably/ably-php
```

다음으로, `config/broadcasting.php` 설정 파일에 Ably Key를 등록합니다. 보통 아래와 같이 `.env` 파일에서 관리합니다.

```ini
ABLY_KEY=your-ably-key
```

그리고, `.env`에서 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 지정합니다.

```ini
BROADCAST_CONNECTION=ably
```

마지막으로, [Laravel Echo](#client-side-installation)를 설치하고 브로드캐스트 수신을 준비하세요.

<a name="client-side-installation"></a>
## 클라이언트 사이드 설치 (Client Side Installation)

<a name="client-reverb"></a>
### Reverb

[Laravel Echo](https://github.com/laravel/echo)는 서버 사이드 브로드캐스트 드라이버가 브로드캐스트한 이벤트를 손쉽게 수신하고, 채널에 구독할 수 있게 돕는 자바스크립트 라이브러리입니다.

`install:broadcasting` 아티즌 명령으로 Reverb를 설치하면 Echo 관련 초기화 작업과 설정이 자동 삽입됩니다. 수동으로 Laravel Echo를 직접 설정하는 방법은 아래 설명을 참고하세요.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Laravel Echo를 직접 설정하려면, 먼저 Reverb가 WebSocket 구독/채널/메시지 처리에 Pusher 프로토콜을 사용하기 때문에, `pusher-js` 패키지를 함께 설치해야 합니다.

```shell
npm install --save-dev laravel-echo pusher-js
```

Echo 설치 후, 애플리케이션의 `resources/js/bootstrap.js` 하단에 새 Echo 인스턴스를 생성하는 게 좋습니다.

```js
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

React, Vue에서도 각각 예시와 같이 사용할 수 있습니다.

설정이 끝났다면, 애플리케이션 에셋을 빌드하세요.

```shell
npm run build
```

> [!WARNING]
> Laravel Echo의 `reverb` 브로드캐스터는 laravel-echo v1.16.0 이상 버전이 필요합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 브로드캐스트 이벤트를 쉽게 수신하고, 채널 구독을 용이하게 해줍니다.

`install:broadcasting --pusher` 아티즌 명령으로 Pusher/Echo 관련 설정이 자동 반영됩니다. 직접 Echo를 설정해야 한다면 아래 과정을 따라하세요.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

프론트엔드에서 Echo를 직접 세팅하려면, WebSocket 구독/채널을 위해 `laravel-echo`와 `pusher-js`를 모두 설치하세요.

```shell
npm install --save-dev laravel-echo pusher-js
```

설치 후, `resources/js/bootstrap.js` 파일에서 Echo 인스턴스를 아래와 같이 만드세요.

```js
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

React, Vue 환경도 별도 예시대로 설정 가능합니다.

이후 `.env` 파일에 필요한 Pusher 환경 변수를 정의해야 합니다. 환경 변수가 없다면 아래와 같이 추가합니다.

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

Echo 설정을 마친 뒤 에셋을 빌드하면 준비가 완료됩니다.

```shell
npm run build
```

> [!NOTE]
> 애플리케이션 자바스크립트 에셋 빌드에 관해서는 [Vite](/docs/12.x/vite) 문서를 참고하세요.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용하기

이미 사전 설정된 Pusher Channels 클라이언트 인스턴스를 Echo와 함께 사용하려면, Echo 생성 시 `client` 옵션에 인스턴스를 전달하면 됩니다.

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
> 아래 문서는 Ably의 "Pusher 호환" 모드 사용법을 설명합니다. Ably 고유의 기능을 활용하려면 [Ably의 Laravel 브로드캐스터 공식 문서](https://github.com/ably/laravel-broadcaster)를 참고하세요.

[Laravel Echo](https://github.com/laravel/echo)는 서버브로드캐스트 이벤트를 쉽게 사용할 수 있게 해줍니다.

`install:broadcasting --ably` 실행 시 Ably와 Echo 관련 설정이 자동으로 반영됩니다. 수동으로 직접 Echo를 구성하려면 아래 설명을 참고하세요.

<a name="ably-client-manual-installation"></a>
#### 수동 설치

Echo를 프론트엔드에 직접 세팅하려면, `laravel-echo`, `pusher-js`를 설치하세요.

```shell
npm install --save-dev laravel-echo pusher-js
```

**계속하기 전, 반드시 Ably 앱 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다.**

설치가 끝나면, `resources/js/bootstrap.js`에서 Echo 인스턴스를 아래처럼 만듭니다.

```js
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

React, Vue 설정도 예시와 같이 맞출 수 있습니다.

Ably Echo 설정의 `VITE_ABLY_PUBLIC_KEY`는 Ably 공개키(Ably Key의 `:` 앞부분)로 지정합니다.

설정 후 애플리케이션 에셋을 빌드하세요.

```shell
npm run dev
```

> [!NOTE]
> 자바스크립트 에셋 빌드에 관한 자세한 설명은 [Vite](/docs/12.x/vite) 문서를 참고하세요.

<a name="concept-overview"></a>
## 개념 개요 (Concept Overview)

Laravel의 이벤트 브로드캐스팅은 WebSocket에 기반하여 서버의 이벤트를 클라이언트 자바스크립트 애플리케이션으로 전달합니다. Laravel은 [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com) 등 다양한 드라이버를 지원합니다. 클라이언트에서는 [Laravel Echo](#client-side-installation) 자바스크립트 패키지로 브로드캐스트 이벤트를 손쉽게 받을 수 있습니다.

이벤트는 "채널"을 통해 브로드캐스트되며, 채널은 공개(Public)와 비공개(Private)로 나눌 수 있습니다. 공개 채널은 인증 없이 모든 사용자가 구독할 수 있지만, 비공개 채널은 인증과 인가가 반드시 필요합니다.

<a name="using-example-application"></a>
### 예제 애플리케이션 활용

이벤트 브로드캐스팅의 각 컴포넌트로 들어가기 전에, 전자상거래 서비스를 예로 들며 고수준 흐름을 살펴보겠습니다.

가령, 사용자가 자신의 주문 배송 상태를 볼 수 있는 페이지가 있고, `OrderShipmentStatusUpdated` 이벤트가 처리될 때마다 발생시킨다고 가정합시다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="the-shouldbroadcast-interface"></a>
#### ShouldBroadcast 인터페이스

주문을 보고 있는 사용자가 새로고침 없이 상태를 확인하도록 하려면, `OrderShipmentStatusUpdated` 이벤트에 `ShouldBroadcast` 인터페이스를 반드시 적용해야 합니다. 이렇게 하면 해당 이벤트가 발생할 때마다 자동으로 브로드캐스팅 됩니다.

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
     * 주문 인스턴스
     *
     * @var \App\Models\Order
     */
    public $order;
}
```

`ShouldBroadcast`를 구현하면, 이벤트 내에 `broadcastOn` 메서드를 반드시 구현해야 합니다. 이 메서드는 이벤트를 브로드캐스트할 채널(들)을 반환합니다. 예를 들어 주문의 생성자만이 상태 변화를 볼 수 있게 하려면, 해당 주문에 고유하게 연결된 비공개 채널을 반환하면 됩니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트를 브로드캐스트할 채널 반환
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```

이벤트를 여러 채널로 브로드캐스트하고 싶다면, `array`를 반환하면 됩니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 이벤트를 브로드캐스트할 채널 배열 반환
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

비공개 채널에 대해 사용자의 인가가 필요함을 기억하세요. 채널 인가 규칙은 애플리케이션의 `routes/channels.php` 파일에서 정의할 수 있습니다. 아래 예시처럼, 특정 주문의 비공개 채널(`orders.1`)을 구독하는 사용자가 실제 해당 주문의 소유자인지 확인할 수 있습니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

`channel` 메서드는 채널 이름과, 사용자가 해당 채널을 청취할 자격이 있는지 `true`/`false`를 반환하는 콜백을 받습니다.

모든 인가 콜백은 인증된 사용자가 첫 번째 인수로, 채널 이름 내의 와일드카드에 해당하는 값들은 그 이후 인수로 전달받습니다. 위 예시처럼 `{orderId}`는 채널 이름에서 ID 부분이 변하는 와일드카드임을 뜻합니다.

<a name="listening-for-event-broadcasts"></a>
#### 브로드캐스트 이벤트 수신

이제 나머지는 자바스크립트 애플리케이션에서 이벤트를 수신하는 일만 남았습니다. [Laravel Echo](#client-side-installation)를 사용하면 매우 간단하게 할 수 있습니다. Echo의 React 및 Vue hook을 활용하면 손쉽게 이벤트를 감지할 수 있고, 기본적으로 이벤트의 public 속성은 모두 브로드캐스트 데이터에 포함됩니다.

```js
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue
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
## 브로드캐스트 이벤트 정의 (Defining Broadcast Events)

특정 이벤트를 브로드캐스트 대상으로 만들려면 해당 이벤트 클래스에 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크가 생성하는 모든 이벤트 클래스에 이미 import되어 있으므로, 언제든 손쉽게 붙여 사용할 수 있습니다.

`ShouldBroadcast`는 반드시 하나의 메서드, 즉 `broadcastOn`을 구현해야 합니다. 이 메서드는 이벤트가 브로드캐스트될 채널 또는 채널 배열을 반환하는데, 반환값은 `Channel`, `PrivateChannel`, 또는 `PresenceChannel` 인스턴스여야 합니다. `Channel`은 모든 사용자가 구독할 수 있는 공개 채널이며, `PrivateChannel`과 `PresenceChannel`은 인가가 반드시 필요한 비공개 채널입니다.

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
     * 새 이벤트 인스턴스 생성자
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * 이벤트가 브로드캐스트될 채널(들) 반환
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

이제 `ShouldBroadcast`를 구현한 상태라면, [이벤트를 디스패치](/docs/12.x/events)하면 자동으로 큐 작업을 통해 해당 드라이버로 이벤트가 브로드캐스팅됩니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트 클래스 이름을 브로드캐스트 이벤트명으로 사용합니다. 하지만 `broadcastAs` 메서드를 정의해 브로드캐스트 이름을 커스터마이징할 수 있습니다.

```php
/**
 * 이벤트의 브로드캐스트 이름 반환
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```

이렇게 브로드캐스트 이름을 커스터마이징했다면, Echo에서 리스닝할 때 반드시 앞에 `.`(dot)를 셋팅해야 네임스페이스가 붙지 않습니다.

```javascript
.listen('.server.created', function (e) {
    // ...
});
```

<a name="broadcast-data"></a>
### 브로드캐스트 데이터

이벤트가 브로드캐스트될 때, 해당 이벤트의 `public` 속성들은 자동으로 직렬화되어 페이로드로 전송됩니다. 따라서 자바스크립트에서 모든 public 데이터를 접근할 수 있습니다. 예를 들어 public `$user` 속성에 Eloquent 모델이 포함되어 있으면 다음과 같은 JSON이 전송됩니다.

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```

브로드캐스트 페이로드를 세밀하게 제어하고 싶다면, `broadcastWith` 메서드를 추가로 구현할 수 있습니다.

```php
/**
 * 브로드캐스트할 데이터 반환
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

기본적으로 각 브로드캐스트 이벤트는 `queue.php` 설정 파일에 명시된 기본 연결/큐에 할당됩니다. 필요하다면 이벤트 클래스에 `connection` 및 `queue` 속성을 추가해 커스터마이징할 수 있습니다.

```php
/**
 * 브로드캐스트 시 사용할 큐 연결명
 *
 * @var string
 */
public $connection = 'redis';

/**
 * 브로드캐스트 작업을 올릴 큐 이름
 *
 * @var string
 */
public $queue = 'default';
```

또는, `broadcastQueue` 메서드로 큐 이름만 간단하게 커스터마이징할 수도 있습니다.

```php
/**
 * 브로드캐스트 작업을 올릴 큐 이름 반환
 */
public function broadcastQueue(): string
{
    return 'default';
}
```

이벤트를 기본 큐 드라이버가 아닌 `sync` 큐로 즉시 브로드캐스트해야 할 경우, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현하면 됩니다.

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

특정 조건일 때만 이벤트를 브로드캐스트하고 싶다면, 이벤트 클래스에 `broadcastWhen` 메서드를 추가할 수 있습니다.

```php
/**
 * 이 이벤트가 브로드캐스트될지 여부 반환
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```

<a name="broadcasting-and-database-transactions"></a>
#### 브로드캐스팅과 데이터베이스 트랜잭션

브로드캐스트 이벤트가 데이터베이스 트랜잭션 내에서 디스패치되면, 큐에서 이 이벤트 작업이 트랜잭션 커밋 전에 처리될 수 있습니다. 이렇게 되면, 트랜잭션 내에서 변경된 모델이나 레코드가 실제 DB에 반영되지 않은 상태일 수 있으므로 예상치 못한 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 옵션이 `false`로 설정된 경우에도, 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 트랜잭션이 모두 마무리된 이후에 브로드캐스트 작업이 진행됩니다.

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
> 이러한 이슈의 대안 및 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션 문서](/docs/12.x/queues#jobs-and-database-transactions)를 참고하세요.

<a name="authorizing-channels"></a>
## 채널 인가 (Authorizing Channels)

Private 채널에서는 인증된 사용자가 실제로 해당 채널을 구독할 자격이 있는지 추가 확인이 필요합니다. 이 과정은 채널 이름을 포함하여 HTTP 요청을 Laravel 애플리케이션으로 보내고, 애플리케이션이 인가 여부를 결정하게 됩니다. [Laravel Echo](#client-side-installation)를 사용할 경우, 이러한 인증 라우트 호출은 자동으로 처리됩니다.

브로드캐스팅이 설치되면, Laravel은 자동으로 `/broadcasting/auth` 라우트를 등록합니다. 자동 등록이 실패했다면, 다음과 같이 직접 등록할 수 있습니다.

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    channels: __DIR__.'/../routes/channels.php',
    health: '/up',
)
```

<a name="defining-authorization-callbacks"></a>
### 인가 콜백 정의

이제 실제로 요청 사용자가 채널을 청취할 자격이 있는지 판단하는 로직을 작성해야 합니다. 이 코드는 `install:broadcasting` 명령어로 생성된 `routes/channels.php` 파일에서 관리합니다. `Broadcast::channel` 메서드에 콜백을 등록하여 인가 로직을 구현하세요.

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```

모든 인가 콜백은 인증된 사용자가 첫 번째 인자로, 와일드카드는 두 번째 인자로 자동 전달받습니다.

현재 등록된 브로드캐스트 채널 인가 콜백을 보려면 다음 아티즌 명령을 사용할 수 있습니다.

```shell
php artisan channel:list
```

<a name="authorization-callback-model-binding"></a>
#### 인가 콜백에서 모델 바인딩

HTTP 라우트처럼, 채널 라우트에서도 암묵적/명시적 [라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 사용할 수 있습니다. 예를 들어, 문자열/숫자 ID 대신 실제 `Order` 모델 인스턴스를 받을 수 있습니다.

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```

> [!WARNING]
> HTTP 라우트 모델 바인딩과 다르게, 채널 모델 바인딩에서는 [암묵적 모델 바인딩 스코핑](/docs/12.x/routing#implicit-model-binding-scoping)이 지원되지 않습니다. 하지만 대부분의 경우 한 모델의 기본키로 충분히 범위 지정이 가능합니다.

<a name="authorization-callback-authentication"></a>
#### 인가 콜백에서 인증 처리

Private 및 Presence 채널은 기본 인증 가드를 통해 현재 사용자를 인증합니다. 인증되지 않으면 콜백이 실행되지 않으며 자동으로 인가가 거부됩니다. 필요하다면 여러 커스텀 가드를 아래와 같이 지정할 수도 있습니다.

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```

<a name="defining-channel-classes"></a>
### 채널 클래스 정의

여러 채널을 사용하는 대형 애플리케이션이라면 `routes/channels.php`가 쉽게 커질 수 있습니다. 이럴 때는 콜백 대신 채널 클래스를 생성해 관리할 수 있습니다. `make:channel` 아티즌 명령으로 클래스 기초를 만들고, `App/Broadcasting` 디렉터리에서 사용할 수 있습니다.

```shell
php artisan make:channel OrderChannel
```

다음으로, 채널을 라우트에 등록하세요.

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```

실제 인가 로직은 채널 클래스의 `join` 메서드에 배치하세요. 여기서도 모델 바인딩을 활용할 수 있습니다.

```php
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    public function __construct() {}

    /**
     * 채널 접근 인증
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```

> [!NOTE]
> 다른 Laravel 클래스처럼, 채널 클래스도 [서비스 컨테이너](/docs/12.x/container)에서 자동으로 의존성 주입됩니다. 생성자에 필요한 의존성을 타입힌트로 선언할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅 (Broadcasting Events)

이벤트가 정의되고 `ShouldBroadcast` 인터페이스로 지정되었다면, 해당 이벤트를 단순히 디스패치하면 Laravel 이벤트 디스패처가 이를 알아서 큐에 브로드캐스팅합니다.

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```

<a name="only-to-others"></a>
### Others만을 대상으로 브로드캐스팅

애플리케이션 내부의 특정 채널 구독자 전체(자기 자신 제외)에게만 이벤트를 브로드캐스트하고 싶을 때가 있습니다. 이럴 땐 `broadcast` 헬퍼와 `toOthers` 메서드를 사용하세요.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```

보다 명확하게 예를 들자면, 사용자가 새로운 할 일을 만들어서 `/task` 엔드포인트에 POST 요청을 보낼 때, 서버에서 새로 추가된 작업 정보를 브로드캐스트 하는 상황을 생각해 봅시다. 이 때, 브라우저는 아래 코드처럼 엔드포인트 응답을 받아 직접 배열에 작업을 추가할 수 있습니다.

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```

하지만, 이미 서버에서 작업 추가를 브로드캐스트하면 클라이언트가 이 이벤트도 수신하므로, 같은 할 일이 두 번 추가될 수 있습니다. 이런 중복을 막으려면 `toOthers`를 사용해 현재 사용자에게는 브로드캐스트하지 않도록 설정해야 합니다.

> [!WARNING]
> `toOthers` 메서드 호출을 위해서는 이벤트 클래스에 반드시 `Illuminate\Broadcasting\InteractsWithSockets` 트레이트가 필요합니다.

<a name="only-to-others-configuration"></a>
#### 설정

Laravel Echo 인스턴스를 초기화하면, 해당 커넥션에 소켓 ID가 할당됩니다. 전역 [Axios](https://github.com/axios/axios) 인스턴스를 사용해 HTTP 요청을 보낼 경우, `X-Socket-ID` 헤더가 자동으로 모든 요청에 포함됩니다. 그리고 `toOthers` 호출 시 Laravel이 이 헤더에서 소켓 ID를 추출해 현재 커넥션에는 브로드캐스트하지 않도록 처리합니다.

전역 Axios 인스턴스를 사용하지 않는다면, 모든 요청에 `X-Socket-ID`를 직접 헤더로 전달해야 합니다. 소켓 ID는 다음처럼 가져올 수 있습니다.

```js
var socketId = Echo.socketId();
```

<a name="customizing-the-connection"></a>
### 커넥션 커스터마이징

여러 브로드캐스트 커넥션을 사용하는 애플리케이션에서, 기본 브로드캐스터가 아닌 특정 드라이버로 이벤트를 브로드캐스트하려면 `via` 메서드로 연결명을 지정할 수 있습니다.

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```

또는, 이벤트 클래스의 생성자에 `broadcastVia`를 호출하여 브로드캐스트 커넥션을 지정해도 됩니다. 다만, 사전에 `InteractsWithBroadcasting` 트레이트를 클래스에 포함해야 합니다.

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

    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```

<a name="anonymous-events"></a>
### 익명 이벤트

별도의 이벤트 클래스를 만들지 않고 프론트엔드로 간단히 이벤트를 브로드캐스트하고 싶다면, `Broadcast` 파사드의 "익명 이벤트" 메서드를 활용할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->send();
```

위 예시의 브로드캐스트 결과는 다음과 같습니다.

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```

`as`, `with` 메서드로 이벤트 이름과 데이터도 변경할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```

결과:

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```

비공개 또는 프레즌스 채널로 익명 이벤트를 브로드캐스트하고 싶다면 다음 메서드를 사용하세요.

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```

`send` 메서드는 작업을 [큐](/docs/12.x/queues)에 등록해 비동기로 처리합니다. 즉시 브로드캐스트하려면 `sendNow` 메서드를 사용할 수 있습니다.

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```

현재 인증 사용자를 제외한 전체 채널에 브로드캐스트하려면 `toOthers`를 체이닝하면 됩니다.

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```

<a name="rescuing-broadcasts"></a>
### 브로드캐스팅 예외 처리

큐 서버가 사용할 수 없거나 Laravel이 이벤트 브로드캐스팅 중 오류를 만나면 예외가 발생해, 사용자가 에러 페이지를 볼 수 있습니다. 브로드캐스팅은 핵심 기능이 아닌 보조 기능인 경우가 많으므로, 이런 예외로 사용자 경험이 저해되지 않도록 이벤트에 `ShouldRescue` 인터페이스를 구현할 수 있습니다.

`ShouldRescue`를 구현한 이벤트는 브로드캐스트 시 Laravel의 [rescue 헬퍼](/docs/12.x/helpers#method-rescue)로 감싸 예외를 자동으로 로깅하고, 애플리케이션이 정상적으로 계속 동작하도록 해 줍니다.

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

[Laravel Echo 설치 및 인스턴스화](#client-side-installation)가 끝났다면, 이제 서버에서 브로드캐스트된 이벤트를 청취할 수 있습니다. 먼저 `channel` 메서드로 채널 인스턴스를 얻고, `listen` 메서드로 원하는 이벤트를 수신하세요.

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```

비공개 채널의 이벤트를 리스닝하려면 `private` 메서드를 사용하면 됩니다. 여러 이벤트 수신도 체이닝으로 가능합니다.

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```

<a name="stop-listening-for-events"></a>
#### 이벤트 리스닝 중단

채널에서 [완전히 나가지 않고](#leaving-a-channel), 특정 이벤트 리스닝만 중단하려면 `stopListening` 메서드를 사용할 수 있습니다.

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```

<a name="leaving-a-channel"></a>
### 채널 나가기

채널을 완전히 나가려면 Echo 인스턴스의 `leaveChannel` 메서드를 호출합니다.

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```

채널뿐만 아니라 관련된 private, presence 채널도 모두 나가고 싶다면 `leave`를 사용하세요.

```js
Echo.leave(`orders.${this.order.id}`);
```
<a name="namespaces"></a>
### 네임스페이스

위 예시들에서 이벤트 클래스의 전체 네임스페이스를 지정하지 않은 것을 볼 수 있습니다. Echo는 기본적으로 이벤트가 `App\Events` 네임스페이스에 있다고 가정합니다. Echo 인스턴스 생성 시 `namespace` 옵션으로 변경도 가능합니다.

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```

혹은, Echo에서 이벤트를 구독할 때 클래스명 앞에 `.`을 붙여서 항상 전체 네임스페이스명을 지정할 수 있습니다.

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```

<a name="using-react-or-vue"></a>
### React 또는 Vue 사용하기

Laravel Echo는 React, Vue hook을 기본 제공하여 이벤트 리스닝을 매우 간단하게 만들어줍니다. 시작하려면 `useEcho` 훅을 호출하면 됩니다. 이 훅은 private 이벤트 리스닝 전용이며, 컴포넌트 언마운트 시 자동으로 채널을 떠나줍니다.

```js
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue
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

여러 이벤트를 동시에 청취하려면 이벤트 배열을 넘기세요.

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```

이벤트 페이로드의 타입을 명시하면 타입 안정성과 자동 완성도 누릴 수 있습니다.

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

`useEcho` 훅은 컴포넌트가 언마운트되면 자동으로 채널을 떠나지만, 반환되는 함수를 이용해 프로그래밍적으로 수동 시작/중단도 가능합니다.

```js
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// 리스닝 중단(채널은 그대로 유지)
stopListening();

// 리스닝 다시 시작
listen();

// 채널 나가기
leaveChannel();

// 채널 및 관련 채널 모두 나가기
leave();
```

```vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// 리스닝 중단(채널은 그대로 유지)
stopListening();

// 리스닝 재시작
listen();

// 채널 나가기
leaveChannel();

// 채널 및 관련 private, presence 채널 모두 나가기
leave();
</script>
```

<a name="react-vue-connecting-to-public-channels"></a>
#### 공개 채널 연결

공개 채널로 연결하려면 `useEchoPublic` 훅을 사용하세요.

```js
import { useEchoPublic } from "@laravel/echo-react";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue
<script setup lang="ts">
import { useEchoPublic } from "@laravel/echo-vue";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connecting-to-presence-channels"></a>
#### 프레즌스 채널 연결

프레즌스 채널 연결에는 `useEchoPresence` 훅을 활용하세요.

```js
import { useEchoPresence } from "@laravel/echo-react";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue
<script setup lang="ts">
import { useEchoPresence } from "@laravel/echo-vue";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

<a name="react-vue-connection-status"></a>
#### 커넥션 상태 확인

현재 WebSocket 커넥션 상태를 가져오려면, 자동으로 반영되는 `useConnectionStatus` 훅을 사용할 수 있습니다.

```js
import { useConnectionStatus } from "@laravel/echo-react";

function ConnectionIndicator() {
    const status = useConnectionStatus();

    return <div>Connection: {status}</div>;
}
```

```vue
<script setup lang="ts">
import { useConnectionStatus } from "@laravel/echo-vue";

const status = useConnectionStatus();
</script>

<template>
    <div>Connection: {{ status }}</div>
</template>
```

가능한 상태 값:

<div class="content-list" markdown="1">

- `connected` - WebSocket 서버에 정상적으로 연결됨
- `connecting` - 연결 시도 중
- `reconnecting` - 연결이 끊어져 재연결 시도 중
- `disconnected` - 연결 끊김 및 재연결 시도 중 아님
- `failed` - 연결 실패/재연결 시도 안함

</div>

<a name="presence-channels"></a>
## 프레즌스 채널(Presence Channels)

프레즌스 채널은 비공개 채널 기반의 보안은 그대로 두면서, 누가 채널에 참여 중인지까지 알 수 있는 기능이 추가된 특별한 채널입니다. 예를 들어 채팅방 접속자 목록, 동시 접속 사용자 감지 등 실시간 협업 및 알림 기능 구축에 유용합니다.

<a name="authorizing-presence-channels"></a>
### 프레즌스 채널 인가

프레즌스 채널 역시 비공개 채널이므로, 반드시 [인가가 필요합니다](#authorizing-channels). 단, 인가 콜백을 구현할 때 `true`만 반환하면 안 되고, 사용자의 정보를 담은 배열을 반환해야 합니다.

인가 콜백에서 반환한 정보는 프론트엔드 Javascript의 프레즌스 채널 리스너에서 사용할 수 있습니다. 사용자 인가에 실패할 경우에는 `false`나 `null`을 반환하세요.

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

<a name="joining-presence-channels"></a>
### 프레즌스 채널 참여

Echo의 `join` 메서드로 프레즌스 채널에 참여할 수 있습니다. 여기서 반환되는 `PresenceChannel` 인스턴스는 `listen` 외에도 `here`, `joining`, `leaving` 등의 이벤트를 청취할 수 있습니다.

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

- `here`: 채널에 입장 성공 시 즉시 실행되며, 현재 채널에 접속 중인 모든 사용자 정보를 배열로 받습니다.
- `joining`: 새 사용자가 채널에 입장할 때 실행됩니다.
- `leaving`: 사용자가 채널을 떠날 때 실행됩니다.
- `error`: 인증 엔드포인트의 HTTP 응답이 200이 아니거나, JSON 파싱에 실패할 때 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널에 브로드캐스트

프레즌스 채널에도 다른 채널과 마찬가지로 이벤트를 브로드캐스트할 수 있습니다. 예를 들어 채팅방에서 `NewMessage` 이벤트를 방 전체에 브로드캐스트하려면, 이벤트 클래스의 `broadcastOn` 메서드에서 `PresenceChannel`을 반환하세요.

```php
/**
 * 이벤트 브로드캐스트 채널(들) 반환
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

다른 이벤트와 마찬가지로, `broadcast` 헬퍼와 `toOthers`를 함께 사용하면 현재 유저를 제외하고 브로드캐스트할 수도 있습니다.

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```

Echo의 `listen`으로 프레즌스 채널 이벤트를 수신할 수 있습니다.

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
> 모델 브로드캐스팅 문서를 읽기 전에, Laravel 모델 브로드캐스트의 기본 개념과 브로드캐스트 이벤트 생성 및 리스닝 방법을 충분히 이해하시길 권장합니다.

애플리케이션의 [Eloquent 모델](/docs/12.x/eloquent)이 생성, 수정, 삭제될 때마다 이벤트를 브로드캐스트하는 것은 흔한 요구입니다. 물론 직접 [커스텀 이벤트](/docs/12.x/eloquent#events)를 정의하고, 이를 `ShouldBroadcast`로 지정해 처리할 수도 있습니다.

하지만, 오직 브로드캐스트만을 위해 이벤트 클래스를 만드는 것이 번거롭다면, Laravel은 Eloquent 모델이 상태 변경 시 자동으로 브로드캐스트하도록 설정할 수 있도록 제공합니다.

먼저, Eloquent 모델에 `Illuminate\Database\Eloquent\BroadcastsEvents` 트레이트를 추가하세요. 그리고 `broadcastOn` 메서드를 정의해, 어떤 채널에 이벤트가 브로드캐스트될지 반환하면 됩니다.

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
     * 이 포스트의 소유자 반환
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * 모델 이벤트가 브로드캐스트될 채널(들) 반환
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```

이제 트레이트와 `broadcastOn` 정의가 끝나면, 생성/수정/삭제/휴지통 이동/복원 등 모델 인스턴스 변화에 따라 자동으로 이벤트가 브로드캐스트됩니다.

또한, `broadcastOn`의 `$event` 파라미터에는 변화의 종류(`created`, `updated`, `deleted`, `trashed`, `restored`)가 문자열로 전달되어, 상황에 따라 채널 구성을 다르게 할 수도 있습니다.

```php
/**
 * 모델 이벤트가 브로드캐스트될 채널(들) 반환
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

Laravel이 내부적으로 어떤 방식으로 모델 브로드캐스트 이벤트를 생성할지 커스터마이징 하고 싶다면, 모델에 `newBroadcastableEvent` 메서드를 정의하세요. 반환값은 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스여야 합니다.

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * 모델의 브로드캐스트 이벤트를 생성
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
#### 채널 명명 규칙

위 예시의 `broadcastOn` 메서드는 `Channel` 인스턴스 대신 Eloquent 모델 인스턴스를 반환했습니다. 만약 Eloquent 모델을 직접 반환하면, Laravel은 자동으로 모델 클래스명과 PK(기본키)로 비공개 채널을 만듭니다.

예를 들어, `App\Models\User` 모델의 `id`가 1일 경우, `Illuminate\Broadcasting\PrivateChannel`의 채널명은 `App.Models.User.1`이 됩니다. 물론 직접 채널명을 제어하려면, `Channel` 인스턴스를 반환하면 됩니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * 모델 이벤트 브로드캐스트 채널 반환
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

직접 채널 인스턴스에 모델을 전달할 수도 있습니다. 이 때에는 모델 채널 명명 규칙이 그대로 적용됩니다.

```php
return [new Channel($this->user)];
```

모델의 채널 이름이 궁금하다면, 모델 인스턴스의 `broadcastChannel` 메서드를 호출하면 됩니다. 예를 들어 `App.Models.User.1`이 반환됩니다.

```php
$user->broadcastChannel();
```

<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 명명 규칙

모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉터리에 실제로 존재하는 이벤트가 아니기 때문에, Laravel이 관례적으로 이벤트명, 페이로드를 결정합니다. 관례상, 이벤트명은 모델의 클래스명(네임스페이스 제외) + 이벤트 종류(예: `PostUpdated`) 형태로 브로드캐스트됩니다.

즉, `App\Models\Post` 모델이 업데이트되면, `.PostUpdated`라는 이벤트명을 가진 데이터가 아래와 같이 브로드캐스트됩니다.

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

모델 삭제 시에는 `.UserDeleted`와 같은 이름이 됩니다.

원한다면, `broadcastAs`, `broadcastWith` 메서드를 정의해 이벤트명/페이로드를 커스터마이징할 수 있습니다. 이때 `$event` 파라미터에 이벤트 종류가 들어와 활용할 수 있습니다. `null`을 반환하면 Laravel 관례 규칙이 적용됩니다.

```php
/**
 * 모델 이벤트의 브로드캐스트명 반환
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * 모델의 브로드캐스트 데이터 반환
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

`BroadcastsEvents` 트레이트와 `broadcastOn` 메서드를 추가했다면, 클라이언트 애플리케이션에서 모델 브로드캐스트 이벤트를 리스닝할 준비가 된 것입니다. 더 자세한 방식은 [이벤트 리스닝 문서](#listening-for-events)를 참조하세요.

우선, `private` 메서드로 채널 인스턴스를 얻고, `listen`으로 이벤트를 수신하세요. 이때 채널 이름은 [모델 브로드캐스팅 규칙](#model-broadcasting-conventions)과 일치해야 합니다.

특이하게, 모델 브로드캐스트 이벤트는 `App\Events`에 실제 클래스가 없으므로 이벤트명을 반드시 앞에 `.`을 붙여야 합니다. 각 브로드캐스트 이벤트의 `model` 속성이 모델의 모든 데이터를 포함합니다.

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```

<a name="model-broadcasts-with-react-or-vue"></a>
#### React 또는 Vue에서 사용하기

React, Vue 환경에서는 Echo의 `useEchoModel` 훅을 사용하면 훨씬 쉽게 모델 브로드캐스트를 수신할 수 있습니다.

```js
import { useEchoModel } from "@laravel/echo-react";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
```

```vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```

더 정확한 타입 지원을 위해 이벤트 페이로드 형태에 타입을 지정할 수도 있습니다.

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
> [Pusher Channels](https://pusher.com/channels)를 사용할 경우, [애플리케이션 대시보드](https://dashboard.pusher.com/)의 "App Settings"에서 반드시 "Client Events" 옵션을 활성화해야 클라이언트 이벤트를 보낼 수 있습니다.

때로는, Laravel 애플리케이션을 거치지 않고도 브라우저 간 직접 이벤트를 브로드캐스트해야 할 필요가 있습니다. 예를 들어, 채팅방에서 "사용자가 입력 중…" 알림 등 클라이언트 간 인터랙션이 필요한 경우입니다.

이때 Echo의 `whisper` 메서드를 사용하세요.

```js
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

React, Vue 환경에서는 아래와 같이 사용할 수 있습니다.

```js
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
```

```vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

리스닝은 `listenForWhisper` 메서드로 핸들링합니다.

```js
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

React, Vue도 동일 원리로 활용할 수 있습니다.

```js
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
```

```vue
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
## 알림(Notifications)

이벤트 브로드캐스팅과 [알림](/docs/12.x/notifications)을 결합하면, 자바스크립트 애플리케이션이 새 알림이 도착할 때마다 페이지를 새로고침하지 않고도 푸시 알림을 받아볼 수 있습니다. 시작 전, [브로드캐스트 알림 채널](/docs/12.x/notifications#broadcast-notifications) 사용법을 충분히 확인하세요.

알림이 브로드캐스트 채널을 사용하도록 구성했다면, Echo의 `notification` 메서드로 해당 브로드캐스트를 받을 수 있습니다. 채널 이름은 알림을 받는 엔티티 클래스명으로 지정되어야 합니다.

```js
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

React, Vue에서의 활용 예시도 아래와 같습니다.

```js
import { useEchoModel } from "@laravel/echo-react";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
```

```vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

이 예시에서는, `App\Models\User`에 브로드캐스트 채널로 발송된 모든 알림이 콜백에서 수신됩니다. `routes/channels.php`에는 `App.Models.User.{id}` 채널 인가 콜백도 이미 포함되어 있습니다.

<a name="stop-listening-for-notifications"></a>
#### 알림 리스닝 중단

알림 리스닝만 중단하고 싶을 땐, [채널을 나가거나](#leaving-a-channel) 하지 않고도 `stopListeningForNotification` 메서드를 사용할 수 있습니다.

```js
const callback = (notification) => {
    console.log(notification.type);
}

// 리스닝 시작
Echo.private(`App.Models.User.${userId}`)
    .notification(callback);

// 리스닝 중단(같은 콜백이어야 함)
Echo.private(`App.Models.User.${userId}`)
    .stopListeningForNotification(callback);
```
