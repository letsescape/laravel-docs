# 서비스 컨테이너 (Service Container)

- [소개](#introduction)
    - [제로 설정 자동 해석](#zero-configuration-resolution)
    - [컨테이너 사용 시점](#when-to-use-the-container)
- [바인딩](#binding)
    - [바인딩 기본](#binding-basics)
    - [인터페이스를 구현체에 바인딩](#binding-interfaces-to-implementations)
    - [컨텍스트 바인딩](#contextual-binding)
    - [컨텍스트 속성](#contextual-attributes)
    - [기본형 바인딩](#binding-primitives)
    - [타입 지정 가변 인자 바인딩](#binding-typed-variadics)
    - [태깅](#tagging)
    - [바인딩 확장](#extending-bindings)
- [해결(Resolve)](#resolving)
    - [Make 메서드](#the-make-method)
    - [자동 주입](#automatic-injection)
- [메서드 호출 및 주입](#method-invocation-and-injection)
- [컨테이너 이벤트](#container-events)
    - [리바인딩](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 서비스 컨테이너는 클래스 간의 의존성을 관리하고, 의존성 주입(dependency injection)을 수행하는 데 매우 강력한 도구입니다. 의존성 주입이란, 클래스가 필요로 하는 의존성 객체를 생성자 혹은 일부 경우 ‘세터(setter)’ 메서드를 통해 “주입”하는 방식입니다.

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

이 예제에서 `PodcastController`는 Apple Music과 같은 데이터 소스에서 podcast를 가져올 필요가 있습니다. 이를 위해, podcast를 가져올 수 있는 서비스를 **주입**합니다. 서비스를 주입받으면, 애플리케이션을 테스트할 때 `AppleMusic` 서비스의 모조(mock) 객체나 테스트용 구현체로 쉽게 대체할 수 있습니다.

서비스 컨테이너에 대한 깊은 이해는 강력하고 대규모의 애플리케이션을 구축하거나 Laravel의 코어에 기여할 때 매우 중요합니다.

<a name="zero-configuration-resolution"></a>
### 제로 설정 자동 해석 (Zero Configuration Resolution)

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

이 예제에서 애플리케이션의 `/` 경로로 접속하면, 컨테이너가 `Service` 클래스를 자동으로 해석하여 라우트 핸들러에 주입합니다. 이는 상당한 변화입니다. 즉, 번거로운 설정 파일 없이도, 의존성 주입의 이점을 누리면서 애플리케이션을 개발할 수 있습니다.

다행히도 Laravel 애플리케이션을 개발할 때 작성하는 많은 클래스들은 서비스 컨테이너를 통해 의존성을 자동으로 주입받습니다. 여기에는 [컨트롤러](/docs/12.x/controllers), [이벤트 리스너](/docs/12.x/events), [미들웨어](/docs/12.x/middleware) 등이 포함됩니다. 또한, [큐 작업](/docs/12.x/queues)의 `handle` 메서드에 의존성을 타입힌트로 지정하면 주입받을 수 있습니다. 이런 자동, 무설정(제로 설정) 의존성 주입의 강력함을 한 번 경험하면, 이를 사용하지 않고는 개발할 수 없게 됩니다.

<a name="when-to-use-the-container"></a>
### 컨테이너 사용 시점 (When to Utilize the Container)

제로 설정 자동 해석 덕분에, 라우트, 컨트롤러, 이벤트 리스너 등 여러 곳에서 타입힌트만으로 자연스럽게 의존성을 주입받을 수 있으며, 컨테이너와 직접 상호작용할 필요가 거의 없습니다. 예를 들어, 현재 요청에 쉽게 접근하기 위해 라우트 정의에서 `Illuminate\Http\Request` 객체를 타입힌트로 지정할 수 있습니다. 아래 코드를 작성할 때 컨테이너와 직접 상호작용하지 않아도, 실제로 컨테이너가 이 의존성을 관리합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

실제로 대부분의 경우에는 자동 의존성 주입과 [파사드](/docs/12.x/facades)를 통해 컨테이너에서 아무것도 직접 바인딩하거나 해석하지 않고도 Laravel 애플리케이션을 쉽게 개발할 수 있습니다. **그렇다면 언제 직접 컨테이너와 상호작용해야 할까요?** 아래 두 가지 상황을 예로 들 수 있습니다.

첫째, 직접 인터페이스를 구현한 클래스를 작성하고 라우트나 생성자에서 해당 인터페이스를 타입힌트로 지정하려면, [컨테이너에게 해당 인터페이스를 어떻게 해석해야 하는지 알려주어야 합니다](#binding-interfaces-to-implementations). 둘째, 당신이 [공유용 Laravel 패키지](/docs/12.x/packages)를 개발한다면, 패키지의 서비스를 컨테이너에 바인딩해야 할 수도 있습니다.

<a name="binding"></a>
## 바인딩 (Binding)

<a name="binding-basics"></a>
### 바인딩 기본 (Binding Basics)

<a name="simple-bindings"></a>
#### 단순 바인딩 (Simple Bindings)

대부분의 서비스 컨테이너 바인딩은 [서비스 프로바이더](/docs/12.x/providers) 내에서 등록합니다. 아래 예시들은 이 맥락에서 컨테이너를 사용하는 방법을 보여줍니다.

서비스 프로바이더 내에서는 항상 `$this->app` 속성을 통해 컨테이너에 접근할 수 있습니다. 바인딩할 클래스나 인터페이스명과, 해당 클래스의 인스턴스를 반환하는 클로저를 `bind` 메서드에 전달하여 바인딩을 등록할 수 있습니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

해석자(Resolver)로 전달되는 인수로 컨테이너 자체를 받을 수 있습니다. 이를 통해 객체를 생성할 때 하위 의존성도 컨테이너로부터 해석할 수 있습니다.

앞서 설명한 대로, 보통 서비스 프로바이더에서 컨테이너와 상호작용하지만, 필요할 때는 `App` [파사드](/docs/12.x/facades)를 통해 프로바이더 밖에서도 사용할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```

이미 해당 타입에 대한 바인딩이 존재하지 않을 때만 컨테이너 바인딩을 등록하려면 `bindIf` 메서드를 사용할 수 있습니다.

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

편의를 위해, 바인딩하려는 클래스/인터페이스명을 별도의 인수로 전달하지 않고, 클로저의 반환 타입으로 타입을 추론하게 할 수도 있습니다.

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```

> [!NOTE]
> 어떤 클래스가 인터페이스에 의존하지 않는다면, 컨테이너에 바인딩할 필요가 없습니다. 컨테이너는 리플렉션을 사용해 이런 객체를 자동으로 해석합니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩 (Binding A Singleton)

`singleton` 메서드는 클래스나 인터페이스를 단 한 번만 컨테이너에 해석하여, 이후에는 항상 동일한 객체 인스턴스를 반환하도록 바인딩합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

또한, 이미 바인딩이 존재하지 않을 때만 싱글톤으로 등록하려면 `singletonIf` 메서드를 사용할 수 있습니다.

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="singleton-attribute"></a>
#### Singleton 속성

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
#### Scoped 싱글톤 바인딩

`scoped` 메서드는 클래스나 인터페이스를 주어진 Laravel 요청/작업(job)의 라이프사이클 안에서 단 한 번만 해석하도록 바인딩합니다. 이 방식은 `singleton`과 비슷하지만, `scoped`로 등록된 인스턴스는 [Laravel Octane](/docs/12.x/octane) 워커가 새로운 요청을 처리하거나, [큐 워커](/docs/12.x/queues)가 새 작업을 처리할 때마다 플러시(flush)됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

바인딩이 이미 존재하지 않을 때만 scoped 바인딩을 등록하려면 `scopedIf` 메서드를 사용합니다.

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```

<a name="scoped-attribute"></a>
#### Scoped 속성

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
#### 인스턴스 바인딩

이미 존재하는 객체 인스턴스를 `instance` 메서드를 사용해 컨테이너에 바인딩할 수 있습니다. 해당 인스턴스는 이후 컨테이너에서 계속 반환됩니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```

<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩 (Binding Interfaces to Implementations)

서비스 컨테이너의 강력한 기능 중 하나는 인터페이스와 구현체를 바인딩할 수 있다는 점입니다. 예를 들어, `EventPusher` 인터페이스와 이를 구현한 `RedisEventPusher` 구현체가 있다고 합시다. 아래와 같이 컨테이너에 등록할 수 있습니다.

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```

이렇게 등록하면, 컨테이너가 `EventPusher` 구현이 필요한 클래스에 자동으로 `RedisEventPusher`를 주입합니다. 컨트롤러, 이벤트 리스너, 미들웨어 등 다양한 클래스는 항상 컨테이너로 해석됩니다.

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
#### Bind 속성

Laravel은 더 편리하게 사용할 수 있도록 `Bind` 속성도 제공합니다. 인터페이스에 이 속성을 지정하면, 해당 인터페이스가 요청될 때 어떤 구현체가 자동으로 주입되어야 하는지 Laravel이 알게 됩니다. 이 경우, 추가적인 서비스 등록이 서비스 프로바이더에서 불필요합니다.

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
### 컨텍스트 바인딩 (Contextual Binding)

때때로 두 개의 클래스가 같은 인터페이스를 사용하지만 각각 다른 구현체가 주입되어야 할 때가 있습니다. 예를 들어, 두 컨트롤러가 각기 다른 `Illuminate\Contracts\Filesystem\Filesystem` [컨트랙트](/docs/12.x/contracts) 구현체에 의존한다면, 아래와 같은 방식으로 컨텍스트 바인딩을 정의할 수 있습니다.

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
### 컨텍스트 속성 (Contextual Attributes)

컨텍스트 바인딩은 보통 드라이버 구현체나 설정값을 주입할 때 많이 사용합니다. Laravel은 이런 값을 서비스 프로바이더에서 수동으로 정의하지 않고도 속성(Attribute)으로 쉽게 주입할 수 있도록 여러 컨텍스트 바인딩 속성을 제공합니다.

예를 들어, `Storage` 속성(Attribute)을 사용하면 특정 [스토리지 디스크](/docs/12.x/filesystem)를 주입할 수 있습니다.

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

이외에도, Laravel은 `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RouteParameter`, [Tag](#tagging) 속성을 제공합니다.

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

더불어, 현재 인증된 사용자를 라우트나 클래스에 주입할 때 사용할 수 있는 `CurrentUser` 속성도 제공합니다.

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```

<a name="defining-custom-attributes"></a>
#### 커스텀 속성 정의하기

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
### 기본형 바인딩 (Binding Primitives)

클래스에 의존성 객체뿐 아니라 정수 등 기본 자료형 값을 주입하고 싶을 때, 컨텍스트 바인딩을 활용할 수 있습니다.

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```

클래스가 [태그된](#tagging) 인스턴스의 배열을 필요로 한다면, `giveTagged` 메서드를 사용해 해당 태그로 컨테이너에 등록된 모든 것을 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```

애플리케이션 환경설정파일에서 값을 주입해야 할 경우 `giveConfig` 메서드를 사용할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```

<a name="binding-typed-variadics"></a>
### 타입 지정 가변 인자 바인딩 (Binding Typed Variadics)

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

더 간단하게 클래스명 배열만 전달하면, 컨테이너가 해당 클래스들을 자동으로 해석하여 `Firewall`에 주입합니다.

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
#### 태그 기반 가변 인자 의존성

클래스의 가변 인자 의존성이 특정 클래스(예: `Report ...$reports`)로 타입힌트된 경우, `needs`와 `giveTagged` 메서드를 사용해 [태그](#tagging)로 연결된 바인딩을 주입할 수 있습니다.

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```

<a name="tagging"></a>
### 태깅 (Tagging)

특정 “카테고리”의 모든 바인딩을 한 번에 해석해야 할 때가 있습니다. 예를 들어 여러 종류의 `Report` 인터페이스 구현체 배열을 받는 리포트 분석기를 만든다고 해봅시다. 먼저 각 구현체를 등록한 뒤, `tag` 메서드로 하나의 태그를 부여할 수 있습니다.

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```

이후, 컨테이너의 `tagged` 메서드로 해당 태그가 부여된 모든 서비스를 쉽게 해석할 수 있습니다.

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```

<a name="extending-bindings"></a>
### 바인딩 확장 (Extending Bindings)

`extend` 메서드를 사용하면 이미 해석된 서비스를 수정하거나 데코레이션(decorate)할 수 있습니다. 이 메서드는 확장할 서비스 클래스와, 수정된 서비스를 반환하는 클로저(서비스 인스턴스와 컨테이너를 인수로 받음)를 전달받습니다.

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```

<a name="resolving"></a>
## 해결(Resolve)

<a name="the-make-method"></a>
### `make` 메서드 (The `make` Method)

`make` 메서드를 사용하여 컨테이너에서 클래스 인스턴스를 해석할 수 있습니다. 이 메서드는 해석할 클래스나 인터페이스명을 인수로 받습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```

클래스의 일부 의존성이 컨테이너에서 해석되지 않는다면, `makeWith` 메서드로 연관 배열로 직접 값을 전달할 수 있습니다. 예를 들어, `Transistor` 서비스의 `$id` 생성자 인자를 수동으로 전달할 수 있습니다.

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```

`bound` 메서드를 사용하면 컨테이너에 클래스나 인터페이스가 명시적으로 바인딩되어 있는지 확인할 수 있습니다.

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```

서비스 프로바이더 외부 등 `$app` 변수에 접근할 수 없는 위치에서는 `App` [파사드](/docs/12.x/facades)나, `app` [헬퍼](/docs/12.x/helpers#method-app)를 사용해 클래스 인스턴스를 해석할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```

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
### 자동 주입 (Automatic Injection)

컨테이너에서 해석되는 클래스(컨트롤러, 이벤트 리스너, 미들웨어 등)의 생성자에 의존성을 타입힌트로 지정하면 자동으로 주입됩니다. [큐 작업](/docs/12.x/queues)의 `handle` 메서드도 마찬가지로 지원합니다. 실무에서 객체 대부분은 이처럼 컨테이너에 의해 해석됩니다.

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
## 메서드 호출 및 주입 (Method Invocation and Injection)

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

컨테이너의 `call` 메서드를 사용하면 아래처럼 `generate` 메서드를 호출할 수 있습니다.

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```

`call` 메서드는 PHP의 어떤 콜러블도 받을 수 있습니다. 또한, 클로저를 전달하면 해당 클로저에 필요한 의존성도 자동으로 주입해줍니다.

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```

<a name="container-events"></a>
## 컨테이너 이벤트 (Container Events)

서비스 컨테이너는 객체를 해석할 때마다 이벤트를 발생시킵니다. `resolving` 메서드로 이 이벤트를 수신할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // "Transistor" 타입의 객체가 컨테이너에서 해석될 때 호출됩니다.
});

$this->app->resolving(function (mixed $object, Application $app) {
    // 어떤 타입이든 컨테이너에서 해석될 때 호출됩니다.
});
```

위와 같이 해석 중인 객체 인스턴스가 콜백에 전달되므로, 주입되기 전에 필요한 속성을 추가로 설정할 수 있습니다.

<a name="rebinding"></a>
### 리바인딩 (Rebinding)

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

// 새로운 바인딩이 리바인딩 콜백을 트리거합니다.
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```

<a name="psr-11"></a>
## PSR-11

Laravel의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 PSR-11 컨테이너 인터페이스를 타입힌트로 지정하면 Laravel 컨테이너 인스턴스를 주입받을 수 있습니다.

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

만약 전달된 식별자를 해석할 수 없으면 예외가 발생합니다. 해당 식별자가 한 번도 바인딩된 적이 없다면, `Psr\Container\NotFoundExceptionInterface`의 인스턴스가, 바인딩은 되어 있지만 해석에 실패하면 `Psr\Container\ContainerExceptionInterface`의 인스턴스가 throw 됩니다.
