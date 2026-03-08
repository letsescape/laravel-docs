# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [제로 설정(Zero Configuration) 해석](#zero-configuration-resolution)
    - [컨테이너를 사용해야 하는 경우](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩하기](#binding-interfaces-to-implementations)
    - [상황별 바인딩](#contextual-binding)
    - [상황별 속성](#contextual-attributes)
    - [원시값 바인딩](#binding-primitives)
    - [타입 지정 가변 인수 바인딩](#binding-typed-variadics)
    - [태그 지정](#tagging)
    - [바인딩 확장](#extending-bindings)
- [해결(Resolving)](#resolving)
    - [`make` 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출 및 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [리바인딩(Rebinding)](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 서비스 컨테이너는 클래스 의존성 관리와 의존성 주입(Dependency Injection)을 매우 강력하게 지원하는 도구입니다. 의존성 주입이란, 복잡하게 들릴 수 있지만 사실 간단하게 설명하면 클래스가 필요로 하는 의존성 객체(다른 클래스)를 생성자나 때로는 setter 메서드를 통해 "주입"받는다는 의미입니다.

간단한 예제를 살펴보겠습니다.

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

이 예제에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트 정보를 가져와야 합니다. 그래서 이 역할을 수행할 수 있는 서비스를 **주입**합니다. 이렇게 서비스를 주입함으로써, 테스트 시에는 `AppleMusic` 서비스의 더미(가짜) 구현을 쉽게 "모킹(mock)"하여 사용하거나 대체할 수 있습니다.

Laravel 서비스 컨테이너를 깊이 있게 이해하는 것은 강력하고 큰 규모의 애플리케이션을 개발할 때 필수적이며, Laravel 코어 자체에 기여하고자 할 때도 꼭 필요한 지식입니다.

<a name="zero-configuration-resolution"></a>
### 제로 설정 해석 (Zero Configuration Resolution)

클래스가 별도의 의존성이 없거나, 인터페이스가 아니라 구체적인(具體的, concrete) 클래스만을 의존할 경우, 컨테이너는 그 클래스를 어떻게 해석해야 하는지 따로 지시하지 않아도 됩니다. 예를 들어, 아래와 같이 `routes/web.php` 파일 내에 코드를 작성할 수 있습니다.

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

이 예제에서, 애플리케이션의 `/` 경로에 접속하면 `Service` 클래스가 자동으로 해석되어 해당 경로의 핸들러에 주입됩니다. 이것은 매우 혁신적인 기능입니다. 즉, 복잡한 설정 파일 작성 없이도 의존성 주입의 이점을 마음껏 활용하며 애플리케이션을 개발할 수 있다는 뜻입니다.

다행히도, Laravel 애플리케이션 개발 시 작성하게 되는 대부분의 클래스는 컨테이너가 의존성을 자동으로 주입해줍니다. [컨트롤러](/docs/master/controllers), [이벤트 리스너](/docs/master/events), [미들웨어](/docs/master/middleware) 등도 모두 해당됩니다. 또한 [큐 작업](/docs/master/queues)의 `handle` 메서드에 타입 힌트를 지정하여 의존성을 바로 주입받을 수 있습니다. 자동 의존성 주입과 제로 설정을 한 번 경험해 보면, 이를 빼고 개발을 상상하기 어려울 정도가 됩니다.

<a name="when-to-use-the-container"></a>
### 컨테이너를 사용해야 하는 경우 (When to Utilize the Container)

제로 설정 해석 덕분에, 라우트, 컨트롤러, 이벤트 리스너, 기타 여러 곳에서 별도의 컨테이너 조작 없이 타입 힌트만으로 손쉽게 의존성 주입을 할 수 있습니다. 예를 들어, 현재 요청 정보를 손쉽게 사용하기 위해 라우트 정의에 `Illuminate\Http\Request` 객체만 타입 힌트하면 됩니다. 우리가 컨테이너와 직접 상호작용하는 코드가 없음에도, 컨테이너는 이 의존성을 자동으로 주입해줍니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

대부분의 경우, 자동 의존성 주입과 [파사드](/docs/master/facades) 덕분에 컨테이너를 직접 바인딩하거나 해석할 필요 없이 Laravel 애플리케이션을 개발할 수 있습니다.  
**그렇다면 언제 직접 컨테이너와 상호작용해야 할까요?** 다음 두 가지 대표적인 상황이 있습니다.

1. 인터페이스를 구현하는 클래스를 작성하고, 라우트나 생성자에서 해당 인터페이스를 타입 힌트하고 싶을 때는 [컨테이너에 해당 인터페이스의 구현체를 바인딩](#binding-interfaces-to-implementations)해야 합니다.
2. [패키지 개발](/docs/master/packages)을 하여 다른 Laravel 개발자와 공유하려는 경우, 패키지의 서비스를 컨테이너에 직접 바인딩해야 할 수 있습니다.

<a name="binding"></a>
## 바인딩 (Binding)

<a name="binding-basics"></a>
### 바인딩 기본

<a name="simple-bindings"></a>
#### 단순 바인딩

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/master/providers) 내에서 등록됩니다. 아래 모든 예제는 이 컨텍스트에서 컨테이너 사용법을 설명합니다.

서비스 프로바이더에서는 항상 `$this->app` 프로퍼티를 통해 컨테이너에 접근할 수 있습니다. 바인딩할 클래스 또는 인터페이스명과, 해당 클래스의 인스턴스를 반환하는 클로저를 `bind` 메서드에 전달하여 바인딩을 등록할 수 있습니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

여기서 해석기(클로저)는 컨테이너 자체를 인수로 받습니다. 이를 통해 객체를 생성할 때 필요한 하위 의존성도 컨테이너를 활용하여 해석할 수 있습니다.

앞서 설명했듯, 주로 서비스 프로바이더 내에서 컨테이너와 상호작용하게 됩니다. 만약 서비스 프로바이더 밖에서 컨테이너를 다루어야 한다면, `App` [파사드](/docs/master/facades)를 사용할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

이미 해당 타입에 대해 바인딩이 등록되어 있지 않은 경우에만 바인딩하려면 `bindIf` 메서드를 사용할 수 있습니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

더 편리하게, 바인딩할 클래스나 인터페이스명을 별도 인수로 전달하지 않고, 클로저의 반환 타입에서 자동으로 해당 타입을 추론하게 할 수도 있습니다.

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 어떤 클래스가 인터페이스에 의존하지 않는다면 컨테이너에 해당 클래스를 바인딩할 필요가 없습니다. 컨테이너가 리플렉션(reflection)을 이용해 자동으로 이런 객체들을 해석할 수 있기 때문입니다.

<a name="binding-a-singleton"></a>
#### 싱글턴 바인딩

`singleton` 메서드는 클래스나 인터페이스를 컨테이너에 한 번만 해석(생성)되도록 바인딩합니다. 한 번 싱글턴 바인딩이 해석되면, 이후 컨테이너에서 해당 타입을 요청할 때마다 동일한 인스턴스가 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

이미 싱글턴 바인딩이 없다면 등록하는 `singletonIf` 메서드도 사용할 수 있습니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="singleton-attribute"></a>
#### 싱글턴 속성(Attribute)

또는 인터페이스나 클래스에 `#[Singleton]` 속성을 지정하여, 컨테이너가 한 번만 해석해야 함을 알릴 수 있습니다.

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
#### 범위(Scoped) 싱글턴 바인딩

`scoped` 메서드는 클래스나 인터페이스를, 각 Laravel 요청/작업(job) 생명주기에서 한 번만 해석되도록 바인딩합니다. `singleton`과 비슷하나, `scoped`로 등록한 인스턴스는 [Laravel Octane](/docs/master/octane) 워커가 새 요청을 처리하거나, [큐 작업자](/docs/master/queues)가 새로운 작업을 처리할 때마다 플러시(초기화)됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

이미 바인딩이 없을 경우에만 등록하는 `scopedIf` 메서드도 사용할 수 있습니다.

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="scoped-attribute"></a>
#### 범위(Scoped) 속성(Attribute)

또는 인터페이스나 클래스에 `#[Scoped]` 속성을 지정하여, 컨테이너가 각 요청/작업 생명주기에서 한 번만 해석하도록 지정할 수 있습니다.

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
#### 인스턴스 바인딩

기존에 생성한 객체 인스턴스를 컨테이너에 바인딩하려면 `instance` 메서드를 사용합니다. 이렇게 등록한 인스턴스는 이후 컨테이너에서 해당 타입을 요청할 때마다 항상 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 매우 강력한 기능 중 하나는, 인터페이스에 대해 원하는 구현체를 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 `RedisEventPusher` 구현체가 있다고 가정해보겠습니다.  
`RedisEventPusher` 구현체를 작성한 뒤, 아래와 같이 컨테이너에 등록할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이 코드는, `EventPusher` 구현체가 필요한 클래스에 컨테이너가 `RedisEventPusher`를 주입하도록 지시합니다. 이제 컨테이너로 해석되는 클래스의 생성자에서 `EventPusher` 인터페이스로 타입 힌트할 수 있습니다. 컨트롤러, 이벤트 리스너, 미들웨어 등은 모두 컨테이너를 통해 해석됩니다.

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
#### 바인드 속성(Bind Attribute)

Laravel은 더욱 편리하게 사용할 수 있도록 `Bind` 속성(Attribute)도 제공합니다. 이 속성을 인터페이스에 지정하면, 해당 인터페이스가 필요할 때 어떤 구현체를 자동으로 주입해야 하는지 명시할 수 있습니다.  
`Bind` 속성을 사용할 때는 서비스 프로바이더에서 별도의 바인딩 등록이 필요 없습니다.

또한, 여러 개의 `Bind` 속성을 사용할 수 있어, 환경에 따라 주입할 구현체를 다르게 지정할 수 있습니다.

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

더불어, [Singleton](#singleton-attribute)과 [Scoped](#scoped-attribute) 속성을 함께 지정해 해당 컨테이너 바인딩이 한 번만, 또는 각 요청/작업 생명주기 마다 한 번만 해석되도록 할 수 있습니다.

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
### 상황별 바인딩 (Contextual Binding)

어떤 경우에는 동일한 인터페이스를 사용하는 두 클래스에 서로 다른 구현체를 주입하고 싶을 수 있습니다. 예를 들어, 두 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [컨트랙트](/docs/master/contracts)의 서로 다른 구현체에 의존한다면, 아래와 같이 상황별 바인딩을 구성할 수 있습니다.

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
### 상황별 속성 (Contextual Attributes)

상황별 바인딩은 주로 드라이버 구현체나 특정 설정 값을 주입하는 데 사용됩니다. Laravel은 이런 값을 서비스 프로바이더에 직접 바인딩하지 않고도 속성(Attribute) 방식으로 손쉽게 주입할 수 있도록 여러 상황별 바인딩 속성을 제공합니다.

예를 들어, `Storage` 속성으로 특정 [스토리지 디스크](/docs/master/filesystem)를 주입할 수 있습니다.

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

`Storage` 외에도 Laravel은 `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RouteParameter`, 그리고 [Tag](#tagging) 속성을 제공합니다.

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

또한, 현재 인증된 사용자를 해당 라우트 또는 클래스에 주입하기 위한 `CurrentUser` 속성도 제공합니다.

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 커스텀 속성 정의하기

`Illuminate\Contracts\Container\ContextualAttribute` 컨트랙트를 구현하여, 직접 커스텀 상황별 속성을 만들 수도 있습니다. 컨테이너는 속성의 `resolve` 메서드를 호출하며, 이 메서드는 해당 속성이 붙은 곳에 어떤 값을 주입할지 해석합니다. 아래는 Laravel 내장 `Config` 속성을 재구현한 예시입니다.

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
### 원시값 바인딩 (Binding Primitives)

클래스가 다른 클래스 의존성을 주입받을 뿐만 아니라, 정수와 같은 원시값(primitive value)도 주입받아야 할 때가 있습니다. 상황별 바인딩을 사용하면 아래와 같이 어떤 값이든 주입할 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

어떤 클래스가 [태그 지정된](#tagging) 인스턴스의 배열에 의존한다면, `giveTagged` 메서드를 사용해 해당 태그의 바인딩 전체를 손쉽게 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션의 설정 파일에 정의된 값을 주입해야 한다면, `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입 지정 가변 인수 바인딩 (Binding Typed Variadics)

가끔 클래스가 가변 인수(varidic: ...) 형식으로 타입이 지정된 객체 배열을 생성자에서 받는 경우가 있습니다.

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

상황별 바인딩에서, `give` 메서드에 클로저를 전달하고 그 안에서 `Filter` 인스턴스 배열을 반환하게 하면, 이 의존성을 해결할 수 있습니다.

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

더 간단하게, `Firewall`에서 `Filter` 인스턴스가 필요할 때마다 컨테이너가 아래 클래스명 배열을 해석해 인스턴스를 주입하도록 할 수도 있습니다.

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
#### 가변 인수 태그 의존성

가변 인수 의존성이 특정 클래스(`Report ...$reports`) 타입 힌트로 선언된 경우, `needs`와 `giveTagged` 메서드를 이용해 지정된 [태그](#tagging)의 바인딩 전체를 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태그 지정 (Tagging)

특정 "카테고리"에 속한 모든 바인딩을 한 번에 해석해야 할 일이 있을 수 있습니다. 예를 들어, 여러 가지 `Report` 인터페이스 구현체 배열을 받아 분석하는 리포트 분석기를 만든다고 가정해보겠습니다.  
각 `Report` 구현체를 바인딩한 뒤, `tag` 메서드를 사용해 태그를 부여할 수 있습니다.

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

서비스에 태그가 부여된 후에는, 컨테이너의 `tagged` 메서드를 통해 태그된 모든 바인딩을 쉽게 해석할 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장 (Extending Bindings)

`extend` 메서드를 사용하면 이미 해석된 서비스 객체를 수정할 수 있습니다. 예를 들어, 어느 서비스가 해석될 때 추가적인 데코레이션이나 설정 작업을 하고 싶다면 아래와 같이 사용할 수 있습니다.  
`extend`는 두 개의 인수(확장할 서비스 클래스, 수정 후 객체를 반환하는 클로저)를 받으며, 클로저는 해석된 서비스 인스턴스와 컨테이너 인스턴스를 전달받습니다.

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결 (Resolving)

<a name="the-make-method"></a>
### `make` 메서드

`make` 메서드를 사용하여 컨테이너에서 클래스 인스턴스를 해석할 수 있습니다. 이 메서드는 해석하고자 하는 클래스 또는 인터페이스명을 인수로 받습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

해석하려는 클래스의 일부 의존성을 컨테이너가 해결할 수 없는 경우, `makeWith` 메서드에 생성자 인수를 연관 배열로 직접 전달해 줄 수도 있습니다.  
예를 들어, `Transistor` 서비스가 `$id` 생성자 인수를 필요로 한다면 아래와 같이 사용할 수 있습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드를 사용하면 클래스 또는 인터페이스가 컨테이너에 명시적으로 바인딩되어 있는지 확인할 수 있습니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 바깥 등 `$app` 변수에 접근할 수 없는 환경에서는, `App` [파사드](/docs/master/facades) 또는 `app` [헬퍼](/docs/master/helpers#method-app)를 사용해 컨테이너에서 클래스 인스턴스를 해석할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

컨테이너 자체 인스턴스를 주입받고 싶다면, 클래스 생성자에 `Illuminate\Container\Container` 클래스를 타입 힌트하세요.

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
### 자동 주입 (Automatic Injection)

이와 더불어, 컨테이너에서 해석되는 클래스의 생성자에서 의존성을 타입 힌트 하면 자동으로 주입됩니다. 이 방식은 [컨트롤러](/docs/master/controllers), [이벤트 리스너](/docs/master/events), [미들웨어](/docs/master/middleware) 등에서 특히 자주 쓰이며, [큐 작업](/docs/master/queues)의 `handle` 메서드에도 동일하게 적용할 수 있습니다.  
실제 개발에서는 대부분의 객체가 이 방식으로 컨테이너에 의해 해석됩니다.

예를 들어, 컨트롤러 생성자에 애플리케이션에서 정의한 서비스를 타입 힌트하면, 해당 서비스가 자동으로 주입됩니다.

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
## 메서드 호출 및 주입 (Method Invocation and Injection)

객체 인스턴스의 메서드를 호출할 때, 그 메서드 의존성도 컨테이너가 자동으로 주입해주길 원할 때가 있습니다.  
예를 들어 아래와 같은 클래스가 있다고 가정합니다.

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

이때 `generate` 메서드를 컨테이너를 통해 아래와 같이 호출할 수 있습니다.

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 아무 PHP 콜러블(callable)이든 받을 수 있습니다.  
컨테이너의 `call` 메서드는 클로저도 받아들이며, 이 경우에도 의존성이 자동 주입됩니다.

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트 (Container Events)

서비스 컨테이너는 객체를 해석할 때마다 이벤트를 발생시킵니다. `resolving` 메서드를 사용해 이 이벤트를 수신할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입 객체가 컨테이너에서 해석될 때 호출됨...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 모든 타입의 객체가 해석될 때 호출됨...
});
```

이처럼, 해석된 객체가 콜백에 전달되므로, 객체를 최종적으로 소비자에게 전달하기 전 추가 설정이 가능합니다.

<a name="rebinding"></a>
### 리바인딩 (Rebinding)

`rebinding` 메서드를 사용하면 서비스가 컨테이너에 재등록(초기 바인딩 이후 교체 또는 덮어쓰기)될 때마다 수신할 수 있습니다. 이 기능은 특정 바인딩이 갱신될 때마다 의존성을 갱신하거나 동작을 수정할 필요가 있을 때 활용할 수 있습니다.

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

// 새 바인딩이 리바인딩 콜백을 트리거함...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

Laravel의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서, PSR-11 컨테이너 인터페이스를 타입 힌트하여 Laravel 컨테이너 인스턴스에 접근할 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

주어진 식별자를 해석하지 못하면 예외가 발생합니다.  
식별자가 한 번도 바인딩된 적 없다면 `Psr\Container\NotFoundExceptionInterface` 인스턴스가, 바인딩되었으나 해석할 수 없다면 `Psr\Container\ContainerExceptionInterface` 인스턴스 예외가 발생합니다.
