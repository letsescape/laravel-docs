# 파사드 (Facades)

- [소개](#introduction)
- [파사드를 사용할 때](#when-to-use-facades)
    - [파사드 vs. 의존성 주입](#facades-vs-dependency-injection)
    - [파사드 vs. 헬퍼 함수](#facades-vs-helper-functions)
- [파사드는 어떻게 동작하는가](#how-facades-work)
- [실시간 파사드(Real-Time Facades)](#real-time-facades)
- [파사드 클래스 레퍼런스](#facade-class-reference)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 공식 문서 전반에서는 Laravel의 다양한 기능과 상호작용하는 코드 예제에서 "파사드(Facade)"를 자주 볼 수 있습니다. 파사드는 애플리케이션의 [서비스 컨테이너](/docs/master/container) 내의 클래스에 대해 "정적(static)" 인터페이스를 제공합니다. Laravel은 거의 모든 기능에 접근할 수 있는 다양한 파사드를 기본적으로 제공합니다.

Laravel의 파사드는 서비스 컨테이너 내부 클래스에 대한 "정적 프록시(static proxy)" 역할을 하며, 간결하면서도 표현력이 뛰어난 문법을 제공하여 전통적인 정적 메서드보다 뛰어난 테스트 용이성 및 유연성을 확보할 수 있게 해줍니다. 파사드가 어떻게 동작하는지 완전히 이해하지 못해도 괜찮으니 일단 자연스럽게 Laravel을 따라 학습해 나가시면 됩니다.

Laravel의 모든 파사드는 `Illuminate\Support\Facades` 네임스페이스에 정의되어 있습니다. 따라서 아래와 같이 쉽게 파사드를 불러와 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel 문서 곳곳의 다양한 예제에서는 프레임워크의 여러 기능을 설명할 때 파사드를 사용합니다.

<a name="helper-functions"></a>
#### 헬퍼 함수

파사드를 보완하기 위해, Laravel은 공통적으로 사용되는 기능을 더욱 쉽게 사용할 수 있도록 다양한 글로벌 "헬퍼 함수"도 제공합니다. 자주 사용되는 헬퍼 함수로는 `view`, `response`, `url`, `config` 등이 있습니다. Laravel에서 제공하는 각 헬퍼 함수는 해당 기능의 문서에서 자세히 설명되어 있으며, 전체 목록은 별도의 [헬퍼 함수 문서](/docs/master/helpers)에서 확인할 수 있습니다.

예를 들어, `Illuminate\Support\Facades\Response` 파사드를 사용해 JSON 응답을 생성하는 대신, 아래처럼 `response` 헬퍼 함수를 사용할 수 있습니다. 헬퍼 함수는 전역적으로 사용할 수 있으므로 별도의 클래스를 import할 필요가 없습니다.

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
## 파사드를 사용할 때 (When to Utilize Facades)

파사드는 여러 장점이 있습니다. 파사드를 이용하면 복잡한 클래스명을 기억하거나 직접 주입하거나 별도로 설정할 필요 없이, Laravel의 기능을 쉽고 명확하게 사용할 수 있습니다. 뿐만 아니라, PHP의 동적 메서드(Dynamic methods)를 독특하게 활용하고 있어 테스트 작성도 매우 편합니다.

다만, 파사드를 사용할 때 주의할 점도 있습니다. 파사드는 너무 쉽게 사용할 수 있기 때문에, 한 클래스 안에서 너무 많은 파사드를 사용하게 되는 소위 "클래스 범위 확장(scope creep)" 문제가 발생할 수 있습니다. 반면, 의존성 주입을 사용할 경우 생성자(Constructor)가 점점 커진다는 시각적 단서를 통해 클래스가 커지고 있음을 쉽게 인지할 수 있으나, 파사드는 이런 부분이 감춰질 수 있습니다. 따라서 파사드를 사용할 때는 클래스의 규모가 커지지 않도록 특히 신경써야 합니다. 만약 클래스가 점점 커진다면, 여러 개의 작은 클래스로 나누는 것을 고려하세요.

<a name="facades-vs-dependency-injection"></a>
### 파사드 vs. 의존성 주입 (Facades vs. Dependency Injection)

의존성 주입의 가장 큰 장점 중 하나는, 주입된 클래스 구현체를 쉽게 교체할 수 있다는 점입니다. 이 기능은 테스트 과정에서 특히 유용하게 쓰이는데, 목(mock) 객체나 스텁(stub)을 주입하여 특정 메서드 호출을 확인할 수 있기 때문입니다.

전통적인 정적 클래스 메서드는 목이나 스텁으로 교체하기 어렵지만, 파사드는 동적 메서드를 사용하여, 컨테이너에서 객체를 가져와 메서드 호출을 위임하므로, 실제로 파사드 역시 의존성 주입된 인스턴스처럼 테스트가 가능합니다. 아래는 그 예시입니다.

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

Laravel의 파사드 테스트 메서드를 이용하면, `Cache::get` 메서드가 우리가 원하는 인수로 호출되었는지 다음과 같이 테스트할 수 있습니다.

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
### 파사드 vs. 헬퍼 함수 (Facades vs. Helper Functions)

파사드 외에도 Laravel에는 뷰를 생성하거나, 이벤트를 발생시키거나, 작업(job)을 디스패치하거나, HTTP 응답을 반환하는 등 흔하게 쓰이는 작업을 수행할 수 있는 다양한 "헬퍼" 함수가 있습니다. 대부분의 헬퍼 함수는 대응하는 파사드와 동일한 기능을 제공합니다. 아래 두 코드는 같은 동작을 수행합니다.

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

파사드와 헬퍼 함수 사이에는 사용상 아무런 실질적 차이가 없습니다. 헬퍼 함수를 사용할 때도, 파사드에서처럼 동일하게 테스트할 수 있습니다. 예를 들어, 아래 라우트에서

```php
Route::get('/cache', function () {
    return cache('key');
});
```

`cache` 헬퍼 함수는 내부적으로 `Cache` 파사드가 감싸고 있는 클래스의 `get` 메서드를 호출합니다. 따라서 헬퍼 함수를 사용해도, 우리가 기대한 인수로 해당 메서드가 호출되는지를 다음과 같이 테스트할 수 있습니다.

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
## 파사드는 어떻게 동작하는가 (How Facades Work)

Laravel 애플리케이션에서 파사드는 컨테이너에서 객체에 접근할 수 있도록 해주는 클래스입니다. 이러한 동작을 가능하게 하는 구조는 `Facade` 클래스에 구현되어 있습니다. Laravel이 기본 제공하는 파사드나 여러분이 직접 생성하는 파사드는 모두 `Illuminate\Support\Facades\Facade` 클래스에서 상속받습니다.

`Facade` 기본 클래스는 PHP의 매직 메서드인 `__callStatic()`을 사용하여, 파사드를 통한 메서드 호출을 컨테이너에서 가져온 객체로 위임합니다. 아래 예제에서는 Laravel 캐시(Cache) 시스템을 호출하는 모습을 볼 수 있습니다. 얼핏 보면 `Cache` 클래스의 정적(static) 메서드인 `get`이 호출되었다고 생각할 수 있습니다.

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

파일 상단에서 `Cache` 파사드를 import해서 사용하고 있습니다. 이 파사드는 내부적으로 `Illuminate\Contracts\Cache\Factory` 인터페이스의 구현체에 접근할 수 있도록 프록시 역할을 합니다. 파사드를 이용한 모든 호출은 실제로 Laravel의 캐시 서비스 인스턴스로 위임됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 살펴보면, 정적 메서드 `get` 자체는 존재하지 않고 다음과 같은 구조로 되어 있습니다.

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

Cache 파사드는 기본 `Facade` 클래스를 확장하고, `getFacadeAccessor()` 메서드를 정의하여 서비스 컨테이너 바인딩의 이름을 반환합니다. 개발자가 `Cache` 파사드의 어떤 정적 메서드를 호출하면, Laravel은 [서비스 컨테이너](/docs/master/container)에서 `cache` 바인딩을 해결하고, 해당 객체에 요청된 메서드(여기서는 `get`)를 실제로 실행합니다.

<a name="real-time-facades"></a>
## 실시간 파사드 (Real-Time Facades)

실시간 파사드(Real-Time Facade)를 사용하면, 애플리케이션 내의 어떤 클래스든 마치 파사드인 것처럼 사용할 수 있습니다. 예시를 통해 차이점을 살펴보겠습니다.

아래 예제를 보시면, `Podcast` 모델에는 `publish`라는 메서드가 있습니다. 여기서 팟캐스트를 게시하기 위해 `Publisher` 인스턴스를 메서드에 주입하고 있습니다.

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

이처럼 구현체를 메서드에 주입하면, 주입된 publisher를 목(mock) 객체로 대체하여 테스트할 수 있기 때문에, 코드의 테스트 용이성이 높아집니다. 단, 매번 `publish` 메서드를 호출할 때마다 publisher를 직접 넘겨줘야 한다는 번거로움이 있습니다. 실시간 파사드를 사용하면, 동일한 테스트 용이성은 유지하면서, publisher 인스턴스를 명시적으로 넘길 필요 없이 메서드를 호출할 수 있습니다. 실시간 파사드를 쓰려면, Import 구문에서 클래스 네임스페이스 앞에 `Facades`를 붙이면 됩니다.

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

실시간 파사드를 사용하면, 클래스명 또는 인터페이스명에서 `Facades` 접두어 뒤의 부분을 기준으로 서비스 컨테이너에서 구현체를 자동으로 가져와서 대신 실행해 줍니다. 테스트할 때도, Laravel이 제공하는 파사드 테스트 헬퍼로 메서드 호출을 목(mock) 처리가 가능합니다.

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
## 파사드 클래스 레퍼런스 (Facade Class Reference)

아래는 각 파사드와 그에 해당하는 실체 클래스, 그리고(해당되는 경우) 서비스 컨테이너 바인딩 키를 정리한 표입니다. 관련 파사드 루트의 API 문서를 빠르게 찾고 싶을 때 활용할 수 있습니다. [서비스 컨테이너 바인딩](/docs/master/container) 키도 함께 참고하세요.

<div class="overflow-auto">

| 파사드 | 클래스 | 서비스 컨테이너 바인딩 |
| --- | --- | --- |
| App | [Illuminate\Foundation\Application](https://api.laravel.com/docs/master/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/master/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| Auth (인스턴스) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/master/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/master/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/master/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| Broadcast (인스턴스) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/master/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/master/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| Bus | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/master/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| Cache (인스턴스) | [Illuminate\Cache\Repository](https://api.laravel.com/docs/master/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/master/Illuminate/Cache/CacheManager.html) | `cache` |
| Config | [Illuminate\Config\Repository](https://api.laravel.com/docs/master/Illuminate/Config/Repository.html) | `config` |
| Context | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/master/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/master/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/master/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| Date | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/master/Illuminate/Support/DateFactory.html) | `date` |
| DB (인스턴스) | [Illuminate\Database\Connection](https://api.laravel.com/docs/master/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/master/Illuminate/Database/DatabaseManager.html) | `db` |
| Event | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/master/Illuminate/Events/Dispatcher.html) | `events` |
| Exceptions (인스턴스) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/master/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| Exceptions | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.com/docs/master/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| File | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/master/Illuminate/Filesystem/Filesystem.html) | `files` |
| Gate | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/master/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| Hash | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/master/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| Http | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/master/Illuminate/Http/Client/Factory.html) | &nbsp; |
| Lang | [Illuminate\Translation\Translator](https://api.laravel.com/docs/master/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://api.laravel.com/docs/master/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/master/Illuminate/Mail/Mailer.html) | `mailer` |
| Notification | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/master/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| Password (인스턴스) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/master/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/master/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| Pipeline (인스턴스) | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/master/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://api.laravel.com/docs/master/Illuminate/Process/Factory.html) | &nbsp; |
| Queue (기본 클래스) | [Illuminate\Queue\Queue](https://api.laravel.com/docs/master/Illuminate/Queue/Queue.html) | &nbsp; |
| Queue (인스턴스) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/master/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/master/Illuminate/Queue/QueueManager.html) | `queue` |
| RateLimiter | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/master/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| Redirect | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/master/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (인스턴스) | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/master/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/master/Illuminate/Redis/RedisManager.html) | `redis` |
| Request | [Illuminate\Http\Request](https://api.laravel.com/docs/master/Illuminate/Http/Request.html) | `request` |
| Response (인스턴스) | [Illuminate\Http\Response](https://api.laravel.com/docs/master/Illuminate/Http/Response.html) | &nbsp; |
| Response | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/master/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://api.laravel.com/docs/master/Illuminate/Routing/Router.html) | `router` |
| Schedule | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/master/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| Schema | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/master/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| Session (인스턴스) | [Illuminate\Session\Store](https://api.laravel.com/docs/master/Illuminate/Session/Store.html) | `session.store` |
| Session | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/master/Illuminate/Session/SessionManager.html) | `session` |
| Storage (인스턴스) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/master/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| Storage | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/master/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/master/Illuminate/Routing/UrlGenerator.html) | `url` |
| Validator (인스턴스) | [Illuminate\Validation\Validator](https://api.laravel.com/docs/master/Illuminate/Validation/Validator.html) | &nbsp; |
| Validator | [Illuminate\Validation\Factory](https://api.laravel.com/docs/master/Illuminate/Validation/Factory.html) | `validator` |
| View (인스턴스) | [Illuminate\View\View](https://api.laravel.com/docs/master/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://api.laravel.com/docs/master/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/master/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>
