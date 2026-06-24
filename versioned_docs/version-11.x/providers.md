<!-- # Service Providers -->
# Service Providers

- [Introduction](#introduction)
- [Writing Service Providers](#writing-service-providers)
    - [The Register Method](#the-register-method)
    - [The Boot Method](#the-boot-method)
- [Registering Providers](#registering-providers)
- [Deferred Providers](#deferred-providers)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Service providers are the central place of all Laravel application bootstrapping. Your own application, as well as all of Laravel's core services, are bootstrapped via service providers. -->
서비스 프로바이더는 Laravel 애플리케이션이 부트스트랩(초기화)되는 중심 역할을 담당합니다. 여러분이 작성한 애플리케이션은 물론, Laravel의 모든 핵심 서비스들도 서비스 프로바이더를 통해 부트스트랩됩니다.

<!-- But, what do we mean by "bootstrapped"? In general, we mean **registering** things, including registering service container bindings, event listeners, middleware, and even routes. Service providers are the central place to configure your application. -->
여기서 "부트스트랩"이란 정확히 무엇일까요? 일반적으로 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 라우트 등록 등 다양한 설정 작업을 의미합니다. 서비스 프로바이더는 이러한 애플리케이션 구성을 한 곳에서 담당하는 역할을 합니다.

<!-- Laravel uses dozens of service providers internally to bootstrap its core services, such as the mailer, queue, cache, and others. Many of these providers are "deferred" providers, meaning they will not be loaded on every request, but only when the services they provide are actually needed. -->
Laravel 내부에서는 메일러, 큐, 캐시 등과 같은 핵심 서비스를 부트스트랩하기 위해 수십 개의 서비스 프로바이더를 사용합니다. 이 중 다수는 "지연 프로바이더"로 동작하는데, 이러한 프로바이더는 제공하는 서비스가 실제로 필요할 때만 로드되고, 모든 요청 시마다 로드되는 것은 아닙니다.

<!-- All user-defined service providers are registered in the `bootstrap/providers.php` file. In the following documentation, you will learn how to write your own service providers and register them with your Laravel application. -->
사용자가 직접 정의한 모든 서비스 프로바이더는 `bootstrap/providers.php` 파일에 등록됩니다. 아래 설명에서는 직접 서비스 프로바이더를 작성하고 이를 Laravel 애플리케이션에 등록하는 방법을 알아봅니다.

> [!NOTE]
> Laravel이 요청을 처리하는 방식과 내부 동작 원리를 더 깊이 이해하고 싶다면, Laravel [request lifecycle](/docs/11.x/lifecycle) 문서를 참고해 보시기 바랍니다.

<a name="writing-service-providers"></a>
<!-- ## Writing Service Providers -->
## Writing Service Providers

<!-- All service providers extend the `Illuminate\Support\ServiceProvider` class. Most service providers contain a `register` and a `boot` method. Within the `register` method, you should **only bind things into the [service container](/docs/11.x/container)**. You should never attempt to register any event listeners, routes, or any other piece of functionality within the `register` method. -->
모든 서비스 프로바이더 클래스는 `Illuminate\Support\ServiceProvider` 클래스를 상속합니다. 대부분의 서비스 프로바이더에는 `register` 메서드와 `boot` 메서드가 포함되어 있습니다. 이 중 `register` 메서드에서는 **반드시 [service container](/docs/11.x/container)에 바인딩만** 수행해야 합니다. 이벤트 리스너, 라우트, 그 외 기능은 `register` 메서드에서 등록해서는 안 됩니다.

<!-- The Artisan CLI can generate a new provider via the `make:provider` command. Laravel will automatically register your new provider in your application's `bootstrap/providers.php` file: -->
Artisan CLI를 사용하여 `make:provider` 명령어로 새로운 프로바이더를 생성할 수 있습니다. Laravel은 이 명령어로 생성된 프로바이더를 자동으로 애플리케이션의 `bootstrap/providers.php` 파일에 등록합니다.

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
<!-- ### The Register Method -->
### The Register Method

<!-- As mentioned previously, within the `register` method, you should only bind things into the [service container](/docs/11.x/container). You should never attempt to register any event listeners, routes, or any other piece of functionality within the `register` method. Otherwise, you may accidentally use a service that is provided by a service provider which has not loaded yet. -->
앞서 언급한 대로, `register` 메서드에서는 오직 [service container](/docs/11.x/container)에 바인딩만 해야 합니다. 이벤트 리스너나 라우트, 그 외 기타 기능을 `register` 메서드에서 등록해서는 안 됩니다. 그렇지 않으면, 아직 로드되지 않은 서비스 프로바이더에서 제공하는 서비스를 실수로 사용하게 될 수 있습니다.

<!-- Let's take a look at a basic service provider. Within any of your service provider methods, you always have access to the `$app` property which provides access to the service container: -->
아래는 기본적인 서비스 프로바이더 예시입니다. 서비스 프로바이더의 어떤 메서드에서든 `$app` 프로퍼티에 접근할 수 있으며, 이 프로퍼티는 서비스 컨테이너에 대한 접근을 제공합니다.

```
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection(config('riak'));
        });
    }
}
```

<!-- This service provider only defines a `register` method, and uses that method to define an implementation of `App\Services\Riak\Connection` in the service container. If you're not yet familiar with Laravel's service container, check out [its documentation](/docs/11.x/container). -->
이 서비스 프로바이더는 오직 `register` 메서드만 정의하며, 해당 메서드를 사용하여 서비스 컨테이너에 `App\Services\Riak\Connection` 클래스에 대한 구현을 등록합니다. Laravel의 서비스 컨테이너에 대해 잘 모르신다면, [its documentation](/docs/11.x/container)를 참고하시기 바랍니다.

<a name="the-bindings-and-singletons-properties"></a>
<!-- #### The `bindings` and `singletons` Properties -->
#### The `bindings` and `singletons` Properties

<!-- If your service provider registers many simple bindings, you may wish to use the `bindings` and `singletons` properties instead of manually registering each container binding. When the service provider is loaded by the framework, it will automatically check for these properties and register their bindings: -->
서비스 프로바이더에서 여러 개의 간단한 바인딩을 등록해야 하는 경우, 각 바인딩을 일일이 메서드로 작성하는 대신 `bindings` 및 `singletons` 프로퍼티를 사용할 수 있습니다. 프레임워크가 서비스 프로바이더를 로드할 때 이 프로퍼티들을 자동으로 확인하고, 지정된 바인딩을 등록합니다.

```
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
     * All of the container bindings that should be registered.
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * All of the container singletons that should be registered.
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
<!-- ### The Boot Method -->
### The Boot Method

<!-- So, what if we need to register a [view composer](/docs/11.x/views#view-composers) within our service provider? This should be done within the `boot` method. **This method is called after all other service providers have been registered**, meaning you have access to all other services that have been registered by the framework: -->
서비스 프로바이더에서 [view composer](/docs/11.x/views#view-composers)와 같은 기능을 등록하고 싶다면, 이는 반드시 `boot` 메서드에서 처리해야 합니다. **이 메서드는 모든 다른 서비스 프로바이더의 등록(=register)이 완료된 후 호출**되므로, 프레임워크가 등록한 모든 서비스에 접근할 수 있습니다.

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
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
<!-- #### Boot Method Dependency Injection -->
#### Boot Method Dependency Injection

<!-- You may type-hint dependencies for your service provider's `boot` method. The [service container](/docs/11.x/container) will automatically inject any dependencies you need: -->
서비스 프로바이더의 `boot` 메서드에서 의존성 주입도 사용할 수 있습니다. [service container](/docs/11.x/container)가 자동으로 필요한 의존성을 주입해 줍니다.

```
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * Bootstrap any application services.
 */
public function boot(ResponseFactory $response): void
{
    $response->macro('serialized', function (mixed $value) {
        // ...
    });
}
```

<a name="registering-providers"></a>
<!-- ## Registering Providers -->
## Registering Providers

<!-- All service providers are registered in the `bootstrap/providers.php` configuration file. This file returns an array that contains the class names of your application's service providers: -->
모든 서비스 프로바이더는 `bootstrap/providers.php` 설정 파일에 등록됩니다. 이 파일은 애플리케이션에서 사용되는 서비스 프로바이더 클래스명을 배열로 반환합니다.

```
<?php

return [
    App\Providers\AppServiceProvider::class,
];
```

<!-- When you invoke the `make:provider` Artisan command, Laravel will automatically add the generated provider to the `bootstrap/providers.php` file. However, if you have manually created the provider class, you should manually add the provider class to the array: -->
`make:provider` 아티즌 명령어를 실행하면, Laravel이 자동으로 생성된 프로바이더를 `bootstrap/providers.php` 파일에 추가해줍니다. 하지만 직접 클래스를 만들었을 경우에는 추가로 프로바이더 클래스를 이 배열에 수동으로 등록해야 합니다.

```
<?php

return [
    App\Providers\AppServiceProvider::class,
    App\Providers\ComposerServiceProvider::class, // [tl! add]
];
```

<a name="deferred-providers"></a>
<!-- ## Deferred Providers -->
## Deferred Providers

<!-- If your provider is **only** registering bindings in the [service container](/docs/11.x/container), you may choose to defer its registration until one of the registered bindings is actually needed. Deferring the loading of such a provider will improve the performance of your application, since it is not loaded from the filesystem on every request. -->
여러분이 작성한 프로바이더가 오로지 [service container](/docs/11.x/container) 바인딩만 등록한다면, 실제로 해당 바인딩이 필요할 때까지 로드를 "지연"시킬 수 있습니다. 이러한 지연 로딩 방식은 프로바이더가 매번 파일 시스템에서 로드되지 않기 때문에 애플리케이션 성능을 향상시킬 수 있습니다.

<!-- Laravel compiles and stores a list of all of the services supplied by deferred service providers, along with the name of its service provider class. Then, only when you attempt to resolve one of these services does Laravel load the service provider. -->
Laravel은 지연 프로바이더가 제공하는 서비스 목록과 해당 서비스 프로바이더 클래스명을 컴파일하여 저장합니다. 그리고 이 서비스들 중 하나를 애플리케이션이 해결(resolve)하려 할 때 실제로 해당 서비스 프로바이더를 로드합니다.

<!-- To defer the loading of a provider, implement the `\Illuminate\Contracts\Support\DeferrableProvider` interface and define a `provides` method. The `provides` method should return the service container bindings registered by the provider: -->
프로바이더의 로딩을 지연시키려면, `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고, `provides` 메서드를 정의해야 합니다. 이 `provides` 메서드는 해당 프로바이더에서 등록하는 서비스 컨테이너 바인딩의 목록을 반환해야 합니다.

```
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection($app['config']['riak']);
        });
    }

    /**
     * Get the services provided by the provider.
     *
     * @return array<int, string>
     */
    public function provides(): array
    {
        return [Connection::class];
    }
}
```
