# コンテクスト (Context)

- [Introduction](#introduction)
    - [仕組み](#how-it-works)
- [コンテキストのキャプチャ](#capturing-context)
    - [Stacks](#stacks)
- [コンテキストの取得](#retrieving-context)
    - [アイテムの存在を判断する](#determining-item-existence)
- [コンテキストの削除](#removing-context)
- [隠されたコンテキスト](#hidden-context)
- [Events](#events)
    - [Dehydrating](#dehydrating)
    - [Hydrated](#hydrated)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel の「コンテキスト」機能を使用すると、アプリケーション内で実行されるリクエスト、ジョブ、コマンド全体にわたって情報をキャプチャ、取得、共有できます。この取得された情報は、アプリケーションによって書き込まれるログにも含まれるため、ログ エントリが書き込まれる前に発生した周囲のコード実行履歴についてより深い洞察が得られ、分散システム全体の実行フローを追跡できるようになります。

<a name="how-it-works"></a>
### 仕組み

Laravel のコンテキスト機能を理解する最良の方法は、組み込みのログ機能を使用して実際の動作を確認することです。まず、`Context` ファサードを使用して [コンテキストに情報を追加する](#capturing-context) を実行します。この例では、[middleware](/docs/{{version}}/middleware) を使用して、すべての受信リクエストのコンテキストにリクエスト URL と一意のトレース ID を追加します。

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

コンテキストに追加された情報は、リクエスト全体に書き込まれるすべての [ログエントリ](/docs/{{version}}/logging) にメタデータとして自動的に追加されます。コンテキストをメタデータとして追加すると、個々のログ エントリに渡される情報を、`Context` を介して共有される情報と区別できるようになります。たとえば、次のログ エントリを書き込むとします。

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);
```

書き込まれたログには、ログ エントリに渡された `auth_id` が含まれますが、コンテキストの `url` および `trace_id` もメタデータとして含まれます。

```
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

コンテキストに追加された情報は、キューにディスパッチされたジョブでも利用できるようになります。たとえば、コンテキストに情報を追加した後、`ProcessPodcast` ジョブをキューにディスパッチするとします。

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);
```

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

結果として得られるログ エントリには、最初にジョブをディスパッチしたリクエスト中にコンテキストに追加された情報が含まれます。

```
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}
```

Laravel コンテキストの組み込みロギング関連機能に焦点を当ててきましたが、次のドキュメントでは、コンテキストを使用して HTTP リクエスト/キューに入れられたジョブの境界を越えて情報を共有する方法と、ログエントリで書き込まれない [隠されたコンテキストデータ](#hidden-context) を追加する方法についても説明します。

<a name="capturing-context"></a>
## コンテキストのキャプチャ (Capturing Context)

`Context` ファサードの `add` メソッドを使用して、現在のコンテキストに情報を保存できます。

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');
```

複数の項目を一度に追加するには、連想配列を `add` メソッドに渡すことができます。

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);
```

`add` メソッドは、同じキーを共有する既存の値をオーバーライドします。キーがまだ存在しない場合にのみコンテキストに情報を追加したい場合は、`addIf` メソッドを使用できます。

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"
```

<a name="conditional-context"></a>
#### 条件付きコンテキスト

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

<a name="stacks"></a>
### スタック

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

スタックは、アプリケーション全体で発生するイベントなど、リクエストに関する履歴情報を取得するのに役立ちます。たとえば、クエリが実行されるたびにスタックにプッシュするイベント リスナを作成し、クエリ SQL と期間をタプルとしてキャプチャできます。

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});
```

`stackContains` メソッドと `hiddenStackContains` メソッドを使用して、値がスタック内にあるかどうかを確認できます。

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}
```

`stackContains` メソッドと `hiddenStackContains` メソッドは、2 番目の引数としてクロージャーも受け入れ、値の比較操作をより詳細に制御できるようにします。

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});
```

<a name="retrieving-context"></a>
## コンテキストの取得 (Retrieving Context)

`Context` ファサードの `get` メソッドを使用して、コンテキストから情報を取得できます。

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');
```

`only` メソッドを使用して、コンテキスト内の情報のサブセットを取得できます。

```php
$data = Context::only(['first_key', 'second_key']);
```

`pull` メソッドを使用すると、コンテキストから情報を取得し、それをコンテキストから即座に削除できます。

```php
$value = Context::pull('key');
```

コンテキスト データが [stack](#stacks) に保存されている場合は、`pop` メソッドを使用してスタックから項目をポップできます。

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs')
// second_value

Context::get('breadcrumbs');
// ['first_value'] 
```

コンテキストに保存されているすべての情報を取得したい場合は、`all` メソッドを呼び出します。

```php
$data = Context::all();
```

<a name="determining-item-existence"></a>
### アイテムの存在を判断する

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

`has` メソッドは、格納された値に関係なく、`true` を返します。したがって、たとえば、`null` 値を持つキーは存在するとみなされます。

```php
Context::add('key', null);

Context::has('key');
// true
```

<a name="removing-context"></a>
## コンテキストの削除 (Removing Context)

`forget` メソッドは、現在のコンテキストからキーとその値を削除するために使用できます。

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]
```

`forget` メソッドに配列を指定すると、一度に複数のキーを忘れることがあります。

```php
Context::forget(['first_key', 'second_key']);
```

<a name="hidden-context"></a>
## 隠されたコンテキスト (Hidden Context)

コンテキストは、「隠し」データを保存する機能を提供します。この隠された情報はログに追加されず、上記のデータ取得方法ではアクセスできません。 Context は、非表示のコンテキスト情報を操作するためのさまざまなメソッドのセットを提供します。

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null
```

「非表示」メソッドは、上記で説明した非非表示メソッドの機能を反映しています。

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
## イベント (Events)

コンテキストは、コンテキストのハイドレーションおよびデハイドレーション プロセスにフックできる 2 つのイベントをディスパッチします。

これらのイベントがどのように使用されるかを説明するために、アプリケーションのミドルウェアで、受信 HTTP リクエストの `Accept-Language` ヘッダーに基づいて `app.locale` 構成値を設定すると想像してください。コンテキストのイベントを使用すると、リクエスト中にこの値を取得してキューに復元できるため、キューに送信される通知に正しい `app.locale` 値が含まれるようになります。これを実現するには、コンテキストのイベントと [hidden](#hidden-context) データを使用できます。これについては、次のドキュメントで説明します。

<a name="dehydrating"></a>
### 脱水症状

ジョブがキューにディスパッチされるたびに、コンテキスト内のデータは「デハイドレート」され、ジョブのペイロードとともにキャプチャされます。 `Context::dehydrating` メソッドを使用すると、デハイドレーション プロセス中に呼び出されるクロージャーを登録できます。このクロージャ内で、キューに入れられたジョブと共有されるデータに変更を加えることができます。

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
### 水分補給

キューに入れられたジョブがキュー上で実行を開始すると、そのジョブと共有されていたコンテキストはすべて現在のコンテキストに「ハイドレート」されて戻ります。 `Context::hydrated` メソッドを使用すると、ハイドレーション プロセス中に呼び出されるクロージャーを登録できます。

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

