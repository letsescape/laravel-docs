# リリースノート (Release Notes)

- [バージョン管理スキーム](#versioning-scheme)
    - [Exceptions](#exceptions)
- [サポートポリシー](#support-policy)
- [Laravel8](#laravel-8)

<a name="versioning-scheme"></a>
## バージョン管理スキーム (Versioning Scheme)

Laravel とその他のファーストパーティ パッケージは [セマンティック バージョニング](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~2 月) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^8.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="exceptions"></a>
### 例外

<a name="named-arguments"></a>
#### 名前付き引数

現時点では、PHP の [名前付き引数](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) 機能は、Laravel の下位互換性ガイドラインの対象になっていません。 Laravel コードベースを改善するために、必要に応じて関数パラメータの名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
## サポートポリシー (Support Policy)

すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。 Lumen を含むすべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [Laravelによってサポートされています](/docs/{{version}}/database#introduction) を確認してください。

| バージョン | PHP(*) | リリース | バグ修正まで | セキュリティ修正の期限 |
| --- | --- | --- | --- | --- |
| 6 (LTS) | 7.2～8.0 | 2019年9月3日 | 2022 年 1 月 25 日 | 2022 年 9 月 6 日 |
| 7 | 7.2～8.0 | 2020年3月3日 | 2020年10月6日 | 2021年3月3日 |
| 8 | 7.3 - 8.1 | 2020年9月8日 | 2022 年 7 月 26 日 | 2023 年 1 月 24 日 |
| 9 | 8.0～8.1 | 2022 年 2 月 8 日 | 2023 年 8 月 8 日 | 2024 年 2 月 6 日 |
| 10 | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日 | 2025 年 2 月 4 日 |

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>

(*) サポートされている PHP バージョン

<a name="laravel-8"></a>
## Laravel8 (Laravel 8)

Laravel 8では、Laravel Jetstream、モデルファクトリークラス、マイグレーションスカッシング、ジョブバッチング、レート制限の改善、キューの改善、動的なBladeコンポーネント、Tailwindページネーションビュー、タイムテストヘルパ、`artisan serve`の改善、イベントリスナの改善、その他さまざまなバグ修正とユーザビリティの改善を導入することにより、Laravel 7.xで行われた改善を継続しています。

<a name="laravel-jetstream"></a>
### Laravel Jetstream

_Laravel Jetstream は [テイラー・オトウェル](https://github.com/taylorotwell)_ によって作成されました。

[Laravel Jetstream](https://jetstream.laravel.com) は、Laravel 用に美しく設計されたアプリケーション スキャフォールディングです。 Jetstream は次のプロジェクトの完璧な出発点を提供し、ログイン、登録、電子メール検証、二要素認証、セッション管理、Laravel Sanctum による API サポート、およびオプションのチーム管理が含まれています。 Laravel Jetstream は、Laravel の以前のバージョンで利用可能な従来の認証 UI スキャフォールディングを置き換え、改良しました。

Jetstream は [Tailwind CSS](https://tailwindcss.com) を使用して設計されており、[Livewire](https://laravel-livewire.com) または [Inertia](https://inertiajs.com) スキャフォールディングの選択を提供します。

<a name="models-directory"></a>
### モデルディレクトリ

コミュニティの圧倒的な需要により、デフォルトの Laravel アプリケーション スケルトンには `app/Models` ディレクトリが含まれるようになりました。 Eloquent モデルのこの新しい家を楽しんでいただければ幸いです。関連するすべてのジェネレーター コマンドが更新され、`app/Models` ディレクトリーが存在する場合、そのディレクトリー内にモデルが存在すると想定されます。ディレクトリが存在しない場合、フレームワークはモデルが `app` ディレクトリ内に配置されるべきであると想定します。

<a name="model-factory-classes"></a>
### モデルファクトリークラス

_モデル ファクトリ クラスは [テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

Eloquent [モデル工場](/docs/{{version}}/database-testing#defining-model-factories) はクラスベースのファクトリーとして完全に書き直され、ファーストクラスのリレーションシップをサポートするように改良されました。たとえば、Laravel に含まれる `UserFactory` は次のように記述されます。

    <?php

    namespace Database\Factories;

    use App\Models\User;
    use Illuminate\Database\Eloquent\Factories\Factory;
    use Illuminate\Support\Str;

    class UserFactory extends Factory
    {
        /**
         * The name of the factory's corresponding model.
         *
         * @var string
         */
        protected $model = User::class;

        /**
         * Define the model's default state.
         *
         * @return array
         */
        public function definition()
        {
            return [
                'name' => $this->faker->name(),
                'email' => $this->faker->unique()->safeEmail(),
                'email_verified_at' => now(),
                'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
                'remember_token' => Str::random(10),
            ];
        }
    }

生成されたモデルで利用できる新しい `HasFactory` トレイトのおかげで、モデル ファクトリは次のように使用できます。

    use App\Models\User;

    User::factory()->count(50)->create();

モデル ファクトリは単純な PHP クラスになっているため、状態変換はクラス メソッドとして記述できます。さらに、必要に応じて、他のヘルパ クラスを Eloquent モデル ファクトリに追加することもできます。

たとえば、`User` モデルには、デフォルトの属性値の 1 つを変更する `suspended` 状態がある可能性があります。ベース ファクトリの `state` メソッドを使用して状態変換を定義できます。状態メソッドには好きな名前を付けることができます。結局のところ、これは典型的な PHP メソッドにすぎません。

    /**
     * Indicate that the user is suspended.
     *
     * @return \Illuminate\Database\Eloquent\Factories\Factory
     */
    public function suspended()
    {
        return $this->state([
            'account_status' => 'suspended',
        ]);
    }

状態変換メソッドを定義した後、それを次のように使用できます。

    use App\Models\User;

    User::factory()->count(5)->suspended()->create();

前述したように、Laravel 8 のモデルファクトリーには、リレーションシップに対する第一級のサポートが含まれています。したがって、`User` モデルに `posts` 関係メソッドがあると仮定すると、次のコードを実行するだけで、3 つの投稿を持つユーザーを生成できます。

    $users = User::factory()
                ->hasPosts(3, [
                    'published' => false,
                ])
                ->create();

アップグレードプロセスを容易にするために、Laravel 8.x 内のモデルファクトリーの以前のイテレーションのサポートを提供する [laravel/legacy-factories](https://github.com/laravel/legacy-factories) パッケージがリリースされました。

Laravel の書き直されたファクトリーには、きっと気に入っていただけると思われる機能がさらに多く含まれています。モデルファクトリーの詳細については、[データベーステストのドキュメント](/docs/{{version}}/database-testing#defining-model-factories) を参照してください。

<a name="migration-squashing"></a>
### 移行の潰し

_移行スカッシュは [テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

アプリケーションを構築すると、時間の経過とともにさらに多くの移行が蓄積される可能性があります。これにより、移行ディレクトリが数百もの移行によって肥大化する可能性があります。 MySQL または PostgreSQL を使用している場合は、移行を単一の SQL ファイルに「圧縮」できるようになりました。まず、`schema:dump` コマンドを実行します。

    php artisan schema:dump

    // Dump the current database schema and prune all existing migrations...
    php artisan schema:dump --prune

このコマンドを実行すると、Laravel は「スキーマ」ファイルを `database/schema` ディレクトリに書き込みます。ここで、他の移行が実行されていないときにデータベースを移行しようとすると、Laravel は最初にスキーマ ファイルの SQL を実行します。スキーマファイルのコマンドを実行した後、Laravel はスキーマダンプの一部ではなかった残りの移行を実行します。

<a name="job-batching"></a>
### ジョブのバッチ処理

_ジョブのバッチ処理は、[テイラー・オトウェル](https://github.com/taylorotwell) および [モハメド・サイード](https://github.com/themsaid)_ によって提供されました。

Laravel のジョブバッチ機能を使用すると、ジョブのバッチを簡単に実行し、ジョブのバッチの実行が完了したときに何らかのアクションを実行できます。

`Bus` ファサードの新しい `batch` メソッドを使用して、ジョブのバッチをディスパッチできます。もちろん、バッチ処理は主に完了コールバックと組み合わせると便利です。したがって、`then`、`catch`、および `finally` メソッドを使用して、バッチの完了コールバックを定義できます。これらの各コールバックは、呼び出されるときに `Illuminate\Bus\Batch` インスタンスを受け取ります。

    use App\Jobs\ProcessPodcast;
    use App\Models\Podcast;
    use Illuminate\Bus\Batch;
    use Illuminate\Support\Facades\Bus;
    use Throwable;

    $batch = Bus::batch([
        new ProcessPodcast(Podcast::find(1)),
        new ProcessPodcast(Podcast::find(2)),
        new ProcessPodcast(Podcast::find(3)),
        new ProcessPodcast(Podcast::find(4)),
        new ProcessPodcast(Podcast::find(5)),
    ])->then(function (Batch $batch) {
        // All jobs completed successfully...
    })->catch(function (Batch $batch, Throwable $e) {
        // First batch job failure detected...
    })->finally(function (Batch $batch) {
        // The batch has finished executing...
    })->dispatch();

    return $batch->id;

ジョブのバッチ処理の詳細については、[キューのドキュメント](/docs/{{version}}/queues#job-batching) を参照してください。

<a name="improved-rate-limiting"></a>
### レート制限の改善

_レート制限の改善は、[テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

Laravel のリクエスト レート リミッター機能は、以前のリリースの `throttle` ミドルウェア API との下位互換性を維持しながら、より柔軟かつ強力に強化されました。

レート リミッターは、`RateLimiter` ファサードの `for` メソッドを使用して定義されます。 `for` メソッドは、レート リミッター名と、このレート リミッターが割り当てられたルートに適用される制限設定を返すクロージャを受け入れます。

    use Illuminate\Cache\RateLimiting\Limit;
    use Illuminate\Support\Facades\RateLimiter;

    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });

レート リミッター コールバックは受信 HTTP リクエスト インスタンスを受け取るため、受信リクエストまたは認証されたユーザーに基づいて適切なレート制限を動的に構築できます。

    RateLimiter::for('uploads', function (Request $request) {
        return $request->user()->vipCustomer()
                    ? Limit::none()
                    : Limit::perMinute(100);
    });

場合によっては、レート制限を任意の値で分割したい場合があります。たとえば、ユーザーが IP アドレスごとに 1 分あたり 100 回、特定のルートにアクセスできるようにしたい場合があります。これを実現するには、レート制限を構築するときに `by` メソッドを使用します。

    RateLimiter::for('uploads', function (Request $request) {
        return $request->user()->vipCustomer()
                    ? Limit::none()
                    : Limit::perMinute(100)->by($request->ip());
    });

レート リミッターは、`throttle` [middleware](/docs/{{version}}/middleware) を使用してルートまたはルート グループに接続できます。スロットル ミドルウェアは、ルートに割り当てるレート リミッターの名前を受け入れます。

    Route::middleware(['throttle:uploads'])->group(function () {
        Route::post('/audio', function () {
            //
        });

        Route::post('/video', function () {
            //
        });
    });

レート制限の詳細については、[ルーティングのドキュメント](/docs/{{version}}/routing#rate-limiting) を参照してください。

<a name="improved-maintenance-mode"></a>
### 改善されたメンテナンスモード

_メンテナンス モードの改善は、[Spatie](https://github.com/taylorotwell)_ からのインスピレーションを得て、[テイラー・オトウェル](https://spatie.be) によって提供されました。

Laravel の以前のリリースでは、アプリケーションへのアクセスが許可された IP アドレスの「許可リスト」を使用して、`php artisan down` メンテナンス モード機能がバイパスされる可能性がありました。この機能は、よりシンプルな「シークレット」/トークン ソリューションを採用するために削除されました。

メンテナンス モードでは、`secret` オプションを使用してメンテナンス モード バイパス トークンを指定できます。

    php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"

アプリケーションをメンテナンス モードにした後、このトークンに一致するアプリケーション URL に移動すると、Laravel はブラウザにメンテナンス モード バイパス Cookie を発行します。

    https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515

この非表示のルートにアクセスすると、アプリケーションの `/` ルートにリダイレクトされます。ブラウザに Cookie が発行されると、メンテナンス モードでないかのようにアプリケーションを通常どおり閲覧できるようになります。

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### メンテナンス モード ビューのプリレンダリング

デプロイメント中に `php artisan down` コマンドを使用する場合でも、Composer の依存関係または他のインフラストラクチャ コンポーネントの更新中にユーザーがアプリケーションにアクセスすると、エラーが発生することがあります。これは、アプリケーションがメンテナンス モードであることを判断し、テンプレート エンジンを使用してメンテナンス モード ビューをレンダリングするために、Laravel フレームワークの重要な部分を起動する必要があるために発生します。

このため、Laravel では、リクエスト サイクルの最初に返されるメンテナンス モード ビューを事前レンダリングできるようになりました。このビューは、アプリケーションの依存関係が読み込まれる前にレンダリングされます。 `down` コマンドの `render` オプションを使用して、選択したテンプレートを事前レンダリングできます。

    php artisan down --render="errors::503"

<a name="closure-dispatch-chain-catch"></a>
### クロージャディスパッチ/チェーン `catch`

_Catch の改善は、[モハメド・サイード](https://github.com/themsaid)_ によって提供されました。

新しい `catch` メソッドを使用して、キューに設定された再試行をすべて使い果たした後にキューに入れられたクロージャが正常に完了しなかった場合に実行されるクロージャを提供できるようになりました。

    use Throwable;

    dispatch(function () use ($podcast) {
        $podcast->publish();
    })->catch(function (Throwable $e) {
        // This job has failed...
    });

<a name="dynamic-blade-components"></a>
### ダイナミックBlade コンポーネント

_Dynamic Blade コンポーネントは、[テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

コンポーネントをレンダリングする必要があるが、実行時までどのコンポーネントをレンダリングすべきかわからない場合があります。この状況では、Laravel の組み込み `dynamic-component` コンポーネントを使用して、実行時の値または変数に基づいてコンポーネントをレンダリングできるようになりました。

    <x-dynamic-component :component="$componentName" class="mt-4" />

Blade コンポーネントの詳細については、[Bladeのドキュメント](/docs/{{version}}/blade#components) を参照してください。

<a name="event-listener-improvements"></a>
### イベントリスナの改善

_イベント リスナの改善は、[テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

クロージャ ベースのイベント リスナは、クロージャを `Event::listen` メソッドに渡すだけで登録できるようになりました。 Laravel はクロージャを検査して、リスナがどのタイプのイベントを処理するかを判断します。

    use App\Events\PodcastProcessed;
    use Illuminate\Support\Facades\Event;

    Event::listen(function (PodcastProcessed $event) {
        //
    });

さらに、`Illuminate\Events\queueable` 関数を使用して、クロージャ ベースのイベント リスナをキュー可能としてマークできるようになりました。

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;

    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    }));

キューに入れられたジョブと同様に、`onConnection`、`onQueue`、および `delay` メソッドを使用して、キューに入れられたリスナの実行をカスタマイズできます。

    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    })->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));

匿名のキューに入れられたリスナの失敗を処理したい場合は、`queueable` リスナを定義するときに、`catch` メソッドにクロージャーを提供できます。

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;
    use Throwable;

    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    })->catch(function (PodcastProcessed $event, Throwable $e) {
        // The queued listener failed...
    }));

<a name="time-testing-helpers"></a>
### タイムテストヘルパ

_時間テスト ヘルパは、Ruby on Rails からインスピレーションを得て、[テイラー・オトウェル](https://github.com/taylorotwell) によって提供されました_。

テスト時に、`now` や `Illuminate\Support\Carbon::now()` などのヘルパによって返される時間を変更する必要がある場合があります。 Laravel の基本機能テスト クラスには、現在時刻を操作できるヘルパが含まれています。

    public function testTimeCanBeManipulated()
    {
        // Travel into the future...
        $this->travel(5)->milliseconds();
        $this->travel(5)->seconds();
        $this->travel(5)->minutes();
        $this->travel(5)->hours();
        $this->travel(5)->days();
        $this->travel(5)->weeks();
        $this->travel(5)->years();

        // Travel into the past...
        $this->travel(-5)->hours();

        // Travel to an explicit time...
        $this->travelTo(now()->subHours(6));

        // Return back to the present time...
        $this->travelBack();
    }

<a name="artisan-serve-improvements"></a>
### Artisan `serve` の改善

_Artisan `serve` の改善は、[テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

Artisan `serve` コマンドは、ローカル `.env` ファイル内で環境変数の変更が検出された場合に自動リロードされるように改善されました。以前は、コマンドを手動で停止して再起動する必要がありました。

<a name="tailwind-pagination-views"></a>
### Tailwind ページネーション ビュー

Laravel ページネータは、デフォルトで [Tailwind CSS](https://tailwindcss.com) フレームワークを使用するように更新されました。 Tailwind CSS は高度にカスタマイズ可能な低レベル CSS フレームワークで、オーバーライドするために苦労する煩わしい独自のスタイルを必要とせずに、オーダーメイドのデザインを構築するために必要なすべての構成要素を提供します。もちろん、Bootstrap 3 および 4 のビューも引き続き利用できます。

<a name="routing-namespace-updates"></a>
### ルーティング名前空間の更新

Laravel の以前のリリースでは、`RouteServiceProvider` には `$namespace` プロパティが含まれていました。このプロパティの値は、コントローラのルート定義に自動的にプレフィックスとして付けられ、`action` ヘルパ / `URL::action` メソッドを呼び出します。 Laravel 8.x では、このプロパティはデフォルトで `null` です。これは、Laravel によって名前空間のプレフィックスが自動的に付加されないことを意味します。したがって、新しい Laravel 8.x アプリケーションでは、標準の PHP 呼び出し可能構文を使用してコントローラのルート定義を定義する必要があります。

    use App\Http\Controllers\UserController;

    Route::get('/users', [UserController::class, 'index']);

`action` 関連メソッドの呼び出しでは、同じ呼び出し可能な構文を使用する必要があります。

    action([UserController::class, 'index']);

    return Redirect::action([UserController::class, 'index']);

Laravel 7.x スタイルのコントローラルートプレフィックスを使用したい場合は、アプリケーションの `RouteServiceProvider` に `$namespace` プロパティを追加するだけです。

> {note} この変更は、新しい Laravel 8.x アプリケーションにのみ影響します。 Laravel 7.x からアップグレードするアプリケーションには、`RouteServiceProvider` に `$namespace` プロパティが引き続き含まれます。

