<!-- # Laravel Pulse -->
# Laravel Pulse

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
- [Dashboard](#dashboard)
    - [Authorization](#dashboard-authorization)
    - [Customization](#dashboard-customization)
    - [Resolving Users](#dashboard-resolving-users)
    - [Cards](#dashboard-cards)
- [Capturing Entries](#capturing-entries)
    - [Recorders](#recorders)
    - [Filtering](#filtering)
- [Performance](#performance)
    - [Using a Different Database](#using-a-different-database)
    - [Redis Ingest](#ingest)
    - [Sampling](#sampling)
    - [Trimming](#trimming)
    - [Handling Pulse Exceptions](#pulse-exceptions)
- [Custom Cards](#custom-cards)
    - [Card Components](#custom-card-components)
    - [Styling](#custom-card-styling)
    - [Data Capture and Aggregation](#custom-card-data)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Pulse](https://github.com/laravel/pulse) delivers at-a-glance insights into your application's performance and usage. With Pulse, you can track down bottlenecks like slow jobs and endpoints, find your most active users, and more. -->
[Laravel Pulse](https://github.com/laravel/pulse) は、アプリケーションのパフォーマンスと使用状況を一目で把握できる情報を提供します。 Pulse を使用すると、遅いジョブやエンドポイントなどのボトルネックを追跡したり、最もアクティブなユーザーを見つけたりすることができます。

<!-- For in-depth debugging of individual events, check out [Laravel Telescope](/docs/master/telescope). -->
個々のイベントの詳細なデバッグについては、[Laravel Telescope](/docs/master/telescope) を確認してください。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Pulse のファーストパーティ ストレージ実装には現在、MySQL、MariaDB、または PostgreSQL データベースが必要です。別のデータベース エンジンを使用している場合は、Pulse データ用に別の MySQL、MariaDB、または PostgreSQL データベースが必要になります。

<!-- You may install Pulse using the Composer package manager: -->
Composer パッケージ マネージャーを使用して Pulse をインストールできます。

```shell
composer require laravel/pulse
```

<!-- Next, you should publish the Pulse configuration and migration files using the `vendor:publish` Artisan command: -->
次に、`vendor:publish` Artisan コマンドを使用して、Pulse 構成ファイルと移行ファイルを公開する必要があります。

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

<!-- Finally, you should run the `migrate` command in order to create the tables needed to store Pulse's data: -->
最後に、`migrate` コマンドを実行して、Pulse のデータを保存するために必要なテーブルを作成する必要があります。

```shell
php artisan migrate
```

<!-- Once Pulse's database migrations have been run, you may access the Pulse dashboard via the `/pulse` route. -->
Pulse のデータベース移行が実行されると、`/pulse` ルート経由で Pulse ダッシュボードにアクセスできるようになります。

> [!NOTE]
> Pulse データをアプリケーションのプライマリ データベースに保存したくない場合は、[specify a dedicated database connection](#using-a-different-database) を実行できます。

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Many of Pulse's configuration options can be controlled using environment variables. To see the available options, register new recorders, or configure advanced options, you may publish the `config/pulse.php` configuration file: -->
Pulse の構成オプションの多くは、環境変数を使用して制御できます。利用可能なオプションを確認したり、新しいレコーダーを登録したり、詳細オプションを構成したりするには、`config/pulse.php` 構成ファイルを公開します。

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
<!-- ## Dashboard -->
## Dashboard

<a name="dashboard-authorization"></a>
<!-- ### Authorization -->
### Authorization

<!-- The Pulse dashboard may be accessed via the `/pulse` route. By default, you will only be able to access this dashboard in the `local` environment, so you will need to configure authorization for your production environments by customizing the `'viewPulse'` authorization gate. You can accomplish this within your application's `app/Providers/AppServiceProvider.php` file: -->
Pulse ダッシュボードには、`/pulse` ルート経由でアクセスできます。デフォルトでは、`local` 環境でのみこのダッシュボードにアクセスできるため、`'viewPulse'` 認可ゲートをカスタマイズして実稼働環境の認可を構成する必要があります。これは、アプリケーションの `app/Providers/AppServiceProvider.php` ファイル内で実行できます。

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('viewPulse', function (User $user) {
        return $user->isAdmin();
    });

    // ...
}
```

<a name="dashboard-customization"></a>
<!-- ### Customization -->
### Customization

<!-- The Pulse dashboard cards and layout may be configured by publishing the dashboard view. The dashboard view will be published to `resources/views/vendor/pulse/dashboard.blade.php`: -->
Pulse ダッシュボード カードとレイアウトは、ダッシュボード ビューを公開することで構成できます。ダッシュボード ビューは `resources/views/vendor/pulse/dashboard.blade.php` に公開されます。

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

<!-- The dashboard is powered by [Livewire](https://livewire.laravel.com/), and allows you to customize the cards and layout without needing to rebuild any JavaScript assets. -->
ダッシュボードは [Livewire](https://livewire.laravel.com/) を利用しており、JavaScript アセットを再構築することなくカードとレイアウトをカスタマイズできます。

<!-- Within this file, the `<x-pulse>` component is responsible for rendering the dashboard and provides a grid layout for the cards. If you would like the dashboard to span the full width of the screen, you may provide the `full-width` prop to the component: -->
このファイル内では、`<x-pulse>` コンポーネントがダッシュボードのレンダリングを担当し、カードのグリッド レイアウトを提供します。ダッシュボードを画面の幅全体に広げたい場合は、コンポーネントに `full-width` プロパティを指定できます。

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

<!-- By default, the `<x-pulse>` component will create a 12 column grid, but you may customize this using the `cols` prop: -->
デフォルトでは、`<x-pulse>` コンポーネントは 12 列のグリッドを作成しますが、`cols` プロパティを使用してこれをカスタマイズできます。

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

<!-- Each card accepts a `cols` and `rows` prop to control the space and positioning: -->
各カードは、スペースと位置を制御するための `cols` および `rows` プロップを受け入れます。

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

<!-- Most cards also accept an `expand` prop to show the full card instead of scrolling: -->
ほとんどのカードは、スクロールする代わりにカード全体を表示する `expand` プロップも受け入れます。

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
<!-- ### Resolving Users -->
### Resolving Users

<!-- For cards that display information about your users, such as the Application Usage card, Pulse will only record the user's ID. When rendering the dashboard, Pulse will resolve the `name` and `email` fields from your default `Authenticatable` model and display avatars using the Gravatar web service. -->
アプリケーション使用状況カードなど、ユーザーに関する情報を表示するカードの場合、Pulse はユーザーの ID のみを記録します。ダッシュボードをレンダリングするとき、Pulse はデフォルトの `Authenticatable` モデルから `name` フィールドと `email` フィールドを解決し、Gravatar Web サービスを使用してアバターを表示します。

<!-- You may customize the fields and avatar by invoking the `Pulse::user` method within your application's `App\Providers\AppServiceProvider` class. -->
アプリケーションの `App\Providers\AppServiceProvider` クラス内で `Pulse::user` メソッドを呼び出すことで、フィールドとアバターをカスタマイズできます。

<!-- The `user` method accepts a closure which will receive the `Authenticatable` model to be displayed and should return an array containing `name`, `extra`, and `avatar` information for the user: -->
`user` メソッドは、表示される `Authenticatable` モデルを受け取るクロージャーを受け入れ、ユーザーの `name`、`extra`、および `avatar` 情報を含む配列を返す必要があります。

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::user(fn ($user) => [
        'name' => $user->name,
        'extra' => $user->email,
        'avatar' => $user->avatar_url,
    ]);

    // ...
}
```

> [!NOTE]
> `Laravel\Pulse\Contracts\ResolvesUsers` コントラクトを実装し、Laravel の [service container](/docs/master/container#binding-a-singleton) にバインドすることで、認証されたユーザーのキャプチャおよび取得方法を完全にカスタマイズできます。

<a name="dashboard-cards"></a>
<!-- ### Cards -->
### Cards

<a name="servers-card"></a>
<!-- #### Servers -->
#### Servers

<!-- The `<livewire:pulse.servers />` card displays system resource usage for all servers running the `pulse:check` command. Please refer to the documentation regarding the [servers recorder](#servers-recorder) for more information on system resource reporting. -->
`<livewire:pulse.servers />` カードには、`pulse:check` コマンドを実行しているすべてのサーバーのシステム リソース使用量が表示されます。システム リソース レポートの詳細については、[servers recorder](#servers-recorder) に関するドキュメントを参照してください。

<!-- If you replace a server in your infrastructure, you may wish to stop displaying the inactive server in the Pulse dashboard after a given duration. You may accomplish this using the `ignore-after` prop, which accepts the number of seconds after which inactive servers should be removed from the Pulse dashboard. Alternatively, you may provide a relative time formatted string, such as `1 hour` or `3 days and 1 hour`: -->
インフラストラクチャ内のサーバーを交換する場合、一定期間後に非アクティブなサーバーの Pulse ダッシュボードへの表示を停止したい場合があります。これは、非アクティブなサーバーが Pulse ダッシュボードから削除されるまでの秒数を受け入れる `ignore-after` プロパティを使用して実現できます。あるいは、`1 hour` や `3 days and 1 hour` などの相対時間形式の文字列を指定することもできます。

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
<!-- #### Application Usage -->
#### Application Usage

<!-- The `<livewire:pulse.usage />` card displays the top 10 users making requests to your application, dispatching jobs, and experiencing slow requests. -->
`<livewire:pulse.usage />` カードには、アプリケーションにリクエストを行ったり、ジョブをディスパッチしたり、リクエストの速度が遅くなったりしている上位 10 人のユーザーが表示されます。

<!-- If you wish to view all usage metrics on screen at the same time, you may include the card multiple times and specify the `type` attribute: -->
すべての使用状況メトリクスを画面上に同時に表示したい場合は、カードを複数回含めて、`type` 属性を指定できます。

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

<!-- To learn how to customize how Pulse retrieves and displays user information, consult our documentation on [resolving users](#dashboard-resolving-users). -->
Pulse がユーザー情報を取得して表示する方法をカスタマイズする方法については、[resolving users](#dashboard-resolving-users) のドキュメントを参照してください。

> [!NOTE]
> アプリケーションが大量のリクエストを受信したり、大量のジョブをディスパッチしたりする場合は、[sampling](#sampling) を有効にすることができます。詳細については、[user requests recorder](#user-requests-recorder)、[user jobs recorder](#user-jobs-recorder)、および [slow jobs recorder](#slow-jobs-recorder) のドキュメントを参照してください。

<a name="exceptions-card"></a>
<!-- #### Exceptions -->
#### Exceptions

<!-- The `<livewire:pulse.exceptions />` card shows the frequency and recency of exceptions occurring in your application. By default, exceptions are grouped based on the exception class and location where it occurred. See the [exceptions recorder](#exceptions-recorder) documentation for more information. -->
`<livewire:pulse.exceptions />` カードは、アプリケーションで発生する例外の頻度と最新性を示します。デフォルトでは、例外は例外クラスと例外が発生した場所に基づいてグループ化されます。詳細については、[exceptions recorder](#exceptions-recorder) のドキュメントを参照してください。

<a name="queues-card"></a>
<!-- #### Queues -->
#### Queues

<!-- The `<livewire:pulse.queues />` card shows the throughput of the queues in your application, including the number of jobs queued, processing, processed, released, and failed. See the [queues recorder](#queues-recorder) documentation for more information. -->
`<livewire:pulse.queues />` カードには、キューに入れられたジョブ、処理中のジョブ、処理されたジョブ、リリースされたジョブ、失敗したジョブの数など、アプリケーションのキューのスループットが表示されます。詳細については、[queues recorder](#queues-recorder) のドキュメントを参照してください。

<a name="slow-requests-card"></a>
<!-- #### Slow Requests -->
#### Slow Requests

<!-- The `<livewire:pulse.slow-requests />` card shows incoming requests to your application that exceed the configured threshold, which is 1,000ms by default. See the [slow requests recorder](#slow-requests-recorder) documentation for more information. -->
`<livewire:pulse.slow-requests />` カードは、設定されたしきい値 (デフォルトでは 1,000 ミリ秒) を超える、アプリケーションへの受信リクエストを表示します。詳細については、[slow requests recorder](#slow-requests-recorder) のドキュメントを参照してください。

<a name="slow-jobs-card"></a>
<!-- #### Slow Jobs -->
#### Slow Jobs

<!-- The `<livewire:pulse.slow-jobs />` card shows the queued jobs in your application that exceed the configured threshold, which is 1,000ms by default. See the [slow jobs recorder](#slow-jobs-recorder) documentation for more information. -->
`<livewire:pulse.slow-jobs />` カードには、設定されたしきい値 (デフォルトでは 1,000 ミリ秒) を超える、アプリケーション内のキューに入れられたジョブが表示されます。詳細については、[slow jobs recorder](#slow-jobs-recorder) のドキュメントを参照してください。

<a name="slow-queries-card"></a>
<!-- #### Slow Queries -->
#### Slow Queries

<!-- The `<livewire:pulse.slow-queries />` card shows the database queries in your application that exceed the configured threshold, which is 1,000ms by default. -->
`<livewire:pulse.slow-queries />` カードには、設定されたしきい値 (デフォルトでは 1,000 ミリ秒) を超えるアプリケーション内のデータベース クエリが表示されます。

<!-- By default, slow queries are grouped based on the SQL query (without bindings) and the location where it occurred, but you may choose to not capture the location if you wish to group solely on the SQL query. -->
デフォルトでは、遅いクエリは SQL クエリ (バインドなし) とそれが発生した場所に基づいてグループ化されますが、SQL クエリのみに基づいてグループ化したい場合は、場所を取得しないことも選択できます。

<!-- If you encounter rendering performance issues due to extremely large SQL queries receiving syntax highlighting, you may disable highlighting by adding the `without-highlighting` prop: -->
構文の強調表示を受け取る非常に大規模な SQL クエリが原因でレンダリングのパフォーマンスの問題が発生した場合は、`without-highlighting` プロパティを追加して強調表示を無効にすることができます。

```blade
<livewire:pulse.slow-queries without-highlighting />
```

<!-- See the [slow queries recorder](#slow-queries-recorder) documentation for more information. -->
詳細については、[slow queries recorder](#slow-queries-recorder) のドキュメントを参照してください。

<a name="slow-outgoing-requests-card"></a>
<!-- #### Slow Outgoing Requests -->
#### Slow Outgoing Requests

<!-- The `<livewire:pulse.slow-outgoing-requests />` card shows outgoing requests made using Laravel's [HTTP client](/docs/master/http-client) that exceed the configured threshold, which is 1,000ms by default. -->
`<livewire:pulse.slow-outgoing-requests />` カードは、Laravel の [HTTP client](/docs/master/http-client) を使用して行われた、設定されたしきい値 (デフォルトでは 1,000 ミリ秒) を超える送信リクエストを示します。

<!-- By default, entries will be grouped by the full URL. However, you may wish to normalize or group similar outgoing requests using regular expressions. See the [slow outgoing requests recorder](#slow-outgoing-requests-recorder) documentation for more information. -->
デフォルトでは、エントリは完全な URL によってグループ化されます。ただし、正規表現を使用して、同様の送信リクエストを正規化またはグループ化したい場合があります。詳細については、[slow outgoing requests recorder](#slow-outgoing-requests-recorder) のドキュメントを参照してください。

<a name="cache-card"></a>
<!-- #### Cache -->
#### Cache

<!-- The `<livewire:pulse.cache />` card shows the cache hit and miss statistics for your application, both globally and for individual keys. -->
`<livewire:pulse.cache />` カードは、アプリケーションのキャッシュ ヒットとミスの統計を、グローバルと個々のキーの両方で表示します。

<!-- By default, entries will be grouped by key. However, you may wish to normalize or group similar keys using regular expressions. See the [cache interactions recorder](#cache-interactions-recorder) documentation for more information. -->
デフォルトでは、エントリはキーごとにグループ化されます。ただし、正規表現を使用して類似したキーを正規化またはグループ化したい場合があります。詳細については、[cache interactions recorder](#cache-interactions-recorder) のドキュメントを参照してください。

<a name="capturing-entries"></a>
<!-- ## Capturing Entries -->
## Capturing Entries

<!-- Most Pulse recorders will automatically capture entries based on framework events dispatched by Laravel. However, the [servers recorder](#servers-recorder) and some third-party cards must poll for information regularly. To use these cards, you must run the `pulse:check` daemon on all of your individual application servers: -->
ほとんどの Pulse レコーダーは、Laravel によって送出されたフレームワーク イベントに基づいてエントリを自動的にキャプチャします。ただし、[servers recorder](#servers-recorder) および一部のサードパーティ カードは定期的に情報をポーリングする必要があります。これらのカードを使用するには、すべての個々のアプリケーション サーバーで `pulse:check` デーモンを実行する必要があります。

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` プロセスをバックグラウンドで永続的に実行し続けるには、Supervisorなどのプロセス モニターを使用して、コマンドの実行が停止しないようにする必要があります。

<!-- As the `pulse:check` command is a long-lived process, it will not see changes to your codebase without being restarted. You should gracefully restart the command by calling the `pulse:restart` command during your application's deployment process: -->
`pulse:check` コマンドは存続期間の長いプロセスであるため、再起動しない限りコードベースへの変更は表示されません。アプリケーションのデプロイメントプロセス中に `pulse:restart` コマンドを呼び出して、コマンドを正常に再起動する必要があります。

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse は [cache](/docs/master/cache) を使用して再起動信号を保存するため、この機能を使用する前に、キャッシュ ドライバがアプリケーションに対して適切に構成されていることを確認する必要があります。

<a name="recorders"></a>
<!-- ### Recorders -->
### Recorders

<!-- Recorders are responsible for capturing entries from your application to be recorded in the Pulse database. Recorders are registered and configured in the `recorders` section of the [Pulse configuration file](#configuration). -->
レコーダーは、アプリケーションからエントリを取得して Pulse データベースに記録する役割を果たします。レコーダーは、[Pulse configuration file](#configuration) の `recorders` セクションで登録および構成されます。

<a name="cache-interactions-recorder"></a>
<!-- #### Cache Interactions -->
#### Cache Interactions

<!-- The `CacheInteractions` recorder captures information about the [cache](/docs/master/cache) hits and misses occurring in your application for display on the [Cache](#cache-card) card. -->
`CacheInteractions` レコーダーは、アプリケーションで発生する [cache](/docs/master/cache) のヒットとミスに関する情報をキャプチャし、[Cache](#cache-card) カードに表示します。

<!-- You may optionally adjust the [sample rate](#sampling) and ignored key patterns. -->
必要に応じて、[sample rate](#sampling) および無視されるキー パターンを調整できます。

<!-- You may also configure key grouping so that similar keys are grouped as a single entry. For example, you may wish to remove unique IDs from keys caching the same type of information. Groups are configured using a regular expression to "find and replace" parts of the key. An example is included in the configuration file: -->
同様のキーが 1 つのエントリとしてグループ化されるように、キーのグループ化を構成することもできます。たとえば、同じ種類の情報をキャッシュしているキーから一意の ID を削除したい場合があります。グループは、キーの一部を「検索して置換」するための正規表現を使用して構成されます。例は構成ファイルに含まれています。

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

<!-- The first pattern that matches will be used. If no patterns match, then the key will be captured as-is. -->
最初に一致したパターンが使用されます。一致するパターンがない場合、キーはそのままキャプチャされます。

<a name="exceptions-recorder"></a>
<!-- #### Exceptions -->
#### Exceptions

<!-- The `Exceptions` recorder captures information about reportable exceptions occurring in your application for display on the [Exceptions](#exceptions-card) card. -->
`Exceptions` レコーダーは、アプリケーションで発生する報告可能な例外に関する情報をキャプチャし、[Exceptions](#exceptions-card) カードに表示します。

<!-- You may optionally adjust the [sample rate](#sampling) and ignored exception patterns. You may also configure whether to capture the location that the exception originated from. The captured location will be displayed on the Pulse dashboard which can help to track down the exception origin; however, if the same exception occurs in multiple locations then it will appear multiple times for each unique location. -->
必要に応じて、[sample rate](#sampling) および無視される例外パターンを調整できます。例外の発生元の場所をキャプチャするかどうかを構成することもできます。キャプチャされた位置は Pulse ダッシュボードに表示され、例外の原因を追跡するのに役立ちます。ただし、同じ例外が複数の場所で発生する場合は、一意の場所ごとに複数回表示されます。

<a name="queues-recorder"></a>
<!-- #### Queues -->
#### Queues

<!-- The `Queues` recorder captures information about your application's queues for display on the [Queues](#queues-card). -->
`Queues` レコーダーは、[Queues](#queues-card) に表示するためにアプリケーションのキューに関する情報をキャプチャします。

<!-- You may optionally adjust the [sample rate](#sampling) and ignored jobs patterns. -->
必要に応じて、[sample rate](#sampling) および無視されたジョブ パターンを調整できます。

<a name="slow-jobs-recorder"></a>
<!-- #### Slow Jobs -->
#### Slow Jobs

<!-- The `SlowJobs` recorder captures information about slow jobs occurring in your application for display on the [Slow Jobs](#slow-jobs-recorder) card. -->
`SlowJobs` レコーダーは、アプリケーションで発生する遅いジョブに関する情報をキャプチャし、[Slow Jobs](#slow-jobs-recorder) カードに表示します。

<!-- You may optionally adjust the slow job threshold, [sample rate](#sampling), and ignored job patterns. -->
オプションで、低速ジョブしきい値 [sample rate](#sampling) および無視されるジョブ パターンを調整できます。

<!-- You may have some jobs that you expect to take longer than others. In those cases, you may configure per-job thresholds: -->
他のジョブよりも時間がかかると予想されるジョブがいくつかあるかもしれません。そのような場合は、ジョブごとのしきい値を構成できます。

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

<!-- If no regular expression patterns match the job's classname, then the `'default'` value will be used. -->
ジョブのクラス名に一致する正規表現パターンがない場合は、`'default'` 値が使用されます。

<a name="slow-outgoing-requests-recorder"></a>
<!-- #### Slow Outgoing Requests -->
#### Slow Outgoing Requests

<!-- The `SlowOutgoingRequests` recorder captures information about outgoing HTTP requests made using Laravel's [HTTP client](/docs/master/http-client) that exceed the configured threshold for display on the [Slow Outgoing Requests](#slow-outgoing-requests-card) card. -->
`SlowOutgoingRequests` レコーダーは、Laravel の [HTTP client](/docs/master/http-client) を使用して行われた、[Slow Outgoing Requests](#slow-outgoing-requests-card) カードに表示するために構成されたしきい値を超える送信 HTTP リクエストに関する情報をキャプチャします。

<!-- You may optionally adjust the slow outgoing request threshold, [sample rate](#sampling), and ignored URL patterns. -->
オプションで、低速送信リクエストのしきい値、[sample rate](#sampling)、および無視される URL パターンを調整できます。

<!-- You may have some outgoing requests that you expect to take longer than others. In those cases, you may configure per-request thresholds: -->
他の送信リクエストよりも時間がかかると予想される送信リクエストがいくつかある場合があります。そのような場合は、リクエストごとのしきい値を構成できます。

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

<!-- If no regular expression patterns match the request's URL, then the `'default'` value will be used. -->
リクエストの URL に一致する正規表現パターンがない場合は、`'default'` 値が使用されます。

<!-- You may also configure URL grouping so that similar URLs are grouped as a single entry. For example, you may wish to remove unique IDs from URL paths or group by domain only. Groups are configured using a regular expression to "find and replace" parts of the URL. Some examples are included in the configuration file: -->
同様の URL が 1 つのエントリとしてグループ化されるように、URL グループ化を構成することもできます。たとえば、URL パスから一意の ID を削除したり、ドメインのみでグループ化したりすることができます。グループは、URL の一部を「検索して置換」するための正規表現を使用して構成されます。構成ファイルにはいくつかの例が含まれています。

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'groups' => [
        // '#^https://api\.github\.com/repos/.*$#' => 'api.github.com/repos/*',
        // '#^https?://([^/]*).*$#' => '\1',
        // '#/\d+#' => '/*',
    ],
],
```

<!-- The first pattern that matches will be used. If no patterns match, then the URL will be captured as-is. -->
最初に一致したパターンが使用されます。一致するパターンがない場合、URL はそのままキャプチャされます。

<a name="slow-queries-recorder"></a>
<!-- #### Slow Queries -->
#### Slow Queries

<!-- The `SlowQueries` recorder captures any database queries in your application that exceed the configured threshold for display on the [Slow Queries](#slow-queries-card) card. -->
`SlowQueries` レコーダーは、[Slow Queries](#slow-queries-card) カードに表示するために設定されたしきい値を超えるアプリケーション内のデータベース クエリをキャプチャします。

<!-- You may optionally adjust the slow query threshold, [sample rate](#sampling), and ignored query patterns. You may also configure whether to capture the query location. The captured location will be displayed on the Pulse dashboard which can help to track down the query origin; however, if the same query is made in multiple locations then it will appear multiple times for each unique location. -->
オプションで、低速クエリしきい値 [sample rate](#sampling) および無視されるクエリ パターンを調整できます。クエリの場所をキャプチャするかどうかを構成することもできます。キャプチャされた位置は Pulse ダッシュボードに表示され、クエリの発信元を追跡するのに役立ちます。ただし、同じクエリが複数の場所で作成された場合は、一意の場所ごとに複数回表示されます。

<!-- You may have some queries that you expect to take longer than others. In those cases, you may configure per-query thresholds: -->
他のクエリよりも時間がかかることが予想されるクエリがいくつかあるかもしれません。そのような場合は、クエリごとのしきい値を構成できます。

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

<!-- If no regular expression patterns match the query's SQL, then the `'default'` value will be used. -->
クエリの SQL に一致する正規表現パターンがない場合は、`'default'` 値が使用されます。

<a name="slow-requests-recorder"></a>
<!-- #### Slow Requests -->
#### Slow Requests

<!-- The `Requests` recorder captures information about requests made to your application for display on the [Slow Requests](#slow-requests-card) and [Application Usage](#application-usage-card) cards. -->
`Requests` レコーダーは、[Slow Requests](#slow-requests-card) カードおよび [Application Usage](#application-usage-card) カードに表示するためにアプリケーションに対して行われたリクエストに関する情報をキャプチャします。

<!-- You may optionally adjust the slow route threshold, [sample rate](#sampling), and ignored paths. -->
オプションで、低速ルートのしきい値、[sample rate](#sampling)、および無視されるパスを調整できます。

<!-- You may have some requests that you expect to take longer than others. In those cases, you may configure per-request thresholds: -->
他のリクエストよりも時間がかかることが予想されるリクエストもあるかもしれません。そのような場合は、リクエストごとのしきい値を構成できます。

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

<!-- If no regular expression patterns match the request's URL, then the `'default'` value will be used. -->
リクエストの URL に一致する正規表現パターンがない場合は、`'default'` 値が使用されます。

<a name="servers-recorder"></a>
<!-- #### Servers -->
#### Servers

<!-- The `Servers` recorder captures CPU, memory, and storage usage of the servers that power your application for display on the [Servers](#servers-card) card. This recorder requires the [pulse:check command](#capturing-entries) to be running on each of the servers you wish to monitor. -->
`Servers` レコーダーは、[Servers](#servers-card) カードに表示するためにアプリケーションに電力を供給するサーバーの CPU、メモリ、ストレージの使用状況をキャプチャします。このレコーダーを使用するには、監視する各サーバー上で [pulse:check command](#capturing-entries) が実行されている必要があります。

<!-- Each reporting server must have a unique name. By default, Pulse will use the value returned by PHP's `gethostname` function. If you wish to customize this, you may set the `PULSE_SERVER_NAME` environment variable: -->
各レポート サーバーには一意の名前が必要です。デフォルトでは、Pulse は PHP の `gethostname` 関数によって返された値を使用します。これをカスタマイズしたい場合は、`PULSE_SERVER_NAME` 環境変数を設定します。

```env
PULSE_SERVER_NAME=load-balancer
```

<!-- The Pulse configuration file also allows you to customize the directories that are monitored. -->
Pulse 構成ファイルを使用すると、監視されるディレクトリをカスタマイズすることもできます。

<a name="user-jobs-recorder"></a>
<!-- #### User Jobs -->
#### User Jobs

<!-- The `UserJobs` recorder captures information about the users dispatching jobs in your application for display on the [Application Usage](#application-usage-card) card. -->
`UserJobs` レコーダーは、アプリケーションでジョブをディスパッチしているユーザーに関する情報をキャプチャし、[Application Usage](#application-usage-card) カードに表示します。

<!-- You may optionally adjust the [sample rate](#sampling) and ignored job patterns. -->
必要に応じて、[sample rate](#sampling) および無視されたジョブ パターンを調整できます。

<a name="user-requests-recorder"></a>
<!-- #### User Requests -->
#### User Requests

<!-- The `UserRequests` recorder captures information about the users making requests to your application for display on the [Application Usage](#application-usage-card) card. -->
`UserRequests` レコーダーは、[Application Usage](#application-usage-card) カードに表示するためにアプリケーションにリクエストを行っているユーザーに関する情報をキャプチャします。

<!-- You may optionally adjust the [sample rate](#sampling) and ignored URL patterns. -->
必要に応じて、[sample rate](#sampling) および無視される URL パターンを調整できます。

<a name="filtering"></a>
<!-- ### Filtering -->
### Filtering

<!-- As we have seen, many [recorders](#recorders) offer the ability to, via configuration, "ignore" incoming entries based on their value, such as a request's URL. But, sometimes it may be useful to filter out records based on other factors, such as the currently authenticated user. To filter out these records, you may pass a closure to Pulse's `filter` method. Typically, the `filter` method should be invoked within the `boot` method of your application's `AppServiceProvider`: -->
これまで見てきたように、多くの [recorders](#recorders) は、構成を通じて、リクエストの URL などの値に基づいて受信エントリを「無視」する機能を提供します。ただし、現在認証されているユーザーなど、他の要素に基づいてレコードをフィルターで除外すると便利な場合があります。これらのレコードをフィルターで除外するには、Pulse の `filter` メソッドにクロージャを渡すことができます。通常、`filter` メソッドは、アプリケーションの `AppServiceProvider` の `boot` メソッド内で呼び出す必要があります。

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::filter(function (Entry|Value $entry) {
        return Auth::user()->isNotAdmin();
    });

    // ...
}
```

<a name="performance"></a>
<!-- ## Performance -->
## Performance

<!-- Pulse has been designed to drop into an existing application without requiring any additional infrastructure. However, for high-traffic applications, there are several ways of removing any impact Pulse may have on your application's performance. -->
Pulse は、追加のインフラストラクチャを必要とせずに、既存のアプリケーションに組み込めるように設計されています。ただし、トラフィックの多いアプリケーションの場合、Pulse がアプリケーションのパフォーマンスに与える影響を取り除く方法がいくつかあります。

<a name="using-a-different-database"></a>
<!-- ### Using a Different Database -->
### Using a Different Database

<!-- For high-traffic applications, you may prefer to use a dedicated database connection for Pulse to avoid impacting your application database. -->
トラフィックの多いアプリケーションの場合は、アプリケーション データベースへの影響を避けるために、Pulse 専用のデータベース接続を使用することをお勧めします。

<!-- You may customize the [database connection](/docs/master/database#configuration) used by Pulse by setting the `PULSE_DB_CONNECTION` environment variable. -->
`PULSE_DB_CONNECTION` 環境変数を設定することで、Pulse によって使用される [database connection](/docs/master/database#configuration) をカスタマイズできます。

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
<!-- ### Redis Ingest -->
### Redis Ingest

> [!WARNING]
> Redis Ingest には、Redis 6.2 以降と、アプリケーションの構成済み Redis クライアント ドライバとして `phpredis` または `predis` が必要です。

<!-- By default, Pulse will store entries directly to the [configured database connection](#using-a-different-database) after the HTTP response has been sent to the client or a job has been processed; however, you may use Pulse's Redis ingest driver to send entries to a Redis stream instead. This can be enabled by configuring the `PULSE_INGEST_DRIVER` environment variable: -->
デフォルトでは、Pulse は、HTTP 応答がクライアントに送信された後、またはジョブが処理された後、エントリを [configured database connection](#using-a-different-database) に直接保存します。ただし、代わりに Pulse の Redis インジェスト ドライバを使用して、エントリを Redis ストリームに送信することもできます。これは、`PULSE_INGEST_DRIVER` 環境変数を構成することで有効にできます。

```ini
PULSE_INGEST_DRIVER=redis
```

<!-- Pulse will use your default [Redis connection](/docs/master/redis#configuration) by default, but you may customize this via the `PULSE_REDIS_CONNECTION` environment variable: -->
Pulse はデフォルトでデフォルトの [Redis connection](/docs/master/redis#configuration) を使用しますが、`PULSE_REDIS_CONNECTION` 環境変数を使用してこれをカスタマイズできます。

```ini
PULSE_REDIS_CONNECTION=pulse
```

> [!WARNING]
> Redis インジェスト ドライバを使用する場合、Pulse インストールでは、該当する場合、Redis を利用したキューとは異なる Redis 接続を常に使用する必要があります。

<!-- When using the Redis ingest, you will need to run the `pulse:work` command to monitor the stream and move entries from Redis into Pulse's database tables. -->
Redis インジェストを使用する場合、`pulse:work` コマンドを実行してストリームを監視し、エントリを Redis から Pulse のデータベース テーブルに移動する必要があります。

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` プロセスをバックグラウンドで永続的に実行し続けるには、Supervisorなどのプロセス モニターを使用して、Pulse ワーカーの実行が停止しないようにする必要があります。

<!-- As the `pulse:work` command is a long-lived process, it will not see changes to your codebase without being restarted. You should gracefully restart the command by calling the `pulse:restart` command during your application's deployment process: -->
`pulse:work` コマンドは存続期間の長いプロセスであるため、再起動しない限りコードベースへの変更は表示されません。アプリケーションのデプロイメントプロセス中に `pulse:restart` コマンドを呼び出して、コマンドを正常に再起動する必要があります。

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse は [cache](/docs/master/cache) を使用して再起動信号を保存するため、この機能を使用する前に、キャッシュ ドライバがアプリケーションに対して適切に構成されていることを確認する必要があります。

<a name="sampling"></a>
<!-- ### Sampling -->
### Sampling

<!-- By default, Pulse will capture every relevant event that occurs in your application. For high-traffic applications, this can result in needing to aggregate millions of database rows in the dashboard, especially for longer time periods. -->
デフォルトでは、Pulse はアプリケーションで発生するすべての関連イベントをキャプチャします。トラフィックの多いアプリケーションの場合、特に長期間にわたって、ダッシュボードに何百万ものデータベース行を集約する必要が生じる可能性があります。

<!-- You may instead choose to enable "sampling" on certain Pulse data recorders. For example, setting the sample rate to `0.1` on the [User Requests](#user-requests-recorder) recorder will mean that you only record approximately 10% of the requests to your application. In the dashboard, the values will be scaled up and prefixed with a `~` to indicate that they are an approximation. -->
代わりに、特定の Pulse データ レコーダーで「サンプリング」を有効にすることを選択できます。たとえば、[User Requests](#user-requests-recorder) レコーダーでサンプル レートを `0.1` に設定すると、アプリケーションへのリクエストの約 10% のみが記録されることになります。ダッシュボードでは、値がスケールアップされ、近似値であることを示すために `~` という接頭辞が付けられます。

<!-- In general, the more entries you have for a particular metric, the lower you can safely set the sample rate without sacrificing too much accuracy. -->
一般に、特定のメトリクスのエントリが多いほど、精度をあまり犠牲にすることなくサンプル レートを安全に低く設定できます。

<a name="trimming"></a>
<!-- ### Trimming -->
### Trimming

<!-- Pulse will automatically trim its stored entries once they are outside of the dashboard window. Trimming occurs when ingesting data using a lottery system which may be customized in the Pulse [configuration file](#configuration). -->
Pulse は、保存されているエントリがダッシュボード ウィンドウの外に出ると、自動的にトリミングします。トリミングは、Pulse [configuration file](#configuration) でカスタマイズできる抽選システムを使用してデータを取り込むときに発生します。

<a name="pulse-exceptions"></a>
<!-- ### Handling Pulse Exceptions -->
### Handling Pulse Exceptions

<!-- If an exception occurs while capturing Pulse data, such as being unable to connect to the storage database, Pulse will silently fail to avoid impacting your application. -->
ストレージ データベースに接続できないなど、Pulse データのキャプチャ中に例外が発生した場合、Pulse はアプリケーションへの影響を回避するためにサイレントに失敗します。

<!-- If you wish to customize how these exceptions are handled, you may provide a closure to the `handleExceptionsUsing` method: -->
これらの例外の処理方法をカスタマイズしたい場合は、`handleExceptionsUsing` メソッドにクロージャを提供できます。

```php
use Laravel\Pulse\Facades\Pulse;
use Illuminate\Support\Facades\Log;

Pulse::handleExceptionsUsing(function ($e) {
    Log::debug('An exception happened in Pulse', [
        'message' => $e->getMessage(),
        'stack' => $e->getTraceAsString(),
    ]);
});
```

<a name="custom-cards"></a>
<!-- ## Custom Cards -->
## Custom Cards

<!-- Pulse allows you to build custom cards to display data relevant to your application's specific needs. Pulse uses [Livewire](https://livewire.laravel.com), so you may want to [review its documentation](https://livewire.laravel.com/docs) before building your first custom card. -->
Pulse を使用すると、アプリケーションの特定のニーズに関連するデータを表示するカスタム カードを作成できます。 Pulse は [Livewire](https://livewire.laravel.com) を使用するため、最初のカスタム カードを作成する前に [review its documentation](https://livewire.laravel.com/docs) を実行することをお勧めします。

<a name="custom-card-components"></a>
<!-- ### Card Components -->
### Card Components

<!-- Creating a custom card in Laravel Pulse starts with extending the base `Card` Livewire component and defining a corresponding view: -->
Laravel Pulse でカスタム カードを作成するには、ベースの `Card` Livewire コンポーネントを拡張し、対応するビューを定義することから始まります。

```php
namespace App\Livewire\Pulse;

use Laravel\Pulse\Livewire\Card;
use Livewire\Attributes\Lazy;

#[Lazy]
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers');
    }
}
```

<!-- When using Livewire's [lazy loading](https://livewire.laravel.com/docs/lazy) feature, The `Card` component will automatically provide a placeholder that respects the `cols` and `rows` attributes passed to your component. -->
Livewire の [lazy loading](https://livewire.laravel.com/docs/lazy) 機能を使用する場合、`Card` コンポーネントは、コンポーネントに渡された `cols` 属性と `rows` 属性を尊重するプレースホルダーを自動的に提供します。

<!-- When writing your Pulse card's corresponding view, you may leverage Pulse's Blade components for a consistent look and feel: -->
Pulse カードの対応するビューを作成するときは、一貫したルック アンド フィールを実現するために Pulse の Blade コンポーネントを利用できます。

```blade
<x-pulse::card :cols="$cols" :rows="$rows" :class="$class" wire:poll.5s="">
    <x-pulse::card-header name="Top Sellers">
        <x-slot:icon>
            ...
        </x-slot:icon>
    </x-pulse::card-header>

    <x-pulse::scroll :expand="$expand">
        ...
    </x-pulse::scroll>
</x-pulse::card>
```

<!-- The `$cols`, `$rows`, `$class`, and `$expand` variables should be passed to their respective Blade components so the card layout may be customized from the dashboard view. You may also wish to include the `wire:poll.5s=""` attribute in your view to have the card automatically update. -->
カード レイアウトをダッシュ​​ボード ビューからカスタマイズできるように、`$cols`、`$rows`、`$class`、および `$expand` 変数をそれぞれのBlade コンポーネントに渡す必要があります。カードを自動的に更新するために、ビューに `wire:poll.5s=""` 属性を含めることもできます。

<!-- Once you have defined your Livewire component and template, the card may be included in your [dashboard view](#dashboard-customization): -->
Livewire コンポーネントとテンプレートを定義したら、カードを [dashboard view](#dashboard-customization) に含めることができます。

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> カードがパッケージに含まれている場合は、`Livewire::component` メソッドを使用してコンポーネントを Livewire に登録する必要があります。

<a name="custom-card-styling"></a>
<!-- ### Styling -->
### Styling

<!-- If your card requires additional styling beyond the classes and components included with Pulse, there are a few options for including custom CSS for your cards. -->
カードに Pulse に含まれるクラスやコンポーネント以外の追加のスタイルが必要な場合は、カードにカスタム CSS を含めるオプションがいくつかあります。

<a name="custom-card-styling-vite"></a>
<!-- #### Laravel Vite Integration -->
#### Laravel Vite Integration

<!-- If your custom card lives within your application's code base and you are using Laravel's [Vite integration](/docs/master/vite), you may update your `vite.config.js` file to include a dedicated CSS entry point for your card: -->
カスタム カードがアプリケーションのコード ベース内にあり、Laravel の [Vite integration](/docs/master/vite) を使用している場合は、`vite.config.js` ファイルを更新して、カードの専用 CSS エントリ ポイントを含めることができます。

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

<!-- You may then use the `@vite` Blade directive in your [dashboard view](#dashboard-customization), specifying the CSS entrypoint for your card: -->
次に、[dashboard view](#dashboard-customization) で `@vite` Blade ディレクティブを使用し、カードの CSS エントリポイントを指定します。

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
<!-- #### CSS Files -->
#### CSS Files

<!-- For other use cases, including Pulse cards contained within a package, you may instruct Pulse to load additional stylesheets by defining a `css` method on your Livewire component that returns the file path to your CSS file: -->
パッケージ内に含まれる Pulse カードなど、他の使用例では、CSS ファイルへのファイル パスを返す Livewire コンポーネントで `css` メソッドを定義することで、追加のスタイルシートをロードするように Pulse に指示できます。

```php
class TopSellers extends Card
{
    // ...

    protected function css()
    {
        return __DIR__.'/../../dist/top-sellers.css';
    }
}
```

<!-- When this card is included on the dashboard, Pulse will automatically include the contents of this file within a `<style>` tag so it does not need to be published to the `public` directory. -->
このカードがダッシュボードに含まれる場合、Pulse はこのファイルの内容を `<style>` タグ内に自動的に含めるため、`public` ディレクトリに公開する必要はありません。

<a name="custom-card-styling-tailwind"></a>
<!-- #### Tailwind CSS -->
#### Tailwind CSS

<!-- When using Tailwind CSS, you should create a dedicated CSS entrypoint. The following example excludes Tailwind's [Preflight](https://tailwindcss.com/docs/preflight) base styles which are already included by Pulse, and scopes Tailwind using a CSS selector to avoid conflicts with Pulse's Tailwind classes: -->
Tailwind CSS を使用する場合は、専用の CSS エントリポイントを作成する必要があります。次の例では、Pulse に既に含まれている Tailwind の [Preflight](https://tailwindcss.com/docs/preflight) 基本スタイルを除外し、CSS セレクターを使用して Tailwind のスコープを設定して、Pulse の Tailwind クラスとの競合を回避します。

```css
@import "tailwindcss/theme.css";

@custom-variant dark (&:where(.dark, .dark *));
@source "./../../views/livewire/pulse/top-sellers.blade.php";

@theme {
  /* ... */
}

#top-sellers {
  @import "tailwindcss/utilities.css" source(none);
}
```

<!-- You will also need to include an `id` or `class` attribute in your card's view that matches the CSS selector in your entrypoint: -->
また、エントリーポイントの CSS セレクターと一致する `id` または `class` 属性をカードのビューに含める必要があります。

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
<!-- ### Data Capture and Aggregation -->
### Data Capture and Aggregation

<!-- Custom cards may fetch and display data from anywhere; however, you may wish to leverage Pulse's powerful and efficient data recording and aggregation system. -->
カスタム カードはどこからでもデータを取得して表示できます。ただし、Pulse の強力で効率的なデータ記録および集計システムを活用したい場合もあります。

<a name="custom-card-data-capture"></a>
<!-- #### Capturing Entries -->
#### Capturing Entries

<!-- Pulse allows you to record "entries" using the `Pulse::record` method: -->
Pulse では、`Pulse::record` メソッドを使用して「エントリ」を記録できます。

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

<!-- The first argument provided to the `record` method is the `type` for the entry you are recording, while the second argument is the `key` that determines how the aggregated data should be grouped. For most aggregation methods you will also need to specify a `value` to be aggregated. In the example above, the value being aggregated is `$sale->amount`. You may then invoke one or more aggregation methods (such as `sum`) so that Pulse may capture pre-aggregated values into "buckets" for efficient retrieval later. -->
`record` メソッドに指定される最初の引数は、記録しているエントリの `type` であり、2 番目の引数は、集計されたデータをグループ化する方法を決定する `key` です。ほとんどの集計方法では、集計対象の `value` も指定する必要があります。上の例では、集計される値は `$sale->amount` です。次に、1 つ以上の集計メソッド (`sum` など) を呼び出して、Pulse が事前に集計された値を「バケット」にキャプチャして、後で効率的に取得できるようにすることができます。

<!-- The available aggregation methods are: -->
使用可能な集計方法は次のとおりです。

<!--
* `avg`
* `count`
* `max`
* `min`
* `sum`
-->
* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 現在認証されているユーザー ID を取得するカード パッケージを構築する場合は、アプリケーションに対して作成された [user resolver customizations](#dashboard-resolving-users) を尊重する `Pulse::resolveAuthenticatedUserId()` メソッドを使用する必要があります。

<a name="custom-card-data-retrieval"></a>
<!-- #### Retrieving Aggregate Data -->
#### Retrieving Aggregate Data

<!-- When extending Pulse's `Card` Livewire component, you may use the `aggregate` method to retrieve aggregated data for the period being viewed in the dashboard: -->
Pulse の `Card` Livewire コンポーネントを拡張する場合、`aggregate` メソッドを使用して、ダッシュボードに表示されている期間の集計データを取得できます。

```php
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers', [
            'topSellers' => $this->aggregate('user_sale', ['sum', 'count'])
        ]);
    }
}
```

<!-- The `aggregate` method returns a collection of PHP `stdClass` objects. Each object will contain the `key` property captured earlier, along with keys for each of the requested aggregates: -->
`aggregate` メソッドは、PHP `stdClass` オブジェクトのコレクションを返します。各オブジェクトには、前に取得した `key` プロパティと、要求された各集計のキーが含まれます。

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

<!-- Pulse will primarily retrieve data from the pre-aggregated buckets; therefore, the specified aggregates must have been captured up-front using the `Pulse::record` method. The oldest bucket will typically fall partially outside the period, so Pulse will aggregate the oldest entries to fill the gap and give an accurate value for the entire period, without needing to aggregate the entire period on each poll request. -->
Pulse は主に、事前に集約されたバケットからデータを取得します。したがって、指定された集計は、`Pulse::record` メソッドを使用して事前にキャプチャされている必要があります。通常、最も古いバケットは部分的に期間外にあるため、Pulse は最も古いエントリを集計してギャップを埋め、各ポーリング リクエストで期間全体を集計する必要なく、期間全体の正確な値を提供します。

<!-- You may also retrieve a total value for a given type by using the `aggregateTotal` method. For example, the following method would retrieve the total of all user sales instead of grouping them by user. -->
`aggregateTotal` メソッドを使用して、特定のタイプの合計値を取得することもできます。たとえば、次のメソッドは、ユーザーごとにグループ化するのではなく、すべてのユーザーの売上の合計を取得します。

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
<!-- #### Displaying Users -->
#### Displaying Users

<!-- When working with aggregates that record a user ID as the key, you may resolve the keys to user records using the `Pulse::resolveUsers` method: -->
ユーザー ID をキーとして記録する集計を操作する場合、`Pulse::resolveUsers` メソッドを使用してキーをユーザー レコードに解決できます。

```php
$aggregates = $this->aggregate('user_sale', ['sum', 'count']);

$users = Pulse::resolveUsers($aggregates->pluck('key'));

return view('livewire.pulse.top-sellers', [
    'sellers' => $aggregates->map(fn ($aggregate) => (object) [
        'user' => $users->find($aggregate->key),
        'sum' => $aggregate->sum,
        'count' => $aggregate->count,
    ])
]);
```

<!-- The `find` method returns an object containing `name`, `extra`, and `avatar` keys, which you may optionally pass directly to the `<x-pulse::user-card>` Blade component: -->
`find` メソッドは、`name`、`extra`、および `avatar` キーを含むオブジェクトを返します。オプションで、これらのキーを `<x-pulse::user-card>` Blade コンポーネントに直接渡すこともできます。

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
<!-- #### Custom Recorders -->
#### Custom Recorders

<!-- Package authors may wish to provide recorder classes to allow users to configure the capturing of data. -->
パッケージ作成者は、ユーザーがデータのキャプチャを構成できるようにレコーダー クラスを提供したい場合があります。

<!-- Recorders are registered in the `recorders` section of the application's `config/pulse.php` configuration file: -->
レコーダーは、アプリケーションの `config/pulse.php` 構成ファイルの `recorders` セクションに登録されます。

```php
[
    // ...
    'recorders' => [
        Acme\Recorders\Deployments::class => [
            // ...
        ],

        // ...
    ],
]
```

<!-- Recorders may listen to events by specifying a `$listen` property. Pulse will automatically register the listeners and call the recorders `record` method: -->
レコーダーは、`$listen` プロパティを指定することでイベントをリッスンできます。 Pulse は自動的にリスナを登録し、レコーダーの `record` メソッドを呼び出します。

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * The events to listen for.
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * Record the deployment.
     */
    public function record(Deployment $event): void
    {
        $config = Config::get('pulse.recorders.'.static::class);

        Pulse::record(
            // ...
        );
    }
}
```

