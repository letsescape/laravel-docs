# ファイルストレージ (File Storage)

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [地元のドライバ](#the-local-driver)
    - [パブリックディスク](#the-public-disk)
    - [ドライバの前提条件](#driver-prerequisites)
    - [スコープ指定された読み取り専用ファイルシステム](#scoped-and-read-only-filesystems)
    - [Amazon S3 互換ファイルシステム](#amazon-s3-compatible-filesystems)
- [ディスクインスタンスの取得](#obtaining-disk-instances)
    - [オンデマンドディスク](#on-demand-disks)
- [ファイルの取得](#retrieving-files)
    - [ファイルのダウンロード](#downloading-files)
    - [ファイルの URL](#file-urls)
    - [一時的な URL](#temporary-urls)
    - [ファイルのメタデータ](#file-metadata)
- [ファイルの保存](#storing-files)
    - [ファイルの先頭および末尾に追加する](#prepending-appending-to-files)
    - [ファイルのコピーと移動](#copying-moving-files)
    - [自動ストリーミング](#automatic-streaming)
    - [ファイルのアップロード](#file-uploads)
    - [ファイルの可視性](#file-visibility)
- [ファイルの削除](#deleting-files)
- [Directories](#directories)
- [Testing](#testing)
- [カスタム ファイルシステム](#custom-filesystems)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、Frank de Jonge による素晴らしい [Flysystem](https://github.com/thephpleague/flysystem) PHP パッケージのおかげで、強力なファイルシステムの抽象化を提供します。 Laravel Flysystem 統合では、ローカル ファイルシステム、SFTP、Amazon S3 を操作するためのシンプルなドライバが提供されます。さらに良いことに、API は各システムで同じままであるため、ローカル開発マシンと運用サーバーの間でこれらのストレージ オプションを切り替えるのは驚くほど簡単です。

<a name="configuration"></a>
## 構成 (Configuration)

Laravel のファイルシステム構成ファイルは、`config/filesystems.php` にあります。このファイル内で、すべてのファイルシステムの「ディスク」を構成できます。各ディスクは、特定のストレージ ドライバとストレージの場所を表します。サポートされている各ドライバの構成例が構成ファイルに含まれているため、ストレージ設定と資格情報を反映するように構成を変更できます。

`local` ドライバは、Laravel アプリケーションを実行しているサーバー上にローカルに保存されているファイルと対話し、`s3` ドライバは Amazon の S3 クラウド ストレージ サービスへの書き込みに使用されます。

> [!NOTE]  
> ディスクは好きなだけ構成でき、同じドライバを使用する複数のディスクを使用することもできます。

<a name="the-local-driver"></a>
### 地元のドライバ

`local` ドライバを使用する場合、すべてのファイル操作は、`filesystems` 構成ファイルで定義された `root` ディレクトリに対して相対的に行われます。デフォルトでは、この値は `storage/app` ディレクトリに設定されます。したがって、次のメソッドは `storage/app/example.txt` に書き込みます。

    use Illuminate\Support\Facades\Storage;

    Storage::disk('local')->put('example.txt', 'Contents');

<a name="the-public-disk"></a>
### パブリックディスク

アプリケーションの `filesystems` 構成ファイルに含まれる `public` ディスクは、パブリックにアクセスできるファイル用です。デフォルトでは、`public` ディスクは `local` ドライバを使用し、そのファイルを `storage/app/public` に保存します。

これらのファイルに Web からアクセスできるようにするには、`public/storage` から `storage/app/public` へのシンボリック リンクを作成する必要があります。このフォルダー規則を利用すると、パブリックにアクセスできるファイルが 1 つのディレクトリに保存され、[Envoyer](https://envoyer.io) のようなダウンタイムなしの展開システムを使用する場合、展開間で簡単に共有できます。

シンボリック リンクを作成するには、`storage:link` Artisan コマンドを使用できます。

```shell
php artisan storage:link
```

ファイルが保存され、シンボリック リンクが作成されたら、`asset` ヘルパを使用してファイルへの URL を作成できます。

    echo asset('storage/file.txt');

`filesystems` 構成ファイルで追加のシンボリック リンクを構成できます。構成された各リンクは、`storage:link` コマンドを実行すると作成されます。

    'links' => [
        public_path('storage') => storage_path('app/public'),
        public_path('images') => storage_path('app/images'),
    ],

`storage:unlink` コマンドを使用して、構成されたシンボリック リンクを破棄することができます。

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### ドライバの前提条件

<a name="s3-driver-configuration"></a>
#### S3 ドライバの構成

S3 ドライバを使用する前に、Composer パッケージ マネージャーを介して Flysystem S3 パッケージをインストールする必要があります。

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 ドライバの構成情報は、`config/filesystems.php` 構成ファイルにあります。このファイルには、S3 ドライバの構成配列の例が含まれています。このアレイは、独自の S3 構成と認証情報を使用して自由に変更できます。便宜上、これらの環境変数は AWS CLI で使用される命名規則と一致しています。

<a name="ftp-driver-configuration"></a>
#### FTPドライバの設定

FTP ドライバを使用する前に、Composer パッケージ マネージャーを介して Flysystem FTP パッケージをインストールする必要があります。

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel の Flysystem 統合は FTP とうまく連携します。ただし、サンプル構成はフレームワークのデフォルトの `filesystems.php` 構成ファイルには含まれていません。 FTP ファイルシステムを構成する必要がある場合は、以下の構成例を使用できます。

    'ftp' => [
        'driver' => 'ftp',
        'host' => env('FTP_HOST'),
        'username' => env('FTP_USERNAME'),
        'password' => env('FTP_PASSWORD'),

        // Optional FTP Settings...
        // 'port' => env('FTP_PORT', 21),
        // 'root' => env('FTP_ROOT'),
        // 'passive' => true,
        // 'ssl' => true,
        // 'timeout' => 30,
    ],

<a name="sftp-driver-configuration"></a>
#### SFTPドライバの構成

SFTP ドライバを使用する前に、Composer パッケージ マネージャーを介して Flysystem SFTP パッケージをインストールする必要があります。

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel の Flysystem 統合は SFTP とうまく連携します。ただし、サンプル構成はフレームワークのデフォルトの `filesystems.php` 構成ファイルには含まれていません。 SFTP ファイルシステムを構成する必要がある場合は、以下の構成例を使用できます。

    'sftp' => [
        'driver' => 'sftp',
        'host' => env('SFTP_HOST'),

        // Settings for basic authentication...
        'username' => env('SFTP_USERNAME'),
        'password' => env('SFTP_PASSWORD'),

        // Settings for SSH key based authentication with encryption password...
        'privateKey' => env('SFTP_PRIVATE_KEY'),
        'passphrase' => env('SFTP_PASSPHRASE'),

        // Settings for file / directory permissions...
        'visibility' => 'private', // `private` = 0600, `public` = 0644
        'directory_visibility' => 'private', // `private` = 0700, `public` = 0755

        // Optional SFTP Settings...
        // 'hostFingerprint' => env('SFTP_HOST_FINGERPRINT'),
        // 'maxTries' => 4,
        // 'passphrase' => env('SFTP_PASSPHRASE'),
        // 'port' => env('SFTP_PORT', 22),
        // 'root' => env('SFTP_ROOT', ''),
        // 'timeout' => 30,
        // 'useAgent' => true,
    ],

<a name="scoped-and-read-only-filesystems"></a>
### スコープ指定された読み取り専用ファイルシステム

スコープ付きディスクを使用すると、すべてのパスに特定のパス プレフィックスが自動的に付加されるファイル システムを定義できます。スコープ付きファイルシステム ディスクを作成する前に、Composer パッケージ マネージャーを介して追加の Flysystem パッケージをインストールする必要があります。

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

`scoped` ドライバを使用するディスクを定義することにより、既存のファイル システム ディスクのパス スコープのインスタンスを作成できます。たとえば、既存の `s3` ディスクのスコープを特定のパス プレフィックスに設定するディスクを作成すると、スコープ指定されたディスクを使用するすべてのファイル操作で指定されたプレフィックスが使用されます。

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

「読み取り専用」ディスクを使用すると、書き込み操作を許可しないファイルシステム ディスクを作成できます。 `read-only` 構成オプションを使用する前に、Composer パッケージ マネージャーを介して追加の Flysystem パッケージをインストールする必要があります。

```shell
composer require league/flysystem-read-only "^3.0"
```

次に、1 つ以上のディスクの構成配列に `read-only` 構成オプションを含めることができます。

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 互換ファイルシステム

デフォルトでは、アプリケーションの `filesystems` 構成ファイルには、`s3` ディスクのディスク構成が含まれています。このディスクを使用して Amazon S3 と対話するだけでなく、[MinIO](https://github.com/minio/minio) や [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/) などの S3 互換ファイルストレージ サービスと対話するために使用することもできます。

通常、使用する予定のサービスの資格情報と一致するようにディスクの資格情報を更新した後、`endpoint` 構成オプションの値を更新するだけで済みます。このオプションの値は通常、`AWS_ENDPOINT` 環境変数によって定義されます。

    'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),

<a name="minio"></a>
#### MinIO

MinIO の使用時に Laravel の Flysystem 統合で適切な URL を生成するには、アプリケーションのローカル URL と一致し、URL パスにバケット名が含まれるように `AWS_URL` 環境変数を定義する必要があります。

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]  
> MinIO を使用する場合、`temporaryUrl` メソッドによる一時ストレージ URL の生成はサポートされません。

<a name="obtaining-disk-instances"></a>
## ディスクインスタンスの取得 (Obtaining Disk Instances)

`Storage` ファサードは、構成されたディスクと対話するために使用できます。たとえば、ファサードで `put` メソッドを使用して、デフォルトのディスクにアバターを保存できます。最初に `disk` メソッドを呼び出さずに、`Storage` ファサードでメソッドを呼び出すと、メソッドは自動的にデフォルトのディスクに渡されます。

    use Illuminate\Support\Facades\Storage;

    Storage::put('avatars/1', $content);

アプリケーションが複数のディスクと対話する場合は、`Storage` ファサードで `disk` メソッドを使用して、特定のディスク上のファイルを操作できます。

    Storage::disk('s3')->put('avatars/1', $content);

<a name="on-demand-disks"></a>
### オンデマンドディスク

場合によっては、アプリケーションの `filesystems` 構成ファイルにその構成が実際に存在していなくても、指定された構成を使用して実行時にディスクを作成したい場合があります。これを実現するには、構成配列を `Storage` ファサードの `build` メソッドに渡すことができます。

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a name="retrieving-files"></a>
## ファイルの取得 (Retrieving Files)

`get` メソッドは、ファイルの内容を取得するために使用できます。ファイルの生の文字列コンテンツがメソッドによって返されます。すべてのファイル パスは、ディスクの「ルート」の場所を基準にして指定する必要があることに注意してください。

    $contents = Storage::get('file.jpg');

取得しているファイルに JSON が含まれている場合は、`json` メソッドを使用してファイルを取得し、その内容をデコードできます。

    $orders = Storage::json('orders.json');

`exists` メソッドを使用して、ファイルがディスク上に存在するかどうかを確認できます。

    if (Storage::disk('s3')->exists('file.jpg')) {
        // ...
    }

`missing` メソッドを使用して、ファイルがディスクに欠落しているかどうかを確認できます。

    if (Storage::disk('s3')->missing('file.jpg')) {
        // ...
    }

<a name="downloading-files"></a>
### ファイルのダウンロード

`download` メソッドは、ユーザーのブラウザに指定されたパスにファイルをダウンロードさせる応答を生成するために使用できます。 `download` メソッドは、メソッドの 2 番目の引数としてファイル名を受け入れます。これにより、ファイルをダウンロードするユーザーに表示されるファイル名が決まります。最後に、HTTP ヘッダーの配列を 3 番目の引数としてメソッドに渡すことができます。

    return Storage::download('file.jpg');

    return Storage::download('file.jpg', $name, $headers);

<a name="file-urls"></a>
### ファイルの URL

`url` メソッドを使用して、特定のファイルの URL を取得できます。 `local` ドライバを使用している場合、これは通常、指定されたパスの先頭に `/storage` を追加し、ファイルへの相対 URL を返します。 `s3` ドライバを使用している場合は、完全修飾リモート URL が返されます。

    use Illuminate\Support\Facades\Storage;

    $url = Storage::url('file.jpg');

`local` ドライバを使用する場合、パブリックにアクセスできるすべてのファイルを `storage/app/public` ディレクトリに配置する必要があります。さらに、`storage/app/public` ディレクトリを指す `public/storage` で [シンボリックリンクを作成する](#the-public-disk) する必要があります。

> [!WARNING]  
> `local` ドライバを使用する場合、`url` の戻り値は URL エンコードされません。このため、常に有効な URL を作成できる名前を使用してファイルを保存することをお勧めします。

<a name="url-host-customization"></a>
#### URLホストのカスタマイズ

`Storage` ファサードを使用して生成された URL のホストを事前定義したい場合は、ディスクの構成配列に `url` オプションを追加できます。

    'public' => [
        'driver' => 'local',
        'root' => storage_path('app/public'),
        'url' => env('APP_URL').'/storage',
        'visibility' => 'public',
    ],

<a name="temporary-urls"></a>
### 一時的な URL

`temporaryUrl` メソッドを使用すると、`s3` ドライバを使用して保存されたファイルへの一時 URL を作成できます。このメソッドは、URL の有効期限がいつ切れるかを指定するパスと `DateTime` インスタンスを受け入れます。

    use Illuminate\Support\Facades\Storage;

    $url = Storage::temporaryUrl(
        'file.jpg', now()->addMinutes(5)
    );

追加の [S3リクエストパラメータ](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests) を指定する必要がある場合は、リクエスト パラメーターの配列を 3 番目の引数として `temporaryUrl` メソッドに渡すことができます。

    $url = Storage::temporaryUrl(
        'file.jpg',
        now()->addMinutes(5),
        [
            'ResponseContentType' => 'application/octet-stream',
            'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
        ]
    );

特定のストレージ ディスクに対して一時 URL を作成する方法をカスタマイズする必要がある場合は、`buildTemporaryUrlsUsing` メソッドを使用できます。たとえば、これは、通常は一時 URL をサポートしないディスク経由で保存されたファイルをダウンロードできるコントローラを持っている場合に便利です。通常、このメソッドはサービスプロバイダの `boot` メソッドから呼び出す必要があります。

    <?php

    namespace App\Providers;

    use DateTime;
    use Illuminate\Support\Facades\Storage;
    use Illuminate\Support\Facades\URL;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         */
        public function boot(): void
        {
            Storage::disk('local')->buildTemporaryUrlsUsing(
                function (string $path, DateTime $expiration, array $options) {
                    return URL::temporarySignedRoute(
                        'files.download',
                        $expiration,
                        array_merge($options, ['path' => $path])
                    );
                }
            );
        }
    }

<a name="temporary-upload-urls"></a>
#### 一時アップロード URL

> [!WARNING]  
> 一時アップロード URL を生成する機能は、`s3` ドライバでのみサポートされています。

クライアント側アプリケーションからファイルを直接アップロードするために使用できる一時 URL を生成する必要がある場合は、`temporaryUploadUrl` メソッドを使用できます。このメソッドは、パスと、URL の有効期限がいつ切れるかを指定する `DateTime` インスタンスを受け入れます。 `temporaryUploadUrl` メソッドは、アップロード URL とアップロード リクエストに含めるヘッダーに分解できる連想配列を返します。

    use Illuminate\Support\Facades\Storage;

    ['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
        'file.jpg', now()->addMinutes(5)
    );

この方法は主に、クライアント側アプリケーションが Amazon S3 などのクラウド ストレージ システムにファイルを直接アップロードする必要があるサーバーレス環境で役立ちます。

<a name="file-metadata"></a>
### ファイルのメタデータ

Laravel は、ファイルの読み取りと書き込みに加えて、ファイル自体に関する情報を提供することもできます。たとえば、`size` メソッドを使用して、ファイルのサイズをバイト単位で取得できます。

    use Illuminate\Support\Facades\Storage;

    $size = Storage::size('file.jpg');

`lastModified` メソッドは、ファイルが最後に変更されたときの UNIX タイムスタンプを返します。

    $time = Storage::lastModified('file.jpg');

特定のファイルの MIME タイプは、`mimeType` メソッド経由で取得できます。

    $mime = Storage::mimeType('file.jpg');

<a name="file-paths"></a>
#### ファイルパス

`path` メソッドを使用して、特定のファイルのパスを取得できます。 `local` ドライバを使用している場合、ファイルへの絶対パスが返されます。 `s3` ドライバを使用している場合、このメソッドは S3 バケット内のファイルへの相対パスを返します。

    use Illuminate\Support\Facades\Storage;

    $path = Storage::path('file.jpg');

<a name="storing-files"></a>
## ファイルの保存 (Storing Files)

`put` メソッドは、ファイルの内容をディスクに保存するために使用できます。 PHP `resource` を `put` メソッドに渡すこともできます。これにより、Flysystem の基礎となるストリーム サポートが使用されます。すべてのファイル パスは、ディスクに構成された「ルート」の場所を基準にして指定する必要があることに注意してください。

    use Illuminate\Support\Facades\Storage;

    Storage::put('file.jpg', $contents);

    Storage::put('file.jpg', $resource);

<a name="failed-writes"></a>
#### 失敗した書き込み

`put` メソッド (または他の「書き込み」操作) がファイルをディスクに書き込むことができない場合、`false` が返されます。

    if (! Storage::put('file.jpg', $contents)) {
        // The file could not be written to disk...
    }

必要に応じて、ファイルシステム ディスクの構成配列内で `throw` オプションを定義できます。このオプションが `true` として定義されている場合、書き込み操作が失敗すると、`put` などの「書き込み」メソッドは `League\Flysystem\UnableToWriteFile` のインスタンスをスローします。

    'public' => [
        'driver' => 'local',
        // ...
        'throw' => true,
    ],

<a name="prepending-appending-to-files"></a>
### ファイルの先頭および末尾に追加する

`prepend` メソッドと `append` メソッドを使用すると、ファイルの先頭または末尾に書き込むことができます。

    Storage::prepend('file.log', 'Prepended Text');

    Storage::append('file.log', 'Appended Text');

<a name="copying-moving-files"></a>
### ファイルのコピーと移動

`copy` メソッドは既存のファイルをディスク上の新しい場所にコピーするために使用できますが、`move` メソッドは既存のファイルの名前を変更したり、既存のファイルを新しい場所に移動したりするために使用できます。

    Storage::copy('old/file.jpg', 'new/file.jpg');

    Storage::move('old/file.jpg', 'new/file.jpg');

<a name="automatic-streaming"></a>
### 自動ストリーミング

ファイルをストレージにストリーミングすると、メモリ使用量が大幅に削減されます。 Laravel で指定されたファイルの保存場所へのストリーミングを自動的に管理したい場合は、`putFile` または `putFileAs` メソッドを使用できます。このメソッドは、`Illuminate\Http\File` または `Illuminate\Http\UploadedFile` インスタンスを受け入れ、ファイルを目的の場所に自動的にストリーミングします。

    use Illuminate\Http\File;
    use Illuminate\Support\Facades\Storage;

    // Automatically generate a unique ID for filename...
    $path = Storage::putFile('photos', new File('/path/to/photo'));

    // Manually specify a filename...
    $path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');

`putFile` メソッドについては、注意すべき重要な点がいくつかあります。ファイル名ではなくディレクトリ名のみを指定したことに注意してください。デフォルトでは、`putFile` メソッドはファイル名として機能する一意の ID を生成します。ファイルの拡張子は、ファイルの MIME タイプを調べることによって決定されます。ファイルへのパスは `putFile` メソッドによって返されるため、生成されたファイル名を含むパスをデータベースに保存できます。

`putFile` メソッドと `putFileAs` メソッドは、保存されたファイルの「可視性」を指定する引数も受け入れます。これは、Amazon S3 などのクラウド ディスクにファイルを保存しており、生成された URL を介してファイルにパブリックにアクセスできるようにしたい場合に特に便利です。

    Storage::putFile('photos', new File('/path/to/photo'), 'public');

<a name="file-uploads"></a>
### ファイルのアップロード

Web アプリケーションでは、ファイルを保存するための最も一般的な使用例の 1 つは、写真やドキュメントなどのユーザーがアップロードしたファイルを保存することです。 Laravel では、アップロードされたファイルインスタンスで `store` メソッドを使用して、アップロードされたファイルを非常に簡単に保存できます。アップロードされたファイルを保存するパスを指定して、`store` メソッドを呼び出します。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;

    class UserAvatarController extends Controller
    {
        /**
         * Update the avatar for the user.
         */
        public function update(Request $request): string
        {
            $path = $request->file('avatar')->store('avatars');

            return $path;
        }
    }

この例については、注意すべき重要な点がいくつかあります。ファイル名ではなく、ディレクトリ名のみを指定したことに注意してください。デフォルトでは、`store` メソッドはファイル名として機能する一意の ID を生成します。ファイルの拡張子は、ファイルの MIME タイプを調べることによって決定されます。ファイルへのパスは `store` メソッドによって返されるため、生成されたファイル名を含むパスをデータベースに保存できます。

`Storage` ファサードで `putFile` メソッドを呼び出して、上記の例と同じファイルストレージ操作を実行することもできます。

    $path = Storage::putFile('avatars', $request->file('avatar'));

<a name="specifying-a-file-name"></a>
#### ファイル名の指定

保存されたファイルにファイル名を自動的に割り当てたくない場合は、パス、ファイル名、および (オプションの) ディスクを引数として受け取る `storeAs` メソッドを使用できます。

    $path = $request->file('avatar')->storeAs(
        'avatars', $request->user()->id
    );

`Storage` ファサードで `putFileAs` メソッドを使用することもできます。これにより、上記の例と同じファイルストレージ操作が実行されます。

    $path = Storage::putFileAs(
        'avatars', $request->file('avatar'), $request->user()->id
    );

> [!WARNING]  
> 印刷不可能な Unicode 文字や無効な Unicode 文字は、ファイル パスから自動的に削除されます。したがって、ファイルパスをLaravelのファイルストレージメソッドに渡す前に、ファイルパスをサニタイズすることをお勧めします。ファイル パスは、`League\Flysystem\WhitespacePathNormalizer::normalizePath` メソッドを使用して正規化されます。

<a name="specifying-a-disk"></a>
#### ディスクの指定

デフォルトでは、このアップロードされたファイルの `store` メソッドはデフォルトのディスクを使用します。別のディスクを指定する場合は、ディスク名を 2 番目の引数として `store` メソッドに渡します。

    $path = $request->file('avatar')->store(
        'avatars/'.$request->user()->id, 's3'
    );

`storeAs` メソッドを使用している場合は、ディスク名を 3 番目の引数としてメソッドに渡すことができます。

    $path = $request->file('avatar')->storeAs(
        'avatars',
        $request->user()->id,
        's3'
    );

<a name="other-uploaded-file-information"></a>
#### その他のアップロードされたファイル情報

アップロードされたファイルの元の名前と拡張子を取得したい場合は、`getClientOriginalName` メソッドと `getClientOriginalExtension` メソッドを使用して取得できます。

    $file = $request->file('avatar');

    $name = $file->getClientOriginalName();
    $extension = $file->getClientOriginalExtension();

ただし、`getClientOriginalName` メソッドと `getClientOriginalExtension` メソッドは、ファイル名と拡張子が悪意のあるユーザーによって改ざんされる可能性があるため、安全ではないとみなされることに注意してください。このため、指定されたファイルのアップロードの名前と拡張子を取得するには、通常、`hashName` メソッドと `extension` メソッドを使用することをお勧めします。

    $file = $request->file('avatar');

    $name = $file->hashName(); // Generate a unique, random name...
    $extension = $file->extension(); // Determine the file's extension based on the file's MIME type...

<a name="file-visibility"></a>
### ファイルの可視性

Laravel の Flysystem 統合では、「可視性」は複数のプラットフォームにわたるファイルのアクセス許可を抽象化したものです。ファイルは、`public` または `private` として宣言できます。ファイルが `public` と宣言されている場合、そのファイルは通常、他のユーザーがアクセスできる必要があることを示しています。たとえば、S3 ドライバを使用する場合、`public` ファイルの URL を取得できます。

`put` メソッドを使用してファイルを書き込むときに、可視性を設定できます。

    use Illuminate\Support\Facades\Storage;

    Storage::put('file.jpg', $contents, 'public');

ファイルがすでに保存されている場合は、`getVisibility` メソッドと `setVisibility` メソッドを使用してその可視性を取得および設定できます。

    $visibility = Storage::getVisibility('file.jpg');

    Storage::setVisibility('file.jpg', 'public');

アップロードされたファイルを操作する場合、`storePublicly` メソッドと `storePubliclyAs` メソッドを使用して、アップロードされたファイルを `public` 可視性で保存できます。

    $path = $request->file('avatar')->storePublicly('avatars', 's3');

    $path = $request->file('avatar')->storePubliclyAs(
        'avatars',
        $request->user()->id,
        's3'
    );

<a name="local-files-and-visibility"></a>
#### ローカル ファイルと可視性

`local` ドライバを使用する場合、`public` [visibility](#file-visibility) は、ディレクトリに対する `0755` 権限とファイルに対する `0644` 権限に変換されます。アプリケーションの `filesystems` 構成ファイルで権限マッピングを変更できます。

    'local' => [
        'driver' => 'local',
        'root' => storage_path('app'),
        'permissions' => [
            'file' => [
                'public' => 0644,
                'private' => 0600,
            ],
            'dir' => [
                'public' => 0755,
                'private' => 0700,
            ],
        ],
    ],

<a name="deleting-files"></a>
## ファイルの削除 (Deleting Files)

`delete` メソッドは、削除する単一のファイル名またはファイルの配列を受け入れます。

    use Illuminate\Support\Facades\Storage;

    Storage::delete('file.jpg');

    Storage::delete(['file.jpg', 'file2.jpg']);

必要に応じて、ファイルを削除するディスクを指定できます。

    use Illuminate\Support\Facades\Storage;

    Storage::disk('s3')->delete('path/file.jpg');

<a name="directories"></a>
## ディレクトリ (Directories)

<a name="get-all-files-within-a-directory"></a>
#### ディレクトリ内のすべてのファイルを取得する

`files` メソッドは、指定されたディレクトリ内のすべてのファイルの配列を返します。すべてのサブディレクトリを含む、指定されたディレクトリ内のすべてのファイルのリストを取得したい場合は、`allFiles` メソッドを使用できます。

    use Illuminate\Support\Facades\Storage;

    $files = Storage::files($directory);

    $files = Storage::allFiles($directory);

<a name="get-all-directories-within-a-directory"></a>
#### ディレクトリ内のすべてのディレクトリを取得する

`directories` メソッドは、指定されたディレクトリ内のすべてのディレクトリの配列を返します。さらに、`allDirectories` メソッドを使用して、指定されたディレクトリ内のすべてのディレクトリとそのすべてのサブディレクトリのリストを取得できます。

    $directories = Storage::directories($directory);

    $directories = Storage::allDirectories($directory);

<a name="create-a-directory"></a>
#### ディレクトリを作成する

`makeDirectory` メソッドは、必要なサブディレクトリを含む指定されたディレクトリを作成します。

    Storage::makeDirectory($directory);

<a name="delete-a-directory"></a>
#### ディレクトリを削除する

最後に、`deleteDirectory` メソッドを使用して、ディレクトリとそのすべてのファイルを削除できます。

    Storage::deleteDirectory($directory);

<a name="testing"></a>
## テスト (Testing)

`Storage` ファサードの `fake` メソッドを使用すると、偽のディスクを簡単に生成でき、`Illuminate\Http\UploadedFile` クラスのファイル生成ユーティリティと組み合わせることで、ファイルのアップロードのテストが大幅に簡素化されます。例えば：

    <?php

    namespace Tests\Feature;

    use Illuminate\Http\UploadedFile;
    use Illuminate\Support\Facades\Storage;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_albums_can_be_uploaded(): void
        {
            Storage::fake('photos');

            $response = $this->json('POST', '/photos', [
                UploadedFile::fake()->image('photo1.jpg'),
                UploadedFile::fake()->image('photo2.jpg')
            ]);

            // Assert one or more files were stored...
            Storage::disk('photos')->assertExists('photo1.jpg');
            Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

            // Assert one or more files were not stored...
            Storage::disk('photos')->assertMissing('missing.jpg');
            Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

            // Assert that a given directory is empty...
            Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
        }
    }

デフォルトでは、`fake` メソッドは一時ディレクトリ内のすべてのファイルを削除します。これらのファイルを保持したい場合は、代わりに「persistentFake」メソッドを使用できます。ファイルのアップロードのテストの詳細については、[ファイルのアップロードに関する HTTP テストのドキュメントの情報](/docs/{{version}}/http-tests#testing-file-uploads) を参照してください。

> [!WARNING]  
> `image` メソッドには、[GD拡張](https://www.php.net/manual/en/book.image.php) が必要です。

<a name="custom-filesystems"></a>
## カスタム ファイルシステム (Custom Filesystems)

Laravel の Flysystem 統合は、すぐに使用できるいくつかの「ドライバ」のサポートを提供します。ただし、Flysystem はこれらに限定されず、他の多くのストレージ システム用のアダプタを備えています。 Laravel アプリケーションでこれらの追加アダプターのいずれかを使用する場合は、カスタムドライバを作成できます。

カスタム ファイルシステムを定義するには、Flysystem アダプターが必要です。コミュニティが管理する Dropbox アダプターをプロジェクトに追加しましょう。

```shell
composer require spatie/flysystem-dropbox
```

次に、アプリケーションのいずれかの [サービスプロバイダ](/docs/{{version}}/providers) の `boot` メソッド内でドライバを登録できます。これを実現するには、`Storage` ファサードの `extend` メソッドを使用する必要があります。

    <?php

    namespace App\Providers;

    use Illuminate\Contracts\Foundation\Application;
    use Illuminate\Filesystem\FilesystemAdapter;
    use Illuminate\Support\Facades\Storage;
    use Illuminate\Support\ServiceProvider;
    use League\Flysystem\Filesystem;
    use Spatie\Dropbox\Client as DropboxClient;
    use Spatie\FlysystemDropbox\DropboxAdapter;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         */
        public function register(): void
        {
            // ...
        }

        /**
         * Bootstrap any application services.
         */
        public function boot(): void
        {
            Storage::extend('dropbox', function (Application $app, array $config) {
                $adapter = new DropboxAdapter(new DropboxClient(
                    $config['authorization_token']
                ));

                return new FilesystemAdapter(
                    new Filesystem($adapter, $config),
                    $adapter,
                    $config
                );
            });
        }
    }

`extend` メソッドの最初の引数はドライバの名前で、2 番目の引数は `$app` 変数と `$config` 変数を受け取るクロージャです。クロージャーは `Illuminate\Filesystem\FilesystemAdapter` のインスタンスを返す必要があります。 `$config` 変数には、指定されたディスクの `config/filesystems.php` で定義された値が含まれます。

拡張機能のサービスプロバイダを作成して登録すると、`config/filesystems.php` 構成ファイルで `dropbox` ドライバを使用できるようになります。

