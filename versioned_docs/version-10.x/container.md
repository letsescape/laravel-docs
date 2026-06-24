<!-- # Service Container -->
# Service Container

- [Introduction](#introduction)
    - [Zero Configuration Resolution](#zero-configuration-resolution)
    - [When to Utilize the Container](#when-to-use-the-container)
- [Binding](#binding)
    - [Binding Basics](#binding-basics)
    - [Binding Interfaces to Implementations](#binding-interfaces-to-implementations)
    - [Contextual Binding](#contextual-binding)
    - [Binding Primitives](#binding-primitives)
    - [Binding Typed Variadics](#binding-typed-variadics)
    - [Tagging](#tagging)
    - [Extending Bindings](#extending-bindings)
- [Resolving](#resolving)
    - [The Make Method](#the-make-method)
    - [Automatic Injection](#automatic-injection)
- [Method Invocation and Injection](#method-invocation-and-injection)
- [Container Events](#container-events)
- [PSR-11](#psr-11)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The Laravel service container is a powerful tool for managing class dependencies and performing dependency injection. Dependency injection is a fancy phrase that essentially means this: class dependencies are "injected" into the class via the constructor or, in some cases, "setter" methods. -->
Laravel 서비스 컨테이너는 클래스 의존성을 관리하고, 의존성 주입을 수행하는 데 강력한 도구입니다. 여기서 의존성 주입이란, 클래스가 필요로 하는 객체(의존성)를 생성자 또는 경우에 따라 "setter" 메서드를 통해 클래스 내부로 "주입"하는 기법을 의미합니다.

<!-- Let's look at a simple example: -->
간단한 예제를 살펴보겠습니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Repositories\UserRepository;
use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * Show the profile for the given user.
     */
    public function show(string $id): View
    {
        $user = $this->users->find($id);

        return view('user.profile', ['user' => $user]);
    }
}
```

<!-- In this example, the `UserController` needs to retrieve users from a data source. So, we will **inject** a service that is able to retrieve users. In this context, our `UserRepository` most likely uses [Eloquent](/docs/10.x/eloquent) to retrieve user information from the database. However, since the repository is injected, we are able to easily swap it out with another implementation. We are also able to easily "mock", or create a dummy implementation of the `UserRepository` when testing our application. -->
위 예시에서 `UserController`는 데이터 소스에서 사용자 정보를 조회해야 합니다. 이를 위해 사용자 정보를 가져올 수 있는 서비스를 **주입**합니다. 이때 `UserRepository`는 일반적으로 [Eloquent](/docs/10.x/eloquent)를 사용해 데이터베이스에서 사용자 정보를 추출합니다. 하지만 리포지토리를 주입했기 때문에 언제든지 다른 구현체로 쉽게 대체할 수 있습니다. 또한 애플리케이션 테스트 시에는 `UserRepository`의 더미 구현(모의 객체, mock)을 만들어 사용할 수도 있습니다.

<!-- A deep understanding of the Laravel service container is essential to building a powerful, large application, as well as for contributing to the Laravel core itself. -->
Laravel 서비스 컨테이너를 깊이 있게 이해하는 것은 강력하고 대규모의 애플리케이션을 만들 때뿐만 아니라, Laravel 핵심(코어)에 기여할 때에도 필수적인 지식입니다.

<a name="zero-configuration-resolution"></a>
<!-- ### Zero Configuration Resolution -->
### Zero Configuration Resolution

<!-- If a class has no dependencies or only depends on other concrete classes (not interfaces), the container does not need to be instructed on how to resolve that class. For example, you may place the following code in your `routes/web.php` file: -->
클래스가 의존성 없이 단독으로 존재하거나, 또는 다른 구체 클래스(인터페이스가 아닌)만을 의존할 경우에는, 컨테이너에 해당 클래스를 어떻게 해석해야 할지 별도의 안내가 필요하지 않습니다. 예를 들어, 아래와 같은 코드를 `routes/web.php` 파일에 작성할 수 있습니다.

```
<?php

class Service
{
    // ...
}

Route::get('/', function (Service $service) {
    die($service::class);
});
```

<!-- In this example, hitting your application's `/` route will automatically resolve the `Service` class and inject it into your route's handler. This is game changing. It means you can develop your application and take advantage of dependency injection without worrying about bloated configuration files. -->
이 예제에서, 애플리케이션의 `/` 라우트를 요청하면 `Service` 클래스가 자동으로 해석되어 라우트 핸들러에 주입됩니다. 이 기능은 개발 방식에 혁신적 변화를 가져옵니다. 즉, 복잡한 설정 파일을 신경 쓸 필요 없이, 의존성 주입의 강점을 즉시 활용할 수 있습니다.

<!-- Thankfully, many of the classes you will be writing when building a Laravel application automatically receive their dependencies via the container, including [controllers](/docs/10.x/controllers), [event listeners](/docs/10.x/events), [middleware](/docs/10.x/middleware), and more. Additionally, you may type-hint dependencies in the `handle` method of [queued jobs](/docs/10.x/queues). Once you taste the power of automatic and zero configuration dependency injection it feels impossible to develop without it. -->
실제로, Laravel 애플리케이션에서 작성하는 컨트롤러([controllers](/docs/10.x/controllers)), 이벤트 리스너([event listeners](/docs/10.x/events)), 미들웨어([middleware](/docs/10.x/middleware)) 등 대부분의 클래스들은 자동으로 컨테이너를 통해 필요한 의존성을 전달받습니다. 또한 [queued jobs](/docs/10.x/queues)의 `handle` 메서드에서도 의존성을 타입힌트로 명확하게 지정할 수 있습니다. 자동이면서도 별도 설정 없는 의존성 주입의 강력함을 한 번 경험하면, 이 기능 없이 개발하기가 어려워질 것입니다.

<a name="when-to-use-the-container"></a>
<!-- ### When to Utilize the Container -->
### When to Utilize the Container

<!-- Thanks to zero configuration resolution, you will often type-hint dependencies on routes, controllers, event listeners, and elsewhere without ever manually interacting with the container. For example, you might type-hint the `Illuminate\Http\Request` object on your route definition so that you can easily access the current request. Even though we never have to interact with the container to write this code, it is managing the injection of these dependencies behind the scenes: -->
제로 설정 해석 덕분에, 여러분은 라우트, 컨트롤러, 이벤트 리스너 등 곳곳에 의존성을 타입힌트로 지정하기만 해도, 컨테이너와 직접적으로 상호작용하지 않고도 많은 기능을 쓸 수 있습니다. 예를 들어, 라우트에서 현재 요청 정보를 간편하게 사용하기 위해 `Illuminate\Http\Request` 객체를 타입힌트로 지정할 수 있습니다. 이렇게 작성해도 우리가 직접 컨테이너를 다루는 코드는 없지만, 실제로는 컨테이너가 내부적으로 이러한 의존성의 주입을 처리합니다.

```
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<!-- In many cases, thanks to automatic dependency injection and [facades](/docs/10.x/facades), you can build Laravel applications without **ever** manually binding or resolving anything from the container. **So, when would you ever manually interact with the container?** Let's examine two situations. -->
실제로, 자동 의존성 주입과 [facades](/docs/10.x/facades)의 조합 덕분에, Laravel 애플리케이션을 개발하면서 **직접** 컨테이너에서 바인딩하거나 해석(resolving)하지 않고도 대부분의 요구를 충족할 수 있습니다. **그렇다면 언제 직접 컨테이너에 접근해야 할까요?** 대표적으로 두 가지 상황을 살펴보겠습니다.

<!-- First, if you write a class that implements an interface and you wish to type-hint that interface on a route or class constructor, you must [tell the container how to resolve that interface](#binding-interfaces-to-implementations). Secondly, if you are [writing a Laravel package](/docs/10.x/packages) that you plan to share with other Laravel developers, you may need to bind your package's services into the container. -->
첫 번째는, 어떤 클래스가 인터페이스를 구현하고 있고, 해당 인터페이스를 라우트나 생성자에서 타입힌트로 사용하고 싶을 때입니다. 이 경우에는 [tell the container how to resolve that interface](#binding-interfaces-to-implementations)을 컨테이너에 명시해야 합니다. 두 번째는, [writing a Laravel package](/docs/10.x/packages)를 작성하여 다른 개발자와 공유하고자 할 때입니다. 이럴 때는 패키지에서 제공하는 서비스들을 컨테이너에 바인딩해 주어야 합니다.

<a name="binding"></a>
<!-- ## Binding -->
## Binding

<a name="binding-basics"></a>
<!-- ### Binding Basics -->
### Binding Basics

<a name="simple-bindings"></a>
<!-- #### Simple Bindings -->
#### Simple Bindings

<!-- Almost all of your service container bindings will be registered within [service providers](/docs/10.x/providers), so most of these examples will demonstrate using the container in that context. -->
대부분의 서비스 컨테이너 바인딩은 [service providers](/docs/10.x/providers) 내부에 등록됩니다. 아래의 예제들도 이러한 컨텍스트(서비스 프로바이더)에서 컨테이너를 사용하는 방법을 보여줍니다.

<!-- Within a service provider, you always have access to the container via the `$this->app` property. We can register a binding using the `bind` method, passing the class or interface name that we wish to register along with a closure that returns an instance of the class: -->
서비스 프로바이더 내부에서, 언제든 `$this->app` 속성을 통해 컨테이너에 접근할 수 있습니다. 바인딩을 등록하려면, `bind` 메서드를 사용해 등록할 클래스나 인터페이스 이름과 해당 클래스의 인스턴스를 반환하는 클로저를 전달하면 됩니다.

```
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<!-- Note that we receive the container itself as an argument to the resolver. We can then use the container to resolve sub-dependencies of the object we are building. -->
여기서 주의할 점은, 리졸버에서 컨테이너 자신을 인자로 받아온다는 점입니다. 이를 통해 우리가 만들 객체의 하위 의존성도 컨테이너를 사용해 해석할 수 있습니다.

<!-- As mentioned, you will typically be interacting with the container within service providers; however, if you would like to interact with the container outside of a service provider, you may do so via the `App` [facade](/docs/10.x/facades): -->
앞서 말했듯, 일반적으로 서비스 프로바이더 내부에서 컨테이너를 다루게 되지만, 서비스 프로바이더 외부에서도 컨테이너와 상호작용하고 싶다면 `App` [facade](/docs/10.x/facades)를 사용할 수 있습니다.

```
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

<!-- You may use the `bindIf` method to register a container binding only if a binding has not already been registered for the given type: -->
이미 동일한 타입에 대한 바인딩이 없다면, `bindIf` 메서드를 사용하여 조건부로 바인딩할 수도 있습니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 어떤 클래스가 인터페이스에 의존하지 않는다면, 컨테이너에 별도 바인딩을 등록할 필요가 없습니다. 컨테이너는 반사(reflection)를 이용해 이런 객체는 자동으로 해석할 수 있기 때문입니다.

<a name="binding-a-singleton"></a>
<!-- #### Binding A Singleton -->
#### Binding A Singleton

<!-- The `singleton` method binds a class or interface into the container that should only be resolved one time. Once a singleton binding is resolved, the same object instance will be returned on subsequent calls into the container: -->
`singleton` 메서드는 하나의 클래스나 인터페이스를 컨테이너에 **단 한 번만** 해석하여 바인딩하는 방법입니다. 싱글톤 바인딩이 한 번 해석되면, 이후에는 언제나 동일한 객체 인스턴스를 반환합니다.

```
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<!-- You may use the `singletonIf` method to register a singleton container binding only if a binding has not already been registered for the given type: -->
이미 바인딩이 존재하지 않을 때만 싱글톤 바인딩을 등록하려면 `singletonIf` 메서드를 사용할 수 있습니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-scoped"></a>
<!-- #### Binding Scoped Singletons -->
#### Binding Scoped Singletons

<!-- The `scoped` method binds a class or interface into the container that should only be resolved one time within a given Laravel request / job lifecycle. While this method is similar to the `singleton` method, instances registered using the `scoped` method will be flushed whenever the Laravel application starts a new "lifecycle", such as when a [Laravel Octane](/docs/10.x/octane) worker processes a new request or when a Laravel [queue worker](/docs/10.x/queues) processes a new job: -->
`scoped` 메서드는 주어진 Laravel 요청 또는 작업(job) 라이프사이클 내에서 **한 번만** 해석되어야 하는 클래스나 인터페이스를 바인딩합니다. 이 방식은 `singleton`과 매우 비슷하지만, `scoped`로 등록한 인스턴스는 새로운 "라이프사이클"이 시작될 때마다(예: [Laravel Octane](/docs/10.x/octane) 워커가 새로운 요청을 처리하거나, [queue worker](/docs/10.x/queues)가 새 작업을 처리할 때) 초기화됩니다.

```
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="binding-instances"></a>
<!-- #### Binding Instances -->
#### Binding Instances

<!-- You may also bind an existing object instance into the container using the `instance` method. The given instance will always be returned on subsequent calls into the container: -->
기존에 생성해 둔 객체 인스턴스를 컨테이너에 등록하고 싶다면 `instance` 메서드를 사용할 수 있습니다. 이렇게 등록된 인스턴스는 이후 컨테이너에서 항상 동일한 객체가 반환됩니다.

```
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
<!-- ### Binding Interfaces to Implementations -->
### Binding Interfaces to Implementations

<!-- A very powerful feature of the service container is its ability to bind an interface to a given implementation. For example, let's assume we have an `EventPusher` interface and a `RedisEventPusher` implementation. Once we have coded our `RedisEventPusher` implementation of this interface, we can register it with the service container like so: -->
서비스 컨테이너의 가장 강력한 기능 중 하나는, 특정 인터페이스를 원하는 구현체에 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher`라는 인터페이스와 이를 구현한 `RedisEventPusher` 구현체가 있다고 가정해 봅시다. 이 인터페이스에 대한 `RedisEventPusher` 구현체를 작성했다면, 컨테이너에 다음과 같이 등록할 수 있습니다.

```
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

<!-- This statement tells the container that it should inject the `RedisEventPusher` when a class needs an implementation of `EventPusher`. Now we can type-hint the `EventPusher` interface in the constructor of a class that is resolved by the container. Remember, controllers, event listeners, middleware, and various other types of classes within Laravel applications are always resolved using the container: -->
이 코드는 컨테이너에게 `EventPusher` 인터페이스가 필요할 때마다 `RedisEventPusher`를 주입하라고 알려줍니다. 이제 컨테이너가 해석하는 클래스의 생성자에 `EventPusher` 인터페이스를 타입힌트로 명시하면 됩니다. 앞서 언급한 대로, 컨트롤러, 이벤트 리스너, 미들웨어 등 Laravel 안에서 다양한 클래스들이 컨테이너를 통해 생성됩니다.

```
use App\Contracts\EventPusher;

/**
 * Create a new class instance.
 */
public function __construct(
    protected EventPusher $pusher
) {}
```

<a name="contextual-binding"></a>
<!-- ### Contextual Binding -->
### Contextual Binding

<!-- Sometimes you may have two classes that utilize the same interface, but you wish to inject different implementations into each class. For example, two controllers may depend on different implementations of the `Illuminate\Contracts\Filesystem\Filesystem` [contract](/docs/10.x/contracts). Laravel provides a simple, fluent interface for defining this behavior: -->
두 개 이상의 클래스가 동일한 인터페이스를 사용하지만, 각각 다른 구현체를 주입하고 싶을 때가 있습니다. 예를 들어, 두 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [contract](/docs/10.x/contracts)에 의존하지만, 각기 다른 파일 시스템 드라이버(예: local vs s3)를 쓰고 싶을 수 있습니다. Laravel에서는 이를 위한 간단한 유창한(fluid) 인터페이스를 제공합니다.

```
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

<a name="binding-primitives"></a>
<!-- ### Binding Primitives -->
### Binding Primitives

<!-- Sometimes you may have a class that receives some injected classes, but also needs an injected primitive value such as an integer. You may easily use contextual binding to inject any value your class may need: -->
클래스가 몇몇은 클래스(객체), 몇몇은 정수와 같은 원시값을 주입받아야 할 때가 있습니다. 이 경우에도 상황별 바인딩을 이용해 필요한 값을 주입할 수 있습니다.

```
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
          ->needs('$variableName')
          ->give($value);
```

<!-- Sometimes a class may depend on an array of [tagged](#tagging) instances. Using the `giveTagged` method, you may easily inject all of the container bindings with that tag: -->
때로는 클래스가 [tagged](#tagging)된 인스턴스의 배열을 필요로 할 수도 있습니다. `giveTagged` 메서드를 사용하면 해당 태그로 바인딩된 모든 인스턴스를 쉽게 주입할 수 있습니다.

```
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

<!-- If you need to inject a value from one of your application's configuration files, you may use the `giveConfig` method: -->
애플리케이션의 설정 파일 값이 필요하다면 `giveConfig` 메서드를 사용할 수 있습니다.

```
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
<!-- ### Binding Typed Variadics -->
### Binding Typed Variadics

<!-- Occasionally, you may have a class that receives an array of typed objects using a variadic constructor argument: -->
때로는 생성자에서 동일한 타입의 객체를 여러 개(가변 인수) 받아야 할 때가 있습니다.

```
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
상황별 바인딩을 사용하면, 해석된 `Filter` 인스턴스의 배열을 반환하는 클로저를 `give` 메서드에 전달하여 이 의존성을 해석할 수 있습니다.

```
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
좀 더 간편하게, 클래스명 배열을 지정하면 `Firewall`이 `Filter` 인스턴스를 필요로 할 때마다 컨테이너가 해당 클래스를 해석해 주입합니다.

```
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
클래스가 가변 인수 형태로 특정 클래스 타입(예: `Report ...$reports`)의 객체를 필요로 할 때, `needs`와 `giveTagged` 메서드를 조합하면 해당 [tag](#tagging)로 등록된 모든 인스턴스를 한번에 주입할 수 있습니다.

```
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
<!-- ### Tagging -->
### Tagging

<!-- Occasionally, you may need to resolve all of a certain "category" of binding. For example, perhaps you are building a report analyzer that receives an array of many different `Report` interface implementations. After registering the `Report` implementations, you can assign them a tag using the `tag` method: -->
때때로 특정 "범주"에 속하는 모든 바인딩을 한 번에 해석해야 할 때가 있습니다. 예를 들어, 다양한 `Report` 인터페이스 구현체를 배열로 받아서 동작하는 보고서 분석기를 만든다고 가정합시다. 먼저 여러 개의 `Report` 구현체를 바인딩한 뒤, 다음과 같이 `tag` 메서드를 사용해 각각에 태그를 지정할 수 있습니다.

```
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

<!-- Once the services have been tagged, you may easily resolve them all via the container's `tagged` method: -->
이렇게 태그가 지정된 서비스들은 컨테이너의 `tagged` 메서드를 이용해 한 번에 모두 해석할 수 있습니다.

```
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
<!-- ### Extending Bindings -->
### Extending Bindings

<!-- The `extend` method allows the modification of resolved services. For example, when a service is resolved, you may run additional code to decorate or configure the service. The `extend` method accepts two arguments, the service class you're extending and a closure that should return the modified service. The closure receives the service being resolved and the container instance: -->
`extend` 메서드를 사용하면, 이미 해석된 서비스를 수정(데코레이션, 설정 등)할 수 있습니다. 서비스가 해석되는 시점에 추가적인 코드를 실행하고 싶을 때 사용합니다. `extend`는 두 개의 인자를 받는데, 첫 번째는 확장할 서비스 클래스, 두 번째는 수정된 서비스를 반환하는 클로저입니다. 이 클로저에는 현재 해석 중인 서비스와 컨테이너 인스턴스가 전달됩니다.

```
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
컨테이너에서 클래스를 해석(인스턴스 생성)하려면 `make` 메서드를 사용할 수 있습니다. `make` 메서드는 해석하려는 클래스나 인터페이스의 이름을 인수로 받습니다.

```
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

<!-- If some of your class's dependencies are not resolvable via the container, you may inject them by passing them as an associative array into the `makeWith` method. For example, we may manually pass the `$id` constructor argument required by the `Transistor` service: -->
클래스 의존성 중 일부가 컨테이너에서 자동으로 해석될 수 없는 경우, `makeWith` 메서드로 연관 배열 형태로 직접 값을 전달할 수 있습니다. 아래는 `Transistor` 서비스의 생성자에 필요한 `$id` 값을 직접 지정하는 예시입니다.

```
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

<!-- The `bound` method may be used to determine if a class or interface has been explicitly bound in the container: -->
`bound` 메서드를 사용하면 컨테이너에 해당 클래스나 인터페이스가 명시적으로 바인딩되어 있는지 확인할 수 있습니다.

```
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

<!-- If you are outside of a service provider in a location of your code that does not have access to the `$app` variable, you may use the `App` [facade](/docs/10.x/facades) or the `app` [helper](/docs/10.x/helpers#method-app) to resolve a class instance from the container: -->
서비스 프로바이더 외부, 즉 `$app` 변수에 접근할 수 없는 위치에서 컨테이너를 이용하고 싶다면, `App` [facade](/docs/10.x/facades)나 `app` [helper](/docs/10.x/helpers#method-app)를 사용할 수 있습니다.

```
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

<!-- If you would like to have the Laravel container instance itself injected into a class that is being resolved by the container, you may type-hint the `Illuminate\Container\Container` class on your class's constructor: -->
컨테이너 자체(Laravel 컨테이너 인스턴스)를 다른 클래스에 주입하고 싶다면, 생성자에서 `Illuminate\Container\Container` 클래스를 타입힌트로 지정하면 됩니다.

```
use Illuminate\Container\Container;

/**
 * Create a new class instance.
 */
public function __construct(
    protected Container $container
) {}
```

<a name="automatic-injection"></a>
<!-- ### Automatic Injection -->
### Automatic Injection

<!-- Alternatively, and importantly, you may type-hint the dependency in the constructor of a class that is resolved by the container, including [controllers](/docs/10.x/controllers), [event listeners](/docs/10.x/events), [middleware](/docs/10.x/middleware), and more. Additionally, you may type-hint dependencies in the `handle` method of [queued jobs](/docs/10.x/queues). In practice, this is how most of your objects should be resolved by the container. -->
또는, 더 중요한 것은 컨테이너가 해석하는 클래스의 생성자에 필요한 의존성을 바로 타입힌트로 지정하는 것입니다. 이는 [controllers](/docs/10.x/controllers), [event listeners](/docs/10.x/events), [middleware](/docs/10.x/middleware) 등 거의 모든 객체에서 사용할 수 있습니다. 또한 [queued jobs](/docs/10.x/queues)의 `handle` 메서드에서도 의존성을 타입힌트로 받을 수 있습니다. 실제로, 여러분이 정의하는 대부분의 객체는 이렇게 자동으로 컨테이너에 의해 해석되어야 합니다.

<!-- For example, you may type-hint a repository defined by your application in a controller's constructor. The repository will automatically be resolved and injected into the class: -->
예를 들어, 컨트롤러의 생성자에서 애플리케이션이 정의한 리포지토리를 타입힌트로 지정하면, 저장소 객체가 자동으로 해석되어 주입됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;
use App\Models\User;

class UserController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * Show the user with the given ID.
     */
    public function show(string $id): User
    {
        $user = $this->users->findOrFail($id);

        return $user;
    }
}
```

<a name="method-invocation-and-injection"></a>
<!-- ## Method Invocation and Injection -->
## Method Invocation and Injection

<!-- Sometimes you may wish to invoke a method on an object instance while allowing the container to automatically inject that method's dependencies. For example, given the following class: -->
때로는 객체 인스턴스의 메서드를 호출할 때, 해당 메서드에 필요한 의존성을 컨테이너가 자동으로 주입해주길 원할 수 있습니다. 예를 들어, 다음과 같은 클래스를 보겠습니다.

```
<?php

namespace App;

use App\Repositories\UserRepository;

class UserReport
{
    /**
     * Generate a new user report.
     */
    public function generate(UserRepository $repository): array
    {
        return [
            // ...
        ];
    }
}
```

<!-- You may invoke the `generate` method via the container like so: -->
컨테이너를 통해 `generate` 메서드를 다음과 같이 호출할 수 있습니다.

```
use App\UserReport;
use Illuminate\Support\Facades\App;

$report = App::call([new UserReport, 'generate']);
```

<!-- The `call` method accepts any PHP callable. The container's `call` method may even be used to invoke a closure while automatically injecting its dependencies: -->
`call` 메서드는 PHP에서 사용할 수 있는 어떤 콜러블(callable)도 받을 수 있습니다. 컨테이너의 `call` 메서드를 사용하면, 클로저를 호출하면서도 컨테이너가 자동으로 의존성을 주입하게 할 수 있습니다.

```
use App\Repositories\UserRepository;
use Illuminate\Support\Facades\App;

$result = App::call(function (UserRepository $repository) {
    // ...
});
```

<a name="container-events"></a>
<!-- ## Container Events -->
## Container Events

<!-- The service container fires an event each time it resolves an object. You may listen to this event using the `resolving` method: -->
서비스 컨테이너는 객체를 해석할 때마다 이벤트를 발생시킵니다. 이 이벤트는 `resolving` 메서드를 사용해 감지할 수 있습니다.

```
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
이처럼, 해석된 객체가 콜백에 전달되기 때문에, 해당 객체에 추가적인 속성을 지정한 후 실제로 소비(사용)되기 전에 설정을 더 해줄 수 있습니다.

<a name="psr-11"></a>
<!-- ## PSR-11 -->
## PSR-11

<!-- Laravel's service container implements the [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) interface. Therefore, you may type-hint the PSR-11 container interface to obtain an instance of the Laravel container: -->
Laravel의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11 컨테이너 인터페이스를 타입힌트로 지정해 Laravel 컨테이너 인스턴스를 얻을 수 있습니다.

```
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

<!-- An exception is thrown if the given identifier can't be resolved. The exception will be an instance of `Psr\Container\NotFoundExceptionInterface` if the identifier was never bound. If the identifier was bound but was unable to be resolved, an instance of `Psr\Container\ContainerExceptionInterface` will be thrown. -->
해당 식별자를 해석할 수 없을 때는 예외가 던져집니다. 만약 식별자가 한 번도 바인딩된 적이 없다면, 예외는 `Psr\Container\NotFoundExceptionInterface`의 인스턴스가 됩니다. 한 번은 바인딩됐지만 해석할 수 없는 경우엔 `Psr\Container\ContainerExceptionInterface` 예외가 던져집니다.
