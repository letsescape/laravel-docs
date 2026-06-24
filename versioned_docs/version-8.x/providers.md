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
서비스 프로바이더는 모든 Laravel 애플리케이션의 부트스트래핑(초기 설정)을 담당하는 중심 역할을 합니다. 여러분이 작성한 애플리케이션뿐 아니라, Laravel의 모든 핵심 서비스들도 서비스 프로바이더를 통해 부트스트랩됩니다.

<!-- But, what do we mean by "bootstrapped"? In general, we mean **registering** things, including registering service container bindings, event listeners, middleware, and even routes. Service providers are the central place to configure your application. -->
여기서 "부트스트랩(bootstrapped)"이란 무엇을 의미할까요? 일반적으로, 여기서는 각종 설정 등록, 즉 서비스 컨테이너 바인딩, 이벤트 리스너, 미들웨어, 라우트 등의 다양한 것들을 **등록**하는 과정을 의미합니다. 서비스 프로바이더는 애플리케이션을 구성하는 핵심적인 위치입니다.

<!-- If you open the `config/app.php` file included with Laravel, you will see a `providers` array. These are all of the service provider classes that will be loaded for your application. By default, a set of Laravel core service providers are listed in this array. These providers bootstrap the core Laravel components, such as the mailer, queue, cache, and others. Many of these providers are "deferred" providers, meaning they will not be loaded on every request, but only when the services they provide are actually needed. -->
`config/app.php` 파일을 열어보면 `providers` 배열이 있습니다. 이 배열에는 애플리케이션에서 로드될 서비스 프로바이더 클래스들이 나열되어 있습니다. 기본적으로 Laravel의 핵심 서비스 프로바이더들이 이 배열에 포함되어 있습니다. 이 프로바이더들은 메일러, 큐, 캐시 등 핵심 Laravel 컴포넌트들을 부트스트랩합니다. 이 중 상당수는 "지연(deferred) 프로바이더"로 분류되는데, 이는 해당 프로바이더가 매 요청마다 로드되는 것이 아니라, 그 서비스가 실제로 필요할 때만 로드된다는 뜻입니다.

<!-- In this overview, you will learn how to write your own service providers and register them with your Laravel application. -->
이 세션에서는 나만의 서비스 프로바이더를 작성하고, 이를 Laravel 애플리케이션에 등록하는 방법을 알아봅니다.

> [!TIP]
> Laravel이 요청을 어떻게 처리하고 내부적으로 어떻게 동작하는지 더 자세히 알고 싶다면, Laravel [request lifecycle](/docs/8.x/lifecycle) 문서도 참고해보세요.

<a name="writing-service-providers"></a>
<!-- ## Writing Service Providers -->
## Writing Service Providers

<!-- All service providers extend the `Illuminate\Support\ServiceProvider` class. Most service providers contain a `register` and a `boot` method. Within the `register` method, you should **only bind things into the [service container](/docs/8.x/container)**. You should never attempt to register any event listeners, routes, or any other piece of functionality within the `register` method. -->
모든 서비스 프로바이더는 `Illuminate\Support\ServiceProvider` 클래스를 상속합니다. 보통 서비스 프로바이더에는 `register`와 `boot` 두 개의 메서드가 포함됩니다. `register` 메서드 안에서는 **오직 [service container](/docs/8.x/container)에 바인딩만** 해야 합니다. 이벤트 리스너나 라우트, 그 밖의 다른 기능들은 절대 `register` 메서드 안에서 등록하지 않아야 합니다.

<!-- The Artisan CLI can generate a new provider via the `make:provider` command: -->
Artisan CLI의 `make:provider` 명령어를 사용해서 새로운 프로바이더를 만들 수 있습니다.

```
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
<!-- ### The Register Method -->
### The Register Method

<!-- As mentioned previously, within the `register` method, you should only bind things into the [service container](/docs/8.x/container). You should never attempt to register any event listeners, routes, or any other piece of functionality within the `register` method. Otherwise, you may accidentally use a service that is provided by a service provider which has not loaded yet. -->
앞서 설명했듯이, `register` 메서드에서는 오직 [service container](/docs/8.x/container)에 바인딩 작업만 수행해야 합니다. `register` 메서드에서 이벤트 리스너, 라우트, 그 외의 기능을 등록하려고 시도하면 안 됩니다. 그렇지 않으면, 아직 로드되지 않은 다른 서비스 프로바이더에서 제공하는 서비스가 예기치 않게 사용되어 문제가 발생할 수 있습니다.

<!-- Let's take a look at a basic service provider. Within any of your service provider methods, you always have access to the `$app` property which provides access to the service container: -->
아래는 기본적인 서비스 프로바이더 작성 예시입니다. 서비스 프로바이더의 모든 메서드 안에서는 항상 `$app` 프로퍼티에 접근할 수 있으며, 이를 통해 서비스 컨테이너를 사용할 수 있습니다:

```
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->app->singleton(Connection::class, function ($app) {
            return new Connection(config('riak'));
        });
    }
}
```

<!-- This service provider only defines a `register` method, and uses that method to define an implementation of `App\Services\Riak\Connection` in the service container. If you're not yet familiar with Laravel's service container, check out [its documentation](/docs/8.x/container). -->
이 서비스 프로바이더는 오직 `register` 메서드만 정의하며, 이 안에서 `App\Services\Riak\Connection`의 구현체를 서비스 컨테이너에 바인딩합니다. Laravel의 서비스 컨테이너가 익숙하지 않다면, [its documentation](/docs/8.x/container)를 참고해주세요.

<a name="the-bindings-and-singletons-properties"></a>
<!-- #### The `bindings` And `singletons` Properties -->
#### The `bindings` And `singletons` Properties

<!-- If your service provider registers many simple bindings, you may wish to use the `bindings` and `singletons` properties instead of manually registering each container binding. When the service provider is loaded by the framework, it will automatically check for these properties and register their bindings: -->
여러 개의 단순한 바인딩을 서비스 프로바이더에서 등록해야 한다면, 각각을 따로 코드로 작성하는 대신 `bindings`와 `singletons` 프로퍼티를 활용할 수 있습니다. 프레임워크가 서비스 프로바이더를 로드할 때 이 프로퍼티들을 자동으로 확인해서 바인딩을 등록합니다:

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

<!-- So, what if we need to register a [view composer](/docs/8.x/views#view-composers) within our service provider? This should be done within the `boot` method. **This method is called after all other service providers have been registered**, meaning you have access to all other services that have been registered by the framework: -->
그렇다면 서비스 프로바이더 안에서 [view composer](/docs/8.x/views#view-composers)와 같은 기능을 등록해야 할 때는 어떻게 할까요? 이런 경우에는 `boot` 메서드 안에서 처리해야 합니다. **이 메서드는 모든 다른 서비스 프로바이더가 등록된 이후에 실행되므로**, 프레임워크에서 등록된 다른 모든 서비스에 접근할 수 있습니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        View::composer('view', function () {
            //
        });
    }
}
```

