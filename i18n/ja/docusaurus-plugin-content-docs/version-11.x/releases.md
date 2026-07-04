<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 11](#laravel-11)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~Q1), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel とその他のファーストパーティ パッケージは [Semantic Versioning](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~第 1 四半期) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^11.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^11.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- [Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) は、Laravel の下位互換性ガイドラインではカバーされていません。 Laravel コードベースを改善するために、必要に応じて関数の引数の名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, including Lumen, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/11.x/database#introduction). -->
すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。 Lumen を含むすべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [supported by Laravel](/docs/11.x/database#introduction) を確認してください。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| バージョン | PHP(*) | リリース | バグ修正まで | セキュリティ修正の期限 |
| --- | --- | --- | --- | --- |
| 9 | 8.0～8.2 | 2022 年 2 月 8 日 | 2023 年 8 月 8 日 | 2024 年 2 月 6 日 |
| 10 | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日 | 2025 年 2 月 4 日 |
| 11 | 8.2～8.4 | 2024 年 3 月 12 日 | 2025 年 9 月 3 日 | 2026 年 3 月 12 日 |
| 12 | 8.2～8.4 | 2025 年 2 月 24 日 | 2026 年 8 月 13 日 | 2027 年 2 月 24 日 |

<!-- </div> -->
</div>

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

<a name="laravel-11"></a>
<!-- ## Laravel 11 -->
## Laravel 11

<!-- Laravel 11 continues the improvements made in Laravel 10.x by introducing a streamlined application structure, per-second rate limiting, health routing, graceful encryption key rotation, queue testing improvements, [Resend](https://resend.com) mail transport, Prompt validator integration, new Artisan commands, and more. In addition, Laravel Reverb, a first-party, scalable WebSocket server has been introduced to provide robust real-time capabilities to your applications. -->
Laravel 11は、合理化されたアプリケーション構造、1秒あたりのレート制限、ヘルスルーティング、適切な暗号化キーローテーション、キューテストの改善、[Resend](https://resend.com)メールトランスポート、プロンプトバリデーターの統合、新しいArtisan コマンドなどを導入することにより、Laravel 10.xで行われた改善を継続しています。さらに、アプリケーションに堅牢なリアルタイム機能を提供するために、ファーストパーティのスケーラブルな WebSocket サーバーである Laravel Reverb が導入されました。

<a name="php-8"></a>
<!-- ### PHP 8.2 -->
### PHP 8.2

<!-- Laravel 11.x requires a minimum PHP version of 8.2. -->
Laravel 11.x には、最小 PHP バージョン 8.2 が必要です。

<a name="structure"></a>
<!-- ### Streamlined Application Structure -->
### Streamlined Application Structure

<!-- _Laravel's streamlined application structure was developed by [Taylor Otwell](https://github.com/taylorotwell) and [Nuno Maduro](https://github.com/nunomaduro)_. -->
_Laravel の合理化されたアプリケーション構造は、[Taylor Otwell](https://github.com/taylorotwell) および [Nuno Maduro](https://github.com/nunomaduro)_ によって開発されました。

<!-- Laravel 11 introduces a streamlined application structure for **new** Laravel applications, without requiring any changes to existing applications. The new application structure is intended to provide a leaner, more modern experience, while retaining many of the concepts that Laravel developers are already familiar with. Below we will discuss the highlights of Laravel's new application structure. -->
Laravel 11 では、既存のアプリケーションを変更する必要がなく、**新しい** Laravel アプリケーション用に合理化されたアプリケーション構造が導入されています。新しいアプリケーション構造は、Laravel 開発者がすでによく知っている概念の多くを保持しながら、より無駄がなく、より現代的なエクスペリエンスを提供することを目的としています。以下では、Laravel の新しいアプリケーション構造のハイライトについて説明します。

<!-- #### The Application Bootstrap File -->
#### The Application Bootstrap File

<!-- The `bootstrap/app.php` file has been revitalized as a code-first application configuration file. From this file, you may now customize your application's routing, middleware, service providers, exception handling, and more. This file unifies a variety of high-level application behavior settings that were previously scattered throughout your application's file structure: -->
`bootstrap/app.php` ファイルは、コードファーストのアプリケーション構成ファイルとして復活しました。このファイルから、アプリケーションのルーティング、ミドルウェア、サービスプロバイダ、例外処理などをカスタマイズできます。このファイルは、以前はアプリケーションのファイル構造全体に散在していたさまざまな高レベルのアプリケーション動作設定を統合します。

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        //
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();
```

<a name="service-providers"></a>
<!-- #### Service Providers -->
#### Service Providers

<!-- Instead of the default Laravel application structure containing five service providers, Laravel 11 only includes a single `AppServiceProvider`. The functionality of the previous service providers has been incorporated into the `bootstrap/app.php`, is handled automatically by the framework, or may be placed in your application's `AppServiceProvider`. -->
デフォルトの Laravel アプリケーション構造には 5 つのサービスプロバイダが含まれていますが、Laravel 11 には `AppServiceProvider` が 1 つだけ含まれています。以前のサービスプロバイダの機能は `bootstrap/app.php` に組み込まれており、フレームワークによって自動的に処理されるか、アプリケーションの `AppServiceProvider` に配置される場合があります。

<!-- For example, event discovery is now enabled by default, largely eliminating the need for manual registration of events and their listeners. However, if you do need to manually register events, you may simply do so in the `AppServiceProvider`. Similarly, route model bindings or authorization gates you may have previously registered in the `AuthServiceProvider` may also be registered in the `AppServiceProvider`. -->
たとえば、イベント検出がデフォルトで有効になり、イベントとそのリスナを手動で登録する必要がほとんどなくなりました。ただし、イベントを手動で登録する必要がある場合は、`AppServiceProvider` で簡単に登録できます。同様に、以前に `AuthServiceProvider` に登録したルート モデル バインディングまたは認可ゲートも、`AppServiceProvider` に登録される可能性があります。

<a name="opt-in-routing"></a>
<!-- #### Opt-in API and Broadcast Routing -->
#### Opt-in API and Broadcast Routing

<!-- The `api.php` and `channels.php` route files are no longer present by default, as many applications do not require these files. Instead, they may be created using simple Artisan commands: -->
`api.php` および `channels.php` ルート ファイルは、多くのアプリケーションでこれらのファイルが必要ないため、デフォルトでは存在しません。代わりに、単純な Artisan コマンドを使用して作成することもできます。

```shell
php artisan install:api

php artisan install:broadcasting
```

<a name="middleware"></a>
<!-- #### Middleware -->
#### Middleware

<!-- Previously, new Laravel applications included nine middleware. These middleware performed a variety of tasks such as authenticating requests, trimming input strings, and validating CSRF tokens. -->
以前は、新しい Laravel アプリケーションには 9 つのミドルウェアが含まれていました。これらのミドルウェアは、リクエストの認証、入力文字列のトリミング、CSRF トークンの検証などのさまざまなタスクを実行しました。

<!-- In Laravel 11, these middleware have been moved into the framework itself, so that they do not add bulk to your application's structure. New methods for customizing the behavior of these middleware have been added to the framework and may be invoked from your application's `bootstrap/app.php` file: -->
Laravel 11 では、これらのミドルウェアはフレームワーク自体に移動されているため、アプリケーションの構造がかさばることはありません。これらのミドルウェアの動作をカスタマイズするための新しいメソッドがフレームワークに追加されており、アプリケーションの `bootstrap/app.php` ファイルから呼び出すことができます。

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(
        except: ['stripe/*']
    );

    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ])
})
```

<!-- Since all middleware can be easily customized via your application's `bootstrap/app.php`, the need for a separate HTTP "kernel" class has been eliminated. -->
すべてのミドルウェアはアプリケーションの `bootstrap/app.php` を介して簡単にカスタマイズできるため、別個の HTTP "カーネル" クラスの必要性がなくなりました。

<a name="scheduling"></a>
<!-- #### Scheduling -->
#### Scheduling

<!-- Using a new `Schedule` facade, scheduled tasks may now be defined directly in your application's `routes/console.php` file, eliminating the need for a separate console "kernel" class: -->
新しい `Schedule` ファサードを使用すると、スケジュールされたタスクをアプリケーションの `routes/console.php` ファイルで直接定義できるようになり、別個のコンソール「カーネル」クラスが不要になります。

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->daily();
```

<a name="exception-handling"></a>
<!-- #### Exception Handling -->
#### Exception Handling

<!-- Like routing and middleware, exception handling can now be customized from your application's `bootstrap/app.php` file instead of a separate exception handler class, reducing the overall number of files included in a new Laravel application: -->
ルーティングやミドルウェアと同様に、例外処理を個別の例外ハンドラー クラスではなくアプリケーションの `bootstrap/app.php` ファイルからカスタマイズできるようになり、新しい Laravel アプリケーションに含まれるファイル全体の数が削減されます。

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport(MissedFlightException::class);

    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

<a name="base-controller-class"></a>
<!-- #### Base `Controller` Class -->
#### Base `Controller` Class

<!-- The base controller included in new Laravel applications has been simplified. It no longer extends Laravel's internal `Controller` class, and the `AuthorizesRequests` and `ValidatesRequests` traits have been removed, as they may be included in your application's individual controllers if desired: -->
新しい Laravel アプリケーションに含まれるベース コントローラが簡素化されました。 Laravel の内部 `Controller` クラスは拡張されなくなり、必要に応じてアプリケーションの個々のコントローラに含めることができるため、`AuthorizesRequests` および `ValidatesRequests` トレイトは削除されました。

```
<?php

namespace App\Http\Controllers;

abstract class Controller
{
    //
}
```

<a name="application-defaults"></a>
<!-- #### Application Defaults -->
#### Application Defaults

<!-- By default, new Laravel applications use SQLite for database storage, as well as the `database` driver for Laravel's session, cache, and queue. This allows you to begin building your application immediately after creating a new Laravel application, without being required to install additional software or create additional database migrations. -->
デフォルトでは、新しい Laravel アプリケーションはデータベース ストレージに SQLite を使用するほか、Laravel のセッション、キャッシュ、キューに `database` ドライバを使用します。これにより、追加のソフトウェアをインストールしたり、追加のデータベース移行を作成したりすることなく、新しい Laravel アプリケーションを作成した後すぐにアプリケーションの構築を開始できます。

<!-- In addition, over time, the `database` drivers for these Laravel services have become robust enough for production usage in many application contexts; therefore, they provide a sensible, unified choice for both local and production applications. -->
さらに、時間の経過とともに、これらの Laravel サービスの `database` ドライバは、多くのアプリケーション コンテキストで実稼働環境で使用できるほど十分に堅牢になりました。したがって、ローカル アプリケーションと運用アプリケーションの両方に賢明で統一された選択肢を提供します。

<a name="reverb"></a>
<!-- ### Laravel Reverb -->
### Laravel Reverb

<!-- _Laravel Reverb was developed by [Joe Dixon](https://github.com/joedixon)_. -->
_Laravel Reverb は [Joe Dixon](https://github.com/joedixon)_ によって開発されました。

<!-- [Laravel Reverb](https://reverb.laravel.com) brings blazing-fast and scalable real-time WebSocket communication directly to your Laravel application, and provides seamless integration with Laravel’s existing suite of event broadcasting tools, such as Laravel Echo. -->
[Laravel Reverb](https://reverb.laravel.com) は、超高速でスケーラブルなリアルタイム WebSocket 通信を Laravel アプリケーションに直接もたらし、Laravel Echo などの Laravel の既存のイベント ブロードキャスト ツール スイートとのシームレスな統合を提供します。

```shell
php artisan reverb:start
```

<!-- In addition, Reverb supports horizontal scaling via Redis's publish / subscribe capabilities, allowing you to distribute your WebSocket traffic across multiple backend Reverb servers all supporting a single, high-demand application. -->
さらに、Reverb は Redis のパブリッシュ/サブスクライブ機能を介した水平スケーリングをサポートしており、単一の高需要アプリケーションをサポートする複数のバックエンド Reverb サーバー全体に WebSocket トラフィックを分散できます。

<!-- For more information on Laravel Reverb, please consult the complete [Reverb documentation](/docs/11.x/reverb). -->
Laravel Reverb の詳細については、完全な [Reverb documentation](/docs/11.x/reverb) を参照してください。

<a name="rate-limiting"></a>
<!-- ### Per-Second Rate Limiting -->
### Per-Second Rate Limiting

<!-- _Per-second rate limiting was contributed by [Tim MacDonald](https://github.com/timacdonald)_. -->
_秒あたりのレート制限は、[Tim MacDonald](https://github.com/timacdonald)_ によって提供されました。

<!-- Laravel now supports "per-second" rate limiting for all rate limiters, including those for HTTP requests and queued jobs. Previously, Laravel's rate limiters were limited to "per-minute" granularity: -->
Laravel は、HTTP リクエストやキューに入れられたジョブのレート リミッターを含む、すべてのレート リミッターに対して「1 秒あたり」のレート制限をサポートするようになりました。以前は、Laravel のレート リミッターは「1 分あたり」の粒度に制限されていました。

```php
RateLimiter::for('invoices', function (Request $request) {
    return Limit::perSecond(1);
});
```

<!-- For more information on rate limiting in Laravel, check out the [rate limiting documentation](/docs/11.x/routing#rate-limiting). -->
Laravel のレート制限の詳細については、[rate limiting documentation](/docs/11.x/routing#rate-limiting) を確認してください。

<a name="health"></a>
<!-- ### Health Routing -->
### Health Routing

<!-- _Health routing was contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_ヘルス ルーティングは [Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- New Laravel 11 applications include a `health` routing directive, which instructs Laravel to define a simple health-check endpoint that may be invoked by third-party application health monitoring services or orchestration systems like Kubernetes. By default, this route is served at `/up`: -->
新しい Laravel 11 アプリケーションには、`health` ルーティング ディレクティブが含まれています。これは、サードパーティのアプリケーション健全性監視サービスや Kubernetes などのオーケストレーション システムによって呼び出される単純な健全性チェック エンドポイントを定義するように Laravel に指示します。デフォルトでは、このルートは `/up` で提供されます。

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up',
)
```

<!-- When HTTP requests are made to this route, Laravel will also dispatch a `DiagnosingHealth` event, allowing you to perform additional health checks that are relevant to your application. -->
このルートに対して HTTP リクエストが行われると、Laravel は `DiagnosingHealth` イベントも送出し、アプリケーションに関連する追加のヘルスチェックを実行できるようにします。

<a name="encryption"></a>
<!-- ### Graceful Encryption Key Rotation -->
### Graceful Encryption Key Rotation

<!-- _Graceful encryption key rotation was contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_正常な暗号化キーのローテーションは、[Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- Since Laravel encrypts all cookies, including your application's session cookie, essentially every request to a Laravel application relies on encryption. However, because of this, rotating your application's encryption key would log all users out of your application. In addition, decrypting data that was encrypted by the previous encryption key becomes impossible. -->
Laravel はアプリケーションのセッション Cookie を含むすべての Cookie を暗号化するため、基本的に Laravel アプリケーションへのすべてのリクエストは暗号化に依存します。ただし、このため、アプリケーションの暗号化キーをローテーションすると、すべてのユーザーがアプリケーションからログアウトされます。また、以前の暗号鍵で暗号化されたデータは復号できなくなります。

<!-- Laravel 11 allows you to define your application's previous encryption keys as a comma-delimited list via the `APP_PREVIOUS_KEYS` environment variable. -->
Laravel 11 では、`APP_PREVIOUS_KEYS` 環境変数を使用して、アプリケーションの以前の暗号化キーをカンマ区切りのリストとして定義できます。

<!-- When encrypting values, Laravel will always use the "current" encryption key, which is within the `APP_KEY` environment variable. When decrypting values, Laravel will first try the current key. If decryption fails using the current key, Laravel will try all previous keys until one of the keys is able to decrypt the value. -->
値を暗号化するとき、Laravel は常に `APP_KEY` 環境変数内にある「現在の」暗号化キーを使用します。値を復号化するとき、Laravel は最初に現在のキーを試行します。現在のキーを使用した復号化が失敗した場合、Laravel はキーの 1 つで値を復号化できるまで、以前のすべてのキーを試します。

<!-- This approach to graceful decryption allows users to keep using your application uninterrupted even if your encryption key is rotated. -->
この正常な復号化のアプローチにより、暗号化キーがローテーションされた場合でも、ユーザーはアプリケーションを中断することなく使用し続けることができます。

<!-- For more information on encryption in Laravel, check out the [encryption documentation](/docs/11.x/encryption). -->
Laravel での暗号化の詳細については、[encryption documentation](/docs/11.x/encryption) を確認してください。

<a name="automatic-password-rehashing"></a>
<!-- ### Automatic Password Rehashing -->
### Automatic Password Rehashing

<!-- _Automatic password rehashing was contributed by [Stephen Rees-Carter](https://github.com/valorin)_. -->
_自動パスワード再ハッシュは、[Stephen Rees-Carter](https://github.com/valorin)_ によって提供されました。

<!-- Laravel's default password hashing algorithm is bcrypt. The "work factor" for bcrypt hashes can be adjusted via the `config/hashing.php` configuration file or the `BCRYPT_ROUNDS` environment variable. -->
Laravel のデフォルトのパスワードハッシュアルゴリズムは bcrypt です。 bcrypt ハッシュの「作業係数」は、`config/hashing.php` 構成ファイルまたは `BCRYPT_ROUNDS` 環境変数を介して調整できます。

<!-- Typically, the bcrypt work factor should be increased over time as CPU / GPU processing power increases. If you increase the bcrypt work factor for your application, Laravel will now gracefully and automatically rehash user passwords as users authenticate with your application. -->
通常、CPU / GPU の処理能力が増加するにつれて、bcrypt 作業係数は時間の経過とともに増加する必要があります。アプリケーションの bcrypt 作業係数を増やすと、ユーザーがアプリケーションで認証されるときに、Laravel はユーザーのパスワードを適切かつ自動的に再ハッシュするようになります。

<a name="prompt-validation"></a>
<!-- ### Prompt Validation -->
### Prompt Validation

<!-- _Prompt validator integration was contributed by [Andrea Marco Sartori](https://github.com/cerbero90)_. -->
_プロンプトバリデーターの統合は、[Andrea Marco Sartori](https://github.com/cerbero90)_ によって提供されました。

<!-- [Laravel Prompts](/docs/11.x/prompts) is a PHP package for adding beautiful and user-friendly forms to your command-line applications, with browser-like features including placeholder text and validation. -->
[Laravel Prompts](/docs/11.x/prompts) は、プレースホルダー テキストや検証などのブラウザーのような機能を備えた、美しくユーザーフレンドリーなフォームをコマンドライン アプリケーションに追加するための PHP パッケージです。

<!-- Laravel Prompts supports input validation via closures: -->
Laravel プロンプトは、クロージャーを介した入力検証をサポートしています。

```php
$name = text(
    label: 'What is your name?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

<!-- However, this can become cumbersome when dealing with many inputs or complicated validation scenarios. Therefore, in Laravel 11, you may utilize the full power of Laravel's [validator](/docs/11.x/validation) when validating prompt inputs: -->
ただし、多くの入力や複雑な検証シナリオを扱う場合、これは面倒になる可能性があります。したがって、Laravel 11 では、プロンプト入力を検証するときに Laravel の [validator](/docs/11.x/validation) の機能を最大限に活用できます。

```php
$name = text('What is your name?', validate: [
    'name' => 'required|min:3|max:255',
]);
```

<a name="queue-interaction-testing"></a>
<!-- ### Queue Interaction Testing -->
### Queue Interaction Testing

<!-- _Queue interaction testing was contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_キューの相互作用テストは [Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- Previously, attempting to test that a queued job was released, deleted, or manually failed was cumbersome and required the definition of custom queue fakes and stubs. However, in Laravel 11, you may easily test for these queue interactions using the `withFakeQueueInteractions` method: -->
以前は、キューに入れられたジョブが解放、削除されたか、手動で失敗したかをテストしようとするのは面倒で、カスタム キューのフェイクとスタブを定義する必要がありました。ただし、Laravel 11 では、`withFakeQueueInteractions` メソッドを使用して、これらのキューの相互作用を簡単にテストできます。

```php
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
```

<!-- For more information on testing queued jobs, check out the [queue documentation](/docs/11.x/queues#testing). -->
キューに入れられたジョブのテストの詳細については、[queue documentation](/docs/11.x/queues#testing) を確認してください。

<a name="new-artisan-commands"></a>
<!-- ### New Artisan Commands -->
### New Artisan Commands

<!-- _Class creation Artisan commands were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_クラス作成Artisan コマンドは、[Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- New Artisan commands have been added to allow the quick creation of classes, enums, interfaces, and traits: -->
新しい Artisan コマンドが追加され、クラス、列挙型、インターフェイス、特性を迅速に作成できるようになりました。

```shell
php artisan make:class
php artisan make:enum
php artisan make:interface
php artisan make:trait
```

<a name="model-cast-improvements"></a>
<!-- ### Model Casts Improvements -->
### Model Casts Improvements

<!-- _Model casts improvements were contributed by [Nuno Maduro](https://github.com/nunomaduro)_. -->
_モデル castの改善は、[Nuno Maduro](https://github.com/nunomaduro)_ によって提供されました。

<!-- Laravel 11 supports defining your model's casts using a method instead of a property. This allows for streamlined, fluent cast definitions, especially when using casts with arguments: -->
Laravel 11 では、プロパティの代わりにメソッドを使用したモデルのcastの定義がサポートされています。これにより、特に引数付きのcastを使用する場合に、合理的で流暢なcast定義が可能になります。

```
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::using(OptionCollection::class),
                  // AsEncryptedCollection::using(OptionCollection::class),
                  // AsEnumArrayObject::using(OptionEnum::class),
                  // AsEnumCollection::using(OptionEnum::class),
    ];
}
```

<!-- For more information on attribute casting, review the [Eloquent documentation](/docs/11.x/eloquent-mutators#attribute-casting). -->
attribute castingの詳細については、[Eloquent documentation](/docs/11.x/eloquent-mutators#attribute-casting) を参照してください。

<a name="the-once-function"></a>
<!-- ### The `once` Function -->
### The `once` Function

<!-- _The `once` helper was contributed by [Taylor Otwell](https://github.com/taylorotwell)_ and _[Nuno Maduro](https://github.com/nunomaduro)_. -->
_`once` ヘルパは、[Taylor Otwell](https://github.com/taylorotwell)_ および _[Nuno Maduro](https://github.com/nunomaduro)_ によって提供されました。

<!-- The `once` helper function executes the given callback and caches the result in memory for the duration of the request. Any subsequent calls to the `once` function with the same callback will return the previously cached result: -->
`once` ヘルパ関数は、指定されたコールバックを実行し、リクエストの間、結果をメモリにキャッシュします。同じコールバックを使用した後続の `once` 関数の呼び出しでは、以前にキャッシュされた結果が返されます。

```
function random(): int
{
    return once(function () {
        return random_int(1, 1000);
    });
}

random(); // 123
random(); // 123 (cached result)
random(); // 123 (cached result)
```

<!-- For more information on the `once` helper, check out the [helpers documentation](/docs/11.x/helpers#method-once). -->
`once` ヘルパの詳細については、[helpers documentation](/docs/11.x/helpers#method-once) を確認してください。

<a name="database-performance"></a>
<!-- ### Improved Performance When Testing With In-Memory Databases -->
### Improved Performance When Testing With In-Memory Databases

<!-- _Improved in-memory database testing performance was contributed by [Anders Jenbo](https://github.com/AJenbo)_ -->
_メモリ内データベースのテスト パフォーマンスの向上は、[Anders Jenbo](https://github.com/AJenbo) によるものです_

<!-- Laravel 11 offers a significant speed boost when using the `:memory:` SQLite database during testing. To accomplish this, Laravel now maintains a reference to PHP's PDO object and reuses it across connections, often cutting total test run time in half. -->
Laravel 11 では、テスト中に `:memory:` SQLite データベースを使用すると速度が大幅に向上します。これを達成するために、Laravel は PHP の PDO オブジェクトへの参照を維持し、それを接続全体で再利用することで、多くの場合、合計テスト実行時間を半分に短縮します。

<a name="mariadb"></a>
<!-- ### Improved Support for MariaDB -->
### Improved Support for MariaDB

<!-- _Improved support for MariaDB was contributed by [Jonas Staudenmeir](https://github.com/staudenmeir) and [Julius Kiekbusch](https://github.com/Jubeki)_ -->
_MariaDB のサポートの改善は、[Jonas Staudenmeir](https://github.com/staudenmeir) および [Julius Kiekbusch](https://github.com/Jubeki) によって提供されました_

<!-- Laravel 11 includes improved support for MariaDB. In previous Laravel releases, you could use MariaDB via Laravel's MySQL driver. However, Laravel 11 now includes a dedicated MariaDB driver which provides better defaults for this database system. -->
Laravel 11 には、MariaDB のサポートが改善されました。以前の Laravel リリースでは、Laravel の MySQL ドライバ経由で MariaDB を使用できました。ただし、Laravel 11 には、このデータベース システムにより良いデフォルトを提供する専用の MariaDB ドライバが含まれています。

<!-- For more information on Laravel's database drivers, check out the [database documentation](/docs/11.x/database). -->
Laravel のデータベースドライバの詳細については、[database documentation](/docs/11.x/database) を確認してください。

<a name="inspecting-database"></a>
<!-- ### Inspecting Databases and Improved Schema Operations -->
### Inspecting Databases and Improved Schema Operations

<!-- _Improved schema operations and database inspection was contributed by [Hafez Divandari](https://github.com/hafezdivandari)_ -->
_スキーマ操作とデータベース検査の改善は、[Hafez Divandari](https://github.com/hafezdivandari) の貢献によるものです_

<!-- Laravel 11 provides additional database schema operation and inspection methods, including the native modifying, renaming, and dropping of columns. Furthermore, advanced spatial types, non-default schema names, and native schema methods for manipulating tables, views, columns, indexes, and foreign keys are provided: -->
Laravel 11 では、ネイティブの変更、名前変更、列の削除など、追加のデータベース スキーマ操作および検査方法が提供されます。さらに、テーブル、ビュー、列、インデックス、外部キーを操作するための高度な空間タイプ、デフォルト以外のスキーマ名、およびネイティブ スキーマ メソッドが提供されます。

```
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

