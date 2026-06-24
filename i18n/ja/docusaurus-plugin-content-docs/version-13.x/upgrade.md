<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading To 13.0 From 12.x](#upgrade-13.0)
    - [Upgrading Using AI](#upgrading-using-ai)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating the Laravel Installer](#updating-the-laravel-installer)
- [Request Forgery Protection](#request-forgery-protection)

<!-- </div> -->
</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Cache `serializable_classes` Configuration](#cache-serializable_classes-configuration)
- [Database `upsert` With MySQL or MariaDB](#database-upsert-mariadb-mysql)

<!-- </div> -->
</div>

<a name="low-impact-changes"></a>
<!-- ## Low Impact Changes -->
## Low Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Cache Prefixes and Session Cookie Names](#cache-prefixes-and-session-cookie-names)
- [Collection Model Serialization Restores Eager-Loaded Relations](#collection-model-serialization-restores-eager-loaded-relations)
- [`Container::call` and Nullable Class Defaults](#containercall-and-nullable-class-defaults)
- [Domain Route Registration Precedence](#domain-route-registration-precedence)
- [`JobAttempted` Event Exception Payload](#jobattempted-event-exception-payload)
- [Manager `extend` Callback Binding](#manager-extend-callback-binding)
- [MySQL `DELETE` Queries With `JOIN`, `ORDER BY`, and `LIMIT`](#mysql-delete-queries-with-join-order-by-and-limit)
- [Pagination Bootstrap View Names](#pagination-bootstrap-view-names)
- [Polymorphic Pivot Table Name Generation](#polymorphic-pivot-table-name-generation)
- [`QueueBusy` Event Property Rename](#queuebusy-event-property-rename)
- [`Str` Factories Reset Between Tests](#str-factories-reset-between-tests)

<!-- </div> -->
</div>

<a name="upgrade-13.0"></a>
<!-- ## Upgrading To 13.0 From 12.x -->
## Upgrading To 13.0 From 12.x

<!-- #### Estimated Upgrade Time: 10 Minutes -->
#### Estimated Upgrade Time: 10 Minutes

> [!NOTE]
> 私たちは、考えられるすべての重大な変更を文書化するよう努めます。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。時間を節約するには、[Shift](https://laravelshift.com) を使用できます。 Shift は、Laravel のアップグレードを自動化するコミュニティによって管理されるサービスです。

<a name="upgrading-using-ai"></a>
<!-- ### Upgrading Using AI -->
### Upgrading Using AI

<!-- You can automate your upgrade using [Laravel Boost](https://github.com/laravel/boost). Boost is a first-party MCP server that provides your AI assistant with guided upgrade prompts — once installed in any Laravel 12 application, use the `/upgrade-laravel-v13` slash command in Claude Code, Cursor, OpenCode, Gemini, or VS Code to begin the upgrade to Laravel 13. This command requires Laravel Boost `^2.0`. -->
[Laravel Boost](https://github.com/laravel/boost) を使用してアップグレードを自動化できます。 Boost は、AI アシスタントにガイド付きアップグレード プロンプトを提供するファーストパーティ MCP サーバーです。Laravel 12 アプリケーションにインストールしたら、Claude Code、Cursor、OpenCode、Gemini、または VS Code で `/upgrade-laravel-v13` スラッシュ コマンドを使用して、Laravel 13 へのアップグレードを開始します。このコマンドには、Laravel Boost `^2.0` が必要です。

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- You should update the following dependencies in your application's `composer.json` file: -->
アプリケーションの `composer.json` ファイル内の次の依存関係を更新する必要があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `laravel/framework` to `^13.0`
- `laravel/boost` to `^2.0`
- `laravel/tinker` to `^3.0`
- `phpunit/phpunit` to `^12.0`
- `pestphp/pest` to `^4.0`
-->
- `laravel/framework` ～ `^13.0`
- `laravel/boost` ～ `^2.0`
- `laravel/tinker` ～ `^3.0`
- `phpunit/phpunit` ～ `^12.0`
- `pestphp/pest` ～ `^4.0`

<!-- </div> -->
</div>

<a name="updating-the-laravel-installer"></a>
<!-- ### Updating the Laravel Installer -->
### Updating the Laravel Installer

<!-- If you are using the Laravel installer CLI tool to create new Laravel applications, you should update your installer installation for Laravel 13.x compatibility. -->
Laravel インストーラー CLI ツールを使用して新しい Laravel アプリケーションを作成している場合は、Laravel 13.x との互換性を確保するためにインストーラーのインストールを更新する必要があります。

<!-- If you installed the Laravel installer via `composer global require`, you may update the installer using `composer global update`: -->
`composer global require` 経由で Laravel インストーラーをインストールした場合は、`composer global update` を使用してインストーラーを更新できます。

```shell
composer global update laravel/installer
```

<!-- Or, if you are using [Laravel Herd's](https://herd.laravel.com) bundled copy of the Laravel installer, you should update your Herd installation to the latest release. -->
または、Laravel インストーラーの [Laravel Herd's](https://herd.laravel.com) バンドル コピーを使用している場合は、Herd インストールを最新リリースに更新する必要があります。

<a name="cache"></a>
<!-- ### Cache -->
### Cache

<a name="cache-prefixes-and-session-cookie-names"></a>
<!-- #### Cache Prefixes and Session Cookie Names -->
#### Cache Prefixes and Session Cookie Names

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Laravel's default cache and Redis key prefixes now use hyphenated suffixes. -->
Laravel のデフォルトのキャッシュと Redis キーのプレフィックスは、ハイフンで区切られたサフィックスを使用するようになりました。

<!-- In most applications, this change will not apply because application-level configuration files already define these values. This primarily affects applications that rely on framework-level fallback configuration when corresponding application config values are not present. -->
ほとんどのアプリケーションでは、アプリケーション レベルの構成ファイルでこれらの値がすでに定義されているため、この変更は適用されません。これは主に、対応するアプリケーション構成値が存在しない場合にフレームワーク レベルのフォールバック構成に依存するアプリケーションに影響します。

<!-- If your application relies on these generated defaults, cache keys and session cookie names may change after upgrading: -->
アプリケーションがこれらの生成されたデフォルトに依存している場合、アップグレード後にキャッシュ キーとセッション Cookie 名が変更される可能性があります。

```php
// Laravel <= 12.x
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_cache_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_database_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_session';

// Laravel >= 13.x
Str::slug((string) env('APP_NAME', 'laravel')).'-cache-';
Str::slug((string) env('APP_NAME', 'laravel')).'-database-';
Str::slug((string) env('APP_NAME', 'laravel')).'-session';
```

<!-- To retain previous behavior, explicitly configure `CACHE_PREFIX`, `REDIS_PREFIX`, and `SESSION_COOKIE` in your environment. -->
以前の動作を保持するには、環境内で `CACHE_PREFIX`、`REDIS_PREFIX`、および `SESSION_COOKIE` を明示的に構成します。

<a name="store-and-repository-contracts-touch"></a>
<!-- #### `Store` and `Repository` Contracts: `touch` -->
#### `Store` and `Repository` Contracts: `touch`

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The cache contracts now include a `touch` method for extending item TTLs. If you maintain custom cache store implementations, you should add this method: -->
キャッシュ コントラクトには、アイテム TTL を拡張するための `touch` メソッドが含まれるようになりました。カスタム キャッシュ ストアの実装を維持する場合は、次のメソッドを追加する必要があります。

```php
// Illuminate\Contracts\Cache\Store
public function touch($key, $seconds);
```

<a name="cache-serializable_classes-configuration"></a>
<!-- #### Cache `serializable_classes` Configuration -->
#### Cache `serializable_classes` Configuration

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The default application `cache` configuration now includes a `serializable_classes` option set to `false`. This hardens cache unserialization behavior to help prevent PHP deserialization gadget chain attacks if your application's `APP_KEY` is leaked. If your application intentionally stores PHP objects in cache, you should explicitly list the classes that may be unserialized: -->
デフォルトのアプリケーションの `cache` 構成には、`false` に設定された `serializable_classes` オプションが含まれるようになりました。これにより、キャッシュのシリアル化解除動作が強化され、アプリケーションの `APP_KEY` が漏洩した場合に PHP シリアル化解除ガジェット チェーン攻撃を防ぐことができます。アプリケーションが意図的に PHP オブジェクトをキャッシュに保存する場合は、シリアル化解除される可能性のあるクラスを明示的にリストする必要があります。

```php
'serializable_classes' => [
    App\Data\CachedDashboardStats::class,
    App\Support\CachedPricingSnapshot::class,
],
```

<!-- If your application previously relied on unserializing arbitrary cached objects, you will need to migrate that usage to explicit class allow-lists or to non-object cache payloads (such as arrays). -->
アプリケーションが以前に任意のキャッシュされたオブジェクトのシリアル化解除に依存していた場合は、その使用法を明示的なクラス許可リストまたは非オブジェクト キャッシュ ペイロード (配列など) に移行する必要があります。

<a name="container"></a>
<!-- ### Container -->
### Container

<a name="containercall-and-nullable-class-defaults"></a>
<!-- #### `Container::call` and Nullable Class Defaults -->
#### `Container::call` and Nullable Class Defaults

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- `Container::call` now respects nullable class parameter defaults when no binding exists, matching constructor injection behavior introduced in Laravel 12: -->
`Container::call` は、バインディングが存在しない場合に null 許容クラス パラメーターのデフォルトを尊重するようになり、Laravel 12 で導入されたコンストラクター インジェクション動作と一致します。

```php
$container->call(function (?Carbon $date = null) {
    return $date;
});

// Laravel <= 12.x: Carbon instance
// Laravel >= 13.x: null
```

<!-- If your method-call injection logic depended on the previous behavior, you may need to update it. -->
メソッド呼び出し挿入ロジックが以前の動作に依存していた場合は、それを更新する必要がある場合があります。

<a name="contracts"></a>
<!-- ### Contracts -->
### Contracts

<a name="dispatcher-contract-dispatchafterresponse"></a>
<!-- #### `Dispatcher` Contract: `dispatchAfterResponse` -->
#### `Dispatcher` Contract: `dispatchAfterResponse`

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Illuminate\Contracts\Bus\Dispatcher` contract now includes the `dispatchAfterResponse($command, $handler = null)` method. -->
`Illuminate\Contracts\Bus\Dispatcher` コントラクトに `dispatchAfterResponse($command, $handler = null)` メソッドが含まれるようになりました。

<!-- If you maintain a custom dispatcher implementation, add this method to your class. -->
カスタム ディスパッチャ実装を維持する場合は、このメソッドをクラスに追加します。

<a name="responsefactory-contract-eventstream"></a>
<!-- #### `ResponseFactory` Contract: `eventStream` -->
#### `ResponseFactory` Contract: `eventStream`

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Illuminate\Contracts\Routing\ResponseFactory` contract now includes an `eventStream` signature. -->
`Illuminate\Contracts\Routing\ResponseFactory` コントラクトに `eventStream` 署名が含まれるようになりました。

<!-- If you maintain a custom implementation of this contract, you should add this method. -->
このコントラクトのカスタム実装を維持する場合は、このメソッドを追加する必要があります。

<a name="mustverifyemail-contract-markemailasunverified"></a>
<!-- #### `MustVerifyEmail` Contract: `markEmailAsUnverified` -->
#### `MustVerifyEmail` Contract: `markEmailAsUnverified`

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Illuminate\Contracts\Auth\MustVerifyEmail` contract now includes `markEmailAsUnverified()`. -->
`Illuminate\Contracts\Auth\MustVerifyEmail` コントラクトに `markEmailAsUnverified()` が含まれるようになりました。

<!-- If you provide a custom implementation of this contract, add this method to remain compatible. -->
このコントラクトのカスタム実装を提供する場合は、互換性を維持するためにこのメソッドを追加してください。

<a name="database"></a>
<!-- ### Database -->
### Database

<a name="database-upsert-mariadb-mysql"></a>
<!-- #### Database `upsert` With MySQL or MariaDB -->
#### Database `upsert` With MySQL or MariaDB

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- Laravel now validates that the caller provides a non-empty value for `uniqueBy`, and will throw an `InvalidArgumentException` instead of generating invalid SQL. -->
Laravel は、呼び出し元が `uniqueBy` に空ではない値を提供していることを検証し、無効な SQL を生成する代わりに `InvalidArgumentException` をスローするようになりました。

<!-- Although the MariaDB and MySQL database drivers ignore the `uniqueBy` value and always use the table's primary and unique indexes to detect existing records, the validation still applies. An `InvalidArgumentException` will be thrown if `uniqueBy` is empty. -->
MariaDB および MySQL データベース ドライバは `uniqueBy` 値を無視し、常にテーブルのプライマリ インデックスと一意のインデックスを使用して既存のレコードを検出しますが、検証は引き続き適用されます。 `uniqueBy` が空の場合、`InvalidArgumentException` がスローされます。

<a name="mysql-delete-queries-with-join-order-by-and-limit"></a>
<!-- #### MySQL `DELETE` Queries With `JOIN`, `ORDER BY`, and `LIMIT` -->
#### MySQL `DELETE` Queries With `JOIN`, `ORDER BY`, and `LIMIT`

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Laravel now compiles full `DELETE ... JOIN` queries including `ORDER BY` and `LIMIT` for MySQL grammar. -->
Laravel は、MySQL 文法用の `ORDER BY` および `LIMIT` を含む完全な `DELETE ... JOIN` クエリをコンパイルするようになりました。

<!-- In previous versions, `ORDER BY` / `LIMIT` clauses could be silently ignored on joined deletes. In Laravel 13, these clauses are included in the generated SQL. As a result, database engines that do not support this syntax (such as standard MySQL / MariaDB variants) may now throw a `QueryException` instead of executing an unbounded delete. -->
以前のバージョンでは、結合削除時に `ORDER BY` / `LIMIT` 句がサイレントに無視される可能性がありました。 Laravel 13 では、これらの句は生成される SQL に含まれます。その結果、この構文をサポートしないデータベース エンジン (標準の MySQL / MariaDB バリアントなど) は、無制限の削除を実行する代わりに `QueryException` をスローする可能性があります。

<a name="eloquent"></a>
<!-- ### Eloquent -->
### Eloquent

<a name="model-booting-and-nested-instantiation"></a>
<!-- #### Model Booting and Nested Instantiation -->
#### Model Booting and Nested Instantiation

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Creating a new model instance while that model is still booting is now disallowed and throws a `LogicException`. -->
モデルの起動中に新しいモデル インスタンスを作成することは禁止され、`LogicException` がスローされます。

<!-- This affects code that instantiates models from inside model `boot` methods or trait `boot*` methods: -->
これは、モデル `boot` メソッドまたは特性 `boot*` メソッド内からモデルをインスタンス化するコードに影響します。

```php
protected static function boot()
{
    parent::boot();

    // No longer allowed during booting...
    (new static())->getTable();
}
```

<!-- Move this logic outside the boot cycle to avoid nested booting. -->
ネストされたブートを避けるために、このロジックをブート サイクルの外側に移動します。

<a name="polymorphic-pivot-table-name-generation"></a>
<!-- #### Polymorphic Pivot Table Name Generation -->
#### Polymorphic Pivot Table Name Generation

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- When table names are inferred for polymorphic pivot models using custom pivot model classes, Laravel now generates pluralized names. -->
カスタムピボットモデルクラスを使用して多態性ピボットモデルのテーブル名が推論されると、Laravel は複数形の名前を生成するようになりました。

<!-- If your application depended on the previous singular inferred names for morph pivot tables and used custom pivot classes, you should explicitly define the table name on your pivot model. -->
アプリケーションがモーフ ピボット テーブルの以前の単数形の推論名に依存し、カスタム ピボット クラスを使用していた場合は、ピボット モデルでテーブル名を明示的に定義する必要があります。

<a name="collection-model-serialization-restores-eager-loaded-relations"></a>
<!-- #### Collection Model Serialization Restores Eager-Loaded Relations -->
#### Collection Model Serialization Restores Eager-Loaded Relations

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- When Eloquent model collections are serialized and restored (such as in queued jobs), eager-loaded relations are now restored for the collection's models. -->
Eloquent モデル コレクションがシリアル化されて復元されるとき (キューに入れられたジョブなど)、コレクションのモデルに対して一括ロードされたリレーションが復元されるようになりました。

<!-- If your code depended on relations not being present after deserialization, you may need to adjust that logic. -->
コードが、逆シリアル化後に存在しないリレーションに依存している場合は、そのロジックを調整する必要がある場合があります。

<a name="http-client"></a>
<!-- ### HTTP Client -->
### HTTP Client

<a name="http-client-response-throw-and-throwif-signatures"></a>
<!-- #### HTTP Client `Response::throw` and `throwIf` Signatures -->
#### HTTP Client `Response::throw` and `throwIf` Signatures

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The HTTP client response methods now declare their callback parameters in the method signatures: -->
HTTP クライアント応答メソッドは、メソッド シグネチャでコールバック パラメータを宣言するようになりました。

```php
public function throw($callback = null);
public function throwIf($condition, $callback = null);
```

<!-- If you override these methods in custom response classes, ensure your method signatures are compatible. -->
カスタム応答クラスでこれらのメソッドをオーバーライドする場合は、メソッドのシグネチャに互換性があることを確認してください。

<a name="notifications"></a>
<!-- ### Notifications -->
### Notifications

<a name="default-password-reset-subject"></a>
<!-- #### Default Password Reset Subject -->
#### Default Password Reset Subject

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Laravel's default password reset mail subject has changed: -->
Laravelのデフォルトのパスワードリセットメールの件名が変更されました:

```text
// Laravel <= 12.x
Reset Password Notification

// Laravel >= 13.x
Reset your password
```

<!-- If your tests, assertions, or translation overrides depend on the previous default string, update them accordingly. -->
テスト、アサーション、または変換のオーバーライドが以前のデフォルト文字列に依存している場合は、それに応じてそれらを更新します。

<a name="queued-notifications-and-missing-models"></a>
<!-- #### Queued Notifications and Missing Models -->
#### Queued Notifications and Missing Models

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Queued notifications now respect the `#[DeleteWhenMissingModels]` attribute and `$deleteWhenMissingModels` property defined on the notification class. -->
キューに入れられた通知は、通知クラスで定義された `#[DeleteWhenMissingModels]` 属性と `$deleteWhenMissingModels` プロパティを尊重するようになりました。

<!-- In previous versions, missing models could still cause queued notification jobs to fail in cases where you expected them to be deleted. -->
以前のバージョンでは、モデルが欠落していると、キューに入れられた通知ジョブが削除されると予想していた場合に失敗する可能性がありました。

<a name="queue"></a>
<!-- ### Queue -->
### Queue

<a name="jobattempted-event-exception-payload"></a>
<!-- #### `JobAttempted` Event Exception Payload -->
#### `JobAttempted` Event Exception Payload

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `Illuminate\Queue\Events\JobAttempted` event now exposes the exception object (or `null`) via `$exception`, replacing the previous boolean `$exceptionOccurred` property: -->
`Illuminate\Queue\Events\JobAttempted` イベントは、以前のブール型 `$exceptionOccurred` プロパティを置き換えて、`$exception` 経由で例外オブジェクト (または `null`) を公開するようになりました。

```php
// Laravel <= 12.x
$event->exceptionOccurred;

// Laravel >= 13.x
$event->exception;
```

<!-- If you listen for this event, update your listener code accordingly. -->
このイベントをリッスンする場合は、それに応じてリスナ コードを更新してください。

<a name="queuebusy-event-property-rename"></a>
<!-- #### `QueueBusy` Event Property Rename -->
#### `QueueBusy` Event Property Rename

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `Illuminate\Queue\Events\QueueBusy` event property `$connection` has been renamed to `$connectionName` for consistency with other queue events. -->
他のキュー イベントとの一貫性を保つために、`Illuminate\Queue\Events\QueueBusy` イベント プロパティ `$connection` の名前が `$connectionName` に変更されました。

<!-- If your listeners reference `$connection`, update them to `$connectionName`. -->
リスナが `$connection` を参照している場合は、`$connectionName` に更新します。

<a name="queue-contract-method-additions"></a>
<!-- #### `Queue` Contract Method Additions -->
#### `Queue` Contract Method Additions

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Illuminate\Contracts\Queue\Queue` contract now includes queue size inspection methods that were previously only declared in docblocks. -->
`Illuminate\Contracts\Queue\Queue` コントラクトには、以前は docblock でのみ宣言されていたキュー サイズ検査メソッドが含まれるようになりました。

<!-- If you maintain custom queue driver implementations of this contract, add implementations for: -->
このコントラクトのカスタム キュー ドライバ実装を維持する場合は、次の実装を追加します。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `pendingSize`
- `delayedSize`
- `reservedSize`
- `creationTimeOfOldestPendingJob`
-->
- `pendingSize`
- `delayedSize`
- `reservedSize`
- `creationTimeOfOldestPendingJob`

<!-- </div> -->
</div>

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<a name="domain-route-registration-precedence"></a>
<!-- #### Domain Route Registration Precedence -->
#### Domain Route Registration Precedence

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Routes with an explicit domain are now prioritized before non-domain routes in route matching. -->
明示的なドメインを持つルートが、ルート マッチングで非ドメイン ルートよりも優先されるようになりました。

<!-- This allows catch-all subdomain routes to behave consistently even when non-domain routes are registered earlier. If your application relied on previous registration precedence between domain and non-domain routes, review route matching behavior. -->
これにより、非ドメイン ルートが以前に登録されている場合でも、キャッチオール サブドメイン ルートが一貫して動作できるようになります。アプリケーションがドメイン ルートと非ドメイン ルート間の以前の登録の優先順位に依存している場合は、ルート マッチングの動作を確認してください。

<a name="scheduling"></a>
<!-- ### Scheduling -->
### Scheduling

<a name="withscheduling-registration-timing"></a>
<!-- #### `withScheduling` Registration Timing -->
#### `withScheduling` Registration Timing

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Schedules registered via `ApplicationBuilder::withScheduling()` are now deferred until `Schedule` is resolved. -->
`ApplicationBuilder::withScheduling()` 経由で登録されたスケジュールは、`Schedule` が解決されるまで延期されるようになりました。

<!-- If your application relied on immediate schedule registration timing during bootstrap, you may need to adjust that logic. -->
アプリケーションがブートストラップ中の即時スケジュール登録タイミングに依存している場合は、そのロジックを調整する必要がある場合があります。

<a name="security"></a>
<!-- ### Security -->
### Security

<a name="request-forgery-protection"></a>
<!-- #### Request Forgery Protection -->
#### Request Forgery Protection

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- Laravel's CSRF middleware has been renamed from `VerifyCsrfToken` to `PreventRequestForgery`, and now includes request-origin verification using the `Sec-Fetch-Site` header. -->
Laravel の CSRF ミドルウェアの名前が `VerifyCsrfToken` から `PreventRequestForgery` に変更され、`Sec-Fetch-Site` ヘッダーを使用したリクエスト送信元の検証が含まれるようになりました。

<!-- `VerifyCsrfToken` and `ValidateCsrfToken` remain as deprecated aliases, but direct references should be updated to `PreventRequestForgery`, especially when excluding middleware in tests or route definitions: -->
`VerifyCsrfToken` および `ValidateCsrfToken` は非推奨のエイリアスとして残りますが、特にテストまたはルート定義でミドルウェアを除外する場合は、直接参照を `PreventRequestForgery` に更新する必要があります。

```php
use Illuminate\Foundation\Http\Middleware\PreventRequestForgery;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;

// Laravel <= 12.x
->withoutMiddleware([VerifyCsrfToken::class]);

// Laravel >= 13.x
->withoutMiddleware([PreventRequestForgery::class]);
```

<!-- The middleware configuration API now also provides `preventRequestForgery(...)`. -->
ミドルウェア構成 API では、`preventRequestForgery(...)` も提供されるようになりました。

<a name="support"></a>
<!-- ### Support -->
### Support

<a name="manager-extend-callback-binding"></a>
<!-- #### Manager `extend` Callback Binding -->
#### Manager `extend` Callback Binding

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Custom driver closures registered via manager `extend` methods are now bound to the manager instance. -->
マネージャーの `extend` メソッドを介して登録されたカスタム ドライバ クロージャーがマネージャー インスタンスにバインドされるようになりました。

<!-- If you previously relied on another bound object (such as a service provider instance) as `$this` inside these callbacks, you should move those values into closure captures using `use (...)`. -->
以前にこれらのコールバック内で `$this` として別のバインドされたオブジェクト (サービスプロバイダ インスタンスなど) に依存していた場合は、`use (...)` を使用してそれらの値をクロージャ キャプチャに移動する必要があります。

<a name="str-factories-reset-between-tests"></a>
<!-- #### `Str` Factories Reset Between Tests -->
#### `Str` Factories Reset Between Tests

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Laravel now resets custom `Str` factories during test teardown. -->
Laravel は、テストのティアダウン中にカスタム `Str` ファクトリをリセットするようになりました。

<!-- If your tests depended on custom UUID / ULID / random string factories persisting between test methods, you should set them in each relevant test or setup hook. -->
テストがテスト メソッド間で持続するカスタム UUID / ULID / ランダム文字列ファクトリに依存している場合は、関連する各テスト フックまたはセットアップ フックでそれらを設定する必要があります。

<a name="jsfrom-uses-unescaped-unicode-by-default"></a>
<!-- #### `Js::from` Uses Unescaped Unicode By Default -->
#### `Js::from` Uses Unescaped Unicode By Default

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- `Illuminate\Support\Js::from` now uses `JSON_UNESCAPED_UNICODE` by default. -->
`Illuminate\Support\Js::from` はデフォルトで `JSON_UNESCAPED_UNICODE` を使用するようになりました。

<!-- If your tests or frontend output comparisons depended on escaped Unicode sequences (for example `\u00e8`), update your expectations. -->
テストまたはフロントエンドの出力比較がエスケープされた Unicode シーケンス (`\u00e8` など) に依存している場合は、期待値を更新してください。

<a name="utilities"></a>
<!-- ### Utilities -->
### Utilities

<a name="symfony-polyfill"></a>
<!-- #### Symfony PHP 8.5 Polyfill and Global Function Conflicts -->
#### Symfony PHP 8.5 Polyfill and Global Function Conflicts

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Laravel 13 introduces a dependency on `symfony/polyfill-php85`. On PHP versions below 8.5, this polyfill defines global functions such as `array_first()` and `array_last()` unless they have already been defined earlier during bootstrap. -->
Laravel 13 では、`symfony/polyfill-php85` への依存関係が導入されています。 8.5 より前の PHP バージョンでは、ブートストラップ中に事前に定義されていない限り、このポリフィルは `array_first()` や `array_last()` などのグローバル関数を定義します。

<!-- These functions may conflict with legacy helper packages like `laravel/helpers` or custom global helpers using the same names. For example, the historical `array_first()` helper accepted a callback to return the first matching element, while the polyfilled version only returns the first element of the array. -->
これらの関数は、`laravel/helpers` などの従来のヘルパ パッケージや、同じ名前を使用するカスタム グローバル ヘルパと競合する可能性があります。たとえば、従来の `array_first()` ヘルパはコールバックを受け入れて最初に一致した要素を返しましたが、ポリフィルされたバージョンは配列の最初の要素のみを返しました。

<!-- To avoid conflicts and ensure consistent behavior across PHP versions, you should prefer the `Illuminate\Support\Arr` methods: -->
競合を回避し、PHP バージョン間で一貫した動作を保証するには、`Illuminate\Support\Arr` メソッドを優先する必要があります。

```php
use Illuminate\Support\Arr;

Arr::first($array, function ($value) {
  return /* condition */;
});
```

<a name="views"></a>
<!-- ### Views -->
### Views

<a name="pagination-bootstrap-view-names"></a>
<!-- #### Pagination Bootstrap View Names -->
#### Pagination Bootstrap View Names

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The internal pagination view names for Bootstrap 3 defaults are now explicit: -->
Bootstrap 3 のデフォルトの内部ページネーション ビュー名が明示的になりました。

```nothing
// Laravel <= 12.x
pagination::default
pagination::simple-default

// Laravel >= 13.x
pagination::bootstrap-3
pagination::simple-bootstrap-3
```

<!-- If your application references the old pagination view names directly, update those references. -->
アプリケーションが古いページネーション ビュー名を直接参照している場合は、それらの参照を更新します。

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/12.x...13.x) and choose which updates are important to you. -->
`laravel/laravel` [GitHub repository](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。 [GitHub comparison tool](https://github.com/laravel/laravel/compare/12.x...13.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。

