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
Laravel の「コンテキスト」機能を使用すると、アプリケーション内で実行されるリクエスト、ジョブ、コマンド全体にわたって情報をキャプチャ、取得、共有できます。この取得された情報は、アプリケーションによって書き込まれるログにも含まれるため、ログ エントリが書き込まれる前に発生した周囲のコード実行履歴についてより深い洞察が得られ、分散システム全体の実行フローを追跡できるようになります。

<a name="how-it-works"></a>
<!-- ### How it Works -->
### How it Works

<!-- The best way to understand Laravel's context capabilities is to see it in action using  the built-in logging features. To get started, you may [add information to the context](#capturing-context) using the `Context` facade. In this example, we will use a [middleware](/docs/12.x/middleware) to add the request URL and a unique trace ID to the context on every incoming request: -->
Laravel のコンテキスト機能を理解する最良の方法は、組み込みのログ機能を使用して実際の動作を確認することです。まず、`Context` ファサードを使用して [add information to the context](#capturing-context) を実行します。この例では、[middleware](/docs/12.x/middleware) を使用して、すべての受信リクエストのコンテキストにリクエスト URL と一意のトレース ID を追加します。

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

<!-- Information added to the context is automatically appended as metadata to any [log entries](/docs/12.x/logging) that are written throughout the request. Appending context as metadata allows information passed to individual log entries to be differentiated from the information shared via `Context`. For example, imagine we write the following log entry: -->
コンテキストに追加された情報は、リクエスト全体に書き込まれるすべての [log entries](/docs/12.x/logging) にメタデータとして自動的に追加されます。コンテキストをメタデータとして追加すると、個々のログ エントリに渡される情報を、`Context` を介して共有される情報と区別できるようになります。たとえば、次のログ エントリを書き込むとします。

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

<!-- The written log will contain the `auth_id` passed to the log entry, but it will also contain the context's `url` and `trace_id` as metadata: -->
書き込まれたログには、ログ エントリに渡された `auth_id` が含まれますが、コンテキストの `url` および `trace_id` もメタデータとして含まれます。

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

<!-- Information added to the context is also made available to jobs dispatched to the queue. For example, imagine we dispatch a `ProcessPodcast` job to the queue after adding some information to the context: -->
コンテキストに追加された情報は、キューにディスパッチされたジョブでも利用できるようになります。たとえば、コンテキストに情報を追加した後、`ProcessPodcast` ジョブをキューにディスパッチするとします。

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);
```

<!-- When the job is dispatched, any information currently stored in the context is captured and shared with the job. The captured information is then hydrated back into the current context while the job is executing. So, if our job's handle method was to write to the log: -->
ジョブがディスパッチされると、コンテキストに現在保存されている情報がキャプチャされ、ジョブと共有されます。キャプチャされた情報は、ジョブの実行中に現在のコンテキストに反映されます。したがって、ジョブのハンドル メソッドがログに書き込む場合は次のようになります。

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
結果として得られるログ エントリには、最初にジョブをディスパッチしたリクエスト中にコンテキストに追加された情報が含まれます。

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

<!-- Although we have focused on the built-in logging related features of Laravel's context, the following documentation will illustrate how context allows you to share information across the HTTP request / queued job boundary and even how to add [hidden context data](#hidden-context) that is not written with log entries. -->
Laravel コンテキストの組み込みロギング関連機能に焦点を当ててきましたが、次のドキュメントでは、コンテキストを使用して HTTP リクエスト/キューに入れられたジョブの境界を越えて情報を共有する方法と、ログエントリで書き込まれない [hidden context data](#hidden-context) を追加する方法についても説明します。

<a name="capturing-context"></a>
<!-- ## Capturing Context -->
## Capturing Context

<!-- You may store information in the current context using the `Context` facade's `add` method: -->
`Context` ファサードの `add` メソッドを使用して、現在のコンテキストに情報を保存できます。

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

<!-- To add multiple items at once, you may pass an associative array to the `add` method: -->
複数の項目を一度に追加するには、連想配列を `add` メソッドに渡すことができます。

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

<!-- The `add` method will override any existing value that shares the same key. If you only wish to add information to the context if the key does not already exist, you may use the `addIf` method: -->
`add` メソッドは、同じキーを共有する既存の値をオーバーライドします。キーがまだ存在しない場合にのみコンテキストに情報を追加したい場合は、`addIf` メソッドを使用できます。

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

<!-- Context also provides convenient methods for incrementing or decrementing a given key. Both of these methods accept at least one argument: the key to track. A second argument may be provided to specify the amount by which the key should be incremented or decremented: -->
Context は、特定のキーをインクリメントまたはデクリメントするための便利なメソッドも提供します。これらのメソッドは両方とも、少なくとも 1 つの引数、つまり追跡するキーを受け入れます。 2 番目の引数を指定して、キーをインクリメントまたはデクリメントする量を指定できます。

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
`when` メソッドは、特定の条件に基づいてコンテキストにデータを追加するために使用できます。 `when` メソッドに指定された最初のクロージャは、指定された条件が `true` と評価された場合に呼び出され、2 番目のクロージャは、条件が `false` と評価された場合に呼び出されます。

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
`scope` メソッドは、特定のコールバックの実行中にコンテキストを一時的に変更し、コールバックの実行終了時にコンテキストを元の状態に復元する方法を提供します。さらに、クロージャの実行中に、コンテキストにマージする必要がある追加のデータを (2 番目と 3 番目の引数として) 渡すことができます。

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
> コンテキスト内のオブジェクトがスコープ付きクロージャ内で変更された場合、その変更はスコープの外に反映されます。

<a name="stacks"></a>
<!-- ### Stacks -->
### Stacks

<!-- Context offers the ability to create "stacks", which are lists of data stored in the order that they were added. You can add information to a stack by invoking the `push` method: -->
Context は、追加された順序で保存されたデータのリストである「スタック」を作成する機能を提供します。 `push` メソッドを呼び出して、スタックに情報を追加できます。

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
スタックは、アプリケーション全体で発生するイベントなど、リクエストに関する履歴情報を取得するのに役立ちます。たとえば、クエリが実行されるたびにスタックにプッシュするイベント リスナを作成し、クエリ SQL と期間をタプルとしてキャプチャできます。

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

// In AppServiceProvider.php...
DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

<!-- You may determine if a value is in a stack using the `stackContains` and `hiddenStackContains` methods: -->
`stackContains` メソッドと `hiddenStackContains` メソッドを使用して、値がスタック内にあるかどうかを確認できます。

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

<!-- The `stackContains` and `hiddenStackContains` methods also accept a closure as their second argument, allowing more control over the value comparison operation: -->
`stackContains` メソッドと `hiddenStackContains` メソッドは、2 番目の引数としてクロージャーも受け入れ、値の比較操作をより詳細に制御できるようにします。

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
`Context` ファサードの `get` メソッドを使用して、コンテキストから情報を取得できます。

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

<!-- The `only` and `except` methods may be used to retrieve a subset of the information in the context: -->
`only` メソッドと `except` メソッドは、コンテキスト内の情報のサブセットを取得するために使用できます。

```php
$data = Context::only(['first_key', 'second_key']);

