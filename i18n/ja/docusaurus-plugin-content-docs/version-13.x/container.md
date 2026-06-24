<!-- # Service Container -->
# Service Container

- [Introduction](#introduction)
    - [Zero Configuration Resolution](#zero-configuration-resolution)
    - [When to Utilize the Container](#when-to-use-the-container)
- [Binding](#binding)
    - [Binding Basics](#binding-basics)
    - [Binding Interfaces to Implementations](#binding-interfaces-to-implementations)
    - [Contextual Binding](#contextual-binding)
    - [Contextual Attributes](#contextual-attributes)
    - [Binding Primitives](#binding-primitives)
    - [Binding Typed Variadics](#binding-typed-variadics)
    - [Tagging](#tagging)
    - [Extending Bindings](#extending-bindings)
- [Resolving](#resolving)
    - [The Make Method](#the-make-method)
    - [Automatic Injection](#automatic-injection)
- [Method Invocation and Injection](#method-invocation-and-injection)
- [Container Events](#container-events)
    - [Rebinding](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The Laravel service container is a powerful tool for managing class dependencies and performing dependency injection. Dependency injection is a fancy phrase that essentially means this: class dependencies are "injected" into the class via the constructor or, in some cases, "setter" methods. -->
Laravel サービスコンテナは、クラスの依存関係を管理し、依存関係の注入を実行するための強力なツールです。依存関係の注入とは、本質的には次のことを意味する派手な表現です。クラスの依存関係は、コンストラクター、または場合によっては「セッター」メソッドを介してクラスに「注入」されます。

<!-- Let's look at a simple example: -->
簡単な例を見てみましょう。

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;
use Illuminate\View\View;

class PodcastController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * Show information about the given podcast.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```

<!-- In this example, the `PodcastController` needs to retrieve podcasts from a data source such as Apple Music. So, we will **inject** a service that is able to retrieve podcasts. Since the service is injected, we are able to easily "mock", or create a dummy implementation of the `AppleMusic` service when testing our application. -->
この例では、`PodcastController` は Apple Music などのデータ ソースからポッドキャストを取得する必要があります。そこで、ポッドキャストを取得できるサービスを**挿入**します。サービスが挿入されるため、アプリケーションをテストするときに、`AppleMusic` サービスのダミー実装を簡単に「モック」または作成できます。

<!-- A deep understanding of the Laravel service container is essential to building a powerful, large application, as well as for contributing to the Laravel core itself. -->
Laravel サービスコンテナを深く理解することは、強力で大規模なアプリケーションを構築するだけでなく、Laravel コア自体に貢献するためにも不可欠です。

<a name="zero-configuration-resolution"></a>
<!-- ### Zero Configuration Resolution -->
### Zero Configuration Resolution

<!-- If a class has no dependencies or only depends on other concrete classes (not interfaces), the container does not need to be instructed on how to resolve that class. For example, you may place the following code in your `routes/web.php` file: -->
クラスに依存関係がない場合、または他の具象クラス (インターフェイスではない) にのみ依存する場合、コンテナーにそのクラスを解決する方法を指示する必要はありません。たとえば、次のコードを `routes/web.php` ファイルに配置できます。

```php
<?php

class Service
{
    // ...
}

Route::get('/', function (Service $service) {
    dd($service::class);
});
```

<!-- In this example, hitting your application's `/` route will automatically resolve the `Service` class and inject it into your route's handler. This is game changing. It means you can develop your application and take advantage of dependency injection without worrying about bloated configuration files. -->
この例では、アプリケーションの `/` ルートにアクセスすると、自動的に `Service` クラスが解決され、それがルートのハンドラーに挿入されます。これはゲームチェンジです。つまり、肥大化した構成ファイルを気にせずにアプリケーションを開発し、依存関係の注入を活用できるということです。

<!-- Thankfully, many of the classes you will be writing when building a Laravel application automatically receive their dependencies via the container, including [controllers](/docs/13.x/controllers), [event listeners](/docs/13.x/events), [middleware](/docs/13.x/middleware), and more. Additionally, you may type-hint dependencies in the `handle` method of [queued jobs](/docs/13.x/queues). Once you taste the power of automatic and zero configuration dependency injection it feels impossible to develop without it. -->
ありがたいことに、Laravel アプリケーションを構築するときに作成するクラスの多くは、[controllers](/docs/13.x/controllers)、[event listeners](/docs/13.x/events)、[middleware](/docs/13.x/middleware) などの依存関係をコンテナ経由で自動的に受け取ります。さらに、[queued jobs](/docs/13.x/queues) の `handle` メソッドで依存関係をタイプヒントすることもできます。自動かつ構成ゼロの依存注入の威力を一度味わってしまうと、それなしで開発することは不可能に感じられます。

<a name="when-to-use-the-container"></a>
<!-- ### When to Utilize the Container -->
### When to Utilize the Container

<!-- Thanks to zero configuration resolution, you will often type-hint dependencies on routes, controllers, event listeners, and elsewhere without ever manually interacting with the container. For example, you might type-hint the `Illuminate\Http\Request` object on your route definition so that you can easily access the current request. Even though we never have to interact with the container to write this code, it is managing the injection of these dependencies behind the scenes: -->
構成解決が不要なため、コンテナーと手動でやり取りすることなく、ルート、コントローラ、イベント リスナなどの依存関係をタイプヒントで確認できるようになります。たとえば、現在のリクエストに簡単にアクセスできるように、ルート定義で `Illuminate\Http\Request` オブジェクトにタイプヒントを指定できます。このコードを記述するためにコンテナーと対話する必要はありませんが、コンテナーはバックグラウンドでこれらの依存関係の注入を管理しています。

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<!-- In many cases, thanks to automatic dependency injection and [facades](/docs/13.x/facades), you can build Laravel applications without **ever** manually binding or resolving anything from the container. **So, when would you ever manually interact with the container?** Let's examine two situations. -->
多くの場合、自動依存注入と [facades](/docs/13.x/facades) のおかげで、コンテナから何も手動でバインドしたり解決したりすることなく、Laravel アプリケーションを構築できます。 **それでは、コンテナを手動で操作するのはどのような場合でしょうか?** 2 つの状況を調べてみましょう。

<!-- First, if you write a class that implements an interface and you wish to type-hint that interface on a route or class constructor, you must [tell the container how to resolve that interface](#binding-interfaces-to-implementations). Secondly, if you are [writing a Laravel package](/docs/13.x/packages) that you plan to share with other Laravel developers, you may need to bind your package's services into the container. -->
まず、インターフェイスを実装するクラスを作成し、ルートまたはクラス コンストラクターでそのインターフェイスをタイプヒントで指定したい場合は、[tell the container how to resolve that interface](#binding-interfaces-to-implementations) を実行する必要があります。次に、他の Laravel 開発者と共有する予定の [writing a Laravel package](/docs/13.x/packages) の場合は、パッケージのサービスをコンテナにバインドする必要がある場合があります。

<a name="binding"></a>
<!-- ## Binding -->
## Binding

<a name="binding-basics"></a>
<!-- ### Binding Basics -->
### Binding Basics

<a name="simple-bindings"></a>
<!-- #### Simple Bindings -->
#### Simple Bindings

<!-- Almost all of your service container bindings will be registered within [service providers](/docs/13.x/providers), so most of these examples will demonstrate using the container in that context. -->
ほとんどすべてのサービスコンテナー バインディングは [service providers](/docs/13.x/providers) 内に登録されるため、これらの例のほとんどは、そのコンテキストでコンテナーを使用する方法を示しています。

<!-- Within a service provider, you always have access to the container via the `$this->app` property. We can register a binding using the `bind` method, passing the class or interface name that we wish to register along with a closure that returns an instance of the class: -->
サービスプロバイダ内では、`$this->app` プロパティを介して常にコンテナーにアクセスできます。 `bind` メソッドを使用してバインディングを登録し、クラスのインスタンスを返すクロージャとともに登録したいクラス名またはインターフェイス名を渡します。

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<!-- Note that we receive the container itself as an argument to the resolver. We can then use the container to resolve sub-dependencies of the object we are building. -->
コンテナ自体をリゾルバーへの引数として受け取ることに注意してください。その後、コンテナを使用して、構築しているオブジェクトのサブ依存関係を解決できます。

<!-- As mentioned, you will typically be interacting with the container within service providers; however, if you would like to interact with the container outside of a service provider, you may do so via the `App` [facade](/docs/13.x/facades): -->
前述したように、通常はサービスプロバイダ内のコンテナーと対話します。ただし、サービスプロバイダの外部でコンテナーと対話したい場合は、`App` [facade](/docs/13.x/facades) 経由で行うことができます。

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

<!-- You may use the `bindIf` method to register a container binding only if a binding has not already been registered for the given type: -->
特定のタイプに対してバインディングがまだ登録されていない場合にのみ、`bindIf` メソッドを使用してコンテナー バインディングを登録できます。

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<!-- For convenience, you may omit providing the class or interface name that you wish to register as a separate argument and instead allow Laravel to infer the type from the return type of the closure you provide to the `bind` method: -->
便宜上、別の引数として登録するクラスまたはインターフェイス名の指定を省略し、代わりに `bind` メソッドに指定したクロージャの戻り値の型から Laravel が型を推測できるようにすることもできます。

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> クラスがインターフェイスに依存しない場合は、クラスをコンテナにバインドする必要はありません。コンテナはリフレクションを使用してこれらのオブジェクトを自動的に解決できるため、これらのオブジェクトの構築方法を指示する必要はありません。

<a name="binding-a-singleton"></a>
<!-- #### Binding A Singleton -->
#### Binding A Singleton

<!-- The `singleton` method binds a class or interface into the container that should only be resolved one time. Once a singleton binding is resolved, the same object instance will be returned on subsequent calls into the container: -->
`singleton` メソッドは、クラスまたはインターフェイスをコンテナーにバインドしますが、解決されるのは 1 回だけです。シングルトン バインディングが解決されると、コンテナへの後続の呼び出しで同じオブジェクト インスタンスが返されます。

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<!-- You may use the `singletonIf` method to register a singleton container binding only if a binding has not already been registered for the given type: -->
特定のタイプに対してバインディングがまだ登録されていない場合にのみ、`singletonIf` メソッドを使用してシングルトン コンテナー バインディングを登録できます。

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="singleton-attribute"></a>
<!-- #### Singleton Attribute -->
#### Singleton Attribute

<!-- Alternatively, you may mark an interface or class with the `#[Singleton]` attribute to indicate to the container that it should be resolved one time: -->
あるいは、インターフェイスまたはクラスを `#[Singleton]` 属性でマークして、一度解決する必要があることをコンテナに示すこともできます。

```php
<?php

namespace App\Services;

use Illuminate\Container\Attributes\Singleton;

#[Singleton]
class Transistor
{
    // ...
}
```

<a name="binding-scoped"></a>
<!-- #### Binding Scoped Singletons -->
#### Binding Scoped Singletons

<!-- The `scoped` method binds a class or interface into the container that should only be resolved one time within a given Laravel request / job lifecycle. While this method is similar to the `singleton` method, instances registered using the `scoped` method will be flushed whenever the Laravel application starts a new "lifecycle", such as when a [Laravel Octane](/docs/13.x/octane) worker processes a new request or when a Laravel [queue worker](/docs/13.x/queues) processes a new job: -->
`scoped` メソッドは、特定の Laravel リクエスト/ジョブのライフサイクル内で 1 回だけ解決されるクラスまたはインターフェイスをコンテナーにバインドします。このメソッドは `singleton` メソッドに似ていますが、`scoped` メソッドを使用して登録されたインスタンスは、[Laravel Octane](/docs/13.x/octane) ワーカーが新しいリクエストを処理するときや、Laravel [queue worker](/docs/13.x/queues) が新しいジョブを処理するときなど、Laravel アプリケーションが新しい「ライフサイクル」を開始するたびにフラッシュされます。

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<!-- You may use the `scopedIf` method to register a scoped container binding only if a binding has not already been registered for the given type: -->
特定のタイプに対してバインディングがまだ登録されていない場合にのみ、`scopedIf` メソッドを使用してスコープ付きコンテナー バインディングを登録できます。

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="scoped-attribute"></a>
<!-- #### Scoped Attribute -->
#### Scoped Attribute

<!-- Alternatively, you may mark an interface or class with the `#[Scoped]` attribute to indicate to the container that it should be resolved one time within a given Laravel request / job lifecycle: -->
あるいは、インターフェイスまたはクラスを `#[Scoped]` 属性でマークして、特定の Laravel リクエスト/ジョブのライフサイクル内で 1 回解決する必要があることをコンテナに示すこともできます。

```php
<?php

namespace App\Services;

use Illuminate\Container\Attributes\Scoped;

#[Scoped]
class Transistor
{
    // ...
}
```

<a name="binding-instances"></a>
<!-- #### Binding Instances -->
#### Binding Instances

<!-- You may also bind an existing object instance into the container using the `instance` method. The given instance will always be returned on subsequent calls into the container: -->
`instance` メソッドを使用して、既存のオブジェクト インスタンスをコンテナにバインドすることもできます。指定されたインスタンスは、コンテナへの後続の呼び出しで常に返されます。

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
<!-- ### Binding Interfaces to Implementations -->
### Binding Interfaces to Implementations

<!-- A very powerful feature of the service container is its ability to bind an interface to a given implementation. For example, let's assume we have an `EventPusher` interface and a `RedisEventPusher` implementation. Once we have coded our `RedisEventPusher` implementation of this interface, we can register it with the service container like so: -->
サービスコンテナの非常に強力な機能は、インターフェイスを特定の実装にバインドできることです。たとえば、`EventPusher` インターフェイスと `RedisEventPusher` 実装があると仮定します。このインターフェースの `RedisEventPusher` 実装をコーディングしたら、次のようにサービスコンテナーに登録できます。

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

<!-- This statement tells the container that it should inject the `RedisEventPusher` when a class needs an implementation of `EventPusher`. Now we can type-hint the `EventPusher` interface in the constructor of a class that is resolved by the container. Remember, controllers, event listeners, middleware, and various other types of classes within Laravel applications are always resolved using the container: -->
このステートメントは、クラスが `EventPusher` の実装を必要とする場合に、`RedisEventPusher` を注入する必要があることをコンテナーに指示します。これで、コンテナーによって解決されるクラスのコンストラクターで `EventPusher` インターフェイスをタイプヒントできるようになりました。 Laravel アプリケーション内のコントローラ、イベントリスナ、ミドルウェア、その他のさまざまなタイプのクラスは、常にコンテナーを使用して解決されることに注意してください。

```php
use App\Contracts\EventPusher;

/**
 * Create a new class instance.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```

<a name="bind-attribute"></a>
<!-- #### Bind Attribute -->
#### Bind Attribute

<!-- Laravel also provides a `Bind` attribute for added convenience. You can apply this attribute to any interface to tell Laravel which implementation should be automatically injected whenever that interface is requested. When using the `Bind` attribute, there is no need to perform any additional service registration in your application's service providers. -->
Laravel は、利便性を高めるために `Bind` 属性も提供します。この属性を任意のインターフェイスに適用して、そのインターフェイスがリクエストされるたびにどの実装を自動的に挿入するかを Laravel に指示できます。 `Bind` 属性を使用する場合、アプリケーションのサービスプロバイダで追加のサービス登録を実行する必要はありません。

<!-- In addition, multiple `Bind` attributes may be placed on an interface in order to configure a different implementation that should be injected for a given set of environments: -->
さらに、特定の環境セットに注入する必要がある別の実装を構成するために、複数の `Bind` 属性をインターフェイスに配置することもできます。

```php
<?php

namespace App\Contracts;

use App\Services\FakeEventPusher;
use App\Services\RedisEventPusher;
use Illuminate\Container\Attributes\Bind;

#[Bind(RedisEventPusher::class)]
#[Bind(FakeEventPusher::class, environments: ['local', 'testing'])]
interface EventPusher
{
    // ...
}
```

<!-- Furthermore, [Singleton](#singleton-attribute) and [Scoped](#scoped-attribute) attributes may be applied to indicate if the container bindings should be resolved once or once per request / job lifecycle: -->
さらに、[Singleton](#singleton-attribute) 属性と [Scoped](#scoped-attribute) 属性を適用して、コンテナーのバインディングを 1 回解決するか、リクエスト/ジョブのライフサイクルごとに 1 回解決するかを示すことができます。

```php
use App\Services\RedisEventPusher;
use Illuminate\Container\Attributes\Bind;
use Illuminate\Container\Attributes\Singleton;

#[Bind(RedisEventPusher::class)]
#[Singleton]
interface EventPusher
{
    // ...
}
```

<a name="contextual-binding"></a>
<!-- ### Contextual Binding -->
### Contextual Binding

<!-- Sometimes you may have two classes that utilize the same interface, but you wish to inject different implementations into each class. For example, two controllers may depend on different implementations of the `Illuminate\Contracts\Filesystem\Filesystem` [contract](/docs/13.x/contracts). Laravel provides a simple, fluent interface for defining this behavior: -->
同じインターフェイスを利用する 2 つのクラスがあり、各クラスに異なる実装を挿入したい場合があります。たとえば、2 つのコントローラが `Illuminate\Contracts\Filesystem\Filesystem` [contract](/docs/13.x/contracts) の異なる実装に依存している場合があります。 Laravel は、この動作を定義するためのシンプルで流暢なインターフェイスを提供します。

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\UploadController;
use App\Http\Controllers\VideoController;
use Illuminate\Contracts\Filesystem\Filesystem;
use Illuminate\Support\Facades\Storage;

$this->app->when(PhotoController::class)
    ->needs(Filesystem::class)
    ->give(function () {
        return Storage::disk('local');
    });

$this->app->when([VideoController::class, UploadController::class])
    ->needs(Filesystem::class)
    ->give(function () {
        return Storage::disk('s3');
    });
```

<a name="contextual-attributes"></a>
<!-- ### Contextual Attributes -->
### Contextual Attributes

<!-- Since contextual binding is often used to inject implementations of drivers or configuration values, Laravel offers a variety of contextual binding attributes that allow to inject these types of values without manually defining the contextual bindings in your service providers. -->
コンテキストバインディングは、ドライバや設定値の実装を挿入するためによく使用されるため、Laravel は、サービスプロバイダでコンテキストバインディングを手動で定義しなくても、これらのタイプの値を注入できるようにするさまざまなコンテキストバインディング属性を提供します。

<!-- For example, the `Storage` attribute may be used to inject a specific [storage disk](/docs/13.x/filesystem): -->
たとえば、`Storage` 属性を使用して、特定の [storage disk](/docs/13.x/filesystem) を挿入できます。

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Container\Attributes\Storage;
use Illuminate\Contracts\Filesystem\Filesystem;

class PhotoController extends Controller
{
    public function __construct(
        #[Storage('local')] protected Filesystem $filesystem
    ) {
        // ...
    }
}
```

<!-- In addition to the `Storage` attribute, Laravel offers `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RouteParameter`, and [Tag](#tagging) attributes: -->
`Storage` 属性に加えて、Laravel は `Auth`、`Cache`、`Config`、`Context`、`DB`、`Give`、`Log`、`RouteParameter`、および [Tag](#tagging) 属性を提供します:

```php
<?php

namespace App\Http\Controllers;

use App\Contracts\UserRepository;
use App\Models\Photo;
use App\Repositories\DatabaseRepository;
use Illuminate\Container\Attributes\Auth;
use Illuminate\Container\Attributes\Cache;
use Illuminate\Container\Attributes\Config;
use Illuminate\Container\Attributes\Context;
use Illuminate\Container\Attributes\DB;
use Illuminate\Container\Attributes\Give;
use Illuminate\Container\Attributes\Log;
use Illuminate\Container\Attributes\RouteParameter;
use Illuminate\Container\Attributes\Tag;
use Illuminate\Contracts\Auth\Guard;
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Database\Connection;
use Psr\Log\LoggerInterface;

class PhotoController extends Controller
{
    public function __construct(
        #[Auth('web')] protected Guard $auth,
        #[Cache('redis')] protected Repository $cache,
        #[Config('app.timezone')] protected string $timezone,
        #[Context('uuid')] protected string $uuid,
        #[Context('ulid', hidden: true)] protected string $ulid,
        #[DB('mysql')] protected Connection $connection,
        #[Give(DatabaseRepository::class)] protected UserRepository $users,
        #[Log('daily')] protected LoggerInterface $log,
        #[RouteParameter] protected Photo $photo,
        #[Tag('reports')] protected iterable $reports,
    ) {
        // ...
    }
}
```

<!-- The `RouteParameter` attribute will resolve the route parameter matching the variable name. If needed, you may specify the route parameter name explicitly: `#[RouteParameter('photo')]`. -->
`RouteParameter` 属性は、変数名に一致するルートパラメータを解決します。必要であれば、ルートパラメータ名を明示的に指定できます: `#[RouteParameter('photo')]`。

<!-- In addition, Laravel provides a `CurrentUser` attribute for injecting the currently authenticated user into a given route or class: -->
さらに、Laravel は、現在認証されているユーザーを特定のルートまたはクラスに注入するための `CurrentUser` 属性を提供します。

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
<!-- #### Defining Custom Attributes -->
#### Defining Custom Attributes

<!-- You can create your own contextual attributes by implementing the `Illuminate\Contracts\Container\ContextualAttribute` contract. The container will call your attribute's `resolve` method, which should resolve the value that should be injected into the class utilizing the attribute. In the example below, we will re-implement Laravel's built-in `Config` attribute: -->
`Illuminate\Contracts\Container\ContextualAttribute` コントラクトを実装することで、独自のコンテキスト属性を作成できます。コンテナーは属性の `resolve` メソッドを呼び出します。これにより、属性を利用してクラスに注入される値が解決されます。以下の例では、Laravel の組み込み `Config` 属性を再実装します。

```php
<?php

namespace App\Attributes;

use Attribute;
use Illuminate\Contracts\Container\Container;
use Illuminate\Contracts\Container\ContextualAttribute;
use ReflectionParameter;

#[Attribute(Attribute::TARGET_PARAMETER)]
class Config implements ContextualAttribute
{
    /**
     * Create a new attribute instance.
     */
    public function __construct(public string $key, public mixed $default = null)
    {
    }

    /**
     * Resolve the configuration value.
     *
     * @param  self  $attribute
     * @param  \Illuminate\Contracts\Container\Container  $container
     * @param  \ReflectionParameter  $parameter
     * @return mixed
     */
    public static function resolve(self $attribute, Container $container, ReflectionParameter $parameter)
    {
        return $container->make('config')->get($attribute->key, $attribute->default);
    }
}
```

<a name="binding-primitives"></a>
<!-- ### Binding Primitives -->
### Binding Primitives

<!-- Sometimes you may have a class that receives some injected classes, but also needs an injected primitive value such as an integer. You may easily use contextual binding to inject any value your class may need: -->
場合によっては、注入されたクラスを受け取るクラスが、整数などの注入されたプリミティブ値も必要とする場合があります。コンテキスト バインディングを使用して、クラスに必要な値を簡単に注入できます。

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

<!-- Sometimes a class may depend on an array of [tagged](#tagging) instances. Using the `giveTagged` method, you may easily inject all of the container bindings with that tag: -->
クラスが [tagged](#tagging) インスタンスの配列に依存する場合があります。 `giveTagged` メソッドを使用すると、そのタグを含むすべてのコンテナー バインディングを簡単に挿入できます。

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

<!-- If you need to inject a value from one of your application's configuration files, you may use the `giveConfig` method: -->
アプリケーションの構成ファイルの 1 つから値を挿入する必要がある場合は、`giveConfig` メソッドを使用できます。

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
<!-- ### Binding Typed Variadics -->
### Binding Typed Variadics

<!-- Occasionally, you may have a class that receives an array of typed objects using a variadic constructor argument: -->
場合によっては、可変長コンストラクター引数を使用して型指定されたオブジェクトの配列を受け取るクラスがある場合があります。

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * The filter instances.
     *
     * @var array
     */
    protected $filters;

    /**
     * Create a new class instance.
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```

<!-- Using contextual binding, you may resolve this dependency by providing the `give` method with a closure that returns an array of resolved `Filter` instances: -->
コンテキスト バインディングを使用すると、解決された `Filter` インスタンスの配列を返すクロージャを `give` メソッドに提供することで、この依存関係を解決できます。

```php
$this->app->when(Firewall::class)
    ->needs(Filter::class)
    ->give(function (Application $app) {
          return [
              $app->make(NullFilter::class),
              $app->make(ProfanityFilter::class),
              $app->make(TooLongFilter::class),
          ];
    });
```

<!-- For convenience, you may also just provide an array of class names to be resolved by the container whenever `Firewall` needs `Filter` instances: -->
便宜上、`Firewall` が `Filter` インスタンスを必要とするときに、コンテナーによって解決されるクラス名の配列を指定することもできます。

```php
$this->app->when(Firewall::class)
    ->needs(Filter::class)
    ->give([
        NullFilter::class,
        ProfanityFilter::class,
        TooLongFilter::class,
    ]);
```

<a name="variadic-tag-dependencies"></a>
<!-- #### Variadic Tag Dependencies -->
#### Variadic Tag Dependencies

<!-- Sometimes a class may have a variadic dependency that is type-hinted as a given class (`Report ...$reports`). Using the `needs` and `giveTagged` methods, you may easily inject all of the container bindings with that [tag](#tagging) for the given dependency: -->
場合によっては、クラスに、特定のクラス (`Report ...$reports`) としてタイプヒントされる可変個引数の依存関係がある場合があります。 `needs` メソッドと `giveTagged` メソッドを使用すると、指定された依存関係の [tag](#tagging) を持つすべてのコンテナー バインディングを簡単に注入できます。

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
<!-- ### Tagging -->
### Tagging

<!-- Occasionally, you may need to resolve all of a certain "category" of binding. For example, perhaps you are building a report analyzer that receives an array of many different `Report` interface implementations. After registering the `Report` implementations, you can assign them a tag using the `tag` method: -->
場合によっては、バインディングの特定の「カテゴリ」をすべて解決する必要がある場合があります。たとえば、さまざまな `Report` インターフェイス実装の配列を受け取るレポート アナライザーを構築しているとします。 `Report` 実装を登録した後、`tag` メソッドを使用してタグを割り当てることができます。

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

<!-- Once the services have been tagged, you may easily resolve them all via the container's `tagged` method: -->
サービスにタグを付けたら、コンテナーの `tagged` メソッドを使用してすべてを簡単に解決できます。

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
<!-- ### Extending Bindings -->
### Extending Bindings

<!-- The `extend` method allows the modification of resolved services. For example, when a service is resolved, you may run additional code to decorate or configure the service. The `extend` method accepts two arguments, the service class you're extending and a closure that should return the modified service. The closure receives the service being resolved and the container instance: -->
`extend` メソッドを使用すると、解決されたサービスを変更できます。たとえば、サービスが解決されると、追加のコードを実行してサービスを修飾または構成することができます。 `extend` メソッドは、拡張するサービス クラスと、変更されたサービスを返すクロージャの 2 つの引数を受け入れます。クロージャーは、解決されるサービスとコンテナー インスタンスを受け取ります。

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
<!-- ## Resolving -->
## Resolving

<a name="the-make-method"></a>
<!-- ### The `make` Method -->
### The `make` Method

<!-- You may use the `make` method to resolve a class instance from the container. The `make` method accepts the name of the class or interface you wish to resolve: -->
`make` メソッドを使用して、コンテナからクラス インスタンスを解決できます。 `make` メソッドは、解決するクラスまたはインターフェイスの名前を受け入れます。

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

<!-- If some of your class's dependencies are not resolvable via the container, you may inject them by passing them as an associative array into the `makeWith` method. For example, we may manually pass the `$id` constructor argument required by the `Transistor` service: -->
クラスの依存関係の一部がコンテナー経由で解決できない場合は、それらを連想配列として `makeWith` メソッドに渡すことによって注入できます。たとえば、`Transistor` サービスに必要な `$id` コンストラクター引数を手動で渡すことができます。

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

<!-- The `bound` method may be used to determine if a class or interface has been explicitly bound in the container: -->
`bound` メソッドは、クラスまたはインターフェイスがコンテナ内で明示的にバインドされているかどうかを判断するために使用できます。

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

<!-- If you are outside of a service provider in a location of your code that does not have access to the `$app` variable, you may use the `App` [facade](/docs/13.x/facades) or the `app` [helper](/docs/13.x/helpers#method-app) to resolve a class instance from the container: -->
サービスプロバイダの外部で、`$app` 変数にアクセスできないコードの場所にいる場合は、`App` [facade](/docs/13.x/facades) または `app` [helper](/docs/13.x/helpers#method-app) を使用して、コンテナーからクラス インスタンスを解決できます。

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

<!-- If you would like to have the Laravel container instance itself injected into a class that is being resolved by the container, you may type-hint the `Illuminate\Container\Container` class on your class's constructor: -->
Laravel コンテナインスタンス自体を、コンテナによって解決されるクラスに挿入したい場合は、クラスのコンストラクタで `Illuminate\Container\Container` クラスをタイプヒントできます。

```php
use Illuminate\Container\Container;

/**
 * Create a new class instance.
 */
public function __construct(
    protected Container $container,
) {}
```

<a name="automatic-injection"></a>
<!-- ### Automatic Injection -->
### Automatic Injection

<!-- Alternatively, and importantly, you may type-hint the dependency in the constructor of a class that is resolved by the container, including [controllers](/docs/13.x/controllers), [event listeners](/docs/13.x/events), [middleware](/docs/13.x/middleware), and more. Additionally, you may type-hint dependencies in the `handle` method of [queued jobs](/docs/13.x/queues). In practice, this is how most of your objects should be resolved by the container. -->
あるいは、重要なことですが、[controllers](/docs/13.x/controllers)、[event listeners](/docs/13.x/events)、[middleware](/docs/13.x/middleware) など、コンテナーによって解決されるクラスのコンストラクター内の依存関係をタイプヒントで指定することもできます。さらに、[queued jobs](/docs/13.x/queues) の `handle` メソッドで依存関係をタイプヒントすることもできます。実際には、これがほとんどのオブジェクトがコンテナによって解決される方法です。

<!-- For example, you may type-hint a service defined by your application in a controller's constructor. The service will automatically be resolved and injected into the class: -->
たとえば、アプリケーションによってコントローラのコンストラクターで定義されたサービスをタイプヒントで指定できます。サービスは自動的に解決され、クラスに挿入されます。

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;

class PodcastController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * Show information about the given podcast.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```

<a name="method-invocation-and-injection"></a>
<!-- ## Method Invocation and Injection -->
## Method Invocation and Injection

<!-- Sometimes you may wish to invoke a method on an object instance while allowing the container to automatically inject that method's dependencies. For example, given the following class: -->
場合によっては、コンテナーがそのメソッドの依存関係を自動的に挿入できるようにしながら、オブジェクト インスタンスでメソッドを呼び出したい場合があります。たとえば、次のクラスがあるとします。

```php
<?php

namespace App;

use App\Services\AppleMusic;

class PodcastStats
{
    /**
     * Generate a new podcast stats report.
     */
    public function generate(AppleMusic $apple): array
    {
        return [
            // ...
        ];
    }
}
```

<!-- You may invoke the `generate` method via the container like so: -->
次のようにコンテナ経由で `generate` メソッドを呼び出すことができます。

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

<!-- The `call` method accepts any PHP callable. The container's `call` method may even be used to invoke a closure while automatically injecting its dependencies: -->
`call` メソッドは、任意の PHP 呼び出し可能メソッドを受け入れます。コンテナーの `call` メソッドを使用して、依存関係を自動的に注入しながらクロージャーを呼び出すこともできます。

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
<!-- ## Container Events -->
## Container Events

<!-- The service container fires an event each time it resolves an object. You may listen to this event using the `resolving` method: -->
サービスコンテナは、オブジェクトを解決するたびにイベントを起動します。 `resolving` メソッドを使用して、このイベントをリッスンできます。

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // Called when container resolves objects of type "Transistor"...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // Called when container resolves object of any type...
});
```

<!-- As you can see, the object being resolved will be passed to the callback, allowing you to set any additional properties on the object before it is given to its consumer. -->
ご覧のとおり、解決されるオブジェクトはコールバックに渡されるため、コンシューマーに渡される前にオブジェクトに追加のプロパティを設定できるようになります。

<a name="rebinding"></a>
<!-- ### Rebinding -->
### Rebinding

<!-- The `rebinding` method allows you to listen for when a service is re-bound to the container, meaning it is registered again or overridden after its initial binding. This can be useful when you need to update dependencies or modify behavior each time a specific binding is updated: -->
`rebinding` メソッドを使用すると、サービスがコンテナに再バインドされたとき、つまり最初のバインド後に再登録またはオーバーライドされたときをリッスンできます。これは、特定のバインディングが更新されるたびに依存関係を更新したり、動作を変更したりする必要がある場合に役立ちます。

```php
use App\Contracts\PodcastPublisher;
use App\Services\SpotifyPublisher;
use App\Services\TransistorPublisher;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(PodcastPublisher::class, SpotifyPublisher::class);

$this->app->rebinding(
    PodcastPublisher::class,
    function (Application $app, PodcastPublisher $newInstance) {
        //
    },
);

// New binding will trigger rebinding closure...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
<!-- ## PSR-11 -->
## PSR-11

<!-- Laravel's service container implements the [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) interface. Therefore, you may type-hint the PSR-11 container interface to obtain an instance of the Laravel container: -->
Laravelのサービスコンテナは[PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md)インターフェースを実装しています。したがって、PSR-11 コンテナ インターフェイスにタイプヒントを入力して、Laravel コンテナのインスタンスを取得できます。

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

<!-- An exception is thrown if the given identifier can't be resolved. The exception will be an instance of `Psr\Container\NotFoundExceptionInterface` if the identifier was never bound. If the identifier was bound but was unable to be resolved, an instance of `Psr\Container\ContainerExceptionInterface` will be thrown. -->
指定された識別子を解決できない場合は、例外がスローされます。識別子がバインドされていない場合、例外は `Psr\Container\NotFoundExceptionInterface` のインスタンスになります。識別子がバインドされているが解決できなかった場合、`Psr\Container\ContainerExceptionInterface` のインスタンスがスローされます。

