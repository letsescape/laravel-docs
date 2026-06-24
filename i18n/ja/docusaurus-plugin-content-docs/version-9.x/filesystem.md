<!-- # File Storage -->
# File Storage

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [The Local Driver](#the-local-driver)
    - [The Public Disk](#the-public-disk)
    - [Driver Prerequisites](#driver-prerequisites)
    - [Scoped & Read-Only Filesystems](#scoped-and-read-only-filesystems)
    - [Amazon S3 Compatible Filesystems](#amazon-s3-compatible-filesystems)
- [Obtaining Disk Instances](#obtaining-disk-instances)
    - [On-Demand Disks](#on-demand-disks)
- [Retrieving Files](#retrieving-files)
    - [Downloading Files](#downloading-files)
    - [File URLs](#file-urls)
    - [File Metadata](#file-metadata)
- [Storing Files](#storing-files)
    - [Prepending & Appending To Files](#prepending-appending-to-files)
    - [Copying & Moving Files](#copying-moving-files)
    - [Automatic Streaming](#automatic-streaming)
    - [File Uploads](#file-uploads)
    - [File Visibility](#file-visibility)
- [Deleting Files](#deleting-files)
- [Directories](#directories)
- [Custom Filesystems](#custom-filesystems)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides a powerful filesystem abstraction thanks to the wonderful [Flysystem](https://github.com/thephpleague/flysystem) PHP package by Frank de Jonge. The Laravel Flysystem integration provides simple drivers for working with local filesystems, SFTP, and Amazon S3. Even better, it's amazingly simple to switch between these storage options between your local development machine and production server as the API remains the same for each system. -->
Laravel は、Frank de Jonge による素晴らしい [Flysystem](https://github.com/thephpleague/flysystem) PHP パッケージのおかげで、強力なファイルシステムの抽象化を提供します。 Laravel Flysystem 統合では、ローカル ファイルシステム、SFTP、Amazon S3 を操作するためのシンプルなドライバが提供されます。さらに良いことに、API は各システムで同じままであるため、ローカル開発マシンと運用サーバーの間でこれらのストレージ オプションを切り替えるのは驚くほど簡単です。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Laravel's filesystem configuration file is located at `config/filesystems.php`. Within this file, you may configure all of your filesystem "disks". Each disk represents a particular storage driver and storage location. Example configurations for each supported driver are included in the configuration file so you can modify the configuration to reflect your storage preferences and credentials. -->
Laravel のファイルシステム構成ファイルは、`config/filesystems.php` にあります。このファイル内で、すべてのファイルシステムの「ディスク」を構成できます。各ディスクは、特定のストレージ ドライバとストレージの場所を表します。サポートされている各ドライバの構成例が構成ファイルに含まれているため、ストレージ設定と資格情報を反映するように構成を変更できます。

<!-- The `local` driver interacts with files stored locally on the server running the Laravel application while the `s3` driver is used to write to Amazon's S3 cloud storage service. -->
`local` ドライバは、Laravel アプリケーションを実行しているサーバー上にローカルに保存されているファイルと対話し、`s3` ドライバは Amazon の S3 クラウド ストレージ サービスへの書き込みに使用されます。

> [!NOTE]
> ディスクは好きなだけ構成でき、同じドライバを使用する複数のディスクを使用することもできます。

<a name="the-local-driver"></a>
<!-- ### The Local Driver -->
### The Local Driver

<!-- When using the `local` driver, all file operations are relative to the `root` directory defined in your `filesystems` configuration file. By default, this value is set to the `storage/app` directory. Therefore, the following method would write to `storage/app/example.txt`: -->
`local` ドライバを使用する場合、すべてのファイル操作は、`filesystems` 構成ファイルで定義された `root` ディレクトリに対して相対的に行われます。デフォルトでは、この値は `storage/app` ディレクトリに設定されます。したがって、次のメソッドは `storage/app/example.txt` に書き込みます。

```
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
<!-- ### The Public Disk -->
### The Public Disk

<!-- The `public` disk included in your application's `filesystems` configuration file is intended for files that are going to be publicly accessible. By default, the `public` disk uses the `local` driver and stores its files in `storage/app/public`. -->
アプリケーションの `filesystems` 構成ファイルに含まれる `public` ディスクは、パブリックにアクセスできるファイル用です。デフォルトでは、`public` ディスクは `local` ドライバを使用し、そのファイルを `storage/app/public` に保存します。

<!-- To make these files accessible from the web, you should create a symbolic link from `public/storage` to `storage/app/public`. Utilizing this folder convention will keep your publicly accessible files in one directory that can be easily shared across deployments when using zero down-time deployment systems like [Envoyer](https://envoyer.io). -->
これらのファイルに Web からアクセスできるようにするには、`public/storage` から `storage/app/public` へのシンボリック リンクを作成する必要があります。このフォルダー規則を利用すると、パブリックにアクセスできるファイルが 1 つのディレクトリに保存され、[Envoyer](https://envoyer.io) のようなダウンタイムなしの展開システムを使用する場合、展開間で簡単に共有できます。

<!-- To create the symbolic link, you may use the `storage:link` Artisan command: -->
シンボリック リンクを作成するには、`storage:link` Artisan コマンドを使用できます。

```shell
php artisan storage:link
```

<!-- Once a file has been stored and the symbolic link has been created, you can create a URL to the files using the `asset` helper: -->
ファイルが保存され、シンボリック リンクが作成されたら、`asset` ヘルパを使用してファイルへの URL を作成できます。

```
echo asset('storage/file.txt');
```

<!-- You may configure additional symbolic links in your `filesystems` configuration file. Each of the configured links will be created when you run the `storage:link` command: -->
`filesystems` 構成ファイルで追加のシンボリック リンクを構成できます。構成された各リンクは、`storage:link` コマンドを実行すると作成されます。

```
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="s3-driver-configuration"></a>
<!-- #### S3 Driver Configuration -->
#### S3 Driver Configuration

<!-- Before using the S3 driver, you will need to install the Flysystem S3 package via the Composer package manager: -->
S3 ドライバを使用する前に、Composer パッケージ マネージャーを介して Flysystem S3 パッケージをインストールする必要があります。

```shell
composer require league/flysystem-aws-s3-v3 "^3.0"
```

<!-- The S3 driver configuration information is located in your `config/filesystems.php` configuration file. This file contains an example configuration array for an S3 driver. You are free to modify this array with your own S3 configuration and credentials. For convenience, these environment variables match the naming convention used by the AWS CLI. -->
S3 ドライバの構成情報は、`config/filesystems.php` 構成ファイルにあります。このファイルには、S3 ドライバの構成配列の例が含まれています。このアレイは、独自の S3 構成と認証情報を使用して自由に変更できます。便宜上、これらの環境変数は AWS CLI で使用される命名規則と一致しています。

<a name="ftp-driver-configuration"></a>
<!-- #### FTP Driver Configuration -->
#### FTP Driver Configuration

<!-- Before using the FTP driver, you will need to install the Flysystem FTP package via the Composer package manager: -->
FTP ドライバを使用する前に、Composer パッケージ マネージャーを介して Flysystem FTP パッケージをインストールする必要があります。

```shell
composer require league/flysystem-ftp "^3.0"
```

<!-- Laravel's Flysystem integrations work great with FTP; however, a sample configuration is not included with the framework's default `filesystems.php` configuration file. If you need to configure an FTP filesystem, you may use the configuration example below: -->
Laravel の Flysystem 統合は FTP とうまく連携します。ただし、サンプル構成はフレームワークのデフォルトの `filesystems.php` 構成ファイルには含まれていません。 FTP ファイルシステムを構成する必要がある場合は、以下の構成例を使用できます。

```
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
```

<a name="sftp-driver-configuration"></a>
<!-- #### SFTP Driver Configuration -->
#### SFTP Driver Configuration

<!-- Before using the SFTP driver, you will need to install the Flysystem SFTP package via the Composer package manager: -->
SFTP ドライバを使用する前に、Composer パッケージ マネージャーを介して Flysystem SFTP パッケージをインストールする必要があります。

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

<!-- Laravel's Flysystem integrations work great with SFTP; however, a sample configuration is not included with the framework's default `filesystems.php` configuration file. If you need to configure an SFTP filesystem, you may use the configuration example below: -->
Laravel の Flysystem 統合は SFTP とうまく連携します。ただし、サンプル構成はフレームワークのデフォルトの `filesystems.php` 構成ファイルには含まれていません。 SFTP ファイルシステムを構成する必要がある場合は、以下の構成例を使用できます。

```
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // Settings for basic authentication...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // Settings for SSH key based authentication with encryption password...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // Optional SFTP Settings...
    // 'hostFingerprint' => env('SFTP_HOST_FINGERPRINT'),
    // 'maxTries' => 4,
    // 'passphrase' => env('SFTP_PASSPHRASE'),
    // 'port' => env('SFTP_PORT', 22),
    // 'root' => env('SFTP_ROOT', ''),
    // 'timeout' => 30,
    // 'useAgent' => true,
],
```

<a name="scoped-and-read-only-filesystems"></a>
<!-- ### Scoped & Read-Only Filesystems -->
### Scoped & Read-Only Filesystems

<!-- Scoped disks allow you to define a filesystem where all paths are automatically prefixed with a given path prefix. Before creating a scoped filesystem disk, you will need to install an additional Flysystem package via the Composer package manager: -->
スコープ付きディスクを使用すると、すべてのパスに特定のパス プレフィックスが自動的に付加されるファイル システムを定義できます。スコープ付きファイルシステム ディスクを作成する前に、Composer パッケージ マネージャーを介して追加の Flysystem パッケージをインストールする必要があります。

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

<!-- You may create a path scoped instance of any existing filesystem disk by defining a disk that utilizes the `scoped` driver. For example, you may create a disk which scopes your existing `s3` disk to a specific path prefix, and then every file operation using your scoped disk will utilize the specified prefix: -->
`scoped` ドライバを使用するディスクを定義することにより、既存のファイル システム ディスクのパス スコープのインスタンスを作成できます。たとえば、既存の `s3` ディスクのスコープを特定のパス プレフィックスに設定するディスクを作成すると、スコープ指定されたディスクを使用するすべてのファイル操作で指定されたプレフィックスが使用されます。

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

<!-- "Read-only" disks allow you to create filesystem disks that do not allow write operations. Before using the `read-only` configuration option, you will need to install an additional Flysystem package via the Composer package manager: -->
「読み取り専用」ディスクを使用すると、書き込み操作を許可しないファイルシステム ディスクを作成できます。 `read-only` 構成オプションを使用する前に、Composer パッケージ マネージャーを介して追加の Flysystem パッケージをインストールする必要があります。

```shell
composer require league/flysystem-read-only "^3.0"
```

<!-- Next, you may include the `read-only` configuration option in one or more of your disk's configuration arrays: -->
次に、1 つ以上のディスクの構成配列に `read-only` 構成オプションを含めることができます。

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
<!-- ### Amazon S3 Compatible Filesystems -->
### Amazon S3 Compatible Filesystems

<!-- By default, your application's `filesystems` configuration file contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as [MinIO](https://github.com/minio/minio) or [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/). -->
デフォルトでは、アプリケーションの `filesystems` 構成ファイルには、`s3` ディスクのディスク構成が含まれています。このディスクを使用して Amazon S3 と対話するだけでなく、[MinIO](https://github.com/minio/minio) や [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/) などの S3 互換ファイルストレージ サービスと対話するために使用することもできます。

<!-- Typically, after updating the disk's credentials to match the credentials of the service you are planning to use, you only need to update the value of the `endpoint` configuration option. This option's value is typically defined via the `AWS_ENDPOINT` environment variable: -->
通常、使用する予定のサービスの資格情報と一致するようにディスクの資格情報を更新した後、`endpoint` 構成オプションの値を更新するだけで済みます。このオプションの値は通常、`AWS_ENDPOINT` 環境変数によって定義されます。

```
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="minio"></a>
<!-- #### MinIO -->
#### MinIO

<!-- In order for Laravel's Flysystem integration to generate proper URLs when using MinIO, you should define the `AWS_URL` environment variable so that it matches your application's local URL and includes the bucket name in the URL path: -->
MinIO の使用時に Laravel の Flysystem 統合で適切な URL を生成するには、アプリケーションのローカル URL と一致し、URL パスにバケット名が含まれるように `AWS_URL` 環境変数を定義する必要があります。

```ini
AWS_URL=http://localhost:9000/local
```

> [!WARNING]
> MinIO を使用する場合、`temporaryUrl` メソッドによる一時ストレージ URL の生成はサポートされません。

<a name="obtaining-disk-instances"></a>
<!-- ## Obtaining Disk Instances -->
## Obtaining Disk Instances

<!-- The `Storage` facade may be used to interact with any of your configured disks. For example, you may use the `put` method on the facade to store an avatar on the default disk. If you call methods on the `Storage` facade without first calling the `disk` method, the method will automatically be passed to the default disk: -->
`Storage` ファサードは、構成されたディスクと対話するために使用できます。たとえば、ファサードで `put` メソッドを使用して、デフォルトのディスクにアバターを保存できます。最初に `disk` メソッドを呼び出さずに、`Storage` ファサードでメソッドを呼び出すと、メソッドは自動的にデフォルトのディスクに渡されます。

```
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

<!-- If your application interacts with multiple disks, you may use the `disk` method on the `Storage` facade to work with files on a particular disk: -->
アプリケーションが複数のディスクと対話する場合は、`Storage` ファサードで `disk` メソッドを使用して、特定のディスク上のファイルを操作できます。

```
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
<!-- ### On-Demand Disks -->
### On-Demand Disks

<!-- Sometimes you may wish to create a disk at runtime using a given configuration without that configuration actually being present in your application's `filesystems` configuration file. To accomplish this, you may pass a configuration array to the `Storage` facade's `build` method: -->
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
<!-- ## Retrieving Files -->
## Retrieving Files

<!-- The `get` method may be used to retrieve the contents of a file. The raw string contents of the file will be returned by the method. Remember, all file paths should be specified relative to the disk's "root" location: -->
`get` メソッドは、ファイルの内容を取得するために使用できます。ファイルの生の文字列コンテンツがメソッドによって返されます。すべてのファイル パスは、ディスクの「ルート」の場所を基準にして指定する必要があることに注意してください。

```
$contents = Storage::get('file.jpg');
```

<!-- The `exists` method may be used to determine if a file exists on the disk: -->
`exists` メソッドを使用して、ファイルがディスク上に存在するかどうかを確認できます。

```
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

<!-- The `missing` method may be used to determine if a file is missing from the disk: -->
`missing` メソッドを使用して、ファイルがディスクに欠落しているかどうかを確認できます。

```
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
<!-- ### Downloading Files -->
### Downloading Files

<!-- The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method: -->
`download` メソッドは、ユーザーのブラウザに指定されたパスにファイルをダウンロードさせる応答を生成するために使用できます。 `download` メソッドは、メソッドの 2 番目の引数としてファイル名を受け入れます。これにより、ファイルをダウンロードするユーザーに表示されるファイル名が決まります。最後に、HTTP ヘッダーの配列を 3 番目の引数としてメソッドに渡すことができます。

```
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
<!-- ### File URLs -->
### File URLs

<!-- You may use the `url` method to get the URL for a given file. If you are using the `local` driver, this will typically just prepend `/storage` to the given path and return a relative URL to the file. If you are using the `s3` driver, the fully qualified remote URL will be returned: -->
`url` メソッドを使用して、特定のファイルの URL を取得できます。 `local` ドライバを使用している場合、これは通常、指定されたパスの先頭に `/storage` を追加し、ファイルへの相対 URL を返します。 `s3` ドライバを使用している場合は、完全修飾リモート URL が返されます。

```
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

<!-- When using the `local` driver, all files that should be publicly accessible should be placed in the `storage/app/public` directory. Furthermore, you should [create a symbolic link](#the-public-disk) at `public/storage` which points to the `storage/app/public` directory. -->
`local` ドライバを使用する場合、パブリックにアクセスできるすべてのファイルを `storage/app/public` ディレクトリに配置する必要があります。さらに、`storage/app/public` ディレクトリを指す `public/storage` で [create a symbolic link](#the-public-disk) する必要があります。

> [!WARNING]
> `local` ドライバを使用する場合、`url` の戻り値は URL エンコードされません。このため、常に有効な URL を作成できる名前を使用してファイルを保存することをお勧めします。

<a name="temporary-urls"></a>
<!-- #### Temporary URLs -->
#### Temporary URLs

<!-- Using the `temporaryUrl` method, you may create temporary URLs to files stored using the `s3` driver. This method accepts a path and a `DateTime` instance specifying when the URL should expire: -->
`temporaryUrl` メソッドを使用すると、`s3` ドライバを使用して保存されたファイルへの一時 URL を作成できます。このメソッドは、URL の有効期限がいつ切れるかを指定するパスと `DateTime` インスタンスを受け入れます。

```
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

<!-- If you need to specify additional [S3 request parameters](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests), you may pass the array of request parameters as the third argument to the `temporaryUrl` method: -->
追加の [S3 request parameters](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests) を指定する必要がある場合は、リクエスト パラメーターの配列を 3 番目の引数として `temporaryUrl` メソッドに渡すことができます。

```
$url = Storage::temporaryUrl(
    'file.jpg',
    now()->addMinutes(5),
    [
        'ResponseContentType' => 'application/octet-stream',
        'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
    ]
);
```

<!-- If you need to customize how temporary URLs are created for a specific storage disk, you can use the `buildTemporaryUrlsUsing` method. For example, this can be useful if you have a controller that allows you to download files stored via a disk that doesn't typically support temporary URLs. Usually, this method should be called from the `boot` method of a service provider: -->
特定のストレージ ディスクに対して一時 URL を作成する方法をカスタマイズする必要がある場合は、`buildTemporaryUrlsUsing` メソッドを使用できます。たとえば、これは、通常は一時 URL をサポートしないディスク経由で保存されたファイルをダウンロードできるコントローラを持っている場合に便利です。通常、このメソッドはサービスプロバイダの `boot` メソッドから呼び出す必要があります。

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Storage::disk('local')->buildTemporaryUrlsUsing(function ($path, $expiration, $options) {
            return URL::temporarySignedRoute(
                'files.download',
                $expiration,
                array_merge($options, ['path' => $path])
            );
        });
    }
}
```

<a name="url-host-customization"></a>
<!-- #### URL Host Customization -->
#### URL Host Customization

<!-- If you would like to pre-define the host for URLs generated using the `Storage` facade, you may add a `url` option to the disk's configuration array: -->
`Storage` ファサードを使用して生成された URL のホストを事前定義したい場合は、ディスクの構成配列に `url` オプションを追加できます。

```
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
],
```

<a name="file-metadata"></a>
<!-- ### File Metadata -->
### File Metadata

<!-- In addition to reading and writing files, Laravel can also provide information about the files themselves. For example, the `size` method may be used to get the size of a file in bytes: -->
Laravel は、ファイルの読み取りと書き込みに加えて、ファイル自体に関する情報を提供することもできます。たとえば、`size` メソッドを使用して、ファイルのサイズをバイト単位で取得できます。

```
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

<!-- The `lastModified` method returns the UNIX timestamp of the last time the file was modified: -->
`lastModified` メソッドは、ファイルが最後に変更されたときの UNIX タイムスタンプを返します。

```
$time = Storage::lastModified('file.jpg');
```

<!-- The MIME type of a given file may be obtained via the `mimeType` method: -->
特定のファイルの MIME タイプは、`mimeType` メソッド経由で取得できます。

```
$mime = Storage::mimeType('file.jpg')
```

<a name="file-paths"></a>
<!-- #### File Paths -->
#### File Paths

<!-- You may use the `path` method to get the path for a given file. If you are using the `local` driver, this will return the absolute path to the file. If you are using the `s3` driver, this method will return the relative path to the file in the S3 bucket: -->
`path` メソッドを使用して、特定のファイルのパスを取得できます。 `local` ドライバを使用している場合、ファイルへの絶対パスが返されます。 `s3` ドライバを使用している場合、このメソッドは S3 バケット内のファイルへの相対パスを返します。

```
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
<!-- ## Storing Files -->
## Storing Files

<!-- The `put` method may be used to store file contents on a disk. You may also pass a PHP `resource` to the `put` method, which will use Flysystem's underlying stream support. Remember, all file paths should be specified relative to the "root" location configured for the disk: -->
`put` メソッドは、ファイルの内容をディスクに保存するために使用できます。 PHP `resource` を `put` メソッドに渡すこともできます。これにより、Flysystem の基礎となるストリーム サポートが使用されます。すべてのファイル パスは、ディスクに構成された「ルート」の場所を基準にして指定する必要があることに注意してください。

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
<!-- #### Failed Writes -->
#### Failed Writes

<!-- If the `put` method (or other "write" operations) is unable to write the file to disk, `false` will be returned: -->
`put` メソッド (または他の「書き込み」操作) がファイルをディスクに書き込むことができない場合、`false` が返されます。

```
if (! Storage::put('file.jpg', $contents)) {
    // The file could not be written to disk...
}
```

<!-- If you wish, you may define the `throw` option within your filesystem disk's configuration array. When this option is defined as `true`, "write" methods such as `put` will throw an instance of `League\Flysystem\UnableToWriteFile` when write operations fail: -->
必要に応じて、ファイルシステム ディスクの構成配列内で `throw` オプションを定義できます。このオプションが `true` として定義されている場合、書き込み操作が失敗すると、`put` などの「書き込み」メソッドは `League\Flysystem\UnableToWriteFile` のインスタンスをスローします。

```
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
<!-- ### Prepending & Appending To Files -->
### Prepending & Appending To Files

<!-- The `prepend` and `append` methods allow you to write to the beginning or end of a file: -->
`prepend` メソッドと `append` メソッドを使用すると、ファイルの先頭または末尾に書き込むことができます。

```
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
<!-- ### Copying & Moving Files -->
### Copying & Moving Files

<!-- The `copy` method may be used to copy an existing file to a new location on the disk, while the `move` method may be used to rename or move an existing file to a new location: -->
`copy` メソッドは既存のファイルをディスク上の新しい場所にコピーするために使用できますが、`move` メソッドは既存のファイルの名前を変更したり、既存のファイルを新しい場所に移動したりするために使用できます。

```
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
<!-- ### Automatic Streaming -->
### Automatic Streaming

<!-- Streaming files to storage offers significantly reduced memory usage. If you would like Laravel to automatically manage streaming a given file to your storage location, you may use the `putFile` or `putFileAs` method. This method accepts either an `Illuminate\Http\File` or `Illuminate\Http\UploadedFile` instance and will automatically stream the file to your desired location: -->
ファイルをストレージにストリーミングすると、メモリ使用量が大幅に削減されます。 Laravel で指定されたファイルの保存場所へのストリーミングを自動的に管理したい場合は、`putFile` または `putFileAs` メソッドを使用できます。このメソッドは、`Illuminate\Http\File` または `Illuminate\Http\UploadedFile` インスタンスを受け入れ、ファイルを目的の場所に自動的にストリーミングします。

```
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// Automatically generate a unique ID for filename...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// Manually specify a filename...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

<!-- There are a few important things to note about the `putFile` method. Note that we only specified a directory name and not a filename. By default, the `putFile` method will generate a unique ID to serve as the filename. The file's extension will be determined by examining the file's MIME type. The path to the file will be returned by the `putFile` method so you can store the path, including the generated filename, in your database. -->
`putFile` メソッドについては、注意すべき重要な点がいくつかあります。ファイル名ではなくディレクトリ名のみを指定したことに注意してください。デフォルトでは、`putFile` メソッドはファイル名として機能する一意の ID を生成します。ファイルの拡張子は、ファイルの MIME タイプを調べることによって決定されます。ファイルへのパスは `putFile` メソッドによって返されるため、生成されたファイル名を含むパスをデータベースに保存できます。

<!-- The `putFile` and `putFileAs` methods also accept an argument to specify the "visibility" of the stored file. This is particularly useful if you are storing the file on a cloud disk such as Amazon S3 and would like the file to be publicly accessible via generated URLs: -->
`putFile` メソッドと `putFileAs` メソッドは、保存されたファイルの「可視性」を指定する引数も受け入れます。これは、Amazon S3 などのクラウド ディスクにファイルを保存しており、生成された URL を介してファイルにパブリックにアクセスできるようにしたい場合に特に便利です。

```
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
<!-- ### File Uploads -->
### File Uploads

<!-- In web applications, one of the most common use-cases for storing files is storing user uploaded files such as photos and documents. Laravel makes it very easy to store uploaded files using the `store` method on an uploaded file instance. Call the `store` method with the path at which you wish to store the uploaded file: -->
Web アプリケーションでは、ファイルを保存するための最も一般的な使用例の 1 つは、写真やドキュメントなどのユーザーがアップロードしたファイルを保存することです。 Laravel では、アップロードされたファイルインスタンスで `store` メソッドを使用して、アップロードされたファイルを非常に簡単に保存できます。アップロードされたファイルを保存するパスを指定して、`store` メソッドを呼び出します。

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * Update the avatar for the user.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request)
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

<!-- There are a few important things to note about this example. Note that we only specified a directory name, not a filename. By default, the `store` method will generate a unique ID to serve as the filename. The file's extension will be determined by examining the file's MIME type. The path to the file will be returned by the `store` method so you can store the path, including the generated filename, in your database. -->
この例については、注意すべき重要な点がいくつかあります。ファイル名ではなく、ディレクトリ名のみを指定したことに注意してください。デフォルトでは、`store` メソッドはファイル名として機能する一意の ID を生成します。ファイルの拡張子は、ファイルの MIME タイプを調べることによって決定されます。ファイルへのパスは `store` メソッドによって返されるため、生成されたファイル名を含むパスをデータベースに保存できます。

<!-- You may also call the `putFile` method on the `Storage` facade to perform the same file storage operation as the example above: -->
`Storage` ファサードで `putFile` メソッドを呼び出して、上記の例と同じファイルストレージ操作を実行することもできます。

```
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
<!-- #### Specifying A File Name -->
#### Specifying A File Name

<!-- If you do not want a filename to be automatically assigned to your stored file, you may use the `storeAs` method, which receives the path, the filename, and the (optional) disk as its arguments: -->
保存されたファイルにファイル名を自動的に割り当てたくない場合は、パス、ファイル名、および (オプションの) ディスクを引数として受け取る `storeAs` メソッドを使用できます。

```
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

<!-- You may also use the `putFileAs` method on the `Storage` facade, which will perform the same file storage operation as the example above: -->
`Storage` ファサードで `putFileAs` メソッドを使用することもできます。これにより、上記の例と同じファイルストレージ操作が実行されます。

```
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 印刷不可能な Unicode 文字や無効な Unicode 文字は、ファイル パスから自動的に削除されます。したがって、ファイルパスをLaravelのファイルストレージメソッドに渡す前に、ファイルパスをサニタイズすることをお勧めします。ファイル パスは、`League\Flysystem\WhitespacePathNormalizer::normalizePath` メソッドを使用して正規化されます。

<a name="specifying-a-disk"></a>
<!-- #### Specifying A Disk -->
#### Specifying A Disk

<!-- By default, this uploaded file's `store` method will use your default disk. If you would like to specify another disk, pass the disk name as the second argument to the `store` method: -->
デフォルトでは、このアップロードされたファイルの `store` メソッドはデフォルトのディスクを使用します。別のディスクを指定する場合は、ディスク名を 2 番目の引数として `store` メソッドに渡します。

```
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

<!-- If you are using the `storeAs` method, you may pass the disk name as the third argument to the method: -->
`storeAs` メソッドを使用している場合は、ディスク名を 3 番目の引数としてメソッドに渡すことができます。

```
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="other-uploaded-file-information"></a>
<!-- #### Other Uploaded File Information -->
#### Other Uploaded File Information

<!-- If you would like to get the original name and extension of the uploaded file, you may do so using the `getClientOriginalName` and `getClientOriginalExtension` methods: -->
アップロードされたファイルの元の名前と拡張子を取得したい場合は、`getClientOriginalName` メソッドと `getClientOriginalExtension` メソッドを使用して取得できます。

```
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

<!-- However, keep in mind that the `getClientOriginalName` and `getClientOriginalExtension` methods are considered unsafe, as the file name and extension may be tampered with by a malicious user. For this reason, you should typically prefer the `hashName` and `extension` methods to get a name and an extension for the given file upload: -->
ただし、`getClientOriginalName` メソッドと `getClientOriginalExtension` メソッドは、ファイル名と拡張子が悪意のあるユーザーによって改ざんされる可能性があるため、安全ではないとみなされることに注意してください。このため、指定されたファイルのアップロードの名前と拡張子を取得するには、通常、`hashName` メソッドと `extension` メソッドを使用することをお勧めします。

```
$file = $request->file('avatar');

$name = $file->hashName(); // Generate a unique, random name...
$extension = $file->extension(); // Determine the file's extension based on the file's MIME type...
```

<a name="file-visibility"></a>
<!-- ### File Visibility -->
### File Visibility

<!-- In Laravel's Flysystem integration, "visibility" is an abstraction of file permissions across multiple platforms. Files may either be declared `public` or `private`. When a file is declared `public`, you are indicating that the file should generally be accessible to others. For example, when using the S3 driver, you may retrieve URLs for `public` files. -->
Laravel の Flysystem 統合では、「可視性」は複数のプラットフォームにわたるファイルのアクセス許可を抽象化したものです。ファイルは、`public` または `private` として宣言できます。ファイルが `public` と宣言されている場合、そのファイルは通常、他のユーザーがアクセスできる必要があることを示しています。たとえば、S3 ドライバを使用する場合、`public` ファイルの URL を取得できます。

<!-- You can set the visibility when writing the file via the `put` method: -->
`put` メソッドを使用してファイルを書き込むときに、可視性を設定できます。

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

<!-- If the file has already been stored, its visibility can be retrieved and set via the `getVisibility` and `setVisibility` methods: -->
ファイルがすでに保存されている場合は、`getVisibility` メソッドと `setVisibility` メソッドを使用してその可視性を取得および設定できます。

```
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

<!-- When interacting with uploaded files, you may use the `storePublicly` and `storePubliclyAs` methods to store the uploaded file with `public` visibility: -->
アップロードされたファイルを操作する場合、`storePublicly` メソッドと `storePubliclyAs` メソッドを使用して、アップロードされたファイルを `public` 可視性で保存できます。

```
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="local-files-and-visibility"></a>
<!-- #### Local Files & Visibility -->
#### Local Files & Visibility

<!-- When using the `local` driver, `public` [visibility](#file-visibility) translates to `0755` permissions for directories and `0644` permissions for files. You can modify the permissions mappings in your application's `filesystems` configuration file: -->
`local` ドライバを使用する場合、`public` [visibility](#file-visibility) は、ディレクトリに対する `0755` 権限とファイルに対する `0644` 権限に変換されます。アプリケーションの `filesystems` 構成ファイルで権限マッピングを変更できます。

```
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
```

<a name="deleting-files"></a>
<!-- ## Deleting Files -->
## Deleting Files

<!-- The `delete` method accepts a single filename or an array of files to delete: -->
`delete` メソッドは、削除する単一のファイル名またはファイルの配列を受け入れます。

```
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

<!-- If necessary, you may specify the disk that the file should be deleted from: -->
必要に応じて、ファイルを削除するディスクを指定できます。

```
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
<!-- ## Directories -->
## Directories

<a name="get-all-files-within-a-directory"></a>
<!-- #### Get All Files Within A Directory -->
#### Get All Files Within A Directory

<!-- The `files` method returns an array of all of the files in a given directory. If you would like to retrieve a list of all files within a given directory including all subdirectories, you may use the `allFiles` method: -->
`files` メソッドは、指定されたディレクトリ内のすべてのファイルの配列を返します。すべてのサブディレクトリを含む、指定されたディレクトリ内のすべてのファイルのリストを取得したい場合は、`allFiles` メソッドを使用できます。

```
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
<!-- #### Get All Directories Within A Directory -->
#### Get All Directories Within A Directory

<!-- The `directories` method returns an array of all the directories within a given directory. Additionally, you may use the `allDirectories` method to get a list of all directories within a given directory and all of its subdirectories: -->
`directories` メソッドは、指定されたディレクトリ内のすべてのディレクトリの配列を返します。さらに、`allDirectories` メソッドを使用して、指定されたディレクトリ内のすべてのディレクトリとそのすべてのサブディレクトリのリストを取得できます。

```
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
<!-- #### Create A Directory -->
#### Create A Directory

<!-- The `makeDirectory` method will create the given directory, including any needed subdirectories: -->
`makeDirectory` メソッドは、必要なサブディレクトリを含む指定されたディレクトリを作成します。

```
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
<!-- #### Delete A Directory -->
#### Delete A Directory

<!-- Finally, the `deleteDirectory` method may be used to remove a directory and all of its files: -->
最後に、`deleteDirectory` メソッドを使用して、ディレクトリとそのすべてのファイルを削除できます。

```
Storage::deleteDirectory($directory);
```

<a name="custom-filesystems"></a>
<!-- ## Custom Filesystems -->
## Custom Filesystems

<!-- Laravel's Flysystem integration provides support for several "drivers" out of the box; however, Flysystem is not limited to these and has adapters for many other storage systems. You can create a custom driver if you want to use one of these additional adapters in your Laravel application. -->
Laravel の Flysystem 統合は、すぐに使用できるいくつかの「ドライバ」のサポートを提供します。ただし、Flysystem はこれらに限定されず、他の多くのストレージ システム用のアダプタを備えています。 Laravel アプリケーションでこれらの追加アダプターのいずれかを使用する場合は、カスタムドライバを作成できます。

<!-- In order to define a custom filesystem you will need a Flysystem adapter. Let's add a community maintained Dropbox adapter to our project: -->
カスタム ファイルシステムを定義するには、Flysystem アダプターが必要です。コミュニティが管理する Dropbox アダプターをプロジェクトに追加しましょう。

```shell
composer require spatie/flysystem-dropbox
```

<!-- Next, you can register the driver within the `boot` method of one of your application's [service providers](/docs/9.x/providers). To accomplish this, you should use the `extend` method of the `Storage` facade: -->
次に、アプリケーションのいずれかの [service providers](/docs/9.x/providers) の `boot` メソッド内でドライバを登録できます。これを実現するには、`Storage` ファサードの `extend` メソッドを使用する必要があります。

```
<?php

namespace App\Providers;

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
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Storage::extend('dropbox', function ($app, $config) {
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
```

<!-- The first argument of the `extend` method is the name of the driver and the second is a closure that receives the `$app` and `$config` variables. The closure must return an instance of `Illuminate\Filesystem\FilesystemAdapter`. The `$config` variable contains the values defined in `config/filesystems.php` for the specified disk. -->
`extend` メソッドの最初の引数はドライバの名前で、2 番目の引数は `$app` 変数と `$config` 変数を受け取るクロージャです。クロージャーは `Illuminate\Filesystem\FilesystemAdapter` のインスタンスを返す必要があります。 `$config` 変数には、指定されたディスクの `config/filesystems.php` で定義された値が含まれます。

<!-- Once you have created and registered the extension's service provider, you may use the `dropbox` driver in your `config/filesystems.php` configuration file. -->
拡張機能のサービスプロバイダを作成して登録すると、`config/filesystems.php` 構成ファイルで `dropbox` ドライバを使用できるようになります。

