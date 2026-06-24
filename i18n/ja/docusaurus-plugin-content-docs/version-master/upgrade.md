<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading To 12.0 From 11.x](#upgrade-12.0)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating the Laravel Installer](#updating-the-laravel-installer)

<!-- </div> -->
</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Models and UUIDv7](#models-and-uuidv7)

<!-- </div> -->
</div>

<a name="low-impact-changes"></a>
<!-- ## Low Impact Changes -->
## Low Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [Concurrency Result Index Mapping](#concurrency-result-index-mapping)
- [Container Class Dependency Resolution](#container-class-dependency-resolution)
- [Image Validation Now Excludes SVGs](#image-validation)
- [Local Filesystem Disk Default Root Path](#local-filesystem-disk-default-root-path)
- [Multi-Schema Database Inspecting](#multi-schema-database-inspecting)
- [Nested Array Request Merging](#nested-array-request-merging)

<!-- </div> -->
</div>

<a name="upgrade-12.0"></a>
<!-- ## Upgrading To 12.0 From 11.x -->
## Upgrading To 12.0 From 11.x

<!-- #### Estimated Upgrade Time: 5 Minutes -->
#### Estimated Upgrade Time: 5 Minutes

> [!NOTE]
> 私たちは、考えられるすべての重大な変更を文書化するよう努めます。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。時間を節約したいですか? [Laravel Shift](https://laravelshift.com/) を使用すると、アプリケーションのアップグレードを自動化できます。

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
- `laravel/framework` to `^12.0`
- `phpunit/phpunit` to `^11.0`
- `pestphp/pest` to `^3.0`
-->
- `laravel/framework` ～ `^12.0`
- `phpunit/phpunit` ～ `^11.0`
- `pestphp/pest` ～ `^3.0`

<!-- </div> -->
</div>

<a name="carbon-3"></a>
<!-- #### Carbon 3 -->
#### Carbon 3

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Support for Carbon 2.x has been removed. All Laravel 12 applications now require [Carbon 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html). -->
Carbon 2.x のサポートは削除されました。すべての Laravel 12 アプリケーションには [Carbon 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html) が必要になりました。

<a name="updating-the-laravel-installer"></a>
<!-- ### Updating the Laravel Installer -->
### Updating the Laravel Installer

<!-- If you are using the Laravel installer CLI tool to create new Laravel applications, you should update your installer installation to be compatible with Laravel 12.x and the [new Laravel starter kits](https://laravel.com/starter-kits). If you installed the Laravel installer via `composer global require`, you may update the installer using `composer global update`: -->
Laravel インストーラー CLI ツールを使用して新しい Laravel アプリケーションを作成している場合は、Laravel 12.x および [new Laravel starter kits](https://laravel.com/starter-kits) と互換性があるようにインストーラーのインストールを更新する必要があります。 `composer global require` 経由で Laravel インストーラーをインストールした場合は、`composer global update` を使用してインストーラーを更新できます。

```shell
composer global update laravel/installer
```

<!-- If you originally installed PHP and Laravel via `php.new`, you may simply re-run the `php.new` installation commands for your operating system to install the latest version of PHP and the Laravel installer: -->
最初に `php.new` 経由で PHP と Laravel をインストールした場合は、オペレーティング システムの `php.new` インストール コマンドを再実行して、最新バージョンの PHP と Laravel インストーラーをインストールできます。

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

<!-- Or, if you are using [Laravel Herd's](https://herd.laravel.com) bundled copy of the Laravel installer, you should update your Herd installation to the latest release. -->
または、Laravel インストーラーの [Laravel Herd's](https://herd.laravel.com) バンドル コピーを使用している場合は、Herd インストールを最新リリースに更新する必要があります。

<a name="authentication"></a>
<!-- ### Authentication -->
### Authentication

<a name="updated-databasetokenrepository-constructor-signature"></a>
<!-- #### Updated `DatabaseTokenRepository` Constructor Signature -->
#### Updated `DatabaseTokenRepository` Constructor Signature

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The constructor of the `Illuminate\Auth\Passwords\DatabaseTokenRepository` class now expects the `$expires` parameter to be given in seconds, rather than minutes. -->
`Illuminate\Auth\Passwords\DatabaseTokenRepository` クラスのコンストラクターは、`$expires` パラメーターが分ではなく秒で指定されることを期待するようになりました。

<a name="concurrency"></a>
<!-- ### Concurrency -->
### Concurrency

<a name="concurrency-result-index-mapping"></a>
<!-- #### Concurrency Result Index Mapping -->
#### Concurrency Result Index Mapping

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- When invoking the `Concurrency::run` method with an associative array, the results of the concurrent operations are now returned with their associated keys: -->
連想配列を使用して `Concurrency::run` メソッドを呼び出すと、同時操作の結果が関連付けられたキーとともに返されるようになりました。

```php
$result = Concurrency::run([
    'task-1' => fn () => 1 + 1,
    'task-2' => fn () => 2 + 2,
]);

// ['task-1' => 2, 'task-2' => 4]
```

<a name="container"></a>
<!-- ### Container -->
### Container

<a name="container-class-dependency-resolution"></a>
<!-- #### Container Class Dependency Resolution -->
#### Container Class Dependency Resolution

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The dependency injection container now respects the default value of class properties when resolving a class instance. If you were previously relying on the container to resolve a class instance without the default value, you may need to adjust your application to account for this new behavior: -->
依存注入コンテナーは、クラス インスタンスを解決するときにクラス プロパティのデフォルト値を尊重するようになりました。以前にデフォルト値を使用せずにクラス インスタンスを解決するためにコンテナに依存していた場合は、この新しい動作を考慮してアプリケーションを調整する必要がある場合があります。

```php
class Example
{
    public function __construct(public ?Carbon $date = null) {}
}

$example = resolve(Example::class);

// <= 11.x
$example->date instanceof Carbon;

// >= 12.x
$example->date === null;
```

<a name="database"></a>
<!-- ### Database -->
### Database

<a name="multi-schema-database-inspecting"></a>
<!-- #### Multi-Schema Database Inspecting -->
#### Multi-Schema Database Inspecting

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `Schema::getTables()`, `Schema::getViews()`, and `Schema::getTypes()` methods now include the results from all schemas by default. You may pass the `schema` argument to retrieve the result for the given schema only: -->
`Schema::getTables()`、`Schema::getViews()`、および `Schema::getTypes()` メソッドには、デフォルトですべてのスキーマの結果が含まれるようになりました。 `schema` 引数を渡して、指定されたスキーマのみの結果を取得できます。

```php
// All tables on all schemas...
$tables = Schema::getTables();

// All tables on the 'main' schema...
$tables = Schema::getTables(schema: 'main');

// All tables on the 'main' and 'blog' schemas...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

<!-- The `Schema::getTableListing()` method now returns schema-qualified table names by default. You may pass the `schemaQualified` argument to change the behavior as desired: -->
`Schema::getTableListing()` メソッドは、デフォルトでスキーマ修飾されたテーブル名を返すようになりました。 `schemaQualified` 引数を渡して、必要に応じて動作を変更できます。

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

<!-- The `db:table` and `db:show` commands now output the results of all schemas on MySQL, MariaDB, and SQLite, just like PostgreSQL and SQL Server. -->
`db:table` および `db:show` コマンドは、PostgreSQL や SQL Server と同様に、MySQL、MariaDB、SQLite 上のすべてのスキーマの結果を出力するようになりました。

<a name="database-constructor-signature-changes"></a>
<!-- #### Database Constructor Signature Changes -->
#### Database Constructor Signature Changes

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- In Laravel 12, several low-level database classes now require an `Illuminate\Database\Connection` instance to be provided via their constructors. -->
Laravel 12 では、いくつかの低レベルのデータベース クラスで、コンストラクターを介して `Illuminate\Database\Connection` インスタンスを提供する必要があります。

<!-- **These changes are primarily applicable to database package maintainers - it is extremely unlikely any of these changes affect normal application development.** -->
**これらの変更は主にデータベース パッケージの管理者に適用されます。これらの変更が通常のアプリケーション開発に影響を与える可能性はほとんどありません。**

<!-- `Illuminate\Database\Schema\Blueprint` -->
`Illuminate\Database\Schema\Blueprint`

<!-- The constructor of the `Illuminate\Database\Schema\Blueprint` class now expects a `Connection` instance as its first argument. This primarily affects applications or packages that manually instantiate `Blueprint` instances. -->
`Illuminate\Database\Schema\Blueprint` クラスのコンストラクターは、最初の引数として `Connection` インスタンスを期待するようになりました。これは主に、`Blueprint` インスタンスを手動でインスタンス化するアプリケーションまたはパッケージに影響します。

<!-- `Illuminate\Database\Grammar` -->
`Illuminate\Database\Grammar`

<!-- The constructor of the `Illuminate\Database\Grammar` class also now requires a `Connection` instance. In previous versions, the connection was assigned after construction using the `setConnection()` method. This method has been removed in Laravel 12: -->
`Illuminate\Database\Grammar` クラスのコンストラクターには、`Connection` インスタンスも必要になりました。以前のバージョンでは、接続は構築後に `setConnection()` メソッドを使用して割り当てられていました。このメソッドは Laravel 12 では削除されました。

```php
// Laravel <= 11.x
$grammar = new MySqlGrammar;
$grammar->setConnection($connection);

// Laravel >= 12.x
$grammar = new MySqlGrammar($connection);
````

<!-- In addition, the following APIs have been removed or deprecated: -->
さらに、次の API が削除または非推奨になりました。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The `Blueprint::getPrefix()` method is deprecated.
- The `Connection::withTablePrefix()` method has been removed.
- The `Grammar::getTablePrefix()` and `setTablePrefix()` methods are deprecated.
- The `Grammar::setConnection()` method has been removed.
-->
- `Blueprint::getPrefix()` メソッドは非推奨になりました。
- `Connection::withTablePrefix()` メソッドは削除されました。
- `Grammar::getTablePrefix()` メソッドと `setTablePrefix()` メソッドは非推奨になりました。
- `Grammar::setConnection()` メソッドは削除されました。

<!-- </div> -->
</div>

<!-- When working with table prefixes, you should now retrieve them directly from the database connection: -->
テーブルの接頭辞を操作する場合は、データベース接続から直接接頭辞を取得する必要があります。

```php
$prefix = $connection->getTablePrefix();
```

<!-- If you maintain custom database drivers, schema builders, or grammar implementations, you should review their constructors and ensure a `Connection` instance is provided. -->
カスタム データベース ドライバ、スキーマ ビルダ、または文法実装を保守する場合は、それらのコンストラクターを確認し、`Connection` インスタンスが提供されていることを確認する必要があります。

<a name="eloquent"></a>
<!-- ### Eloquent -->
### Eloquent

<a name="models-and-uuidv7"></a>
<!-- #### Models and UUIDv7 -->
#### Models and UUIDv7

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The `HasUuids` trait now returns UUIDs that are compatible with version 7 of the UUID spec (ordered UUIDs). If you would like to continue using ordered UUIDv4 strings for your model's IDs, you should now use the `HasVersion4Uuids` trait: -->
`HasUuids` トレイトは、UUID 仕様のバージョン 7 と互換性のある UUID (順序付けされた UUID) を返すようになりました。モデルの ID に順序付けされた UUIDv4 文字列を引き続き使用したい場合は、`HasVersion4Uuids` 特性を使用する必要があります。

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

<!-- The `HasVersion7Uuids` trait has been removed. If you were previously using this trait, you should use the `HasUuids` trait instead, which now provides the same behavior. -->
`HasVersion7Uuids` 特性は削除されました。以前にこの特性を使用していた場合は、代わりに `HasUuids` 特性を使用する必要があります。これにより、同じ動作が提供されるようになります。

<a name="requests"></a>
<!-- ### Requests -->
### Requests

<a name="nested-array-request-merging"></a>
<!-- #### Nested Array Request Merging -->
#### Nested Array Request Merging

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `$request->mergeIfMissing()` method now allows merging nested array data using "dot" notation. If you were previously relying on this method to create a top-level array key containing the "dot" notation version of the key, you may need to adjust your application to account for this new behavior: -->
`$request->mergeIfMissing()` メソッドでは、「ドット」表記を使用してネストされた配列データをマージできるようになりました。以前にこのメソッドを使用して、キーの「ドット」表記バージョンを含む最上位の配列キーを作成していた場合は、この新しい動作を考慮してアプリケーションを調整する必要がある場合があります。

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<a name="route-precedence"></a>
<!-- #### Route Precedence -->
#### Route Precedence

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The routing behavior when multiple routes have the same name has been unified between cached and uncached routing. This means that uncached routing now matches the first route registered with a given name instead of the last one. -->
複数のルートが同じ名前を持つ場合のルーティング動作は、キャッシュされたルーティングとキャッシュされていないルーティングの間で統合されました。これは、キャッシュされていないルーティングが、最後のルートではなく、指定された名前で登録された最初のルートと一致することを意味します。

<a name="storage"></a>
<!-- ### Storage -->
### Storage

<a name="local-filesystem-disk-default-root-path"></a>
<!-- #### Local Filesystem Disk Default Root Path -->
#### Local Filesystem Disk Default Root Path

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- If your application does not explicitly define a `local` disk in your filesystems configuration, Laravel will now default the local disk's root to `storage/app/private`. In previous releases, this defaulted to `storage/app`. As a result, calls to `Storage::disk('local')` will read from and write to `storage/app/private` unless otherwise configured. To restore the previous behavior, you may define the `local` disk manually and set the desired root path. -->
アプリケーションがファイルシステム構成で `local` ディスクを明示的に定義していない場合、Laravel はローカル ディスクのルートをデフォルトで `storage/app/private` に設定します。以前のリリースでは、これはデフォルトで `storage/app` でした。その結果、別途設定されていない限り、`Storage::disk('local')` への呼び出しは `storage/app/private` との間で読み取りおよび書き込みを行います。以前の動作を復元するには、`local` ディスクを手動で定義し、目的のルート パスを設定します。

<a name="validation"></a>
<!-- ### Validation -->
### Validation

<a name="image-validation"></a>
<!-- #### Image Validation Now Excludes SVGs -->
#### Image Validation Now Excludes SVGs

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `image` validation rule no longer allows SVG images by default. If you would like to allow SVGs when using the `image` rule, you must explicitly allow them: -->
`image` 検証ルールでは、デフォルトで SVG 画像が許可されなくなりました。 `image` ルールの使用時に SVG を許可したい場合は、明示的に許可する必要があります。

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// Or...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/11.x...12.x) and choose which updates are important to you. -->
`laravel/laravel` [GitHub repository](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。 [GitHub comparison tool](https://github.com/laravel/laravel/compare/11.x...12.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。

