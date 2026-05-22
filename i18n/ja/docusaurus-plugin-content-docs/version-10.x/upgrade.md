# アップグレードガイド (Upgrade Guide)

- [9.x から 10.0 へのアップグレード](#upgrade-10.0)

<a name="high-impact-changes"></a>
## 大きな影響を与える変更 (High Impact Changes)

<div class="content-list" markdown="1">

- [依存関係の更新](#updating-dependencies)
- [最小安定性の更新](#updating-minimum-stability)

</div>

<a name="medium-impact-changes"></a>
## 中程度の影響のある変更 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [データベース式](#database-expressions)
- [モデルの「日付」プロパティ](#model-dates-property)
- [モノローグ3](#monolog-3)
- [Redis キャッシュのタグ](#redis-cache-tags)
- [サービスモッキング](#service-mocking)
- [言語ディレクトリ](#language-directory)

</div>

<a name="low-impact-changes"></a>
## 影響の少ない変更 (Low Impact Changes)

<div class="content-list" markdown="1">

- [クロージャ検証ルールのメッセージ](#closure-validation-rule-messages)
- [フォームリクエスト `after` メソッド](#form-request-after-method)
- [パブリックパスバインディング](#public-path-binding)
- [クエリ例外コンストラクター](#query-exception-constructor)
- [レート リミッタの戻り値](#rate-limiter-return-values)
- [The `Redirect::home` Method](#redirect-home)
- [The `Bus::dispatchNow` Method](#dispatch-now)
- [`registerPolicies` メソッド](#register-policies)
- [ULID列](#ulid-columns)

</div>

<a name="upgrade-10.0"></a>
## 9.x から 10.0 へのアップグレード (Upgrading to 10.0 from 9.x)

<a name="estimated-upgrade-time-??-minutes"></a>
#### アップグレードの推定時間: 10 分

> [!NOTE]  
> 私たちは、考えられるすべての重大な変更を文書化するよう努めます。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。時間を節約したいですか? [Laravelシフト](https://laravelshift.com/) を使用すると、アプリケーションのアップグレードを自動化できます。

<a name="updating-dependencies"></a>
### 依存関係の更新

**影響の可能性: 高**

#### PHP 8.1.0が必要

Laravel には PHP 8.1.0 以降が必要になりました。

#### Composer 2.2.0 が必要

Laravel には [Composer](https://getcomposer.org) 2.2.0 以降が必要になりました。

#### Composer の依存関係

アプリケーションの `composer.json` ファイル内の次の依存関係を更新する必要があります。

<div class="content-list" markdown="1">

- `laravel/framework` ～ `^10.0`
- `laravel/sanctum` ～ `^3.2`
- `doctrine/dbal` ～ `^3.0`
- `spatie/laravel-ignition` ～ `^2.0`
- `laravel/passport` ～ `^11.0` ([アップグレードガイド](https://github.com/laravel/passport/blob/11.x/UPGRADE.md))
- `laravel/ui` ～ `^4.0`

</div>

2.x リリース シリーズから Sanctum 3.x にアップグレードする場合は、[Sanctumアップグレードガイド](https://github.com/laravel/sanctum/blob/3.x/UPGRADE.md) を参照してください。

さらに、[PHPUユニット 10](https://phpunit.de/announcements/phpunit-10.html) を使用したい場合は、アプリケーションの `phpunit.xml` 構成ファイルの `<coverage>` セクションから `processUncoveredFiles` 属性を削除する必要があります。次に、アプリケーションの `composer.json` ファイル内の次の依存関係を更新します。

<div class="content-list" markdown="1">

- `nunomaduro/collision` ～ `^7.0`
- `phpunit/phpunit` ～ `^10.0`

</div>

最後に、アプリケーションで使用される他のサードパーティパッケージを調べて、Laravel 10 をサポートする適切なバージョンを使用していることを確認します。

<a name="updating-minimum-stability"></a>
#### 最小の安定性

アプリケーションの `composer.json` ファイル内の `minimum-stability` 設定を `stable` に更新する必要があります。または、`minimum-stability` のデフォルト値は `stable` であるため、アプリケーションの `composer.json` ファイルからこの設定を削除することもできます。

```json
"minimum-stability": "stable",
```

### 応用

<a name="public-path-binding"></a>
#### パブリックパスバインディング

**影響の可能性: 低い**

アプリケーションが `path.public` をコンテナーにバインドすることで「パブリック パス」をカスタマイズしている場合は、代わりにコードを更新して、`Illuminate\Foundation\Application` オブジェクトによって提供される `usePublicPath` メソッドを呼び出す必要があります。

```php
app()->usePublicPath(__DIR__.'/public');
```

### 認可

<a name="register-policies"></a>
### `registerPolicies` メソッド

**影響の可能性: 低い**

`AuthServiceProvider` の `registerPolicies` メソッドがフレームワークによって自動的に呼び出されるようになりました。したがって、アプリケーションの `AuthServiceProvider` の `boot` メソッドからこのメソッドの呼び出しを削除できます。

### キャッシュ

<a name="redis-cache-tags"></a>
#### Redis キャッシュのタグ

**影響の可能性: 中**

`Cache::tags()` の使用は、Memcached を使用するアプリケーションにのみ推奨されます。アプリケーションのキャッシュドライバとして Redis を使用している場合は、Memcached に移行するか、アプリケーションを Laravel [12.30.0](https://github.com/laravel/framework/pull/57098) にアップグレードすることを検討する必要があります。

### データベース

<a name="database-expressions"></a>
#### データベース式

**影響の可能性: 中**

データベースの「式」(通常は `DB::raw` によって生成される) は、将来追加機能を提供するために Laravel 10.x で書き直されました。特に、文法の生の文字列値は、式の `getValue(Grammar $grammar)` メソッドを介して取得する必要があることに注意してください。 `(string)` を使用した式の文字列へのキャストはサポートされなくなりました。

**通常、これはエンドユーザー アプリケーションには影響しません**。ただし、アプリケーションが `(string)` を使用してデータベース式を手動で文字列にキャストしている場合、または式に対して `__toString` メソッドを直接呼び出している場合は、代わりに `getValue` メソッドを呼び出すようにコードを更新する必要があります。

```php
use Illuminate\Support\Facades\DB;

$expression = DB::raw('select 1');

$string = $expression->getValue(DB::connection()->getQueryGrammar());
```

<a name="query-exception-constructor"></a>
#### クエリ例外コンストラクター

**影響の可能性: 非常に低い**

`Illuminate\Database\QueryException` コンストラクターは、最初の引数として文字列接続名を受け入れるようになりました。アプリケーションがこの例外を手動でスローしている場合は、それに応じてコードを調整する必要があります。

<a name="ulid-columns"></a>
#### ULID列

**影響の可能性: 低い**

移行で引数を指定せずに `ulid` メソッドを呼び出すと、列の名前は `ulid` になります。 Laravel の以前のリリースでは、引数を指定せずにこのメソッドを呼び出すと、誤って `uuid` という名前の列が作成されました。

    $table->ulid();

`ulid` メソッドを呼び出すときに列名を明示的に指定するには、列名をメソッドに渡すことができます。

    $table->ulid('ulid');

### Eloquent

<a name="model-dates-property"></a>
#### モデルの「日付」プロパティ

**影響の可能性: 中**

Eloquent モデルの非推奨の `$dates` プロパティは削除されました。アプリケーションは `$casts` プロパティを使用する必要があります。

```php
protected $casts = [
    'deployed_at' => 'datetime',
];
```

### ローカリゼーション

<a name="language-directory"></a>
#### 言語ディレクトリ

**影響の可能性: なし**

既存のアプリケーションには関係ありませんが、Laravel アプリケーション スケルトンにはデフォルトで `lang` ディレクトリが含まれなくなりました。代わりに、新しい Laravel アプリケーションを作成するときは、`lang:publish` Artisan コマンドを使用して公開できます。

```shell
php artisan lang:publish
```

### ロギング

<a name="monolog-3"></a>
#### モノローグ3

**影響の可能性: 中**

Laravel の Monolog 依存関係が Monolog 3.x に更新されました。アプリケーション内で Monolog と直接対話している場合は、Monolog の [アップグレードガイド](https://github.com/Seldaek/monolog/blob/main/UPGRADE.md) を確認する必要があります。

BugSnag や Rollbar などのサードパーティのログ サービスを使用している場合は、それらのサードパーティ パッケージを Monolog 3.x および Laravel 10.x をサポートするバージョンにアップグレードする必要がある場合があります。

### キュー

<a name="dispatch-now"></a>
#### `Bus::dispatchNow` メソッド

**影響の可能性: 低い**

非推奨の `Bus::dispatchNow` メソッドと `dispatch_now` メソッドは削除されました。代わりに、アプリケーションでは `Bus::dispatchSync` メソッドと `dispatch_sync` メソッドをそれぞれ使用する必要があります。

<a name="dispatch-return"></a>
#### `dispatch()` ヘルパの戻り値

**影響の可能性: 低い**

`Illuminate\Contracts\Queue` を実装していないクラスで `dispatch` を呼び出すと、以前はクラスの `handle` メソッドの結果が返されていました。ただし、これにより `Illuminate\Foundation\Bus\PendingBatch` インスタンスが返されるようになります。 `dispatch_sync()` を使用して、以前の動作を複製できます。

### ルーティング

<a name="middleware-aliases"></a>
#### ミドルウェアのエイリアス

**影響の可能性: オプション**

新しい Laravel アプリケーションでは、その目的をより適切に反映するために、`App\Http\Kernel` クラスの `$routeMiddleware` プロパティの名前が `$middlewareAliases` に変更されました。既存のアプリケーションでこのプロパティの名前を変更しても構いません。ただし、必須ではありません。

<a name="rate-limiter-return-values"></a>
#### レート リミッタの戻り値

**影響の可能性: 低い**

`RateLimiter::attempt` メソッドを呼び出すと、提供されたクロージャによって返される値がメソッドによって返されるようになります。何も返されない場合、または `null` が返された場合、`attempt` メソッドは `true` を返します。

```php
$value = RateLimiter::attempt('key', 10, fn () => ['example'], 1);

$value; // ['example']
```

<a name="redirect-home"></a>
#### `Redirect::home` メソッド

**影響の可能性: 非常に低い**

非推奨の `Redirect::home` メソッドは削除されました。代わりに、アプリケーションは明示的に名前を付けたルートにリダイレクトする必要があります。

```php
return Redirect::route('home');
```

### テスト

<a name="service-mocking"></a>
#### サービスモッキング

**影響の可能性: 中**

非推奨の `MocksApplicationServices` 特性はフレームワークから削除されました。この特性により、`expectsEvents`、`expectsJobs`、`expectsNotifications` などのテスト メソッドが提供されました。

アプリケーションでこれらのメソッドを使用している場合は、それぞれ `Event::fake`、`Bus::fake`、および `Notification::fake` に移行することをお勧めします。フェイクによるモックの詳細については、偽装しようとしているコンポーネントの対応するドキュメントを参照してください。

### 検証

<a name="closure-validation-rule-messages"></a>
#### クロージャ検証ルールのメッセージ

**影響の可能性: 非常に低い**

クロージャ ベースのカスタム検証ルールを作成する場合、`$fail` コールバックを複数回呼び出すと、前のメッセージを上書きするのではなく、メッセージが配列に追加されるようになりました。通常、これはアプリケーションには影響しません。

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
#### 検証メッセージと終了ルール

**影響の可能性: 非常に低い**

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
#### メソッド後のフォームリクエスト

**影響の可能性: 非常に低い**

フォームリクエスト内では、`after` メソッドは [Laravelによって予約されています](https://github.com/laravel/framework/pull/46757) になりました。フォームリクエストで `after` メソッドが定義されている場合は、Laravel のフォームリクエストの新しい「検証後」機能を利用するようにメソッドの名前を変更または変更する必要があります。

<a name="miscellaneous"></a>
### その他

`laravel/laravel` [GitHub リポジトリ](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。

[GitHub比較ツール](https://github.com/laravel/laravel/compare/9.x...10.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。ただし、GitHub 比較ツールによって示される変更の多くは、組織が PHP ネイティブ タイプを採用したことによるものです。これらの変更には下位互換性があり、Laravel 10 への移行中の変更の導入はオプションです。

