# アップグレードガイド (Upgrade Guide)

- [8.x から 9.0 へのアップグレード](#upgrade-9.0)

<a name="high-impact-changes"></a>
## 大きな影響を与える変更 (High Impact Changes)

<div class="content-list" markdown="1">

- [依存関係の更新](#updating-dependencies)
- [フライシステム 3.x](#flysystem-3)
- [Symfony Mailer](#symfony-mailer)

</div>

<a name="medium-impact-changes"></a>
## 中程度の影響のある変更 (Medium Impact Changes)

<div class="content-list" markdown="1">

- [多くの `firstOrNew`、`firstOrCreate`、および `updateOrCreate` メソッドに属します](#belongs-to-many-first-or-new)
- [カスタム キャストと `null`](#custom-casts-and-null)
- [デフォルトのHTTPクライアントタイムアウト](#http-client-default-timeout)
- [PHP の戻り値の型](#php-return-types)
- [Postgresの「スキーマ」構成](#postgres-schema-configuration)
- [`assertDeleted` メソッド](#the-assert-deleted-method)
- [`lang` ディレクトリ](#the-lang-directory)
- [`password` ルール](#the-password-rule)
- [`when` / `unless` メソッド](#when-and-unless-methods)
- [未検証の配列キー](#unvalidated-array-keys)

</div>

<a name="upgrade-9.0"></a>
## 8.x から 9.0 へのアップグレード (Upgrading To 9.0 From 8.x)

<a name="estimated-upgrade-time-30-minutes"></a>
#### アップグレードの推定時間: 30 分

> **注記**
> 私たちは、考えられるすべての重大な変更を文書化するよう努めます。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。時間を節約したいですか? [Laravelシフト](https://laravelshift.com/) を使用すると、アプリケーションのアップグレードを自動化できます。

<a name="updating-dependencies"></a>
### 依存関係の更新

**影響の可能性: 高**

#### PHP 8.0.2が必要

Laravel には PHP 8.0.2 以降が必要になりました。

#### Composer の依存関係

アプリケーションの `composer.json` ファイル内の次の依存関係を更新する必要があります。

<div class="content-list" markdown="1">

- `laravel/framework` ～ `^9.0`
- `nunomaduro/collision` ～ `^6.1`

</div>

さらに、アプリケーションの `composer.json` ファイル内の `facade/ignition` を `"spatie/laravel-ignition": "^1.0"` に、`pusher/pusher-php-server` (該当する場合) を `"pusher/pusher-php-server": "^5.0"` に置き換えてください。

さらに、次のファーストパーティパッケージは、Laravel 9.x をサポートするための新しいメジャーリリースを受け取りました。該当する場合は、アップグレードする前に、それぞれのアップグレード ガイドを読む必要があります。

<div class="content-list" markdown="1">

- [Vonage 通知チャネル (v3.0)](https://github.com/laravel/vonage-notification-channel/blob/3.x/UPGRADE.md) (Nexmo を置き換え)

</div>

最後に、アプリケーションで使用される他のサードパーティパッケージを調べて、Laravel 9 をサポートする適切なバージョンを使用していることを確認します。

<a name="php-return-types"></a>
#### PHP の戻り値の型

PHP は、`offsetGet`、`offsetSet` などの PHP メソッドで戻り値の型の定義を要求するように移行し始めています。これを考慮して、Laravel 9 ではこれらの戻り値の型をコードベースに実装しました。通常、これはユーザーが作成したコードには影響しません。ただし、Laravel のコアクラスを拡張してこれらのメソッドのいずれかをオーバーライドする場合は、これらの戻り値の型を独自のアプリケーションまたはパッケージ コードに追加する必要があります。

<div class="content-list" markdown="1">

- `count(): int`
- `getIterator(): Traversable`
- `getSize(): int`
- `jsonSerialize(): array`
- `offsetExists($key): bool`
- `offsetGet($key): mixed`
- `offsetSet($key, $value): void`
- `offsetUnset($key): void`

</div>

さらに、PHP の `SessionHandlerInterface` を実装するメソッドに戻り値の型が追加されました。繰り返しますが、この変更が独自のアプリケーションまたはパッケージのコードに影響を与える可能性は低いです。

<div class="content-list" markdown="1">

- `open($savePath, $sessionName): bool`
- `close(): bool`
- `read($sessionId): string|false`
- `write($sessionId, $data): bool`
- `destroy($sessionId): bool`
- `gc($lifetime): int`

</div>

<a name="application"></a>
### 応用

<a name="the-application-contract"></a>
#### `Application` 契約

**影響の可能性: 低い**

`Illuminate\Contracts\Foundation\Application` インターフェイスの `storagePath` メソッドが更新され、`$path` 引数を受け入れるようになりました。このインターフェースを実装している場合は、それに応じて実装を更新する必要があります。

    public function storagePath($path = '');
    
同様に、`Illuminate\Foundation\Application` クラスの `langPath` メソッドは、`$path` 引数を受け入れるように更新されました。

    public function langPath($path = '');

#### 例外ハンドラ `ignore` メソッド

**影響の可能性: 低い**

例外ハンドラーの `ignore` メソッドは、`protected` ではなく `public` になりました。このメソッドは、デフォルトのアプリケーション スケルトンには含まれていません。ただし、このメソッドを手動で定義した場合は、その可視性を `public` に更新する必要があります。

```php
public function ignore(string $class);
```

#### 例外ハンドラーコントラクトバインディング

**影響の可能性: 非常に低い**

以前は、デフォルトの Laravel 例外ハンドラーをオーバーライドするために、カスタム実装は `\App\Exceptions\Handler::class` タイプを使用してサービスコンテナーにバインドされていました。ただし、`\Illuminate\Contracts\Debug\ExceptionHandler::class` タイプを使用してカスタム実装をバインドする必要があります。

### Blade

#### Lazy コレクションと `$loop` 変数

**影響の可能性: 低い**

Blade テンプレート内の `LazyCollection` インスタンスを反復処理する場合、`$loop` 変数は使用できなくなります。この変数にアクセスすると、`LazyCollection` 全体がメモリにロードされるため、このシナリオでは遅延コレクションの使用が無意味になります。

#### オン/無効/選択されたBlade ディレクティブ

**影響の可能性: 低い**

新しい `@checked`、`@disabled`、および `@selected` Blade ディレクティブは、同じ名前の Vue イベントと競合する可能性があります。 `@@` を使用してディレクティブをエスケープし、この競合を回避できます: `@@selected`。

### コレクション

#### `Enumerable` 契約

**影響の可能性: 低い**

`Illuminate\Support\Enumerable` コントラクトは、`sole` メソッドを定義するようになりました。このインターフェースを手動で実装している場合は、この新しいメソッドを反映するように実装を更新する必要があります。

```php
public function sole($key = null, $operator = null, $value = null);
```

#### `reduceWithKeys` メソッド

`reduce` メソッドが同じ機能を提供するため、`reduceWithKeys` メソッドは削除されました。 `reduceWithKeys` の代わりに `reduce` を呼び出すようにコードを更新するだけです。

#### `reduceMany` メソッド

他の同様のメソッドとの名前の一貫性を保つために、`reduceMany` メソッドの名前が `reduceSpread` に変更されました。

### 容器

#### `Container` 契約

**影響の可能性: 非常に低い**

`Illuminate\Contracts\Container\Container` コントラクトは、`scoped` と `scopedIf` という 2 つのメソッド定義を受け取りました。このコントラクトを手動で実装している場合は、これらの新しいメソッドを反映するように実装を更新する必要があります。

#### `ContextualBindingBuilder` 契約

**影響の可能性: 非常に低い**

`Illuminate\Contracts\Container\ContextualBindingBuilder` コントラクトは、`giveConfig` メソッドを定義するようになりました。このインターフェースを手動で実装している場合は、この新しいメソッドを反映するように実装を更新する必要があります。

```php
public function giveConfig($key, $default = null);
```

### データベース

<a name="postgres-schema-configuration"></a>
#### Postgresの「スキーマ」構成

**影響の可能性: 中**

アプリケーションの `config/database.php` 構成ファイルで Postgres 接続検索パスの構成に使用される `schema` 構成オプションの名前を `search_path` に変更する必要があります。

<a name="schema-builder-doctrine-method"></a>
#### スキーマ ビルダ `registerCustomDoctrineType` メソッド

**影響の可能性: 低い**

`registerCustomDoctrineType` メソッドが `Illuminate\Database\Schema\Builder` クラスから削除されました。代わりに、`DB` ファサードで `registerDoctrineType` メソッドを使用することも、`config/database.php` 構成ファイルにカスタム Doctrine タイプを登録することもできます。

### Eloquent

<a name="custom-casts-and-null"></a>
#### カスタム キャストと `null`

**影響の可能性: 中**

Laravel の以前のリリースでは、キャスト属性が `null` に設定されている場合、カスタム キャスト クラスの `set` メソッドは呼び出されませんでした。ただし、この動作は Laravel ドキュメントと矛盾していました。 Laravel 9.xでは、キャストクラスの`set`メソッドは、指定された`$value`引数として`null`を使用して呼び出されます。したがって、カスタム キャストがこのシナリオを十分に処理できることを確認する必要があります。

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
#### 多くの `firstOrNew`、`firstOrCreate`、および `updateOrCreate` メソッドに属します

**影響の可能性: 中**

`belongsToMany` 関係の `firstOrNew`、`firstOrCreate`、および `updateOrCreate` メソッドはすべて、最初の引数として属性の配列を受け入れます。 Laravel の以前のリリースでは、この属性の配列は既存のレコードの「ピボット」/中間テーブルと比較されました。

ただし、この動作は予期せぬものであり、通常は望ましくないものでした。代わりに、これらのメソッドは属性の配列を関連モデルのテーブルと比較するようになりました。

```php
$user->roles()->updateOrCreate([
    'name' => 'Administrator',
]);
```

さらに、`firstOrCreate` メソッドは、2 番目の引数として `$values` 配列を受け入れるようになりました。関連モデルが存在しない場合、この配列は、関連モデルの作成時にメソッド (`$attributes`) の最初の引数とマージされます。この変更により、このメソッドは、他の関係タイプが提供する `firstOrCreate` メソッドと一貫性を持つようになります。

```php
$user->roles()->firstOrCreate([
    'name' => 'Administrator',
], [
    'created_by' => $user->id,
]);
```

#### `touch` メソッド

**影響の可能性: 低い**

`touch` メソッドは、タッチする属性を受け入れるようになりました。以前にこのメソッドを上書きしていた場合は、この新しい引数を反映するようにメソッド シグネチャを更新する必要があります。

```php
public function touch($attribute = null);
```

### 暗号化

#### 暗号化契約

**影響の可能性: 低い**

`Illuminate\Contracts\Encryption\Encrypter` コントラクトは、`getKey` メソッドを定義するようになりました。このインターフェースを手動で実装している場合は、それに応じて実装を更新する必要があります。

```php
public function getKey();
```

### ファサード

#### `getFacadeAccessor` メソッド

**影響の可能性: 低い**

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

### ファイルシステム

#### `FILESYSTEM_DRIVER` 環境変数

**影響の可能性: 低い**

`FILESYSTEM_DRIVER` 環境変数の名前は、その使用法をより正確に反映するために `FILESYSTEM_DISK` に変更されました。この変更はアプリケーションのスケルトンにのみ影響します。ただし、必要に応じて、独自のアプリケーションの環境変数を更新して、この変更を反映することもできます。

#### 「クラウド」ディスク

**影響の可能性: 低い**

`cloud` ディスク構成オプションは、2020 年 11 月にデフォルトのアプリケーション スケルトンから削除されました。この変更はアプリケーション スケルトンにのみ影響します。アプリケーション内で `cloud` ディスクを使用している場合は、この構成値を独自のアプリケーションのスケルトンに残す必要があります。

<a name="flysystem-3"></a>
### フライシステム 3.x

**影響の可能性: 高**

Laravel 9.x は [Flysystem](https://flysystem.thephpleague.com/v2/docs/) 1.x から 3.x に移行しました。 Flysystem は内部で、`Storage` ファサードによって提供されるすべてのファイル操作メソッドを強化します。これを考慮して、アプリケーション内でいくつかの変更が必要になる場合があります。ただし、この移行を可能な限りシームレスにするよう努めてきました。

#### ドライバの前提条件

S3、FTP、または SFTP ドライバを使用する前に、Composer パッケージ マネージャーを介して適切なパッケージをインストールする必要があります。

- Amazon S3: `composer require -W league/flysystem-aws-s3-v3 "^3.0"`
- FTP: `composer require league/flysystem-ftp "^3.0"`
- SFTP: `composer require league/flysystem-sftp-v3 "^3.0"`

#### 既存のファイルを上書きする

`put`、`write`、`writeStream` などの書き込み操作は、デフォルトで既存のファイルを上書きするようになりました。既存のファイルを上書きしたくない場合は、書き込み操作を実行する前にファイルの存在を手動で確認する必要があります。

#### 書き込み例外

`put`、`write`、`writeStream` などの書き込み操作は、書き込み操作が失敗したときに例外をスローしなくなりました。代わりに、`false` が返されます。例外をスローした以前の動作を保持したい場合は、ファイルシステム ディスクの構成配列内で `throw` オプションを定義できます。

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

#### 不足しているファイルの読み取り

存在しないファイルから読み取ろうとすると、`null` が返されるようになりました。 Laravel の以前のリリースでは、`Illuminate\Contracts\Filesystem\FileNotFoundException` がスローされていました。

#### 失われたファイルの削除

存在しないファイルに対して `delete` を実行しようとすると、`true` が返されるようになりました。

#### キャッシュされたアダプター

Flysystem は「キャッシュされたアダプター」をサポートしなくなりました。したがって、それらはLaravelから削除され、関連する構成(ディスク構成内の`cache`キーなど)は削除できます。

#### カスタム ファイルシステム

カスタム ファイルシステム ドライバを登録するために必要な手順に若干の変更が加えられました。したがって、独自のカスタム ファイル システム ドライバを定義している場合、またはカスタム ドライバを定義するパッケージを使用している場合は、コードと依存関係を更新する必要があります。

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

#### SFTP 秘密鍵と公開鍵のパスフレーズ

アプリケーションが Flysystem の SFTP アダプターと秘密-公開キー認証を使用している場合、秘密キーの復号化に使用される `password` 構成項目の名前を `passphrase` に変更する必要があります。

### ヘルパ

<a name="data-get-function"></a>
#### `data_get` ヘルパと反復可能オブジェクト

**影響の可能性: 非常に低い**

以前は、`data_get` ヘルパを使用して、配列および `Collection` インスタンスのネストされたデータを取得できました。ただし、このヘルパはすべての反復可能なオブジェクトのネストされたデータを取得できるようになりました。

<a name="str-function"></a>
#### `str` ヘルパ

**影響の可能性: 非常に低い**

Laravel 9.x には、グローバル `str` [ヘルパ関数](/docs/{{version}}/helpers#method-str) が含まれるようになりました。アプリケーションでグローバル `str` ヘルパを定義している場合は、Laravel 独自の `str` ヘルパと競合しないように、ヘルパの名前を変更するか削除する必要があります。

<a name="when-and-unless-methods"></a>
#### `when` / `unless` メソッド

**影響の可能性: 中**

ご存知のとおり、`when` メソッドと `unless` メソッドは、フレームワーク全体のさまざまなクラスによって提供されます。これらのメソッドを使用すると、メソッドの最初の引数のブール値が `true` または `false` に評価される場合に条件付きでアクションを実行できます。

```php
$collection->when(true, function ($collection) {
    $collection->merge([1, 2, 3]);
});
```

したがって、Laravelの以前のリリースでは、クロージャを`when`メソッドまたは`unless`メソッドに渡すことは、クロージャオブジェクト(または他のオブジェクト)との緩やかな比較が常に`true`と評価されるため、条件付き操作が常に実行されることを意味していました。開発者はクロージャの **結果** が条件付きアクションを実行するかどうかを決定するブール値として使用されることを期待しているため、これにより予期せぬ結果が生じることがよくあります。

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

### HTTPクライアント

<a name="http-client-default-timeout"></a>
#### デフォルトのタイムアウト

**影響の可能性: 中**

[HTTPクライアント](/docs/{{version}}/http-client) のデフォルトのタイムアウトは 30 秒になりました。つまり、サーバーが 30 秒以内に応答しない場合、例外がスローされます。以前は、HTTP クライアントにデフォルトのタイムアウト長が設定されていなかったため、リクエストが無期限に「ハング」することがありました。

特定のリクエストに対してより長いタイムアウトを指定したい場合は、`timeout` メソッドを使用して指定できます。

    $response = Http::timeout(120)->get(/* ... */);

#### HTTP フェイクとミドルウェア

**影響の可能性: 低い**

以前は、Laravel は、[HTTPクライアント](/docs/{{version}}/http-client) が「偽装」された場合、提供されている Guzzle HTTP ミドルウェアを実行しませんでした。ただし、Laravel 9.x では、HTTP クライアントが偽装された場合でも、Guzzle HTTP ミドルウェアが実行されます。

#### HTTP フェイクと依存関係の注入

**影響の可能性: 低い**

Laravel の以前のリリースでは、`Http::fake()` メソッドを呼び出しても、クラス コンストラクターに挿入された `Illuminate\Http\Client\Factory` のインスタンスには影響しませんでした。ただし、Laravel 9.x では、`Http::fake()` は、依存注入を通じて他のサービスに注入された HTTP クライアントによって偽の応答が返されることを保証します。この動作は、他のファサードや偽物の動作とより一貫性があります。

<a name="symfony-mailer"></a>
### Symfony Mailer

**影響の可能性: 高**

Laravel 9.x の最大の変更点の 1 つは、2021 年 12 月の時点でメンテナンスが終了した SwiftMailer から Symfony Mailer への移行です。ただし、私たちはこの移行をアプリケーションにとって可能な限りシームレスにするよう努めてきました。そうは言っても、アプリケーションが完全に互換性があることを確認するために、以下の変更点のリストをよく確認してください。

#### ドライバの前提条件

Mailgun トランスポートを引き続き使用するには、アプリケーションに `symfony/mailgun-mailer` および `symfony/http-client` Composer パッケージが必要です。

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

`wildbit/swiftmailer-postmark` Composer パッケージをアプリケーションから削除する必要があります。代わりに、アプリケーションには `symfony/postmark-mailer` および `symfony/http-client` Composer パッケージが必要です。

```shell
composer require symfony/postmark-mailer symfony/http-client
```

#### 更新された戻り値の型

`Illuminate\Mail\Mailer` の `send`、`html`、`raw`、および `plain` メソッドは、`void` を返さなくなりました。代わりに、`Illuminate\Mail\SentMessage` のインスタンスが返されます。このオブジェクトには、`getSymfonySentMessage` メソッドを介して、またはオブジェクトのメソッドを動的に呼び出すことによってアクセスできる、`Symfony\Component\Mailer\SentMessage` のインスタンスが含まれています。

#### 「Swift」メソッドの名前が変更されました

文書化されていないものもあるさまざまな SwiftMailer 関連のメソッドの名前が、対応する Symfony Mailer に変更されました。たとえば、`withSwiftMessage` メソッドの名前は `withSymfonyMessage` に変更されました。

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

> **警告**
> `Symfony\Component\Mime\Email` オブジェクトとのあらゆる対話について、[Symfony Mailerのドキュメント](https://symfony.com/doc/6.0/mailer.html#creating-sending-messages) を徹底的に確認してください。

以下のリストには、名前が変更されたメソッドのより詳細な概要が含まれています。これらのメソッドの多くは、SwiftMailer / Symfony Mailer と直接対話するために使用される低レベルのメソッドであるため、ほとんどの Laravel アプリケーション内では一般的に使用されない可能性があります。

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

#### プロキシされた `Illuminate\Mail\Message` メソッド

`Illuminate\Mail\Message` は通常、欠落しているメソッドを基になる `Swift_Message` インスタンスにプロキシします。ただし、不足しているメソッドは代わりに `Symfony\Component\Mime\Email` のインスタンスにプロキシされるようになりました。そのため、これまで SwiftMailer にプロキシされる欠落メソッドに依存していたコードは、対応する Symfony Mailer に更新する必要があります。

繰り返しになりますが、これらのメソッドは Laravel ドキュメントに記載されていないため、多くのアプリケーションはこれらのメソッドと対話していない可能性があります。

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

#### 生成されたメッセージID

SwiftMailer は、`mime.idgenerator.idright` 構成オプションを介して、生成されたメッセージ ID に含めるカスタム ドメインを定義する機能を提供しました。これは Symfony Mailer ではサポートされていません。代わりに、Symfony Mailer は送信者に基づいてメッセージ ID を自動的に生成します。

#### `MessageSent` イベントの変更

`Illuminate\Mail\Events\MessageSent` イベントの `message` プロパティには、`Swift_Message` のインスタンスではなく、`Symfony\Component\Mime\Email` のインスタンスが含まれるようになりました。このメッセージは、送信される**前**の電子メールを表しています。

さらに、新しい `sent` プロパティが `MessageSent` イベントに追加されました。このプロパティには、`Illuminate\Mail\SentMessage` のインスタンスが含まれており、メッセージ ID など、送信された電子メールに関する情報が含まれています。

#### 強制再接続

トランスポートの再接続を強制することはできなくなりました (たとえば、メーラーがデーモン プロセスを介して実行されている場合)。代わりに、Symfony Mailer は自動的にトランスポートへの再接続を試み、再接続が失敗した場合は例外をスローします。

#### SMTP ストリーム オプション

SMTP トランスポートのストリーム オプションの定義はサポートされなくなりました。代わりに、関連するオプションがサポートされている場合は、構成内で直接定義する必要があります。たとえば、TLS ピア検証を無効にするには、次のようにします。

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

利用可能な構成オプションの詳細については、[Symfony Mailerのドキュメント](https://symfony.com/doc/6.0/mailer.html#transport-setup) を参照してください。

> **警告**
> 上記の例にもかかわらず、SSL 検証を無効にすると「中間者」攻撃の可能性が生じるため、通常は SSL 検証を無効にすることはお勧めできません。

#### SMTP `auth_mode`

`mail` 構成ファイルで SMTP `auth_mode` を定義する必要はなくなりました。認証モードは、Symfony Mailer と SMTP サーバーの間で自動的にネゴシエートされます。

#### 失敗した受信者

メッセージの送信後に失敗した受信者のリストを取得できなくなりました。代わりに、メッセージの送信に失敗した場合は、`Symfony\Component\Mailer\Exception\TransportExceptionInterface` 例外がスローされます。メッセージの送信後に無効な電子メール アドレスを取得することに頼るのではなく、メッセージを送信する前に電子メール アドレスを検証することをお勧めします。

### パッケージ

<a name="the-lang-directory"></a>
#### `lang` ディレクトリ

**影響の可能性: 中**

新しい Laravel アプリケーションでは、`resources/lang` ディレクトリがルート プロジェクト ディレクトリ (`lang`) に配置されるようになりました。パッケージが言語ファイルをこのディレクトリに公開している場合は、パッケージがハードコードされたパスではなく `app()->langPath()` に公開していることを確認する必要があります。

<a name="queue"></a>
### 列

<a name="the-opis-closure-library"></a>
#### `opis/closure` ライブラリ

**影響の可能性: 低い**

Laravel の `opis/closure` への依存関係は、`laravel/serializable-closure` に置き換えられました。 `opis/closure` ライブラリを直接操作しない限り、これによってアプリケーションに重大な変更が生じることはありません。さらに、以前に非推奨になった `Illuminate\Queue\SerializableClosureFactory` クラスと `Illuminate\Queue\SerializableClosure` クラスが削除されました。 `opis/closure` ライブラリと直接対話している場合、または削除されたクラスのいずれかを使用している場合は、代わりに [Laravel シリアル化可能なクロージャ](https://github.com/laravel/serializable-closure) を使用できます。

#### 失敗したジョブプロバイダの `flush` メソッド

**影響の可能性: 低い**

`Illuminate\Queue\Failed\FailedJobProviderInterface` インターフェースによって定義された `flush` メソッドは、`queue:flush` コマンドによってフラッシュされる前に、失敗したジョブがどれくらい経過する必要があるかを (時間単位で) 決定する `$hours` 引数を受け入れるようになりました。 `FailedJobProviderInterface` を手動で実装している場合は、この新しい引数を反映するように実装が更新されていることを確認する必要があります。

```php
public function flush($hours = null);
```

### セッション

#### `getSession` メソッド

**影響の可能性: 低い**

Laravel 独自の `Illuminate\Http\Request` クラスによって拡張された `Symfony\Component\HttpFoundaton\Request` クラスは、現在のセッション ストレージ ハンドラーを取得する `getSession` メソッドを提供します。ほとんどの Laravel アプリケーションは Laravel 独自の `session` メソッドを通じてセッションと対話するため、このメソッドは Laravel によって文書化されていません。

`getSession` メソッドは、以前は `Illuminate\Session\Store` または `null` のインスタンスを返していました。ただし、Symfony 6.x リリースでは戻り値の型 `Symfony\Component\HttpFoundation\Session\SessionInterface` が強制されているため、`getSession` は `SessionInterface` 実装を正しく返すか、セッションが使用できない場合に `\Symfony\Component\HttpFoundation\Exception\SessionNotFoundException` 例外をスローするようになりました。

### テスト

<a name="the-assert-deleted-method"></a>
#### `assertDeleted` メソッド

**影響の可能性: 中**

`assertDeleted` メソッドへのすべての呼び出しは、`assertModelMissing` に更新する必要があります。

### 信頼できるプロキシ

**影響の可能性: 低い**

既存のアプリケーションコードをまったく新しい Laravel 9 アプリケーションスケルトンにインポートして、Laravel 8 プロジェクトを Laravel 9 にアップグレードする場合は、アプリケーションの「信頼できるプロキシ」ミドルウェアを更新する必要がある場合があります。

`app/Http/Middleware/TrustProxies.php` ファイル内で、`use Fideloper\Proxy\TrustProxies as Middleware` を `use Illuminate\Http\Middleware\TrustProxies as Middleware` に更新します。

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

最後に、アプリケーションから `fideloper/proxy` Composer 依存関係を削除できます。

```shell
composer remove fideloper/proxy
```

### 検証

#### フォームリクエスト `validated` メソッド

**影響の可能性: 低い**

フォームリクエストによって提供される `validated` メソッドは、`$key` および `$default` 引数を受け入れるようになりました。このメソッドの定義を手動で上書きする場合は、次の新しい引数を反映するようにメソッドのシグネチャを更新する必要があります。

```php
public function validated($key = null, $default = null)
```

<a name="the-password-rule"></a>
#### `password` ルール

**影響の可能性: 中**

指定された入力値が認証されたユーザーの現在のパスワードと一致することを検証する `password` ルールの名前が `current_password` に変更されました。

<a name="unvalidated-array-keys"></a>
#### 未検証の配列キー

**影響の可能性: 中**

Laravel の以前のリリースでは、特に許可されたキーのリストを指定しない `array` ルールと組み合わせた場合、Laravel のバリデーターが返す「検証済み」データから未検証の配列キーを除外するように手動で指示する必要がありました。

ただし、Laravel 9.x では、`array` ルールで許可されたキーが指定されていない場合でも、未検証の配列キーは常に「検証済み」データから除外されます。通常、この動作は最も予期される動作であり、以前の `excludeUnvalidatedArrayKeys` メソッドは、下位互換性を維持するための一時的な措置として Laravel 8.x に追加されただけです。

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
### その他

`laravel/laravel` [GitHub リポジトリ](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。 [GitHub比較ツール](https://github.com/laravel/laravel/compare/8.x...9.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。