$data = Context::except(['first_key']);
```

<!-- The `pull` method may be used to retrieve information from the context and immediately remove it from the context: -->
`pull` メソッドを使用すると、コンテキストから情報を取得し、それをコンテキストから即座に削除できます。

```php
$value = Context::pull('key');
```

<!-- If context data is stored in a [stack](#stacks), you may pop items from the stack using the `pop` method: -->
コンテキスト データが [stack](#stacks) に保存されている場合は、`pop` メソッドを使用してスタックから項目をポップできます。

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs');
// second_value

Context::get('breadcrumbs');
// ['first_value']
```

<!-- The `remember` and `rememberHidden` methods may be used to retrieve information from the context, while setting the context value to the value returned by the given closure if the requested information doesn't exist: -->
`remember` メソッドと `rememberHidden` メソッドは、コンテキストから情報を取得するために使用できますが、要求された情報が存在しない場合は、コンテキスト値を指定されたクロージャによって返される値に設定します。

```php
$permissions = Context::remember(
    'user-permissions',
    fn () => $user->permissions,
);
```

<!-- If you would like to retrieve all of the information stored in the context, you may invoke the `all` method: -->
コンテキストに保存されているすべての情報を取得したい場合は、`all` メソッドを呼び出します。

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
<!-- ### Determining Item Existence -->
### Determining Item Existence

<!-- You may use the `has` and `missing` methods to determine if the context has any value stored for the given key: -->
`has` メソッドと `missing` メソッドを使用して、コンテキストに指定されたキーに値が格納されているかどうかを確認できます。

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
`has` メソッドは、格納された値に関係なく、`true` を返します。したがって、たとえば、`null` 値を持つキーは存在するとみなされます。

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
<!-- ## Removing Context -->
## Removing Context

