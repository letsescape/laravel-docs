<!-- # Context -->
# Context

- [Introduction](#introduction)
    - [How it Works](#how-it-works)
- [Capturing Context](#capturing-context)
    - [Stacks](#stacks)
- [Retrieving Context](#retrieving-context)
    - [Determining Item Existence](#determining-item-existence)
- [Removing Context](#removing-context)
- [Hidden Context](#hidden-context)
- [Events](#events)
    - [Dehydrating](#dehydrating)
    - [Hydrated](#hydrated)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's "context" capabilities enable you to capture, retrieve, and share information throughout requests, jobs, and commands executing within your application. This captured information is also included in logs written by your application, giving you deeper insight into the surrounding code execution history that occurred before a log entry was written and allowing you to trace execution flows throughout a distributed system. -->
Laravel의 "컨텍스트" 기능은 애플리케이션 내에서 실행되는 요청, 작업(job), 명령어 전반에 걸쳐 정보를 캡처하고, 가져오고, 공유할 수 있게 해줍니다. 이렇게 캡처된 정보는 애플리케이션에서 작성하는 로그에도 포함되어, 로그가 기록되기 전에 실행된 코드의 수행 이력에 대한 깊은 통찰을 제공하며, 분산 시스템 전체의 실행 흐름을 추적할 수 있게 합니다.

<a name="how-it-works"></a>
<!-- ### How it Works -->
### How it Works

<!-- The best way to understand Laravel's context capabilities is to see it in action using  the built-in logging features. To get started, you may [add information to the context](#capturing-context) using the `Context` facade. In this example, we will use a [middleware](/docs/master/middleware) to add the request URL and a unique trace ID to the context on every incoming request: -->
Laravel의 컨텍스트 기능을 이해하는 가장 좋은 방법은 내장된 로깅 기능을 활용하여 실제로 작동하는 예를 보는 것입니다. 시작하려면 `Context` 파사드를 사용해 [add information to the context](#capturing-context)부터 해봅니다. 이 예에서는 모든 들어오는 요청마다 요청 URL과 고유한 추적 ID를 컨텍스트에 추가하는 [middleware](/docs/master/middleware)를 사용합니다:

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

<!-- Information added to the context is automatically appended as metadata to any [log entries](/docs/master/logging) that are written throughout the request. Appending context as metadata allows information passed to individual log entries to be differentiated from the information shared via `Context`. For example, imagine we write the following log entry: -->
컨텍스트에 추가된 정보는 요청 전반에서 작성되는 모든 [log entries](/docs/master/logging)에 메타데이터로 자동 추가됩니다. 컨텍스트를 메타데이터로 덧붙이면, 개별 로그 항목에 전달되는 정보와 `Context`를 통해 공유되는 정보를 구분할 수 있습니다. 예를 들어, 다음과 같이 로그를 작성한다고 가정해봅시다:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

<!-- The written log will contain the `auth_id` passed to the log entry, but it will also contain the context's `url` and `trace_id` as metadata: -->
작성된 로그에는 `auth_id`가 포함되지만, 동시에 컨텍스트의 `url`과 `trace_id`도 메타데이터로 포함됩니다:

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

<!-- Information added to the context is also made available to jobs dispatched to the queue. For example, imagine we dispatch a `ProcessPodcast` job to the queue after adding some information to the context: -->
컨텍스트에 추가된 정보는 큐에 디스패치된 작업에도 적용됩니다. 예를 들어, 컨텍스트에 정보를 추가한 후에 `ProcessPodcast` 작업을 큐에 디스패치한다고 가정해봅시다:

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);
```

<!-- When the job is dispatched, any information currently stored in the context is captured and shared with the job. The captured information is then hydrated back into the current context while the job is executing. So, if our job's handle method was to write to the log: -->
작업이 디스패치될 때, 현재 컨텍스트에 저장된 모든 정보가 캡처되어 작업과 함께 공유됩니다. 그리고 작업이 실행되는 동안 캡처된 정보가 다시 현재 컨텍스트로 "활성화"됩니다. 만약 작업의 handle 메서드가 로그를 작성한다면:

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

<!-- The resulting log entry would contain the information that was added to the context during the request that originally dispatched the job: -->
해당 로그 항목에는 작업을 디스패치했던 요청 시점에 컨텍스트에 추가된 정보도 포함됩니다:

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

<!-- Although we have focused on the built-in logging related features of Laravel's context, the following documentation will illustrate how context allows you to share information across the HTTP request / queued job boundary and even how to add [hidden context data](#hidden-context) that is not written with log entries. -->
이 문서에서는 Laravel 컨텍스트의 내장된 로깅 관련 기능에 집중했지만, 이후 문서에서는 HTTP 요청과 큐 작업 경계를 넘어 정보를 공유할 수 있는 방법과, 로그 항목에 기록되지 않는 [hidden context data](#hidden-context)를 추가하는 방법도 설명할 것입니다.

<a name="capturing-context"></a>
<!-- ## Capturing Context -->
## Capturing Context

<!-- You may store information in the current context using the `Context` facade's `add` method: -->
`Context` 파사드의 `add` 메서드를 사용해 현재 컨텍스트에 정보를 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

<!-- To add multiple items at once, you may pass an associative array to the `add` method: -->
여러 항목을 한꺼번에 추가하려면, 연관 배열을 `add` 메서드에 전달하면 됩니다:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

<!-- The `add` method will override any existing value that shares the same key. If you only wish to add information to the context if the key does not already exist, you may use the `addIf` method: -->
`add` 메서드는 같은 키가 이미 존재하면 기존 값을 덮어씁니다. 만약 키가 존재하지 않을 경우에만 추가하고 싶다면 `addIf` 메서드를 사용하십시오:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

<!-- Context also provides convenient methods for incrementing or decrementing a given key. Both of these methods accept at least one argument: the key to track. A second argument may be provided to specify the amount by which the key should be incremented or decremented: -->
컨텍스트는 지정한 키의 값을 증가시키거나 감소시키는 편리한 메서드도 제공합니다. 이 두 메서드는 최소 하나의 인수(추적할 키)를 받으며, 두 번째 인수로 증가 또는 감소할 값을 지정할 수 있습니다:

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);
```

<a name="conditional-context"></a>
<!-- #### Conditional Context -->
#### Conditional Context

<!-- The `when` method may be used to add data to the context based on a given condition. The first closure provided to the `when` method will be invoked if the given condition evaluates to `true`, while the second closure will be invoked if the condition evaluates to `false`: -->
`when` 메서드는 주어진 조건에 따라 컨텍스트에 데이터를 추가할 때 사용됩니다. `when` 메서드에 전달한 첫 번째 클로저는 주어진 조건이 `true`로 평가될 때 호출되고, 두 번째 클로저는 조건이 `false`로 평가될 때 호출됩니다:

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
<!-- #### Scoped Context -->
#### Scoped Context

<!-- The `scope` method provides a way to temporarily modify the context during the execution of a given callback and restore the context to its original state when the callback finishes executing. Additionally, you can pass extra data that should be merged into the context (as the second and third arguments) while the closure executes. -->
`scope` 메서드는 지정된 콜백 함수 실행 동안 컨텍스트를 일시적으로 변경하고, 콜백 실행이 끝난 후 원래 상태로 복원하는 방법을 제공합니다. 콜백 실행 중 병합할 추가 데이터는 두 번째와 세 번째 인수로 전달할 수 있습니다.

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
> 스코프 내부에서 컨텍스트 안 객체를 수정하면, 해당 변경이 스코프 외부에도 반영됩니다.

<a name="stacks"></a>
<!-- ### Stacks -->
### Stacks

<!-- Context offers the ability to create "stacks", which are lists of data stored in the order that they were added. You can add information to a stack by invoking the `push` method: -->
컨텍스트는 스택이라는 기능을 제공하는데, 이는 추가된 순서대로 데이터를 저장하는 리스트입니다. `push` 메서드를 호출해 스택에 정보를 추가할 수 있습니다:

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

<!-- Stacks can be useful to capture historical information about a request, such as events that are happening throughout your application. For example, you could create an event listener to push to a stack every time a query is executed, capturing the query SQL and duration as a tuple: -->
스택은 요청 중 발생한 일련의 이벤트처럼, 시간 순으로 발생한 기록 정보를 캡처하는 데 유용합니다. 예를 들어, 쿼리가 실행될 때마다 쿼리 SQL과 소요 시간을 튜플로 스택에 푸시하는 이벤트 리스너를 생성할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

// In AppServiceProvider.php...
DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

<!-- You may determine if a value is in a stack using the `stackContains` and `hiddenStackContains` methods: -->
`stackContains`와 `hiddenStackContains` 메서드를 사용해 스택에 값이 존재하는지 확인할 수 있습니다:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

<!-- The `stackContains` and `hiddenStackContains` methods also accept a closure as their second argument, allowing more control over the value comparison operation: -->
`stackContains`와 `hiddenStackContains` 메서드는 두 번째 인수로 클로저도 받아, 값 비교 작업을 더 세밀하게 제어할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
<!-- ## Retrieving Context -->
## Retrieving Context

<!-- You may retrieve information from the context using the `Context` facade's `get` method: -->
`Context` 파사드의 `get` 메서드를 사용해 컨텍스트에서 정보를 가져올 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

<!-- The `only` and `except` methods may be used to retrieve a subset of the information in the context: -->
`only`와 `except` 메서드는 컨텍스트에서 특정 부분 집합만 가져올 때 사용합니다:

```php
$data = Context::only(['first_key', 'second_key']);

$data = Context::except(['first_key']);
```

<!-- The `pull` method may be used to retrieve information from the context and immediately remove it from the context: -->
`pull` 메서드를 사용하면 컨텍스트에서 값을 가져오면서 동시에 제거할 수 있습니다:

```php
$value = Context::pull('key');
```

<!-- If context data is stored in a [stack](#stacks), you may pop items from the stack using the `pop` method: -->
만약 컨텍스트 데이터가 [stack](#stacks)에 저장되어 있다면 `pop` 메서드로 스택의 마지막 항목을 꺼낼 수 있습니다:

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs');
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

<!-- The `remember` and `rememberHidden` methods may be used to retrieve information from the context, while setting the context value to the value returned by the given closure if the requested information doesn't exist: -->
`remember`와 `rememberHidden` 메서드는 특정 정보를 컨텍스트에서 가져오고, 요청한 정보가 없으면 주어진 클로저가 반환하는 값으로 설정하는 데 사용됩니다:

```php
$permissions = Context::remember(
    'user-permissions',
    fn () => $user->permissions,
);
```

<!-- If you would like to retrieve all of the information stored in the context, you may invoke the `all` method: -->
컨텍스트에 저장된 모든 정보를 가져오려면 `all` 메서드를 호출하십시오:

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
<!-- ### Determining Item Existence -->
### Determining Item Existence

<!-- You may use the `has` and `missing` methods to determine if the context has any value stored for the given key: -->
`has`와 `missing` 메서드를 사용해 주어진 키에 컨텍스트 값이 저장되어 있는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}
```

<!-- The `has` method will return `true` regardless of the value stored. So, for example, a key with a `null` value will be considered present: -->
`has` 메서드는 저장된 값이 무엇이든 간에 `true`를 반환합니다. 따라서 `null` 값이어도 키가 존재하는 것으로 간주됩니다:

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
<!-- ## Removing Context -->
## Removing Context

<!-- The `forget` method may be used to remove a key and its value from the current context: -->
`forget` 메서드를 사용해 현재 컨텍스트에서 특정 키와 값을 제거할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

<!-- You may forget several keys at once by providing an array to the `forget` method: -->
여러 키를 한꺼번에 제거하려면 배열을 `forget` 메서드에 전달하면 됩니다:

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
<!-- ## Hidden Context -->
## Hidden Context

<!-- Context offers the ability to store "hidden" data. This hidden information is not appended to logs, and is not accessible via the data retrieval methods documented above. Context provides a different set of methods to interact with hidden context information: -->
컨텍스트는 "숨겨진" 데이터를 저장하는 기능도 제공합니다. 이 숨겨진 정보는 로그에 추가되지 않으며, 앞서 설명한 데이터 조회 메서드로 접근할 수 없습니다. 숨겨진 컨텍스트 데이터와 상호작용하려면 다른 메서드 집합을 사용해야 합니다:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

<!-- The "hidden" methods mirror the functionality of the non-hidden methods documented above: -->
숨겨진 컨텍스트 관련 메서드는 비숨김 메서드와 동일한 기능을 제공합니다:

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
<!-- ## Events -->
## Events

<!-- Context dispatches two events that allow you to hook into the hydration and dehydration process of the context. -->
컨텍스트는 컨텍스트의 활성화(hydration)와 비활성화(dehydration) 과정에 훅을 걸 수 있도록 두 가지 이벤트를 발행합니다.

<!-- To illustrate how these events may be used, imagine that in a middleware of your application you set the `app.locale` configuration value based on the incoming HTTP request's `Accept-Language` header. Context's events allow you to capture this value during the request and restore it on the queue, ensuring notifications sent on the queue have the correct `app.locale` value. We can use context's events and [hidden](#hidden-context) data to achieve this, which the following documentation will illustrate. -->
예를 들어, 애플리케이션 미들웨어에서 들어오는 HTTP 요청의 `Accept-Language` 헤더를 기반으로 `app.locale` 설정 값을 지정한다고 가정해봅시다. 컨텍스트 이벤트를 활용하면 이 값을 요청 동안 캡처하고, 큐에서 복원하여, 큐에서 실행되는 알림 등이 올바른 `app.locale` 설정을 사용할 수 있도록 할 수 있습니다. 이 과정에서 [hidden](#hidden-context)를 함께 사용합니다. 아래 문서를 통해 구현 예를 확인할 수 있습니다.

<a name="dehydrating"></a>
<!-- ### Dehydrating -->
### Dehydrating

<!-- Whenever a job is dispatched to the queue the data in the context is "dehydrated" and captured alongside the job's payload. The `Context::dehydrating` method allows you to register a closure that will be invoked during the dehydration process. Within this closure, you may make changes to the data that will be shared with the queued job. -->
작업이 큐에 디스패치될 때마다, 컨텍스트의 데이터는 "비활성화"되어 작업 페이로드와 함께 캡처됩니다. `Context::dehydrating` 메서드를 통해 비활성화 과정 동안 호출될 클로저를 등록할 수 있습니다. 이 클로저 내에서 큐 작업과 함께 공유할 데이터를 수정할 수 있습니다.

<!-- Typically, you should register `dehydrating` callbacks within the `boot` method of your application's `AppServiceProvider` class: -->
일반적으로 `AppServiceProvider` 클래스의 `boot` 메서드에서 `dehydrating` 콜백을 등록합니다:

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
> `dehydrating` 콜백 안에서 `Context` 파사드 사용은 권장하지 않습니다. 현재 프로세스의 컨텍스트가 변경될 수 있으므로, 반드시 콜백에 전달된 저장소 인스턴스에서만 작업하세요.

<a name="hydrated"></a>
<!-- ### Hydrated -->
### Hydrated

<!-- Whenever a queued job begins executing on the queue, any context that was shared with the job will be "hydrated" back into the current context. The `Context::hydrated` method allows you to register a closure that will be invoked during the hydration process. -->
큐에 디스패치된 작업이 실행되기 시작할 때, 작업과 함께 공유된 컨텍스트가 현재 컨텍스트로 "활성화"됩니다. `Context::hydrated` 메서드를 통해 활성화 과정에서 호출될 클로저를 등록할 수 있습니다.

<!-- Typically, you should register `hydrated` callbacks within the `boot` method of your application's `AppServiceProvider` class: -->
일반적으로 `AppServiceProvider` 클래스의 `boot` 메서드에서 `hydrated` 콜백을 등록합니다:

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
> `hydrated` 콜백 내에서 `Context` 파사드를 직접 사용하지 말고, 반드시 콜백에 전달된 저장소 인스턴스를 통해만 작업하세요.