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
Laravel의 서비스 컨테이너는 클래스 간의 의존성을 관리하고, 의존성 주입(dependency injection)을 수행하는 데 매우 강력한 도구입니다. 의존성 주입이란, 클래스가 필요로 하는 의존성 객체를 생성자 혹은 일부 경우 ‘세터(setter)’ 메서드를 통해 “주입”하는 방식입니다.

<!-- Let's look at a simple example: -->
간단한 예제를 살펴보겠습니다:

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
이 예제에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 podcast를 가져올 필요가 있습니다. 이를 위해, podcast를 가져올 수 있는 서비스를 **주입**합니다. 서비스를 주입받으면, 애플리케이션을 테스트할 때 `AppleMusic` 서비스의 모조(mock) 객체나 테스트용 구현체로 쉽게 대체할 수 있습니다.

<!-- A deep understanding of the Laravel service container is essential to building a powerful, large application, as well as for contributing to the Laravel core itself. -->
서비스 컨테이너에 대한 깊은 이해는 강력하고 대규모의 애플리케이션을 구축하거나 Laravel의 코어에 기여할 때 매우 중요합니다.

<a name="zero-configuration-resolution"></a>
<!-- ### Zero Configuration Resolution -->
### Zero Configuration Resolution

<!-- If a class has no dependencies or only depends on other concrete classes (not interfaces), the container does not need to be instructed on how to resolve that class. For example, you may place the following code in your `routes/web.php` file: -->
어떤 클래스가 의존성이 없거나, 의존성이 모두 구체 클래스(인터페이스가 아님)라면, 컨테이너가 해당 클래스를 어떻게 해석해야 할지 미리 알려줄 필요가 없습니다. 예를 들어, 아래와 같이 `routes/web.php` 파일에 코드를 작성할 수 있습니다:

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
이 예제에서 애플리케이션의 `/` 경로로 접속하면, 컨테이너가 `Service` 클래스를 자동으로 해석하여 라우트 핸들러에 주입합니다. 이는 상당한 변화입니다. 즉, 번거로운 설정 파일 없이도, 의존성 주입의 이점을 누리면서 애플리케이션을 개발할 수 있습니다.

<!-- Thankfully, many of the classes you will be writing when building a Laravel application automatically receive their dependencies via the container, including [controllers](/docs/12.x/controllers), [event listeners](/docs/12.x/events), [middleware](/docs/12.x/middleware), and more. Additionally, you may type-hint dependencies in the `handle` method of [queued jobs](/docs/12.x/queues). Once you taste the power of automatic and zero configuration dependency injection it feels impossible to develop without it. -->
다행히도 Laravel 애플리케이션을 개발할 때 작성하는 많은 클래스들은 서비스 컨테이너를 통해 의존성을 자동으로 주입받습니다. 여기에는 [controllers](/docs/12.x/controllers), [event listeners](/docs/12.x/events), [middleware](/docs/12.x/middleware) 등이 포함됩니다. 또한, [queued jobs](/docs/12.x/queues)의 `handle` 메서드에 의존성을 타입힌트로 지정하면 주입받을 수 있습니다. 이런 자동, 무설정(제로 설정) 의존성 주입의 강력함을 한 번 경험하면, 이를 사용하지 않고는 개발할 수 없게 됩니다.

<a name="when-to-use-the-container"></a>
<!-- ### When to Utilize the Container -->
### When to Utilize the Container

<!-- Thanks to zero configuration resolution, you will often type-hint dependencies on routes, controllers, event listeners, and elsewhere without ever manually interacting with the container. For example, you might type-hint the `Illuminate\Http\Request` object on your route definition so that you can easily access the current request. Even though we never have to interact with the container to write this code, it is managing the injection of these dependencies behind the scenes: -->
제로 설정 자동 해석 덕분에, 라우트, 컨트롤러, 이벤트 리스너 등 여러 곳에서 타입힌트만으로 자연스럽게 의존성을 주입받을 수 있으며, 컨테이너와 직접 상호작용할 필요가 거의 없습니다. 예를 들어, 현재 요청에 쉽게 접근하기 위해 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌트로 지정할 수 있습니다. 아래 코드를 작성할 때 컨테이너와 직접 상호작용하지 않아도, 실제로 컨테이너가 이 의존성을 관리합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<!-- In many cases, thanks to automatic dependency injection and [facades](/docs/12.x/facades), you can build Laravel applications without **ever** manually binding or resolving anything from the container. **So, when would you ever manually interact with the container?** Let's examine two situations. -->
실제로 대부분의 경우에는 자동 의존성 주입과 [facades](/docs/12.x/facades)를 통해 컨테이너에서 아무것도 직접 바인딩하거나 해석하지 않고도 Laravel 애플리케이션을 쉽게 개발할 수 있습니다. **그렇다면 언제 직접 컨테이너와 상호작용해야 할까요?** 아래 두 가지 상황을 예로 들 수 있습니다.

