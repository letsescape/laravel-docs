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
サービスプロバイダは、すべての Laravel アプリケーションのブートストラップの中心的な場所です。独自のアプリケーションと Laravel のすべてのコア サービスは、サービスプロバイダを通じてブートストラップされます。

<!-- But, what do we mean by "bootstrapped"? In general, we mean **registering** things, including registering service container bindings, event listeners, middleware, and even routes. Service providers are the central place to configure your application. -->
しかし、「ブートストラップ」とは何を意味するのでしょうか?一般に、サービスコンテナ バインディング、イベント リスナ、ミドルウェア、さらにはルートの登録を含む、**登録** を意味します。サービスプロバイダは、アプリケーションを構成する中心的な場所です。

<!-- Laravel uses dozens of service providers internally to bootstrap its core services, such as the mailer, queue, cache, and others. Many of these providers are "deferred" providers, meaning they will not be loaded on every request, but only when the services they provide are actually needed. -->
Laravel は、メーラー、キュー、キャッシュなどのコア サービスをブートストラップするために内部で数十のサービスプロバイダを使用しています。これらのプロバイダの多くは「遅延」プロバイダです。つまり、プロバイダはすべてのリクエストでロードされるのではなく、提供するサービスが実際に必要な場合にのみロードされます。

<!-- All user-defined service providers are registered in the `bootstrap/providers.php` file. In the following documentation, you will learn how to write your own service providers and register them with your Laravel application. -->
すべてのユーザー定義のサービスプロバイダは、`bootstrap/providers.php` ファイルに登録されます。次のドキュメントでは、独自のサービスプロバイダを作成し、Laravel アプリケーションに登録する方法を学習します。

> [!NOTE]
> Laravel がどのようにリクエストを処理し、内部で動作するかについて詳しく知りたい場合は、Laravel [request lifecycle](/docs/11.x/lifecycle) のドキュメントを確認してください。

<a name="writing-service-providers"></a>
<!-- ## Writing Service Providers -->
## Writing Service Providers

<!-- All service providers extend the `Illuminate\Support\ServiceProvider` class. Most service providers contain a `register` and a `boot` method. Within the `register` method, you should **only bind things into the [service container](/docs/11.x/container)**. You should never attempt to register any event listeners, routes, or any other piece of functionality within the `register` method. -->
すべてのサービスプロバイダは、`Illuminate\Support\ServiceProvider` クラスを拡張します。ほとんどのサービスプロバイダには、`register` メソッドと `boot` メソッドが含まれています。 `register` メソッド内では、**[service container](/docs/11.x/container) にのみバインドする必要があります**。 `register` メソッド内でイベント リスナ、ルート、またはその他の機能を登録しようとしないでください。

<!-- The Artisan CLI can generate a new provider via the `make:provider` command. Laravel will automatically register your new provider in your application's `bootstrap/providers.php` file: -->
Artisan CLI は、`make:provider` コマンドを使用して新しいプロバイダを生成できます。 Laravel は、アプリケーションの `bootstrap/providers.php` ファイルに新しいプロバイダを自動的に登録します。

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
<!-- ### The Register Method -->
### The Register Method

<!-- As mentioned previously, within the `register` method, you should only bind things into the [service container](/docs/11.x/container). You should never attempt to register any event listeners, routes, or any other piece of functionality within the `register` method. Otherwise, you may accidentally use a service that is provided by a service provider which has not loaded yet. -->
前述したように、`register` メソッド内では、[service container](/docs/11.x/container) にのみバインドする必要があります。 `register` メソッド内にイベント リスナ、ルート、またはその他の機能を登録しようとしないでください。そうしないと、まだロードされていないサービスプロバイダが提供するサービスを誤って使用してしまう可能性があります。

<!-- Let's take a look at a basic service provider. Within any of your service provider methods, you always have access to the `$app` property which provides access to the service container: -->
基本的なサービスプロバイダを見てみましょう。どのサービスプロバイダ メソッド内でも、サービスコンテナーへのアクセスを提供する `$app` プロパティに常にアクセスできます。

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
このサービスプロバイダは、`register` メソッドのみを定義し、そのメソッドを使用してサービスコンテナー内の `App\Services\Riak\Connection` の実装を定義します。 Laravel のサービスコンテナにまだ慣れていない場合は、[its documentation](/docs/11.x/container) を確認してください。

<a name="the-bindings-and-singletons-properties"></a>
<!-- #### The `bindings` and `singletons` Properties -->
#### The `bindings` and `singletons` Properties

<!-- If your service provider registers many simple bindings, you may wish to use the `bindings` and `singletons` properties instead of manually registering each container binding. When the service provider is loaded by the framework, it will automatically check for these properties and register their bindings: -->
サービスプロバイダが多数の単純なバインディングを登録する場合は、各コンテナー バインディングを手動で登録する代わりに、`bindings` プロパティと `singletons` プロパティを使用することをお勧めします。サービスプロバイダがフレームワークによって読み込まれると、これらのプロパティが自動的にチェックされ、そのバインディングが登録されます。

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
では、サービスプロバイダ内で [view composer](/docs/11.x/views#view-composers) を登録する必要がある場合はどうすればよいでしょうか?これは、`boot` メソッド内で実行する必要があります。 **このメソッドは、他のすべてのサービスプロバイダが登録された後に呼び出されます**。これは、フレームワークによって登録されている他のすべてのサービスにアクセスできることを意味します。

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
サービスプロバイダの `boot` メソッドの依存関係をタイプヒントで指定できます。 [service container](/docs/11.x/container) は、必要な依存関係を自動的に挿入します。

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
すべてのサービスプロバイダは、`bootstrap/providers.php` 構成ファイルに登録されます。このファイルは、アプリケーションのサービスプロバイダのクラス名を含む配列を返します。

```
<?php

return [
    App\Providers\AppServiceProvider::class,
];
```

<!-- When you invoke the `make:provider` Artisan command, Laravel will automatically add the generated provider to the `bootstrap/providers.php` file. However, if you have manually created the provider class, you should manually add the provider class to the array: -->
`make:provider` Artisan コマンドを呼び出すと、Laravel は生成されたプロバイダを `bootstrap/providers.php` ファイルに自動的に追加します。ただし、プロバイダ クラスを手動で作成した場合は、プロバイダ クラスを配列に手動で追加する必要があります。

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
プロバイダが [service container](/docs/11.x/container) にバインディングを**のみ**登録している場合は、登録されたバインディングの 1 つが実際に必要になるまで登録を延期することを選択できます。このようなプロバイダのロードを延期すると、リクエストごとにプロバイダがファイルシステムからロードされるわけではないため、アプリケーションのパフォーマンスが向上します。

<!-- Laravel compiles and stores a list of all of the services supplied by deferred service providers, along with the name of its service provider class. Then, only when you attempt to resolve one of these services does Laravel load the service provider. -->
Laravel は、遅延サービスプロバイダによって提供されるすべてのサービスのリストを、そのサービスプロバイダクラスの名前とともにコンパイルして保存します。その後、これらのサービスのいずれかを解決しようとした場合にのみ、Laravel はサービスプロバイダを読み込みます。

<!-- To defer the loading of a provider, implement the `\Illuminate\Contracts\Support\DeferrableProvider` interface and define a `provides` method. The `provides` method should return the service container bindings registered by the provider: -->
プロバイダの読み込みを延期するには、`\Illuminate\Contracts\Support\DeferrableProvider` インターフェイスを実装し、`provides` メソッドを定義します。 `provides` メソッドは、プロバイダによって登録されたサービスコンテナー バインディングを返す必要があります。

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

