<!-- # Facades -->
# Facades

- [Introduction](#introduction)
- [When to Utilize Facades](#when-to-use-facades)
    - [Facades vs. Dependency Injection](#facades-vs-dependency-injection)
    - [Facades vs. Helper Functions](#facades-vs-helper-functions)
- [How Facades Work](#how-facades-work)
- [Real-Time Facades](#real-time-facades)
- [Facade Class Reference](#facade-class-reference)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Throughout the Laravel documentation, you will see examples of code that interacts with Laravel's features via "facades". Facades provide a "static" interface to classes that are available in the application's [service container](/docs/13.x/container). Laravel ships with many facades which provide access to almost all of Laravel's features. -->
Laravel 문서 전반에서 "파사드"를 통해 Laravel의 기능과 상호 작용하는 코드 예제를 볼 수 있습니다. 파사드는 애플리케이션의 [service container](/docs/13.x/container)에서 사용할 수 있는 클래스에 "정적" 인터페이스를 제공합니다. Laravel에는 Laravel의 거의 모든 기능에 액세스할 수 있도록 해 주는 다양한 파사드가 포함되어 있습니다.

<!-- Laravel facades serve as "static proxies" to underlying classes in the service container, providing the benefit of a terse, expressive syntax while maintaining more testability and flexibility than traditional static methods. It's perfectly fine if you don't totally understand how facades work - just go with the flow and continue learning about Laravel. -->
Laravel 파사드는 서비스 컨테이너 내부의 클래스에 대한 "정적 프록시(static proxy)"로 동작합니다. 이 방식은 간결하면서도 표현력 있는 문법을 제공하며, 전통적인 정적 메서드보다 테스트와 유연성 면에서 더 큰 장점을 가집니다. 파사드가 어떻게 동작하는지 완전히 이해하지 못해도 괜찮으니, 우선은 다양한 예시를 통해 Laravel을 계속 학습해 나가면 됩니다.

<!-- All of Laravel's facades are defined in the `Illuminate\Support\Facades` namespace. So, we can easily access a facade like so: -->
모든 Laravel의 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 그래서 다음과 같이 손쉽게 파사드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

<!-- Throughout the Laravel documentation, many of the examples will use facades to demonstrate various features of the framework. -->
Laravel 공식 문서 전반에서는 프레임워크의 다양한 기능을 설명할 때 파사드 사용 예시를 자주 제공합니다.

<a name="helper-functions"></a>
<!-- #### Helper Functions -->
#### Helper Functions

<!-- To complement facades, Laravel offers a variety of global "helper functions" that make it even easier to interact with common Laravel features. Some of the common helper functions you may interact with are `view`, `response`, `url`, `config`, and more. Each helper function offered by Laravel is documented with their corresponding feature; however, a complete list is available within the dedicated [helper documentation](/docs/13.x/helpers). -->
파사드를 보완하기 위해 Laravel은 일반적인 Laravel 기능과 더 쉽게 상호 작용할 수 있도록 다양한 전역 "헬퍼 함수"를 제공합니다. 자주 사용하는 헬퍼 함수로는 `view`, `response`, `url`, `config` 등이 있습니다. Laravel이 제공하는 각 헬퍼 함수는 해당 기능과 함께 문서화되어 있지만, 전체 목록은 전용 [helper documentation](/docs/13.x/helpers)에서 확인할 수 있습니다.

<!-- For example, instead of using the `Illuminate\Support\Facades\Response` facade to generate a JSON response, we may simply use the `response` function. Because helper functions are globally available, you do not need to import any classes in order to use them: -->
예를 들어, `Illuminate\Support\Facades\Response` 파사드를 사용해 JSON 응답을 만들 수도 있지만, 단순히 `response` 헬퍼 함수를 사용하는 것도 가능합니다. 헬퍼 함수는 전역적으로 쓸 수 있기 때문에 클래스를 따로 임포트하지 않아도 됩니다.

```php
use Illuminate\Support\Facades\Response;

Route::get('/users', function () {
    return Response::json([
        // ...
    ]);
});

Route::get('/users', function () {
    return response()->json([
        // ...
    ]);
});
```

<a name="when-to-use-facades"></a>
<!-- ## When to Utilize Facades -->
## When to Utilize Facades

<!-- Facades have many benefits. They provide a terse, memorable syntax that allows you to use Laravel's features without remembering long class names that must be injected or configured manually. Furthermore, because of their unique usage of PHP's dynamic methods, they are easy to test. -->
파사드는 여러 가지 이점을 제공합니다. 긴 클래스명을 직접 기억하거나, 일일이 주입(injection) 또는 수동 설정 없이 Laravel의 다양한 기능을 간결하면서도 기억하기 쉬운 문법으로 사용할 수 있습니다. 또한, PHP의 동적 메서드 방식을 활용하기 때문에 테스트도 쉽게 할 수 있습니다.

<!-- However, some care must be taken when using facades. The primary danger of facades is class "scope creep". Since facades are so easy to use and do not require injection, it can be easy to let your classes continue to grow and use many facades in a single class. Using dependency injection, this potential is mitigated by the visual feedback a large constructor gives you that your class is growing too large. So, when using facades, pay special attention to the size of your class so that its scope of responsibility stays narrow. If your class is getting too large, consider splitting it into multiple smaller classes. -->
다만 파사드 사용 시 주의할 점도 있습니다. 가장 큰 위험은 클래스의 "스코프 크리프(scope creep)", 즉 책임 영역이 너무 커지는 문제입니다. 파사드는 사용이 매우 쉬워서, 클래스 내에서 점점 더 많은 파사드를 추가하게 되어 클래스가 비대해지기 쉽습니다. 의존성 주입을 사용하는 경우, 생성자가 커지는 것을 시각적으로 확인할 수 있어 이런 문제를 어느 정도 방지할 수 있습니다. 파사드를 사용할 때도, 해당 클래스가 너무 커지지 않도록 항상 주의하고 책임 범위를 좁게 유지해야 합니다. 클래스가 과하게 커진다면 여러 개의 더 작은 클래스로 분리하는 것도 고려해야 합니다.

<a name="facades-vs-dependency-injection"></a>
<!-- ### Facades vs. Dependency Injection -->
### Facades vs. Dependency Injection

<!-- One of the primary benefits of dependency injection is the ability to swap implementations of the injected class. This is useful during testing since you can inject a mock or stub and assert that various methods were called on the stub. -->
의존성 주입의 주요 장점은 주입 받은 클래스의 구현체를 쉽게 바꿀 수 있다는 점입니다. 예를 들어, 테스트 시에는 실제 객체 대신 Mock(가짜 객체)이나 Stub을 주입해서, 특정 메서드가 제대로 호출되었는지 확인할 수 있습니다.

<!-- Typically, it would not be possible to mock or stub a truly static class method. However, since facades use dynamic methods to proxy method calls to objects resolved from the service container, we actually can test facades just as we would test an injected class instance. For example, given the following route: -->
전통적인 정적(static) 클래스 메서드는 Mock이나 Stub으로 대체할 수가 없습니다. 하지만 파사드는 동적 메서드를 사용해 메서드 호출을 서비스 컨테이너에서 가져온 객체로 프록시 처리하기 때문에, 실제로 의존성 주입과 동일하게 테스트할 수 있습니다. 예를 들어, 아래와 같은 라우트 코드가 있다고 가정해보겠습니다.

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

<!-- Using Laravel's facade testing methods, we can write the following test to verify that the `Cache::get` method was called with the argument we expected: -->
Laravel의 파사드 테스트 메서드를 활용하면, 우리가 기대하는 인수로 `Cache::get` 메서드가 호출되는지 아래와 같이 테스트할 수 있습니다.

```php tab=Pest
use Illuminate\Support\Facades\Cache;

test('basic example', function () {
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
});
```

```php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="facades-vs-helper-functions"></a>
<!-- ### Facades vs. Helper Functions -->
### Facades vs. Helper Functions

<!-- In addition to facades, Laravel includes a variety of "helper" functions which can perform common tasks like generating views, firing events, dispatching jobs, or sending HTTP responses. Many of these helper functions perform the same function as a corresponding facade. For example, this facade call and helper call are equivalent: -->
Laravel은 파사드 이외에도, 뷰 생성, 이벤트 발생, 작업 디스패치, HTTP 응답 전송 등 다양한 "헬퍼 함수"를 제공합니다. 많은 헬퍼 함수는 해당 파사드와 동일한 기능을 수행합니다. 예를 들어, 아래 파사드 호출과 헬퍼 함수 호출은 완전히 동일하게 동작합니다.

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

<!-- There is absolutely no practical difference between facades and helper functions. When using helper functions, you may still test them exactly as you would the corresponding facade. For example, given the following route: -->
파사드와 헬퍼 함수 모두 실제 사용상 차이가 없습니다. 헬퍼 함수를 사용할 때도 해당 파사드와 똑같이 테스트가 가능합니다. 예를 들어, 다음과 같은 라우트 코드가 있다고 할 때,

```php
Route::get('/cache', function () {
    return cache('key');
});
```

<!-- The `cache` helper is going to call the `get` method on the class underlying the `Cache` facade. So, even though we are using the helper function, we can write the following test to verify that the method was called with the argument we expected: -->
`cache` 헬퍼 함수는 내부적으로 `Cache` 파사드에 연결된 클래스의 `get` 메서드를 호출합니다. 즉, 우리가 헬퍼 함수를 써서 코드를 작성해도, 아래와 같이 메서드가 올바른 인수로 호출되었는지 동일하게 테스트할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="how-facades-work"></a>
<!-- ## How Facades Work -->
## How Facades Work

<!-- In a Laravel application, a facade is a class that provides access to an object from the container. The machinery that makes this work is in the `Facade` class. Laravel's facades, and any custom facades you create, will extend the base `Illuminate\Support\Facades\Facade` class. -->
Laravel 애플리케이션에서 파사드는 서비스 컨테이너의 객체에 접근하는 클래스를 의미합니다. 파사드를 가능하게 해 주는 핵심은 `Facade`라는 클래스에 있습니다. Laravel의 모든 파사드, 그리고 사용자가 커스텀 파사드를 만들 때에도, 기본적으로 `Illuminate\Support\Facades\Facade` 클래스를 확장하게 됩니다.

<!-- The `Facade` base class makes use of the `__callStatic()` magic-method to defer calls from your facade to an object resolved from the container. In the example below, a call is made to the Laravel cache system. By glancing at this code, one might assume that the static `get` method is being called on the `Cache` class: -->
`Facade` 기본 클래스는 `__callStatic()` 매직 메서드를 활용해 파사드의 모든 호출을 서비스 컨테이너에서 가져온 객체에 위임합니다. 아래 예시에서, Laravel 캐시 시스템에 접근하는 코드를 볼 수 있습니다. 이 코드를 보면, 마치 `Cache` 클래스의 정적 `get` 메서드를 호출하는 것처럼 보일 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function showProfile(string $id): View
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}
```

<!-- Notice that near the top of the file we are "importing" the `Cache` facade. This facade serves as a proxy for accessing the underlying implementation of the `Illuminate\Contracts\Cache\Factory` interface. Any calls we make using the facade will be passed to the underlying instance of Laravel's cache service. -->
파일 상단에서 `Cache` 파사드를 "임포트"한 것을 확인할 수 있습니다. 이 파사드는 실제로는 `Illuminate\Contracts\Cache\Factory` 인터페이스의 구현체에 접근하는 프록시 역할을 합니다. 개발자가 파사드를 통해 메서드를 호출하면, 이 메서드 호출이 실제로는 Laravel의 캐시 서비스 인스턴스에 전달됩니다.

<!-- If we look at that `Illuminate\Support\Facades\Cache` class, you'll see that there is no static method `get`: -->
실제 `Illuminate\Support\Facades\Cache` 클래스를 살펴보면, 정적 메서드 `get`이 정의되어 있지 않다는 것을 알 수 있습니다.

```php
class Cache extends Facade
{
    /**
     * Get the registered name of the component.
     */
    protected static function getFacadeAccessor(): string
    {
        return 'cache';
    }
}
```

<!-- Instead, the `Cache` facade extends the base `Facade` class and defines the method `getFacadeAccessor()`. This method's job is to return the name of a service container binding. When a user references any static method on the `Cache` facade, Laravel resolves the `cache` binding from the [service container](/docs/13.x/container) and runs the requested method (in this case, `get`) against that object. -->
대신 `Cache` 파사드는 기본 `Facade` 클래스를 확장하고 `getFacadeAccessor()` 메서드를 정의합니다. 이 메서드는 서비스 컨테이너 바인딩의 이름을 반환합니다. 사용자가 `Cache` 파사드의 정적 메서드를 참조하면 Laravel은 [service container](/docs/13.x/container)에서 `cache` 바인딩을 가져와 해당 객체에 요청된 메서드(이 경우 `get`)를 실행합니다.

<a name="real-time-facades"></a>
<!-- ## Real-Time Facades -->
## Real-Time Facades

<!-- Using real-time facades, you may treat any class in your application as if it was a facade. To illustrate how this can be used, let's first examine some code that does not use real-time facades. For example, let's assume our `Podcast` model has a `publish` method. However, in order to publish the podcast, we need to inject a `Publisher` instance: -->
실시간 파사드(Real-Time Facades)를 사용하면, 애플리케이션 내의 어떤 클래스든 파사드처럼 사용할 수 있습니다. 이를 좀 더 쉽게 이해하기 위해, 먼저 실시간 파사드를 사용하지 않는 코드를 살펴보겠습니다. 예를 들어, `Podcast` 모델에 `publish`라는 메서드가 있다고 가정하겠습니다. 이 메서드는 팟캐스트를 발행하기 위해 `Publisher` 인스턴스가 필요하여 주입받는 구조입니다.

```php
<?php

namespace App\Models;

use App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     */
    public function publish(Publisher $publisher): void
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this);
    }
}
```

<!-- Injecting a publisher implementation into the method allows us to easily test the method in isolation since we can mock the injected publisher. However, it requires us to always pass a publisher instance each time we call the `publish` method. Using real-time facades, we can maintain the same testability while not being required to explicitly pass a `Publisher` instance. To generate a real-time facade, prefix the namespace of the imported class with `Facades`: -->
이렇게 메서드에 퍼블리셔를 주입하면, 테스트 시에 퍼블리셔를 Mock 객체로 주입할 수 있으므로, 독립적인 테스트가 용이합니다. 하지만 매번 `publish` 메서드를 호출할 때마다 퍼블리셔 인스턴스를 직접 전달해야 합니다. 실시간 파사드를 사용하면, 동일한 테스트 가능성을 유지하면서도 `Publisher` 인스턴스를 명시적으로 전달할 필요가 없어집니다. 실시간 파사드를 만들기 위해서는, 임포트하는 클래스의 네임스페이스 앞에 `Facades` 프리픽스를 붙이면 됩니다.

```php
<?php

namespace App\Models;

use App\Contracts\Publisher; // [tl! remove]
use Facades\App\Contracts\Publisher; // [tl! add]
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     */
    public function publish(Publisher $publisher): void // [tl! remove]
    public function publish(): void // [tl! add]
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this); // [tl! remove]
        Publisher::publish($this); // [tl! add]
    }
}
```

<!-- When the real-time facade is used, the publisher implementation will be resolved out of the service container using the portion of the interface or class name that appears after the `Facades` prefix. When testing, we can use Laravel's built-in facade testing helpers to mock this method call: -->
실시간 파사드를 사용할 때는, `Facades` 프리픽스 이후의 인터페이스 또는 클래스 이름을 기반으로 서비스 컨테이너에서 해당 클래스를 해석해 객체를 가져옵니다. 테스트 시에도, Laravel이 제공하는 파사드 테스트 헬퍼를 그대로 사용할 수 있습니다.

```php tab=Pest
<?php

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

test('podcast can be published', function () {
    $podcast = Podcast::factory()->create();

    Publisher::shouldReceive('publish')->once()->with($podcast);

    $podcast->publish();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PodcastTest extends TestCase
{
    use RefreshDatabase;

    /**
     * A test example.
     */
    public function test_podcast_can_be_published(): void
    {
        $podcast = Podcast::factory()->create();

        Publisher::shouldReceive('publish')->once()->with($podcast);

        $podcast->publish();
    }
}
```

<a name="facade-class-reference"></a>
<!-- ## Facade Class Reference -->
## Facade Class Reference

<!-- Below you will find every facade and its underlying class. This is a useful tool for quickly digging into the API documentation for a given facade root. The [service container binding](/docs/13.x/container) key is also included where applicable. -->
아래에는 모든 파사드와 해당 파사드의 기반 클래스가 나와 있습니다. 특정 파사드 루트의 API 문서를 빠르게 살펴볼 때 유용하게 활용할 수 있습니다. 해당하는 경우 [service container binding](/docs/13.x/container) 키도 함께 표시됩니다.

<div class="overflow-auto">

<!-- | Facade | Class | Service Container Binding | | --- | --- | --- | | App | [Illuminate\Foundation\Application](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Application.html) | `app` | | Artisan | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Console/Kernel.html) | `artisan` | | Auth (Instance) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` | | Auth | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/13.x/Illuminate/Auth/AuthManager.html) | `auth` | | Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/13.x/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` | | Broadcast (Instance) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; | | Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; | | Bus | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; | | Cache (Instance) | [Illuminate\Cache\Repository](https://api.laravel.com/docs/13.x/Illuminate/Cache/Repository.html) | `cache.store` | | Cache | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/13.x/Illuminate/Cache/CacheManager.html) | `cache` | | Cloud | [Illuminate\Foundation\Cloud\CloudManager](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Cloud/CloudManager.html) | &nbsp; | | Config | [Illuminate\Config\Repository](https://api.laravel.com/docs/13.x/Illuminate/Config/Repository.html) | `config` | | Context | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/13.x/Illuminate/Log/Context/Repository.html) | &nbsp; | | Cookie | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/13.x/Illuminate/Cookie/CookieJar.html) | `cookie` | | Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/13.x/Illuminate/Encryption/Encrypter.html) | `encrypter` | | Date | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/13.x/Illuminate/Support/DateFactory.html) | `date` | | DB (Instance) | [Illuminate\Database\Connection](https://api.laravel.com/docs/13.x/Illuminate/Database/Connection.html) | `db.connection` | | DB | [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/13.x/Illuminate/Database/DatabaseManager.html) | `db` | | Event | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/13.x/Illuminate/Events/Dispatcher.html) | `events` | | Exceptions (Instance) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; | | Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; | | File | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/13.x/Illuminate/Filesystem/Filesystem.html) | `files` | | Gate | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; | | Hash | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Hashing/Hasher.html) | `hash` | | Http | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/13.x/Illuminate/Http/Client/Factory.html) | &nbsp; | | Lang | [Illuminate\Translation\Translator](https://api.laravel.com/docs/13.x/Illuminate/Translation/Translator.html) | `translator` | | Log | [Illuminate\Log\LogManager](https://api.laravel.com/docs/13.x/Illuminate/Log/LogManager.html) | `log` | | Mail | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/13.x/Illuminate/Mail/Mailer.html) | `mailer` | | Notification | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/13.x/Illuminate/Notifications/ChannelManager.html) | &nbsp; | | Password (Instance) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/13.x/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` | | Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/13.x/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` | | Pipeline (Instance) | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/13.x/Illuminate/Pipeline/Pipeline.html) | &nbsp; | | Process | [Illuminate\Process\Factory](https://api.laravel.com/docs/13.x/Illuminate/Process/Factory.html) | &nbsp; | | Queue (Base Class) | [Illuminate\Queue\Queue](https://api.laravel.com/docs/13.x/Illuminate/Queue/Queue.html) | &nbsp; | | Queue (Instance) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` | | Queue | [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/13.x/Illuminate/Queue/QueueManager.html) | `queue` | | RateLimiter | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/13.x/Illuminate/Cache/RateLimiter.html) | &nbsp; | | Redirect | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/13.x/Illuminate/Routing/Redirector.html) | `redirect` | | Redis (Instance) | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/13.x/Illuminate/Redis/Connections/Connection.html) | `redis.connection` | | Redis | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/13.x/Illuminate/Redis/RedisManager.html) | `redis` | | Request | [Illuminate\Http\Request](https://api.laravel.com/docs/13.x/Illuminate/Http/Request.html) | `request` | | Response (Instance) | [Illuminate\Http\Response](https://api.laravel.com/docs/13.x/Illuminate/Http/Response.html) | &nbsp; | | Response | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; | | Route | [Illuminate\Routing\Router](https://api.laravel.com/docs/13.x/Illuminate/Routing/Router.html) | `router` | | Schedule | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/13.x/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; | | Schema | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/13.x/Illuminate/Database/Schema/Builder.html) | &nbsp; | | Session (Instance) | [Illuminate\Session\Store](https://api.laravel.com/docs/13.x/Illuminate/Session/Store.html) | `session.store` | | Session | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/13.x/Illuminate/Session/SessionManager.html) | `session` | | Storage (Instance) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` | | Storage | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/13.x/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` | | URL | [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/13.x/Illuminate/Routing/UrlGenerator.html) | `url` | | Validator (Instance) | [Illuminate\Validation\Validator](https://api.laravel.com/docs/13.x/Illuminate/Validation/Validator.html) | &nbsp; | | Validator | [Illuminate\Validation\Factory](https://api.laravel.com/docs/13.x/Illuminate/Validation/Factory.html) | `validator` | | View (Instance) | [Illuminate\View\View](https://api.laravel.com/docs/13.x/Illuminate/View/View.html) | &nbsp; | | View | [Illuminate\View\Factory](https://api.laravel.com/docs/13.x/Illuminate/View/Factory.html) | `view` | | Vite | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Vite.html) | &nbsp; | -->
| 파사드 | 클래스 | 서비스 컨테이너 바인딩 |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth (Instance) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/13.x/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/13.x/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (Instance) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (Instance) | [Illuminate\Cache\Repository](https://api.laravel.com/docs/13.x/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/13.x/Illuminate/Cache/CacheManager.html) | `cache` |
| Cloud | [Illuminate\Foundation\Cloud\CloudManager](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Cloud/CloudManager.html) | &nbsp; |
| Config | [Illuminate\Config\Repository](https://api.laravel.com/docs/13.x/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/13.x/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/13.x/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/13.x/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/13.x/Illuminate/Support/DateFactory.html) | `date` |
| DB (Instance) | [Illuminate\Database\Connection](https://api.laravel.com/docs/13.x/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/13.x/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/13.x/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (Instance) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/13.x/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/13.x/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://api.laravel.com/docs/13.x/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://api.laravel.com/docs/13.x/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/13.x/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/13.x/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (Instance) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/13.x/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/13.x/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (Instance) | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/13.x/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://api.laravel.com/docs/13.x/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (Base Class) | [Illuminate\Queue\Queue](https://api.laravel.com/docs/13.x/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (Instance) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/13.x/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/13.x/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/13.x/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (Instance) | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/13.x/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/13.x/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://api.laravel.com/docs/13.x/Illuminate/Http/Request.html) | `request` |
| Response (Instance) | [Illuminate\Http\Response](https://api.laravel.com/docs/13.x/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://api.laravel.com/docs/13.x/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/13.x/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/13.x/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (Instance) | [Illuminate\Session\Store](https://api.laravel.com/docs/13.x/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/13.x/Illuminate/Session/SessionManager.html) | `session` |
| Storage (Instance) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/13.x/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/13.x/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/13.x/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (Instance) | [Illuminate\Validation\Validator](https://api.laravel.com/docs/13.x/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://api.laravel.com/docs/13.x/Illuminate/Validation/Factory.html) | `validator` |
| View (Instance) | [Illuminate\View\View](https://api.laravel.com/docs/13.x/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://api.laravel.com/docs/13.x/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/13.x/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>
