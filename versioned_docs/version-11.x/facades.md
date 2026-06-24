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

<!-- Throughout the Laravel documentation, you will see examples of code that interacts with Laravel's features via "facades". Facades provide a "static" interface to classes that are available in the application's [service container](/docs/11.x/container). Laravel ships with many facades which provide access to almost all of Laravel's features. -->
Laravel 공식 문서 전반에서, Laravel의 기능과 상호작용하는 예제 코드에 “파사드(facade)”가 자주 등장하는 것을 볼 수 있습니다. 파사드는 애플리케이션의 [service container](/docs/11.x/container)에 등록된 클래스를 “정적(static)” 인터페이스처럼 사용할 수 있게 해주는 기능입니다. Laravel은 파사드를 통해 거의 모든 기능에 접근할 수 있도록 여러 파사드를 기본 제공하고 있습니다.

<!-- Laravel facades serve as "static proxies" to underlying classes in the service container, providing the benefit of a terse, expressive syntax while maintaining more testability and flexibility than traditional static methods. It's perfectly fine if you don't totally understand how facades work - just go with the flow and continue learning about Laravel. -->
Laravel 파사드는 서비스 컨테이너 내부의 클래스에 대해 “정적 프록시” 역할을 하며, 간결하고 표현력이 뛰어난 문법을 제공함과 동시에, 전통적인 정적(static) 메서드 방식보다 테스트하기 쉽고 유연합니다. 파사드가 내부적으로 어떻게 동작하는지 완전히 이해하지 못해도 괜찮습니다. 일단 편하게 사용하며 Laravel을 익히다 보면 자연스럽게 이해하게 됩니다.

<!-- All of Laravel's facades are defined in the `Illuminate\Support\Facades` namespace. So, we can easily access a facade like so: -->
Laravel의 모든 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 아래와 같이 파사드에 쉽게 접근할 수 있습니다.

```
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

<!-- Throughout the Laravel documentation, many of the examples will use facades to demonstrate various features of the framework. -->
Laravel 공식 문서에서는 다양한 기능을 설명할 때, 파사드를 활용한 예제를 많이 사용합니다.

<a name="helper-functions"></a>
<!-- #### Helper Functions -->
#### Helper Functions

<!-- To complement facades, Laravel offers a variety of global "helper functions" that make it even easier to interact with common Laravel features. Some of the common helper functions you may interact with are `view`, `response`, `url`, `config`, and more. Each helper function offered by Laravel is documented with their corresponding feature; however, a complete list is available within the dedicated [helper documentation](/docs/11.x/helpers). -->
파사드와 더불어, Laravel은 일반적인 기능을 더욱 쉽게 사용할 수 있도록 다양한 전역 “헬퍼 함수”도 제공합니다. 자주 사용되는 헬퍼 함수로는 `view`, `response`, `url`, `config` 등이 있으며, 이 외에도 여러 가지가 있습니다. 각각의 헬퍼 함수는 관련 기능의 문서에서 다루고 있지만, 모든 헬퍼 함수 목록은 별도의 [helper documentation](/docs/11.x/helpers)에서 확인할 수 있습니다.

<!-- For example, instead of using the `Illuminate\Support\Facades\Response` facade to generate a JSON response, we may simply use the `response` function. Because helper functions are globally available, you do not need to import any classes in order to use them: -->
예를 들어, `Illuminate\Support\Facades\Response` 파사드를 사용해 JSON 응답을 생성하는 대신, 아래처럼 `response` 헬퍼 함수를 바로 사용할 수도 있습니다. 헬퍼 함수는 전역에서 바로 사용할 수 있으므로, 별도의 클래스를 import할 필요가 없습니다.

```
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
파사드는 여러 장점이 있습니다. 길고 복잡한 클래스 이름을 일일이 기억하거나 직접 주입/설정하지 않아도, 간결하고 기억하기 쉬운 문법으로 Laravel의 다양한 기능을 바로 사용할 수 있습니다. 그리고, PHP의 동적 메서드 호출 방식을 활용하기 때문에 테스트하기도 편리합니다.

