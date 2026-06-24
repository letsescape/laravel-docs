<!-- # File Storage -->
# File Storage

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [The Local Driver](#the-local-driver)
    - [The Public Disk](#the-public-disk)
    - [Driver Prerequisites](#driver-prerequisites)
    - [Amazon S3 Compatible Filesystems](#amazon-s3-compatible-filesystems)
    - [Caching](#caching)
- [Obtaining Disk Instances](#obtaining-disk-instances)
    - [On-Demand Disks](#on-demand-disks)
- [Retrieving Files](#retrieving-files)
    - [Downloading Files](#downloading-files)
    - [File URLs](#file-urls)
    - [File Metadata](#file-metadata)
- [Storing Files](#storing-files)
    - [File Uploads](#file-uploads)
    - [File Visibility](#file-visibility)
- [Deleting Files](#deleting-files)
- [Directories](#directories)
- [Custom Filesystems](#custom-filesystems)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides a powerful filesystem abstraction thanks to the wonderful [Flysystem](https://github.com/thephpleague/flysystem) PHP package by Frank de Jonge. The Laravel Flysystem integration provides simple drivers for working with local filesystems, SFTP, and Amazon S3. Even better, it's amazingly simple to switch between these storage options between your local development machine and production server as the API remains the same for each system. -->
Laravel은 Frank de Jonge가 만든 훌륭한 [Flysystem](https://github.com/thephpleague/flysystem) PHP 패키지를 통해 강력한 파일 시스템 추상화를 제공합니다. Laravel의 Flysystem 통합 기능을 사용하면 로컬 파일 시스템, SFTP, Amazon S3 등 다양한 스토리지 시스템을 손쉽게 다룰 수 있습니다. 더 나아가, 각 스토리지 시스템의 API가 동일하게 유지되므로, 로컬 개발 환경과 운영 서버(프로덕션) 간에 스토리지 옵션을 손쉽게 전환할 수 있습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Laravel's filesystem configuration file is located at `config/filesystems.php`. Within this file, you may configure all of your filesystem "disks". Each disk represents a particular storage driver and storage location. Example configurations for each supported driver are included in the configuration file so you can modify the configuration to reflect your storage preferences and credentials. -->
Laravel의 파일 시스템 구성 파일은 `config/filesystems.php`에 위치해 있습니다. 이 파일에서 모든 파일 시스템 "디스크"를 설정할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 저장 위치를 의미합니다. 지원되는 각 드라이버의 예시 구성도 포함되어 있으므로, 이를 참고하여 자신의 저장소 환경과 인증 정보에 맞게 설정을 변경하시면 됩니다.

<!-- The `local` driver interacts with files stored locally on the server running the Laravel application while the `s3` driver is used to write to Amazon's S3 cloud storage service. -->
`local` 드라이버는 Laravel 애플리케이션이 실행 중인 서버의 로컬 파일을 다루는 데 사용하며, `s3` 드라이버는 Amazon의 S3 클라우드 스토리지 서비스에 파일을 쓰는 데 사용됩니다.

> [!TIP]
> 여러 개의 디스크를 원하는 만큼 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크도 생성할 수 있습니다.

<a name="the-local-driver"></a>
<!-- ### The Local Driver -->
### The Local Driver

<!-- When using the `local` driver, all file operations are relative to the `root` directory defined in your `filesystems` configuration file. By default, this value is set to the `storage/app` directory. Therefore, the following method would write to `storage/app/example.txt`: -->
`local` 드라이버를 사용할 때는, 모든 파일 작업이 `filesystems` 구성 파일에서 정의한 `root` 디렉터리 기준으로 상대 경로로 처리됩니다. 기본적으로 이 값은 `storage/app` 디렉터리로 설정되어 있습니다. 따라서, 아래 예시는 `storage/app/example.txt` 파일에 데이터를 기록합니다.

```
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
<!-- ### The Public Disk -->
### The Public Disk

<!-- The `public` disk included in your application's `filesystems` configuration file is intended for files that are going to be publicly accessible. By default, the `public` disk uses the `local` driver and stores its files in `storage/app/public`. -->
애플리케이션의 `filesystems` 구성 파일에 포함된 `public` 디스크는 일반적으로 외부에 공개할 파일을 저장하는 데 사용합니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며, 파일은 `storage/app/public` 디렉터리에 저장됩니다.

<!-- To make these files accessible from the web, you should create a symbolic link from `public/storage` to `storage/app/public`. Utilizing this folder convention will keep your publicly accessible files in one directory that can be easily shared across deployments when using zero down-time deployment systems like [Envoyer](https://envoyer.io). -->
이 파일들을 웹에서 접근할 수 있도록 하려면, `public/storage`에서 `storage/app/public`으로 연결되는 심볼릭 링크를 생성해야 합니다. 이러한 폴더 관리 방식을 사용하면, [Envoyer](https://envoyer.io)와 같은 무중단 배포 시스템을 사용하더라도 공개 파일을 한 디렉터리에서 깔끔하게 관리하고 쉽게 공유할 수 있습니다.

<!-- To create the symbolic link, you may use the `storage:link` Artisan command: -->
심볼릭 링크를 생성하려면, `storage:link` Artisan 명령어를 사용하면 됩니다.

```
php artisan storage:link
```

<!-- Once a file has been stored and the symbolic link has been created, you can create a URL to the files using the `asset` helper: -->
파일을 저장하고 심볼릭 링크를 생성한 후에는, `asset` 헬퍼를 사용해 해당 파일의 URL을 만들 수 있습니다.

```
echo asset('storage/file.txt');
```

<!-- You may configure additional symbolic links in your `filesystems` configuration file. Each of the configured links will be created when you run the `storage:link` command: -->
애플리케이션의 `filesystems` 구성 파일에서 추가 심볼릭 링크를 설정할 수도 있습니다. 설정된 각 링크는 `storage:link` 명령 실행 시 생성됩니다.

```
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="composer-packages"></a>
<!-- #### Composer Packages -->
#### Composer Packages

<!-- Before using the S3 or SFTP drivers, you will need to install the appropriate package via the Composer package manager: -->
S3 또는 SFTP 드라이버를 사용하기 전에는 Composer 패키지 매니저를 통해 해당 패키지를 설치해야 합니다.

<!--
- Amazon S3: `composer require --with-all-dependencies league/flysystem-aws-s3-v3 "^1.0"`
- SFTP: `composer require league/flysystem-sftp "~1.0"`
-->
- Amazon S3: `composer require --with-all-dependencies league/flysystem-aws-s3-v3 "^1.0"`
- SFTP: `composer require league/flysystem-sftp "~1.0"`

<!-- In addition, you may choose to install a cached adapter for increased performance: -->
또한, 퍼포먼스를 높이고 싶다면 캐시 어댑터를 추가로 설치할 수 있습니다.

<!-- - CachedAdapter: `composer require league/flysystem-cached-adapter "~1.0"` -->
- CachedAdapter: `composer require league/flysystem-cached-adapter "~1.0"`

<a name="s3-driver-configuration"></a>
<!-- #### S3 Driver Configuration -->
#### S3 Driver Configuration

<!-- The S3 driver configuration information is located in your `config/filesystems.php` configuration file. This file contains an example configuration array for an S3 driver. You are free to modify this array with your own S3 configuration and credentials. For convenience, these environment variables match the naming convention used by the AWS CLI. -->
S3 드라이버의 구성 정보는 `config/filesystems.php` 구성 파일에 있습니다. 이 파일에는 S3 드라이버를 위한 예시 배열이 포함되어 있으므로, 본인의 S3 설정값과 인증 정보에 맞게 자유롭게 수정할 수 있습니다. 참고로, 관련 환경 변수는 AWS CLI에서 사용되는 작명 규칙과 일치합니다.

<a name="ftp-driver-configuration"></a>
<!-- #### FTP Driver Configuration -->
#### FTP Driver Configuration

<!-- Laravel's Flysystem integrations work great with FTP; however, a sample configuration is not included with the framework's default `filesystems.php` configuration file. If you need to configure an FTP filesystem, you may use the configuration example below: -->
Laravel의 Flysystem 통합 기능은 FTP와도 잘 호환됩니다만, 프레임워크의 기본 `filesystems.php` 구성 파일에는 FTP 설정 예시가 포함되어 있지 않습니다. 만약 FTP 파일 시스템을 구성해야 한다면 아래 예시를 참고하세요.

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

<!-- Laravel's Flysystem integrations work great with SFTP; however, a sample configuration is not included with the framework's default `filesystems.php` configuration file. If you need to configure an SFTP filesystem, you may use the configuration example below: -->
마찬가지로, SFTP 드라이버도 Flysystem과 잘 호환되며, 기본 `filesystems.php` 구성 파일에는 SFTP 설정 예시가 포함되어 있지 않습니다. 아래 예시를 참고하여 SFTP 파일 시스템을 추가로 설정할 수 있습니다.

```
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // Settings for basic authentication...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // Settings for SSH key based authentication with encryption password...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'password' => env('SFTP_PASSWORD'),

    // Optional SFTP Settings...
    // 'port' => env('SFTP_PORT', 22),
    // 'root' => env('SFTP_ROOT'),
    // 'timeout' => 30,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
<!-- ### Amazon S3 Compatible Filesystems -->
### Amazon S3 Compatible Filesystems

<!-- By default, your application's `filesystems` configuration file contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as [MinIO](https://github.com/minio/minio) or [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/). -->
기본적으로, 애플리케이션의 `filesystems` 구성 파일에는 `s3` 디스크에 대한 설정이 들어 있습니다. Amazon S3뿐만 아니라, [MinIO](https://github.com/minio/minio)나 [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/)와 같은 S3 호환 파일 스토리지 서비스와도 연동이 가능합니다.

<!-- Typically, after updating the disk's credentials to match the credentials of the service you are planning to use, you only need to update the value of the `url` configuration option. This option's value is typically defined via the `AWS_ENDPOINT` environment variable: -->
일반적으로, 서비스에 맞는 자격증명으로 값들을 변경한 후에는 `url` 설정 값을 업데이트해야 합니다. 이 값은 보통 `AWS_ENDPOINT` 환경 변수로 정의됩니다.

```
'endpoint' => env('AWS_ENDPOINT', 'https://minio:9000'),
```

<a name="caching"></a>
<!-- ### Caching -->
### Caching

<!-- To enable caching for a given disk, you may add a `cache` directive to the disk's configuration options. The `cache` option should be an array of caching options containing the cache `store` name, the `expire` time in seconds, and the cache `prefix`: -->
특정 디스크에 캐싱을 활성화하려면, 디스크의 설정 옵션에 `cache` 지시어를 추가할 수 있습니다. `cache` 옵션은 캐시 `store` 이름, 만료 시간(`expire`, 초 단위), 캐시 `prefix` 등을 포함하는 배열이어야 합니다.

```
's3' => [
    'driver' => 's3',

    // Other Disk Options...

    'cache' => [
        'store' => 'memcached',
        'expire' => 600,
        'prefix' => 'cache-prefix',
    ],
],
```

<a name="obtaining-disk-instances"></a>
<!-- ## Obtaining Disk Instances -->
## Obtaining Disk Instances

<!-- The `Storage` facade may be used to interact with any of your configured disks. For example, you may use the `put` method on the facade to store an avatar on the default disk. If you call methods on the `Storage` facade without first calling the `disk` method, the method will automatically be passed to the default disk: -->
`Storage` 파사드를 사용해 구성된 모든 디스크와 상호작용할 수 있습니다. 예를 들어, 기본 디스크에 아바타를 저장하려면 파사드의 `put` 메서드를 사용할 수 있습니다. 만약 `disk` 메서드를 먼저 호출하지 않고 `Storage` 파사드에서 메서드를 호출하면, 메서드는 자동으로 기본 디스크를 사용합니다.

```
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

<!-- If your application interacts with multiple disks, you may use the `disk` method on the `Storage` facade to work with files on a particular disk: -->
여러 디스크를 다루는 경우에는, `Storage` 파사드의 `disk` 메서드로 특정 디스크를 지정해서 파일을 저장할 수도 있습니다.

```
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
<!-- ### On-Demand Disks -->
### On-Demand Disks

<!-- Sometimes you may wish to create a disk at runtime using a given configuration without that configuration actually being present in your application's `filesystems` configuration file. To accomplish this, you may pass a configuration array to the `Storage` facade's `build` method: -->
가끔 필요에 따라, 애플리케이션의 `filesystems` 구성 파일에는 없는 설정을 사용해 실행 중에 디스크를 생성하고 싶을 수 있습니다. 이럴 때는 `Storage` 파사드의 `build` 메서드에 설정 배열을 전달하면 됩니다.

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
`get` 메서드를 사용해 파일의 내용을 가져올 수 있습니다. 이 메서드는 파일의 원시 문자열 데이터를 반환합니다. 모든 파일 경로는 반드시 디스크의 "root" 위치를 기준으로 한 상대 경로여야 합니다.

```
$contents = Storage::get('file.jpg');
```

<!-- The `exists` method may be used to determine if a file exists on the disk: -->
`exists` 메서드를 사용하면, 디스크에 파일이 존재하는지 확인할 수 있습니다.

```
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

<!-- The `missing` method may be used to determine if a file is missing from the disk: -->
`missing` 메서드를 사용하면, 디스크에 파일이 없는지 확인할 수 있습니다.

```
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a name="downloading-files"></a>
<!-- ### Downloading Files -->
### Downloading Files

<!-- The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method: -->
`download` 메서드는 사용자의 브라우저가 해당 경로의 파일을 강제로 다운로드하도록 하는 응답을 생성합니다. `download` 메서드는 두 번째 인수로 파일 다운로드 시 표시될 파일명을 지정할 수 있으며, 세 번째 인수에 HTTP 헤더 배열도 전달 가능합니다.

```
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a name="file-urls"></a>
<!-- ### File URLs -->
### File URLs

<!-- You may use the `url` method to get the URL for a given file. If you are using the `local` driver, this will typically just prepend `/storage` to the given path and return a relative URL to the file. If you are using the `s3` driver, the fully qualified remote URL will be returned: -->
`url` 메서드를 사용해 특정 파일의 URL을 가져올 수 있습니다. `local` 드라이버를 사용할 경우, 주로 `/storage`를 경로 앞에 덧붙여 해당 파일의 상대 URL을 반환합니다. `s3` 드라이버를 사용하는 경우, 완전한 원격 URL이 반환됩니다.

```
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

<!-- When using the `local` driver, all files that should be publicly accessible should be placed in the `storage/app/public` directory. Furthermore, you should [create a symbolic link](#the-public-disk) at `public/storage` which points to the `storage/app/public` directory. -->
`local` 드라이버를 사용할 때, 공개적으로 접근 가능한 모든 파일은 `storage/app/public` 디렉터리에 위치해야 합니다. 또한, [create a symbolic link](#the-public-disk)하여 `public/storage`가 `storage/app/public`을 가리키도록 설정해야 합니다.

> [!NOTE]
> `local` 드라이버 사용 시 `url` 메서드의 반환값은 URL 인코딩이 적용되지 않습니다. 따라서, 항상 유효한 URL이 생성될 수 있는 파일 이름을 사용하여 파일을 저장하는 것을 권장합니다.

<a name="temporary-urls"></a>
<!-- #### Temporary URLs -->
#### Temporary URLs

<!-- Using the `temporaryUrl` method, you may create temporary URLs to files stored using the `s3` driver. This method accepts a path and a `DateTime` instance specifying when the URL should expire: -->
`temporaryUrl` 메서드를 사용하면 `s3` 드라이버로 저장된 파일에 대해 임시로 접근 가능한 URL을 생성할 수 있습니다. 이 메서드는 파일 경로와, URL 만료 시점을 지정하는 `DateTime` 인스턴스를 받습니다.

```
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->addMinutes(5)
);
```

<!-- If you need to specify additional [S3 request parameters](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests), you may pass the array of request parameters as the third argument to the `temporaryUrl` method: -->
추가로 [S3 request parameters](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)를 더 지정해야 한다면, 파라미터 배열을 `temporaryUrl` 메서드의 세 번째 인수로 전달할 수 있습니다.

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
특정 스토리지 디스크에 대해 임시 URL 생성 방식을 커스터마이즈해야 한다면, `buildTemporaryUrlsUsing` 메서드를 활용할 수 있습니다. 예를 들어, 임시 URL을 기본적으로 지원하지 않는 디스크에 저장된 파일을 다운로드할 수 있도록 컨트롤러에서 이 기능을 활용할 수 있습니다. 보통 이 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출하는 것이 좋습니다.

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
`Storage` 파사드를 사용해 생성되는 URL의 호스트를 미리 지정하고 싶다면, 디스크 설정 배열에 `url` 옵션을 추가하면 됩니다.

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
파일의 읽기 및 쓰기뿐만 아니라, Laravel은 파일 자체에 대한 정보도 제공합니다. 예를 들어, `size` 메서드는 파일의 바이트 단위 크기를 반환합니다.

```
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

<!-- The `lastModified` method returns the UNIX timestamp of the last time the file was modified: -->
`lastModified` 메서드는 파일이 마지막으로 수정된 시점의 UNIX 타임스탬프를 반환합니다.

```
$time = Storage::lastModified('file.jpg');
```

<a name="file-paths"></a>
<!-- #### File Paths -->
#### File Paths

<!-- You may use the `path` method to get the path for a given file. If you are using the `local` driver, this will return the absolute path to the file. If you are using the `s3` driver, this method will return the relative path to the file in the S3 bucket: -->
`path` 메서드를 사용하면 특정 파일의 경로를 얻을 수 있습니다. `local` 드라이버를 사용할 경우, 해당 파일의 절대 경로를 반환합니다. `s3` 드라이버를 사용할 경우, S3 버킷 내에서의 상대 경로가 반환됩니다.

```
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a name="storing-files"></a>
<!-- ## Storing Files -->
## Storing Files

<!-- The `put` method may be used to store file contents on a disk. You may also pass a PHP `resource` to the `put` method, which will use Flysystem's underlying stream support. Remember, all file paths should be specified relative to the "root" location configured for the disk: -->
`put` 메서드를 이용해 파일 내용물을 디스크에 저장할 수 있습니다. PHP의 `resource`를 `put` 메서드에 전달할 수도 있으며, 이 경우 Flysystem의 스트림 지원 기능을 사용할 수 있습니다. 모든 파일 경로는 반드시 디스크에 설정한 "root" 기반의 상대 경로임을 기억하세요.

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a name="automatic-streaming"></a>
<!-- #### Automatic Streaming -->
#### Automatic Streaming

<!-- Streaming files to storage offers significantly reduced memory usage. If you would like Laravel to automatically manage streaming a given file to your storage location, you may use the `putFile` or `putFileAs` method. This method accepts either an `Illuminate\Http\File` or `Illuminate\Http\UploadedFile` instance and will automatically stream the file to your desired location: -->
파일을 저장할 때 스트리밍을 활용하면 메모리 사용량을 크게 줄일 수 있습니다. Laravel이 파일 스트리밍을 자동으로 관리하도록 하려면 `putFile` 또는 `putFileAs` 메서드를 사용할 수 있습니다. 이 메서드들은 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받은 뒤, 해당 파일을 지정된 위치로 자동 스트림 전송합니다.

```
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// Automatically generate a unique ID for filename...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// Manually specify a filename...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

<!-- There are a few important things to note about the `putFile` method. Note that we only specified a directory name and not a filename. By default, the `putFile` method will generate a unique ID to serve as the filename. The file's extension will be determined by examining the file's MIME type. The path to the file will be returned by the `putFile` method so you can store the path, including the generated filename, in your database. -->
`putFile` 메서드와 관련해 몇 가지 중요한 점이 있습니다. 디렉터리명만 지정하고 파일명을 지정하지 않아도, 기본적으로 `putFile`이 고유 ID를 생성하여 파일 이름으로 사용합니다. 파일 확장자는 파일의 MIME 타입을 기반으로 결정됩니다. `putFile` 메서드는 실제 경로(생성된 파일명 포함)를 반환하므로, 데이터베이스 등에 해당 경로를 저장할 수 있습니다.

<!-- The `putFile` and `putFileAs` methods also accept an argument to specify the "visibility" of the stored file. This is particularly useful if you are storing the file on a cloud disk such as Amazon S3 and would like the file to be publicly accessible via generated URLs: -->
또한, `putFile` 및 `putFileAs` 메서드는 저장하는 파일의 "공개 범위(visibility)"를 지정하는 인수를 받을 수 있습니다. 예를 들어, Amazon S3 등 클라우드 디스크에 저장하고 퍼블릭 URL로 공개하고 싶을 때 유용합니다.

```
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a name="prepending-appending-to-files"></a>
<!-- #### Prepending & Appending To Files -->
#### Prepending & Appending To Files

<!-- The `prepend` and `append` methods allow you to write to the beginning or end of a file: -->
`prepend` 및 `append` 메서드는 파일 앞쪽이나 뒷쪽에 데이터를 추가할 수 있습니다.

```
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a name="copying-moving-files"></a>
<!-- #### Copying & Moving Files -->
#### Copying & Moving Files

<!-- The `copy` method may be used to copy an existing file to a new location on the disk, while the `move` method may be used to rename or move an existing file to a new location: -->
`copy` 메서드는 기존 파일을 디스크 내 새로운 위치로 복사할 때 사용하며, `move` 메서드는 기존 파일의 이름을 변경하거나 위치를 옮길 때 사용할 수 있습니다.

```
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

<a name="file-uploads"></a>
<!-- ### File Uploads -->
### File Uploads

<!-- In web applications, one of the most common use-cases for storing files is storing user uploaded files such as photos and documents. Laravel makes it very easy to store uploaded files using the `store` method on an uploaded file instance. Call the `store` method with the path at which you wish to store the uploaded file: -->
웹 애플리케이션에서 가장 흔히 파일 저장이 필요한 경우는 사용자 업로드(사진, 문서 등)입니다. Laravel에서는 업로드된 파일 인스턴스의 `store` 메서드를 통해 손쉽게 파일을 저장할 수 있습니다. 파일을 저장할 경로를 지정해 `store` 메서드를 호출하면 됩니다.

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
이 예시에서 몇 가지 중요한 점은, 디렉터리명만 지정했지만 파일명은 지정하지 않았다는 것입니다. 기본적으로 `store` 메서드는 고유 ID를 파일명으로 자동 생성합니다. 파일 확장자는 파일의 MIME 타입을 기준으로 결정됩니다. 실제 파일의 전체 경로(생성된 파일명 포함)는 `store` 메서드가 반환하므로, 데이터베이스에 쉽게 저장할 수 있습니다.

<!-- You may also call the `putFile` method on the `Storage` facade to perform the same file storage operation as the example above: -->
위와 동일한 저장을 `Storage` 파사드의 `putFile` 메서드를 통해서도 구현할 수 있습니다.

```
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a name="specifying-a-file-name"></a>
<!-- #### Specifying A File Name -->
#### Specifying A File Name

<!-- If you do not want a filename to be automatically assigned to your stored file, you may use the `storeAs` method, which receives the path, the filename, and the (optional) disk as its arguments: -->
저장된 파일에 자동으로 이름이 지정되길 원하지 않는 경우, `storeAs` 메서드를 사용해 직접 파일명을 설정할 수 있습니다. 이때는 경로와 파일명, 그리고 (옵션) 디스크명을 인수로 전달합니다.

```
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

<!-- You may also use the `putFileAs` method on the `Storage` facade, which will perform the same file storage operation as the example above: -->
`Storage` 파사드의 `putFileAs` 메서드를 사용해 동일한 작업을 할 수도 있습니다.

```
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> [!NOTE]
> 출력 불가하거나 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 파일 경로를 Laravel의 파일 저장 메서드에 전달하기 전 미리 정제하는 것을 권장합니다. 파일 경로는 `League\Flysystem\Util::normalizePath` 메서드로 정규화 처리됩니다.

<a name="specifying-a-disk"></a>
<!-- #### Specifying A Disk -->
#### Specifying A Disk

<!-- By default, this uploaded file's `store` method will use your default disk. If you would like to specify another disk, pass the disk name as the second argument to the `store` method: -->
기본적으로, 업로드 파일의 `store` 메서드는 설정한 기본 디스크를 사용합니다. 만약 다른 디스크에 파일을 저장하고 싶다면, `store` 메서드의 두 번째 인수로 디스크 이름을 전달하면 됩니다.

```
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

<!-- If you are using the `storeAs` method, you may pass the disk name as the third argument to the method: -->
`storeAs` 메서드를 사용할 경우, 디스크 이름을 세 번째 인수로 전달하면 됩니다.

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
업로드된 파일의 원래 이름과 확장자를 알고 싶다면, `getClientOriginalName` 및 `getClientOriginalExtension` 메서드를 사용할 수 있습니다.

```
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

<!-- However, keep in mind that the `getClientOriginalName` and `getClientOriginalExtension` methods are considered unsafe, as the file name and extension may be tampered with by a malicious user. For this reason, you should typically prefer the `hashName` and `extension` methods to get a name and an extension for the given file upload: -->
단, `getClientOriginalName`과 `getClientOriginalExtension` 메서드는 사용자가 심어놓은 악성 파일명, 확장자일 수 있으므로 안전하지 않습니다. 보통은 `hashName`과 `extension` 메서드를 사용해 안전하게 무작위 파일명, 확장자를 구하는 것이 좋습니다.

```
$file = $request->file('avatar');

$name = $file->hashName(); // Generate a unique, random name...
$extension = $file->extension(); // Determine the file's extension based on the file's MIME type...
```

<a name="file-visibility"></a>
<!-- ### File Visibility -->
### File Visibility

<!-- In Laravel's Flysystem integration, "visibility" is an abstraction of file permissions across multiple platforms. Files may either be declared `public` or `private`. When a file is declared `public`, you are indicating that the file should generally be accessible to others. For example, when using the S3 driver, you may retrieve URLs for `public` files. -->
Laravel의 Flysystem 통합에서 "공개 범위(visibility)"는 다양한 플랫폼에서의 파일 권한을 추상화한 개념입니다. 파일은 `public`(공개) 또는 `private`(비공개) 중 하나로 선언할 수 있습니다. `public`으로 선언된 파일은 기본적으로 외부에서 접근할 수 있음을 의미합니다. 예를 들어, S3 드라이버에서는 `public` 파일에 대해 URL을 가져올 수 있습니다.

<!-- You can set the visibility when writing the file via the `put` method: -->
파일을 저장할 때 `put` 메서드의 인수로 공개 범위를 설정할 수 있습니다.

```
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

<!-- If the file has already been stored, its visibility can be retrieved and set via the `getVisibility` and `setVisibility` methods: -->
이미 저장된 파일의 공개 범위는 `getVisibility`, 변경은 `setVisibility` 메서드로 처리할 수 있습니다.

```
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

<!-- When interacting with uploaded files, you may use the `storePublicly` and `storePubliclyAs` methods to store the uploaded file with `public` visibility: -->
업로드된 파일과 함께 작업할 때는, `storePublicly` 및 `storePubliclyAs` 메서드를 사용해 파일을 바로 `public` 공개 범위로 저장할 수 있습니다.

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
`local` 드라이버를 사용할 때, `public` [visibility](#file-visibility)는 디렉터리에는 `0755`, 파일에는 `0644` 퍼미션으로 적용됩니다. 이 권한 매핑은 애플리케이션의 `filesystems` 구성 파일에서 변경할 수 있습니다.

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
`delete` 메서드는 파일명 하나 또는 삭제할 파일명 배열을 받을 수 있습니다.

```
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

<!-- If necessary, you may specify the disk that the file should be deleted from: -->
필요하다면, 파일을 삭제할 디스크를 지정할 수도 있습니다.

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
`files` 메서드는 지정한 디렉터리 내 모든 파일의 배열을 반환합니다. 하위 디렉터리를 포함해 전체 디렉터리 트리의 모든 파일을 가져오고 싶다면, `allFiles` 메서드를 사용할 수 있습니다.

```
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a name="get-all-directories-within-a-directory"></a>
<!-- #### Get All Directories Within A Directory -->
#### Get All Directories Within A Directory

<!-- The `directories` method returns an array of all the directories within a given directory. Additionally, you may use the `allDirectories` method to get a list of all directories within a given directory and all of its subdirectories: -->
`directories` 메서드는 지정한 디렉터리 내 모든 폴더의 배열을 반환합니다. 추가로, `allDirectories` 메서드를 사용하면 하위 디렉터리를 포함한 모든 디렉터리 리스트도 얻을 수 있습니다.

```
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a name="create-a-directory"></a>
<!-- #### Create A Directory -->
#### Create A Directory

<!-- The `makeDirectory` method will create the given directory, including any needed subdirectories: -->
`makeDirectory` 메서드는 지정한 디렉터리 및 필요시 하위 디렉터리까지 생성해줍니다.

```
Storage::makeDirectory($directory);
```

<a name="delete-a-directory"></a>
<!-- #### Delete A Directory -->
#### Delete A Directory

<!-- Finally, the `deleteDirectory` method may be used to remove a directory and all of its files: -->
마지막으로, `deleteDirectory` 메서드를 사용해 해당 디렉터리와 그 안의 모든 파일을 삭제할 수 있습니다.

```
Storage::deleteDirectory($directory);
```

<a name="custom-filesystems"></a>
<!-- ## Custom Filesystems -->
## Custom Filesystems

<!-- Laravel's Flysystem integration provides support for several "drivers" out of the box; however, Flysystem is not limited to these and has adapters for many other storage systems. You can create a custom driver if you want to use one of these additional adapters in your Laravel application. -->
Laravel Flysystem 통합은 여러 종류의 "드라이버"를 기본 지원하지만, Flysystem 자체는 이 외에도 다양한 스토리지 시스템용 어댑터를 제공합니다. Laravel 애플리케이션에서 이러한 어댑터를 활용하려면 커스텀 드라이버를 생성할 수 있습니다.

<!-- In order to define a custom filesystem you will need a Flysystem adapter. Let's add a community maintained Dropbox adapter to our project: -->
커스텀 파일 시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 예를 들어, 커뮤니티가 유지보수하는 Dropbox 어댑터를 프로젝트에 추가해보겠습니다.

```
composer require spatie/flysystem-dropbox
```

<!-- Next, you can register the driver within the `boot` method of one of your application's [service providers](/docs/8.x/providers). To accomplish this, you should use the `extend` method of the `Storage` facade: -->
그 다음, 애플리케이션의 [service providers](/docs/8.x/providers) 중 하나의 `boot` 메서드에서 드라이버를 등록합니다. 이를 위해서는 `Storage` 파사드의 `extend` 메서드를 사용해야 합니다.

```
<?php

namespace App\Providers;

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
            $client = new DropboxClient(
                $config['authorization_token']
            );

            return new Filesystem(new DropboxAdapter($client));
        });
    }
}
```

<!-- The first argument of the `extend` method is the name of the driver and the second is a closure that receives the `$app` and `$config` variables. The closure must return an instance of `League\Flysystem\Filesystem`. The `$config` variable contains the values defined in `config/filesystems.php` for the specified disk. -->
`extend` 메서드의 첫 번째 인수는 드라이버 이름이며, 두 번째는 `$app`과 `$config` 변수를 받는 클로저입니다. 클로저는 반드시 `League\Flysystem\Filesystem` 인스턴스를 반환해야 하며, `$config` 변수에는 지정한 디스크에 대해 `config/filesystems.php`에 정의한 값들이 담깁니다.

<!-- Once you have created and registered the extension's service provider, you may use the `dropbox` driver in your `config/filesystems.php` configuration file. -->
확장 서비스 프로바이더를 직접 생성 및 등록한 후에는, 이제 `config/filesystems.php` 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.

