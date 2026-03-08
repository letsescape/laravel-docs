# 파일 스토리지 (File Storage)

- [소개](#introduction)
- [설정](#configuration)
    - [Local 드라이버](#the-local-driver)
    - [Public 디스크](#the-public-disk)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [Scoped 및 Read-Only 파일 시스템](#scoped-and-read-only-filesystems)
    - [Amazon S3 호환 파일 시스템](#amazon-s3-compatible-filesystems)
- [디스크 인스턴스 가져오기](#obtaining-disk-instances)
    - [On-Demand 디스크](#on-demand-disks)
- [파일 조회](#retrieving-files)
    - [파일 다운로드](#downloading-files)
    - [파일 URL](#file-urls)
    - [임시 URL](#temporary-urls)
    - [파일 메타데이터](#file-metadata)
- [파일 저장](#storing-files)
    - [파일 앞/뒤에 내용 추가](#prepending-appending-to-files)
    - [파일 복사 및 이동](#copying-moving-files)
    - [자동 스트리밍](#automatic-streaming)
    - [파일 업로드](#file-uploads)
    - [파일 가시성](#file-visibility)
- [파일 삭제](#deleting-files)
- [디렉토리](#directories)
- [테스트](#testing)
- [커스텀 파일 시스템](#custom-filesystems)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 Frank de Jonge가 만든 훌륭한 PHP 패키지인 [Flysystem](https://github.com/thephpleague/flysystem)을 기반으로 강력한 파일 시스템 추상화 기능을 제공합니다. Laravel의 Flysystem 통합은 로컬 파일 시스템, SFTP, Amazon S3와 같은 저장소를 간단하게 사용할 수 있는 드라이버를 제공합니다. 더 나아가, 각 시스템에서 동일한 API를 사용하기 때문에 로컬 개발 환경과 운영 서버 간에 스토리지 옵션을 매우 쉽게 전환할 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

Laravel의 파일 시스템 설정 파일은 `config/filesystems.php`에 있습니다. 이 파일에서 애플리케이션에서 사용할 모든 파일 시스템 "디스크(disk)"를 설정할 수 있습니다. 각 디스크는 특정 스토리지 드라이버와 저장 위치를 의미합니다. 설정 파일에는 지원되는 각 드라이버의 예시 설정이 포함되어 있으므로, 자신의 스토리지 환경과 인증 정보에 맞게 수정할 수 있습니다.

`local` 드라이버는 Laravel 애플리케이션이 실행되는 서버의 로컬 파일을 다루며, `sftp` 드라이버는 SSH 키 기반 FTP를 사용할 때 사용합니다. `s3` 드라이버는 Amazon의 S3 클라우드 스토리지 서비스를 사용하기 위해 사용됩니다.

> [!NOTE]
> 원하는 만큼 많은 디스크를 설정할 수 있으며, 동일한 드라이버를 사용하는 여러 디스크를 구성할 수도 있습니다.

<a name="the-local-driver"></a>
### Local 드라이버

`local` 드라이버를 사용할 때 모든 파일 작업은 `filesystems` 설정 파일에 정의된 `root` 디렉토리를 기준으로 이루어집니다. 기본값은 `storage/app/private` 디렉토리입니다. 따라서 다음 메서드는 `storage/app/private/example.txt` 파일을 생성합니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a name="the-public-disk"></a>
### Public 디스크

애플리케이션의 `filesystems` 설정 파일에 포함된 `public` 디스크는 공개적으로 접근 가능한 파일을 저장하기 위한 디스크입니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며 `storage/app/public` 디렉토리에 파일을 저장합니다.

`public` 디스크가 `local` 드라이버를 사용하고 있고 웹에서 해당 파일에 접근하려면, `storage/app/public` 디렉토리를 `public/storage` 디렉토리로 연결하는 심볼릭 링크를 생성해야 합니다.

심볼릭 링크는 `storage:link` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan storage:link
```

파일을 저장하고 심볼릭 링크를 생성한 후에는 `asset` 헬퍼를 사용하여 파일 URL을 생성할 수 있습니다.

```php
echo asset('storage/file.txt');
```

추가적인 심볼릭 링크를 `filesystems` 설정 파일에 정의할 수도 있습니다. `storage:link` 명령어를 실행하면 설정된 모든 링크가 생성됩니다.

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

설정된 심볼릭 링크를 삭제하려면 `storage:unlink` 명령어를 사용할 수 있습니다.

```shell
php artisan storage:unlink
```

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="s3-driver-configuration"></a>
#### S3 드라이버 설정

S3 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem S3 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

S3 디스크 설정 배열은 `config/filesystems.php` 파일에 있습니다. 일반적으로 다음과 같은 환경 변수를 사용하여 S3 자격 증명과 설정을 구성합니다. 이 값들은 `config/filesystems.php` 설정 파일에서 참조됩니다.

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

편의를 위해 이러한 환경 변수 이름은 AWS CLI에서 사용하는 명명 규칙과 동일하게 맞춰져 있습니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 설정

FTP 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem FTP 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-ftp "^3.0"
```

Laravel의 Flysystem 통합은 FTP와 잘 동작하지만, 기본 `config/filesystems.php` 설정 파일에는 FTP 설정 예제가 포함되어 있지 않습니다. FTP 파일 시스템을 설정하려면 다음과 같은 설정 예시를 사용할 수 있습니다.

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
#### SFTP 드라이버 설정

SFTP 드라이버를 사용하기 전에 Composer 패키지 매니저를 통해 Flysystem SFTP 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

Laravel의 Flysystem 통합은 SFTP와도 잘 동작하지만, 기본 `config/filesystems.php` 설정 파일에는 SFTP 설정 예제가 포함되어 있지 않습니다. SFTP 파일 시스템을 설정하려면 다음 예시를 사용할 수 있습니다.

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
### Scoped 및 Read-Only 파일 시스템

Scoped 디스크를 사용하면 모든 경로에 특정 경로 prefix가 자동으로 붙는 파일 시스템을 정의할 수 있습니다. Scoped 파일 시스템 디스크를 생성하기 전에 Composer를 통해 추가 Flysystem 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

`scoped` 드라이버를 사용하는 디스크를 정의하면 기존 파일 시스템 디스크를 특정 경로 prefix로 제한할 수 있습니다. 예를 들어 기존 `s3` 디스크를 특정 경로로 제한하는 디스크를 생성할 수 있습니다. 이 디스크를 통해 수행되는 모든 파일 작업은 해당 prefix를 사용합니다.

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

"Read-only" 디스크를 사용하면 쓰기 작업을 허용하지 않는 파일 시스템 디스크를 만들 수 있습니다. `read-only` 옵션을 사용하기 전에 Composer를 통해 추가 Flysystem 패키지를 설치해야 합니다.

```shell
composer require league/flysystem-read-only "^3.0"
```

그 다음 디스크 설정 배열에 `read-only` 옵션을 추가할 수 있습니다.

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 호환 파일 시스템

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 `s3` 디스크 설정이 포함되어 있습니다. 이 디스크는 [Amazon S3](https://aws.amazon.com/s3/)뿐 아니라 다음과 같은 S3 호환 스토리지 서비스와도 사용할 수 있습니다.

- [RustFS](https://github.com/rustfs/rustfs)  
- [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/)  
- [Vultr Object Storage](https://www.vultr.com/products/object-storage/)  
- [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/)  
- [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/)

일반적으로 사용하려는 서비스의 인증 정보로 디스크 설정을 변경한 뒤, `endpoint` 설정 값만 수정하면 됩니다. 이 값은 보통 `AWS_ENDPOINT` 환경 변수로 정의됩니다.

```php
'endpoint' => env('AWS_ENDPOINT', 'https://rustfs:9000'),
```

<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 가져오기 (Obtaining Disk Instances)

`Storage` 파사드(facade)를 사용하면 설정된 모든 디스크와 상호작용할 수 있습니다. 예를 들어 기본 디스크에 아바타 이미지를 저장하려면 `put` 메서드를 사용할 수 있습니다. `disk` 메서드를 호출하지 않으면 기본 디스크가 자동으로 사용됩니다.

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

애플리케이션에서 여러 디스크를 사용하는 경우 `disk` 메서드를 통해 특정 디스크를 지정할 수 있습니다.

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a name="on-demand-disks"></a>
### On-Demand 디스크

런타임(runtime)에 특정 설정으로 디스크를 생성해야 하는 경우도 있습니다. 이때는 `filesystems` 설정 파일에 정의하지 않고 `Storage` 파사드의 `build` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```