<!-- However, some care must be taken when using facades. The primary danger of facades is class "scope creep". Since facades are so easy to use and do not require injection, it can be easy to let your classes continue to grow and use many facades in a single class. Using dependency injection, this potential is mitigated by the visual feedback a large constructor gives you that your class is growing too large. So, when using facades, pay special attention to the size of your class so that its scope of responsibility stays narrow. If your class is getting too large, consider splitting it into multiple smaller classes. -->
하지만 파사드를 사용할 때 몇 가지 주의해야 할 점이 있습니다. 가장 큰 위험 요인은 클래스의 “스코프 크리프(scope creep)” 현상입니다. 파사드는 너무 쉽게 사용할 수 있고 별도의 의존성 주입 없이 바로 쓸 수 있기 때문에, 한 클래스 안에서 점점 더 많은 파사드를 사용하게 되고, 클래스가 비대해지기 쉽습니다. 의존성 주입을 사용할 때는 생성자가 점점 길어지면서 “이 클래스가 너무 비대해지진 않았나?”란 경계 신호를 시각적으로 확인할 수 있습니다. 반면, 파사드만 써버릇하면 이런 경고등을 놓치기 쉽기 때문에, 클래스가 쓸데없이 방대해지지 않도록 더욱 신경 써야 합니다. 만약 클래스가 너무 커진다고 느껴진다면, 여러 개의 더 작은 클래스로 쪼개는 것을 고려해보십시오.

<a name="facades-vs-dependency-injection"></a>
<!-- ### Facades vs. Dependency Injection -->
### Facades vs. Dependency Injection

<!-- One of the primary benefits of dependency injection is the ability to swap implementations of the injected class. This is useful during testing since you can inject a mock or stub and assert that various methods were called on the stub. -->
의존성 주입의 가장 큰 장점 중 하나는 주입받는 클래스의 구현을 쉽게 교체할 수 있다는 점입니다. 예를 들어 테스트 환경에서는, 진짜 객체 대신 mock이나 stub을 주입해서 메서드가 정상적으로 호출되는지 검증할 수 있습니다.

<!-- Typically, it would not be possible to mock or stub a truly static class method. However, since facades use dynamic methods to proxy method calls to objects resolved from the service container, we actually can test facades just as we would test an injected class instance. For example, given the following route: -->
전통적인 정적 클래스 메서드는 mock이나 stub으로 대체하기가 불가능합니다. 하지만, 파사드는 서비스를 동적으로 서비스 컨테이너에서 resolve해서 메서드를 위임하기 때문에, 실제로는 의존성 주입에 사용하는 인스턴스처럼 똑같이 테스트를 작성할 수 있습니다. 아래의 라우트를 보시면,

```
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

<!-- Using Laravel's facade testing methods, we can write the following test to verify that the `Cache::get` method was called with the argument we expected: -->
Laravel에서 제공하는 파사드 테스트 기능을 활용해, 아래와 같이 `Cache::get` 메서드가 해당 인수로 호출되었는지 손쉽게 테스트할 수 있습니다.

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
파사드 외에도, Laravel에서는 뷰 생성, 이벤트 발생, 작업(Job) 디스패치, HTTP 응답 전송 등 다양한 작업을 쉽게 수행할 수 있는 “헬퍼 함수”들도 제공합니다. 이들 헬퍼 함수 중 상당수는 파사드와 동일한 기능을 수행합니다. 예를 들어, 아래의 파사드 호출과 헬퍼 함수 호출은 완전히 동일한 동작을 합니다.

```
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

<!-- There is absolutely no practical difference between facades and helper functions. When using helper functions, you may still test them exactly as you would the corresponding facade. For example, given the following route: -->
파사드와 헬퍼 함수 사이에는 실제 동작의 차이가 전혀 없습니다. 헬퍼 함수를 사용할 때도, 해당 파사드와 완전히 동일한 방식으로 테스트할 수 있습니다. 아래와 같은 라우트가 있다고 해봅시다.

```
Route::get('/cache', function () {
    return cache('key');
});
```

<!-- The `cache` helper is going to call the `get` method on the class underlying the `Cache` facade. So, even though we are using the helper function, we can write the following test to verify that the method was called with the argument we expected: -->
이때 `cache` 헬퍼는 내부적으로 `Cache` 파사드의 기반 클래스의 `get` 메서드를 호출합니다. 즉, 헬퍼 함수를 사용하더라도, 아래처럼 동일하게 원하는 메서드가 의도한 인수로 호출되었는지 테스트할 수 있습니다.

