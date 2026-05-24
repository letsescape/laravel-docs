# Laravel Horizon (Laravel Horizon)

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [戦略のバランスを取る](#balancing-strategies)
    - [ダッシュボードの認証](#dashboard-authorization)
    - [サイレントジョブ](#silenced-jobs)
- [Horizon のアップグレード](#upgrading-horizon)
- [ランニングホライゾン](#running-horizon)
    - [Horizon の導入](#deploying-horizon)
- [Tags](#tags)
- [Notifications](#notifications)
- [Metrics](#metrics)
- [失敗したジョブの削除](#deleting-failed-jobs)
- [キューからジョブをクリアする](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 導入 (Introduction)

> [!NOTE]  
> Laravel Horizon について詳しく知る前に、Laravel のベース [キューサービス](/docs/{{version}}/queues) についてよく理解しておく必要があります。 Horizon は、Laravel が提供する基本的なキュー機能にまだ慣れていない場合、混乱を招く可能性がある追加機能で Laravel のキューを強化します。

[Laravel Horizon](https://github.com/laravel/horizon) は、Laravel を利用した [Redisキュー](/docs/{{version}}/queues) に美しいダッシュボードとコード駆動の構成を提供します。 Horizon を使用すると、ジョブのスループット、実行時間、ジョブの失敗など、キュー システムの主要なメトリクスを簡単に監視できます。

Horizon を使用する場合、すべてのキューワーカー構成は 1 つの単純な構成ファイルに保存されます。バージョン管理されたファイルでアプリケーションのワーカー構成を定義すると、アプリケーションのデプロイ時にアプリケーションのキューワーカーを簡単に拡張または変更できます。

<img src="https://laravel.com/img/docs/horizon-example.png">

<a name="installation"></a>
## インストール (Installation)

> [!WARNING]  
> Laravel Horizon では、キューに電力を供給するために [Redis](https://redis.io) を使用する必要があります。したがって、アプリケーションの `config/queue.php` 構成ファイルでキュー接続が `redis` に設定されていることを確認する必要があります。

Composer パッケージ マネージャーを使用して、Horizon をプロジェクトにインストールできます。

```shell
composer require laravel/horizon
```

Horizon をインストールした後、`horizon:install` Artisan コマンドを使用してアセットを公開します。

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 構成

Horizon のアセットを公開すると、そのプライマリ構成ファイルは `config/horizon.php` に配置されます。この構成ファイルを使用すると、アプリケーションのキューワーカー オプションを構成できます。各構成オプションにはその目的の説明が含まれているため、このファイルをよく調べてください。

> [!WARNING]  
> Horizon は内部で `horizon` という名前の Redis 接続を使用します。この Redis 接続名は予約されており、`database.php` 構成ファイル内の別の Redis 接続に割り当てたり、`horizon.php` 構成ファイル内の `use` オプションの値として割り当てたりしないでください。

<a name="environments"></a>
#### 環境

インストール後、よく理解しておく必要がある主な Horizon 構成オプションは、`environments` 構成オプションです。この構成オプションは、アプリケーションが実行される環境の配列であり、各環境のワーカー プロセス オプションを定義します。デフォルトでは、このエントリには `production` および `local` 環境が含まれます。ただし、必要に応じて環境を自由に追加できます。

    'environments' => [
        'production' => [
            'supervisor-1' => [
                'maxProcesses' => 10,
                'balanceMaxShift' => 1,
                'balanceCooldown' => 3,
            ],
        ],

        'local' => [
            'supervisor-1' => [
                'maxProcesses' => 3,
            ],
        ],
    ],

Horizon を起動すると、アプリケーションが実行されている環境のワーカー プロセス構成オプションが使用されます。通常、環境は `APP_ENV` [環境変数](/docs/{{version}}/configuration#determining-the-current-environment) の値によって決まります。たとえば、デフォルトの `local` Horizon 環境は、3 つのワーカー プロセスを開始し、各キューに割り当てられたワーカー プロセスの数のバランスを自動的に調整するように構成されています。デフォルトの `production` 環境は、最大 10 個のワーカー プロセスを開始し、各キューに割り当てられるワーカー プロセスの数のバランスを自動的に調整するように構成されています。

> [!WARNING]  
> `horizon` 構成ファイルの `environments` 部分に、Horizon を実行する予定の各 [environment](/docs/{{version}}/configuration#environment-configuration) のエントリが含まれていることを確認する必要があります。

<a name="supervisors"></a>
#### 監督者

Horizon のデフォルト構成ファイルからわかるように、各環境には 1 つ以上の「スーパーバイザ」を含めることができます。デフォルトでは、構成ファイルはこのスーパーバイザを `supervisor-1` として定義します。ただし、Supervisorの名前は自由に付けることができます。各スーパーバイザは基本的に、ワーカー プロセスのグループを「監視」する責任を負い、キュー間でワーカー プロセスのバランスをとります。

特定の環境で実行するワーカー プロセスの新しいグループを定義したい場合は、その環境にスーパーバイザを追加できます。アプリケーションで使用される特定のキューに対して別のバランシング戦略またはワーカー プロセス数を定義したい場合は、これを行うことを選択できます。

<a name="maintenance-mode"></a>
#### メンテナンスモード

アプリケーションが [メンテナンスモード](/docs/{{version}}/configuration#maintenance-mode) にある間は、Horizon 構成ファイル内でスーパーバイザの `force` オプションが `true` として定義されていない限り、キューに入れられたジョブは Horizon によって処理されません。

    'environments' => [
        'production' => [
            'supervisor-1' => [
                // ...
                'force' => true,
            ],
        ],
    ],

<a name="default-values"></a>
#### デフォルト値

Horizon のデフォルト構成ファイル内に、`defaults` 構成オプションがあることがわかります。この構成オプションは、アプリケーションの [supervisors](#supervisors) のデフォルト値を指定します。スーパーバイザのデフォルト設定値は、各環境のスーパーバイザの設定にマージされるため、スーパーバイザを定義する際に不必要な繰り返しを避けることができます。

<a name="balancing-strategies"></a>
### 戦略のバランスを取る

Laravel のデフォルトのキュー システムとは異なり、Horizon では、`simple`、`auto`、`false` の 3 つのワーカー バランシング戦略から選択できます。 `simple` 戦略は、受信ジョブをワーカー プロセス間で均等に分割します。

    'balance' => 'simple',

構成ファイルのデフォルトである `auto` 戦略は、キューの現在のワークロードに基づいてキューごとのワーカー プロセスの数を調整します。たとえば、`notifications` キューに 1,000 個の保留中のジョブがあり、`render` キューが空の場合、Horizon はキューが空になるまでより多くのワーカーを `notifications` キューに割り当てます。

`auto` 戦略を使用する場合、`minProcesses` および `maxProcesses` 構成オプションを定義して、Horizon がスケールアップおよびスケールダウンするワーカー プロセスの最小数と最大数を制御できます。

    'environments' => [
        'production' => [
            'supervisor-1' => [
                'connection' => 'redis',
                'queue' => ['default'],
                'balance' => 'auto',
                'autoScalingStrategy' => 'time',
                'minProcesses' => 1,
                'maxProcesses' => 10,
                'balanceMaxShift' => 1,
                'balanceCooldown' => 3,
                'tries' => 3,
            ],
        ],
    ],

`autoScalingStrategy` 構成値は、キューをクリアするのにかかる合計時間 (`time` 戦略) に基づいて、またはキュー上のジョブの総数 (`size` 戦略) に基づいて、Horizon がより多くのワーカー プロセスをキューに割り当てるかを決定します。

`balanceMaxShift` および `balanceCooldown` の構成値は、ワーカーの需要を満たすために Horizon がどの程度の速度でスケールするかを決定します。上の例では、3 秒ごとに最大 1 つの新しいプロセスが作成または破棄されます。アプリケーションのニーズに基づいて、必要に応じてこれらの値を自由に調整できます。

`balance` オプションが `false` に設定されている場合、デフォルトの Laravel 動作が使用され、キューは設定にリストされている順序で処理されます。

<a name="dashboard-authorization"></a>
### ダッシュボードの認証

Horizon ダッシュボードには、`/horizon` ルート経由でアクセスできます。デフォルトでは、`local` 環境でのみこのダッシュボードにアクセスできます。ただし、`app/Providers/HorizonServiceProvider.php` ファイル内には、[認証ゲート](/docs/{{version}}/authorization#gates) 定義があります。この認証ゲートは、**非ローカル**環境での Horizon へのアクセスを制御します。 Horizon インストールへのアクセスを制限するために、必要に応じてこのゲートを自由に変更できます。

    /**
     * Register the Horizon gate.
     *
     * This gate determines who can access Horizon in non-local environments.
     */
    protected function gate(): void
    {
        Gate::define('viewHorizon', function (User $user) {
            return in_array($user->email, [
                'taylor@laravel.com',
            ]);
        });
    }

<a name="alternative-authentication-strategies"></a>
#### 代替の認証戦略

Laravel は認証されたユーザーをゲート クロージャに自動的に挿入することに注意してください。アプリケーションが IP 制限などの別の方法で Horizon セキュリティを提供している場合、Horizon ユーザーは「ログイン」する必要がない場合があります。したがって、Laravel に認証を要求しないようにするには、上記の `function (User $user)` クロージャー署名を `function (User $user = null)` に変更する必要があります。

<a name="silenced-jobs"></a>
### サイレントジョブ

場合によっては、アプリケーションまたはサードパーティのパッケージによってディスパッチされた特定のジョブを表示することに興味がない場合があります。これらのジョブが「完了したジョブ」リストのスペースを占める代わりに、それらのジョブを沈黙させることができます。まず、ジョブのクラス名をアプリケーションの `horizon` 構成ファイルの `silenced` 構成オプションに追加します。

    'silenced' => [
        App\Jobs\ProcessPodcast::class,
    ],

あるいは、沈黙させたいジョブは、`Laravel\Horizon\Contracts\Silenced` インターフェイスを実装できます。ジョブがこのインターフェイスを実装している場合、それが `silenced` 構成配列に存在しない場合でも、ジョブは自動的にサイレント化されます。

    use Laravel\Horizon\Contracts\Silenced;

    class ProcessPodcast implements ShouldQueue, Silenced
    {
        use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

        // ...
    }

<a name="upgrading-horizon"></a>
## Horizon のアップグレード (Upgrading Horizon)

Horizon の新しいメジャー バージョンにアップグレードする場合は、[アップグレードガイド](https://github.com/laravel/horizon/blob/master/UPGRADE.md) を注意深く確認することが重要です。さらに、新しい Horizon バージョンにアップグレードする場合は、Horizon のアセットを再公開する必要があります。

```shell
php artisan horizon:publish
```

アセットを最新の状態に保ち、今後の更新での問題を回避するには、アプリケーションの `composer.json` ファイル内の `post-update-cmd` スクリプトに `vendor:publish --tag=laravel-assets` コマンドを追加します。

```json
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ]
    }
}
```

<a name="running-horizon"></a>
## ランニングホライゾン (Running Horizon)

アプリケーションの `config/horizon.php` 構成ファイルでSupervisorとワーカーを構成したら、`horizon` Artisan コマンドを使用して Horizon を起動できます。この 1 つのコマンドは、現在の環境で構成されているすべてのワーカー プロセスを開始します。

```shell
php artisan horizon
```

Horizon プロセスを一時停止し、`horizon:pause` および `horizon:continue` Artisan コマンドを使用してジョブの処理を続行するように指示できます。

```shell
php artisan horizon:pause

php artisan horizon:continue
```

`horizon:pause-supervisor` および `horizon:continue-supervisor` Artisan コマンドを使用して、特定の Horizon [supervisors](#supervisors) を一時停止および続行することもできます。

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

`horizon:status` Artisan コマンドを使用して、Horizon プロセスの現在のステータスを確認できます。

```shell
php artisan horizon:status
```

`horizon:terminate` Artisan コマンドを使用して、Horizon プロセスを正常に終了できます。現在 によって処理されているジョブはすべて完了し、Horizon は実行を停止します。

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
### Horizon の導入

Horizon をアプリケーションの実際のサーバーにデプロイする準備ができたら、`php artisan horizon` コマンドを監視し、予期せず終了した場合にコマンドを再起動するようにプロセス モニターを構成する必要があります。心配しないでください。プロセス モニターのインストール方法については以下で説明します。

アプリケーションのデプロイ プロセス中に、Horizon プロセスがプロセス モニターによって再起動され、コードの変更を受信できるように、プロセスを終了するように指示する必要があります。

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### スーパーバイザのインス​​トール

Supervisorは、Linux オペレーティング システムのプロセス モニターであり、`horizon` プロセスが実行を停止した場合に自動的に再起動します。 Ubuntu に Supervisor をインストールするには、次のコマンドを使用できます。 Ubuntu を使用していない場合は、オペレーティング システムのパッケージ マネージャーを使用して Supervisor をインストールできる可能性があります。

```shell
sudo apt-get install supervisor
```

> [!NOTE]  
> Supervisor を自分で設定するのが面倒に思える場合は、Laravel プロジェクト用に Supervisor を自動的にインストールして設定する [Laravel Forge](https://forge.laravel.com) の使用を検討してください。

<a name="supervisor-configuration"></a>
#### スーパーバイザの構成

スーパーバイザ設定ファイルは通常、サーバーの `/etc/supervisor/conf.d` ディレクトリ内に保存されます。このディレクトリ内に、スーパーバイザにプロセスの監視方法を指示する構成ファイルをいくつでも作成できます。たとえば、`horizon` プロセスを開始して監視する `horizon.conf` ファイルを作成してみましょう。

```ini
[program:horizon]
process_name=%(program_name)s
command=php /home/forge/example.com/artisan horizon
autostart=true
autorestart=true
user=forge
redirect_stderr=true
stdout_logfile=/home/forge/example.com/horizon.log
stopwaitsecs=3600
```

Supervisor構成を定義するときは、`stopwaitsecs` の値が、最も長く実行されているジョブで消費される秒数よりも大きいことを確認する必要があります。そうしないと、Supervisorがジョブの処理が完了する前にジョブを強制終了する可能性があります。

> [!WARNING]  
> 上記の例は Ubuntu ベースのサーバに有効ですが、スーパーバイザ設定ファイルに予期される場所とファイル拡張子は、他のサーバ オペレーティング システムでは異なる場合があります。詳細については、サーバーのドキュメントを参照してください。

<a name="starting-supervisor"></a>
#### スーパーバイザの開始

設定ファイルが作成されたら、次のコマンドを使用してスーパーバイザ設定を更新し、監視対象プロセスを開始できます。

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]  
> スーパーバイザの実行の詳細については、[Supervisorの文書](http://supervisord.org/index.html) を参照してください。

<a name="tags"></a>
## タグ (Tags)

Horizon では、メール可能ファイル、ブロードキャスト イベント、通知、キューに入れられたイベント リスナなどのジョブに「タグ」を割り当てることができます。実際、Horizon は、ジョブにアタッチされている Eloquent モデルに応じて、ほとんどのジョブにインテリジェントかつ自動的にタグ付けします。たとえば、次のジョブを見てください。

    <?php

    namespace App\Jobs;

    use App\Models\Video;
    use Illuminate\Bus\Queueable;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Foundation\Bus\Dispatchable;
    use Illuminate\Queue\InteractsWithQueue;
    use Illuminate\Queue\SerializesModels;

    class RenderVideo implements ShouldQueue
    {
        use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

        /**
         * Create a new job instance.
         */
        public function __construct(
            public Video $video,
        ) {}

        /**
         * Execute the job.
         */
        public function handle(): void
        {
            // ...
        }
    }

このジョブが、`1` の `id` 属性を持つ `App\Models\Video` インスタンスとともにキューに入れられた場合、自動的にタグ `App\Models\Video:1` を受け取ります。これは、Horizon がジョブのプロパティで Eloquent モデルを検索するためです。 Eloquent モデルが見つかった場合、Horizon はモデルのクラス名と主キーを使用してジョブにインテリジェントにタグ付けします。

    use App\Jobs\RenderVideo;
    use App\Models\Video;

    $video = Video::find(1);

    RenderVideo::dispatch($video);

<a name="manually-tagging-jobs"></a>
#### ジョブの手動タグ付け

キュー可能オブジェクトのいずれかのタグを手動で定義したい場合は、クラスに `tags` メソッドを定義できます。

    class RenderVideo implements ShouldQueue
    {
        /**
         * Get the tags that should be assigned to the job.
         *
         * @return array<int, string>
         */
        public function tags(): array
        {
            return ['render', 'video:'.$this->video->id];
        }
    }

<a name="manually-tagging-event-listeners"></a>
#### イベントリスナの手動タグ付け

キューに入れられたイベント リスナのタグを取得するとき、Horizon は自動的にイベント インスタンスを `tags` メソッドに渡し、イベント データをタグに追加できるようにします。

    class SendRenderNotifications implements ShouldQueue
    {
        /**
         * Get the tags that should be assigned to the listener.
         *
         * @return array<int, string>
         */
        public function tags(VideoRendered $event): array
        {
            return ['video:'.$event->video->id];
        }
    }


<a name="notifications"></a>
## 通知 (Notifications)

> [!WARNING]  
> Slack または SMS 通知を送信するように Horizon を構成する場合は、[関連する通知チャネルの前提条件](/docs/{{version}}/notifications) を確認する必要があります。

キューの 1 つで長い待ち時間が発生したときに通知を受け取りたい場合は、`Horizon::routeMailNotificationsTo`、`Horizon::routeSlackNotificationsTo`、および `Horizon::routeSmsNotificationsTo` メソッドを使用できます。これらのメソッドは、アプリケーションの `App\Providers\HorizonServiceProvider` の `boot` メソッドから呼び出すことができます。

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        parent::boot();

        Horizon::routeSmsNotificationsTo('15556667777');
        Horizon::routeMailNotificationsTo('example@example.com');
        Horizon::routeSlackNotificationsTo('slack-webhook-url', '#channel');
    }

<a name="configuring-notification-wait-time-thresholds"></a>
#### 通知待機時間のしきい値の構成

アプリケーションの `config/horizon.php` 構成ファイル内で、「長い待機」とみなされる秒数を構成できます。このファイル内の `waits` 構成オプションを使用すると、接続とキューの組み合わせごとに長時間待機のしきい値を制御できます。未定義の接続/キューの組み合わせは、デフォルトで 60 秒の長時間待機しきい値に設定されます。

    'waits' => [
        'redis:critical' => 30,
        'redis:default' => 60,
        'redis:batch' => 120,
    ],

<a name="metrics"></a>
## メトリクス (Metrics)

Horizon には、ジョブとキューの待機時間とスループットに関する情報を提供するメトリクス ダッシュボードが含まれています。このダッシュボードにデータを入力するには、アプリケーションの [scheduler](/docs/{{version}}/scheduling) 経由で Horizon の `snapshot` Artisan コマンドを 5 分ごとに実行するように構成する必要があります。

    /**
     * Define the application's command schedule.
     */
    protected function schedule(Schedule $schedule): void
    {
        $schedule->command('horizon:snapshot')->everyFiveMinutes();
    }

<a name="deleting-failed-jobs"></a>
## 失敗したジョブの削除 (Deleting Failed Jobs)

失敗したジョブを削除したい場合は、`horizon:forget` コマンドを使用できます。 `horizon:forget` コマンドは、失敗したジョブの ID または UUID を唯一の引数として受け入れます。

```shell
php artisan horizon:forget 5
```

<a name="clearing-jobs-from-queues"></a>
## キューからジョブをクリアする (Clearing Jobs From Queues)

アプリケーションのデフォルト キューからすべてのジョブを削除したい場合は、`horizon:clear` Artisan コマンドを使用して削除できます。

```shell
php artisan horizon:clear
```

`queue` オプションを指定して、特定のキューからジョブを削除できます。

```shell
php artisan horizon:clear --queue=emails
```

