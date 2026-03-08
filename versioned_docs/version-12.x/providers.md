# 서비스 프로바이더 (Service Providers)

- [소개](#introduction)
- [서비스 프로바이더 작성하기](#writing-service-providers)
    - [register 메서드](#the-register-method)
    - [boot 메서드](#the-boot-method)
- [프로바이더 등록하기](#registering-providers)
- [지연 로딩 프로바이더](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 프로바이더는 Laravel 애플리케이션 부트스트랩의 중심 위치입니다. 여러분의 애플리케이션뿐만 아니라 Laravel의 모든 핵심 서비스들도 서비스 프로바이더를 통해 부트스트랩됩니다.

그렇다면 "부트스트랩"이란 무엇을 의미할까요? 일반적으로 이것은 서비스 컨테이너 바인딩 등록, 이벤트 리스너, 미들웨어, 심지어 라우트 등록까지 **등록하는 작업**을 의미합니다. 서비스 프로바이더는 애플리케이션을 설정하는 중심 장소입니다.

Laravel은 메일러, 큐(queue), 캐시(cache) 등과 같은 핵심 서비스를 부트스트랩하기 위해 수십 개의 서비스 프로바이더를 내부적으로 사용합니다. 이들 중 많은 프로바이더는 "지연 로딩(deferred)" 프로바이더로, 매 요청마다 로딩되는 것이 아니라, 해당 서비스가 실제로 필요할 때만 로딩됩니다.

사용자가 정의한 모든 서비스 프로바이더는 `bootstrap/providers.php` 파일에 등록됩니다. 이 문서에서는 여러분이 직접 서비스 프로바이더를 작성하고 Laravel 애플리케이션에 등록하는 방법을 배우게 됩니다.

> [!NOTE]
> Laravel이 요청을 처리하고 내부적으로 작동하는 방식을 더 자세히 알고 싶다면, Laravel [request lifecycle](/docs/12.x/lifecycle) 문서를 참고하세요.

<a name="writing-service-providers"></a>
## 서비스 프로바이더 작성하기

모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속합니다. 대부분의 서비스 프로바이더는 `register`와 `boot` 메서드를 가집니다. `register` 메서드 내에서는 **오직 서비스 컨테이너에 바인딩만 해야 합니다**. 이벤트 리스너, 라우트 또는 기타 기능을 `register` 메서드에서 등록하려고 시도해서는 안 됩니다.

Artisan CLI 명령어 `make:provider`를 통해 새 프로바이더를 생성할 수 있습니다. Laravel은 생성된 프로바이더를 자동으로 애플리케이션 `bootstrap/providers.php` 파일에 등록합니다:

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### register 메서드

앞서 언급했듯이, `register` 메서드 내에서는 서비스 컨테이너에 바인딩만 해야 합니다. 이벤트 리스너, 라우트, 기타 기능을 `register` 메서드에서 등록하지 마세요. 그렇지 않으면 아직 로딩되지 않은 서비스 프로바이더가 제공하는 서비스를 잘못 사용하게 될 수 있습니다.

기본적인 서비스 프로바이더 예제를 살펴보겠습니다. 서비스 프로바이더의 메서드 내에서는 항상 `$app` 속성을 통해 서비스 컨테이너에 접근할 수 있습니다:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection(config('riak'));
        });
    }
}
```

이 서비스 프로바이더는 `register` 메서드만 정의하며, 이 메서드를 이용해 `App\Services\Riak\Connection` 구현을 서비스 컨테이너에 싱글톤으로 바인딩합니다. Laravel의 서비스 컨테이너 사용법이 익숙하지 않다면, [관련 문서](/docs/12.x/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings`와 `singletons` 속성

만약 서비스 프로바이더에서 단순한 바인딩을 다수 등록해야 한다면, 각 바인딩을 수동으로 등록하는 대신 `bindings`와 `singletons` 속성을 사용할 수 있습니다. Laravel은 서비스 프로바이더가 로드될 때 이 속성을 자동으로 확인하고 등록합니다:

```php
<?php

namespace App\Providers;

use App\Contracts\DowntimeNotifier;
use App\Contracts\ServerProvider;
use App\Services\DigitalOceanServerProvider;
use App\Services\PingdomDowntimeNotifier;
use App\Services\ServerToolsProvider;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 등록할 모든 컨테이너 바인딩들
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * 등록할 모든 컨테이너 싱글톤들
     *
     * @var array
     */
    public $singletons = [
        DowntimeNotifier::class => PingdomDowntimeNotifier::class,
        ServerProvider::class => ServerToolsProvider::class,
    ];
}
```

<a name="the-boot-method"></a>
### boot 메서드

그렇다면 서비스 프로바이더 내에서 [view composer](/docs/12.x/views#view-composers)를 등록하고 싶다면 어떻게 해야 할까요? 이 작업은 `boot` 메서드 내에서 수행해야 합니다. **`boot` 메서드는 다른 모든 서비스 프로바이더가 등록된 후 호출**되므로, 프레임워크가 등록한 모든 서비스를 사용할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        View::composer('view', function () {
            // ...
        });
    }
}
```

<a name="boot-method-dependency-injection"></a>
#### boot 메서드 내 의존성 주입

`boot` 메서드에 필요한 의존성을 타입 힌트로 지정할 수 있습니다. 서비스 컨테이너가 자동으로 필요한 의존성을 주입해 줍니다:

```php
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(ResponseFactory $response): void
{
    $response->macro('serialized', function (mixed $value) {
        // ...
    });
}
```

<a name="registering-providers"></a>
## 프로바이더 등록하기

모든 서비스 프로바이더는 `bootstrap/providers.php` 설정 파일에 등록됩니다. 이 파일은 애플리케이션 서비스 프로바이더 클래스들의 배열을 반환합니다:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
];
```

Artisan 명령어 `make:provider`를 실행하면 Laravel이 생성된 프로바이더를 자동으로 `bootstrap/providers.php` 파일에 추가합니다. 하지만 프로바이더 클래스를 수동 생성한 경우, 직접 해당 배열에 프로바이더 클래스를 추가해야 합니다:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
    App\Providers\ComposerServiceProvider::class, // [tl! add]
];
```

<a name="deferred-providers"></a>
## 지연 로딩 프로바이더 (Deferred Providers)

만약 프로바이더가 서비스 컨테이너에 바인딩만 등록한다면, 해당 바인딩이 실제로 필요할 때까지 등록을 지연시킬 수 있습니다. 이렇게 프로바이더 로딩을 지연시키면, 매 요청마다 파일 시스템에서 프로바이더를 로드하지 않아도 되기 때문에 애플리케이션 성능이 향상됩니다.

Laravel은 지연 로딩 서비스 프로바이더가 제공하는 서비스 목록과 프로바이더 클래스 이름을 컴파일하여 저장합니다. 이 후 해당 서비스 중 하나를 해석(해결)하려고 시도할 때 프로바이더를 로드합니다.

프로바이더 로딩을 지연시키려면, `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고 `provides` 메서드를 정의하세요. `provides` 메서드는 프로바이더가 등록하는 서비스 컨테이너 바인딩 목록을 반환해야 합니다:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection($app['config']['riak']);
        });
    }

    /**
     * 프로바이더가 제공하는 서비스 반환
     *
     * @return array<int, string>
     */
    public function provides(): array
    {
        return [Connection::class];
    }
}
```