<!-- First, if you write a class that implements an interface and you wish to type-hint that interface on a route or class constructor, you must [tell the container how to resolve that interface](#binding-interfaces-to-implementations). Secondly, if you are [writing a Laravel package](/docs/12.x/packages) that you plan to share with other Laravel developers, you may need to bind your package's services into the container. -->
첫째, 직접 인터페이스를 구현한 클래스를 작성하고 라우트나 생성자에서 해당 인터페이스를 타입힌트로 지정하려면, [tell the container how to resolve that interface](#binding-interfaces-to-implementations). 둘째, 당신이 [writing a Laravel package](/docs/12.x/packages)를 개발한다면, 패키지의 서비스를 컨테이너에 바인딩해야 할 수도 있습니다.

<a name="binding"></a>
<!-- ## Binding -->
## Binding

<a name="binding-basics"></a>
<!-- ### Binding Basics -->
### Binding Basics

<a name="simple-bindings"></a>
<!-- #### Simple Bindings -->
#### Simple Bindings

<!-- Almost all of your service container bindings will be registered within [service providers](/docs/12.x/providers), so most of these examples will demonstrate using the container in that context. -->
대부분의 서비스 컨테이너 바인딩은 [service providers](/docs/12.x/providers) 내에서 등록합니다. 아래 예시들은 이 맥락에서 컨테이너를 사용하는 방법을 보여줍니다.

<!-- Within a service provider, you always have access to the container via the `$this->app` property. We can register a binding using the `bind` method, passing the class or interface name that we wish to register along with a closure that returns an instance of the class: -->
서비스 프로바이더 내에서는 항상 `$this->app` 속성을 통해 컨테이너에 접근할 수 있습니다. 바인딩할 클래스나 인터페이스명과, 해당 클래스의 인스턴스를 반환하는 클로저를 `bind` 메서드에 전달하여 바인딩을 등록할 수 있습니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<!-- Note that we receive the container itself as an argument to the resolver. We can then use the container to resolve sub-dependencies of the object we are building. -->
해석자(Resolver)로 전달되는 인수로 컨테이너 자체를 받을 수 있습니다. 이를 통해 객체를 생성할 때 하위 의존성도 컨테이너로부터 해석할 수 있습니다.

<!-- As mentioned, you will typically be interacting with the container within service providers; however, if you would like to interact with the container outside of a service provider, you may do so via the `App` [facade](/docs/12.x/facades): -->
앞서 설명한 대로, 보통 서비스 프로바이더에서 컨테이너와 상호작용하지만, 필요할 때는 `App` [facade](/docs/12.x/facades)를 통해 프로바이더 밖에서도 사용할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

<!-- You may use the `bindIf` method to register a container binding only if a binding has not already been registered for the given type: -->
이미 해당 타입에 대한 바인딩이 존재하지 않을 때만 컨테이너 바인딩을 등록하려면 `bindIf` 메서드를 사용할 수 있습니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<!-- For convenience, you may omit providing the class or interface name that you wish to register as a separate argument and instead allow Laravel to infer the type from the return type of the closure you provide to the `bind` method: -->
편의를 위해, 바인딩하려는 클래스/인터페이스명을 별도의 인수로 전달하지 않고, `bind` 메서드에 전달하는 클로저의 반환 타입으로 Laravel이 타입을 추론하게 할 수도 있습니다.

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 어떤 클래스가 인터페이스에 의존하지 않는다면, 컨테이너에 바인딩할 필요가 없습니다. 컨테이너는 리플렉션을 사용해 이런 객체를 자동으로 해석합니다.

<a name="binding-a-singleton"></a>
<!-- #### Binding A Singleton -->
#### Binding A Singleton

<!-- The `singleton` method binds a class or interface into the container that should only be resolved one time. Once a singleton binding is resolved, the same object instance will be returned on subsequent calls into the container: -->
`singleton` 메서드는 클래스나 인터페이스를 단 한 번만 컨테이너에 해석하여, 이후에는 항상 동일한 객체 인스턴스를 반환하도록 바인딩합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<!-- You may use the `singletonIf` method to register a singleton container binding only if a binding has not already been registered for the given type: -->
또한, 이미 바인딩이 존재하지 않을 때만 싱글톤으로 등록하려면 `singletonIf` 메서드를 사용할 수 있습니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="singleton-attribute"></a>
<!-- #### Singleton Attribute -->
#### Singleton Attribute

<!-- Alternatively, you may mark an interface or class with the `#[Singleton]` attribute to indicate to the container that it should be resolved one time: -->
또한, 인터페이스나 클래스에 `#[Singleton]` 속성을 부여하여 컨테이너가 단 한 번만 해석하도록 지정할 수 있습니다.

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

<!-- The `scoped` method binds a class or interface into the container that should only be resolved one time within a given Laravel request / job lifecycle. While this method is similar to the `singleton` method, instances registered using the `scoped` method will be flushed whenever the Laravel application starts a new "lifecycle", such as when a [Laravel Octane](/docs/12.x/octane) worker processes a new request or when a Laravel [queue worker](/docs/12.x/queues) processes a new job: -->
`scoped` 메서드는 클래스나 인터페이스를 주어진 Laravel 요청/작업(job)의 라이프사이클 안에서 단 한 번만 해석하도록 바인딩합니다. 이 방식은 `singleton`과 비슷하지만, `scoped`로 등록된 인스턴스는 [Laravel Octane](/docs/12.x/octane) 워커가 새로운 요청을 처리하거나, [queue worker](/docs/12.x/queues)가 새 작업을 처리할 때마다 플러시(flush)됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<!-- You may use the `scopedIf` method to register a scoped container binding only if a binding has not already been registered for the given type: -->
바인딩이 이미 존재하지 않을 때만 scoped 바인딩을 등록하려면 `scopedIf` 메서드를 사용합니다.

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="scoped-attribute"></a>
<!-- #### Scoped Attribute -->
#### Scoped Attribute

<!-- Alternatively, you may mark an interface or class with the `#[Scoped]` attribute to indicate to the container that it should be resolved one time within a given Laravel request / job lifecycle: -->
인터페이스나 클래스에 `#[Scoped]` 속성을 부여하여, 주어진 요청/작업(job) 라이프사이클 내에서 한 번만 해석되도록 지정할 수도 있습니다.

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
이미 존재하는 객체 인스턴스를 `instance` 메서드를 사용해 컨테이너에 바인딩할 수 있습니다. 해당 인스턴스는 이후 컨테이너에서 계속 반환됩니다.

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
서비스 컨테이너의 강력한 기능 중 하나는 인터페이스와 구현체를 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 이를 구현한 `RedisEventPusher` 구현체가 있다고 합시다. 이 인터페이스에 대한 `RedisEventPusher` 구현체를 작성했다면, 아래와 같이 서비스 컨테이너에 등록할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

<!-- This statement tells the container that it should inject the `RedisEventPusher` when a class needs an implementation of `EventPusher`. Now we can type-hint the `EventPusher` interface in the constructor of a class that is resolved by the container. Remember, controllers, event listeners, middleware, and various other types of classes within Laravel applications are always resolved using the container: -->
이렇게 등록하면, 컨테이너가 `EventPusher` 구현이 필요한 클래스에 자동으로 `RedisEventPusher`를 주입합니다. 이제 컨테이너가 해석하는 클래스의 생성자에 `EventPusher` 인터페이스를 타입힌트로 지정할 수 있습니다. 컨트롤러, 이벤트 리스너, 미들웨어 등 Laravel 애플리케이션의 다양한 클래스는 항상 컨테이너로 해석된다는 점을 기억하세요.

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
Laravel은 더 편리하게 사용할 수 있도록 `Bind` 속성도 제공합니다. 인터페이스에 이 속성을 지정하면, 해당 인터페이스가 요청될 때 어떤 구현체가 자동으로 주입되어야 하는지 Laravel이 알게 됩니다. `Bind` 속성을 사용하면 애플리케이션의 서비스 프로바이더에서 추가적인 서비스 등록을 할 필요가 없습니다.

<!-- In addition, multiple `Bind` attributes may be placed on an interface in order to configure a different implementation that should be injected for a given set of environments: -->
또한, 하나의 인터페이스에 여러 개의 `Bind` 속성을 부여하여 환경별로 다른 구현체를 주입할 수 있습니다.

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
아울러, [Singleton](#singleton-attribute) 및 [Scoped](#scoped-attribute) 속성을 함께 사용하여, 해당 인터페이스의 바인딩 해석 범위를 지정할 수 있습니다.

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

<!-- Sometimes you may have two classes that utilize the same interface, but you wish to inject different implementations into each class. For example, two controllers may depend on different implementations of the `Illuminate\Contracts\Filesystem\Filesystem` [contract](/docs/12.x/contracts). Laravel provides a simple, fluent interface for defining this behavior: -->
때때로 두 개의 클래스가 같은 인터페이스를 사용하지만 각각 다른 구현체가 주입되어야 할 때가 있습니다. 예를 들어, 두 컨트롤러가 각기 다른 `Illuminate\Contracts\Filesystem\Filesystem` [contract](/docs/12.x/contracts) 구현체에 의존한다면, 아래와 같은 방식으로 컨텍스트 바인딩을 정의할 수 있습니다.

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
컨텍스트 바인딩은 보통 드라이버 구현체나 설정값을 주입할 때 많이 사용합니다. Laravel은 이런 값을 서비스 프로바이더에서 수동으로 정의하지 않고도 속성(Attribute)으로 쉽게 주입할 수 있도록 여러 컨텍스트 바인딩 속성을 제공합니다.

<!-- For example, the `Storage` attribute may be used to inject a specific [storage disk](/docs/12.x/filesystem): -->
예를 들어, `Storage` 속성(Attribute)을 사용하면 특정 [storage disk](/docs/12.x/filesystem)를 주입할 수 있습니다.

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
`Storage` 속성 외에도, Laravel은 `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RouteParameter`, [Tag](#tagging) 속성을 제공합니다.

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
        #[RouteParameter('photo')] protected Photo $photo,
        #[Tag('reports')] protected iterable $reports,
    ) {
        // ...
    }
}
```

<!-- Furthermore, Laravel provides a `CurrentUser` attribute for injecting the currently authenticated user into a given route or class: -->
더불어, 현재 인증된 사용자를 라우트나 클래스에 주입할 때 사용할 수 있는 `CurrentUser` 속성도 제공합니다.

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
직접 커스텀 컨텍스트 속성을 만들 수 있습니다. 이를 위해 `Illuminate\Contracts\Container\ContextualAttribute` 컨트랙트를 구현합니다. 컨테이너는 해당 속성의 `resolve` 메서드를 호출하여, 클래스로 주입할 값을 결정합니다. 아래는 Laravel의 내장 `Config` 속성을 다시 구현한 예시입니다.

```php
<?php

namespace App\Attributes;

use Attribute;
use Illuminate\Contracts\Container\Container;
use Illuminate\Contracts\Container\ContextualAttribute;

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
     * @return mixed
     */
    public static function resolve(self $attribute, Container $container)
    {
        return $container->make('config')->get($attribute->key, $attribute->default);
    }
}
```

<a name="binding-primitives"></a>
<!-- ### Binding Primitives -->
### Binding Primitives

<!-- Sometimes you may have a class that receives some injected classes, but also needs an injected primitive value such as an integer. You may easily use contextual binding to inject any value your class may need: -->
클래스에 의존성 객체뿐 아니라 정수 등 기본 자료형 값을 주입하고 싶을 때, 컨텍스트 바인딩을 활용할 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

<!-- Sometimes a class may depend on an array of [tagged](#tagging) instances. Using the `giveTagged` method, you may easily inject all of the container bindings with that tag: -->
클래스가 [tagged](#tagging) 인스턴스의 배열을 필요로 한다면, `giveTagged` 메서드를 사용해 해당 태그로 컨테이너에 등록된 모든 것을 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

<!-- If you need to inject a value from one of your application's configuration files, you may use the `giveConfig` method: -->
애플리케이션 환경설정파일에서 값을 주입해야 할 경우 `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
<!-- ### Binding Typed Variadics -->
### Binding Typed Variadics

<!-- Occasionally, you may have a class that receives an array of typed objects using a variadic constructor argument: -->
가끔씩, 특정 클래스가 가변 인자(variadic)로 타입이 지정된 객체 배열을 받는 경우가 있습니다.

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
컨텍스트 바인딩에서는 `give` 메서드에 `Filter` 인스턴스 배열을 반환하는 클로저를 전달하여 이 의존성을 해석할 수 있습니다.

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
더 간단하게 클래스명 배열만 전달하면, `Firewall`이 `Filter` 인스턴스를 필요로 할 때마다 컨테이너가 해당 클래스들을 자동으로 해석하여 주입합니다.

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
클래스의 가변 인자 의존성이 특정 클래스(예: `Report ...$reports`)로 타입힌트된 경우, `needs`와 `giveTagged` 메서드를 사용해 [tag](#tagging)로 연결된 바인딩을 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
<!-- ### Tagging -->
### Tagging

<!-- Occasionally, you may need to resolve all of a certain "category" of binding. For example, perhaps you are building a report analyzer that receives an array of many different `Report` interface implementations. After registering the `Report` implementations, you can assign them a tag using the `tag` method: -->
특정 “카테고리”의 모든 바인딩을 한 번에 해석해야 할 때가 있습니다. 예를 들어 여러 종류의 `Report` 인터페이스 구현체 배열을 받는 리포트 분석기를 만든다고 해봅시다. `Report` 구현체들을 등록한 뒤, `tag` 메서드로 하나의 태그를 부여할 수 있습니다.

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
이후, 컨테이너의 `tagged` 메서드로 해당 태그가 부여된 모든 서비스를 쉽게 해석할 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
<!-- ### Extending Bindings -->
### Extending Bindings

<!-- The `extend` method allows the modification of resolved services. For example, when a service is resolved, you may run additional code to decorate or configure the service. The `extend` method accepts two arguments, the service class you're extending and a closure that should return the modified service. The closure receives the service being resolved and the container instance: -->
`extend` 메서드를 사용하면 이미 해석된 서비스를 수정하거나 데코레이션(decorate)할 수 있습니다. `extend` 메서드는 확장할 서비스 클래스와, 수정된 서비스를 반환하는 클로저(서비스 인스턴스와 컨테이너를 인수로 받음)를 전달받습니다.

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
`make` 메서드를 사용하여 컨테이너에서 클래스 인스턴스를 해석할 수 있습니다. `make` 메서드는 해석할 클래스나 인터페이스명을 인수로 받습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

<!-- If some of your class's dependencies are not resolvable via the container, you may inject them by passing them as an associative array into the `makeWith` method. For example, we may manually pass the `$id` constructor argument required by the `Transistor` service: -->
클래스의 일부 의존성이 컨테이너에서 해석되지 않는다면, `makeWith` 메서드로 연관 배열로 직접 값을 전달할 수 있습니다. 예를 들어, `Transistor` 서비스의 `$id` 생성자 인자를 수동으로 전달할 수 있습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

<!-- The `bound` method may be used to determine if a class or interface has been explicitly bound in the container: -->
`bound` 메서드를 사용하면 컨테이너에 클래스나 인터페이스가 명시적으로 바인딩되어 있는지 확인할 수 있습니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

<!-- If you are outside of a service provider in a location of your code that does not have access to the `$app` variable, you may use the `App` [facade](/docs/12.x/facades) or the `app` [helper](/docs/12.x/helpers#method-app) to resolve a class instance from the container: -->
서비스 프로바이더 외부 등 `$app` 변수에 접근할 수 없는 위치에서는 `App` [facade](/docs/12.x/facades)나, `app` [helper](/docs/12.x/helpers#method-app)를 사용해 클래스 인스턴스를 해석할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

<!-- If you would like to have the Laravel container instance itself injected into a class that is being resolved by the container, you may type-hint the `Illuminate\Container\Container` class on your class's constructor: -->
클래스 생성자에서 Laravel 컨테이너 자체를 주입받고 싶다면, `Illuminate\Container\Container` 클래스를 타입힌트로 지정하면 됩니다.

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

<!-- Alternatively, and importantly, you may type-hint the dependency in the constructor of a class that is resolved by the container, including [controllers](/docs/12.x/controllers), [event listeners](/docs/12.x/events), [middleware](/docs/12.x/middleware), and more. Additionally, you may type-hint dependencies in the `handle` method of [queued jobs](/docs/12.x/queues). In practice, this is how most of your objects should be resolved by the container. -->
컨테이너에서 해석되는 클래스([controllers](/docs/12.x/controllers), [event listeners](/docs/12.x/events), [middleware](/docs/12.x/middleware) 등)의 생성자에 의존성을 타입힌트로 지정하면 자동으로 주입됩니다. [queued jobs](/docs/12.x/queues)의 `handle` 메서드도 마찬가지로 지원합니다. 실무에서 객체 대부분은 이처럼 컨테이너에 의해 해석됩니다.

<!-- For example, you may type-hint a service defined by your application in a controller's constructor. The service will automatically be resolved and injected into the class: -->
예를 들어, 아래처럼 컨트롤러 생성자에 직접 서비스를 타입힌트로 지정할 수 있습니다. 서비스는 자동으로 해석되어 클래스에 주입됩니다.

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
때로는 객체 인스턴스의 특정 메서드를 호출할 때, 그 메서드가 필요로 하는 의존성도 컨테이너가 자동으로 주입해주길 바랄 수 있습니다. 예를 들어 아래와 같은 클래스가 있다고 합시다.

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
컨테이너의 `call` 메서드를 사용하면 아래처럼 `generate` 메서드를 호출할 수 있습니다.

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

<!-- The `call` method accepts any PHP callable. The container's `call` method may even be used to invoke a closure while automatically injecting its dependencies: -->
`call` 메서드는 PHP의 어떤 콜러블도 받을 수 있습니다. 또한, 클로저를 전달하면 해당 클로저에 필요한 의존성도 자동으로 주입해줍니다.

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
서비스 컨테이너는 객체를 해석할 때마다 이벤트를 발생시킵니다. `resolving` 메서드로 이 이벤트를 수신할 수 있습니다.

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
위와 같이 해석 중인 객체 인스턴스가 콜백에 전달되므로, 주입되기 전에 필요한 속성을 추가로 설정할 수 있습니다.

<a name="rebinding"></a>
<!-- ### Rebinding -->
### Rebinding

<!-- The `rebinding` method allows you to listen for when a service is re-bound to the container, meaning it is registered again or overridden after its initial binding. This can be useful when you need to update dependencies or modify behavior each time a specific binding is updated: -->
`rebinding` 메서드를 사용하면 서비스가 컨테이너에 다시(재)바인딩될 때마다(즉, 이미 등록된 바인딩이 다시 등록되거나 오버라이드될 때) 콜백을 실행할 수 있습니다. 이는 바인딩이 업데이트될 때마다 의존성을 갱신하거나 동작을 수정해야 할 때 유용합니다.

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
Laravel의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11 컨테이너 인터페이스를 타입힌트로 지정하면 Laravel 컨테이너 인스턴스를 주입받을 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

<!-- An exception is thrown if the given identifier can't be resolved. The exception will be an instance of `Psr\Container\NotFoundExceptionInterface` if the identifier was never bound. If the identifier was bound but was unable to be resolved, an instance of `Psr\Container\ContainerExceptionInterface` will be thrown. -->
만약 전달된 식별자를 해석할 수 없으면 예외가 발생합니다. 해당 식별자가 한 번도 바인딩된 적이 없다면, `Psr\Container\NotFoundExceptionInterface`의 인스턴스가, 바인딩은 되어 있지만 해석에 실패하면 `Psr\Container\ContainerExceptionInterface`의 인스턴스가 throw 됩니다.