```
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
Laravel 애플리케이션에서 파사드는 컨테이너에 등록된 객체에 접근할 수 있게 해주는 클래스입니다. 이 동작을 가능하게 하는 핵심이 바로 `Facade` 클래스입니다. Laravel에서 제공하는 파사드는 물론, 직접 만드는 커스텀 파사드도 모두 기본 `Illuminate\Support\Facades\Facade` 클래스를 상속받아서 구현합니다.

<!-- The `Facade` base class makes use of the `__callStatic()` magic-method to defer calls from your facade to an object resolved from the container. In the example below, a call is made to the Laravel cache system. By glancing at this code, one might assume that the static `get` method is being called on the `Cache` class: -->
`Facade`의 핵심 기능은 `__callStatic()` 매직 메서드입니다. 이 매직 메서드는 파사드에서 호출된 메서드를 컨테이너에서 resolve한 실제 객체로 위임합니다. 아래 예제를 살펴보면, Laravel의 캐시 시스템에 접근하는 모습이 보입니다. 이 코드를 보면, `Cache` 클래스의 정적 메서드인 `get`이 호출되는 것처럼 보입니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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
파일 상단 부분에 `Cache` 파사드를 import하고 있는 것을 볼 수 있습니다. 이 파사드는 `Illuminate\Contracts\Cache\Factory` 인터페이스의 실제 구현체에 접근할 수 있는 프록시 역할을 하며, 우리가 파사드를 통해 호출하는 모든 메서드는 내부적으로 Laravel의 캐시 서비스 인스턴스에 요청이 전달됩니다.

<!-- If we look at that `Illuminate\Support\Facades\Cache` class, you'll see that there is no static method `get`: -->
실제로 `Illuminate\Support\Facades\Cache` 클래스의 내용을 들여다보면, `get`이라는 정적 메서드는 아예 존재하지 않습니다.

```
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

<!-- Instead, the `Cache` facade extends the base `Facade` class and defines the method `getFacadeAccessor()`. This method's job is to return the name of a service container binding. When a user references any static method on the `Cache` facade, Laravel resolves the `cache` binding from the [service container](/docs/11.x/container) and runs the requested method (in this case, `get`) against that object. -->
대신, `Cache` 파사드는 기본 `Facade` 클래스를 상속받고, `getFacadeAccessor()` 메서드를 정의하고 있습니다. 이 메서드는 서비스 컨테이너에 바인딩된 이름을 반환하는 역할을 합니다. 사용자가 `Cache` 파사드에서 어떤 정적 메서드를 호출하면, Laravel은 [service container](/docs/11.x/container)에서 `cache` 바인딩을 resolve해서 요청한 메서드(이 경우에는 `get`)를 실제 객체에 대해 실행합니다.

<a name="real-time-facades"></a>
<!-- ## Real-Time Facades -->
## Real-Time Facades

<!-- Using real-time facades, you may treat any class in your application as if it was a facade. To illustrate how this can be used, let's first examine some code that does not use real-time facades. For example, let's assume our `Podcast` model has a `publish` method. However, in order to publish the podcast, we need to inject a `Publisher` instance: -->
실시간 파사드(real-time facade)를 사용하면, 애플리케이션의 어떤 클래스도 파사드처럼 사용할 수 있습니다. 먼저, 실시간 파사드를 사용하지 않은 예제를 살펴보겠습니다. `Podcast` 모델에 `publish`라는 메서드가 있고, 팟캐스트를 발행하려면 `Publisher` 인스턴스를 주입받아야 한다고 가정해봅시다.

```
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
이런 식으로 퍼블리셔 구현체를 메서드에 주입하면, 테스트 환경에서는 퍼블리셔를 mock 등으로 대체해 독립적으로 테스트할 수 있습니다. 단, 이렇게 하면 `publish` 메서드를 호출할 때마다 항상 퍼블리셔 인스턴스를 직접 넘겨줘야 하는 번거로움이 있습니다. 실시간 파사드를 활용하면, 테스트의 용이함은 그대로 유지하면서도 `Publisher` 인스턴스를 명시적으로 넘기지 않아도 됩니다. 실시간 파사드를 적용하려면, import 구문에서 클래스 네임스페이스 앞에 `Facades`를 붙이면 됩니다.

```
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
실시간 파사드를 사용하면, 퍼블리셔 구현체가 서비스 컨테이너에서 자동으로 resolve됩니다. 이때 `Facades` 접두사 뒤에 오는 인터페이스 또는 클래스 이름이 기준이 됩니다. 테스트할 때도 Laravel의 파사드 테스트 헬퍼를 그대로 사용하여 메서드 호출을 mock 처리할 수 있습니다.

