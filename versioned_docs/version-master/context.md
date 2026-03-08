# 컨텍스트 (Context)

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [컨텍스트 캡처](#capturing-context)
    - [스택](#stacks)
- [컨텍스트 조회](#retrieving-context)
    - [항목 존재 여부 확인](#determining-item-existence)
- [컨텍스트 제거](#removing-context)
- [숨겨진 컨텍스트](#hidden-context)
- [이벤트](#events)
    - [디하이드레이팅(Dehydrating)](#dehydrating)
    - [하이드레이티드(Hydrated)](#hydrated)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 "컨텍스트(Context)" 기능은 애플리케이션 내에서 실행되는 요청, 작업(job), 명령어(command) 전반에 걸쳐 정보를 캡처하고, 조회하고, 공유할 수 있게 해줍니다. 이렇게 수집된 정보는 애플리케이션이 기록하는 로그에도 자동으로 포함되어, 로그가 작성되기 전에 실행된 코드 히스토리에 대한 더 깊은 인사이트를 제공하며, 분산 시스템 전반에서 실행 흐름을 추적할 수 있도록 도와줍니다.

<a name="how-it-works"></a>
### 작동 방식

Laravel의 컨텍스트 기능을 가장 잘 이해할 수 있는 방법은 내장된 로깅 기능과 함께 실제로 확인해보는 것입니다. 시작하려면, `Context` 파사드를 사용해 [컨텍스트에 정보를 추가](#capturing-context)할 수 있습니다. 다음 예제에서는 [미들웨어](/docs/master/middleware)를 통해 들어오는 모든 요청마다 요청 URL과 고유 트레이스 ID(trace ID)를 컨텍스트에 추가합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AddContext
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): Response
    {
        Context::add('url', $request->url());
        Context::add('trace_id', Str::uuid()->toString());

        return $next($request);
    }
}
```

컨텍스트에 추가된 정보는 해당 요청 처리 중에 기록되는 모든 [로그 항목](/docs/master/logging)에 메타데이터로 자동 첨부됩니다. 컨텍스트를 메타데이터로 추가하면, 각 로그 항목마다 전달된 정보와 `Context`를 통해 공유된 정보를 구분할 수 있게 됩니다. 예를 들어, 아래와 같이 로그를 작성한다고 가정해보겠습니다:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

기록된 로그에는 로그 엔트리에 전달된 `auth_id` 외에도, 컨텍스트의 `url`과 `trace_id`가 메타데이터로 함께 포함됩니다:

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

컨텍스트에 추가된 정보는 큐로 디스패치된 작업(job)에도 전달됩니다. 예를 들어, 컨텍스트에 정보를 추가한 뒤 `ProcessPodcast` 작업을 큐로 디스패치한다고 상상해보세요:

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);
```

작업이 디스패치될 때, 컨텍스트에 저장되어 있던 모든 정보가 함께 캡처되어 작업에 공유됩니다. 그리고 작업이 실행되는 동안, 이렇게 캡처된 정보가 다시 현재 컨텍스트로 하이드레이션(hydration)됩니다. 따라서, 작업의 handle 메서드에서 로그를 기록하면:

```php
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Log::info('Processing podcast.', [
            'podcast_id' => $this->podcast->id,
        ]);

        // ...
    }
}
```

아래와 같이, 처음 요청에서 컨텍스트에 추가했던 정보가 해당 작업과 연결된 로그에도 포함됩니다:

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

여기서는 주로 Laravel 컨텍스트의 내장 로깅 관련 기능에 대해 집중해서 설명했지만, 아래 문서에서는 컨텍스트를 사용해 HTTP 요청과 큐 작업 간에 정보를 어떻게 공유할 수 있는지, 그리고 로그에 기록되지 않는 [숨겨진 컨텍스트 데이터](#hidden-context)를 추가하는 방법까지도 설명합니다.

<a name="capturing-context"></a>
## 컨텍스트 캡처 (Capturing Context)

현재 컨텍스트에 정보를 저장하려면 `Context` 파사드의 `add` 메서드를 사용하면 됩니다:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

여러 항목을 한 번에 추가하려면, 연관 배열을 `add` 메서드에 전달하면 됩니다:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

`add` 메서드는 동일한 키가 이미 존재한다면 기존 값을 덮어씁니다. 만약 해당 키가 존재하지 않을 때만 정보를 추가하고 싶다면 `addIf` 메서드를 사용할 수 있습니다:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

컨텍스트에는 특정 키의 값을 간편하게 증가시키거나 감소시키기 위한 메서드도 있습니다. 이 메서드들은 첫 번째 인수로 추적할 키를 받고, 두 번째 인수로 증가시키거나 감소시킬 값을 지정할 수 있습니다:

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a name="conditional-context"></a>
#### 조건부 컨텍스트

`when` 메서드를 사용하면 조건에 따라 컨텍스트에 데이터를 추가할 수 있습니다. 첫 번째로 전달한 클로저는 조건이 `true`일 때 실행되며, 두 번째 클로저는 조건이 `false`일 때 실행됩니다:

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Context;

Context::when(
    Auth::user()->isAdmin(),
    fn ($context) => $context->add('permissions', Auth::user()->permissions),
    fn ($context) => $context->add('permissions', []),
);
```

<a name="scoped-context"></a>
#### 범위 컨텍스트(Scoped Context)

`scope` 메서드는 특정 콜백 실행 중에만 일시적으로 컨텍스트를 변경하고, 콜백이 끝나면 원래 상태로 되돌릴 수 있도록 도와줍니다. 또한, 실행하는 동안 컨텍스트에 병합할 추가 데이터(두 번째, 세 번째 인수)도 전달할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\Log;

Context::add('trace_id', 'abc-999');
Context::addHidden('user_id', 123);

Context::scope(
    function () {
        Context::add('action', 'adding_friend');

        $userId = Context::getHidden('user_id');

        Log::debug("Adding user [{$userId}] to friends list.");
        // Adding user [987] to friends list.  {"trace_id":"abc-999","user_name":"taylor_otwell","action":"adding_friend"}
    },
    data: ['user_name' => 'taylor_otwell'],
    hidden: ['user_id' => 987],
);

Context::all();
// [
//     'trace_id' => 'abc-999',
// ]

Context::allHidden();
// [
//     'user_id' => 123,
// ]
```

> [!WARNING]
> 범위가 지정된 콜백 내에서 컨텍스트에 저장된 객체를 직접 수정하면, 그 변경 내용이 범위 바깥에도 반영됨에 유의하세요.

<a name="stacks"></a>
### 스택

컨텍스트는 "스택(stack)" 기능을 지원합니다. 스택은 데이터를 추가한 순서대로 저장하는 리스트입니다. `push` 메서드를 사용해 스택에 정보를 추가할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::push('breadcrumbs', 'first_value');

Context::push('breadcrumbs', 'second_value', 'third_value');

Context::get('breadcrumbs');
// [
//     'first_value',
//     'second_value',
//     'third_value',
// ]
```

스택은 요청 처리 도중 발생한 이벤트나 기록을 순서대로 저장하는 등, 요청의 이력을 추적할 때 유용합니다. 예를 들어, 쿼리가 실행될 때마다 쿼리 SQL과 실행 시간을 스택에 저장하도록 이벤트 리스너를 만들 수도 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

// AppServiceProvider.php 내에서...
DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

특정 값이 스택 내에 포함되어 있는지 확인하려면 `stackContains` 및 `hiddenStackContains` 메서드를 사용할 수 있습니다:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

`stackContains`와 `hiddenStackContains` 메서드는 두 번째 인수로 클로저도 받을 수 있어, 원하는 방식으로 값을 비교할 수도 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## 컨텍스트 조회 (Retrieving Context)

컨텍스트에 저장된 정보를 얻으려면 `Context` 파사드의 `get` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

`only`와 `except` 메서드를 사용하면 컨텍스트 내 일부 정보만 추출할 수 있습니다:

```php
$data = Context::only(['first_key', 'second_key']);

$data = Context::except(['first_key']);
```

`pull` 메서드로 컨텍스트에서 값을 읽은 뒤 바로 해당 값을 제거할 수도 있습니다:

```php
$value = Context::pull('key');
```

컨텍스트 데이터가 [스택](#stacks)에 저장되어 있다면, `pop` 메서드로 값을 꺼낼 수 있습니다:

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs');
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

`remember`, `rememberHidden` 메서드를 이용하면, 요청한 정보가 없을 때 클로저의 반환값으로 값을 설정하고, 그 값을 바로 반환받을 수 있습니다:

```php
$permissions = Context::remember(
    'user-permissions',
    fn () => $user->permissions,
);
```

컨텍스트에 저장된 모든 정보를 조회하려면 `all` 메서드를 사용하세요:

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### 항목 존재 여부 확인

특정 키에 해당하는 값이 컨텍스트에 존재하는지 확인하려면 `has` 및 `missing` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

`has` 메서드는 값이 무엇이든(심지어 `null`이어도) 키가 존재하면 `true`를 반환합니다:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## 컨텍스트 제거 (Removing Context)

`forget` 메서드를 통해 현재 컨텍스트에서 특정 키와 그 값을 제거할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

여러 키를 한 번에 제거하려면 배열 형태로 `forget` 메서드에 전달하면 됩니다:

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## 숨겨진 컨텍스트 (Hidden Context)

컨텍스트는 로그에 기록되지 않고, 이전에 설명한 조회 메서드로는 접근할 수 없는 "숨겨진" 데이터도 저장할 수 있습니다. 숨겨진 컨텍스트에는 전용 메서드를 사용해야 합니다:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

숨겨진 관련 메서드는 아래와 같이, 앞서 설명한 일반 컨텍스트 메서드와 유사하게 사용할 수 있습니다:

```php
Context::addHidden(/* ... */);
Context::addHiddenIf(/* ... */);
Context::pushHidden(/* ... */);
Context::getHidden(/* ... */);
Context::pullHidden(/* ... */);
Context::popHidden(/* ... */);
Context::onlyHidden(/* ... */);
Context::exceptHidden(/* ... */);
Context::allHidden(/* ... */);
Context::hasHidden(/* ... */);
Context::missingHidden(/* ... */);
Context::forgetHidden(/* ... */);
```

<a name="events"></a>
## 이벤트 (Events)

컨텍스트는 하이드레이션(hydration) 및 디하이드레이션(dehydration) 과정에 개입할 수 있도록 두 개의 이벤트를 디스패치(dispatch)합니다.

이 이벤트가 어떻게 활용될 수 있는지 예를 들어 설명하겠습니다. 애플리케이션의 미들웨어에서 들어오는 HTTP 요청의 `Accept-Language` 헤더에 따라 `app.locale` 설정값을 지정한다고 상상해보세요. 컨텍스트 이벤트를 활용하면 이 값을 요청 도중 캡처했다가, 큐 작업에서도 올바른 `app.locale`을 복원할 수 있습니다. 이는 컨텍스트 이벤트와 [숨겨진 데이터](#hidden-context)를 함께 사용하면 가능합니다. 아래에서 자세히 설명합니다.

<a name="dehydrating"></a>
### 디하이드레이팅(Dehydrating)

큐에 작업이 디스패치될 때마다, 컨텍스트 내 데이터가 "디하이드레이트(dehydrate)"되어 작업의 페이로드와 함께 캡처됩니다. `Context::dehydrating` 메서드는 디하이드레이션 과정 중에 호출될 클로저를 등록할 수 있게 해줍니다. 이 클로저 내부에서 큐 작업과 공유할 데이터를 수정할 수 있습니다.

일반적으로는 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 `dehydrating` 콜백을 등록합니다:

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::dehydrating(function (Repository $context) {
        $context->addHidden('locale', Config::get('app.locale'));
    });
}
```

> [!NOTE]
> `dehydrating` 콜백 내에서 `Context` 파사드를 직접 사용하지 마세요. 현재 프로세스의 컨텍스트가 변경될 수 있습니다. 반드시 콜백에 전달되는 레포지토리 인스턴스만 사용해 변경을 수행하세요.

<a name="hydrated"></a>
### 하이드레이티드(Hydrated)

큐에 디스패치된 작업이 실행될 때, 해당 작업과 함께 전달된 컨텍스트 데이터가 현재 컨텍스트로 "하이드레이트(hydrate)"됩니다. `Context::hydrated` 메서드는 이 과정에서 호출될 클로저를 등록할 수 있게 해줍니다.

마찬가지로, 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 `hydrated` 콜백을 등록하는 것이 일반적입니다:

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::hydrated(function (Repository $context) {
        if ($context->hasHidden('locale')) {
            Config::set('app.locale', $context->getHidden('locale'));
        }
    });
}
```

> [!NOTE]
> `hydrated` 콜백 내에서도 `Context` 파사드 대신, 콜백에 전달되는 레포지토리 인스턴스만 사용해서 변경해야 합니다.
