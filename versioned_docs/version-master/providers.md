# 서비스 프로바이더 (Service Providers)

- [소개](#introduction)
- [서비스 프로바이더 작성하기](#writing-service-providers)
    - [register 메서드](#the-register-method)
    - [boot 메서드](#the-boot-method)
- [프로바이더 등록하기](#registering-providers)
- [지연 로딩 프로바이더](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 프로바이더는 모든 Laravel 애플리케이션 부트스트래핑의 중심 역할을 합니다. 사용자 정의 애플리케이션뿐만 아니라 Laravel 핵심 서비스들도 모두 서비스 프로바이더를 통해 부트스트래핑됩니다.

그렇다면 '부트스트래핑(bootstrapped)'이란 무엇일까요? 일반적으로는 **서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 라우트 등록 등 여러 가지 요소를 등록하는 것**을 의미합니다. 서비스 프로바이더는 애플리케이션을 구성하는 중심 장소입니다.

Laravel은 메일러, 큐, 캐시 등 핵심 서비스를 부트스트랩하기 위해 수십 개의 서비스 프로바이더를 내부적으로 사용합니다. 이 중 많은 프로바이더는 "지연 로딩(deferred)" 프로바이더로, 모든 요청 시 매번 로드되는 것이 아니라, 해당 서비스가 실제로 필요할 때 로드됩니다.

모든 사용자 정의 서비스 프로바이더는 `bootstrap/providers.php` 파일에 등록됩니다. 이 문서에서는 사용자가 직접 서비스 프로바이더를 작성하고 Laravel 애플리케이션에 등록하는 방법에 대해 배웁니다.

> [!NOTE]
> Laravel이 요청을 처리하고 내부적으로 작동하는 방식을 더 자세히 알고 싶다면, Laravel [요청 라이프사이클(request lifecycle)](/docs/master/lifecycle) 문서를 참고하세요.

<a name="writing-service-providers"></a>
## 서비스 프로바이더 작성하기

모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 확장합니다. 대부분의 서비스 프로바이더는 `register`와 `boot` 메서드를 포함합니다. `register` 메서드 안에서는 **오직 [서비스 컨테이너](/docs/master/container)에 바인딩만 해야 합니다**. 절대 이벤트 리스너, 라우트, 혹은 다른 기능을 `register` 메서드 안에서 등록하면 안 됩니다.

Artisan CLI의 `make:provider` 명령어로 새 프로바이더를 생성할 수 있습니다. Laravel은 새로 생성한 프로바이더를 자동으로 `bootstrap/providers.php` 파일에 등록합니다:

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### register 메서드

앞서 언급했듯이, `register` 메서드 안에서는 오직 [서비스 컨테이너](/docs/master/container)에 바인딩만 해야 합니다. 이벤트 리스너, 라우트 또는 다른 기능들은 절대 `register` 메서드에서 등록하지 마세요. 그렇지 않으면 아직 로드되지 않은 서비스 프로바이더가 제공하는 서비스를 잘못 사용하게 될 수 있습니다.

간단한 서비스 프로바이더 예제를 살펴보겠습니다. 모든 서비스 프로바이더 메서드 안에서는 `$app` 속성으로 서비스 컨테이너에 접근할 수 있습니다:

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

이 프로바이더는 `register` 메서드만 정의하며, 여기서 `App\Services\Riak\Connection` 구현체를 서비스 컨테이너에 정의합니다. Laravel의 서비스 컨테이너에 익숙하지 않다면, [관련 문서](/docs/master/container)를 참고하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings` 및 `singletons` 속성

만약 여러 간단한 바인딩을 등록해야 한다면, 각각을 수동으로 등록하는 대신 `bindings`와 `singletons` 속성을 사용할 수 있습니다. 프레임워크가 서비스 프로바이더를 로드할 때, 이 속성들을 자동으로 확인하고 바인딩을 등록합니다:

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
     * 등록할 모든 컨테이너 바인딩
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * 등록할 모든 컨테이너 싱글톤
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

그렇다면 서비스 프로바이더 안에서 [view composer](/docs/master/views#view-composers)를 등록하려면 어떻게 해야 할까요? 이는 `boot` 메서드 안에서 해야 합니다. **이 메서드는 모든 다른 서비스 프로바이더가 등록된 이후 호출되므로**, 프레임워크가 등록한 다른 모든 서비스에 접근할 수 있습니다:

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
#### boot 메서드 의존성 주입

`boot` 메서드에 의존성을 타입 힌트로 선언할 수 있습니다. [서비스 컨테이너](/docs/master/container)가 필요한 모든 의존성을 자동으로 주입합니다:

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

모든 서비스 프로바이더는 `bootstrap/providers.php` 설정 파일에서 등록됩니다. 이 파일은 애플리케이션의 서비스 프로바이더 클래스 이름을 담은 배열을 반환합니다:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
];
```

`make:provider` Artisan 명령을 실행하면, Laravel이 생성된 프로바이더를 자동으로 `bootstrap/providers.php` 파일에 추가합니다. 하지만 수동으로 프로바이더 클래스를 생성했다면, 이 파일 배열에 직접 추가해야 합니다:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
    App\Providers\ComposerServiceProvider::class, // [tl! add]
];
```

<a name="deferred-providers"></a>
## 지연 로딩 프로바이더 (Deferred Providers)

프로바이더가 **오직** [서비스 컨테이너](/docs/master/container)에 바인딩만 등록한다면, 이 등록을 실제로 해당 바인딩이 필요할 때까지 미룰 수 있습니다. 이렇게 하면 애플리케이션이 모든 요청에서 파일 시스템에서 프로바이더를 매번 불러오지 않아 성능이 향상됩니다.

Laravel은 지연 로딩 프로바이더가 제공하는 모든 서비스 목록과 서비스 프로바이더 클래스 이름을 컴파일하여 저장합니다. 그리고 이 서비스들 중 하나를 실제로 요청할 때만 해당 프로바이더를 로드합니다.

프로바이더를 지연 로딩으로 만들려면 `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고 `provides` 메서드를 정의해야 합니다. `provides` 메서드는 프로바이더가 등록하는 서비스 컨테이너 바인딩 목록을 반환해야 합니다:

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