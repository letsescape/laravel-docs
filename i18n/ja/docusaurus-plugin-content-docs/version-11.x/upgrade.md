<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading To 11.0 From 10.x](#upgrade-11.0)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Application Structure](#application-structure)
- [Floating-Point Types](#floating-point-types)
- [Modifying Columns](#modifying-columns)
- [SQLite Minimum Version](#sqlite-minimum-version)
- [Updating Sanctum](#updating-sanctum)

<!-- </div> -->
</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [Password Rehashing](#password-rehashing)
- [Per-Second Rate Limiting](#per-second-rate-limiting)
- [Spatie Once Package](#spatie-once-package)

<!-- </div> -->
</div>

<a name="low-impact-changes"></a>
<!-- ## Low Impact Changes -->
## Low Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Doctrine DBAL Removal](#doctrine-dbal-removal)
- [Eloquent Model `casts` Method](#eloquent-model-casts-method)
- [Spatial Types](#spatial-types)
- [The `Enumerable` Contract](#the-enumerable-contract)
- [The `UserProvider` Contract](#the-user-provider-contract)
- [The `Authenticatable` Contract](#the-authenticatable-contract)

<!-- </div> -->
</div>

<a name="upgrade-11.0"></a>
<!-- ## Upgrading To 11.0 From 10.x -->
## Upgrading To 11.0 From 10.x

<a name="estimated-upgrade-time-??-minutes"></a>
<!-- #### Estimated Upgrade Time: 15 Minutes -->
#### Estimated Upgrade Time: 15 Minutes

> [!NOTE]
> 私たちは、考えられるすべての重大な変更を文書化するよう努めます。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。時間を節約したいですか? [Laravel Shift](https://laravelshift.com/) を使用すると、アプリケーションのアップグレードを自動化できます。

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- #### PHP 8.2.0 Required -->
#### PHP 8.2.0 Required

<!-- Laravel now requires PHP 8.2.0 or greater. -->
Laravel には PHP 8.2.0 以降が必要になりました。

<!-- #### curl 7.34.0 Required -->
#### curl 7.34.0 Required

<!-- Laravel's HTTP client now requires curl 7.34.0 or greater. -->
Laravel の HTTP クライアントには、curl 7.34.0 以降が必要になりました。

<!-- #### Composer Dependencies -->
#### Composer Dependencies

<!-- You should update the following dependencies in your application's `composer.json` file: -->
アプリケーションの `composer.json` ファイル内の次の依存関係を更新する必要があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `laravel/framework` to `^11.0`
- `nunomaduro/collision` to `^8.1`
- `laravel/breeze` to `^2.0` (If installed)
- `laravel/cashier` to `^15.0` (If installed)
- `laravel/dusk` to `^8.0` (If installed)
- `laravel/jetstream` to `^5.0` (If installed)
- `laravel/octane` to `^2.3` (If installed)
- `laravel/passport` to `^12.0` (If installed)
- `laravel/sanctum` to `^4.0` (If installed)
- `laravel/scout` to `^10.0` (If installed)
- `laravel/spark-stripe` to `^5.0` (If installed)
- `laravel/telescope` to `^5.0` (If installed)
- `livewire/livewire` to `^3.4` (If installed)
- `inertiajs/inertia-laravel` to `^1.0` (If installed)
-->
- `laravel/framework` ～ `^11.0`
- `nunomaduro/collision` ～ `^8.1`
- `laravel/breeze` ～ `^2.0` (インストールされている場合)
- `laravel/cashier` ～ `^15.0` (インストールされている場合)
- `laravel/dusk` ～ `^8.0` (インストールされている場合)
- `laravel/jetstream` ～ `^5.0` (インストールされている場合)
- `laravel/octane` ～ `^2.3` (インストールされている場合)
- `laravel/passport` ～ `^12.0` (インストールされている場合)
- `laravel/sanctum` ～ `^4.0` (インストールされている場合)
- `laravel/scout` ～ `^10.0` (インストールされている場合)
- `laravel/spark-stripe` ～ `^5.0` (インストールされている場合)
- `laravel/telescope` ～ `^5.0` (インストールされている場合)
- `livewire/livewire` ～ `^3.4` (インストールされている場合)
- `inertiajs/inertia-laravel` ～ `^1.0` (インストールされている場合)

<!-- </div> -->
</div>

<!-- If your application is using Laravel Cashier Stripe, Passport, Sanctum, Spark Stripe, or Telescope, you will need to publish their migrations to your application. Cashier Stripe, Passport, Sanctum, Spark Stripe, and Telescope **no longer automatically load migrations from their own migrations** directory. Therefore, you should run the following command to publish their migrations to your application: -->
アプリケーションが Laravel Cashier Stripe、Passport、Sanctum、Spark Stripe、または Telescope を使用している場合は、それらの移行をアプリケーションに公開する必要があります。 Cashier Stripe、Passport、Sanctum、Spark Stripe、および Telescope は、**独自の移行ディレクトリから移行を自動的にロードしなくなりました**。したがって、次のコマンドを実行して、移行をアプリケーションに公開する必要があります。

```bash
php artisan vendor:publish --tag=cashier-migrations
php artisan vendor:publish --tag=passport-migrations
php artisan vendor:publish --tag=sanctum-migrations
php artisan vendor:publish --tag=spark-migrations
php artisan vendor:publish --tag=telescope-migrations
```

<!-- In addition, you should review the upgrade guides for each of these packages to ensure you are aware of any additional breaking changes: -->
さらに、これらの各パッケージのアップグレード ガイドを参照して、追加の重大な変更を確認してください。

- [Laravel Cashier Stripe](#cashier-stripe)
- [Laravel Passport](#passport)
- [Laravel Sanctum](#sanctum)
- [Laravel Spark Stripe](#spark-stripe)
- [Laravel Telescope](#telescope)

<!-- If you have manually installed the Laravel installer, you should update the installer via Composer: -->
Laravel インストーラーを手動でインストールした場合は、Composer 経由でインストーラーを更新する必要があります。

```bash
composer global require laravel/installer:^5.6
```

<!-- Finally, you may remove the `doctrine/dbal` Composer dependency if you have previously added it to your application, as Laravel is no longer dependent on this package. -->
最後に、Laravel はこのパッケージに依存しなくなったため、以前にアプリケーションに `doctrine/dbal` Composer 依存関係を追加していた場合は、それを削除できます。

<a name="application-structure"></a>
<!-- ### Application Structure -->
### Application Structure

<!-- Laravel 11 introduces a new default application structure with fewer default files. Namely, new Laravel applications contain fewer service providers, middleware, and configuration files. -->
Laravel 11 では、デフォルトのファイルが減った新しいデフォルトのアプリケーション構造が導入されています。つまり、新しい Laravel アプリケーションには、含まれるサービスプロバイダ、ミドルウェア、および構成ファイルが少なくなります。

<!-- However, we do **not recommend** that Laravel 10 applications upgrading to Laravel 11 attempt to migrate their application structure, as Laravel 11 has been carefully tuned to also support the Laravel 10 application structure. -->
ただし、Laravel 11 は Laravel 10 アプリケーション構造もサポートするように慎重に調整されているため、Laravel 10 アプリケーションを Laravel 11 にアップグレードする際にアプリケーション構造を移行しようとすることは**お勧めしません**。

<a name="authentication"></a>
<!-- ### Authentication -->
### Authentication

<a name="password-rehashing"></a>
<!-- #### Password Rehashing -->
#### Password Rehashing

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Laravel 11 will automatically rehash your user's passwords during authentication if your hashing algorithm's "work factor" has been updated since the password was last hashed. -->
Laravel 11は、パスワードが最後にハッシュされてからハッシュアルゴリズムの「作業係数」が更新されている場合、認証中にユーザーのパスワードを自動的に再ハッシュします。

<!-- Typically, this should not disrupt your application; however, if your `User` model's "password" field has a name other than `password`, you should specify the field's name via the model's `authPasswordName` property: -->
通常、これによってアプリケーションが中断されることはありません。ただし、`User` モデルの「パスワード」フィールドに `password` 以外の名前がある場合は、モデルの `authPasswordName` プロパティを使用してフィールドの名前を指定する必要があります。

```
protected $authPasswordName = 'custom_password_field';
```

<!-- Alternatively, you may disable password rehashing by adding the `rehash_on_login` option to your application's `config/hashing.php` configuration file: -->
あるいは、アプリケーションの `config/hashing.php` 構成ファイルに `rehash_on_login` オプションを追加して、パスワードの再ハッシュを無効にすることもできます。

```
'rehash_on_login' => false,
```

<a name="the-user-provider-contract"></a>
<!-- #### The `UserProvider` Contract -->
#### The `UserProvider` Contract

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `Illuminate\Contracts\Auth\UserProvider` contract has received a new `rehashPasswordIfRequired` method. This method is responsible for re-hashing and storing the user's password in storage when the application's hashing algorithm work factor has changed. -->
`Illuminate\Contracts\Auth\UserProvider` コントラクトは、新しい `rehashPasswordIfRequired` メソッドを受け取りました。このメソッドは、アプリケーションのハッシュ アルゴリズムの作業係数が変更されたときに、ユーザーのパスワードを再ハッシュしてストレージに保存する役割を果たします。

<!-- If your application or package defines a class that implements this interface, you should add the new `rehashPasswordIfRequired` method to your implementation. A reference implementation can be found within the `Illuminate\Auth\EloquentUserProvider` class: -->
アプリケーションまたはパッケージがこのインターフェイスを実装するクラスを定義している場合は、新しい `rehashPasswordIfRequired` メソッドを実装に追加する必要があります。参照実装は、`Illuminate\Auth\EloquentUserProvider` クラス内にあります。

```php
public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
```

<a name="the-authenticatable-contract"></a>
<!-- #### The `Authenticatable` Contract -->
#### The `Authenticatable` Contract

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `Illuminate\Contracts\Auth\Authenticatable` contract has received a new `getAuthPasswordName` method. This method is responsible for returning the name of your authenticatable entity's password column. -->
`Illuminate\Contracts\Auth\Authenticatable` コントラクトは、新しい `getAuthPasswordName` メソッドを受け取りました。このメソッドは、認証可能なエンティティのパスワード列の名前を返す役割を果たします。

<!-- If your application or package defines a class that implements this interface, you should add the new `getAuthPasswordName` method to your implementation: -->
アプリケーションまたはパッケージがこのインターフェイスを実装するクラスを定義している場合は、新しい `getAuthPasswordName` メソッドを実装に追加する必要があります。

```php
public function getAuthPasswordName()
{
    return 'password';
}
```

<!-- The default `User` model included with Laravel receives this method automatically since the method is included within the `Illuminate\Auth\Authenticatable` trait. -->
Laravel に含まれるデフォルトの `User` モデルは、メソッドが `Illuminate\Auth\Authenticatable` トレイト内に含まれているため、このメソッドを自動的に受け取ります。

<a name="the-authentication-exception-class"></a>
<!-- #### The `AuthenticationException` Class -->
#### The `AuthenticationException` Class

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `redirectTo` method of the `Illuminate\Auth\AuthenticationException` class now requires an `Illuminate\Http\Request` instance as its first argument. If you are manually catching this exception and calling the `redirectTo` method, you should update your code accordingly: -->
`Illuminate\Auth\AuthenticationException` クラスの `redirectTo` メソッドには、最初の引数として `Illuminate\Http\Request` インスタンスが必要になりました。この例外を手動でキャッチして `redirectTo` メソッドを呼び出している場合は、それに応じてコードを更新する必要があります。

```php
if ($e instanceof AuthenticationException) {
    $path = $e->redirectTo($request);
}
```

<a name="email-verification-notification-on-registration"></a>
<!-- #### Email Verification Notification on Registration -->
#### Email Verification Notification on Registration

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `SendEmailVerificationNotification` listener is now automatically registered for the `Registered` event if it is not already registered by your application's `EventServiceProvider`. If your application's `EventServiceProvider` does not register this listener and you do not want Laravel to automatically register it for you, you should define an empty `configureEmailVerification` method in your application's `EventServiceProvider`: -->
`SendEmailVerificationNotification` リスナは、アプリケーションの `EventServiceProvider` によってまだ登録されていない場合、`Registered` イベントに自動的に登録されるようになりました。アプリケーションの `EventServiceProvider` がこのリスナを登録せず、Laravel に自動的に登録されたくない場合は、アプリケーションの `EventServiceProvider` で空の `configureEmailVerification` メソッドを定義する必要があります。

```php
protected function configureEmailVerification()
{
    // ...
}
```

<a name="cache"></a>
<!-- ### Cache -->
### Cache

<a name="cache-key-prefixes"></a>
<!-- #### Cache Key Prefixes -->
#### Cache Key Prefixes

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Previously, if a cache key prefix was defined for the DynamoDB, Memcached, or Redis cache stores, Laravel would append a `:` to the prefix. In Laravel 11, the cache key prefix does not receive the `:` suffix. If you would like to maintain the previous prefixing behavior, you can manually add the `:` suffix to your cache key prefix. -->
以前は、キャッシュキープレフィックスが DynamoDB、Memcached、または Redis キャッシュストアに定義されている場合、Laravel はプレフィックスに `:` を追加していました。 Laravel 11では、キャッシュキープレフィックスは`:`サフィックスを受け取りません。以前のプレフィックスの動作を維持したい場合は、キャッシュ キー プレフィックスに `:` サフィックスを手動で追加できます。

<a name="collections"></a>
<!-- ### Collections -->
### Collections

<a name="the-enumerable-contract"></a>
<!-- #### The `Enumerable` Contract -->
#### The `Enumerable` Contract

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `dump` method of the `Illuminate\Support\Enumerable` contract has been updated to accept a variadic `...$args` argument. If you are implementing this interface you should update your implementation accordingly: -->
`Illuminate\Support\Enumerable` コントラクトの `dump` メソッドが更新され、可変個の `...$args` 引数を受け入れるようになりました。このインターフェースを実装している場合は、それに応じて実装を更新する必要があります。

```php
public function dump(...$args);
```

<a name="database"></a>
<!-- ### Database -->
### Database

<a name="sqlite-minimum-version"></a>
<!-- #### SQLite 3.26.0+ -->
#### SQLite 3.26.0+

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- If your application is utilizing an SQLite database, SQLite 3.26.0 or greater is required. -->
アプリケーションが SQLite データベースを利用している場合は、SQLite 3.26.0 以降が必要です。

<a name="eloquent-model-casts-method"></a>
<!-- #### Eloquent Model `casts` Method -->
#### Eloquent Model `casts` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The base Eloquent model class now defines a `casts` method in order to support the definition of attribute casts. If one of your application's models is defining a `casts` relationship, it may conflict with the `casts` method now present on the base Eloquent model class. -->
基本 Eloquent モデル クラスは、attribute castingの定義をサポートするために、`casts` メソッドを定義するようになりました。アプリケーションのモデルの 1 つが `casts` 関係を定義している場合、基本 Eloquent モデル クラスに現在存在する `casts` メソッドと競合する可能性があります。

<a name="modifying-columns"></a>
<!-- #### Modifying Columns -->
#### Modifying Columns

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- When modifying a column, you must now explicitly include all the modifiers you want to keep on the column definition after it is changed. Any missing attributes will be dropped. For example, to retain the `unsigned`, `default`, and `comment` attributes, you must call each modifier explicitly when changing the column, even if those attributes have been assigned to the column by a previous migration. -->
列を変更する場合、変更後に列定義に保持したいすべての修飾子を明示的に含める必要があります。欠落している属性は削除されます。たとえば、`unsigned`、`default`、および `comment` 属性を保持するには、これらの属性が以前の移行によって列に割り当てられていたとしても、列を変更するときに各修飾子を明示的に呼び出す必要があります。

<!-- For example, imagine you have a migration that creates a `votes` column with the `unsigned`, `default`, and `comment` attributes: -->
たとえば、`unsigned`、`default`、および `comment` 属性を持つ `votes` 列を作成する移行があると想像してください。

```php
Schema::create('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('The vote count');
});
```

<!-- Later, you write a migration that changes the column to be `nullable` as well: -->
後で、列を `nullable` に変更する移行を作成します。

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->nullable()->change();
});
```

<!-- In Laravel 10, this migration would retain the `unsigned`, `default`, and `comment` attributes on the column. However, in Laravel 11, the migration must now also include all of the attributes that were previously defined on the column. Otherwise, they will be dropped: -->
Laravel 10 では、この移行により列の `unsigned`、`default`、および `comment` 属性が保持されます。ただし、Laravel 11 では、以前に列に定義されていたすべての属性も移行に含める必要があります。それ以外の場合、それらはドロップされます。

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')
        ->unsigned()
        ->default(1)
        ->comment('The vote count')
        ->nullable()
        ->change();
});
```

<!-- The `change` method does not change the indexes of the column. Therefore, you may use index modifiers to explicitly add or drop an index when modifying the column: -->
`change` メソッドは列のインデックスを変更しません。したがって、列を変更するときにインデックス修飾子を使用してインデックスを明示的に追加または削除できます。

```php
// Add an index...
$table->bigIncrements('id')->primary()->change();

// Drop an index...
$table->char('postal_code', 10)->unique(false)->change();
```

<!-- If you do not want to update all of the existing "change" migrations in your application to retain the column's existing attributes, you may simply [squash your migrations](/docs/11.x/migrations#squashing-migrations): -->
列の既存の属性を保持するためにアプリケーション内の既存の「変更」移行をすべて更新したくない場合は、単純に [squash your migrations](/docs/11.x/migrations#squashing-migrations) を実行します。

```bash
php artisan schema:dump
```

<!-- Once your migrations have been squashed, Laravel will "migrate" the database using your application's schema file before running any pending migrations. -->
移行が中断されると、Laravel は保留中の移行を実行する前に、アプリケーションのスキーマ ファイルを使用してデータベースを「移行」します。

<a name="floating-point-types"></a>
<!-- #### Floating-Point Types -->
#### Floating-Point Types

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- The `double` and `float` migration column types have been rewritten to be consistent across all databases. -->
`double` および `float` 移行列タイプは、すべてのデータベースで一貫性があるように書き直されました。

<!-- The `double` column type now creates a `DOUBLE` equivalent column without total digits and places (digits after decimal point), which is the standard SQL syntax. Therefore, you may remove the arguments for `$total` and `$places`: -->
`double` 列タイプは、標準 SQL 構文である合計桁数と桁数 (小数点以下の桁数) を持たない `DOUBLE` と同等の列を作成するようになりました。したがって、`$total` および `$places` の引数を削除できます。

```php
$table->double('amount');
```

<!-- The `float` column type now creates a `FLOAT` equivalent column without total digits and places (digits after decimal point), but with an optional `$precision` specification to determine storage size as a 4-byte single-precision column or an 8-byte double-precision column. Therefore, you may remove the arguments for `$total` and `$places` and specify the optional `$precision` to your desired value and according to your database's documentation: -->
`float` 列タイプは、合計桁数と桁数 (小数点以下の桁数) を持たない `FLOAT` と同等の列を作成するようになりましたが、ストレージ サイズを 4 バイトの単精度列または 8 バイトの倍精度列として決定するオプションの `$precision` 仕様を使用します。したがって、データベースのドキュメントに従って、`$total` および `$places` の引数を削除し、オプションの `$precision` を希望の値に指定できます。

```php
$table->float('amount', precision: 53);
```

<!-- The `unsignedDecimal`, `unsignedDouble`, and `unsignedFloat` methods have been removed, as the unsigned modifier for these column types has been deprecated by MySQL, and was never standardized on other database systems. However, if you wish to continue using the deprecated unsigned attribute for these column types, you may chain the `unsigned` method onto the column's definition: -->
`unsignedDecimal`、`unsignedDouble`、および `unsignedFloat` メソッドは、これらの列タイプの unsigned 修飾子が MySQL で非推奨になり、他のデータベース システムでは標準化されなかったため、削除されました。ただし、これらの列タイプに対して非推奨の unsigned 属性を引き続き使用したい場合は、`unsigned` メソッドを列の定義に連鎖させることができます。

```php
$table->decimal('amount', total: 8, places: 2)->unsigned();
$table->double('amount')->unsigned();
$table->float('amount', precision: 53)->unsigned();
```

<a name="dedicated-mariadb-driver"></a>
<!-- #### Dedicated MariaDB Driver -->
#### Dedicated MariaDB Driver

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Instead of always utilizing the MySQL driver when connecting to MariaDB databases, Laravel 11 adds a dedicated database driver for MariaDB. -->
MariaDB データベースに接続するときに常に MySQL ドライバを使用するのではなく、Laravel 11 では MariaDB 専用のデータベース ドライバを追加します。

<!-- If your application connects to a MariaDB database, you may update the connection configuration to the new `mariadb` driver to benefit from MariaDB specific features in the future: -->
アプリケーションが MariaDB データベースに接続する場合、接続構成を新しい `mariadb` ドライバに更新すると、将来的に MariaDB 固有の機能を利用できるようになります。

```
'driver' => 'mariadb',
'url' => env('DB_URL'),
'host' => env('DB_HOST', '127.0.0.1'),
'port' => env('DB_PORT', '3306'),
// ...
```

<!-- Currently, the new MariaDB driver behaves like the current MySQL driver with one exception: the `uuid` schema builder method creates native UUID columns instead of `char(36)` columns. -->
現在、新しい MariaDB ドライバは、1 つの例外を除いて現在の MySQL ドライバと同様に動作します。それは、`uuid` スキーマ ビルダ メソッドが、`char(36)` 列の代わりにネイティブ UUID 列を作成することです。

<!-- If your existing migrations utilize the `uuid` schema builder method and you choose to use the new `mariadb` database driver, you should update your migration's invocations of the `uuid` method to `char` to avoid breaking changes or unexpected behavior: -->
既存の移行で `uuid` スキーマ ビルダ メソッドを利用し、新しい `mariadb` データベース ドライバの使用を選択した場合は、破壊的な変更や予期しない動作を避けるために、移行による `uuid` メソッドの呼び出しを `char` に更新する必要があります。

```php
Schema::table('users', function (Blueprint $table) {
    $table->char('uuid', 36);

    // ...
});
```

<a name="spatial-types"></a>
<!-- #### Spatial Types -->
#### Spatial Types

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The spatial column types of database migrations have been rewritten to be consistent across all databases. Therefore, you may remove `point`, `lineString`, `polygon`, `geometryCollection`, `multiPoint`, `multiLineString`, `multiPolygon`, and `multiPolygonZ` methods from your migrations and use `geometry` or `geography` methods instead: -->
データベース移行の空間列タイプは、すべてのデータベースで一貫性を保つように書き直されました。したがって、`point`、`lineString`、`polygon`、`geometryCollection`、`multiPoint`、`multiLineString`、`multiPolygon`、および `multiPolygonZ` メソッドを移行から削除し、`geometry` または代わりに `geography` メソッド:

```php
$table->geometry('shapes');
$table->geography('coordinates');
```

<!-- To explicitly restrict the type or the spatial reference system identifier for values stored in the column on MySQL, MariaDB, and PostgreSQL, you may pass the `subtype` and `srid` to the method: -->
MySQL、MariaDB、および PostgreSQL の列に格納される値の型または空間参照系識別子を明示的に制限するには、`subtype` および `srid` をメソッドに渡すことができます。

```php
$table->geometry('dimension', subtype: 'polygon', srid: 0);
$table->geography('latitude', subtype: 'point', srid: 4326);
```

<!-- The `isGeometry` and `projection` column modifiers of the PostgreSQL grammar have been removed accordingly. -->
これに応じて、PostgreSQL 文法の `isGeometry` 列修飾子と `projection` 列修飾子が削除されました。

<a name="doctrine-dbal-removal"></a>
<!-- #### Doctrine DBAL Removal -->
#### Doctrine DBAL Removal

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The following list of Doctrine DBAL related classes and methods have been removed. Laravel is no longer dependent on this package and registering custom Doctrines types is no longer necessary for the proper creation and alteration of various column types that previously required custom types: -->
以下の Doctrine DBAL 関連のクラスとメソッドのリストは削除されました。 Laravel はこのパッケージに依存しなくなり、以前はカスタム型が必要だったさまざまな列型を適切に作成および変更するために、カスタム Doctrines 型を登録する必要がなくなりました。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `Illuminate\Database\Schema\Builder::$alwaysUsesNativeSchemaOperationsIfPossible` class property
- `Illuminate\Database\Schema\Builder::useNativeSchemaOperationsIfPossible()` method
- `Illuminate\Database\Connection::usingNativeSchemaOperations()` method
- `Illuminate\Database\Connection::isDoctrineAvailable()` method
- `Illuminate\Database\Connection::getDoctrineConnection()` method
- `Illuminate\Database\Connection::getDoctrineSchemaManager()` method
- `Illuminate\Database\Connection::getDoctrineColumn()` method
- `Illuminate\Database\Connection::registerDoctrineType()` method
- `Illuminate\Database\DatabaseManager::registerDoctrineType()` method
- `Illuminate\Database\PDO` directory
- `Illuminate\Database\DBAL\TimestampType` class
- `Illuminate\Database\Schema\Grammars\ChangeColumn` class
- `Illuminate\Database\Schema\Grammars\RenameColumn` class
- `Illuminate\Database\Schema\Grammars\Grammar::getDoctrineTableDiff()` method
-->
- `Illuminate\Database\Schema\Builder::$alwaysUsesNativeSchemaOperationsIfPossible` クラスのプロパティ
- `Illuminate\Database\Schema\Builder::useNativeSchemaOperationsIfPossible()`メソッド
- `Illuminate\Database\Connection::usingNativeSchemaOperations()`メソッド
- `Illuminate\Database\Connection::isDoctrineAvailable()`メソッド
- `Illuminate\Database\Connection::getDoctrineConnection()`メソッド
- `Illuminate\Database\Connection::getDoctrineSchemaManager()`メソッド
- `Illuminate\Database\Connection::getDoctrineColumn()`メソッド
- `Illuminate\Database\Connection::registerDoctrineType()`メソッド
- `Illuminate\Database\DatabaseManager::registerDoctrineType()`メソッド
- `Illuminate\Database\PDO` ディレクトリ
- `Illuminate\Database\DBAL\TimestampType`クラス
- `Illuminate\Database\Schema\Grammars\ChangeColumn`クラス
- `Illuminate\Database\Schema\Grammars\RenameColumn`クラス
- `Illuminate\Database\Schema\Grammars\Grammar::getDoctrineTableDiff()`メソッド

<!-- </div> -->
</div>

<!-- In addition, registering custom Doctrine types via `dbal.types` in your application's `database` configuration file is no longer required. -->
さらに、アプリケーションの `database` 設定ファイルで `dbal.types` を介してカスタム Doctrine タイプを登録する必要はなくなりました。

<!-- If you were previously using Doctrine DBAL to inspect your database and its associated tables, you may use Laravel's new native schema methods (`Schema::getTables()`, `Schema::getColumns()`, `Schema::getIndexes()`, `Schema::getForeignKeys()`, etc.) instead. -->
以前に Doctrine DBAL を使用してデータベースとその関連テーブルを検査していた場合は、代わりに Laravel の新しいネイティブ スキーマ メソッド (`Schema::getTables()`、`Schema::getColumns()`、`Schema::getIndexes()`、`Schema::getForeignKeys()` など) を使用できます。

<a name="deprecated-schema-methods"></a>
<!-- #### Deprecated Schema Methods -->
#### Deprecated Schema Methods

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The deprecated, Doctrine based `Schema::getAllTables()`, `Schema::getAllViews()`, and `Schema::getAllTypes()` methods have been removed in favor of new Laravel native `Schema::getTables()`, `Schema::getViews()`, and `Schema::getTypes()` methods. -->
非推奨の Doctrine ベースの `Schema::getAllTables()`、`Schema::getAllViews()`、および `Schema::getAllTypes()` メソッドは削除され、新しい Laravel ネイティブ `Schema::getTables()`、`Schema::getViews()`、および `Schema::getTypes()` メソッドが採用されました。

<!-- When using PostgreSQL and SQL Server, none of the new schema methods will accept a three-part reference (e.g. `database.schema.table`). Therefore, you should use `connection()` to declare the database instead: -->
PostgreSQL と SQL Server を使用する場合、新しいスキーマ メソッドはいずれも 3 部構成の参照 (`database.schema.table` など) を受け入れません。したがって、代わりに `connection()` を使用してデータベースを宣言する必要があります。

```php
Schema::connection('database')->hasTable('schema.table');
```

<a name="get-column-types"></a>
<!-- #### Schema Builder `getColumnType()` Method -->
#### Schema Builder `getColumnType()` Method

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Schema::getColumnType()` method now always returns actual type of the given column, not the Doctrine DBAL equivalent type. -->
`Schema::getColumnType()` メソッドは、Doctrine DBAL の同等の型ではなく、常に指定された列の実際の型を返すようになりました。

<a name="database-connection-interface"></a>
<!-- #### Database Connection Interface -->
#### Database Connection Interface

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Illuminate\Database\ConnectionInterface` interface has received a new `scalar` method. If you are defining your own implementation of this interface, you should add the `scalar` method to your implementation: -->
`Illuminate\Database\ConnectionInterface` インターフェイスは、新しい `scalar` メソッドを受け取りました。このインターフェースの独自の実装を定義している場合は、`scalar` メソッドを実装に追加する必要があります。

```php
public function scalar($query, $bindings = [], $useReadPdo = true);
```

<a name="dates"></a>
<!-- ### Dates -->
### Dates

<a name="carbon-3"></a>
<!-- #### Carbon 3 -->
#### Carbon 3

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- Laravel 11 supports both Carbon 2 and Carbon 3. Carbon is a date manipulation library utilized extensively by Laravel and packages throughout the ecosystem. If you upgrade to Carbon 3, be aware that `diffIn*` methods now return floating-point numbers and may return negative values to indicate time direction, which is a significant change from Carbon 2. Review Carbon's [change log](https://github.com/briannesbitt/Carbon/releases/tag/3.0.0) and [documentation](https://carbon.nesbot.com/guide/getting-started/migration.html) for detailed information on how to handle these and other changes. -->
Laravel 11 は、Carbon 2 と Carbon 3 の両方をサポートしています。Carbon は、Laravel とエコシステム全体のパッケージによって広く利用されている日付操作ライブラリです。 Carbon 3 にアップグレードする場合は、`diffIn*` メソッドが浮動小数点数を返すようになり、時間方向を示すために負の値を返す可能性があることに注意してください。これは、Carbon 2 からの大きな変更点です。これらの変更およびその他の変更の処理方法の詳細については、Carbon の [change log](https://github.com/briannesbitt/Carbon/releases/tag/3.0.0) および [documentation](https://carbon.nesbot.com/guide/getting-started/migration.html) を確認してください。

<a name="mail"></a>
<!-- ### Mail -->
### Mail

<a name="the-mailer-contract"></a>
<!-- #### The `Mailer` Contract -->
#### The `Mailer` Contract

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Illuminate\Contracts\Mail\Mailer` contract has received a new `sendNow` method. If your application or package is manually implementing this contract, you should add the new `sendNow` method to your implementation: -->
`Illuminate\Contracts\Mail\Mailer` コントラクトは、新しい `sendNow` メソッドを受け取りました。アプリケーションまたはパッケージがこのコントラクトを手動で実装している場合は、新しい `sendNow` メソッドを実装に追加する必要があります。

```php
public function sendNow($mailable, array $data = [], $callback = null);
```

<a name="packages"></a>
<!-- ### Packages -->
### Packages

<a name="publishing-service-providers"></a>
<!-- #### Publishing Service Providers to the Application -->
#### Publishing Service Providers to the Application

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- If you have written a Laravel package that manually publishes a service provider to the application's `app/Providers` directory and manually modifies the application's `config/app.php` configuration file to register the service provider, you should update your package to utilize the new `ServiceProvider::addProviderToBootstrapFile` method. -->
サービスプロバイダをアプリケーションの `app/Providers` ディレクトリに手動で公開し、アプリケーションの `config/app.php` 構成ファイルを手動で変更してサービスプロバイダを登録する Laravel パッケージを作成した場合は、新しい `ServiceProvider::addProviderToBootstrapFile` メソッドを利用するようにパッケージを更新する必要があります。

<!-- The `addProviderToBootstrapFile` method will automatically add the service provider you have published to the application's `bootstrap/providers.php` file, since the `providers` array does not exist within the `config/app.php` configuration file in new Laravel 11 applications. -->
新しい Laravel 11 アプリケーションの `config/app.php` 構成ファイル内に `providers` 配列が存在しないため、`addProviderToBootstrapFile` メソッドは、公開したサービスプロバイダをアプリケーションの `bootstrap/providers.php` ファイルに自動的に追加します。

```php
use Illuminate\Support\ServiceProvider;

ServiceProvider::addProviderToBootstrapFile(Provider::class);
```

<a name="queues"></a>
<!-- ### Queues -->
### Queues

<a name="the-batch-repository-interface"></a>
<!-- #### The `BatchRepository` Interface -->
#### The `BatchRepository` Interface

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Illuminate\Bus\BatchRepository` interface has received a new `rollBack` method. If you are implementing this interface within your own package or application, you should add this method to your implementation: -->
`Illuminate\Bus\BatchRepository` インターフェイスは、新しい `rollBack` メソッドを受け取りました。このインターフェイスを独自のパッケージまたはアプリケーション内に実装している場合は、このメソッドを実装に追加する必要があります。

```php
public function rollBack();
```

<a name="synchronous-jobs-in-database-transactions"></a>
<!-- #### Synchronous Jobs in Database Transactions -->
#### Synchronous Jobs in Database Transactions

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Previously, synchronous jobs (jobs using the `sync` queue driver) would execute immediately, regardless of whether the `after_commit` configuration option of the queue connection was set to `true` or the `afterCommit` method was invoked on the job. -->
以前は、キュー接続の `after_commit` 構成オプションが `true` に設定されているか、ジョブで `afterCommit` メソッドが呼び出されたかに関係なく、同期ジョブ (`sync` キュー ドライバを使用するジョブ) がすぐに実行されました。

<!-- In Laravel 11, synchronous queue jobs will now respect the "after commit" configuration of the queue connection or job. -->
Laravel 11では、同期キュージョブはキュー接続またはジョブの「コミット後」設定を尊重するようになりました。

<a name="rate-limiting"></a>
<!-- ### Rate Limiting -->
### Rate Limiting

<a name="per-second-rate-limiting"></a>
<!-- #### Per-Second Rate Limiting -->
#### Per-Second Rate Limiting

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- Laravel 11 supports per-second rate limiting instead of being limited to per-minute granularity. There are a variety of potential breaking changes you should be aware of related to this change. -->
Laravel 11 は、分単位の粒度に制限されるのではなく、秒単位のレート制限をサポートします。この変更に関連して、注意が必要な重大な変更がさまざまに存在する可能性があります。

<!-- The `GlobalLimit` class constructor now accepts seconds instead of minutes. This class is not documented and would not typically be used by your application: -->
`GlobalLimit` クラス コンストラクターは、分の代わりに秒を受け入れるようになりました。このクラスは文書化されていないため、通常はアプリケーションでは使用されません。

```php
new GlobalLimit($attempts, 2 * 60);
```

<!-- The `Limit` class constructor now accepts seconds instead of minutes. All documented usages of this class are limited to static constructors such as `Limit::perMinute` and `Limit::perSecond`. However, if you are instantiating this class manually, you should update your application to provide seconds to the class's constructor: -->
`Limit` クラス コンストラクターは、分の代わりに秒を受け入れるようになりました。このクラスの文書化された使用法はすべて、`Limit::perMinute` や `Limit::perSecond` などの静的コンストラクターに限定されています。ただし、このクラスを手動でインスタンス化する場合は、クラスのコンストラクターに秒を提供するようにアプリケーションを更新する必要があります。

```php
new Limit($key, $attempts, 2 * 60);
```

<!-- The `Limit` class's `decayMinutes` property has been renamed to `decaySeconds` and now contains seconds instead of minutes. -->
`Limit` クラスの `decayMinutes` プロパティの名前が `decaySeconds` に変更され、分の代わりに秒が含まれるようになりました。

<!-- The `Illuminate\Queue\Middleware\ThrottlesExceptions` and `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` class constructors now accept seconds instead of minutes: -->
`Illuminate\Queue\Middleware\ThrottlesExceptions` クラス コンストラクターと `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` クラス コンストラクターは、分の代わりに秒を受け入れるようになりました。

```php
new ThrottlesExceptions($attempts, 2 * 60);
new ThrottlesExceptionsWithRedis($attempts, 2 * 60);
```

<a name="cashier-stripe"></a>
<!-- ### Cashier Stripe -->
### Cashier Stripe

<a name="updating-cashier-stripe"></a>
<!-- #### Updating Cashier Stripe -->
#### Updating Cashier Stripe

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- Laravel 11 no longer supports Cashier Stripe 14.x. Therefore, you should update your application's Laravel Cashier Stripe dependency to `^15.0` in your `composer.json` file. -->
Laravel 11 は Cashier Stripe 14.x をサポートしなくなりました。したがって、アプリケーションの Laravel Cashier Stripe 依存関係を、`composer.json` ファイル内の `^15.0` に更新する必要があります。

<!-- Cashier Stripe 15.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Cashier Stripe's migrations to your application: -->
Cashier Stripe 15.0 は、独自の移行ディレクトリから移行を自動的にロードしなくなりました。代わりに、次のコマンドを実行して、Cashier Stripe の移行をアプリケーションに公開する必要があります。

```shell
php artisan vendor:publish --tag=cashier-migrations
```

<!-- Please review the complete [Cashier Stripe upgrade guide](https://github.com/laravel/cashier-stripe/blob/15.x/UPGRADE.md) for additional breaking changes. -->
その他の重大な変更については、完全な [Cashier Stripe upgrade guide](https://github.com/laravel/cashier-stripe/blob/15.x/UPGRADE.md) を確認してください。

<a name="spark-stripe"></a>
<!-- ### Spark (Stripe) -->
### Spark (Stripe)

<a name="updating-spark-stripe"></a>
<!-- #### Updating Spark Stripe -->
#### Updating Spark Stripe

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- Laravel 11 no longer supports Laravel Spark Stripe 4.x. Therefore, you should update your application's Laravel Spark Stripe dependency to `^5.0` in your `composer.json` file. -->
Laravel 11 は Laravel Spark Stripe 4.x をサポートしなくなりました。したがって、アプリケーションの Laravel Spark Stripe 依存関係を、`composer.json` ファイル内の `^5.0` に更新する必要があります。

<!-- Spark Stripe 5.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Spark Stripe's migrations to your application: -->
Spark Stripe 5.0 は、独自の移行ディレクトリから移行を自動的にロードしなくなりました。代わりに、次のコマンドを実行して、Spark Stripe の移行をアプリケーションに公開する必要があります。

```shell
php artisan vendor:publish --tag=spark-migrations
```

<!-- Please review the complete [Spark Stripe upgrade guide](https://spark.laravel.com/docs/spark-stripe/upgrade.html) for additional breaking changes. -->
その他の重大な変更については、完全な [Spark Stripe upgrade guide](https://spark.laravel.com/docs/spark-stripe/upgrade.html) を確認してください。

<a name="passport"></a>
<!-- ### Passport -->
### Passport

<a name="updating-telescope"></a>
<!-- #### Updating Passport -->
#### Updating Passport

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- Laravel 11 no longer supports Laravel Passport 11.x. Therefore, you should update your application's Laravel Passport dependency to `^12.0` in your `composer.json` file. -->
Laravel 11 は Laravel Passport 11.x をサポートしなくなりました。したがって、アプリケーションの Laravel Passport 依存関係を `composer.json` ファイル内の `^12.0` に更新する必要があります。

<!-- Passport 12.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Passport's migrations to your application: -->
Passport 12.0 は、独自の移行ディレクトリから移行を自動的にロードしなくなりました。代わりに、次のコマンドを実行して、Passport の移行をアプリケーションに公開する必要があります。

```shell
php artisan vendor:publish --tag=passport-migrations
```

<!-- In addition, the password grant type is disabled by default. You may enable it by invoking the `enablePasswordGrant` method in the `boot` method of your application's `AppServiceProvider`: -->
さらに、パスワード付与タイプはデフォルトでは無効になっています。これを有効にするには、アプリケーションの `AppServiceProvider` の `boot` メソッドで `enablePasswordGrant` メソッドを呼び出します。

```
public function boot(): void
{
    Passport::enablePasswordGrant();
}
```

<a name="sanctum"></a>
<!-- ### Sanctum -->
### Sanctum

<a name="updating-sanctum"></a>
<!-- #### Updating Sanctum -->
#### Updating Sanctum

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- Laravel 11 no longer supports Laravel Sanctum 3.x. Therefore, you should update your application's Laravel Sanctum dependency to `^4.0` in your `composer.json` file. -->
Laravel 11 は Laravel Sanctum 3.x をサポートしなくなりました。したがって、`composer.json` ファイルでアプリケーションの Laravel Sanctum 依存関係を `^4.0` に更新する必要があります。

<!-- Sanctum 4.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Sanctum's migrations to your application: -->
Sanctum 4.0 は、独自の移行ディレクトリから移行を自動的にロードしなくなりました。代わりに、次のコマンドを実行して、Sanctum の移行をアプリケーションに公開する必要があります。

```shell
php artisan vendor:publish --tag=sanctum-migrations
```

<!-- Then, in your application's `config/sanctum.php` configuration file, you should update the references to the `authenticate_session`, `encrypt_cookies`, and `validate_csrf_token` middleware to the following: -->
次に、アプリケーションの `config/sanctum.php` 構成ファイルで、`authenticate_session`、`encrypt_cookies`、および `validate_csrf_token` ミドルウェアへの参照を次のように更新する必要があります。

```
'middleware' => [
    'authenticate_session' => Laravel\Sanctum\Http\Middleware\AuthenticateSession::class,
    'encrypt_cookies' => Illuminate\Cookie\Middleware\EncryptCookies::class,
    'validate_csrf_token' => Illuminate\Foundation\Http\Middleware\ValidateCsrfToken::class,
],
```

<a name="telescope"></a>
<!-- ### Telescope -->
### Telescope

<a name="updating-telescope"></a>
<!-- #### Updating Telescope -->
#### Updating Telescope

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- Laravel 11 no longer supports Laravel Telescope 4.x. Therefore, you should update your application's Laravel Telescope dependency to `^5.0` in your `composer.json` file. -->
Laravel 11 は Laravel Telescope 4.x をサポートしなくなりました。したがって、アプリケーションの Laravel Telescope 依存関係を、`composer.json` ファイル内の `^5.0` に更新する必要があります。

<!-- Telescope 5.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Telescope's migrations to your application: -->
Telescope 5.0 は、独自の移行ディレクトリから移行を自動的にロードしなくなりました。代わりに、次のコマンドを実行して、Telescope の移行をアプリケーションに公開する必要があります。

```shell
php artisan vendor:publish --tag=telescope-migrations
```

<a name="spatie-once-package"></a>
<!-- ### Spatie Once Package -->
### Spatie Once Package

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- Laravel 11 now provides its own [`once` function](/docs/11.x/helpers#method-once) to ensure that a given closure is only executed once. Therefore, if your application has a dependency on the `spatie/once` package, you should remove it from your application's `composer.json` file to avoid conflicts. -->
Laravel 11 では、特定のクロージャが 1 回だけ実行されるようにするための独自の [`once` function](/docs/11.x/helpers#method-once) が提供されるようになりました。したがって、アプリケーションに `spatie/once` パッケージへの依存関係がある場合は、競合を避けるためにアプリケーションの `composer.json` ファイルから依存関係を削除する必要があります。

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/10.x...11.x) and choose which updates are important to you. -->
`laravel/laravel` [GitHub repository](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。 [GitHub comparison tool](https://github.com/laravel/laravel/compare/10.x...11.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。

