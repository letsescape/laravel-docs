<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
    - [Exceptions](#exceptions)
- [Support Policy](#support-policy)
- [Laravel 8](#laravel-8)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~February), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel とその他のファーストパーティ パッケージは [Semantic Versioning](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~2 月) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^8.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^8.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="exceptions"></a>
<!-- ### Exceptions -->
### Exceptions

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- At this time, PHP's [named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) functionality are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function parameters when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
現時点では、PHP の [named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) 機能は、Laravel の下位互換性ガイドラインの対象になっていません。 Laravel コードベースを改善するために、必要に応じて関数パラメータの名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, including Lumen, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/8.x/database#introduction). -->
すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。 Lumen を含むすべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [supported by Laravel](/docs/8.x/database#introduction) を確認してください。

| バージョン | PHP(*) | リリース | バグ修正まで | セキュリティ修正の期限 |
| --- | --- | --- | --- | --- |
| 6 (LTS) | 7.2～8.0 | 2019年9月3日 | 2022 年 1 月 25 日 | 2022 年 9 月 6 日 |
| 7 | 7.2～8.0 | 2020年3月3日 | 2020年10月6日 | 2021年3月3日 |
| 8 | 7.3 - 8.1 | 2020年9月8日 | 2022 年 7 月 26 日 | 2023 年 1 月 24 日 |
| 9 | 8.0～8.1 | 2022 年 2 月 8 日 | 2023 年 8 月 8 日 | 2024 年 2 月 6 日 |
| 10 | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日 | 2025 年 2 月 4 日 |

<!--
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
-->
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

<!-- (*) Supported PHP versions -->
(*) サポートされている PHP バージョン

<a name="laravel-8"></a>
<!-- ## Laravel 8 -->
## Laravel 8

<!-- Laravel 8 continues the improvements made in Laravel 7.x by introducing Laravel Jetstream, model factory classes, migration squashing, job batching, improved rate limiting, queue improvements, dynamic Blade components, Tailwind pagination views, time testing helpers, improvements to `artisan serve`, event listener improvements, and a variety of other bug fixes and usability improvements. -->
Laravel 8では、Laravel Jetstream、モデルファクトリークラス、マイグレーションスカッシング、ジョブバッチング、レート制限の改善、キューの改善、動的なBladeコンポーネント、Tailwindページネーションビュー、タイムテストヘルパ、`artisan serve`の改善、イベントリスナの改善、その他さまざまなバグ修正とユーザビリティの改善を導入することにより、Laravel 7.xで行われた改善を継続しています。

<a name="laravel-jetstream"></a>
<!-- ### Laravel Jetstream -->
### Laravel Jetstream

<!-- _Laravel Jetstream was written by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_Laravel Jetstream は [Taylor Otwell](https://github.com/taylorotwell)_ によって作成されました。

<!-- [Laravel Jetstream](https://jetstream.laravel.com) is a beautifully designed application scaffolding for Laravel. Jetstream provides the perfect starting point for your next project and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Laravel Jetstream replaces and improves upon the legacy authentication UI scaffolding available for previous versions of Laravel. -->
[Laravel Jetstream](https://jetstream.laravel.com) は、Laravel 用に美しく設計されたアプリケーション スキャフォールディングです。 Jetstream は次のプロジェクトの完璧な出発点を提供し、ログイン、登録、電子メール検証、二要素認証、セッション管理、Laravel Sanctum による API サポート、およびオプションのチーム管理が含まれています。 Laravel Jetstream は、Laravel の以前のバージョンで利用可能な従来の認証 UI スキャフォールディングを置き換え、改良しました。

<!-- Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://laravel-livewire.com) or [Inertia](https://inertiajs.com) scaffolding. -->
Jetstream は [Tailwind CSS](https://tailwindcss.com) を使用して設計されており、[Livewire](https://laravel-livewire.com) または [Inertia](https://inertiajs.com) スキャフォールディングの選択を提供します。

<a name="models-directory"></a>
<!-- ### Models Directory -->
### Models Directory

<!-- By overwhelming community demand, the default Laravel application skeleton now contains an `app/Models` directory. We hope you enjoy this new home for your Eloquent models! All relevant generator commands have been updated to assume models exist within the `app/Models` directory if it exists. If the directory does not exist, the framework will assume your models should be placed within the `app` directory. -->
コミュニティの圧倒的な需要により、デフォルトの Laravel アプリケーション スケルトンには `app/Models` ディレクトリが含まれるようになりました。 Eloquent モデルのこの新しい家を楽しんでいただければ幸いです。関連するすべてのジェネレーター コマンドが更新され、`app/Models` ディレクトリーが存在する場合、そのディレクトリー内にモデルが存在すると想定されます。ディレクトリが存在しない場合、フレームワークはモデルが `app` ディレクトリ内に配置されるべきであると想定します。

<a name="model-factory-classes"></a>
<!-- ### Model Factory Classes -->
### Model Factory Classes

<!-- _Model factory classes were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_モデル ファクトリ クラスは [Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- Eloquent [model factories](/docs/8.x/database-testing#defining-model-factories) have been entirely re-written as class based factories and improved to have first-class relationship support. For example, the `UserFactory` included with Laravel is written like so: -->
Eloquent [model factories](/docs/8.x/database-testing#defining-model-factories) はクラスベースのファクトリーとして完全に書き直され、ファーストクラスのリレーションシップをサポートするように改良されました。たとえば、Laravel に含まれる `UserFactory` は次のように記述されます。

```
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
```

<!-- Thanks to the new `HasFactory` trait available on generated models, the model factory may be used like so: -->
生成されたモデルで利用できる新しい `HasFactory` トレイトのおかげで、モデル ファクトリは次のように使用できます。

```
use App\Models\User;

User::factory()->count(50)->create();
```

<!-- Since model factories are now simple PHP classes, state transformations may be written as class methods. In addition, you may add any other helper classes to your Eloquent model factory as needed. -->
モデル ファクトリは単純な PHP クラスになっているため、状態変換はクラス メソッドとして記述できます。さらに、必要に応じて、他のヘルパ クラスを Eloquent モデル ファクトリに追加することもできます。

<!-- For example, your `User` model might have a `suspended` state that modifies one of its default attribute values. You may define your state transformations using the base factory's `state` method. You may name your state method anything you like. After all, it's just a typical PHP method: -->
たとえば、`User` モデルには、デフォルトの属性値の 1 つを変更する `suspended` 状態がある可能性があります。ベース ファクトリの `state` メソッドを使用して状態変換を定義できます。状態メソッドには好きな名前を付けることができます。結局のところ、これは典型的な PHP メソッドにすぎません。

```
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
```

<!-- After defining the state transformation method, we may use it like so: -->
状態変換メソッドを定義した後、それを次のように使用できます。

```
use App\Models\User;

User::factory()->count(5)->suspended()->create();
```

<!-- As mentioned, Laravel 8's model factories contain first class support for relationships. So, assuming our `User` model has a `posts` relationship method, we may simply run the following code to generate a user with three posts: -->
前述したように、Laravel 8 のモデルファクトリーには、リレーションシップに対する第一級のサポートが含まれています。したがって、`User` モデルに `posts` 関係メソッドがあると仮定すると、次のコードを実行するだけで、3 つの投稿を持つユーザーを生成できます。

```
$users = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

<!-- To ease the upgrade process, the [laravel/legacy-factories](https://github.com/laravel/legacy-factories) package has been released to provide support for the previous iteration of model factories within Laravel 8.x. -->
アップグレードプロセスを容易にするために、Laravel 8.x 内のモデルファクトリーの以前のイテレーションのサポートを提供する [laravel/legacy-factories](https://github.com/laravel/legacy-factories) パッケージがリリースされました。

<!-- Laravel's re-written factories contain many more features that we think you will love. To learn more about model factories, please consult the [database testing documentation](/docs/8.x/database-testing#defining-model-factories). -->
Laravel の書き直されたファクトリーには、きっと気に入っていただけると思われる機能がさらに多く含まれています。モデルファクトリーの詳細については、[database testing documentation](/docs/8.x/database-testing#defining-model-factories) を参照してください。

<a name="migration-squashing"></a>
<!-- ### Migration Squashing -->
### Migration Squashing

<!-- _Migration squashing was contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_移行スカッシュは [Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- As you build your application, you may accumulate more and more migrations over time. This can lead to your migration directory becoming bloated with potentially hundreds of migrations. If you're using MySQL or PostgreSQL, you may now "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command: -->
アプリケーションを構築すると、時間の経過とともにさらに多くの移行が蓄積される可能性があります。これにより、移行ディレクトリが数百もの移行によって肥大化する可能性があります。 MySQL または PostgreSQL を使用している場合は、移行を単一の SQL ファイルに「圧縮」できるようになりました。まず、`schema:dump` コマンドを実行します。

```
php artisan schema:dump

// Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

<!-- When you execute this command, Laravel will write a "schema" file to your `database/schema` directory. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will execute the schema file's SQL first. After executing the schema file's commands, Laravel will execute any remaining migrations that were not part of the schema dump. -->
このコマンドを実行すると、Laravel は「スキーマ」ファイルを `database/schema` ディレクトリに書き込みます。ここで、他の移行が実行されていないときにデータベースを移行しようとすると、Laravel は最初にスキーマ ファイルの SQL を実行します。スキーマファイルのコマンドを実行した後、Laravel はスキーマダンプの一部ではなかった残りの移行を実行します。

<a name="job-batching"></a>
<!-- ### Job Batching -->
### Job Batching

<!-- _Job batching was contributed by [Taylor Otwell](https://github.com/taylorotwell) & [Mohamed Said](https://github.com/themsaid)_. -->
_ジョブのバッチ処理は、[Taylor Otwell](https://github.com/taylorotwell) および [Mohamed Said](https://github.com/themsaid)_ によって提供されました。

<!-- Laravel's job batching feature allows you to easily execute a batch of jobs and then perform some action when the batch of jobs has completed executing. -->
Laravel のジョブバッチ機能を使用すると、ジョブのバッチを簡単に実行し、ジョブのバッチの実行が完了したときに何らかのアクションを実行できます。

<!-- The new `batch` method of the `Bus` facade may be used to dispatch a batch of jobs. Of course, batching is primarily useful when combined with completion callbacks. So, you may use the `then`, `catch`, and `finally` methods to define completion callbacks for the batch. Each of these callbacks will receive an `Illuminate\Bus\Batch` instance when they are invoked: -->
`Bus` ファサードの新しい `batch` メソッドを使用して、ジョブのバッチをディスパッチできます。もちろん、バッチ処理は主に完了コールバックと組み合わせると便利です。したがって、`then`、`catch`、および `finally` メソッドを使用して、バッチの完了コールバックを定義できます。これらの各コールバックは、呼び出されるときに `Illuminate\Bus\Batch` インスタンスを受け取ります。

```
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
```

<!-- To learn more about job batching, please consult the [queue documentation](/docs/8.x/queues#job-batching). -->
ジョブのバッチ処理の詳細については、[queue documentation](/docs/8.x/queues#job-batching) を参照してください。

<a name="improved-rate-limiting"></a>
<!-- ### Improved Rate Limiting -->
### Improved Rate Limiting

<!-- _Rate limiting improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_レート制限の改善は、[Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- Laravel's request rate limiter feature has been augmented with more flexibility and power, while still maintaining backwards compatibility with previous release's `throttle` middleware API. -->
Laravel のリクエスト レート リミッター機能は、以前のリリースの `throttle` ミドルウェア API との下位互換性を維持しながら、より柔軟かつ強力に強化されました。

<!-- Rate limiters are defined using the `RateLimiter` facade's `for` method. The `for` method accepts a rate limiter name and a closure that returns the limit configuration that should apply to routes that are assigned this rate limiter: -->
レート リミッターは、`RateLimiter` ファサードの `for` メソッドを使用して定義されます。 `for` メソッドは、レート リミッター名と、このレート リミッターが割り当てられたルートに適用される制限設定を返すクロージャを受け入れます。

```
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000);
});
```

<!-- Since rate limiter callbacks receive the incoming HTTP request instance, you may build the appropriate rate limit dynamically based on the incoming request or authenticated user: -->
レート リミッター コールバックは受信 HTTP リクエスト インスタンスを受け取るため、受信リクエストまたは認証されたユーザーに基づいて適切なレート制限を動的に構築できます。

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

<!-- Sometimes you may wish to segment rate limits by some arbitrary value. For example, you may wish to allow users to access a given route 100 times per minute per IP address. To accomplish this, you may use the `by` method when building your rate limit: -->
場合によっては、レート制限を任意の値で分割したい場合があります。たとえば、ユーザーが IP アドレスごとに 1 分あたり 100 回、特定のルートにアクセスできるようにしたい場合があります。これを実現するには、レート制限を構築するときに `by` メソッドを使用します。

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

<!-- Rate limiters may be attached to routes or route groups using the `throttle` [middleware](/docs/8.x/middleware). The throttle middleware accepts the name of the rate limiter you wish to assign to the route: -->
レート リミッターは、`throttle` [middleware](/docs/8.x/middleware) を使用してルートまたはルート グループに接続できます。スロットル ミドルウェアは、ルートに割り当てるレート リミッターの名前を受け入れます。

```
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        //
    });

    Route::post('/video', function () {
        //
    });
});
```

<!-- To learn more about rate limiting, please consult the [routing documentation](/docs/8.x/routing#rate-limiting). -->
レート制限の詳細については、[routing documentation](/docs/8.x/routing#rate-limiting) を参照してください。

<a name="improved-maintenance-mode"></a>
<!-- ### Improved Maintenance Mode -->
### Improved Maintenance Mode

<!-- _Maintenance mode improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell) with inspiration from [Spatie](https://spatie.be)_. -->
_メンテナンス モードの改善は、[Taylor Otwell](https://github.com/taylorotwell)_ からのインスピレーションを得て、[Spatie](https://spatie.be) によって提供されました。

<!-- In previous releases of Laravel, the `php artisan down` maintenance mode feature may be bypassed using an "allow list" of IP addresses that were allowed to access the application. This feature has been removed in favor of a simpler "secret" / token solution. -->
Laravel の以前のリリースでは、アプリケーションへのアクセスが許可された IP アドレスの「許可リスト」を使用して、`php artisan down` メンテナンス モード機能がバイパスされる可能性がありました。この機能は、よりシンプルな「シークレット」/トークン ソリューションを採用するために削除されました。

<!-- While in maintenance mode, you may use the `secret` option to specify a maintenance mode bypass token: -->
メンテナンス モードでは、`secret` オプションを使用してメンテナンス モード バイパス トークンを指定できます。

```
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

<!-- After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser: -->
アプリケーションをメンテナンス モードにした後、このトークンに一致するアプリケーション URL に移動すると、Laravel はブラウザにメンテナンス モード バイパス Cookie を発行します。

<!--     https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515 -->
    https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515

<!-- When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode. -->
この非表示のルートにアクセスすると、アプリケーションの `/` ルートにリダイレクトされます。ブラウザに Cookie が発行されると、メンテナンス モードでないかのようにアプリケーションを通常どおり閲覧できるようになります。

<a name="pre-rendering-the-maintenance-mode-view"></a>
<!-- #### Pre-Rendering The Maintenance Mode View -->
#### Pre-Rendering The Maintenance Mode View

<!-- If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine. -->
デプロイメント中に `php artisan down` コマンドを使用する場合でも、Composer の依存関係または他のインフラストラクチャ コンポーネントの更新中にユーザーがアプリケーションにアクセスすると、エラーが発生することがあります。これは、アプリケーションがメンテナンス モードであることを判断し、テンプレート エンジンを使用してメンテナンス モード ビューをレンダリングするために、Laravel フレームワークの重要な部分を起動する必要があるために発生します。

<!-- For this reason, Laravel now allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option: -->
このため、Laravel では、リクエスト サイクルの最初に返されるメンテナンス モード ビューを事前レンダリングできるようになりました。このビューは、アプリケーションの依存関係が読み込まれる前にレンダリングされます。 `down` コマンドの `render` オプションを使用して、選択したテンプレートを事前レンダリングできます。

```
php artisan down --render="errors::503"
```

<a name="closure-dispatch-chain-catch"></a>
<!-- ### Closure Dispatch / Chain `catch` -->
### Closure Dispatch / Chain `catch`

<!-- _Catch improvements were contributed by [Mohamed Said](https://github.com/themsaid)_. -->
_Catch の改善は、[Mohamed Said](https://github.com/themsaid)_ によって提供されました。

<!-- Using the new `catch` method, you may now provide a closure that should be executed if a queued closure fails to complete successfully after exhausting all of your queue's configured retry attempts: -->
新しい `catch` メソッドを使用して、キューに設定された再試行をすべて使い果たした後にキューに入れられたクロージャが正常に完了しなかった場合に実行されるクロージャを提供できるようになりました。

```
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // This job has failed...
});
```

<a name="dynamic-blade-components"></a>
<!-- ### Dynamic Blade Components -->
### Dynamic Blade Components

<!-- _Dynamic Blade components were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_Dynamic Blade コンポーネントは、[Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- Sometimes you may need to render a component but not know which component should be rendered until runtime. In this situation, you may now use Laravel's built-in `dynamic-component` component to render the component based on a runtime value or variable: -->
コンポーネントをレンダリングする必要があるが、実行時までどのコンポーネントをレンダリングすべきかわからない場合があります。この状況では、Laravel の組み込み `dynamic-component` コンポーネントを使用して、実行時の値または変数に基づいてコンポーネントをレンダリングできるようになりました。

```
<x-dynamic-component :component="$componentName" class="mt-4" />
```

<!-- To learn more about Blade components, please consult the [Blade documentation](/docs/8.x/blade#components). -->
Blade コンポーネントの詳細については、[Blade documentation](/docs/8.x/blade#components) を参照してください。

<a name="event-listener-improvements"></a>
<!-- ### Event Listener Improvements -->
### Event Listener Improvements

<!-- _Event listener improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_イベント リスナの改善は、[Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- Closure based event listeners may now be registered by only passing the closure to the `Event::listen` method. Laravel will inspect the closure to determine which type of event the listener handles: -->
クロージャ ベースのイベント リスナは、クロージャを `Event::listen` メソッドに渡すだけで登録できるようになりました。 Laravel はクロージャを検査して、リスナがどのタイプのイベントを処理するかを判断します。

```
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

Event::listen(function (PodcastProcessed $event) {
    //
});
```

<!-- In addition, closure based event listeners may now be marked as queueable using the `Illuminate\Events\queueable` function: -->
さらに、`Illuminate\Events\queueable` 関数を使用して、クロージャ ベースのイベント リスナをキュー可能としてマークできるようになりました。

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
}));
```

<!-- Like queued jobs, you may use the `onConnection`, `onQueue`, and `delay` methods to customize the execution of the queued listener: -->
キューに入れられたジョブと同様に、`onConnection`、`onQueue`、および `delay` メソッドを使用して、キューに入れられたリスナの実行をカスタマイズできます。

```
Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

<!-- If you would like to handle anonymous queued listener failures, you may provide a closure to the `catch` method while defining the `queueable` listener: -->
匿名のキューに入れられたリスナの失敗を処理したい場合は、`queueable` リスナを定義するときに、`catch` メソッドにクロージャーを提供できます。

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // The queued listener failed...
}));
```

<a name="time-testing-helpers"></a>
<!-- ### Time Testing Helpers -->
### Time Testing Helpers

<!-- _Time testing helpers were contributed by [Taylor Otwell](https://github.com/taylorotwell) with inspiration from Ruby on Rails_. -->
_時間テスト ヘルパは、Ruby on Rails からインスピレーションを得て、[Taylor Otwell](https://github.com/taylorotwell) によって提供されました_。

<!-- When testing, you may occasionally need to modify the time returned by helpers such as `now` or `Illuminate\Support\Carbon::now()`. Laravel's base feature test class now includes helpers that allow you to manipulate the current time: -->
テスト時に、`now` や `Illuminate\Support\Carbon::now()` などのヘルパによって返される時間を変更する必要がある場合があります。 Laravel の基本機能テスト クラスには、現在時刻を操作できるヘルパが含まれています。

```
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
```

<a name="artisan-serve-improvements"></a>
<!-- ### Artisan `serve` Improvements -->
### Artisan `serve` Improvements

<!-- _Artisan `serve` improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_Artisan `serve` の改善は、[Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- The Artisan `serve` command has been improved with automatic reloading when environment variable changes are detected within your local `.env` file. Previously, the command had to be manually stopped and restarted. -->
Artisan `serve` コマンドは、ローカル `.env` ファイル内で環境変数の変更が検出された場合に自動リロードされるように改善されました。以前は、コマンドを手動で停止して再起動する必要がありました。

<a name="tailwind-pagination-views"></a>
<!-- ### Tailwind Pagination Views -->
### Tailwind Pagination Views

<!-- The Laravel paginator has been updated to use the [Tailwind CSS](https://tailwindcss.com) framework by default. Tailwind CSS is a highly customizable, low-level CSS framework that gives you all of the building blocks you need to build bespoke designs without any annoying opinionated styles you have to fight to override. Of course, Bootstrap 3 and 4 views remain available as well. -->
Laravel ページネータは、デフォルトで [Tailwind CSS](https://tailwindcss.com) フレームワークを使用するように更新されました。 Tailwind CSS は高度にカスタマイズ可能な低レベル CSS フレームワークで、オーバーライドするために苦労する煩わしい独自のスタイルを必要とせずに、オーダーメイドのデザインを構築するために必要なすべての構成要素を提供します。もちろん、Bootstrap 3 および 4 のビューも引き続き利用できます。

<a name="routing-namespace-updates"></a>
<!-- ### Routing Namespace Updates -->
### Routing Namespace Updates

<!-- In previous releases of Laravel, the `RouteServiceProvider` contained a `$namespace` property. This property's value would automatically be prefixed onto controller route definitions and calls to the `action` helper / `URL::action` method. In Laravel 8.x, this property is `null` by default. This means that no automatic namespace prefixing will be done by Laravel. Therefore, in new Laravel 8.x applications, controller route definitions should be defined using standard PHP callable syntax: -->
Laravel の以前のリリースでは、`RouteServiceProvider` には `$namespace` プロパティが含まれていました。このプロパティの値は、コントローラのルート定義に自動的にプレフィックスとして付けられ、`action` ヘルパ / `URL::action` メソッドを呼び出します。 Laravel 8.x では、このプロパティはデフォルトで `null` です。これは、Laravel によって名前空間のプレフィックスが自動的に付加されないことを意味します。したがって、新しい Laravel 8.x アプリケーションでは、標準の PHP 呼び出し可能構文を使用してコントローラのルート定義を定義する必要があります。

```
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);
```

<!-- Calls to the `action` related methods should use the same callable syntax: -->
`action` 関連メソッドの呼び出しでは、同じ呼び出し可能な構文を使用する必要があります。

```
action([UserController::class, 'index']);

return Redirect::action([UserController::class, 'index']);
```

<!-- If you prefer Laravel 7.x style controller route prefixing, you may simply add the `$namespace` property into your application's `RouteServiceProvider`. -->
Laravel 7.x スタイルのコントローラルートプレフィックスを使用したい場合は、アプリケーションの `RouteServiceProvider` に `$namespace` プロパティを追加するだけです。

> [!NOTE]
> この変更は、新しい Laravel 8.x アプリケーションにのみ影響します。 Laravel 7.x からアップグレードするアプリケーションには、`RouteServiceProvider` に `$namespace` プロパティが引き続き含まれます。

