# Laravel Telescope (Laravel Telescope)

- [Introduction](#introduction)
- [Installation](#installation)
    - [ローカルのみのインストール](#local-only-installation)
    - [Configuration](#configuration)
    - [データのプルーニング](#data-pruning)
    - [ダッシュボードの認証](#dashboard-authorization)
- [Telescopeのアップグレード](#upgrading-telescope)
- [Filtering](#filtering)
    - [Entries](#filtering-entries)
    - [Batches](#filtering-batches)
- [Tagging](#tagging)
- [利用可能なウォッチャー](#available-watchers)
    - [バッチウォッチャー](#batch-watcher)
    - [キャッシュウォッチャー](#cache-watcher)
    - [コマンドウォッチャー](#command-watcher)
    - [ダンプウォッチャー](#dump-watcher)
    - [イベントウォッチャー](#event-watcher)
    - [例外ウォッチャー](#exception-watcher)
    - [ゲートウォッチャー](#gate-watcher)
    - [HTTP クライアント ウォッチャー](#http-client-watcher)
    - [ジョブウォッチャー](#job-watcher)
    - [ログウォッチャー](#log-watcher)
    - [メールウォッチャー](#mail-watcher)
    - [モデルウォッチャー](#model-watcher)
    - [通知ウォッチャー](#notification-watcher)
    - [クエリウォッチャー](#query-watcher)
    - [Redis ウォッチャー](#redis-watcher)
    - [リクエストウォッチャー](#request-watcher)
    - [スケジュールウォッチャー](#schedule-watcher)
    - [ビューウォッチャー](#view-watcher)
- [ユーザーアバターの表示](#displaying-user-avatars)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Telescope](https://github.com/laravel/telescope) は、ローカルの Laravel 開発環境の素晴らしいパートナーになります。 Telescope は、アプリケーションに送られるリクエスト、例外、ログ エントリ、データベース クエリ、キューに入れられたジョブ、メール、通知、キャッシュ操作、スケジュールされたタスク、変数ダンプなどに関する洞察を提供します。

<img src="https://laravel.com/img/docs/telescope-example.png">

<a name="installation"></a>
## インストール (Installation)

Composer パッケージ マネージャーを使用して、Telescope を Laravel プロジェクトにインストールできます。

    composer require laravel/telescope

Telescope をインストールした後、`telescope:install` Artisan コマンドを使用してそのアセットを公開します。 Telescope をインストールした後、Telescope のデータを保存するために必要なテーブルを作成するために、`migrate` コマンドも実行する必要があります。

    php artisan telescope:install

    php artisan migrate

<a name="migration-customization"></a>
#### 移行のカスタマイズ

Telescope のデフォルトの移行を使用しない場合は、アプリケーションの `App\Providers\AppServiceProvider` クラスの `register` メソッドで `Telescope::ignoreMigrations` メソッドを呼び出す必要があります。次のコマンドを使用してデフォルトの移行をエクスポートできます: `php artisan vendor:publish --tag=telescope-migrations`

<a name="local-only-installation"></a>
### ローカルのみのインストール

ローカル開発を支援するためにのみ Telescope を使用する予定の場合は、`--dev` フラグを使用して Telescope をインストールできます。

    composer require laravel/telescope --dev

    php artisan telescope:install

    php artisan migrate

`telescope:install` を実行した後、アプリケーションの `config/app.php` 構成ファイルから `TelescopeServiceProvider` サービスプロバイダの登録を削除する必要があります。代わりに、`App\Providers\AppServiceProvider` クラスの `register` メソッドで Telescope のサービスプロバイダを手動で登録します。プロバイダを登録する前に、現在の環境が `local` であることを確認します。

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        if ($this->app->environment('local')) {
            $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
            $this->app->register(TelescopeServiceProvider::class);
        }
    }

最後に、`composer.json` ファイルに以下を追加して、Telescope パッケージが [auto-discovered](/docs/{{version}}/packages#package-discovery) になるのを防ぐ必要もあります。

    "extra": {
        "laravel": {
            "dont-discover": [
                "laravel/telescope"
            ]
        }
    },

<a name="configuration"></a>
### 構成

Telescope のアセットを公開すると、そのプライマリ構成ファイルは `config/telescope.php` に配置されます。この設定ファイルを使用すると、[ウォッチャーのオプション](#available-watchers) を設定できます。各構成オプションにはその目的の説明が含まれているため、このファイルをよく調べてください。

必要に応じて、`enabled` 構成オプションを使用して Telescope のデータ収集を完全に無効にすることができます。

    'enabled' => env('TELESCOPE_ENABLED', true),

<a name="data-pruning"></a>
### データのプルーニング

プルーニングを行わない場合、`telescope_entries` テーブルは非常に迅速にレコードを蓄積できます。これを軽減するには、[schedule](/docs/{{version}}/scheduling) `telescope:prune` Artisan コマンドを毎日実行する必要があります。

    $schedule->command('telescope:prune')->daily();

デフォルトでは、24 時間より古いエントリはすべて削除されます。コマンドを呼び出すときに `hours` オプションを使用して、Telescope データを保持する期間を決定できます。たとえば、次のコマンドは 48 時間以上前に作成されたすべてのレコードを削除します。

    $schedule->command('telescope:prune --hours=48')->daily();

<a name="dashboard-authorization"></a>
### ダッシュボードの認証

Telescope ダッシュボードには、`/telescope` ルートでアクセスできます。デフォルトでは、`local` 環境でのみこのダッシュボードにアクセスできます。 `app/Providers/TelescopeServiceProvider.php` ファイル内には、[認証ゲート](/docs/{{version}}/authorization#gates) 定義があります。この認証ゲートは、**非ローカル**環境での Telescope へのアクセスを制御します。必要に応じてこのゲートを自由に変更して、Telescope インストールへのアクセスを制限できます。

    /**
     * Register the Telescope gate.
     *
     * This gate determines who can access Telescope in non-local environments.
     *
     * @return void
     */
    protected function gate()
    {
        Gate::define('viewTelescope', function ($user) {
            return in_array($user->email, [
                'taylor@laravel.com',
            ]);
        });
    }

> {note} 運用環境では、`APP_ENV` 環境変数を `production` に必ず変更する必要があります。そうしないと、Telescope のインストールが公開されてしまいます。

<a name="upgrading-telescope"></a>
## Telescopeのアップグレード (Upgrading Telescope)

Telescope の新しいメジャー バージョンにアップグレードする場合は、[アップグレードガイド](https://github.com/laravel/telescope/blob/master/UPGRADE.md) を注意深く確認することが重要です。

さらに、新しい Telescope バージョンにアップグレードする場合は、Telescope のアセットを再公開する必要があります。

    php artisan telescope:publish

アセットを最新の状態に保ち、今後の更新での問題を回避するには、アプリケーションの `composer.json` ファイル内の `post-update-cmd` スクリプトに `telescope:publish` コマンドを追加します。

    {
        "scripts": {
            "post-update-cmd": [
                "@php artisan telescope:publish --ansi"
            ]
        }
    }

<a name="filtering"></a>
## フィルタリング (Filtering)

<a name="filtering-entries"></a>
### エントリー

Telescope によって記録されたデータは、`App\Providers\TelescopeServiceProvider` クラスで定義されている `filter` クロージャを介してフィルタリングできます。デフォルトでは、このクロージャは、`local` 環境内のすべてのデータと、他のすべての環境内の例外、失敗したジョブ、スケジュールされたタスク、および監視対象のタグを持つデータを記録します。

    use Laravel\Telescope\IncomingEntry;
    use Laravel\Telescope\Telescope;

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->hideSensitiveRequestDetails();

        Telescope::filter(function (IncomingEntry $entry) {
            if ($this->app->environment('local')) {
                return true;
            }

            return $entry->isReportableException() ||
                $entry->isFailedJob() ||
                $entry->isScheduledTask() ||
                $entry->isSlowQuery() ||
                $entry->hasMonitoredTag();
        });
    }

<a name="filtering-batches"></a>
### バッチ

`filter` クロージャは個々のエントリのデータをフィルタリングしますが、`filterBatch` メソッドを使用して、特定のリクエストまたはコンソール コマンドのすべてのデータをフィルタリングするクロージャを登録できます。クロージャが `true` を返す場合、すべてのエントリが Telescope によって記録されます。

    use Illuminate\Support\Collection;
    use Laravel\Telescope\Telescope;

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->hideSensitiveRequestDetails();

        Telescope::filterBatch(function (Collection $entries) {
            if ($this->app->environment('local')) {
                return true;
            }

            return $entries->contains(function ($entry) {
                return $entry->isReportableException() ||
                    $entry->isFailedJob() ||
                    $entry->isScheduledTask() ||
                    $entry->isSlowQuery() ||
                    $entry->hasMonitoredTag();
                });
        });
    }

<a name="tagging"></a>
## タグ付け (Tagging)

Telescope では、「タグ」によるエントリの検索が可能です。多くの場合、タグは Eloquent モデルのクラス名または認証されたユーザー ID であり、Telescope が自動的にエントリに追加します。場合によっては、エントリに独自のカスタム タグを添付したい場合があります。これを実現するには、`Telescope::tag` メソッドを使用できます。 `tag` メソッドは、タグの配列を返すクロージャを受け入れます。クロージャによって返されたタグは、Telescope が自動的にエントリに付加す​​るタグとマージされます。通常、`App\Providers\TelescopeServiceProvider` クラスの `register` メソッド内で `tag` メソッドを呼び出す必要があります。

    use Laravel\Telescope\IncomingEntry;
    use Laravel\Telescope\Telescope;

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->hideSensitiveRequestDetails();

        Telescope::tag(function (IncomingEntry $entry) {
            return $entry->type === 'request'
                        ? ['status:'.$entry->content['response_status']]
                        : [];
        });
     }

<a name="available-watchers"></a>
## 利用可能なウォッチャー (Available Watchers)

Telescopeの「ウォッチャー」は、リクエストまたはコンソール コマンドが実行されるときにアプリケーション データを収集します。 `config/telescope.php` 構成ファイル内で有効にするウォッチャーのリストをカスタマイズできます。

    'watchers' => [
        Watchers\CacheWatcher::class => true,
        Watchers\CommandWatcher::class => true,
        ...
    ],

一部のウォッチャーでは、追加のカスタマイズ オプションを提供することもできます。

    'watchers' => [
        Watchers\QueryWatcher::class => [
            'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
            'slow' => 100,
        ],
        ...
    ],

<a name="batch-watcher"></a>
### バッチウォッチャー

バッチ ウォッチャーは、ジョブや接続情報など、キューに入れられた [batches](/docs/{{version}}/queues#job-batching) に関する情報を記録します。

<a name="cache-watcher"></a>
### キャッシュウォッチャー

キャッシュ ウォッチャーは、キャッシュ キーがヒットしたとき、ミスしたとき、更新されたとき、忘れられたときにデータを記録します。

<a name="command-watcher"></a>
### コマンドウォッチャー

コマンド ウォッチャーは、Artisan コマンドが実行されるたびに、引数、オプション、終了コード、および出力を記録します。ウォッチャーによる記録から特定のコマンドを除外したい場合は、`config/telescope.php` ファイル内の `ignore` オプションでコマンドを指定できます。

    'watchers' => [
        Watchers\CommandWatcher::class => [
            'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
            'ignore' => ['key:generate'],
        ],
        ...
    ],

<a name="dump-watcher"></a>
### ダンプウォッチャー

ダンプ ウォッチャーは、変数ダンプを記録し、Telescope に表示します。 Laravel を使用する場合、グローバル `dump` 関数を使用して変数をダンプすることができます。ダンプを記録するには、ブラウザでダンプ ウォッチャー タブが開かれている必要があります。そうしないと、ダンプはウォッチャーによって無視されます。

<a name="event-watcher"></a>
### イベントウォッチャー

イベント ウォッチャーは、アプリケーションによってディスパッチされた [events](/docs/{{version}}/events) のペイロード、リスナ、およびブロードキャスト データを記録します。 Laravel フレームワークの内部イベントは、イベント ウォッチャーによって無視されます。

<a name="exception-watcher"></a>
### 例外ウォッチャー

例外ウォッチャーは、アプリケーションによってスローされた報告可能な例外のデータとスタック トレースを記録します。

<a name="gate-watcher"></a>
### ゲートウォッチャー

ゲート ウォッチャーは、アプリケーションによる [ゲートとポリシー](/docs/{{version}}/authorization) チェックのデータと結果を記録します。ウォッチャーによる記録から特定の能力を除外したい場合は、`config/telescope.php` ファイルの `ignore_abilities` オプションでそれらを指定できます。

    'watchers' => [
        Watchers\GateWatcher::class => [
            'enabled' => env('TELESCOPE_GATE_WATCHER', true),
            'ignore_abilities' => ['viewNova'],
        ],
        ...
    ],

<a name="http-client-watcher"></a>
### HTTP クライアント ウォッチャー

HTTP クライアント ウォッチャーは、アプリケーションによって作成された送信 [HTTPクライアントリクエスト](/docs/{{version}}/http-client) を記録します。

<a name="job-watcher"></a>
### ジョブウォッチャー

ジョブ ウォッチャーは、アプリケーションによってディスパッチされた [jobs](/docs/{{version}}/queues) のデータとステータスを記録します。

<a name="log-watcher"></a>
### ログウォッチャー

ログ ウォッチャーは、アプリケーションによって書き込まれたログの [ログデータ](/docs/{{version}}/logging) を記録します。

<a name="mail-watcher"></a>
### メールウォッチャー

メール ウォッチャーを使用すると、アプリケーションによって送信された [emails](/docs/{{version}}/mail) とその関連データのブラウザー内プレビューを表示できます。電子メールを `.eml` ファイルとしてダウンロードすることもできます。

<a name="model-watcher"></a>
### モデルウォッチャー

モデル ウォッチャーは、Eloquent [モデルイベント](/docs/{{version}}/eloquent#events) がディスパッチされるたびに、モデルの変更を記録します。ウォッチャーの `events` オプションを使用して、どのモデル イベントを記録するかを指定できます。

    'watchers' => [
        Watchers\ModelWatcher::class => [
            'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
            'events' => ['eloquent.created*', 'eloquent.updated*'],
        ],
        ...
    ],

特定のリクエスト中にハイドレートされたモデルの数を記録したい場合は、`hydrations` オプションを有効にします。

    'watchers' => [
        Watchers\ModelWatcher::class => [
            'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
            'events' => ['eloquent.created*', 'eloquent.updated*'],
            'hydrations' => true,
        ],
        ...
    ],

<a name="notification-watcher"></a>
### 通知ウォッチャー

通知ウォッチャーは、アプリケーションによって送信されたすべての [notifications](/docs/{{version}}/notifications) を記録します。通知によって電子メールが送信され、メール ウォッチャーが有効になっている場合、その電子メールはメール ウォッチャー画面でプレビューすることもできます。

<a name="query-watcher"></a>
### クエリウォッチャー

クエリ ウォッチャーは、アプリケーションによって実行されるすべてのクエリの生の SQL、バインディング、および実行時間を記録します。また、ウォッチャーは、100 ミリ秒未満のクエリに `slow` としてタグ付けします。ウォッチャーの `slow` オプションを使用して、低速クエリのしきい値をカスタマイズできます。

    'watchers' => [
        Watchers\QueryWatcher::class => [
            'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
            'slow' => 50,
        ],
        ...
    ],

<a name="redis-watcher"></a>
### Redis ウォッチャー

Redis ウォッチャーは、アプリケーションによって実行されたすべての [Redis](/docs/{{version}}/redis) コマンドを記録します。キャッシュに Redis を使用している場合、キャッシュ コマンドも Redis ウォッチャーによって記録されます。

<a name="request-watcher"></a>
### リクエストウォッチャー

リクエスト ウォッチャーは、アプリケーションによって処理されるリクエストに関連付けられたリクエスト、ヘッダー、セッション、および応答データを記録します。 `size_limit` (キロバイト単位) オプションを使用して、記録された応答データを制限できます。

    'watchers' => [
        Watchers\RequestWatcher::class => [
            'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
            'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
        ],
        ...
    ],

<a name="schedule-watcher"></a>
### スケジュールウォッチャー

スケジュール ウォッチャーは、アプリケーションによって実行される [スケジュールされたタスク](/docs/{{version}}/scheduling) のコマンドと出力を記録します。

<a name="view-watcher"></a>
### ビューウォッチャー

ビュー ウォッチャーは、ビューのレンダリング時に使用される [view](/docs/{{version}}/views) 名、パス、データ、および「コンポーザー」を記録します。

<a name="displaying-user-avatars"></a>
## ユーザーアバターの表示 (Displaying User Avatars)

Telescope ダッシュボードには、特定のエントリが保存されたときに認証されたユーザーのユーザー アバターが表示されます。デフォルトでは、Telescope は Gravatar Web サービスを使用してアバターを取得します。ただし、`App\Providers\TelescopeServiceProvider` クラスにコールバックを登録することで、アバター URL をカスタマイズできます。コールバックはユーザーの ID と電子メール アドレスを受け取り、ユーザーのアバター画像 URL を返す必要があります。

    use App\Models\User;
    use Laravel\Telescope\Telescope;

    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        // ...

        Telescope::avatar(function ($id, $email) {
            return '/avatars/'.User::find($id)->avatar_path;
        });
    }

