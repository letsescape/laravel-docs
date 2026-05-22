# Laravel Pulse (Laravel Pulse)

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
- [Dashboard](#dashboard)
    - [Authorization](#dashboard-authorization)
    - [Customization](#dashboard-customization)
    - [ユーザーの解決](#dashboard-resolving-users)
    - [Cards](#dashboard-cards)
- [エントリのキャプチャ](#capturing-entries)
    - [Recorders](#recorders)
    - [Filtering](#filtering)
- [Performance](#performance)
    - [別のデータベースの使用](#using-a-different-database)
    - [Redis の取り込み](#ingest)
    - [Sampling](#sampling)
    - [Trimming](#trimming)
    - [Pulse 例外の処理](#pulse-exceptions)
- [カスタムカード](#custom-cards)
    - [カードのコンポーネント](#custom-card-components)
    - [Styling](#custom-card-styling)
    - [データのキャプチャと集約](#custom-card-data)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Pulse](https://github.com/laravel/pulse) は、アプリケーションのパフォーマンスと使用状況を一目で把握できる情報を提供します。 Pulse を使用すると、遅いジョブやエンドポイントなどのボトルネックを追跡したり、最もアクティブなユーザーを見つけたりすることができます。

個々のイベントの詳細なデバッグについては、[Laravel Telescope](/docs/{{version}}/telescope) を確認してください。

<a name="installation"></a>
## インストール (Installation)

> [!WARNING]  
> Pulse のファーストパーティ ストレージ実装には現在、MySQL、MariaDB、または PostgreSQL データベースが必要です。別のデータベース エンジンを使用している場合は、Pulse データ用に別の MySQL、MariaDB、または PostgreSQL データベースが必要になります。

Composer パッケージ マネージャーを使用して Pulse をインストールできます。

```sh
composer require laravel/pulse
```

次に、`vendor:publish` Artisan コマンドを使用して、Pulse 構成ファイルと移行ファイルを公開する必要があります。

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

最後に、`migrate` コマンドを実行して、Pulse のデータを保存するために必要なテーブルを作成する必要があります。

```shell
php artisan migrate
```

Pulse のデータベース移行が実行されると、`/pulse` ルート経由で Pulse ダッシュボードにアクセスできるようになります。

> [!NOTE]  
> Pulse データをアプリケーションのプライマリ データベースに保存したくない場合は、[専用のデータベース接続を指定する](#using-a-different-database) を実行できます。

<a name="configuration"></a>
### 構成

Pulse の構成オプションの多くは、環境変数を使用して制御できます。利用可能なオプションを確認したり、新しいレコーダーを登録したり、詳細オプションを構成したりするには、`config/pulse.php` 構成ファイルを公開します。

```sh
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
## ダッシュボード (Dashboard)

<a name="dashboard-authorization"></a>
### 認可

Pulse ダッシュボードには、`/pulse` ルート経由でアクセスできます。デフォルトでは、`local` 環境でのみこのダッシュボードにアクセスできるため、`'viewPulse'` 認証ゲートをカスタマイズして実稼働環境の認証を構成する必要があります。これは、アプリケーションの `app/Providers/AppServiceProvider.php` ファイル内で実行できます。

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
### カスタマイズ

Pulse ダッシュボード カードとレイアウトは、ダッシュボード ビューを公開することで構成できます。ダッシュボード ビューは `resources/views/vendor/pulse/dashboard.blade.php` に公開されます。

```sh
php artisan vendor:publish --tag=pulse-dashboard
```

ダッシュボードは [Livewire](https://livewire.laravel.com/) を利用しており、JavaScript アセットを再構築することなくカードとレイアウトをカスタマイズできます。

このファイル内では、`<x-pulse>` コンポーネントがダッシュボードのレンダリングを担当し、カードのグリッド レイアウトを提供します。ダッシュボードを画面の幅全体に広げたい場合は、コンポーネントに `full-width` プロパティを指定できます。

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

デフォルトでは、`<x-pulse>` コンポーネントは 12 列のグリッドを作成しますが、`cols` プロパティを使用してこれをカスタマイズできます。

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

各カードは、スペースと位置を制御するための `cols` および `rows` プロップを受け入れます。

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

ほとんどのカードは、スクロールする代わりにカード全体を表示する `expand` プロップも受け入れます。

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
### ユーザーの解決

アプリケーション使用状況カードなど、ユーザーに関する情報を表示するカードの場合、Pulse はユーザーの ID のみを記録します。ダッシュボードをレンダリングするとき、Pulse はデフォルトの `Authenticatable` モデルから `name` フィールドと `email` フィールドを解決し、Gravatar Web サービスを使用してアバターを表示します。

アプリケーションの `App\Providers\AppServiceProvider` クラス内で `Pulse::user` メソッドを呼び出すことで、フィールドとアバターをカスタマイズできます。

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
> `Laravel\Pulse\Contracts\ResolvesUsers` コントラクトを実装し、Laravel の [サービスコンテナ](/docs/{{version}}/container#binding-a-singleton) にバインドすることで、認証されたユーザーのキャプチャおよび取得方法を完全にカスタマイズできます。

<a name="dashboard-cards"></a>
### カード

<a name="servers-card"></a>
#### サーバー

`<livewire:pulse.servers />` カードには、`pulse:check` コマンドを実行しているすべてのサーバーのシステム リソース使用量が表示されます。システム リソース レポートの詳細については、[サーバーレコーダー](#servers-recorder) に関するドキュメントを参照してください。

インフラストラクチャ内のサーバーを交換する場合、一定期間後に非アクティブなサーバーの Pulse ダッシュボードへの表示を停止したい場合があります。これは、非アクティブなサーバーが Pulse ダッシュボードから削除されるまでの秒数を受け入れる `ignore-after` プロパティを使用して実現できます。あるいは、`1 hour` や `3 days and 1 hour` などの相対時間形式の文字列を指定することもできます。

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
#### アプリケーションの使用法

`<livewire:pulse.usage />` カードには、アプリケーションにリクエストを行ったり、ジョブをディスパッチしたり、リクエストの速度が遅くなったりしている上位 10 人のユーザーが表示されます。

すべての使用状況メトリクスを画面上に同時に表示したい場合は、カードを複数回含めて、`type` 属性を指定できます。

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

Pulse がユーザー情報を取得して表示する方法をカスタマイズする方法については、[ユーザーを解決する](#dashboard-resolving-users) のドキュメントを参照してください。

> [!NOTE]  
> アプリケーションが大量のリクエストを受信したり、大量のジョブをディスパッチしたりする場合は、[sampling](#sampling) を有効にすることができます。詳細については、[ユーザーがレコーダーをリクエストする](#user-requests-recorder)、[ユーザージョブレコーダー](#user-jobs-recorder)、および [スロージョブレコーダー](#slow-jobs-recorder) のドキュメントを参照してください。

<a name="exceptions-card"></a>
#### 例外

`<livewire:pulse.exceptions />` カードは、アプリケーションで発生する例外の頻度と最新性を示します。デフォルトでは、例外は例外クラスと例外が発生した場所に基づいてグループ化されます。詳細については、[例外レコーダー](#exceptions-recorder) のドキュメントを参照してください。

<a name="queues-card"></a>
#### キュー

`<livewire:pulse.queues />` カードには、キューに入れられたジョブ、処理中のジョブ、処理されたジョブ、リリースされたジョブ、失敗したジョブの数など、アプリケーションのキューのスループットが表示されます。詳細については、[キューレコーダー](#queues-recorder) のドキュメントを参照してください。

<a name="slow-requests-card"></a>
#### 遅いリクエスト

`<livewire:pulse.slow-requests />` カードは、設定されたしきい値 (デフォルトでは 1,000 ミリ秒) を超える、アプリケーションへの受信リクエストを表示します。詳細については、[スローリクエストレコーダー](#slow-requests-recorder) のドキュメントを参照してください。

<a name="slow-jobs-card"></a>
#### 遅い仕事

`<livewire:pulse.slow-jobs />` カードには、設定されたしきい値 (デフォルトでは 1,000 ミリ秒) を超える、アプリケーション内のキューに入れられたジョブが表示されます。詳細については、[スロージョブレコーダー](#slow-jobs-recorder) のドキュメントを参照してください。

<a name="slow-queries-card"></a>
#### 遅いクエリ

`<livewire:pulse.slow-queries />` カードには、設定されたしきい値 (デフォルトでは 1,000 ミリ秒) を超えるアプリケーション内のデータベース クエリが表示されます。

デフォルトでは、遅いクエリは SQL クエリ (バインドなし) とそれが発生した場所に基づいてグループ化されますが、SQL クエリのみに基づいてグループ化したい場合は、場所を取得しないことも選択できます。

構文の強調表示を受け取る非常に大規模な SQL クエリが原因でレンダリングのパフォーマンスの問題が発生した場合は、`without-highlighting` プロパティを追加して強調表示を無効にすることができます。

```blade
<livewire:pulse.slow-queries without-highlighting />
```

詳細については、[スロークエリレコーダー](#slow-queries-recorder) のドキュメントを参照してください。

<a name="slow-outgoing-requests-card"></a>
#### 送信リクエストが遅い

`<livewire:pulse.slow-outgoing-requests />` カードは、Laravel の [HTTPクライアント](/docs/{{version}}/http-client) を使用して行われた、設定されたしきい値 (デフォルトでは 1,000 ミリ秒) を超える送信リクエストを示します。

デフォルトでは、エントリは完全な URL によってグループ化されます。ただし、正規表現を使用して、同様の送信リクエストを正規化またはグループ化したい場合があります。詳細については、[遅い発信リクエストレコーダー](#slow-outgoing-requests-recorder) のドキュメントを参照してください。

<a name="cache-card"></a>
#### キャッシュ

`<livewire:pulse.cache />` カードは、アプリケーションのキャッシュ ヒットとミスの統計を、グローバルと個々のキーの両方で表示します。

デフォルトでは、エントリはキーごとにグループ化されます。ただし、正規表現を使用して類似したキーを正規化またはグループ化したい場合があります。詳細については、[キャッシュインタラクションレコーダー](#cache-interactions-recorder) のドキュメントを参照してください。

<a name="capturing-entries"></a>
## エントリのキャプチャ (Capturing Entries)

ほとんどの Pulse レコーダーは、Laravel によって送出されたフレームワーク イベントに基づいてエントリを自動的にキャプチャします。ただし、[サーバーレコーダー](#servers-recorder) および一部のサードパーティ カードは定期的に情報をポーリングする必要があります。これらのカードを使用するには、すべての個々のアプリケーション サーバーで `pulse:check` デーモンを実行する必要があります。

```php
php artisan pulse:check
```

> [!NOTE]  
> `pulse:check` プロセスをバックグラウンドで永続的に実行し続けるには、Supervisorなどのプロセス モニターを使用して、コマンドの実行が停止しないようにする必要があります。

`pulse:check` コマンドは存続期間の長いプロセスであるため、再起動しない限りコードベースへの変更は表示されません。アプリケーションのデプロイメントプロセス中に `pulse:restart` コマンドを呼び出して、コマンドを正常に再起動する必要があります。

```sh
php artisan pulse:restart
```

> [!NOTE]  
> Pulse は [cache](/docs/{{version}}/cache) を使用して再起動信号を保存するため、この機能を使用する前に、キャッシュ ドライバがアプリケーションに対して適切に構成されていることを確認する必要があります。

<a name="recorders"></a>
### レコーダー

レコーダーは、アプリケーションからエントリを取得して Pulse データベースに記録する役割を果たします。レコーダーは、[Pulse 設定ファイル](#configuration) の `recorders` セクションで登録および構成されます。

<a name="cache-interactions-recorder"></a>
#### キャッシュインタラクション

`CacheInteractions` レコーダーは、アプリケーションで発生する [cache](/docs/{{version}}/cache) のヒットとミスに関する情報をキャプチャし、[Cache](#cache-card) カードに表示します。

必要に応じて、[サンプルレート](#sampling) および無視されるキー パターンを調整できます。

同様のキーが 1 つのエントリとしてグループ化されるように、キーのグループ化を構成することもできます。たとえば、同じ種類の情報をキャッシュしているキーから一意の ID を削除したい場合があります。グループは、キーの一部を「検索して置換」するための正規表現を使用して構成されます。例は構成ファイルに含まれています。

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

最初に一致したパターンが使用されます。一致するパターンがない場合、キーはそのままキャプチャされます。

<a name="exceptions-recorder"></a>
#### 例外

`Exceptions` レコーダーは、アプリケーションで発生する報告可能な例外に関する情報をキャプチャし、[Exceptions](#exceptions-card) カードに表示します。

必要に応じて、[サンプルレート](#sampling) および無視される例外パターンを調整できます。例外の発生元の場所をキャプチャするかどうかを構成することもできます。キャプチャされた位置は Pulse ダッシュボードに表示され、例外の原因を追跡するのに役立ちます。ただし、同じ例外が複数の場所で発生する場合は、一意の場所ごとに複数回表示されます。

<a name="queues-recorder"></a>
#### キュー

`Queues` レコーダーは、[Queues](#queues-card) に表示するためにアプリケーション キューに関する情報をキャプチャします。

必要に応じて、[サンプルレート](#sampling) および無視されたジョブ パターンを調整できます。

<a name="slow-jobs-recorder"></a>
#### 遅い仕事

`SlowJobs` レコーダーは、アプリケーションで発生する遅いジョブに関する情報をキャプチャし、[遅い仕事](#slow-jobs-recorder) カードに表示します。

オプションで、低速ジョブしきい値 [サンプルレート](#sampling) および無視されるジョブ パターンを調整できます。

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

ジョブのクラス名に一致する正規表現パターンがない場合は、`'default'` 値が使用されます。

<a name="slow-outgoing-requests-recorder"></a>
#### 送信リクエストが遅い

`SlowOutgoingRequests` レコーダーは、Laravel の [HTTPクライアント](/docs/{{version}}/http-client) を使用して行われた、[送信リクエストが遅い](#slow-outgoing-requests-card) カードに表示するために構成されたしきい値を超える送信 HTTP リクエストに関する情報をキャプチャします。

オプションで、低速送信リクエストのしきい値、[サンプルレート](#sampling)、および無視される URL パターンを調整できます。

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

リクエストの URL に一致する正規表現パターンがない場合は、`'default'` 値が使用されます。

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

最初に一致したパターンが使用されます。一致するパターンがない場合、URL はそのままキャプチャされます。

<a name="slow-queries-recorder"></a>
#### 遅いクエリ

`SlowQueries` レコーダーは、[遅いクエリ](#slow-queries-card) カードに表示するために設定されたしきい値を超えるアプリケーション内のデータベース クエリをキャプチャします。

オプションで、低速クエリしきい値 [サンプルレート](#sampling) および無視されるクエリ パターンを調整できます。クエリの場所をキャプチャするかどうかを構成することもできます。キャプチャされた位置は Pulse ダッシュボードに表示され、クエリの発信元を追跡するのに役立ちます。ただし、同じクエリが複数の場所で作成された場合は、一意の場所ごとに複数回表示されます。

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

クエリの SQL に一致する正規表現パターンがない場合は、`'default'` 値が使用されます。

<a name="slow-requests-recorder"></a>
#### 遅いリクエスト

`Requests` レコーダーは、[遅いリクエスト](#slow-requests-card) カードおよび [アプリケーションの使用法](#application-usage-card) カードに表示するためにアプリケーションに対して行われたリクエストに関する情報をキャプチャします。

オプションで、低速ルートのしきい値、[サンプルレート](#sampling)、および無視されるパスを調整できます。

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

リクエストの URL に一致する正規表現パターンがない場合は、`'default'` 値が使用されます。

<a name="servers-recorder"></a>
#### サーバー

`Servers` レコーダーは、[Servers](#servers-card) カードに表示するためにアプリケーションに電力を供給するサーバーの CPU、メモリ、ストレージの使用状況をキャプチャします。このレコーダーを使用するには、監視する各サーバー上で [`pulse:check` コマンド](#capturing-entries) が実行されている必要があります。

各レポート サーバーには一意の名前が必要です。デフォルトでは、Pulse は PHP の `gethostname` 関数によって返された値を使用します。これをカスタマイズしたい場合は、`PULSE_SERVER_NAME` 環境変数を設定します。

```env
PULSE_SERVER_NAME=load-balancer
```

Pulse 構成ファイルを使用すると、監視されるディレクトリをカスタマイズすることもできます。

<a name="user-jobs-recorder"></a>
#### ユーザージョブ

`UserJobs` レコーダーは、アプリケーションでジョブをディスパッチしているユーザーに関する情報をキャプチャし、[アプリケーションの使用法](#application-usage-card) カードに表示します。

必要に応じて、[サンプルレート](#sampling) および無視されたジョブ パターンを調整できます。

<a name="user-requests-recorder"></a>
#### ユーザーのリクエスト

`UserRequests` レコーダーは、[アプリケーションの使用法](#application-usage-card) カードに表示するためにアプリケーションにリクエストを行っているユーザーに関する情報をキャプチャします。

必要に応じて、[サンプルレート](#sampling) および無視される URL パターンを調整できます。

<a name="filtering"></a>
### フィルタリング

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
## パフォーマンス (Performance)

Pulse は、追加のインフラストラクチャを必要とせずに、既存のアプリケーションに組み込めるように設計されています。ただし、トラフィックの多いアプリケーションの場合、Pulse がアプリケーションのパフォーマンスに与える影響を取り除く方法がいくつかあります。

<a name="using-a-different-database"></a>
### 別のデータベースの使用

トラフィックの多いアプリケーションの場合は、アプリケーション データベースへの影響を避けるために、Pulse 専用のデータベース接続を使用することをお勧めします。

`PULSE_DB_CONNECTION` 環境変数を設定することで、Pulse によって使用される [データベース接続](/docs/{{version}}/database#configuration) をカスタマイズできます。

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
### Redis の取り込み

> [!WARNING]  
> Redis Ingest には、Redis 6.2 以降と、アプリケーションの構成済み Redis クライアント ドライバとして `phpredis` または `predis` が必要です。

デフォルトでは、Pulse は、HTTP 応答がクライアントに送信された後、またはジョブが処理された後、エントリを [設定されたデータベース接続](#using-a-different-database) に直接保存します。ただし、代わりに Pulse の Redis インジェスト ドライバを使用して、エントリを Redis ストリームに送信することもできます。これは、`PULSE_INGEST_DRIVER` 環境変数を構成することで有効にできます。

```
PULSE_INGEST_DRIVER=redis
```

Pulse はデフォルトでデフォルトの [Redis接続](/docs/{{version}}/redis#configuration) を使用しますが、`PULSE_REDIS_CONNECTION` 環境変数を使用してこれをカスタマイズできます。

```
PULSE_REDIS_CONNECTION=pulse
```

Redis インジェストを使用する場合、`pulse:work` コマンドを実行してストリームを監視し、エントリを Redis から Pulse のデータベース テーブルに移動する必要があります。

```php
php artisan pulse:work
```

> [!NOTE]  
> `pulse:work` プロセスをバックグラウンドで永続的に実行し続けるには、Supervisorなどのプロセス モニターを使用して、Pulse ワーカーの実行が停止しないようにする必要があります。

`pulse:work` コマンドは存続期間の長いプロセスであるため、再起動しない限りコードベースへの変更は表示されません。アプリケーションのデプロイメントプロセス中に `pulse:restart` コマンドを呼び出して、コマンドを正常に再起動する必要があります。

```sh
php artisan pulse:restart
```

> [!NOTE]  
> Pulse は [cache](/docs/{{version}}/cache) を使用して再起動信号を保存するため、この機能を使用する前に、キャッシュ ドライバがアプリケーションに対して適切に構成されていることを確認する必要があります。

<a name="sampling"></a>
### サンプリング

デフォルトでは、Pulse はアプリケーションで発生するすべての関連イベントをキャプチャします。トラフィックの多いアプリケーションの場合、特に長期間にわたって、ダッシュボードに何百万ものデータベース行を集約する必要が生じる可能性があります。

代わりに、特定の Pulse データ レコーダーで「サンプリング」を有効にすることを選択できます。たとえば、[`User Requests`](#user-requests-recorder) レコーダーでサンプル レートを `0.1` に設定すると、アプリケーションへのリクエストの約 10% のみが記録されることになります。ダッシュボードでは、値がスケールアップされ、近似値であることを示すために `~` という接頭辞が付けられます。

一般に、特定のメトリクスのエントリが多いほど、精度をあまり犠牲にすることなくサンプル レートを安全に低く設定できます。

<a name="trimming"></a>
### トリミング

Pulse は、保存されているエントリがダッシュボード ウィンドウの外に出ると、自動的にトリミングします。トリミングは、Pulse [設定ファイル](#configuration) でカスタマイズできる抽選システムを使用してデータを取り込むときに発生します。

<a name="pulse-exceptions"></a>
### Pulse 例外の処理

ストレージ データベースに接続できないなど、Pulse データのキャプチャ中に例外が発生した場合、Pulse はアプリケーションへの影響を回避するためにサイレントに失敗します。

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
## カスタムカード (Custom Cards)

Pulse を使用すると、アプリケーションの特定のニーズに関連するデータを表示するカスタム カードを作成できます。 Pulse は [Livewire](https://livewire.laravel.com) を使用するため、最初のカスタム カードを作成する前に [ドキュメントを確認してください](https://livewire.laravel.com/docs) を実行することをお勧めします。

<a name="custom-card-components"></a>
### カードのコンポーネント

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

Livewire の [遅延読み込み](https://livewire.laravel.com/docs/lazy) 機能を使用する場合、`Card` コンポーネントは、コンポーネントに渡された `cols` 属性と `rows` 属性を尊重するプレースホルダーを自動的に提供します。

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

カード レイアウトをダッシュ​​ボード ビューからカスタマイズできるように、`$cols`、`$rows`、`$class`、および `$expand` 変数をそれぞれのBlade コンポーネントに渡す必要があります。カードを自動的に更新するために、ビューに `wire:poll.5s=""` 属性を含めることもできます。

Livewire コンポーネントとテンプレートを定義したら、カードを [ダッシュボードビュー](#dashboard-customization) に含めることができます。

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]  
> カードがパッケージに含まれている場合は、`Livewire::component` メソッドを使用してコンポーネントを Livewire に登録する必要があります。

<a name="custom-card-styling"></a>
### スタイリング

カードに Pulse に含まれるクラスやコンポーネント以外の追加のスタイルが必要な場合は、カードにカスタム CSS を含めるオプションがいくつかあります。

<a name="custom-card-styling-vite"></a>
#### Laravel Viteの統合

カスタム カードがアプリケーションのコード ベース内にあり、Laravel の [Viteの統合](/docs/{{version}}/vite) を使用している場合は、`vite.config.js` ファイルを更新して、カードの専用 CSS エントリ ポイントを含めることができます。

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

次に、[ダッシュボードビュー](#dashboard-customization) で `@vite` Blade ディレクティブを使用し、カードの CSS エントリポイントを指定します。

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
#### CSS ファイル

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

このカードがダッシュボードに含まれる場合、Pulse はこのファイルの内容を `<style>` タグ内に自動的に含めるため、`public` ディレクトリに公開する必要はありません。

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS を使用する場合は、不要な CSS のロードや Pulse の Tailwind クラスとの競合を避けるために、専用の Tailwind 構成ファイルを作成する必要があります。

```js
export default {
    darkMode: 'class',
    important: '#top-sellers',
    content: [
        './resources/views/livewire/pulse/top-sellers.blade.php',
    ],
    corePlugins: {
        preflight: false,
    },
};
```

次に、CSS エントリポイントで構成ファイルを指定できます。

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

また、Tailwind の [`important` セレクター戦略](https://tailwindcss.com/docs/configuration#selector-strategy) に渡されるセレクターと一致する `id` または `class` 属性をカードのビューに含める必要があります。

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
### データのキャプチャと集約

カスタム カードはどこからでもデータを取得して表示できます。ただし、Pulse の強力で効率的なデータ記録および集計システムを活用したい場合もあります。

<a name="custom-card-data-capture"></a>
#### エントリのキャプチャ

Pulse では、`Pulse::record` メソッドを使用して「エントリ」を記録できます。

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

`record` メソッドに指定される最初の引数は、記録しているエントリの `type` であり、2 番目の引数は、集計されたデータをグループ化する方法を決定する `key` です。ほとんどの集計方法では、集計対象の `value` も指定する必要があります。上の例では、集計される値は `$sale->amount` です。次に、1 つ以上の集計メソッド (`sum` など) を呼び出して、Pulse が事前に集計された値を「バケット」にキャプチャして、後で効率的に取得できるようにすることができます。

使用可能な集計方法は次のとおりです。

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]  
> 現在認証されているユーザー ID を取得するカード パッケージを構築する場合は、アプリケーションに対して作成された [ユーザーリゾルバーのカスタマイズ](#dashboard-resolving-users) を尊重する `Pulse::resolveAuthenticatedUserId()` メソッドを使用する必要があります。

<a name="custom-card-data-retrieval"></a>
#### 集計データの取得

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

`aggregate` メソッドは、PHP `stdClass` オブジェクトのコレクションを返します。各オブジェクトには、前に取得した `key` プロパティと、要求された各集計のキーが含まれます。

```
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

Pulse は主に、事前に集約されたバケットからデータを取得します。したがって、指定された集計は、`Pulse::record` メソッドを使用して事前にキャプチャされている必要があります。通常、最も古いバケットは部分的に期間外にあるため、Pulse は最も古いエントリを集計してギャップを埋め、各ポーリング リクエストで期間全体を集計する必要なく、期間全体の正確な値を提供します。

`aggregateTotal` メソッドを使用して、特定のタイプの合計値を取得することもできます。たとえば、次のメソッドは、ユーザーごとにグループ化するのではなく、すべてのユーザーの売上の合計を取得します。

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
#### ユーザーの表示

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

`find` メソッドは、`name`、`extra`、および `avatar` キーを含むオブジェクトを返します。オプションで、これらのキーを `<x-pulse::user-card>` Blade コンポーネントに直接渡すこともできます。

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
#### カスタムレコーダー

パッケージ作成者は、ユーザーがデータのキャプチャを構成できるようにレコーダー クラスを提供したい場合があります。

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