<a name="boot-method-dependency-injection"></a>
<!-- #### Boot Method Dependency Injection -->
#### Boot Method Dependency Injection

<!-- You may type-hint dependencies for your service provider's `boot` method. The [service container](/docs/8.x/container) will automatically inject any dependencies you need: -->
서비스 프로바이더의 `boot` 메서드에는 의존성 주입을 사용할 수 있습니다. [service container](/docs/8.x/container)가 필요로 하는 모든 의존성을 자동으로 주입해줍니다:

```
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * Bootstrap any application services.
 *
 * @param  \Illuminate\Contracts\Routing\ResponseFactory  $response
 * @return void
 */
public function boot(ResponseFactory $response)
{
    $response->macro('serialized', function ($value) {
        //
    });
}
```

<a name="registering-providers"></a>
<!-- ## Registering Providers -->
## Registering Providers

<!-- All service providers are registered in the `config/app.php` configuration file. This file contains a `providers` array where you can list the class names of your service providers. By default, a set of Laravel core service providers are listed in this array. These providers bootstrap the core Laravel components, such as the mailer, queue, cache, and others. -->
모든 서비스 프로바이더는 `config/app.php` 설정 파일에 등록합니다. 이 파일 안의 `providers` 배열에 각 서비스 프로바이더 클래스의 이름을 나열할 수 있습니다. 기본적으로 Laravel의 핵심 서비스 프로바이더들이 이 배열에 포함되어 있습니다. 이 프로바이더들은 메일러, 큐, 캐시 등과 같은 핵심 Laravel 컴포넌트들을 부트스트랩합니다.

<!-- To register your provider, add it to the array: -->
나만의 프로바이더를 등록하려면, 아래처럼 배열에 추가하세요:

```
'providers' => [
    // Other Service Providers

    App\Providers\ComposerServiceProvider::class,
],
```

<a name="deferred-providers"></a>
<!-- ## Deferred Providers -->
## Deferred Providers

<!-- If your provider is **only** registering bindings in the [service container](/docs/8.x/container), you may choose to defer its registration until one of the registered bindings is actually needed. Deferring the loading of such a provider will improve the performance of your application, since it is not loaded from the filesystem on every request. -->
프로바이더에서 **오직** [service container](/docs/8.x/container) 바인딩만 등록하는 경우, 실제 바인딩이 필요해질 때까지 프로바이더의 로드를 지연시킬 수 있습니다. 이렇게 하면 파일 시스템에서 해당 프로바이더를 매 요청마다 불러올 필요가 없어, 애플리케이션의 성능이 향상됩니다.

<!-- Laravel compiles and stores a list of all of the services supplied by deferred service providers, along with the name of its service provider class. Then, only when you attempt to resolve one of these services does Laravel load the service provider. -->
Laravel은 지연 서비스 프로바이더가 제공하는 모든 서비스와 서비스 프로바이더 클래스 이름을 컴파일하여 저장합니다. 이후, 이 서비스들 중 하나를 실제로 사용하려고 할 때에만 Laravel이 서비스 프로바이더를 로드합니다.

<!-- To defer the loading of a provider, implement the `\Illuminate\Contracts\Support\DeferrableProvider` interface and define a `provides` method. The `provides` method should return the service container bindings registered by the provider: -->
프로바이더의 로드를 지연시키려면, `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고, `provides` 메서드를 정의하면 됩니다. `provides` 메서드는 이 프로바이더가 등록하는 서비스 컨테이너 바인딩 목록을 반환해야 합니다.

```
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->app->singleton(Connection::class, function ($app) {
            return new Connection($app['config']['riak']);
        });
    }

    /**
     * Get the services provided by the provider.
     *
     * @return array
     */
    public function provides()
    {
        return [Connection::class];
    }
}
```
