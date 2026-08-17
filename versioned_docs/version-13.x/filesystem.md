<!-- # File Storage -->
# File Storage

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [The Local Driver](#the-local-driver)
    - [The Public Disk](#the-public-disk)
    - [Driver Prerequisites](#driver-prerequisites)
    - [Scoped and Read-Only Filesystems](#scoped-and-read-only-filesystems)
    - [Amazon S3 Compatible Filesystems](#amazon-s3-compatible-filesystems)
- [Obtaining Disk Instances](#obtaining-disk-instances)
    - [On-Demand Disks](#on-demand-disks)
- [Retrieving Files](#retrieving-files)
    - [Downloading Files](#downloading-files)
    - [File URLs](#file-urls)
    - [Temporary URLs](#temporary-urls)
    - [File Metadata](#file-metadata)
- [Storing Files](#storing-files)
    - [Prepending and Appending To Files](#prepending-appending-to-files)
    - [Copying and Moving Files](#copying-moving-files)
    - [Automatic Streaming](#automatic-streaming)
    - [File Uploads](#file-uploads)
    - [File Visibility](#file-visibility)
    - [Image Manipulation](#image-manipulation)
- [Deleting Files](#deleting-files)
- [Directories](#directories)
- [Testing](#testing)
- [Custom Filesystems](#custom-filesystems)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides a powerful filesystem abstraction thanks to the wonderful [Flysystem](https://github.com/thephpleague/flysystem) PHP package by Frank de Jonge. The Laravel Flysystem integration provides simple drivers for working with local filesystems, SFTP, and Amazon S3. Even better, it's amazingly simple to switch between these storage options between your local development machine and production server as the API remains the same for each system. -->
Laravel은 Frank de Jonge가 개발한 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지 덕분에 강력한 파일 시스템 추상화를 제공합니다. Laravel의 Flysystem 통합 기능은 로컬 파일 시스템, SFTP, Amazon S3와 쉽게 연동할 수 있는 간단한 드라이버를 제공합니다. 더 좋은 점은, 각 스토리지 시스템의 API가 동일하게 유지되기 때문에, 로컬 개발 환경과 프로덕션 서버 간의 스토리지 옵션을 손쉽게 전환할 수 있다는 것입니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Laravel's filesystem configuration file is located at `config/filesystems.php`. Within this file, you may configure all of your filesystem "disks". Each disk represents a particular storage driver and storage location. Example configurations for each supported driver are included in the configuration file so you can modify the configuration to reflect your storage preferences and credentials. -->
Laravel의 파일 시스템 설정 파일은 `config/filesystems.php`에 위치해 있습니다. 이 파일 안에서 모든 파일 시스템 "디스크"를 설정할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 저장 위치를 의미합니다. 구성 파일에는 지원되는 각 드라이버의 예시 설정이 포함되어 있어, 원하는 저장소 환경과 자격 증명에 맞게 쉽게 수정할 수 있습니다.

<!-- The `local` driver interacts with files stored locally on the server running the Laravel application, while the `sftp` storage driver is used for SSH key-based FTP. The `s3` driver is used to write to Amazon's S3 cloud storage service. -->
`local` 드라이버는 Laravel 애플리케이션이 실행 중인 서버에 저장된 파일과 직접 상호작용하며, `sftp` 드라이버는 SSH 키 기반의 FTP에 사용됩니다. `s3` 드라이버는 Amazon의 S3 클라우드 스토리지 서비스를 이용할 때 사용됩니다.

> [!NOTE]
> 원하는 만큼 다양한 디스크를 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크를 동시에 구성하는 것도 가능합니다.

<a name="the-local-driver"></a>
<!-- ### The Local Driver -->
### The Local Driver

<!-- When using the `local` driver, all file operations are relative to the `root` directory defined in your `filesystems` configuration file. By default, this value is set to the `storage/app/private` directory. Therefore, the following method would write to `storage/app/private/example.txt`: -->
`local` 드라이버를 사용할 경우, 모든 파일 작업 경로는 `filesystems` 설정 파일에 정의된 `root` 디렉터리를 기준으로 합니다. 기본적으로 이 값은 `storage/app/private` 디렉터리로 설정되어 있습니다. 따라서 다음 메서드는 `storage/app/private/example.txt`에 내용을 저장합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
<!-- ### The Public Disk -->
### The Public Disk

<!-- The `public` disk included in your application's `filesystems` configuration file is intended for files that are going to be publicly accessible. By default, the `public` disk uses the `local` driver and stores its files in `storage/app/public`. -->
애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 웹에서 공개적으로 접근 가능한 파일을 위해 제공됩니다. 기본적으로, `public` 디스크는 `local` 드라이버를 사용하며, 파일은 `storage/app/public`에 저장됩니다.

<!-- If your `public` disk uses the `local` driver and you want to make these files accessible from the web, you should create a symbolic link from source directory `storage/app/public` to target directory `public/storage`: -->
만약 `public` 디스크가 `local` 드라이버를 사용하고 있고, 이 파일들을 웹에서 접근 가능하게 하려면 소스 디렉터리 `storage/app/public`에서 대상 디렉터리 `public/storage`로 심볼릭 링크를 생성해야 합니다.

<!-- To create the symbolic link, you may use the `storage:link` Artisan command: -->
심볼릭 링크를 생성하려면 다음과 같이 `storage:link` Artisan 명령어를 사용하면 됩니다:

```shell
php artisan storage:link
```

<!-- Once a file has been stored and the symbolic link has been created, you can create a URL to the files using the `asset` helper: -->
파일이 저장되고 심볼릭 링크가 생성되면, `asset` 헬퍼를 이용해 해당 파일의 URL을 만들 수 있습니다:

```php
echo asset('storage/file.txt');
```

<!-- You may configure additional symbolic links in your `filesystems` configuration file. Each of the configured links will be created when you run the `storage:link` command: -->
`filesystems` 설정 파일에서 추가적인 심볼릭 링크를 구성할 수도 있습니다. 이 파일에 설정된 링크들은 `storage:link` 명령어 실행 시 모두 생성됩니다:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

<!-- The `storage:unlink` command may be used to destroy your configured symbolic links: -->
`storage:unlink` 명령어를 사용하여 설정된 심볼릭 링크를 제거할 수도 있습니다:

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="s3-driver-configuration"></a>
<!-- #### S3 Driver Configuration -->
#### S3 Driver Configuration

<!-- Before using the S3 driver, you will need to install the Flysystem S3 package via the Composer package manager: -->
S3 드라이버를 사용하기 전에 Composer 패키지 매니저로 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

<!-- An S3 disk configuration array is located in your `config/filesystems.php` configuration file. Typically, you should configure your S3 information and credentials using the following environment variables which are referenced by the `config/filesystems.php` configuration file: -->
S3 디스크 설정 배열은 `config/filesystems.php`에 있습니다. 일반적으로, 다음과 같은 환경 변수를 이용해 S3 관련 정보와 자격 증명을 입력합니다. 이 변수들은 `config/filesystems.php`에서 참조합니다:

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

<!-- For convenience, these environment variables match the naming convention used by the AWS CLI. -->
편의를 위해, 이 환경 변수들은 AWS CLI에서 사용하는 네이밍 규칙과 일치합니다.

<a name="ftp-driver-configuration"></a>
<!-- #### FTP Driver Configuration -->
#### FTP Driver Configuration

<!-- Before using the FTP driver, you will need to install the Flysystem FTP package via the Composer package manager: -->
FTP 드라이버를 사용하기 전에, Composer 패키지 매니저로 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```

<!-- Laravel's Flysystem integrations work great with FTP; however, a sample configuration is not included with the framework's default `config/filesystems.php` configuration file. If you need to configure an FTP filesystem, you may use the configuration example below: -->
Laravel의 Flysystem 통합 기능은 FTP와도 훌륭하게 동작합니다. 하지만, 프레임워크의 기본 `config/filesystems.php`에는 샘플 설정이 포함되어 있지 않습니다. FTP 파일 시스템을 설정해야 할 경우 아래 예시를 참고하세요:

```php
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
SFTP 드라이버를 사용하기 전에, Composer 패키지 매니저로 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

<!-- Laravel's Flysystem integrations work great with SFTP; however, a sample configuration is not included with the framework's default `config/filesystems.php` configuration file. If you need to configure an SFTP filesystem, you may use the configuration example below: -->
Laravel의 Flysystem 통합 기능은 SFTP에서도 잘 동작하지만, 프레임워크의 기본 `config/filesystems.php`에는 샘플 설정이 포함되어 있지 않습니다. SFTP 파일 시스템을 설정해야 할 경우 아래 예시를 참고하세요:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // Settings for basic authentication...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // Settings for SSH key-based authentication with encryption password...
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
```

<a name="scoped-and-read-only-filesystems"></a>
<!-- ### Scoped and Read-Only Filesystems -->
### Scoped and Read-Only Filesystems

<!-- Scoped disks allow you to define a filesystem where all paths are automatically prefixed with a given path prefix. Before creating a scoped filesystem disk, you will need to install an additional Flysystem package via the Composer package manager: -->
스코프 디스크는 파일 시스템 내의 모든 경로가 자동으로 지정된 경로 접두사로 시작하도록 설정할 수 있습니다. 스코프 파일 시스템 디스크를 만들기 전에 Composer 패키지 매니저로 추가적인 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

<!-- You may create a path scoped instance of any existing filesystem disk by defining a disk that utilizes the `scoped` driver. For example, you may create a disk which scopes your existing `s3` disk to a specific path prefix, and then every file operation using your scoped disk will utilize the specified prefix: -->
기존 파일 시스템 디스크에 대해 `scoped` 드라이버를 사용하여 경로 스코프 인스턴스를 만들 수 있습니다. 예를 들어, 기존 `s3` 디스크를 특정 경로 접두사로 스코프화하면, 해당 스코프 디스크를 통해 이루어지는 모든 파일 작업에 지정된 접두사가 자동으로 적용됩니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

<!-- "Read-only" disks allow you to create filesystem disks that do not allow write operations. Before using the `read-only` configuration option, you will need to install an additional Flysystem package via the Composer package manager: -->
"읽기 전용(read-only)" 디스크는 쓰기 작업이 허용되지 않는 파일 시스템 디스크를 만드는데 사용할 수 있습니다. `read-only` 옵션을 사용하기 전에, 아래와 같이 추가적인 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```

<!-- Next, you may include the `read-only` configuration option in one or more of your disk's configuration arrays: -->
그 다음, 디스크 설정 배열에 `read-only` 옵션을 추가할 수 있습니다:

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

<!-- By default, your application's `filesystems` configuration file contains a disk configuration for the `s3` disk. In addition to using this disk to interact with [Amazon S3](https://aws.amazon.com/s3/), you may use it to interact with any S3-compatible file storage service such as [RustFS](https://github.com/rustfs/rustfs), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), or [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/). -->
기본적으로, 애플리케이션의 `filesystems` 설정 파일에는 `s3` 디스크에 대한 설정이 포함되어 있습니다. 이 디스크를 통해 [Amazon S3](https://aws.amazon.com/s3/) 뿐만 아니라, [RustFS](https://github.com/rustfs/rustfs), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/) 등 다양한 S3 호환 파일 저장 서비스와도 연동할 수 있습니다.

<!-- Typically, after updating the disk's credentials to match the credentials of the service you are planning to use, you only need to update the value of the `endpoint` configuration option. This option's value is typically defined via the `AWS_ENDPOINT` environment variable: -->
대체로, 사용하려는 서비스의 자격 증명에 맞게 디스크 설정을 변경한 후, `endpoint` 설정 값을 해당 서비스에 맞게 업데이트하면 됩니다. 이 설정 값은 주로 `AWS_ENDPOINT` 환경 변수로 정의됩니다:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://rustfs:9000'),
```

<a name="obtaining-disk-instances"></a>
<!-- ## Obtaining Disk Instances -->
## Obtaining Disk Instances

<!-- The `Storage` facade may be used to interact with any of your configured disks. For example, you may use the `put` method on the facade to store an avatar on the default disk. If you call methods on the `Storage` facade without first calling the `disk` method, the method will automatically be passed to the default disk: -->
`Storage` 파사드를 사용해 설정된 모든 디스크와 상호작용할 수 있습니다. 예를 들어, 파사드의 `put` 메서드를 사용해 기본 디스크에 아바타 이미지를 저장할 수 있습니다. `Storage` 파사드에서 `disk` 메서드를 먼저 호출하지 않으면, 호출된 메서드는 자동으로 기본 디스크에서 실행됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

<!-- If your application interacts with multiple disks, you may use the `disk` method on the `Storage` facade to work with files on a particular disk: -->
만약 여러 개의 디스크를 사용하는 경우, `Storage` 파사드에서 `disk` 메서드를 사용해 특정 디스크에 파일을 저장하거나 불러올 수 있습니다:

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
<!-- ### On-Demand Disks -->
### On-Demand Disks

<!-- Sometimes you may wish to create a disk at runtime using a given configuration without that configuration actually being present in your application's `filesystems` configuration file. To accomplish this, you may pass a configuration array to the `Storage` facade's `build` method: -->
때로는 애플리케이션의 `filesystems` 설정 파일에 미리 정의하지 않은 구성을 사용해 런타임에 디스크를 생성하고 싶을 수 있습니다. 이때는 `Storage` 파사드의 `build` 메서드에 설정 배열을 전달해 온디맨드로 디스크를 만들 수 있습니다:

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
`get` 메서드는 파일의 내용을 문자열로 반환합니다. 모든 파일 경로는 디스크의 "root" 위치를 기준으로 상대 경로로 지정해야 합니다:

```php
$contents = Storage::get('file.jpg');
```

<!-- If the file you are retrieving contains JSON, you may use the `json` method to retrieve the file and decode its contents: -->
만약 가져오는 파일이 JSON이면, `json` 메서드를 사용해 파일을 읽고 디코딩할 수 있습니다:

```php
$orders = Storage::json('orders.json');
```

<!-- The `exists` method may be used to determine if a file exists on the disk: -->
`exists` 메서드는 디스크에 지정된 파일이 존재하는지 확인합니다:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

<!-- The `missing` method may be used to determine if a file is missing from the disk: -->
`missing` 메서드는 지정한 파일이 디스크에 없는지 확인합니다:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
<!-- ### Downloading Files -->
### Downloading Files

<!-- The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method: -->
`download` 메서드는 사용자의 브라우저가 지정한 경로의 파일을 강제로 다운로드하도록 응답을 생성합니다. `download` 메서드는 두 번째 인수로 파일 이름을 받으며, 이 이름이 사용자에게 보이는 다운로드 파일명으로 적용됩니다. 마지막으로, 세 번째 인수로 HTTP 헤더 배열도 전달할 수 있습니다:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
<!-- ### File URLs -->
### File URLs

<!-- You may use the `url` method to get the URL for a given file. If you are using the `local` driver, this will typically just prepend `/storage` to the given path and return a relative URL to the file. If you are using the `s3` driver, the fully qualified remote URL will be returned: -->
`url` 메서드를 이용해 특정 파일의 URL을 얻을 수 있습니다. `local` 드라이버를 사용할 경우, 이 메서드는 일반적으로 지정된 경로에 `/storage`를 앞에 붙여 상대 URL을 반환합니다. `s3` 드라이버를 쓰는 경우에는 완전히 실제 원격 URL이 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

<!-- When using the `local` driver, all files that should be publicly accessible should be placed in the `storage/app/public` directory. Furthermore, you should [create a symbolic link](#the-public-disk) at `public/storage` which points to the `storage/app/public` directory. -->
`local` 드라이버를 쓸 때는 공개적으로 접근 가능한 모든 파일이 `storage/app/public` 디렉터리에 있어야 합니다. 또한, `storage/app/public` 디렉터리를 가리키는 [create a symbolic link](#the-public-disk)를 `public/storage`에 생성해야 합니다.

> [!WARNING]
> `local` 드라이버를 사용할 때 `url` 메서드의 반환값은 URL 인코딩되지 않습니다. 그러므로, 파일 이름은 항상 유효한 URL을 생성할 수 있도록 작성하는 것이 좋습니다.

<a name="url-host-customization"></a>
<!-- #### URL Host Customization -->
#### URL Host Customization

<!-- If you would like to modify the host for URLs generated using the `Storage` facade, you may add or change the `url` option in the disk's configuration array: -->
`Storage` 파사드를 통해 생성되는 URL의 호스트를 수정하고 싶다면, 디스크의 설정 배열에 `url` 옵션을 추가하거나 변경할 수 있습니다:

```php
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
    'throw' => false,
],
```

<a name="temporary-urls"></a>
<!-- ### Temporary URLs -->
### Temporary URLs

<!-- Using the `temporaryUrl` method, you may create temporary URLs to files stored using the `local` and `s3` drivers. This method accepts a path and a `DateTime` instance specifying when the URL should expire: -->
`temporaryUrl` 메서드를 사용해 `local` 또는 `s3` 드라이버로 저장된 파일의 임시 접근 URL을 생성할 수 있습니다. 이 메서드는 경로와 URL의 만료 시간을 `DateTime` 인스턴스로 받습니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

<a name="enabling-local-temporary-urls"></a>
<!-- #### Enabling Local Temporary URLs -->
#### Enabling Local Temporary URLs

<!-- If you started developing your application before support for temporary URLs was introduced to the `local` driver, you may need to enable local temporary URLs. To do so, add the `serve` option to your `local` disk's configuration array within the `config/filesystems.php` configuration file: -->
애플리케이션을 `local` 드라이버의 임시 URL 지원이 도입되기 전에 만들었다면, 임시 URL을 별도로 활성화해야 할 수 있습니다. 활성화하려면 `config/filesystems.php`의 `local` 디스크 설정 배열에 `serve` 옵션을 추가하세요:

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app/private'),
    'serve' => true, // [tl! add]
    'throw' => false,
],
```

<a name="s3-request-parameters"></a>
<!-- #### S3 Request Parameters -->
#### S3 Request Parameters

<!-- If you need to specify additional [S3 request parameters](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests), you may pass the array of request parameters as the third argument to the `temporaryUrl` method: -->
추가적인 [S3 request parameters](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)가 필요하다면, `temporaryUrl` 메서드의 세 번째 인수로 배열을 전달할 수 있습니다:

```php
$url = Storage::temporaryUrl(
    'file.jpg',
    now()->plus(minutes: 5),
    [
        'ResponseContentType' => 'application/octet-stream',
        'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
    ]
);
```

<a name="customizing-temporary-urls"></a>
<!-- #### Customizing Temporary URLs -->
#### Customizing Temporary URLs

<!-- If you need to customize how temporary URLs are created for a specific storage disk, you can use the `buildTemporaryUrlsUsing` method. For example, this can be useful if you have a controller that allows you to download files stored via a disk that doesn't typically support temporary URLs. Usually, this method should be called from the `boot` method of a service provider: -->
특정 스토리지 디스크에 대해 임시 URL 생성 방식을 사용자 지정하고 싶다면, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 일반적으로 임시 URL을 지원하지 않는 디스크에 저장된 파일을 서명된 라우트를 통해 다운로드하는 컨트롤러가 있다고 가정할 수 있습니다. 이 메서드는 일반적으로 서비스 프로바이더의 `boot` 메서드에서 호출하는 것이 좋습니다:

```php
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
```

<a name="temporary-upload-urls"></a>
<!-- #### Temporary Upload URLs -->
#### Temporary Upload URLs

> [!WARNING]
> 임시 업로드 URL 생성 기능은 `s3`와 `local` 드라이버만 지원됩니다.

<!-- If you need to generate a temporary URL that can be used to upload a file directly from your client-side application, you may use the `temporaryUploadUrl` method. This method accepts a path and a `DateTime` instance specifying when the URL should expire. The `temporaryUploadUrl` method returns an associative array which may be destructured into the upload URL and the headers that should be included with the upload request: -->
클라이언트(브라우저 등)에서 파일을 직접 업로드할 수 있는 임시 URL이 필요하다면 `temporaryUploadUrl` 메서드를 사용하세요. 이 메서드는 경로와 URL이 만료될 시점을 지정하는 `DateTime` 인스턴스를 받습니다. `temporaryUploadUrl` 메서드는 업로드 URL과 업로드 요청에 포함해야 하는 헤더로 구조 분해할 수 있는 연관 배열을 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

<!-- This method is primarily useful in serverless environments that require the client-side application to directly upload files to a cloud storage system such as Amazon S3. -->
이 메서드는 주로 클라우드 스토리지 시스템(예: Amazon S3)으로 클라이언트에서 직접 파일을 업로드해야 하는 서버리스 환경에서 유용하게 사용됩니다.

<a name="file-metadata"></a>
<!-- ### File Metadata -->
### File Metadata

<!-- In addition to reading and writing files, Laravel can also provide information about the files themselves. For example, the `size` method may be used to get the size of a file in bytes: -->
파일의 읽기/쓰기 외에도, Laravel은 파일 자체의 정보를 제공할 수 있습니다. 예를 들어, `size` 메서드를 사용해 파일의 바이트 크기를 얻을 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

<!-- The `lastModified` method returns the UNIX timestamp of the last time the file was modified: -->
`lastModified` 메서드는 파일이 마지막으로 수정된 시간을 UNIX 타임스탬프로 반환합니다:

```php
$time = Storage::lastModified('file.jpg');
```

<!-- The MIME type of a given file may be obtained via the `mimeType` method: -->
지정한 파일의 MIME 타입은 `mimeType` 메서드로 얻을 수 있습니다:

```php
$mime = Storage::mimeType('file.jpg');
```

<a name="file-paths"></a>
<!-- #### File Paths -->
#### File Paths

<!-- You may use the `path` method to get the path for a given file. If you are using the `local` driver, this will return the absolute path to the file. If you are using the `s3` driver, this method will return the relative path to the file in the S3 bucket: -->
특정 파일의 실제 경로를 얻고 싶다면 `path` 메서드를 쓰세요. `local` 드라이버의 경우, 이 메서드는 파일의 절대 경로를 반환합니다. `s3` 드라이버의 경우 S3 버킷 내의 상대 경로가 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
<!-- ## Storing Files -->
## Storing Files

<!-- The `put` method may be used to store file contents on a disk. You may also pass a PHP `resource` to the `put` method, which will use Flysystem's underlying stream support. Remember, all file paths should be specified relative to the "root" location configured for the disk: -->
`put` 메서드를 사용해 파일 내용을 디스크에 저장할 수 있습니다. `put` 메서드는 PHP의 `resource`도 인수로 받아, Flysystem의 스트림 기능을 사용할 수 있습니다. 모든 파일 경로는 디스크의 "root" 위치를 기준으로 지정해야 합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="failed-writes"></a>
<!-- #### Failed Writes -->
#### Failed Writes

<!-- If the `put` method (or other "write" operations) is unable to write the file to disk, `false` will be returned: -->
만약 `put` 메서드(혹은 다른 "쓰기" 작업)가 파일을 디스크에 저장하지 못하면, `false`를 반환합니다:

```php
if (! Storage::put('file.jpg', $contents)) {
    // The file could not be written to disk...
}
```

<!-- If you wish, you may define the `throw` option within your filesystem disk's configuration array. When this option is defined as `true`, "write" methods such as `put` will throw an instance of `League\Flysystem\UnableToWriteFile` when write operations fail: -->
원한다면, 파일 시스템 디스크 설정 배열에 `throw` 옵션을 추가할 수 있습니다. 이 옵셥이 `true`로 설정된 경우, `put`와 같은 "쓰기" 메서드가 실패하면 `League\Flysystem\UnableToWriteFile` 예외가 발생합니다:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<a name="prepending-appending-to-files"></a>
<!-- ### Prepending and Appending To Files -->
### Prepending and Appending To Files

<!-- The `prepend` and `append` methods allow you to write to the beginning or end of a file: -->
`prepend` 및 `append` 메서드를 사용해 파일 앞이나 뒤에 내용을 추가할 수 있습니다:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
<!-- ### Copying and Moving Files -->
### Copying and Moving Files

<!-- The `copy` method may be used to copy an existing file to a new location on the disk, while the `move` method may be used to rename or move an existing file to a new location: -->
`copy` 메서드는 기존 파일을 디스크 내의 새로운 위치로 복사합니다. `move` 메서드는 파일을 새 위치로 이동하거나 이름을 변경할 때 사용합니다:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="automatic-streaming"></a>
<!-- ### Automatic Streaming -->
### Automatic Streaming

<!-- Streaming files to storage offers significantly reduced memory usage. If you would like Laravel to automatically manage streaming a given file to your storage location, you may use the `putFile` or `putFileAs` method. This method accepts either an `Illuminate\Http\File` or `Illuminate\Http\UploadedFile` instance and will automatically stream the file to your desired location: -->
파일을 저장할 때 스트리밍 방식을 쓰면 메모리 사용량이 크게 줄어듭니다. Laravel이 파일을 자동으로 스트리밍해 저장하길 원한다면, `putFile` 또는 `putFileAs` 메서드를 사용하세요. 이 메서드는 `Illuminate\Http\File`이나 `Illuminate\Http\UploadedFile` 인스턴스를 받아 원하는 위치에 파일을 스트리밍합니다:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// Automatically generate a unique ID for filename...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// Manually specify a filename...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

<!-- There are a few important things to note about the `putFile` method. Note that we only specified a directory name and not a filename. By default, the `putFile` method will generate a unique ID to serve as the filename. The file's extension will be determined by examining the file's MIME type. The path to the file will be returned by the `putFile` method so you can store the path, including the generated filename, in your database. -->
`putFile` 메서드에서 주의할 점이 몇 가지 있습니다. 여기서는 디렉터리명만 지정하고 파일명은 지정하지 않았습니다. 기본적으로 `putFile` 메서드는 고유한 ID를 파일명으로 자동 생성합니다. 파일의 확장자는 MIME 타입을 참고해 정해집니다. `putFile` 메서드는 파일 경로(자동 생성된 파일명 포함)를 반환하므로, 데이터베이스에 저장할 수 있습니다.

<!-- The `putFile` and `putFileAs` methods also accept an argument to specify the "visibility" of the stored file. This is particularly useful if you are storing the file on a cloud disk such as Amazon S3 and would like the file to be publicly accessible via generated URLs: -->
또한, `putFile` 및 `putFileAs`는 저장 파일의 "visibility" 인수를 받을 수 있습니다. 이 기능은 Amazon S3와 같은 클라우드 디스크에 파일을 저장하면서 URL을 통해 공개적으로 접근할 수 있도록 할 때 유용합니다:

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="file-uploads"></a>
<!-- ### File Uploads -->
### File Uploads

<!-- In web applications, one of the most common use-cases for storing files is storing user uploaded files such as photos and documents. Laravel makes it very easy to store uploaded files using the `store` method on an uploaded file instance. Call the `store` method with the path at which you wish to store the uploaded file: -->
웹 애플리케이션에서 파일 저장의 가장 흔한 사용 사례 중 하나는 사용자가 업로드하는 사진이나 문서 같은 파일입니다. Laravel에서는 업로드된 파일 인스턴스의 `store` 메서드를 이용해 손쉽게 파일을 저장할 수 있습니다. 파일을 저장할 경로를 지정해 `store` 메서드를 호출하세요:

```php
<?php

namespace App\Http\Controllers;

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
```

<!-- There are a few important things to note about this example. Note that we only specified a directory name, not a filename. By default, the `store` method will generate a unique ID to serve as the filename. The file's extension will be determined by examining the file's MIME type. The path to the file will be returned by the `store` method so you can store the path, including the generated filename, in your database. -->
이 예제에서 주의할 점이 몇 가지 있습니다. 여기서는 디렉터리명만 지정하고 파일명은 명시하지 않았습니다. 기본적으로 `store` 메서드는 고유한 ID를 파일명으로 자동 생성합니다. 파일 확장자는 MIME 타입을 참고해 정해집니다. `store` 메서드는 파일 경로(자동 생성된 파일명 포함)를 반환하므로, 데이터베이스에 저장할 수 있습니다.

<!-- You may also call the `putFile` method on the `Storage` facade to perform the same file storage operation as the example above: -->
동일한 작업은 `Storage` 파사드의 `putFile` 메서드로도 할 수 있습니다:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
<!-- #### Specifying a File Name -->
#### Specifying a File Name

<!-- If you do not want a filename to be automatically assigned to your stored file, you may use the `storeAs` method, which receives the path, the filename, and the (optional) disk as its arguments: -->
저장되는 파일의 파일명을 자동으로 할당하지 않고 싶다면, `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 경로, 파일명, (선택적) 디스크 이름을 인수로 받습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

<!-- You may also use the `putFileAs` method on the `Storage` facade, which will perform the same file storage operation as the example above: -->
위 작업은 `Storage` 파사드의 `putFileAs` 메서드를 사용해서도 동일하게 구현할 수 있습니다:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!WARNING]
> 출력이 불가능하거나, 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 Laravel의 파일 저장 메서드에 경로를 전달하기 전에 파일 경로를 정제(sanitize)하는 것이 좋습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드를 통해 정규화됩니다.

<a name="specifying-a-disk"></a>
<!-- #### Specifying a Disk -->
#### Specifying a Disk

<!-- By default, this uploaded file's `store` method will use your default disk. If you would like to specify another disk, pass the disk name as the second argument to the `store` method: -->
기본적으로 업로드된 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 사용하고 싶다면 `store` 메서드의 두 번째 인수로 디스크 이름을 전달하세요:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

<!-- If you are using the `storeAs` method, you may pass the disk name as the third argument to the method: -->
`storeAs` 메서드를 사용하는 경우, 디스크 이름을 세 번째 인수로 넘기면 됩니다:

```php
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
업로드된 파일의 원래 이름과 확장자가 필요하다면, `getClientOriginalName`, `getClientOriginalExtension` 메서드를 사용할 수 있습니다:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

<!-- However, keep in mind that the `getClientOriginalName` and `getClientOriginalExtension` methods are considered unsafe, as the file name and extension may be tampered with by a malicious user. For this reason, you should typically prefer the `hashName` and `extension` methods to get a name and an extension for the given file upload: -->
하지만, `getClientOriginalName`과 `getClientOriginalExtension` 메서드는 악의적인 사용자가 파일 이름과 확장자를 조작할 수 있으므로 안전하지 않다는 점에 유의하세요. 따라서 일반적으로는 `hashName`과 `extension` 메서드를 사용해 업로드 파일의 이름과 확장자를 얻는 편이 좋습니다:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // Generate a unique, random name...
$extension = $file->extension(); // Determine the file's extension based on the file's MIME type...
```

<a name="file-visibility"></a>
<!-- ### File Visibility -->
### File Visibility

<!-- In Laravel's Flysystem integration, "visibility" is an abstraction of file permissions across multiple platforms. Files may either be declared `public` or `private`. When a file is declared `public`, you are indicating that the file should generally be accessible to others. For example, when using the S3 driver, you may retrieve URLs for `public` files. -->
Laravel의 Flysystem 통합에서 "visibility(공개 범위)"는 다양한 플랫폼 간 파일 권한의 추상 개념입니다. 파일은 `public`(공개) 또는 `private`(비공개)로 지정할 수 있습니다. 파일을 `public`으로 지정하면, 누군가(주로 웹 사용자가) 해당 파일에 접근할 수 있음을 나타냅니다. 예를 들어, S3 드라이버를 사용할 때 `public` 파일의 URL을 얻는 것이 가능합니다.

<!-- You can set the visibility when writing the file via the `put` method: -->
파일 저장 시 `put` 메서드로 visibility를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

<!-- If the file has already been stored, its visibility can be retrieved and set via the `getVisibility` and `setVisibility` methods: -->
이미 저장된 파일의 visibility 정보는 `getVisibility`로, 설정은 `setVisibility`로 할 수 있습니다:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

<!-- When interacting with uploaded files, you may use the `storePublicly` and `storePubliclyAs` methods to store the uploaded file with `public` visibility: -->
업로드 파일과 상호작용할 때는, 업로드 파일의 `storePublicly` 및 `storePubliclyAs` 메서드를 사용해 `public`으로 저장할 수 있습니다:

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a name="image-manipulation"></a>
<!-- ### Image Manipulation -->
### Image Manipulation

<!-- If you need to resize, crop, or convert an uploaded image before storing it, you may use Laravel's [image manipulation features](/docs/13.x/images): -->
업로드한 이미지를 저장하기 전에 크기를 조정하거나 자르거나 형식을 변환해야 한다면 Laravel의 [image manipulation features](/docs/13.x/images)를 사용할 수 있습니다.

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->toWebp()
    ->storePublicly('avatars', 'public');
```

<!-- You may also create an image instance from a file already stored on one of your filesystem disks: -->
파일 시스템 디스크 중 하나에 이미 저장된 파일에서 이미지 인스턴스를 생성할 수도 있습니다.

```php
$image = Storage::disk('public')->image('avatars/photo.jpg');
```

<a name="local-files-and-visibility"></a>
<!-- #### Local Files and Visibility -->
#### Local Files and Visibility

<!-- When using the `local` driver, `public` [visibility](#file-visibility) translates to `0755` permissions for directories and `0644` permissions for files. You can modify the permissions mappings in your application's `filesystems` configuration file: -->
`local` 드라이버를 사용할 때, `public` [visibility](#file-visibility)는 디렉터리 `0755`, 파일 `0644`의 권한으로 설정됩니다. 이 권한 매핑은 애플리케이션의 `filesystems` 설정 파일에서 직접 수정할 수 있습니다:

```php
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
    'throw' => false,
],
```

<a name="deleting-files"></a>
<!-- ## Deleting Files -->
## Deleting Files

<!-- The `delete` method accepts a single filename or an array of files to delete: -->
`delete` 메서드는 하나의 파일명 또는 파일명 배열로 파일을 삭제할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

<!-- If necessary, you may specify the disk that the file should be deleted from: -->
필요하다면, 파일이 삭제될 디스크를 지정할 수도 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a name="directories"></a>
<!-- ## Directories -->
## Directories

<a name="get-all-files-within-a-directory"></a>
<!-- #### Get All Files Within a Directory -->
#### Get All Files Within a Directory

<!-- The `files` method returns an array of all files within a given directory. If you would like to retrieve a list of all files within a given directory including subdirectories, you may use the `allFiles` method: -->
`files` 메서드는 지정한 디렉터리 내의 모든 파일을 배열로 반환합니다. 하위 디렉터리까지 포함한 모든 파일 리스트를 얻고 싶다면 `allFiles` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
<!-- #### Get All Directories Within a Directory -->
#### Get All Directories Within a Directory

<!-- The `directories` method returns an array of all directories within a given directory. If you would like to retrieve a list of all directories within a given directory including subdirectories, you may use the `allDirectories` method: -->
`directories` 메서드는 지정한 디렉터리 내의 모든 하위 디렉터리 경로 배열을 반환합니다. 하위 디렉터리까지 포함한 전체 리스트를 얻으려면 `allDirectories`를 사용하세요:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
<!-- #### Create a Directory -->
#### Create a Directory

<!-- The `makeDirectory` method will create the given directory, including any needed subdirectories: -->
`makeDirectory` 메서드는 지정한 경로의 디렉터리(필요한 하위 디렉터리 포함)를 생성합니다:

```php
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
<!-- #### Delete a Directory -->
#### Delete a Directory

<!-- Finally, the `deleteDirectory` method may be used to remove a directory and all of its files: -->
`deleteDirectory` 메서드는 지정한 디렉터리와 그 안의 모든 파일을 삭제합니다:

```php
Storage::deleteDirectory($directory);
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- The `Storage` facade's `fake` method allows you to easily generate a fake disk that, combined with the file generation utilities of the `Illuminate\Http\UploadedFile` class, greatly simplifies the testing of file uploads. For example: -->
`Storage` 파사드의 `fake` 메서드를 사용하면, 임의의 디스크를 쉽게 생성해 파일 업로드 테스트를 단순화할 수 있습니다. 이는 `Illuminate\Http\UploadedFile` 클래스의 파일 생성 기능과 함께 쓰이는데 매우 유용합니다. 예를 들어:

```php tab=Pest
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('albums can be uploaded', function () {
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

    // Assert that the number of files in a given directory matches the expected count...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // Assert that a given directory is empty...
    Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');

    // Assert that the disk contains no files...
    Storage::disk('photos')->assertEmpty();
});
```

```php tab=PHPUnit
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

        // Assert that the number of files in a given directory matches the expected count...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // Assert that a given directory is empty...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');

        // Assert that the disk contains no files...
        Storage::disk('photos')->assertEmpty();
    }
}
```

<!-- By default, the `fake` method will delete all files in its temporary directory. If you would like to keep these files, you may use the "persistentFake" method instead. For more information on testing file uploads, you may consult the [HTTP testing documentation's information on file uploads](/docs/13.x/http-tests#testing-file-uploads). -->
기본적으로 `fake` 메서드는 임시 디렉터리 내의 모든 파일을 삭제합니다. 만약 임시 파일을 유지하고 싶다면 "persistentFake" 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 대한 더 자세한 내용은 [HTTP testing documentation's information on file uploads](/docs/13.x/http-tests#testing-file-uploads)을 참고하세요.

> [!WARNING]
> `image` 메서드는 [GD extension](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="custom-filesystems"></a>
<!-- ## Custom Filesystems -->
## Custom Filesystems

<!-- Laravel's Flysystem integration provides support for several "drivers" out of the box; however, Flysystem is not limited to these and has adapters for many other storage systems. You can create a custom driver if you want to use one of these additional adapters in your Laravel application. -->
Laravel의 Flysystem 통합은 기본적으로 여러 개의 "드라이버"를 지원하지만, Flysystem은 이 외에도 다양한 스토리지 시스템용 어댑터를 제공합니다. Laravel 애플리케이션에서 추가 어댑터를 쓰고 싶을 때는 커스텀 드라이버를 직접 만들 수 있습니다.

<!-- In order to define a custom filesystem you will need a Flysystem adapter. Let's add a community maintained Dropbox adapter to our project: -->
커스텀 파일 시스템을 만들려면 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티에서 유지 관리되는 Dropbox 어댑터를 프로젝트에 추가해보겠습니다:

```shell
composer require spatie/flysystem-dropbox
```

<!-- Next, you can register the driver within the `boot` method of one of your application's [service providers](/docs/13.x/providers). To accomplish this, you should use the `extend` method of the `Storage` facade: -->
그 다음, 애플리케이션의 [service providers](/docs/13.x/providers) 중 하나의 `boot` 메서드에서 드라이버를 등록할 수 있습니다. 이를 위해 `Storage` 파사드의 `extend` 메서드를 사용하세요:

```php
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
```

<!-- The first argument of the `extend` method is the name of the driver and the second is a closure that receives the `$app` and `$config` variables. The closure must return an instance of `Illuminate\Filesystem\FilesystemAdapter`. The `$config` variable contains the values defined in `config/filesystems.php` for the specified disk. -->
`extend` 메서드의 첫 번째 인수는 드라이버 이름이며, 두 번째 인수는 `$app`과 `$config` 변수를 인수로 받는 클로저입니다. 클로저는 반드시 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 합니다. `$config`에는 지정한 디스크에 대해 `config/filesystems.php`에 정의된 값이 들어있습니다.

<!-- Once you have created and registered the extension's service provider, you may use the `dropbox` driver in your `config/filesystems.php` configuration file. -->
이제 확장 서비스 제공자를 만들고 등록했다면, `config/filesystems.php` 설정 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.
