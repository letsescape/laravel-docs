<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading To 9.0 From 8.x](#upgrade-9.0)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Flysystem 3.x](#flysystem-3)
- [Symfony Mailer](#symfony-mailer)

<!-- </div> -->
</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Belongs To Many `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods](#belongs-to-many-first-or-new)
- [Custom Casts & `null`](#custom-casts-and-null)
- [Default HTTP Client Timeout](#http-client-default-timeout)
- [PHP Return Types](#php-return-types)
- [Postgres "Schema" Configuration](#postgres-schema-configuration)
- [The `assertDeleted` Method](#the-assert-deleted-method)
- [The `lang` Directory](#the-lang-directory)
- [The `password` Rule](#the-password-rule)
- [The `when` / `unless` Methods](#when-and-unless-methods)
- [Unvalidated Array Keys](#unvalidated-array-keys)

<!-- </div> -->
</div>

<a name="upgrade-9.0"></a>
<!-- ## Upgrading To 9.0 From 8.x -->
## Upgrading To 9.0 From 8.x

<a name="estimated-upgrade-time-30-minutes"></a>
<!-- #### Estimated Upgrade Time: 30 Minutes -->
#### Estimated Upgrade Time: 30 Minutes

> [!NOTE]
> 私たちは、考えられるすべての重大な変更を文書化するよう努めます。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。時間を節約したいですか? [Laravel Shift](https://laravelshift.com/) を使用すると、アプリケーションのアップグレードを自動化できます。

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- #### PHP 8.0.2 Required -->
#### PHP 8.0.2 Required

<!-- Laravel now requires PHP 8.0.2 or greater. -->
Laravel には PHP 8.0.2 以降が必要になりました。

<!-- #### Composer Dependencies -->
#### Composer Dependencies

<!-- You should update the following dependencies in your application's `composer.json` file: -->
アプリケーションの `composer.json` ファイル内の次の依存関係を更新する必要があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `laravel/framework` to `^9.0`
- `nunomaduro/collision` to `^6.1`
-->
- `laravel/framework` ～ `^9.0`
- `nunomaduro/collision` ～ `^6.1`

<!-- </div> -->
</div>

<!-- In addition, please replace `facade/ignition` with `"spatie/laravel-ignition": "^1.0"` and `pusher/pusher-php-server` (if applicable) with `"pusher/pusher-php-server": "^5.0"` in your application's `composer.json` file. -->
さらに、アプリケーションの `composer.json` ファイル内の `facade/ignition` を `"spatie/laravel-ignition": "^1.0"` に、`pusher/pusher-php-server` (該当する場合) を `"pusher/pusher-php-server": "^5.0"` に置き換えてください。

<!-- Furthermore, the following first-party packages have received new major releases to support Laravel 9.x. If applicable, you should read their individual upgrade guides before upgrading: -->
さらに、次のファーストパーティパッケージは、Laravel 9.x をサポートするための新しいメジャーリリースを受け取りました。該当する場合は、アップグレードする前に、それぞれのアップグレード ガイドを読む必要があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!-- - [Vonage Notification Channel (v3.0)](https://github.com/laravel/vonage-notification-channel/blob/3.x/UPGRADE.md) (Replaces Nexmo) -->
- [Vonage Notification Channel (v3.0)](https://github.com/laravel/vonage-notification-channel/blob/3.x/UPGRADE.md) (Nexmo を置き換え)

<!-- </div> -->
</div>

<!-- Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 9 support. -->
最後に、アプリケーションで使用される他のサードパーティパッケージを調べて、Laravel 9 をサポートする適切なバージョンを使用していることを確認します。

<a name="php-return-types"></a>
<!-- #### PHP Return Types -->
#### PHP Return Types

<!-- PHP is beginning to transition to requiring return type definitions on PHP methods such as `offsetGet`, `offsetSet`, etc. In light of this, Laravel 9 has implemented these return types in its code base. Typically, this should not affect user written code; however, if you are overriding one of these methods by extending Laravel's core classes, you will need to add these return types to your own application or package code: -->
PHP は、`offsetGet`、`offsetSet` などの PHP メソッドで戻り値の型の定義を要求するように移行し始めています。これを考慮して、Laravel 9 ではこれらの戻り値の型をコードベースに実装しました。通常、これはユーザーが作成したコードには影響しません。ただし、Laravel のコアクラスを拡張してこれらのメソッドのいずれかをオーバーライドする場合は、これらの戻り値の型を独自のアプリケーションまたはパッケージ コードに追加する必要があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `count(): int`
- `getIterator(): Traversable`
- `getSize(): int`
- `jsonSerialize(): array`
- `offsetExists($key): bool`
- `offsetGet($key): mixed`
- `offsetSet($key, $value): void`
- `offsetUnset($key): void`
-->
- `count(): int`
- `getIterator(): Traversable`
- `getSize(): int`
- `jsonSerialize(): array`
- `offsetExists($key): bool`
- `offsetGet($key): mixed`
- `offsetSet($key, $value): void`
- `offsetUnset($key): void`

<!-- </div> -->
</div>

<!-- In addition, return types were added to methods implementing PHP's `SessionHandlerInterface`. Again, it is unlikely that this change affects your own application or package code: -->
さらに、PHP の `SessionHandlerInterface` を実装するメソッドに戻り値の型が追加されました。繰り返しますが、この変更が独自のアプリケーションまたはパッケージのコードに影響を与える可能性は低いです。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `open($savePath, $sessionName): bool`
- `close(): bool`
- `read($sessionId): string|false`
- `write($sessionId, $data): bool`
- `destroy($sessionId): bool`
- `gc($lifetime): int`
-->
- `open($savePath, $sessionName): bool`
- `close(): bool`
- `read($sessionId): string|false`
- `write($sessionId, $data): bool`
- `destroy($sessionId): bool`
- `gc($lifetime): int`

<!-- </div> -->
</div>

<a name="application"></a>
<!-- ### Application -->
### Application

<a name="the-application-contract"></a>
<!-- #### The `Application` Contract -->
#### The `Application` Contract

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `storagePath` method of the `Illuminate\Contracts\Foundation\Application` interface has been updated to accept a `$path` argument. If you are implementing this interface you should update your implementation accordingly: -->
`Illuminate\Contracts\Foundation\Application` インターフェイスの `storagePath` メソッドが更新され、`$path` 引数を受け入れるようになりました。このインターフェースを実装している場合は、それに応じて実装を更新する必要があります。

```
public function storagePath($path = '');
```
<!-- Similarly, the `langPath` method of the `Illuminate\Foundation\Application` class has been updated to accept a `$path` argument: -->
同様に、`Illuminate\Foundation\Application` クラスの `langPath` メソッドは、`$path` 引数を受け入れるように更新されました。

```
public function langPath($path = '');
```

<!-- #### Exception Handler `ignore` Method -->
#### Exception Handler `ignore` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The exception handler's `ignore` method is now `public` instead of `protected`. This method is not included in the default application skeleton; however, if you have manually defined this method you should update its visibility to `public`: -->
例外ハンドラーの `ignore` メソッドは、`protected` ではなく `public` になりました。このメソッドは、デフォルトのアプリケーション スケルトンには含まれていません。ただし、このメソッドを手動で定義した場合は、その可視性を `public` に更新する必要があります。

```php
public function ignore(string $class);
```

<!-- #### Exception Handler Contract Binding -->
#### Exception Handler Contract Binding

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Previously, in order to override the default Laravel exception handler, custom implementations were bound into the service container using the `\App\Exceptions\Handler::class` type. However, you should now bind custom implementations using the `\Illuminate\Contracts\Debug\ExceptionHandler::class` type. -->
以前は、デフォルトの Laravel 例外ハンドラーをオーバーライドするために、カスタム実装は `\App\Exceptions\Handler::class` タイプを使用してサービスコンテナーにバインドされていました。ただし、`\Illuminate\Contracts\Debug\ExceptionHandler::class` タイプを使用してカスタム実装をバインドする必要があります。

<!-- ### Blade -->
### Blade

<!-- #### Lazy Collections & The `$loop` Variable -->
#### Lazy Collections & The `$loop` Variable

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- When iterating over a `LazyCollection` instance within a Blade template, the `$loop` variable is no longer available, as accessing this variable causes the entire `LazyCollection` to be loaded into memory, thus rendering the usage of lazy collections pointless in this scenario. -->
Blade テンプレート内の `LazyCollection` インスタンスを反復処理する場合、`$loop` 変数は使用できなくなります。この変数にアクセスすると、`LazyCollection` 全体がメモリにロードされるため、このシナリオでは遅延コレクションの使用が無意味になります。

<!-- #### Checked / Disabled / Selected Blade Directives -->
#### Checked / Disabled / Selected Blade Directives

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The new `@checked`, `@disabled`, and `@selected` Blade directives may conflict with Vue events of the same name. You may use `@@` to escape the directives and avoid this conflict: `@@selected`. -->
新しい `@checked`、`@disabled`、および `@selected` Blade ディレクティブは、同じ名前の Vue イベントと競合する可能性があります。 `@@` を使用してディレクティブをエスケープし、この競合を回避できます: `@@selected`。

<!-- ### Collections -->
### Collections

<!-- #### The `Enumerable` Contract -->
#### The `Enumerable` Contract

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `Illuminate\Support\Enumerable` contract now defines a `sole` method. If you are manually implementing this interface, you should update your implementation to reflect this new method: -->
`Illuminate\Support\Enumerable` コントラクトは、`sole` メソッドを定義するようになりました。このインターフェースを手動で実装している場合は、この新しいメソッドを反映するように実装を更新する必要があります。

```php
public function sole($key = null, $operator = null, $value = null);
```

<!-- #### The `reduceWithKeys` Method -->
#### The `reduceWithKeys` Method

<!-- The `reduceWithKeys` method has been removed as the `reduce` method provides the same functionality. You may simply update your code to call `reduce` instead of `reduceWithKeys`. -->
`reduce` メソッドが同じ機能を提供するため、`reduceWithKeys` メソッドは削除されました。 `reduceWithKeys` の代わりに `reduce` を呼び出すようにコードを更新するだけです。

<!-- #### The `reduceMany` Method -->
#### The `reduceMany` Method

<!-- The `reduceMany` method has been renamed to `reduceSpread` for naming consistency with other similar methods. -->
他の同様のメソッドとの名前の一貫性を保つために、`reduceMany` メソッドの名前が `reduceSpread` に変更されました。

<!-- ### Container -->
### Container

<!-- #### The `Container` Contract -->
#### The `Container` Contract

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Illuminate\Contracts\Container\Container` contract has received two method definitions: `scoped` and `scopedIf`. If you are manually implementing this contract, you should update your implementation to reflect these new methods. -->
`Illuminate\Contracts\Container\Container` コントラクトは、`scoped` と `scopedIf` という 2 つのメソッド定義を受け取りました。このコントラクトを手動で実装している場合は、これらの新しいメソッドを反映するように実装を更新する必要があります。

<!-- #### The `ContextualBindingBuilder` Contract -->
#### The `ContextualBindingBuilder` Contract

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Illuminate\Contracts\Container\ContextualBindingBuilder` contract now defines a `giveConfig` method. If you are manually implementing this interface, you should update your implementation to reflect this new method: -->
`Illuminate\Contracts\Container\ContextualBindingBuilder` コントラクトは、`giveConfig` メソッドを定義するようになりました。このインターフェースを手動で実装している場合は、この新しいメソッドを反映するように実装を更新する必要があります。

```php
public function giveConfig($key, $default = null);
```

<!-- ### Database -->
### Database

<a name="postgres-schema-configuration"></a>
<!-- #### Postgres "Schema" Configuration -->
#### Postgres "Schema" Configuration

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The `schema` configuration option used to configure Postgres connection search paths in your application's `config/database.php` configuration file should be renamed to `search_path`. -->
アプリケーションの `config/database.php` 構成ファイルで Postgres 接続検索パスの構成に使用される `schema` 構成オプションの名前を `search_path` に変更する必要があります。

<a name="schema-builder-doctrine-method"></a>
<!-- #### Schema Builder `registerCustomDoctrineType` Method -->
#### Schema Builder `registerCustomDoctrineType` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `registerCustomDoctrineType` method has been removed from the `Illuminate\Database\Schema\Builder` class. You may use the `registerDoctrineType` method on the `DB` facade instead, or register custom Doctrine types in the `config/database.php` configuration file. -->
`registerCustomDoctrineType` メソッドが `Illuminate\Database\Schema\Builder` クラスから削除されました。代わりに、`DB` ファサードで `registerDoctrineType` メソッドを使用することも、`config/database.php` 構成ファイルにカスタム Doctrine タイプを登録することもできます。

<!-- ### Eloquent -->
### Eloquent

<a name="custom-casts-and-null"></a>
<!-- #### Custom Casts & `null` -->
#### Custom Casts & `null`

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- In previous releases of Laravel, the `set` method of custom cast classes was not invoked if the cast attribute was being set to `null`. However, this behavior was inconsistent with the Laravel documentation. In Laravel 9.x, the `set` method of the cast class will be invoked with `null` as the provided `$value` argument. Therefore, you should ensure your custom casts are able to sufficiently handle this scenario: -->
Laravel の以前のリリースでは、cast属性が `null` に設定されている場合、カスタム cast クラスの `set` メソッドは呼び出されませんでした。ただし、この動作は Laravel ドキュメントと矛盾していました。 Laravel 9.xでは、castクラスの`set`メソッドは、指定された`$value`引数として`null`を使用して呼び出されます。したがって、カスタム castがこのシナリオを十分に処理できることを確認する必要があります。

```php
/**
 * Prepare the given value for storage.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  AddressModel  $value
 * @param  array  $attributes
 * @return array
 */
public function set($model, $key, $value, $attributes)
{
    if (! $value instanceof AddressModel) {
        throw new InvalidArgumentException('The given value is not an Address instance.');
    }

    return [
        'address_line_one' => $value->lineOne,
        'address_line_two' => $value->lineTwo,
    ];
}
```

<a name="belongs-to-many-first-or-new"></a>
<!-- #### Belongs To Many `firstOrNew`, `firstOrCreate`, and `updateOrCreate` Methods -->
#### Belongs To Many `firstOrNew`, `firstOrCreate`, and `updateOrCreate` Methods

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The `belongsToMany` relationship's `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods all accept an array of attributes as their first argument. In previous releases of Laravel, this array of attributes was compared against the "pivot" / intermediate table for existing records. -->
`belongsToMany` 関係の `firstOrNew`、`firstOrCreate`、および `updateOrCreate` メソッドはすべて、最初の引数として属性の配列を受け入れます。 Laravel の以前のリリースでは、この属性の配列は既存のレコードの「ピボット」/中間テーブルと比較されました。

<!-- However, this behavior was unexpected and typically unwanted. Instead, these methods now compare the array of attributes against the table of the related model: -->
ただし、この動作は予期せぬものであり、通常は望ましくないものでした。代わりに、これらのメソッドは属性の配列を関連モデルのテーブルと比較するようになりました。

```php
$user->roles()->updateOrCreate([
    'name' => 'Administrator',
]);
```

<!-- In addition, the `firstOrCreate` method now accepts a `$values` array as its second argument. This array will be merged with the first argument to the method (`$attributes`) when creating the related model if one does not already exist. This change makes this method consistent with the `firstOrCreate` methods offered by other relationship types: -->
さらに、`firstOrCreate` メソッドは、2 番目の引数として `$values` 配列を受け入れるようになりました。関連モデルが存在しない場合、この配列は、関連モデルの作成時にメソッド (`$attributes`) の最初の引数とマージされます。この変更により、このメソッドは、他の関係タイプが提供する `firstOrCreate` メソッドと一貫性を持つようになります。

```php
$user->roles()->firstOrCreate([
    'name' => 'Administrator',
], [
    'created_by' => $user->id,
]);
```

<!-- #### The `touch` Method -->
#### The `touch` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `touch` method now accepts an attribute to touch. If you were previously overwriting this method, you should update your method signature to reflect this new argument: -->
`touch` メソッドは、タッチする属性を受け入れるようになりました。以前にこのメソッドを上書きしていた場合は、この新しい引数を反映するようにメソッド シグネチャを更新する必要があります。

```php
public function touch($attribute = null);
```

<!-- ### Encryption -->
### Encryption

<!-- #### The Encrypter Contract -->
#### The Encrypter Contract

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `Illuminate\Contracts\Encryption\Encrypter` contract now defines a `getKey` method. If you are manually implementing this interface, you should update your implementation accordingly: -->
`Illuminate\Contracts\Encryption\Encrypter` コントラクトは、`getKey` メソッドを定義するようになりました。このインターフェースを手動で実装している場合は、それに応じて実装を更新する必要があります。

```php
public function getKey();
```

<!-- ### Facades -->
### Facades

<!-- #### The `getFacadeAccessor` Method -->
#### The `getFacadeAccessor` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `getFacadeAccessor` method must always return a container binding key. In previous releases of Laravel, this method could return an object instance; however, this behavior is no longer supported. If you have written your own facades, you should ensure that this method returns a container binding string: -->
`getFacadeAccessor` メソッドは、常にコンテナー バインディング キーを返す必要があります。 Laravel の以前のリリースでは、このメソッドはオブジェクト インスタンスを返すことができました。ただし、この動作はサポートされなくなりました。独自のファサードを作成した場合は、このメソッドがコンテナ バインディング文字列を返すようにする必要があります。

```php
/**
 * Get the registered name of the component.
 *
 * @return string
 */
protected static function getFacadeAccessor()
{
    return Example::class;
}
```

<!-- ### Filesystem -->
### Filesystem

<!-- #### The `FILESYSTEM_DRIVER` Environment Variable -->
#### The `FILESYSTEM_DRIVER` Environment Variable

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `FILESYSTEM_DRIVER` environment variable has been renamed to `FILESYSTEM_DISK` to more accurately reflect its usage. This change only affects the application skeleton; however, you are welcome to update your own application's environment variables to reflect this change if you wish. -->
`FILESYSTEM_DRIVER` 環境変数の名前は、その使用法をより正確に反映するために `FILESYSTEM_DISK` に変更されました。この変更はアプリケーションのスケルトンにのみ影響します。ただし、必要に応じて、独自のアプリケーションの環境変数を更新して、この変更を反映することもできます。

<!-- #### The "Cloud" Disk -->
#### The "Cloud" Disk

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `cloud` disk configuration option was removed from the default application skeleton in November of 2020. This change only affects the application skeleton. If you are using the `cloud` disk within your application, you should leave this configuration value in your own application's skeleton. -->
`cloud` ディスク構成オプションは、2020 年 11 月にデフォルトのアプリケーション スケルトンから削除されました。この変更はアプリケーション スケルトンにのみ影響します。アプリケーション内で `cloud` ディスクを使用している場合は、この構成値を独自のアプリケーションのスケルトンに残す必要があります。

<a name="flysystem-3"></a>
<!-- ### Flysystem 3.x -->
### Flysystem 3.x

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- Laravel 9.x has migrated from [Flysystem](https://flysystem.thephpleague.com/v2/docs/) 1.x to 3.x. Under the hood, Flysystem powers all of the file manipulation methods provided by the `Storage` facade. In light of this, some changes may be required within your application; however, we have tried to make this transition as seamless as possible. -->
Laravel 9.x は [Flysystem](https://flysystem.thephpleague.com/v2/docs/) 1.x から 3.x に移行しました。 Flysystem は内部で、`Storage` ファサードによって提供されるすべてのファイル操作メソッドを強化します。これを考慮して、アプリケーション内でいくつかの変更が必要になる場合があります。ただし、この移行を可能な限りシームレスにするよう努めてきました。

<!-- #### Driver Prerequisites -->
#### Driver Prerequisites

<!-- Before using the S3, FTP, or SFTP drivers, you will need to install the appropriate package via the Composer package manager: -->
S3、FTP、または SFTP ドライバを使用する前に、Composer パッケージ マネージャーを介して適切なパッケージをインストールする必要があります。

<!--
- Amazon S3: `composer require -W league/flysystem-aws-s3-v3 "^3.0"`
- FTP: `composer require league/flysystem-ftp "^3.0"`
- SFTP: `composer require league/flysystem-sftp-v3 "^3.0"`
-->
- Amazon S3: `composer require -W league/flysystem-aws-s3-v3 "^3.0"`
- FTP: `composer require league/flysystem-ftp "^3.0"`
- SFTP: `composer require league/flysystem-sftp-v3 "^3.0"`

<!-- #### Overwriting Existing Files -->
#### Overwriting Existing Files

<!-- Write operations such as `put`, `write`, and `writeStream` now overwrite existing files by default. If you do not want to overwrite existing files, you should manually check for the file's existence before performing the write operation. -->
`put`、`write`、`writeStream` などの書き込み操作は、デフォルトで既存のファイルを上書きするようになりました。既存のファイルを上書きしたくない場合は、書き込み操作を実行する前にファイルの存在を手動で確認する必要があります。

<!-- #### Write Exceptions -->
#### Write Exceptions

<!-- Write operations such as `put`, `write`, and `writeStream` no longer throw an exception when a write operation fails. Instead, `false` is returned. If you would like to preserve the previous behavior which threw exceptions, you may define the `throw` option within a filesystem disk's configuration array: -->
`put`、`write`、`writeStream` などの書き込み操作は、書き込み操作が失敗したときに例外をスローしなくなりました。代わりに、`false` が返されます。例外をスローした以前の動作を保持したい場合は、ファイルシステム ディスクの構成配列内で `throw` オプションを定義できます。

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<!-- #### Reading Missing Files -->
#### Reading Missing Files

<!-- Attempting to read from a file that does not exist now returns `null`. In previous releases of Laravel, an `Illuminate\Contracts\Filesystem\FileNotFoundException` would have been thrown. -->
存在しないファイルから読み取ろうとすると、`null` が返されるようになりました。 Laravel の以前のリリースでは、`Illuminate\Contracts\Filesystem\FileNotFoundException` がスローされていました。

<!-- #### Deleting Missing Files -->
#### Deleting Missing Files

<!-- Attempting to `delete` a file that does not exist now returns `true`. -->
存在しないファイルに対して `delete` を実行しようとすると、`true` が返されるようになりました。

<!-- #### Cached Adapters -->
#### Cached Adapters

<!-- Flysystem no longer supports "cached adapters". Thus, they have been removed from Laravel and any relevant configuration (such as the `cache` key within disk configurations) can be removed. -->
Flysystem は「キャッシュされたアダプター」をサポートしなくなりました。したがって、それらはLaravelから削除され、関連する構成(ディスク構成内の`cache`キーなど)は削除できます。

<!-- #### Custom Filesystems -->
#### Custom Filesystems

<!-- Slight changes have been made to the steps required to register custom filesystem drivers. Therefore, if you were defining your own custom filesystem drivers, or using packages that define custom drivers, you should update your code and dependencies. -->
カスタム ファイルシステム ドライバを登録するために必要な手順に若干の変更が加えられました。したがって、独自のカスタム ファイル システム ドライバを定義している場合、またはカスタム ドライバを定義するパッケージを使用している場合は、コードと依存関係を更新する必要があります。

<!-- For example, in Laravel 8.x, a custom filesystem driver might be registered like so: -->
たとえば、Laravel 8.x では、カスタム ファイルシステム ドライバは次のように登録されます。

```php
use Illuminate\Support\Facades\Storage;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

Storage::extend('dropbox', function ($app, $config) {
    $client = new DropboxClient(
        $config['authorization_token']
    );

    return new Filesystem(new DropboxAdapter($client));
});
```

<!-- However, in Laravel 9.x, the callback given to the `Storage::extend` method should return an instance of `Illuminate\Filesystem\FilesystemAdapter` directly: -->
ただし、Laravel 9.x では、`Storage::extend` メソッドに指定されたコールバックは、`Illuminate\Filesystem\FilesystemAdapter` のインスタンスを直接返す必要があります。

```php
use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

Storage::extend('dropbox', function ($app, $config) {
    $adapter = new DropboxAdapter(
        new DropboxClient($config['authorization_token'])
    );

    return new FilesystemAdapter(
        new Filesystem($adapter, $config),
        $adapter,
        $config
    );
});
```

<!-- #### SFTP Private-Public Key Passphrase -->
#### SFTP Private-Public Key Passphrase

<!-- If your application is using Flysystem's SFTP adapter and private-public key authentication, the `password` configuration item that is used to decrypt the private key should be renamed to `passphrase`. -->
アプリケーションが Flysystem の SFTP アダプターと秘密-公開キー認証を使用している場合、秘密キーの復号化に使用される `password` 構成項目の名前を `passphrase` に変更する必要があります。

<!-- ### Helpers -->
### Helpers

<a name="data-get-function"></a>
<!-- #### The `data_get` Helper & Iterable Objects -->
#### The `data_get` Helper & Iterable Objects

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Previously, the `data_get` helper could be used to retrieve nested data on arrays and `Collection` instances; however, this helper can now retrieve nested data on all iterable objects. -->
以前は、`data_get` ヘルパを使用して、配列および `Collection` インスタンスのネストされたデータを取得できました。ただし、このヘルパはすべての反復可能なオブジェクトのネストされたデータを取得できるようになりました。

<a name="str-function"></a>
<!-- #### The `str` Helper -->
#### The `str` Helper

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Laravel 9.x now includes a global `str` [helper function](/docs/9.x/helpers#method-str). If you are defining a global `str` helper in your application, you should rename or remove it so that it does not conflict with Laravel's own `str` helper. -->
Laravel 9.x には、グローバル `str` [helper function](/docs/9.x/helpers#method-str) が含まれるようになりました。アプリケーションでグローバル `str` ヘルパを定義している場合は、Laravel 独自の `str` ヘルパと競合しないように、ヘルパの名前を変更するか削除する必要があります。

<a name="when-and-unless-methods"></a>
<!-- #### The `when` / `unless` Methods -->
#### The `when` / `unless` Methods

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- As you may know, `when` and `unless` methods are offered by various classes throughout the framework. These methods can be used to conditionally perform an action if the boolean value of the first argument to the method evaluates to `true` or `false`: -->
ご存知のとおり、`when` メソッドと `unless` メソッドは、フレームワーク全体のさまざまなクラスによって提供されます。これらのメソッドを使用すると、メソッドの最初の引数のブール値が `true` または `false` に評価される場合に条件付きでアクションを実行できます。

```php
$collection->when(true, function ($collection) {
    $collection->merge([1, 2, 3]);
});
```

<!-- Therefore, in previous releases of Laravel, passing a closure to the `when` or `unless` methods meant that the conditional operation would always execute, since a loose comparison against a closure object (or any other object) always evaluates to `true`. This often led to unexpected outcomes because developers expect the **result** of the closure to be used as the boolean value that determines if the conditional action executes. -->
したがって、Laravelの以前のリリースでは、クロージャを`when`メソッドまたは`unless`メソッドに渡すことは、クロージャオブジェクト(または他のオブジェクト)との緩やかな比較が常に`true`と評価されるため、条件付き操作が常に実行されることを意味していました。開発者はクロージャの **結果** が条件付きアクションを実行するかどうかを決定するブール値として使用されることを期待しているため、これにより予期せぬ結果が生じることがよくあります。

<!-- So, in Laravel 9.x, any closures passed to the `when` or `unless` methods will be executed and the value returned by the closure will be considered the boolean value used by the `when` and `unless` methods: -->
したがって、Laravel 9.xでは、`when`メソッドまたは`unless`メソッドに渡されたクロージャはすべて実行され、クロージャによって返される値は、`when`メソッドおよび`unless`メソッドによって使用されるブール値とみなされます。

```php
$collection->when(function ($collection) {
    // This closure is executed...
    return false;
}, function ($collection) {
    // Not executed since first closure returned "false"...
    $collection->merge([1, 2, 3]);
});
```

<!-- ### HTTP Client -->
### HTTP Client

<a name="http-client-default-timeout"></a>
<!-- #### Default Timeout -->
#### Default Timeout

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The [HTTP client](/docs/9.x/http-client) now has a default timeout of 30 seconds. In other words, if the server does not respond within 30 seconds, an exception will be thrown. Previously, no default timeout length was configured on the HTTP client, causing requests to sometimes "hang" indefinitely. -->
[HTTP client](/docs/9.x/http-client) のデフォルトのタイムアウトは 30 秒になりました。つまり、サーバーが 30 秒以内に応答しない場合、例外がスローされます。以前は、HTTP クライアントにデフォルトのタイムアウト長が設定されていなかったため、リクエストが無期限に「ハング」することがありました。

<!-- If you wish to specify a longer timeout for a given request, you may do so using the `timeout` method: -->
特定のリクエストに対してより長いタイムアウトを指定したい場合は、`timeout` メソッドを使用して指定できます。

```
$response = Http::timeout(120)->get(/* ... */);
```

<!-- #### HTTP Fake & Middleware -->
#### HTTP Fake & Middleware

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Previously, Laravel would not execute any provided Guzzle HTTP middleware when the [HTTP client](/docs/9.x/http-client) was "faked". However, in Laravel 9.x, Guzzle HTTP middleware will be executed even when the HTTP client is faked. -->
以前は、Laravel は、[HTTP client](/docs/9.x/http-client) が「偽装」された場合、提供されている Guzzle HTTP ミドルウェアを実行しませんでした。ただし、Laravel 9.x では、HTTP クライアントが偽装された場合でも、Guzzle HTTP ミドルウェアが実行されます。

<!-- #### HTTP Fake & Dependency Injection -->
#### HTTP Fake & Dependency Injection

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- In previous releases of Laravel, invoking the `Http::fake()` method would not affect instances of the `Illuminate\Http\Client\Factory` that were injected into class constructors. However, in Laravel 9.x, `Http::fake()` will ensure fake responses are returned by HTTP clients injected into other services via dependency injection. This behavior is more consistent with the behavior of other facades and fakes. -->
Laravel の以前のリリースでは、`Http::fake()` メソッドを呼び出しても、クラス コンストラクターに挿入された `Illuminate\Http\Client\Factory` のインスタンスには影響しませんでした。ただし、Laravel 9.x では、`Http::fake()` は、依存注入を通じて他のサービスに注入された HTTP クライアントによって偽の応答が返されることを保証します。この動作は、他のファサードや偽物の動作とより一貫性があります。

<a name="symfony-mailer"></a>
<!-- ### Symfony Mailer -->
### Symfony Mailer

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- One of the largest changes in Laravel 9.x is the transition from SwiftMailer, which is no longer maintained as of December 2021, to Symfony Mailer. However, we have tried to make this transition as seamless as possible for your applications. That being said, please thoroughly review the list of changes below to ensure your application is fully compatible. -->
Laravel 9.x の最大の変更点の 1 つは、2021 年 12 月の時点でメンテナンスが終了した SwiftMailer から Symfony Mailer への移行です。ただし、私たちはこの移行をアプリケーションにとって可能な限りシームレスにするよう努めてきました。そうは言っても、アプリケーションが完全に互換性があることを確認するために、以下の変更点のリストをよく確認してください。

<!-- #### Driver Prerequisites -->
#### Driver Prerequisites

<!-- To continue using the Mailgun transport, your application should require the `symfony/mailgun-mailer` and `symfony/http-client` Composer packages: -->
Mailgun トランスポートを引き続き使用するには、アプリケーションに `symfony/mailgun-mailer` および `symfony/http-client` Composer パッケージが必要です。

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

<!-- The `wildbit/swiftmailer-postmark` Composer package should be removed from your application. Instead, your application should require the `symfony/postmark-mailer` and `symfony/http-client` Composer packages: -->
`wildbit/swiftmailer-postmark` Composer パッケージをアプリケーションから削除する必要があります。代わりに、アプリケーションには `symfony/postmark-mailer` および `symfony/http-client` Composer パッケージが必要です。

```shell
composer require symfony/postmark-mailer symfony/http-client
```

<!-- #### Updated Return Types -->
#### Updated Return Types

<!-- The `send`, `html`, `raw`, and `plain` methods on `Illuminate\Mail\Mailer` no longer return `void`. Instead, an instance of `Illuminate\Mail\SentMessage` is returned. This object contains an instance of `Symfony\Component\Mailer\SentMessage` that is accessible via the `getSymfonySentMessage` method or by dynamically invoking methods on the object. -->
`Illuminate\Mail\Mailer` の `send`、`html`、`raw`、および `plain` メソッドは、`void` を返さなくなりました。代わりに、`Illuminate\Mail\SentMessage` のインスタンスが返されます。このオブジェクトには、`getSymfonySentMessage` メソッドを介して、またはオブジェクトのメソッドを動的に呼び出すことによってアクセスできる、`Symfony\Component\Mailer\SentMessage` のインスタンスが含まれています。

<!-- #### Renamed "Swift" Methods -->
#### Renamed "Swift" Methods

<!-- Various SwiftMailer related methods, some of which were undocumented, have been renamed to their Symfony Mailer counterparts. For example, the `withSwiftMessage` method has been renamed to `withSymfonyMessage`: -->
文書化されていないものもあるさまざまな SwiftMailer 関連のメソッドの名前が、対応する Symfony Mailer に変更されました。たとえば、`withSwiftMessage` メソッドの名前は `withSymfonyMessage` に変更されました。

```
// Laravel 8.x...
$this->withSwiftMessage(function ($message) {
    $message->getHeaders()->addTextHeader(
        'Custom-Header', 'Header Value'
    );
});

// Laravel 9.x...
use Symfony\Component\Mime\Email;

$this->withSymfonyMessage(function (Email $message) {
    $message->getHeaders()->addTextHeader(
        'Custom-Header', 'Header Value'
    );
});
```

> [!WARNING]
> `Symfony\Component\Mime\Email` オブジェクトとのあらゆる対話について、[Symfony Mailer documentation](https://symfony.com/doc/6.0/mailer.html#creating-sending-messages) を徹底的に確認してください。

<!-- The list below contains a more thorough overview of renamed methods. Many of these methods are low-level methods used to interact with SwiftMailer / Symfony Mailer directly, so may not be commonly used within most Laravel applications: -->
以下のリストには、名前が変更されたメソッドのより詳細な概要が含まれています。これらのメソッドの多くは、SwiftMailer / Symfony Mailer と直接対話するために使用される低レベルのメソッドであるため、ほとんどの Laravel アプリケーション内では一般的に使用されない可能性があります。

```
Message::getSwiftMessage();
Message::getSymfonyMessage();

Mailable::withSwiftMessage($callback);
Mailable::withSymfonyMessage($callback);

MailMessage::withSwiftMessage($callback);
MailMessage::withSymfonyMessage($callback);

Mailer::getSwiftMailer();
Mailer::getSymfonyTransport();

Mailer::setSwiftMailer($swift);
Mailer::setSymfonyTransport(TransportInterface $transport);

MailManager::createTransport($config);
MailManager::createSymfonyTransport($config);
```

<!-- #### Proxied `Illuminate\Mail\Message` Methods -->
#### Proxied `Illuminate\Mail\Message` Methods

<!-- The `Illuminate\Mail\Message` typically proxied missing methods to the underlying `Swift_Message` instance. However, missing methods are now proxied to an instance of `Symfony\Component\Mime\Email` instead. So, any code that was previously relying on missing methods to be proxied to SwiftMailer should be updated to their corresponding Symfony Mailer counterparts. -->
`Illuminate\Mail\Message` は通常、欠落しているメソッドを基になる `Swift_Message` インスタンスにプロキシします。ただし、不足しているメソッドは代わりに `Symfony\Component\Mime\Email` のインスタンスにプロキシされるようになりました。そのため、これまで SwiftMailer にプロキシされる欠落メソッドに依存していたコードは、対応する Symfony Mailer に更新する必要があります。

<!-- Again, many applications may not be interacting with these methods, as they are not documented within the Laravel documentation: -->
繰り返しになりますが、これらのメソッドは Laravel ドキュメントに記載されていないため、多くのアプリケーションはこれらのメソッドと対話していない可能性があります。

```
// Laravel 8.x...
$message
    ->setFrom('taylor@laravel.com')
    ->setTo('example@example.org')
    ->setSubject('Order Shipped')
    ->setBody('<h1>HTML</h1>', 'text/html')
    ->addPart('Plain Text', 'text/plain');

// Laravel 9.x...
$message
    ->from('taylor@laravel.com')
    ->to('example@example.org')
    ->subject('Order Shipped')
    ->html('<h1>HTML</h1>')
    ->text('Plain Text');
```

<!-- #### Generated Messages IDs -->
#### Generated Messages IDs

<!-- SwiftMailer offered the ability to define a custom domain to include in generated Message IDs via the `mime.idgenerator.idright` configuration option. This is not supported by Symfony Mailer. Instead, Symfony Mailer will automatically generate a Message ID based on the sender. -->
SwiftMailer は、`mime.idgenerator.idright` 構成オプションを介して、生成されたメッセージ ID に含めるカスタム ドメインを定義する機能を提供しました。これは Symfony Mailer ではサポートされていません。代わりに、Symfony Mailer は送信者に基づいてメッセージ ID を自動的に生成します。

<!-- #### `MessageSent` Event Changes -->
#### `MessageSent` Event Changes

<!-- The `message` property of the `Illuminate\Mail\Events\MessageSent` event now contains an instance of `Symfony\Component\Mime\Email` instead of an instance of `Swift_Message`. This message represents the email **before** it is sent. -->
`Illuminate\Mail\Events\MessageSent` イベントの `message` プロパティには、`Swift_Message` のインスタンスではなく、`Symfony\Component\Mime\Email` のインスタンスが含まれるようになりました。このメッセージは、送信される**前**の電子メールを表しています。

<!-- Additionally, a new `sent` property has been added to the `MessageSent` event. This property contains an instance of `Illuminate\Mail\SentMessage` and contains information about the sent email, such as the message ID. -->
さらに、新しい `sent` プロパティが `MessageSent` イベントに追加されました。このプロパティには、`Illuminate\Mail\SentMessage` のインスタンスが含まれており、メッセージ ID など、送信された電子メールに関する情報が含まれています。

<!-- #### Forced Reconnections -->
#### Forced Reconnections

<!-- It is no longer possible to force a transport reconnection (for example when the mailer is running via a daemon process). Instead, Symfony Mailer will attempt to reconnect to the transport automatically and throw an exception if the reconnection fails. -->
トランスポートの再接続を強制することはできなくなりました (たとえば、メーラーがデーモン プロセスを介して実行されている場合)。代わりに、Symfony Mailer は自動的にトランスポートへの再接続を試み、再接続が失敗した場合は例外をスローします。

<!-- #### SMTP Stream Options -->
#### SMTP Stream Options

<!-- Defining stream options for the SMTP transport is no longer supported. Instead, you must define the relevant options directly within the configuration if they are supported. For example, to disable TLS peer verification: -->
SMTP トランスポートのストリーム オプションの定義はサポートされなくなりました。代わりに、関連するオプションがサポートされている場合は、構成内で直接定義する必要があります。たとえば、TLS ピア検証を無効にするには、次のようにします。

```
'smtp' => [
    // Laravel 8.x...
    'stream' => [
        'ssl' => [
            'verify_peer' => false,
        ],
    ],

    // Laravel 9.x...
    'verify_peer' => false,
],
```

<!-- To learn more about the available configuration options, please review the [Symfony Mailer documentation](https://symfony.com/doc/6.0/mailer.html#transport-setup). -->
利用可能な構成オプションの詳細については、[Symfony Mailer documentation](https://symfony.com/doc/6.0/mailer.html#transport-setup) を参照してください。

> [!WARNING]
> 上記の例にもかかわらず、SSL 検証を無効にすると「中間者」攻撃の可能性が生じるため、通常は SSL 検証を無効にすることはお勧めできません。

<!-- #### SMTP `auth_mode` -->
#### SMTP `auth_mode`

<!-- Defining the SMTP `auth_mode` in the `mail` configuration file is no longer required. The authentication mode will be automatically negotiated between Symfony Mailer and the SMTP server. -->
`mail` 構成ファイルで SMTP `auth_mode` を定義する必要はなくなりました。認証モードは、Symfony Mailer と SMTP サーバーの間で自動的にネゴシエートされます。

<!-- #### Failed Recipients -->
#### Failed Recipients

<!-- It is no longer possible to retrieve a list of failed recipients after sending a message. Instead, a `Symfony\Component\Mailer\Exception\TransportExceptionInterface` exception will be thrown if a message fails to send. Instead of relying on retrieving invalid email addresses after sending a message, we recommend that you validate email addresses before sending the message instead. -->
メッセージの送信後に失敗した受信者のリストを取得できなくなりました。代わりに、メッセージの送信に失敗した場合は、`Symfony\Component\Mailer\Exception\TransportExceptionInterface` 例外がスローされます。メッセージの送信後に無効な電子メール アドレスを取得することに頼るのではなく、メッセージを送信する前に電子メール アドレスを検証することをお勧めします。

<!-- ### Packages -->
### Packages

<a name="the-lang-directory"></a>
<!-- #### The `lang` Directory -->
#### The `lang` Directory

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- In new Laravel applications, the `resources/lang` directory is now located in the root project directory (`lang`). If your package is publishing language files to this directory, you should ensure that your package is publishing to `app()->langPath()` instead of a hard-coded path. -->
新しい Laravel アプリケーションでは、`resources/lang` ディレクトリがルート プロジェクト ディレクトリ (`lang`) に配置されるようになりました。パッケージが言語ファイルをこのディレクトリに公開している場合は、パッケージがハードコードされたパスではなく `app()->langPath()` に公開していることを確認する必要があります。

<a name="queue"></a>
<!-- ### Queue -->
### Queue

<a name="the-opis-closure-library"></a>
<!-- #### The `opis/closure` Library -->
#### The `opis/closure` Library

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Laravel's dependency on `opis/closure` has been replaced by `laravel/serializable-closure`. This should not cause any breaking change in your application unless you are interacting with the `opis/closure` library directly. In addition, the previously deprecated `Illuminate\Queue\SerializableClosureFactory` and `Illuminate\Queue\SerializableClosure` classes have been removed. If you are interacting with `opis/closure` library directly or using any of the removed classes, you may use [Laravel Serializable Closure](https://github.com/laravel/serializable-closure) instead. -->
Laravel の `opis/closure` への依存関係は、`laravel/serializable-closure` に置き換えられました。 `opis/closure` ライブラリを直接操作しない限り、これによってアプリケーションに重大な変更が生じることはありません。さらに、以前に非推奨になった `Illuminate\Queue\SerializableClosureFactory` クラスと `Illuminate\Queue\SerializableClosure` クラスが削除されました。 `opis/closure` ライブラリと直接対話している場合、または削除されたクラスのいずれかを使用している場合は、代わりに [Laravel Serializable Closure](https://github.com/laravel/serializable-closure) を使用できます。

<!-- #### The Failed Job Provider `flush` Method -->
#### The Failed Job Provider `flush` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `flush` method defined by the `Illuminate\Queue\Failed\FailedJobProviderInterface` interface now accepts an `$hours` argument which determines how old a failed job must be (in hours) before it is flushed by the `queue:flush` command. If you are manually implementing the `FailedJobProviderInterface` you should ensure that your implementation is updated to reflect this new argument: -->
`Illuminate\Queue\Failed\FailedJobProviderInterface` インターフェースによって定義された `flush` メソッドは、`queue:flush` コマンドによってフラッシュされる前に、失敗したジョブがどれくらい経過する必要があるかを (時間単位で) 決定する `$hours` 引数を受け入れるようになりました。 `FailedJobProviderInterface` を手動で実装している場合は、この新しい引数を反映するように実装が更新されていることを確認する必要があります。

```php
public function flush($hours = null);
```

<!-- ### Session -->
### Session

<!-- #### The `getSession` Method -->
#### The `getSession` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `Symfony\Component\HttpFoundaton\Request` class that is extended by Laravel's own `Illuminate\Http\Request` class offers a `getSession` method to get the current session storage handler. This method is not documented by Laravel as most Laravel applications interact with the session through Laravel's own `session` method. -->
Laravel 独自の `Illuminate\Http\Request` クラスによって拡張された `Symfony\Component\HttpFoundaton\Request` クラスは、現在のセッション ストレージ ハンドラーを取得する `getSession` メソッドを提供します。ほとんどの Laravel アプリケーションは Laravel 独自の `session` メソッドを通じてセッションと対話するため、このメソッドは Laravel によって文書化されていません。

<!-- The `getSession` method previously returned an instance of `Illuminate\Session\Store` or `null`; however, due to the Symfony 6.x release enforcing a return type of `Symfony\Component\HttpFoundation\Session\SessionInterface`, the `getSession` now correctly returns a `SessionInterface` implementation or throws an `\Symfony\Component\HttpFoundation\Exception\SessionNotFoundException` exception when no session is available. -->
`getSession` メソッドは、以前は `Illuminate\Session\Store` または `null` のインスタンスを返していました。ただし、Symfony 6.x リリースでは戻り値の型 `Symfony\Component\HttpFoundation\Session\SessionInterface` が強制されているため、`getSession` は `SessionInterface` 実装を正しく返すか、セッションが使用できない場合に `\Symfony\Component\HttpFoundation\Exception\SessionNotFoundException` 例外をスローするようになりました。

<!-- ### Testing -->
### Testing

<a name="the-assert-deleted-method"></a>
<!-- #### The `assertDeleted` Method -->
#### The `assertDeleted` Method

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- All calls to the `assertDeleted` method should be updated to `assertModelMissing`. -->
`assertDeleted` メソッドへのすべての呼び出しは、`assertModelMissing` に更新する必要があります。

<!-- ### Trusted Proxies -->
### Trusted Proxies

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- If you are upgrading your Laravel 8 project to Laravel 9 by importing your existing application code into a totally new Laravel 9 application skeleton, you may need to update your application's "trusted proxy" middleware. -->
既存のアプリケーションコードをまったく新しい Laravel 9 アプリケーションスケルトンにインポートして、Laravel 8 プロジェクトを Laravel 9 にアップグレードする場合は、アプリケーションの「信頼できるプロキシ」ミドルウェアを更新する必要がある場合があります。

<!-- Within your `app/Http/Middleware/TrustProxies.php` file, update `use Fideloper\Proxy\TrustProxies as Middleware` to `use Illuminate\Http\Middleware\TrustProxies as Middleware`. -->
`app/Http/Middleware/TrustProxies.php` ファイル内で、`use Fideloper\Proxy\TrustProxies as Middleware` を `use Illuminate\Http\Middleware\TrustProxies as Middleware` に更新します。

<!-- Next, within `app/Http/Middleware/TrustProxies.php`, you should update the `$headers` property definition: -->
次に、`app/Http/Middleware/TrustProxies.php` 内で、`$headers` プロパティ定義を更新する必要があります。

```php
// Before...
protected $headers = Request::HEADER_X_FORWARDED_ALL;

// After...
protected $headers =
    Request::HEADER_X_FORWARDED_FOR |
    Request::HEADER_X_FORWARDED_HOST |
    Request::HEADER_X_FORWARDED_PORT |
    Request::HEADER_X_FORWARDED_PROTO |
    Request::HEADER_X_FORWARDED_AWS_ELB;
```

<!-- Finally, you can remove the `fideloper/proxy` Composer dependency from your application: -->
最後に、アプリケーションから `fideloper/proxy` Composer 依存関係を削除できます。

```shell
composer remove fideloper/proxy
```

<!-- ### Validation -->
### Validation

<!-- #### Form Request `validated` Method -->
#### Form Request `validated` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `validated` method offered by form requests now accepts `$key` and `$default` arguments. If you are manually overwriting the definition of this method, you should update your method's signature to reflect these new arguments: -->
フォームリクエストによって提供される `validated` メソッドは、`$key` および `$default` 引数を受け入れるようになりました。このメソッドの定義を手動で上書きする場合は、次の新しい引数を反映するようにメソッドのシグネチャを更新する必要があります。

```php
public function validated($key = null, $default = null)
```

<a name="the-password-rule"></a>
<!-- #### The `password` Rule -->
#### The `password` Rule

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The `password` rule, which validates that the given input value matches the authenticated user's current password, has been renamed to `current_password`. -->
指定された入力値が認証されたユーザーの現在のパスワードと一致することを検証する `password` ルールの名前が `current_password` に変更されました。

<a name="unvalidated-array-keys"></a>
<!-- #### Unvalidated Array Keys -->
#### Unvalidated Array Keys

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- In previous releases of Laravel, you were required to manually instruct Laravel's validator to exclude unvalidated array keys from the "validated" data it returns, especially in combination with an `array` rule that does not specify a list of allowed keys. -->
Laravel の以前のリリースでは、特に許可されたキーのリストを指定しない `array` ルールと組み合わせた場合、Laravel のバリデーターが返す「検証済み」データから未検証の配列キーを除外するように手動で指示する必要がありました。

<!-- However, in Laravel 9.x, unvalidated array keys are always excluded from the "validated" data even when no allowed keys have been specified via the `array` rule. Typically, this behavior is the most expected behavior and the previous `excludeUnvalidatedArrayKeys` method was only added to Laravel 8.x as a temporary measure in order to preserve backwards compatibility. -->
ただし、Laravel 9.x では、`array` ルールで許可されたキーが指定されていない場合でも、未検証の配列キーは常に「検証済み」データから除外されます。通常、この動作は最も予期される動作であり、以前の `excludeUnvalidatedArrayKeys` メソッドは、下位互換性を維持するための一時的な措置として Laravel 8.x に追加されただけです。

<!-- Although it is not recommended, you may opt-in to the previous Laravel 8.x behavior by invoking a new `includeUnvalidatedArrayKeys` method within the `boot` method of one of your application's service providers: -->
推奨されませんが、アプリケーションのサービスプロバイダのいずれかの `boot` メソッド内で新しい `includeUnvalidatedArrayKeys` メソッドを呼び出すことで、以前の Laravel 8.x の動作をオプトインできます。

```php
use Illuminate\Support\Facades\Validator;

/**
 * Register any application services.
 *
 * @return void
 */
public function boot()
{
    Validator::includeUnvalidatedArrayKeys();
}
```

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/8.x...9.x) and choose which updates are important to you. -->
`laravel/laravel` [GitHub repository](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。 [GitHub comparison tool](https://github.com/laravel/laravel/compare/8.x...9.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。