<!-- The `forget` method may be used to remove a key and its value from the current context: -->
`forget` メソッドは、現在のコンテキストからキーとその値を削除するために使用できます。

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

<!-- You may forget several keys at once by providing an array to the `forget` method: -->
`forget` メソッドに配列を指定すると、一度に複数のキーを忘れることがあります。

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
<!-- ## Hidden Context -->
## Hidden Context

<!-- Context offers the ability to store "hidden" data. This hidden information is not appended to logs, and is not accessible via the data retrieval methods documented above. Context provides a different set of methods to interact with hidden context information: -->
コンテキストは、「隠し」データを保存する機能を提供します。この隠された情報はログに追加されず、上記のデータ取得方法ではアクセスできません。 Context は、非表示のコンテキスト情報を操作するためのさまざまなメソッドのセットを提供します。

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

<!-- The "hidden" methods mirror the functionality of the non-hidden methods documented above: -->
「非表示」メソッドは、上記で説明した非非表示メソッドの機能を反映しています。

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
コンテキストは、コンテキストのハイドレーションおよびデハイドレーション プロセスにフックできる 2 つのイベントをディスパッチします。

<!-- To illustrate how these events may be used, imagine that in a middleware of your application you set the `app.locale` configuration value based on the incoming HTTP request's `Accept-Language` header. Context's events allow you to capture this value during the request and restore it on the queue, ensuring notifications sent on the queue have the correct `app.locale` value. We can use context's events and [hidden](#hidden-context) data to achieve this, which the following documentation will illustrate. -->
これらのイベントがどのように使用されるかを説明するために、アプリケーションのミドルウェアで、受信 HTTP リクエストの `Accept-Language` ヘッダーに基づいて `app.locale` 構成値を設定すると想像してください。コンテキストのイベントを使用すると、リクエスト中にこの値を取得してキューに復元できるため、キューに送信される通知に正しい `app.locale` 値が含まれるようになります。これを実現するには、コンテキストのイベントと [hidden](#hidden-context) データを使用できます。これについては、次のドキュメントで説明します。

<a name="dehydrating"></a>
<!-- ### Dehydrating -->
### Dehydrating

<!-- Whenever a job is dispatched to the queue the data in the context is "dehydrated" and captured alongside the job's payload. The `Context::dehydrating` method allows you to register a closure that will be invoked during the dehydration process. Within this closure, you may make changes to the data that will be shared with the queued job. -->
ジョブがキューにディスパッチされるたびに、コンテキスト内のデータは「デハイドレート」され、ジョブのペイロードとともにキャプチャされます。 `Context::dehydrating` メソッドを使用すると、デハイドレーション プロセス中に呼び出されるクロージャーを登録できます。このクロージャ内で、キューに入れられたジョブと共有されるデータに変更を加えることができます。

<!-- Typically, you should register `dehydrating` callbacks within the `boot` method of your application's `AppServiceProvider` class: -->
通常、アプリケーションの `AppServiceProvider` クラスの `boot` メソッド内で `dehydrating` コールバックを登録する必要があります。

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
> 現在のプロセスのコンテキストが変更されるため、`dehydrating` コールバック内で `Context` ファサードを使用しないでください。コールバックに渡されるリポジトリのみを変更するようにしてください。

<a name="hydrated"></a>
<!-- ### Hydrated -->
### Hydrated

<!-- Whenever a queued job begins executing on the queue, any context that was shared with the job will be "hydrated" back into the current context. The `Context::hydrated` method allows you to register a closure that will be invoked during the hydration process. -->
キューに入れられたジョブがキュー上で実行を開始すると、そのジョブと共有されていたコンテキストはすべて現在のコンテキストに「ハイドレート」されて戻ります。 `Context::hydrated` メソッドを使用すると、ハイドレーション プロセス中に呼び出されるクロージャーを登録できます。

<!-- Typically, you should register `hydrated` callbacks within the `boot` method of your application's `AppServiceProvider` class: -->
通常、アプリケーションの `AppServiceProvider` クラスの `boot` メソッド内で `hydrated` コールバックを登録する必要があります。

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
> `hydrated` コールバック内では `Context` ファサードを使用せず、コールバックに渡されるリポジトリのみを変更するようにしてください。

