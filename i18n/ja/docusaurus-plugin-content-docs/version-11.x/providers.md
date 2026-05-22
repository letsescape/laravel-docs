# サービスプロバイダ (Service Providers)

- [Introduction](#introduction)
- [書き込みサービスプロバイダ](#writing-service-providers)
    - [登録メソッド](#the-register-method)
    - [ブート方法](#the-boot-method)
- [プロバイダの登録](#registering-providers)
- [遅延プロバイダ](#deferred-providers)

<a name="introduction"></a>
## 導入 (Introduction)

サービスプロバイダは、すべての Laravel アプリケーションのブートストラップの中心的な場所です。独自のアプリケーションと Laravel のすべてのコア サービスは、サービスプロバイダを通じてブートストラップされます。

しかし、「ブートストラップ」とは何を意味するのでしょうか?一般に、サービスコンテナ バインディング、イベント リスナ、ミドルウェア、さらにはルートの登録を含む、**登録** を意味します。サービスプロバイダは、アプリケーションを構成する中心的な場所です。

Laravel は、メーラー、キュー、キャッシュなどのコア サービスをブートストラップするために内部で数十のサービスプロバイダを使用しています。これらのプロバイダの多くは「遅延」プロバイダです。つまり、プロバイダはすべてのリクエストでロードされるのではなく、提供するサービスが実際に必要な場合にのみロードされます。

すべてのユーザー定義のサービスプロバイダは、`bootstrap/providers.php` ファイルに登録されます。次のドキュメントでは、独自のサービスプロバイダを作成し、Laravel アプリケーションに登録する方法を学習します。

> [!NOTE]  
> Laravel がどのようにリクエストを処理し、内部で動作するかについて詳しく知りたい場合は、Laravel [リクエストのライフサイクル](/docs/{{version}}/lifecycle) のドキュメントを確認してください。

<a name="writing-service-providers"></a>
## 書き込みサービスプロバイダ (Writing Service Providers)

すべてのサービスプロバイダは、`Illuminate\Support\ServiceProvider` クラスを拡張します。ほとんどのサービスプロバイダには、`register` メソッドと `boot` メソッドが含まれています。 `register` メソッド内では、**[サービスコンテナ](/docs/{{version}}/container) にのみバインドする必要があります**。 `register` メソッド内でイベント リスナ、ルート、またはその他の機能を登録しようとしないでください。

Artisan CLI は、`make:provider` コマンドを使用して新しいプロバイダを生成できます。 Laravel は、アプリケーションの `bootstrap/providers.php` ファイルに新しいプロバイダを自動的に登録します。

```shell
php artisan make:provider RiakServiceProvider
```

<a name="the-register-method"></a>
### 登録メソッド

前述したように、`register` メソッド内では、[サービスコンテナ](/docs/{{version}}/container) にのみバインドする必要があります。 `register` メソッド内にイベント リスナ、ルート、またはその他の機能を登録しようとしないでください。そうしないと、まだロードされていないサービスプロバイダが提供するサービスを誤って使用してしまう可能性があります。

基本的なサービスプロバイダを見てみましょう。どのサービスプロバイダ メソッド内でも、サービスコンテナーへのアクセスを提供する `$app` プロパティに常にアクセスできます。

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

このサービスプロバイダは、`register` メソッドのみを定義し、そのメソッドを使用してサービスコンテナー内の `App\Services\Riak\Connection` の実装を定義します。 Laravel のサービスコンテナにまだ慣れていない場合は、[そのドキュメント](/docs/{{version}}/container) を確認してください。

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings` および `singletons` プロパティ

サービスプロバイダが多数の単純なバインディングを登録する場合は、各コンテナー バインディングを手動で登録する代わりに、`bindings` プロパティと `singletons` プロパティを使用することをお勧めします。サービスプロバイダがフレームワークによって読み込まれると、これらのプロパティが自動的にチェックされ、そのバインディングが登録されます。

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

<a name="the-boot-method"></a>
### ブート方法

では、サービスプロバイダ内で [コンポーザーを表示](/docs/{{version}}/views#view-composers) を登録する必要がある場合はどうすればよいでしょうか?これは、`boot` メソッド内で実行する必要があります。 **このメソッドは、他のすべてのサービスプロバイダが登録された後に呼び出されます**。これは、フレームワークによって登録されている他のすべてのサービスにアクセスできることを意味します。

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

<a name="boot-method-dependency-injection"></a>
#### ブートメソッドの依存関係の注入

サービスプロバイダの `boot` メソッドの依存関係をタイプヒントで指定できます。 [サービスコンテナ](/docs/{{version}}/container) は、必要な依存関係を自動的に挿入します。

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

<a name="registering-providers"></a>
## プロバイダの登録 (Registering Providers)

すべてのサービスプロバイダは、`bootstrap/providers.php` 構成ファイルに登録されます。このファイルは、アプリケーションのサービスプロバイダのクラス名を含む配列を返します。

    <?php

    return [
        App\Providers\AppServiceProvider::class,
    ];

`make:provider` Artisan コマンドを呼び出すと、Laravel は生成されたプロバイダを `bootstrap/providers.php` ファイルに自動的に追加します。ただし、プロバイダ クラスを手動で作成した場合は、プロバイダ クラスを配列に手動で追加する必要があります。

    <?php

    return [
        App\Providers\AppServiceProvider::class,
        App\Providers\ComposerServiceProvider::class, // [tl! add]
    ];

<a name="deferred-providers"></a>
## 遅延プロバイダ (Deferred Providers)

プロバイダが [サービスコンテナ](/docs/{{version}}/container) にバインディングを**のみ**登録している場合は、登録されたバインディングの 1 つが実際に必要になるまで登録を延期することを選択できます。このようなプロバイダのロードを延期すると、リクエストごとにプロバイダがファイルシステムからロードされるわけではないため、アプリケーションのパフォーマンスが向上します。

Laravel は、遅延サービスプロバイダによって提供されるすべてのサービスのリストを、そのサービスプロバイダクラスの名前とともにコンパイルして保存します。その後、これらのサービスのいずれかを解決しようとした場合にのみ、Laravel はサービスプロバイダを読み込みます。

プロバイダの読み込みを延期するには、`\Illuminate\Contracts\Support\DeferrableProvider` インターフェイスを実装し、`provides` メソッドを定義します。 `provides` メソッドは、プロバイダによって登録されたサービスコンテナー バインディングを返す必要があります。

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

