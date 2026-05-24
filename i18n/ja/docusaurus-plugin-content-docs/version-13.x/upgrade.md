# アップグレードガイド (Upgrade Guide)

- [12.x から 13.0 へのアップグレード](#upgrade-13.0)
    - [AIを活用したアップグレード](#upgrading-using-ai)

<a name="high-impact-changes"></a>
## 大きな影響を与える変更 (High Impact Changes)

<div class="content-list" markdown="1">

- [依存関係の更新](#updating-dependencies)
- [Laravelインストーラーの更新](#updating-the-laravel-installer)
- [偽造防止のリクエスト](#request-forgery-protection)

</div>

<a name="medium-impact-changes"></a>
## 中程度の影響のある変更 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [キャッシュ `serializable_classes` 構成](#cache-serializable_classes-configuration)
- [MySQL または MariaDB を使用したデータベース `upsert`](#database-upsert-mariadb-mysql)

</div>

<a name="low-impact-changes"></a>
## 影響の少ない変更 (Low Impact Changes)

<div class="content-list" markdown="1">

- [キャッシュプレフィックスとセッションCookie名](#cache-prefixes-and-session-cookie-names)
- [コレクション モデルのシリアル化により、熱心に読み込まれた関係が復元されます](#collection-model-serialization-restores-eager-loaded-relations)
- [`Container::call` and Nullable Class Defaults](#containercall-and-nullable-class-defaults)
- [ドメインルート登録の優先順位](#domain-route-registration-precedence)
- [`JobAttempted` イベント例外ペイロード](#jobattempted-event-exception-payload)
- [マネージャー `extend` コールバック バインディング](#manager-extend-callback-binding)
- [`JOIN`、`ORDER BY`、および `LIMIT` を使用した MySQL `DELETE` クエリ](#mysql-delete-queries-with-join-order-by-and-limit)
- [ページネーション ブートストラップ ビュー名](#pagination-bootstrap-view-names)
- [多態性ピボット テーブル名の生成](#polymorphic-pivot-table-name-generation)
- [`QueueBusy` イベント プロパティの名前変更](#queuebusy-event-property-rename)
- [`Str` テスト間でのファクトリーリセット](#str-factories-reset-between-tests)

</div>

<a name="upgrade-13.0"></a>
## 12.x から 13.0 へのアップグレード (Upgrading To 13.0 From 12.x)

#### アップグレードの推定時間: 10 分

> [!NOTE]
> 私たちは、考えられるすべての重大な変更を文書化するよう努めます。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。時間を節約するには、[Shift](https://laravelshift.com) を使用できます。 Shift は、Laravel のアップグレードを自動化するコミュニティによって管理されるサービスです。

<a name="upgrading-using-ai"></a>
### AIを活用したアップグレード

[Laravelブースト](https://github.com/laravel/boost) を使用してアップグレードを自動化できます。 Boost は、AI アシスタントにガイド付きアップグレード プロンプトを提供するファーストパーティ MCP サーバーです。Laravel 12 アプリケーションにインストールしたら、Claude Code、Cursor、OpenCode、Gemini、または VS Code で `/upgrade-laravel-v13` スラッシュ コマンドを使用して、Laravel 13 へのアップグレードを開始します。このコマンドには、Laravel Boost `^2.0` が必要です。

<a name="updating-dependencies"></a>
### 依存関係の更新

**影響の可能性: 高**

アプリケーションの `composer.json` ファイル内の次の依存関係を更新する必要があります。

<div class="content-list" markdown="1">

- `laravel/framework` ～ `^13.0`
- `laravel/boost` ～ `^2.0`
- `laravel/tinker` ～ `^3.0`
- `phpunit/phpunit` ～ `^12.0`
- `pestphp/pest` ～ `^4.0`

</div>

<a name="updating-the-laravel-installer"></a>
### Laravelインストーラーの更新

Laravel インストーラー CLI ツールを使用して新しい Laravel アプリケーションを作成している場合は、Laravel 13.x との互換性を確保するためにインストーラーのインストールを更新する必要があります。

`composer global require` 経由で Laravel インストーラーをインストールした場合は、`composer global update` を使用してインストーラーを更新できます。

```shell
composer global update laravel/installer
```

または、Laravel インストーラーの [Laravel・ハードの](https://herd.laravel.com) バンドル コピーを使用している場合は、Herd インストールを最新リリースに更新する必要があります。

<a name="cache"></a>
### キャッシュ

<a name="cache-prefixes-and-session-cookie-names"></a>
#### キャッシュプレフィックスとセッションCookie名

**影響の可能性: 低い**

Laravel のデフォルトのキャッシュと Redis キーのプレフィックスは、ハイフンで区切られたサフィックスを使用するようになりました。

ほとんどのアプリケーションでは、アプリケーション レベルの構成ファイルでこれらの値がすでに定義されているため、この変更は適用されません。これは主に、対応するアプリケーション構成値が存在しない場合にフレームワーク レベルのフォールバック構成に依存するアプリケーションに影響します。

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

以前の動作を保持するには、環境内で `CACHE_PREFIX`、`REDIS_PREFIX`、および `SESSION_COOKIE` を明示的に構成します。

<a name="store-and-repository-contracts-touch"></a>
#### `Store` および `Repository` 契約: `touch`

**影響の可能性: 非常に低い**

キャッシュ コントラクトには、アイテム TTL を拡張するための `touch` メソッドが含まれるようになりました。カスタム キャッシュ ストアの実装を維持する場合は、次のメソッドを追加する必要があります。

```php
// Illuminate\Contracts\Cache\Store
public function touch($key, $seconds);
```

<a name="cache-serializable_classes-configuration"></a>
#### キャッシュ `serializable_classes` 構成

**影響の可能性: 中**

デフォルトのアプリケーションの `cache` 構成には、`false` に設定された `serializable_classes` オプションが含まれるようになりました。これにより、キャッシュのシリアル化解除動作が強化され、アプリケーションの `APP_KEY` が漏洩した場合に PHP シリアル化解除ガジェット チェーン攻撃を防ぐことができます。アプリケーションが意図的に PHP オブジェクトをキャッシュに保存する場合は、シリアル化解除される可能性のあるクラスを明示的にリストする必要があります。

```php
'serializable_classes' => [
    App\Data\CachedDashboardStats::class,
    App\Support\CachedPricingSnapshot::class,
],
```

アプリケーションが以前に任意のキャッシュされたオブジェクトのシリアル化解除に依存していた場合は、その使用法を明示的なクラス許可リストまたは非オブジェクト キャッシュ ペイロード (配列など) に移行する必要があります。

<a name="container"></a>
### 容器

<a name="containercall-and-nullable-class-defaults"></a>
#### `Container::call` および Null 許容クラスのデフォルト

**影響の可能性: 低い**

`Container::call` は、バインディングが存在しない場合に null 許容クラス パラメーターのデフォルトを尊重するようになり、Laravel 12 で導入されたコンストラクター インジェクション動作と一致します。

```php
$container->call(function (?Carbon $date = null) {
    return $date;
});

// Laravel <= 12.x: Carbon instance
// Laravel >= 13.x: null
```

メソッド呼び出し挿入ロジックが以前の動作に依存していた場合は、それを更新する必要がある場合があります。

<a name="contracts"></a>
### 契約

<a name="dispatcher-contract-dispatchafterresponse"></a>
#### `Dispatcher` 契約: `dispatchAfterResponse`

**影響の可能性: 非常に低い**

`Illuminate\Contracts\Bus\Dispatcher` コントラクトに `dispatchAfterResponse($command, $handler = null)` メソッドが含まれるようになりました。

カスタム ディスパッチャ実装を維持する場合は、このメソッドをクラスに追加します。

<a name="responsefactory-contract-eventstream"></a>
#### `ResponseFactory` 契約: `eventStream`

**影響の可能性: 非常に低い**

`Illuminate\Contracts\Routing\ResponseFactory` コントラクトに `eventStream` 署名が含まれるようになりました。

このコントラクトのカスタム実装を維持する場合は、このメソッドを追加する必要があります。

<a name="mustverifyemail-contract-markemailasunverified"></a>
#### `MustVerifyEmail` 契約: `markEmailAsUnverified`

**影響の可能性: 非常に低い**

`Illuminate\Contracts\Auth\MustVerifyEmail` コントラクトに `markEmailAsUnverified()` が含まれるようになりました。

このコントラクトのカスタム実装を提供する場合は、互換性を維持するためにこのメソッドを追加してください。

<a name="database"></a>
### データベース

<a name="database-upsert-mariadb-mysql"></a>
#### MySQL または MariaDB を使用したデータベース `upsert`

**影響の可能性: 中**

Laravel は、呼び出し元が `uniqueBy` に空ではない値を提供していることを検証し、無効な SQL を生成する代わりに `InvalidArgumentException` をスローするようになりました。

MariaDB および MySQL データベース ドライバは `uniqueBy` 値を無視し、常にテーブルのプライマリ インデックスと一意のインデックスを使用して既存のレコードを検出しますが、検証は引き続き適用されます。 `uniqueBy` が空の場合、`InvalidArgumentException` がスローされます。

<a name="mysql-delete-queries-with-join-order-by-and-limit"></a>
#### `JOIN`、`ORDER BY`、および `LIMIT` を使用した MySQL `DELETE` クエリ

**影響の可能性: 低い**

Laravel は、MySQL 文法用の `ORDER BY` および `LIMIT` を含む完全な `DELETE ... JOIN` クエリをコンパイルするようになりました。

以前のバージョンでは、結合削除時に `ORDER BY` / `LIMIT` 句がサイレントに無視される可能性がありました。 Laravel 13 では、これらの句は生成される SQL に含まれます。その結果、この構文をサポートしないデータベース エンジン (標準の MySQL / MariaDB バリアントなど) は、無制限の削除を実行する代わりに `QueryException` をスローする可能性があります。

<a name="eloquent"></a>
### Eloquent

<a name="model-booting-and-nested-instantiation"></a>
#### モデルのブートとネストされたインスタンス化

**影響の可能性: 非常に低い**

モデルの起動中に新しいモデル インスタンスを作成することは禁止され、`LogicException` がスローされます。

これは、モデル `boot` メソッドまたは特性 `boot*` メソッド内からモデルをインスタンス化するコードに影響します。

```php
protected static function boot()
{
    parent::boot();

    // No longer allowed during booting...
    (new static())->getTable();
}
```

ネストされたブートを避けるために、このロジックをブート サイクルの外側に移動します。

<a name="polymorphic-pivot-table-name-generation"></a>
#### 多態性ピボット テーブル名の生成

**影響の可能性: 低い**

カスタムピボットモデルクラスを使用して多態性ピボットモデルのテーブル名が推論されると、Laravel は複数形の名前を生成するようになりました。

アプリケーションがモーフ ピボット テーブルの以前の単数形の推論名に依存し、カスタム ピボット クラスを使用していた場合は、ピボット モデルでテーブル名を明示的に定義する必要があります。

<a name="collection-model-serialization-restores-eager-loaded-relations"></a>
#### コレクション モデルのシリアル化により、熱心に読み込まれた関係が復元されます

**影響の可能性: 低い**

Eloquent モデル コレクションがシリアル化されて復元されるとき (キューに入れられたジョブなど)、コレクションのモデルに対して一括ロードされたリレーションが復元されるようになりました。

コードが、逆シリアル化後に存在しないリレーションに依存している場合は、そのロジックを調整する必要がある場合があります。

<a name="http-client"></a>
### HTTPクライアント

<a name="http-client-response-throw-and-throwif-signatures"></a>
#### HTTP クライアント `Response::throw` および `throwIf` 署名

**影響の可能性: 非常に低い**

HTTP クライアント応答メソッドは、メソッド シグネチャでコールバック パラメータを宣言するようになりました。

```php
public function throw($callback = null);
public function throwIf($condition, $callback = null);
```

カスタム応答クラスでこれらのメソッドをオーバーライドする場合は、メソッドのシグネチャに互換性があることを確認してください。

<a name="notifications"></a>
### 通知

<a name="default-password-reset-subject"></a>
#### デフォルトのパスワードリセットの件名

**影響の可能性: 非常に低い**

Laravelのデフォルトのパスワードリセットメールの件名が変更されました:

```text
// Laravel <= 12.x
Reset Password Notification

// Laravel >= 13.x
Reset your password
```

テスト、アサーション、または変換のオーバーライドが以前のデフォルト文字列に依存している場合は、それに応じてそれらを更新します。

<a name="queued-notifications-and-missing-models"></a>
#### キューに登録された通知と欠落しているモデル

**影響の可能性: 非常に低い**

キューに入れられた通知は、通知クラスで定義された `#[DeleteWhenMissingModels]` 属性と `$deleteWhenMissingModels` プロパティを尊重するようになりました。

以前のバージョンでは、モデルが欠落していると、キューに入れられた通知ジョブが削除されると予想していた場合に失敗する可能性がありました。

<a name="queue"></a>
### 列

<a name="jobattempted-event-exception-payload"></a>
#### `JobAttempted` イベント例外ペイロード

**影響の可能性: 低い**

`Illuminate\Queue\Events\JobAttempted` イベントは、以前のブール型 `$exceptionOccurred` プロパティを置き換えて、`$exception` 経由で例外オブジェクト (または `null`) を公開するようになりました。

```php
// Laravel <= 12.x
$event->exceptionOccurred;

// Laravel >= 13.x
$event->exception;
```

このイベントをリッスンする場合は、それに応じてリスナ コードを更新してください。

<a name="queuebusy-event-property-rename"></a>
#### `QueueBusy` イベント プロパティの名前変更

**影響の可能性: 低い**

他のキュー イベントとの一貫性を保つために、`Illuminate\Queue\Events\QueueBusy` イベント プロパティ `$connection` の名前が `$connectionName` に変更されました。

リスナが `$connection` を参照している場合は、`$connectionName` に更新します。

<a name="queue-contract-method-additions"></a>
#### `Queue` 契約方法の追加

**影響の可能性: 非常に低い**

`Illuminate\Contracts\Queue\Queue` コントラクトには、以前は docblock でのみ宣言されていたキュー サイズ検査メソッドが含まれるようになりました。

このコントラクトのカスタム キュー ドライバ実装を維持する場合は、次の実装を追加します。

<div class="content-list" markdown="1">

- `pendingSize`
- `delayedSize`
- `reservedSize`
- `creationTimeOfOldestPendingJob`

</div>

<a name="routing"></a>
### ルーティング

<a name="domain-route-registration-precedence"></a>
#### ドメインルート登録の優先順位

**影響の可能性: 低い**

明示的なドメインを持つルートが、ルート マッチングで非ドメイン ルートよりも優先されるようになりました。

これにより、非ドメイン ルートが以前に登録されている場合でも、キャッチオール サブドメイン ルートが一貫して動作できるようになります。アプリケーションがドメイン ルートと非ドメイン ルート間の以前の登録の優先順位に依存している場合は、ルート マッチングの動作を確認してください。

<a name="scheduling"></a>
### スケジュール設定

<a name="withscheduling-registration-timing"></a>
#### `withScheduling` 登録タイミング

**影響の可能性: 非常に低い**

`ApplicationBuilder::withScheduling()` 経由で登録されたスケジュールは、`Schedule` が解決されるまで延期されるようになりました。

アプリケーションがブートストラップ中の即時スケジュール登録タイミングに依存している場合は、そのロジックを調整する必要がある場合があります。

<a name="security"></a>
### 安全

<a name="request-forgery-protection"></a>
#### 偽造防止のリクエスト

**影響の可能性: 高**

Laravel の CSRF ミドルウェアの名前が `VerifyCsrfToken` から `PreventRequestForgery` に変更され、`Sec-Fetch-Site` ヘッダーを使用したリクエスト送信元の検証が含まれるようになりました。

`VerifyCsrfToken` および `ValidateCsrfToken` は非推奨のエイリアスとして残りますが、特にテストまたはルート定義でミドルウェアを除外する場合は、直接参照を `PreventRequestForgery` に更新する必要があります。

```php
use Illuminate\Foundation\Http\Middleware\PreventRequestForgery;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;

// Laravel <= 12.x
->withoutMiddleware([VerifyCsrfToken::class]);

// Laravel >= 13.x
->withoutMiddleware([PreventRequestForgery::class]);
```

ミドルウェア構成 API では、`preventRequestForgery(...)` も提供されるようになりました。

<a name="support"></a>
### サポート

<a name="manager-extend-callback-binding"></a>
#### マネージャー `extend` コールバック バインディング

**影響の可能性: 低い**

マネージャーの `extend` メソッドを介して登録されたカスタム ドライバ クロージャーがマネージャー インスタンスにバインドされるようになりました。

以前にこれらのコールバック内で `$this` として別のバインドされたオブジェクト (サービスプロバイダ インスタンスなど) に依存していた場合は、`use (...)` を使用してそれらの値をクロージャ キャプチャに移動する必要があります。

<a name="str-factories-reset-between-tests"></a>
#### `Str` テスト間でのファクトリーリセット

**影響の可能性: 低い**

Laravel は、テストのティアダウン中にカスタム `Str` ファクトリをリセットするようになりました。

テストがテスト メソッド間で持続するカスタム UUID / ULID / ランダム文字列ファクトリに依存している場合は、関連する各テスト フックまたはセットアップ フックでそれらを設定する必要があります。

<a name="jsfrom-uses-unescaped-unicode-by-default"></a>
#### `Js::from` はデフォルトでエスケープされていない Unicode を使用します

**影響の可能性: 非常に低い**

`Illuminate\Support\Js::from` はデフォルトで `JSON_UNESCAPED_UNICODE` を使用するようになりました。

テストまたはフロントエンドの出力比較がエスケープされた Unicode シーケンス (`\u00e8` など) に依存している場合は、期待値を更新してください。

<a name="utilities"></a>
### 公共事業

<a name="symfony-polyfill"></a>
#### Symfony PHP 8.5 ポリフィルとグローバル関数の競合

**影響の可能性: 低い**

Laravel 13 では、`symfony/polyfill-php85` への依存関係が導入されています。 8.5 より前の PHP バージョンでは、ブートストラップ中に事前に定義されていない限り、このポリフィルは `array_first()` や `array_last()` などのグローバル関数を定義します。

これらの関数は、`laravel/helpers` などの従来のヘルパ パッケージや、同じ名前を使用するカスタム グローバル ヘルパと競合する可能性があります。たとえば、従来の `array_first()` ヘルパはコールバックを受け入れて最初に一致した要素を返しましたが、ポリフィルされたバージョンは配列の最初の要素のみを返しました。

競合を回避し、PHP バージョン間で一貫した動作を保証するには、`Illuminate\Support\Arr` メソッドを優先する必要があります。

```php
use Illuminate\Support\Arr;

Arr::first($array, function ($value) {
  return /* condition */;
});
```

<a name="views"></a>
### ビュー

<a name="pagination-bootstrap-view-names"></a>
#### ページネーション ブートストラップ ビュー名

**影響の可能性: 低い**

Bootstrap 3 のデフォルトの内部ページネーション ビュー名が明示的になりました。

```nothing
// Laravel <= 12.x
pagination::default
pagination::simple-default

// Laravel >= 13.x
pagination::bootstrap-3
pagination::simple-bootstrap-3
```

アプリケーションが古いページネーション ビュー名を直接参照している場合は、それらの参照を更新します。

<a name="miscellaneous"></a>
### その他

`laravel/laravel` [GitHub リポジトリ](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。 [GitHub比較ツール](https://github.com/laravel/laravel/compare/12.x...13.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。

