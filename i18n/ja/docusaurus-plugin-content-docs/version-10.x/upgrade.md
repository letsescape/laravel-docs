<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading to 10.0 from 9.x](#upgrade-10.0)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating Minimum Stability](#updating-minimum-stability)

<!-- </div> -->
</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Database Expressions](#database-expressions)
- [Model "Dates" Property](#model-dates-property)
- [Monolog 3](#monolog-3)
- [Redis Cache Tags](#redis-cache-tags)
- [Service Mocking](#service-mocking)
- [The Language Directory](#language-directory)

<!-- </div> -->
</div>

<a name="low-impact-changes"></a>
<!-- ## Low Impact Changes -->
## Low Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Closure Validation Rule Messages](#closure-validation-rule-messages)
- [Form Request `after` Method](#form-request-after-method)
- [Public Path Binding](#public-path-binding)
- [Query Exception Constructor](#query-exception-constructor)
- [Rate Limiter Return Values](#rate-limiter-return-values)
- [The `Redirect::home` Method](#redirect-home)
- [The `Bus::dispatchNow` Method](#dispatch-now)
- [The `registerPolicies` Method](#register-policies)
- [ULID Columns](#ulid-columns)

<!-- </div> -->
</div>

<a name="upgrade-10.0"></a>
<!-- ## Upgrading to 10.0 from 9.x -->
## Upgrading to 10.0 from 9.x

<a name="estimated-upgrade-time-??-minutes"></a>
<!-- #### Estimated Upgrade Time: 10 Minutes -->
#### Estimated Upgrade Time: 10 Minutes

> [!NOTE]
> 私たちは、考えられるすべての重大な変更を文書化するよう努めます。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。時間を節約したいですか? [Laravel Shift](https://laravelshift.com/) を使用すると、アプリケーションのアップグレードを自動化できます。

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- #### PHP 8.1.0 Required -->
#### PHP 8.1.0 Required

<!-- Laravel now requires PHP 8.1.0 or greater. -->
Laravel には PHP 8.1.0 以降が必要になりました。

<!-- #### Composer 2.2.0 Required -->
#### Composer 2.2.0 Required

<!-- Laravel now requires [Composer](https://getcomposer.org) 2.2.0 or greater. -->
Laravel には [Composer](https://getcomposer.org) 2.2.0 以降が必要になりました。

<!-- #### Composer Dependencies -->
#### Composer Dependencies

<!-- You should update the following dependencies in your application's `composer.json` file: -->
アプリケーションの `composer.json` ファイル内の次の依存関係を更新する必要があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `laravel/framework` to `^10.0`
- `laravel/sanctum` to `^3.2`
- `doctrine/dbal` to `^3.0`
- `spatie/laravel-ignition` to `^2.0`
- `laravel/passport` to `^11.0` ([Upgrade Guide](https://github.com/laravel/passport/blob/11.x/UPGRADE.md))
- `laravel/ui` to `^4.0`
-->
- `laravel/framework` ～ `^10.0`
- `laravel/sanctum` ～ `^3.2`
- `doctrine/dbal` ～ `^3.0`
- `spatie/laravel-ignition` ～ `^2.0`
- `laravel/passport` ～ `^11.0` ([Upgrade Guide](https://github.com/laravel/passport/blob/11.x/UPGRADE.md))
- `laravel/ui` ～ `^4.0`

<!-- </div> -->
</div>

<!-- If you are upgrading to Sanctum 3.x from the 2.x release series, please consult the [Sanctum upgrade guide](https://github.com/laravel/sanctum/blob/3.x/UPGRADE.md). -->
2.x リリース シリーズから Sanctum 3.x にアップグレードする場合は、[Sanctum upgrade guide](https://github.com/laravel/sanctum/blob/3.x/UPGRADE.md) を参照してください。

<!-- Furthermore, if you wish to use [PHPUnit 10](https://phpunit.de/announcements/phpunit-10.html), you should delete the `processUncoveredFiles` attribute from the `<coverage>` section of your application's `phpunit.xml` configuration file. Then, update the following dependencies in your application's `composer.json` file: -->
さらに、[PHPUnit 10](https://phpunit.de/announcements/phpunit-10.html) を使用したい場合は、アプリケーションの `phpunit.xml` 構成ファイルの `<coverage>` セクションから `processUncoveredFiles` 属性を削除する必要があります。次に、アプリケーションの `composer.json` ファイル内の次の依存関係を更新します。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `nunomaduro/collision` to `^7.0`
- `phpunit/phpunit` to `^10.0`
-->
- `nunomaduro/collision` ～ `^7.0`
- `phpunit/phpunit` ～ `^10.0`

<!-- </div> -->
</div>

<!-- Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 10 support. -->
最後に、アプリケーションで使用される他のサードパーティパッケージを調べて、Laravel 10 をサポートする適切なバージョンを使用していることを確認します。

<a name="updating-minimum-stability"></a>
<!-- #### Minimum Stability -->
#### Minimum Stability

<!-- You should update the `minimum-stability` setting in your application's `composer.json` file to `stable`. Or, since the default value of `minimum-stability` is `stable`, you may delete this setting from your application's `composer.json` file: -->
アプリケーションの `composer.json` ファイル内の `minimum-stability` 設定を `stable` に更新する必要があります。または、`minimum-stability` のデフォルト値は `stable` であるため、アプリケーションの `composer.json` ファイルからこの設定を削除することもできます。

```json
"minimum-stability": "stable",
```

<!-- ### Application -->
### Application

<a name="public-path-binding"></a>
<!-- #### Public Path Binding -->
#### Public Path Binding

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- If your application is customizing its "public path" by binding `path.public` into the container, you should instead update your code to invoke the `usePublicPath` method offered by the `Illuminate\Foundation\Application` object: -->
アプリケーションが `path.public` をコンテナーにバインドすることで「パブリック パス」をカスタマイズしている場合は、代わりにコードを更新して、`Illuminate\Foundation\Application` オブジェクトによって提供される `usePublicPath` メソッドを呼び出す必要があります。

```php
app()->usePublicPath(__DIR__.'/public');
```

<!-- ### Authorization -->
### Authorization

<a name="register-policies"></a>
<!-- ### The `registerPolicies` Method -->
### The `registerPolicies` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `registerPolicies` method of the `AuthServiceProvider` is now invoked automatically by the framework. Therefore, you may remove the call to this method from the `boot` method of your application's `AuthServiceProvider`. -->
`AuthServiceProvider` の `registerPolicies` メソッドがフレームワークによって自動的に呼び出されるようになりました。したがって、アプリケーションの `AuthServiceProvider` の `boot` メソッドからこのメソッドの呼び出しを削除できます。

<!-- ### Cache -->
### Cache

<a name="redis-cache-tags"></a>
<!-- #### Redis Cache Tags -->
#### Redis Cache Tags

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- Usage of `Cache::tags()` is only recommended for applications using Memcached. If you are using Redis as your application's cache driver, you should consider moving to Memcached or upgrade your application to Laravel [12.30.0](https://github.com/laravel/framework/pull/57098). -->
`Cache::tags()` の使用は、Memcached を使用するアプリケーションにのみ推奨されます。アプリケーションのキャッシュドライバとして Redis を使用している場合は、Memcached に移行するか、アプリケーションを Laravel [12.30.0](https://github.com/laravel/framework/pull/57098) にアップグレードすることを検討する必要があります。

<!-- ### Database -->
### Database

<a name="database-expressions"></a>
<!-- #### Database Expressions -->
#### Database Expressions

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- Database "expressions" (typically generated via `DB::raw`) have been rewritten in Laravel 10.x to offer additional functionality in the future. Notably, the grammar's raw string value must now be retrieved via the expression's `getValue(Grammar $grammar)` method. Casting an expression to a string using `(string)` is no longer supported. -->
データベースの「式」(通常は `DB::raw` によって生成される) は、将来追加機能を提供するために Laravel 10.x で書き直されました。特に、文法の生の文字列値は、式の `getValue(Grammar $grammar)` メソッドを介して取得する必要があることに注意してください。 `(string)` を使用した式の文字列へのcastはサポートされなくなりました。

<!-- **Typically, this does not affect end-user applications**; however, if your application is manually casting database expressions to strings using `(string)` or invoking the `__toString` method on the expression directly, you should update your code to invoke the `getValue` method instead: -->
**通常、これはエンドユーザー アプリケーションには影響しません**。ただし、アプリケーションが `(string)` を使用してデータベース式を手動で文字列にcastしている場合、または式に対して `__toString` メソッドを直接呼び出している場合は、代わりに `getValue` メソッドを呼び出すようにコードを更新する必要があります。

```php
use Illuminate\Support\Facades\DB;

$expression = DB::raw('select 1');

$string = $expression->getValue(DB::connection()->getQueryGrammar());
```

<a name="query-exception-constructor"></a>
<!-- #### Query Exception Constructor -->
#### Query Exception Constructor

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The `Illuminate\Database\QueryException` constructor now accepts a string connection name as its first argument. If your application is manually throwing this exception, you should adjust your code accordingly. -->
`Illuminate\Database\QueryException` コンストラクターは、最初の引数として文字列接続名を受け入れるようになりました。アプリケーションがこの例外を手動でスローしている場合は、それに応じてコードを調整する必要があります。

<a name="ulid-columns"></a>
<!-- #### ULID Columns -->
#### ULID Columns

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- When migrations invoke the `ulid` method without any arguments, the column will now be named `ulid`. In previous releases of Laravel, invoking this method without any arguments created a column erroneously named `uuid`: -->
移行で引数を指定せずに `ulid` メソッドを呼び出すと、列の名前は `ulid` になります。 Laravel の以前のリリースでは、引数を指定せずにこのメソッドを呼び出すと、誤って `uuid` という名前の列が作成されました。

```
$table->ulid();
```

<!-- To explicitly specify a column name when invoking the `ulid` method, you may pass the column name to the method: -->
`ulid` メソッドを呼び出すときに列名を明示的に指定するには、列名をメソッドに渡すことができます。

```
$table->ulid('ulid');
```

<!-- ### Eloquent -->
### Eloquent

<a name="model-dates-property"></a>
<!-- #### Model "Dates" Property -->
#### Model "Dates" Property

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The Eloquent model's deprecated `$dates` property has been removed. Your application should now use the `$casts` property: -->
Eloquent モデルの非推奨の `$dates` プロパティは削除されました。アプリケーションは `$casts` プロパティを使用する必要があります。

```php
protected $casts = [
    'deployed_at' => 'datetime',
];
```

<!-- ### Localization -->
### Localization

<a name="language-directory"></a>
<!-- #### The Language Directory -->
#### The Language Directory

<!-- **Likelihood Of Impact: None** -->
**影響の可能性: なし**

<!-- Though not relevant to existing applications, the Laravel application skeleton no longer contains the `lang` directory by default. Instead, when writing new Laravel applications, it may be published using the `lang:publish` Artisan command: -->
既存のアプリケーションには関係ありませんが、Laravel アプリケーション スケルトンにはデフォルトで `lang` ディレクトリが含まれなくなりました。代わりに、新しい Laravel アプリケーションを作成するときは、`lang:publish` Artisan コマンドを使用して公開できます。

```shell
php artisan lang:publish
```

<!-- ### Logging -->
### Logging

<a name="monolog-3"></a>
<!-- #### Monolog 3 -->
#### Monolog 3

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- Laravel's Monolog dependency has been updated to Monolog 3.x. If you are directly interacting with Monolog within your application, you should review Monolog's [upgrade guide](https://github.com/Seldaek/monolog/blob/main/UPGRADE.md). -->
Laravel の Monolog 依存関係が Monolog 3.x に更新されました。アプリケーション内で Monolog と直接対話している場合は、Monolog の [upgrade guide](https://github.com/Seldaek/monolog/blob/main/UPGRADE.md) を確認する必要があります。

<!-- If you are using third-party logging services such as BugSnag or Rollbar, you may need to upgrade those third-party packages to a version that supports Monolog 3.x and Laravel 10.x. -->
BugSnag や Rollbar などのサードパーティのログ サービスを使用している場合は、それらのサードパーティ パッケージを Monolog 3.x および Laravel 10.x をサポートするバージョンにアップグレードする必要がある場合があります。

<!-- ### Queues -->
### Queues

<a name="dispatch-now"></a>
<!-- #### The `Bus::dispatchNow` Method -->
#### The `Bus::dispatchNow` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The deprecated `Bus::dispatchNow` and `dispatch_now` methods have been removed. Instead, your application should use the `Bus::dispatchSync` and `dispatch_sync` methods, respectively. -->
非推奨の `Bus::dispatchNow` メソッドと `dispatch_now` メソッドは削除されました。代わりに、アプリケーションでは `Bus::dispatchSync` メソッドと `dispatch_sync` メソッドをそれぞれ使用する必要があります。

<a name="dispatch-return"></a>
<!-- #### The `dispatch()` Helper Return Value -->
#### The `dispatch()` Helper Return Value

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Invoking `dispatch` with a class that does not implement `Illuminate\Contracts\Queue` would previously return the result of the class's `handle` method. However, this will now return an `Illuminate\Foundation\Bus\PendingBatch` instance. You may use `dispatch_sync()` to replicate the previous behavior. -->
`Illuminate\Contracts\Queue` を実装していないクラスで `dispatch` を呼び出すと、以前はクラスの `handle` メソッドの結果が返されていました。ただし、これにより `Illuminate\Foundation\Bus\PendingBatch` インスタンスが返されるようになります。 `dispatch_sync()` を使用して、以前の動作を複製できます。

<!-- ### Routing -->
### Routing

<a name="middleware-aliases"></a>
<!-- #### Middleware Aliases -->
#### Middleware Aliases

<!-- **Likelihood Of Impact: Optional** -->
**影響の可能性: オプション**

<!-- In new Laravel applications, the `$routeMiddleware` property of the `App\Http\Kernel` class has been renamed to `$middlewareAliases` to better reflect its purpose. You are welcome to rename this property in your existing applications; however, it is not required. -->
新しい Laravel アプリケーションでは、その目的をより適切に反映するために、`App\Http\Kernel` クラスの `$routeMiddleware` プロパティの名前が `$middlewareAliases` に変更されました。既存のアプリケーションでこのプロパティの名前を変更しても構いません。ただし、必須ではありません。

<a name="rate-limiter-return-values"></a>
<!-- #### Rate Limiter Return Values -->
#### Rate Limiter Return Values

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- When invoking the `RateLimiter::attempt` method, the value returned by the provided closure will now be returned by the method. If nothing or `null` is returned, the `attempt` method will return `true`: -->
`RateLimiter::attempt` メソッドを呼び出すと、提供されたクロージャによって返される値がメソッドによって返されるようになります。何も返されない場合、または `null` が返された場合、`attempt` メソッドは `true` を返します。

```php
$value = RateLimiter::attempt('key', 10, fn () => ['example'], 1);

$value; // ['example']
```

<a name="redirect-home"></a>
<!-- #### The `Redirect::home` Method -->
#### The `Redirect::home` Method

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- The deprecated `Redirect::home` method has been removed. Instead, your application should redirect to an explicitly named route: -->
非推奨の `Redirect::home` メソッドは削除されました。代わりに、アプリケーションは明示的に名前を付けたルートにリダイレクトする必要があります。

```php
return Redirect::route('home');
```

<!-- ### Testing -->
### Testing

<a name="service-mocking"></a>
<!-- #### Service Mocking -->
#### Service Mocking

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The deprecated `MocksApplicationServices` trait has been removed from the framework. This trait provided testing methods such as `expectsEvents`, `expectsJobs`, and `expectsNotifications`. -->
非推奨の `MocksApplicationServices` 特性はフレームワークから削除されました。この特性により、`expectsEvents`、`expectsJobs`、`expectsNotifications` などのテスト メソッドが提供されました。

<!-- If your application uses these methods, we recommend you transition to `Event::fake`, `Bus::fake`, and `Notification::fake`, respectively. You can learn more about mocking via fakes in the corresponding documentation for the component you are attempting to fake. -->
アプリケーションでこれらのメソッドを使用している場合は、それぞれ `Event::fake`、`Bus::fake`、および `Notification::fake` に移行することをお勧めします。フェイクによるモックの詳細については、偽装しようとしているコンポーネントの対応するドキュメントを参照してください。

<!-- ### Validation -->
### Validation

<a name="closure-validation-rule-messages"></a>
<!-- #### Closure Validation Rule Messages -->
#### Closure Validation Rule Messages

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- When writing closure based custom validation rules, invoking the `$fail` callback more than once will now append the messages to an array instead of overwriting the previous message. Typically, this will not affect your application. -->
クロージャ ベースのカスタム検証ルールを作成する場合、`$fail` コールバックを複数回呼び出すと、前のメッセージを上書きするのではなく、メッセージが配列に追加されるようになりました。通常、これはアプリケーションには影響しません。

<!-- In addition, the `$fail` callback now returns an object. If you were previously type-hinting the return type of your validation closure, this may require you to update your type-hint: -->
さらに、`$fail` コールバックはオブジェクトを返すようになりました。以前に検証クロージャの戻り値の型をタイプヒントで指定していた場合は、タイプヒントの更新が必要になる場合があります。

```php
public function rules()
{
    'name' => [
        function ($attribute, $value, $fail) {
            $fail('validation.translation.key')->translate();
        },
    ],
}
```

<a name="validation-messages-and-closure-rules"></a>
<!-- #### Validation Messages and Closure Rules -->
#### Validation Messages and Closure Rules

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Previously, you could assign a failure message to a different key by providing an array to the `$fail` callback injected into Closure based validation rules. However, you should now provide the key as the first argument and the failure message as the second argument: -->
以前は、クロージャ ベースの検証ルールに挿入される `$fail` コールバックに配列を提供することで、失敗メッセージを別のキーに割り当てることができました。ただし、最初の引数としてキーを指定し、2 番目の引数として失敗メッセージを指定する必要があります。

```php
Validator::make([
    'foo' => 'string',
    'bar' => [function ($attribute, $value, $fail) {
        $fail('foo', 'Something went wrong!');
    }],
]);
```

<a name="form-request-after-method"></a>
<!-- #### Form Request After Method -->
#### Form Request After Method

<!-- **Likelihood Of Impact: Very Low** -->
**影響の可能性: 非常に低い**

<!-- Within form requests, the `after` method is now [reserved by Laravel](https://github.com/laravel/framework/pull/46757). If your form requests define an `after` method, the method should be renamed or modified to utilize the new "after validation" feature of Laravel's form requests. -->
フォームリクエスト内では、`after` メソッドは [reserved by Laravel](https://github.com/laravel/framework/pull/46757) になりました。フォームリクエストで `after` メソッドが定義されている場合は、Laravel のフォームリクエストの新しい「検証後」機能を利用するようにメソッドの名前を変更または変更する必要があります。

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. -->
`laravel/laravel` [GitHub repository](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。

<!-- You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/9.x...10.x) and choose which updates are important to you. However, many of the changes shown by the GitHub comparison tool are due to our organization's adoption of PHP native types. These changes are backwards compatible and the adoption of them during the migration to Laravel 10 is optional. -->
[GitHub comparison tool](https://github.com/laravel/laravel/compare/9.x...10.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。ただし、GitHub 比較ツールによって示される変更の多くは、組織が PHP ネイティブ タイプを採用したことによるものです。これらの変更には下位互換性があり、Laravel 10 への移行中の変更の導入はオプションです。