```php tab=Pest
<?php

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

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

<!-- Below you will find every facade and its underlying class. This is a useful tool for quickly digging into the API documentation for a given facade root. The [service container binding](/docs/11.x/container) key is also included where applicable. -->
아래에서는 각 파사드가 어떤 클래스를 기반으로 하는지, 그리고 관련된 [service container binding](/docs/11.x/container) 키가 무엇인지 모두 표로 정리했습니다. 특정 파사드의 내부 구현이나 API 문서를 빠르게 살펴보고 싶을 때 유용하게 활용할 수 있습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 파사드 | 클래스 | 서비스 컨테이너 바인딩 |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://laravel.com/api/11.x/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/11.x/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth (Instance) | [Illuminate\Contracts\Auth\Guard](https://laravel.com/api/11.x/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://laravel.com/api/11.x/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/11.x/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (Instance) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://laravel.com/api/11.x/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://laravel.com/api/11.x/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/11.x/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (Instance) | [Illuminate\Cache\Repository](https://laravel.com/api/11.x/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://laravel.com/api/11.x/Illuminate/Cache/CacheManager.html) | `cache` |
| Config | [Illuminate\Config\Repository](https://laravel.com/api/11.x/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://laravel.com/api/11.x/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://laravel.com/api/11.x/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://laravel.com/api/11.x/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://laravel.com/api/11.x/Illuminate/Support/DateFactory.html) | `date` |
| DB (Instance) | [Illuminate\Database\Connection](https://laravel.com/api/11.x/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://laravel.com/api/11.x/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://laravel.com/api/11.x/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (Instance) | [Illuminate\Contracts\Debug\ExceptionHandler](https://laravel.com/api/11.x/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://laravel.com/api/11.x/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://laravel.com/api/11.x/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/11.x/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/11.x/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://laravel.com/api/11.x/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://laravel.com/api/11.x/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://laravel.com/api/11.x/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://laravel.com/api/11.x/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://laravel.com/api/11.x/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (Instance) | [Illuminate\Auth\Passwords\PasswordBroker](https://laravel.com/api/11.x/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/11.x/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (Instance) | [Illuminate\Pipeline\Pipeline](https://laravel.com/api/11.x/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://laravel.com/api/11.x/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (Base Class) | [Illuminate\Queue\Queue](https://laravel.com/api/11.x/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (Instance) | [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/11.x/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://laravel.com/api/11.x/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://laravel.com/api/11.x/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://laravel.com/api/11.x/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (Instance) | [Illuminate\Redis\Connections\Connection](https://laravel.com/api/11.x/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://laravel.com/api/11.x/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://laravel.com/api/11.x/Illuminate/Http/Request.html) | `request` |
| Response (Instance) | [Illuminate\Http\Response](https://laravel.com/api/11.x/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/11.x/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://laravel.com/api/11.x/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://laravel.com/api/11.x/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://laravel.com/api/11.x/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (Instance) | [Illuminate\Session\Store](https://laravel.com/api/11.x/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://laravel.com/api/11.x/Illuminate/Session/SessionManager.html) | `session` |
| Storage (Instance) | [Illuminate\Contracts\Filesystem\Filesystem](https://laravel.com/api/11.x/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://laravel.com/api/11.x/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://laravel.com/api/11.x/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (Instance) | [Illuminate\Validation\Validator](https://laravel.com/api/11.x/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://laravel.com/api/11.x/Illuminate/Validation/Factory.html) | `validator` |
| View (Instance) | [Illuminate\View\View](https://laravel.com/api/11.x/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://laravel.com/api/11.x/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://laravel.com/api/11.x/Illuminate/Foundation/Vite.html) | &nbsp; |

<!-- </div> -->
</div>
