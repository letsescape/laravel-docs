# アップグレードガイド (Upgrade Guide)

- [11.x から 12.0 へのアップグレード](#upgrade-12.0)

<a name="high-impact-changes"></a>
## 大きな影響を与える変更 (High Impact Changes)

<div class="content-list" markdown="1">

- [依存関係の更新](#updating-dependencies)
- [Laravelインストーラーの更新](#updating-the-laravel-installer)

</div>

<a name="medium-impact-changes"></a>
## 中程度の影響のある変更 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [モデルと UUIDv7](#models-and-uuidv7)

</div>

<a name="low-impact-changes"></a>
## 影響の少ない変更 (Low Impact Changes)

<div class="content-list" markdown="1">

- [カーボン3](#carbon-3)
- [同時実行結果のインデックスマッピング](#concurrency-result-index-mapping)
- [コンテナクラスの依存関係の解決](#container-class-dependency-resolution)
- [画像検証で SVG が除外されるようになりました](#image-validation)
- [ローカル ファイルシステム ディスクのデフォルトのルート パス](#local-filesystem-disk-default-root-path)
- [マルチスキーマデータベースの検査](#multi-schema-database-inspecting)
- [ネストされた配列リクエストのマージ](#nested-array-request-merging)

</div>

<a name="upgrade-12.0"></a>
## 11.x から 12.0 へのアップグレード (Upgrading To 12.0 From 11.x)

#### アップグレードの推定時間: 5 分

> [!NOTE]
> 私たちは、考えられるすべての重大な変更を文書化するよう努めます。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。時間を節約したいですか? [Laravelシフト](https://laravelshift.com/) を使用すると、アプリケーションのアップグレードを自動化できます。

<a name="updating-dependencies"></a>
### 依存関係の更新

**影響の可能性: 高**

アプリケーションの `composer.json` ファイル内の次の依存関係を更新する必要があります。

<div class="content-list" markdown="1">

- `laravel/framework` ～ `^12.0`
- `phpunit/phpunit` ～ `^11.0`
- `pestphp/pest` ～ `^3.0`

</div>

<a name="carbon-3"></a>
#### カーボン3

**影響の可能性: 低い**

Carbon 2.x のサポートは削除されました。すべての Laravel 12 アプリケーションには [カーボン 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html) が必要になりました。

<a name="updating-the-laravel-installer"></a>
### Laravelインストーラーの更新

Laravel インストーラー CLI ツールを使用して新しい Laravel アプリケーションを作成している場合は、Laravel 12.x および [新しいLaravelスターターキット](https://laravel.com/starter-kits) と互換性があるようにインストーラーのインストールを更新する必要があります。 `composer global require` 経由で Laravel インストーラーをインストールした場合は、`composer global update` を使用してインストーラーを更新できます。

```shell
composer global update laravel/installer
```

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

または、Laravel インストーラーの [Laravel・ハードの](https://herd.laravel.com) バンドル コピーを使用している場合は、Herd インストールを最新リリースに更新する必要があります。

<a name="authentication"></a>
### 認証

<a name="updated-databasetokenrepository-constructor-signature"></a>
#### `DatabaseTokenRepository` コンストラクターの署名を更新しました

**影響の可能性: 非常に低い**

`Illuminate\Auth\Passwords\DatabaseTokenRepository` クラスのコンストラクターは、`$expires` パラメーターが分ではなく秒で指定されることを期待するようになりました。

<a name="concurrency"></a>
### 同時実行性

<a name="concurrency-result-index-mapping"></a>
#### 同時実行結果のインデックスマッピング

**影響の可能性: 低い**

連想配列を使用して `Concurrency::run` メソッドを呼び出すと、同時操作の結果が関連付けられたキーとともに返されるようになりました。

```php
$result = Concurrency::run([
    'task-1' => fn () => 1 + 1,
    'task-2' => fn () => 2 + 2,
]);

// ['task-1' => 2, 'task-2' => 4]
```

<a name="container"></a>
### 容器

<a name="container-class-dependency-resolution"></a>
#### コンテナクラスの依存関係の解決

**影響の可能性: 低い**

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
### データベース

<a name="multi-schema-database-inspecting"></a>
#### マルチスキーマデータベースの検査

**影響の可能性: 低い**

`Schema::getTables()`、`Schema::getViews()`、および `Schema::getTypes()` メソッドには、デフォルトですべてのスキーマの結果が含まれるようになりました。 `schema` 引数を渡して、指定されたスキーマのみの結果を取得できます。

```php
// All tables on all schemas...
$tables = Schema::getTables();

// All tables on the 'main' schema...
$tables = Schema::getTables(schema: 'main');

// All tables on the 'main' and 'blog' schemas...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

`Schema::getTableListing()` メソッドは、デフォルトでスキーマ修飾されたテーブル名を返すようになりました。 `schemaQualified` 引数を渡して、必要に応じて動作を変更できます。

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

`db:table` および `db:show` コマンドは、PostgreSQL や SQL Server と同様に、MySQL、MariaDB、SQLite 上のすべてのスキーマの結果を出力するようになりました。

<a name="database-constructor-signature-changes"></a>
#### データベース コンストラクターの署名の変更

**影響の可能性: 非常に低い**

Laravel 12 では、いくつかの低レベルのデータベース クラスで、コンストラクターを介して `Illuminate\Database\Connection` インスタンスを提供する必要があります。

**これらの変更は主にデータベース パッケージの管理者に適用されます。これらの変更が通常のアプリケーション開発に影響を与える可能性はほとんどありません。**

`Illuminate\Database\Schema\Blueprint`

`Illuminate\Database\Schema\Blueprint` クラスのコンストラクターは、最初の引数として `Connection` インスタンスを期待するようになりました。これは主に、`Blueprint` インスタンスを手動でインスタンス化するアプリケーションまたはパッケージに影響します。

`Illuminate\Database\Grammar`

`Illuminate\Database\Grammar` クラスのコンストラクターには、`Connection` インスタンスも必要になりました。以前のバージョンでは、接続は構築後に `setConnection()` メソッドを使用して割り当てられていました。このメソッドは Laravel 12 では削除されました。

```php
// Laravel <= 11.x
$grammar = new MySqlGrammar;
$grammar->setConnection($connection);

// Laravel >= 12.x
$grammar = new MySqlGrammar($connection);
````

さらに、次の API が削除または非推奨になりました。

<div class="content-list" markdown="1">

- `Blueprint::getPrefix()` メソッドは非推奨になりました。
- `Connection::withTablePrefix()` メソッドは削除されました。
- `Grammar::getTablePrefix()` メソッドと `setTablePrefix()` メソッドは非推奨になりました。
- `Grammar::setConnection()` メソッドは削除されました。

</div>

テーブルの接頭辞を操作する場合は、データベース接続から直接接頭辞を取得する必要があります。

```php
$prefix = $connection->getTablePrefix();
```

カスタム データベース ドライバ、スキーマ ビルダ、または文法実装を保守する場合は、それらのコンストラクターを確認し、`Connection` インスタンスが提供されていることを確認する必要があります。

<a name="eloquent"></a>
### Eloquent

<a name="models-and-uuidv7"></a>
#### モデルと UUIDv7

**影響の可能性: 中**

`HasUuids` トレイトは、UUID 仕様のバージョン 7 と互換性のある UUID (順序付けされた UUID) を返すようになりました。モデルの ID に順序付けされた UUIDv4 文字列を引き続き使用したい場合は、`HasVersion4Uuids` 特性を使用する必要があります。

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

`HasVersion7Uuids` 特性は削除されました。以前にこの特性を使用していた場合は、代わりに `HasUuids` 特性を使用する必要があります。これにより、同じ動作が提供されるようになります。

<a name="requests"></a>
### リクエスト

<a name="nested-array-request-merging"></a>
#### ネストされた配列リクエストのマージ

**影響の可能性: 低い**

`$request->mergeIfMissing()` メソッドでは、「ドット」表記を使用してネストされた配列データをマージできるようになりました。以前にこのメソッドを使用して、キーの「ドット」表記バージョンを含む最上位の配列キーを作成していた場合は、この新しい動作を考慮してアプリケーションを調整する必要がある場合があります。

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="routing"></a>
### ルーティング

<a name="route-precedence"></a>
#### ルートの優先順位

**影響の可能性: 低い**

複数のルートが同じ名前を持つ場合のルーティング動作は、キャッシュされたルーティングとキャッシュされていないルーティングの間で統合されました。これは、キャッシュされていないルーティングが、最後のルートではなく、指定された名前で登録された最初のルートと一致することを意味します。

<a name="storage"></a>
### ストレージ

<a name="local-filesystem-disk-default-root-path"></a>
#### ローカル ファイルシステム ディスクのデフォルトのルート パス

**影響の可能性: 低い**

アプリケーションがファイルシステム構成で `local` ディスクを明示的に定義していない場合、Laravel はローカル ディスクのルートをデフォルトで `storage/app/private` に設定します。以前のリリースでは、これはデフォルトで `storage/app` でした。その結果、別途設定されていない限り、`Storage::disk('local')` への呼び出しは `storage/app/private` との間で読み取りおよび書き込みを行います。以前の動作を復元するには、`local` ディスクを手動で定義し、目的のルート パスを設定します。

<a name="validation"></a>
### 検証

<a name="image-validation"></a>
#### 画像検証で SVG が除外されるようになりました

**影響の可能性: 低い**

`image` 検証ルールでは、デフォルトで SVG 画像が許可されなくなりました。 `image` ルールの使用時に SVG を許可したい場合は、明示的に許可する必要があります。

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// Or...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
### その他

`laravel/laravel` [GitHub リポジトリ](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。 [GitHub比較ツール](https://github.com/laravel/laravel/compare/11.x...12.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。

