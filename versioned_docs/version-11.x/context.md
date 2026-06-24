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
Laravel의 "컨텍스트" 기능을 사용하면 애플리케이션 내에서 처리되는 요청, 작업(job), 명령어(command) 전반에 걸쳐 정보를 저장하고, 조회하며, 공유할 수 있습니다. 이렇게 저장한 정보는 애플리케이션이 기록하는 로그에도 자동으로 포함됩니다. 덕분에 로그가 기록되기 전에 어떤 코드 실행 히스토리가 있었는지 더 깊이 파악할 수 있으며, 분산 시스템 전체에서 실행 흐름을 추적하는 것도 용이해집니다.

<a name="how-it-works"></a>
<!-- ### How it Works -->
### How it Works

<!-- The best way to understand Laravel's context capabilities is to see it in action using  the built-in logging features. To get started, you may [add information to the context](#capturing-context) using the `Context` facade. In this example, we will use a [middleware](/docs/11.x/middleware) to add the request URL and a unique trace ID to the context on every incoming request: -->
Laravel의 컨텍스트 기능을 이해하는 가장 좋은 방법은 내장된 로깅 기능과 함께 실제로 사용하는 예시를 보는 것입니다. 먼저, `Context` 파사드(facade)를 사용해 [add information to the context](#capturing-context)해보겠습니다. 아래 예제에서는 [middleware](/docs/11.x/middleware)를 이용해 모든 요청이 들어올 때마다 요청 URL과 고유 트레이스 ID(trace ID)를 컨텍스트에 추가합니다.

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

<!-- Information added to the context is automatically appended as metadata to any [log entries](/docs/11.x/logging) that are written throughout the request. Appending context as metadata allows information passed to individual log entries to be differentiated from the information shared via `Context`. For example, imagine we write the following log entry: -->
컨텍스트에 추가된 정보는 해당 요청에서 기록되는 모든 [log entries](/docs/11.x/logging)에 자동으로 메타데이터 형태로 추가됩니다. 컨텍스트를 메타데이터로 추가하면, 개별 로그 항목에 전달된 정보와 `Context`를 통해 공유된 정보를 구분하여 확인할 수 있습니다. 예를 들어, 아래와 같이 로그를 기록했다고 가정해봅시다.

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

<!-- The written log will contain the `auth_id` passed to the log entry, but it will also contain the context's `url` and `trace_id` as metadata: -->
작성되는 로그에는 로그 항목에 직접 전달한 `auth_id`뿐만 아니라, 컨텍스트에 저장된 `url`과 `trace_id`도 메타데이터로 함께 포함됩니다.

```
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

<!-- Information added to the context is also made available to jobs dispatched to the queue. For example, imagine we dispatch a `ProcessPodcast` job to the queue after adding some information to the context: -->
또한, 컨텍스트에 추가한 정보는 큐(queue)로 디스패치하는 작업(job)에도 함께 전달됩니다. 예를 들어, 컨텍스트에 정보를 추가한 뒤, `ProcessPodcast` 작업을 큐로 디스패치했다고 가정해보겠습니다.

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);
```

<!-- When the job is dispatched, any information currently stored in the context is captured and shared with the job. The captured information is then hydrated back into the current context while the job is executing. So, if our job's handle method was to write to the log: -->
작업이 큐로 디스패치될 때, 현재 컨텍스트에 저장되어 있는 모든 정보가 함께 캡처되고 해당 작업과 공유됩니다. 이렇게 캡처한 정보는 작업이 실행될 때 다시 현재 컨텍스트에 복원(hydrate)됩니다. 만약 작업의 handle 메서드에서 로그를 기록한다면,

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
결과적으로 기록되는 로그 항목에는, 해당 작업을 디스패치한 시점(즉, 요청 처리 도중)에 컨텍스트에 추가되어 있던 정보가 함께 담깁니다.

```
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

<!-- Although we have focused on the built-in logging related features of Laravel's context, the following documentation will illustrate how context allows you to share information across the HTTP request / queued job boundary and even how to add [hidden context data](#hidden-context) that is not written with log entries. -->
여기서는 Laravel의 컨텍스트 기능 중 로깅과 관련된 부분을 중심으로 설명했지만, 아래에서 소개할 문서에서는 컨텍스트를 통해 HTTP 요청과 큐 작업(job) 사이에 정보를 공유하는 방법, 그리고 [hidden context data](#hidden-context)를 추가하는 방법까지 다룹니다.

<a name="capturing-context"></a>
<!-- ## Capturing Context -->
## Capturing Context

<!-- You may store information in the current context using the `Context` facade's `add` method: -->
현재 컨텍스트에 정보를 저장하려면, `Context` 파사드의 `add` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

<!-- To add multiple items at once, you may pass an associative array to the `add` method: -->
여러 개의 항목을 한 번에 추가하려면, 연관 배열(associative array)을 `add` 메서드에 전달하면 됩니다.

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

<!-- The `add` method will override any existing value that shares the same key. If you only wish to add information to the context if the key does not already exist, you may use the `addIf` method: -->
`add` 메서드는 같은 키가 이미 존재할 경우 해당 값을 덮어씁니다. 만약 키가 존재하지 않을 때만 값을 추가하고 싶다면, `addIf` 메서드를 사용할 수 있습니다.

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

<a name="conditional-context"></a>
<!-- #### Conditional Context -->
#### Conditional Context

<!-- The `when` method may be used to add data to the context based on a given condition. The first closure provided to the `when` method will be invoked if the given condition evaluates to `true`, while the second closure will be invoked if the condition evaluates to `false`: -->
`when` 메서드를 사용하면, 특정 조건에 따라 컨텍스트에 데이터를 추가할 수 있습니다. `when` 메서드에 전달한 첫 번째 클로저는 주어진 조건이 `true`로 평가되면 실행되고, 두 번째 클로저는 조건이 `false`로 평가되면 실행됩니다.

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Context;

Context::when(
    Auth::user()->isAdmin(),
    fn ($context) => $context->add('permissions', Auth::user()->permissions),
    fn ($context) => $context->add('permissions', []),
);
```

<a name="stacks"></a>
<!-- ### Stacks -->
### Stacks

<!-- Context offers the ability to create "stacks", which are lists of data stored in the order that they were added. You can add information to a stack by invoking the `push` method: -->
컨텍스트는 "스택" 기능을 제공합니다. 스택이란, 추가된 순서를 그대로 기억하는 데이터의 목록입니다. `push` 메서드를 사용하면 정보를 스택에 추가할 수 있습니다.

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
스택은 요청 처리 중 발생한 여러 이벤트 등, 요청에 대한 히스토리를 기록하거나 추적할 때 유용합니다. 예를 들어, 쿼리가 실행될 때마다 스택에 쿼리의 SQL 문과 소요 시간 정보를 튜플로 추가하는 이벤트 리스너를 만들 수도 있습니다.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

<!-- You may determine if a value is in a stack using the `stackContains` and `hiddenStackContains` methods: -->
특정 값이 스택에 포함되어 있는지 확인하려면 `stackContains`와 `hiddenStackContains` 메서드를 사용할 수 있습니다.

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

<!-- The `stackContains` and `hiddenStackContains` methods also accept a closure as their second argument, allowing more control over the value comparison operation: -->
또한, `stackContains`와 `hiddenStackContains` 메서드의 두 번째 인자로 클로저를 전달하면 값 비교 방식을 더 유연하게 제어할 수 있습니다.

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
컨텍스트에 저장된 정보를 조회하려면, `Context` 파사드의 `get` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

<!-- The `only` method may be used to retrieve a subset of the information in the context: -->
컨텍스트에서 일부 정보만 추출하려면 `only` 메서드를 활용할 수 있습니다.

```php
$data = Context::only(['first_key', 'second_key']);
```

<!-- The `pull` method may be used to retrieve information from the context and immediately remove it from the context: -->
정보를 가져온 후 즉시 컨텍스트에서 제거하고 싶다면 `pull` 메서드를 사용할 수 있습니다.

```php
$value = Context::pull('key');
```

<!-- If context data is stored in a [stack](#stacks), you may pop items from the stack using the `pop` method: -->
만약, 데이터가 [stack](#stacks)에 저장되어 있다면 `pop` 메서드로 스택에서 값을 꺼낼 수 있습니다.

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs')
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

<!-- If you would like to retrieve all of the information stored in the context, you may invoke the `all` method: -->
컨텍스트에 저장된 모든 정보를 한 번에 조회하려면 `all` 메서드를 호출하면 됩니다.

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
<!-- ### Determining Item Existence -->
### Determining Item Existence

<!-- You may use the `has` and `missing` methods to determine if the context has any value stored for the given key: -->
컨텍스트에 특정 키로 저장된 값이 있는지 확인하려면, `has` 또는 `missing` 메서드를 사용할 수 있습니다.

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
`has` 메서드는 저장된 값이 무엇이든(예: `null`이어도) 해당 키가 존재하면 항상 `true`를 반환합니다.

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
<!-- ## Removing Context -->
## Removing Context

<!-- The `forget` method may be used to remove a key and its value from the current context: -->
`forget` 메서드를 사용하면 현재 컨텍스트에서 특정 키와 그 값을 삭제할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

<!-- You may forget several keys at once by providing an array to the `forget` method: -->
`forget` 메서드에 배열을 전달하면 여러 개의 키를 한 번에 제거할 수 있습니다.

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
<!-- ## Hidden Context -->
## Hidden Context

<!-- Context offers the ability to store "hidden" data. This hidden information is not appended to logs, and is not accessible via the data retrieval methods documented above. Context provides a different set of methods to interact with hidden context information: -->
컨텍스트에는 "숨겨진" 데이터를 저장할 수도 있습니다. 이러한 숨겨진 정보는 로그에 포함되지 않으며, 위에서 설명한 데이터 조회 메서드로는 접근할 수 없습니다. 숨겨진 컨텍스트 정보를 저장·조회하려면 별도의 메서드를 사용해야 합니다.

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

<!-- The "hidden" methods mirror the functionality of the non-hidden methods documented above: -->
숨겨진 컨텍스트 관련 메서드는 일반 컨텍스트와 동일한 기능을 제공합니다.

```php
Context::addHidden(/* ... */);
Context::addHiddenIf(/* ... */);
Context::pushHidden(/* ... */);
Context::getHidden(/* ... */);
Context::pullHidden(/* ... */);
Context::popHidden(/* ... */);
Context::onlyHidden(/* ... */);
Context::allHidden(/* ... */);
Context::hasHidden(/* ... */);
Context::forgetHidden(/* ... */);
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Context dispatches two events that allow you to hook into the hydration and dehydration process of the context. -->
컨텍스트는 하이드레이션(hydration) 및 디하이드레이션(dehydration) 과정에서 후킹(hook)할 수 있도록 두 가지 이벤트를 제공합니다.

<!-- To illustrate how these events may be used, imagine that in a middleware of your application you set the `app.locale` configuration value based on the incoming HTTP request's `Accept-Language` header. Context's events allow you to capture this value during the request and restore it on the queue, ensuring notifications sent on the queue have the correct `app.locale` value. We can use context's events and [hidden](#hidden-context) data to achieve this, which the following documentation will illustrate. -->
예를 들어, 애플리케이션의 미들웨어에서 들어오는 HTTP 요청의 `Accept-Language` 헤더에 따라 `app.locale` 설정 값을 지정한다고 가정해봅시다. 컨텍스트의 이벤트를 사용하면 이 값을 요청 도중에 캡처하고, 큐 작업에서도 다시 복원할 수 있습니다. 이런 방식으로 발송되는 알림 등도 올바른 `app.locale` 값이 적용되도록 할 수 있습니다. 아래에서는 이 과정을 컨텍스트 이벤트와 [hidden](#hidden-context) 데이터 기능을 조합해서 처리하는 예시를 보여줍니다.

<a name="dehydrating"></a>
<!-- ### Dehydrating -->
### Dehydrating

<!-- Whenever a job is dispatched to the queue the data in the context is "dehydrated" and captured alongside the job's payload. The `Context::dehydrating` method allows you to register a closure that will be invoked during the dehydration process. Within this closure, you may make changes to the data that will be shared with the queued job. -->
작업을 큐로 디스패치할 때마다 컨텍스트의 데이터가 "디하이드레이트(dehydrate)"되어 작업 페이로드와 함께 저장됩니다. `Context::dehydrating` 메서드를 이용해, 디하이드레이션 과정에서 실행될 클로저를 등록할 수 있습니다. 이 클로저 안에서, 큐 작업에 전달할 데이터(컨텍스트) 내용을 변경할 수도 있습니다.

<!-- Typically, you should register `dehydrating` callbacks within the `boot` method of your application's `AppServiceProvider` class: -->
보통 `dehydrating` 콜백은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 안에서 등록하는 것이 일반적입니다.

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
> `dehydrating` 콜백 안에서는 절대 `Context` 파사드를 사용하지 마십시오. 그렇게 하면 현재 프로세스의 컨텍스트가 변경될 수 있습니다. 반드시 콜백에 전달되는 저장소(repository) 인스턴스만 조작해야 합니다.

<a name="hydrated"></a>
<!-- ### Hydrated -->
### Hydrated

<!-- Whenever a queued job begins executing on the queue, any context that was shared with the job will be "hydrated" back into the current context. The `Context::hydrated` method allows you to register a closure that will be invoked during the hydration process. -->
큐 작업이 실행될 때, 해당 작업과 공유된 컨텍스트 데이터가 현재 컨텍스트로 다시 "하이드레이트(hydrate)"됩니다. `Context::hydrated` 메서드를 사용하면, 하이드레이션 과정에서 호출되는 클로저를 등록할 수 있습니다.

<!-- Typically, you should register `hydrated` callbacks within the `boot` method of your application's `AppServiceProvider` class: -->
`hydrated` 콜백 역시, 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에 등록하는 것이 일반적입니다.

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
> `hydrated` 콜백 안에서도 `Context` 파사드를 직접 사용하지 말고, 반드시 콜백에 전달된 저장소 인스턴스만 조작해야 합니다.
