# 구성 (Configuration)

- [소개](#introduction)
- [환경 구성](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 구성 값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 확인](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [구성 값 접근](#accessing-configuration-values)
- [구성 캐싱](#configuration-caching)
- [구성 파일 퍼블리싱](#configuration-publishing)
- [디버그 모드](#debug-mode)
- [유지보수 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 프레임워크의 모든 구성 파일은 `config` 디렉토리에 저장되어 있습니다. 각 옵션에는 문서가 제공되어 있으니 파일을 자세히 살펴보고 사용할 수 있는 옵션에 익숙해지시기 바랍니다.

이러한 구성 파일을 통해 데이터베이스 연결 정보, 메일 서버 정보, 그리고 애플리케이션 URL 및 암호화 키 등과 같은 다양한 핵심 구성 값을 설정할 수 있습니다.

<a name="the-about-command"></a>
#### `about` 명령어

Laravel은 `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버, 환경에 대한 개요를 표시할 수 있습니다.

```shell
php artisan about
```

애플리케이션 개요 출력에서 특정 섹션만 보고 싶다면, `--only` 옵션을 사용해 해당 섹션만 필터링할 수 있습니다.

```shell
php artisan about --only=environment
```

또는 특정 구성 파일의 값을 자세히 확인하고 싶다면, `config:show` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 구성 (Environment Configuration)

애플리케이션이 실행되는 환경에 따라 서로 다른 구성 값을 사용하는 것이 흔히 도움이 됩니다. 예를 들어, 로컬 환경과 운영 서버에서는 서로 다른 캐시 드라이버를 사용할 수 있습니다.

이를 간편하게 관리할 수 있도록, Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. 새로 설치된 Laravel에는 애플리케이션 루트 디렉토리에 `.env.example` 파일이 포함되어 있으며, 여기에는 여러 일반적인 환경 변수가 정의되어 있습니다. Laravel 설치 과정에서 이 파일이 자동으로 `.env` 파일로 복사됩니다.

Laravel의 기본 `.env` 파일에는 로컬 환경과 운영 웹 서버에서 서로 다를 수 있는 몇 가지 기본 구성 값이 담겨 있습니다. 이러한 값은 `config` 디렉토리의 구성 파일에서 Laravel의 `env` 함수를 통해 읽게 됩니다.

팀으로 개발할 경우, `.env.example` 파일을 계속 포함하고 업데이트하는 것이 좋습니다. 예시 파일에 플레이스홀더 값을 입력하면, 팀의 다른 개발자들도 애플리케이션 실행에 필요한 환경 변수를 명확히 확인할 수 있습니다.

> [!NOTE]
> `.env` 파일의 어떤 변수든 서버 수준이나 시스템 수준의 외부 환경 변수로 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

각 개발자/서버마다 사용해야 하는 환경 구성이 다를 수 있으므로, `.env` 파일은 소스 제어에 커밋하지 않아야 합니다. 또한 만약 공격자가 소스 제어 저장소에 접근한다면 중요한 인증 정보가 노출될 수 있어 보안상 위험합니다.

하지만 Laravel의 내장 [환경 파일 암호화](#encrypting-environment-files) 기능을 이용하면 환경 파일을 암호화할 수 있습니다. 암호화된 환경 파일은 소스 제어에 안전하게 포함할 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 로딩하기 전에, Laravel은 외부에서 `APP_ENV` 환경 변수가 제공되었는지 혹은 `--env` CLI 인수가 지정되었는지 확인합니다. 만약 그렇다면, Laravel은 `.env.[APP_ENV]` 파일이 존재하는지 확인한 뒤, 존재하면 해당 파일을 로드합니다. 만약 없다면 기본 `.env` 파일이 로드됩니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입

`.env` 파일의 모든 변수는 일반적으로 문자열로 파싱되지만, `env()` 함수에서 좀 더 다양한 타입을 반환할 수 있도록 예약된 값들이 마련되어 있습니다.

<div class="overflow-auto">

| `.env` 값    | `env()` 반환값   |
| ------------ | --------------- |
| true         | (bool) true     |
| (true)       | (bool) true     |
| false        | (bool) false    |
| (false)      | (bool) false    |
| empty        | (string) ''     |
| (empty)      | (string) ''     |
| null         | (null) null     |
| (null)       | (null) null     |

</div>

값에 공백이 포함된 환경 변수를 정의하려면 값을 큰따옴표로 감싸면 됩니다.

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 구성 값 가져오기

`.env` 파일에 명시된 모든 변수는 애플리케이션이 요청을 받을 때 `$_ENV` PHP 슈퍼글로벌에 로드됩니다. 그러나 구성 파일에서는 `env` 함수를 사용해 이러한 변수의 값을 가져올 수 있습니다. 실제로 Laravel의 구성 파일을 살펴보면, 여러 옵션에서 이미 이 함수를 사용하는 모습을 확인할 수 있습니다.

```php
'debug' => (bool) env('APP_DEBUG', false),
```

`env` 함수에 두 번째로 전달하는 값은 "기본값"입니다. 해당 키에 대한 환경 변수가 없을 때 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 확인

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수로 결정됩니다. 이 값은 `App` [파사드](/docs/12.x/facades)의 `environment` 메서드를 통해 얻을 수 있습니다.

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

또한, `environment` 메서드에 인수를 전달하여 환경이 특정 값과 일치하는지 확인할 수도 있습니다. 환경이 전달한 값 중 하나와 일치하면 `true`를 반환합니다.

```php
if (App::environment('local')) {
    // 환경이 local입니다.
}

if (App::environment(['local', 'staging'])) {
    // 환경이 local 또는 staging입니다...
}
```

> [!NOTE]
> 현재 애플리케이션 환경 결정은 서버 수준의 `APP_ENV` 환경 변수를 정의하여 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화

암호화되지 않은 환경 파일을 소스 제어에 저장해서는 안 됩니다. 하지만 Laravel은 환경 파일을 암호화할 수 있게 하여, 애플리케이션을 소스 제어에 포함할 때 안전하게 다룰 수 있도록 해줍니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면, `env:encrypt` 명령어를 사용할 수 있습니다.

```shell
php artisan env:encrypt
```

`env:encrypt` 명령어를 실행하면 `.env` 파일이 암호화되어, 암호화된 내용이 `.env.encrypted` 파일로 저장됩니다. 복호화 키는 명령어 실행 결과에 제공되며, 반드시 안전한 비밀번호 관리 도구에 저장해야 합니다. 직접 암호화 키를 지정하려면, 명령어 실행 시 `--key` 옵션을 사용할 수 있습니다.

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 제공하는 키의 길이는 사용되는 암호화 알고리즘의 키 길이와 일치해야 합니다. 기본적으로 Laravel은 32자 키가 필요한 `AES-256-CBC` 알고리즘을 사용합니다. 명령어 실행 시 `--cipher` 옵션을 넘기면 Laravel의 [암호화기](/docs/12.x/encryption)가 지원하는 다른 알고리즘도 사용할 수 있습니다.

`.env`, `.env.staging` 등 여러 환경 파일이 있을 경우, `--env` 옵션에 환경명을 지정하여 암호화할 파일을 선택할 수 있습니다.

```shell
php artisan env:encrypt --env=staging
```

<a name="readable-variable-names"></a>
#### 가독성 있는 변수명 유지

환경 파일 암호화 시, `--readable` 옵션을 사용하면 변수명은 그대로 보이고 값만 암호화됩니다.

```shell
php artisan env:encrypt --readable
```

그러면 아래와 같이 변수명은 노출되고 값만 암호화된 파일이 생성됩니다.

```ini
APP_NAME=eyJpdiI6...
APP_ENV=eyJpdiI6...
APP_KEY=eyJpdiI6...
APP_DEBUG=eyJpdiI6...
APP_URL=eyJpdiI6...
```

가독성 있는 형식을 사용하면 예민한 데이터는 보호하면서도, 어떤 환경 변수가 있는지 쉽게 파악할 수 있습니다. 덕분에 pull request를 리뷰할 때도 어떤 변수가 추가, 삭제, 수정되었는지 암호를 해제할 필요 없이 확인할 수 있습니다.

환경 파일을 복호화할 때는 Laravel이 사용된 형식을 자동으로 감지하므로, `env:decrypt` 명령어에 추가 옵션이 필요하지 않습니다.

> [!NOTE]
> `--readable` 옵션을 사용할 경우, 원본 환경 파일의 주석 및 빈 줄은 암호화된 파일에 포함되지 않습니다.

<a name="decryption"></a>
#### 복호화

환경 파일을 복호화하려면, `env:decrypt` 명령어를 사용할 수 있습니다. 이 명령어는 복호화 키가 필요하며, Laravel은 이를 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 읽어옵니다.

```shell
php artisan env:decrypt
```

또는, `--key` 옵션을 통해 직접 키를 전달할 수도 있습니다.

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령어를 실행하면, `.env.encrypted` 파일의 내용을 복호화하여 `.env` 파일에 저장합니다.

커스텀 암호화 알고리즘을 사용하려면, `env:decrypt` 명령어에서 `--cipher` 옵션을 사용할 수 있습니다.

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

복수 개의 환경 파일이 있을 경우, `--env` 옵션에 환경명을 지정하여 복호화할 파일을 선택할 수 있습니다.

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면, `env:decrypt` 명령어에 `--force` 옵션을 추가합니다.

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 구성 값 접근 (Accessing Configuration Values)

애플리케이션 어디서든 `Config` 파사드 또는 전역 `config` 함수를 사용하여 구성 값에 쉽게 접근할 수 있습니다. 접근 시 파일명과 옵션명을 도트(`.`) 문법으로 사용할 수 있으며, 옵션이 없을 경우 반환할 기본값을 지정할 수도 있습니다.

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 구성 값이 없을 경우 기본값을 반환...
$value = config('app.timezone', 'Asia/Seoul');
```

실행 중에 구성 값을 설정하려면, `Config` 파사드의 `set` 메서드를 호출하거나 `config` 함수에 배열을 전달하면 됩니다.

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

정적 분석(static analysis)를 지원하기 위해, `Config` 파사드는 타입별 구성 값 조회 메서드도 제공합니다. 반환된 값이 기대하는 타입이 아닐 경우 예외가 발생합니다.

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
Config::collection('config-key');
```

<a name="configuration-caching"></a>
## 구성 캐싱 (Configuration Caching)

애플리케이션의 속도를 높이기 위해, 모든 구성 파일을 하나의 파일로 캐싱할 수 있습니다. 이를 위해 `config:cache` Artisan 명령어를 사용합니다. 이 명령어는 애플리케이션의 모든 구성 옵션을 하나의 파일로 병합하여, 프레임워크가 더욱 빠르게 로드할 수 있도록 해줍니다.

이 명령어는 보통 운영 환경 배포 과정의 일부로 실행해야 하며, 로컬 개발 도중에는 빈번한 구성 변경이 필요하므로 실행하지 않는 것이 좋습니다.

구성이 캐싱되면, 애플리케이션의 `.env` 파일은 요청이나 Artisan 명령 실행 시 프레임워크에 의해 로드되지 않습니다. 따라서 `env` 함수는 외부 시스템 환경 변수만 반환하게 됩니다.

이런 이유로, `env` 함수는 반드시 애플리케이션의 구성(`config`) 파일 안에서만 호출해야 합니다. 자세한 내용은 위의 [구성 값 접근](#accessing-configuration-values) 섹션을 참고하세요. 구성 값은 애플리케이션 어디서든 `config` 함수를 통해 접근하면 됩니다.

캐싱된 구성을 삭제하려면 `config:clear` 명령어를 사용합니다.

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행할 경우, 반드시 `env` 함수를 구성 파일 안에서만 호출하는지 확인해야 합니다. 구성이 캐싱되면 `.env` 파일이 로드되지 않으므로, `env` 함수는 오직 외부 시스템 환경 변수만 반환합니다.

<a name="configuration-publishing"></a>
## 구성 파일 퍼블리싱 (Configuration Publishing)

대부분의 Laravel 구성 파일은 이미 애플리케이션의 `config` 디렉토리에 퍼블리시되어 있습니다. 하지만, `cors.php`, `view.php` 같은 일부 파일은 대부분의 애플리케이션에서 수정할 필요가 없으므로 기본적으로는 퍼블리시되지 않습니다.

그럼에도 불구하고, 필요하다면 `config:publish` Artisan 명령어를 사용해 기본적으로 퍼블리시되지 않은 모든 구성 파일을 퍼블리시할 수 있습니다.

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드 (Debug Mode)

`config/app.php` 구성 파일의 `debug` 옵션은 실제로 사용자에게 에러 정보가 얼마나 표시되는지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> 로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영 환경에서는 이 값을 반드시 `false`로 설정하세요. 운영 환경에서 `true`로 설정하면, 민감한 구성 값이 애플리케이션 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 유지보수 모드 (Maintenance Mode)

애플리케이션이 유지보수 모드일 때, 모든 요청에 대해 커스텀 화면이 표시됩니다. 이를 통해 업데이트나 유지보수를 진행하는 동안 애플리케이션을 손쉽게 "비활성화"할 수 있습니다. 유지보수 모드 확인은 애플리케이션의 기본 미들웨어 스택에 포함되어 있으며, 유지보수 상태일 때는 `Symfony\Component\HttpKernel\Exception\HttpException`(상태 코드 503)이 발생합니다.

유지보수 모드를 활성화하려면 `down` Artisan 명령어를 실행합니다.

```shell
php artisan down
```

모든 유지보수 표시 응답에 `Refresh` HTTP 헤더를 전송하려면, `down` 명령어에 `refresh` 옵션을 사용할 수 있습니다. 이 헤더는 브라우저가 지정한 초 후에 페이지를 자동으로 새로고침하도록 안내합니다.

```shell
php artisan down --refresh=15
```

또한, `retry` 옵션을 추가하면 HTTP 응답의 `Retry-After` 헤더로 해당 값을 전송할 수 있습니다(대부분의 브라우저에서는 이 헤더를 무시합니다).

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 유지보수 모드 우회

유지보수 모드를 비밀 토큰으로 우회하도록 하려면, `secret` 옵션을 사용해 우회 토큰을 지정할 수 있습니다.

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

유지보수 모드 상태에서 위 토큰에 해당하는 애플리케이션 URL로 접근하면, Laravel이 유지보수 모드 우회 쿠키를 브라우저에 발급합니다.

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Laravel이 비밀 토큰을 자동 생성하도록 하려면, `with-secret` 옵션을 사용하면 됩니다. 생성된 비밀 토큰은 애플리케이션이 유지보수 모드에 진입한 이후에 표시됩니다.

```shell
php artisan down --with-secret
```

이 숨겨진 경로로 접속하면 `/` 경로로 리디렉션되어, 쿠키가 발급된 후에는 유지보수 모드가 아닌 것처럼 애플리케이션을 정상적으로 이용할 수 있습니다.

> [!NOTE]
> 유지보수 모드 비밀 토큰 값은 일반적으로 영문, 숫자, 그리고 선택적으로 대시(-)로 구성해야 하며, `?`, `&`처럼 URL에서 특별한 의미를 갖는 문자는 피해야 합니다.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 다중 서버에서의 유지보수 모드

Laravel은 기본적으로 파일 기반 방식으로 유지보수 모드 진입 여부를 판단합니다. 즉, 애플리케이션이 여러 서버에 배포되어 있다면 각 서버에서 `php artisan down` 명령을 각각 실행해야 유지보수 모드가 적용됩니다.

대신 Laravel은 캐시 기반 유지보수 모드 방식도 제공합니다. 이 방법을 사용하면 한 서버에서만 `php artisan down` 명령을 실행해도 전체 서버에 유지보수 상태가 공유됩니다. 이를 위해서는 `.env` 파일의 유지보수 모드 관련 변수를 아래처럼 설정하고, 모든 서버에서 접근 가능한 캐시 `store`를 지정해야 합니다.

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 유지보수 모드 뷰 미리 렌더링

배포 과정에서 `php artisan down` 명령을 활용하는 경우, Composer 의존성이나 기타 인프라 요소가 업데이트되는 동안에도 사용자가 접속한다면 종종 에러가 발생할 수 있습니다. 이는 Laravel 프레임워크의 많은 부분이 부팅되어야만 유지보수 모드 여부를 판별하고, 미들웨어 및 템플릿 엔진을 통해 유지보수 화면을 렌더링할 수 있기 때문입니다.

이 문제를 해결하기 위해, Laravel은 요청 사이클의 맨 초기에 반환될 미리 렌더링된 유지보수 뷰를 제작할 수 있습니다. 이 뷰는 애플리케이션의 어떤 의존성도 로드되기 전에 표시됩니다. 원하는 템플릿을 미리 렌더링하려면 `down` 명령어의 `render` 옵션을 사용하면 됩니다.

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 유지보수 모드 요청 리디렉션

유지보수 모드에서 Laravel은 사용자가 접근하는 모든 URL에 대해 유지보수 뷰를 표시합니다. 대신 모든 요청을 특정 URL로 리디렉션(pf)하도록 설정할 수도 있습니다. 예를 들어, 모든 요청을 `/` URI로 리디렉션하고 싶을 때는 다음과 같이 명령어를 사용합니다.

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 유지보수 모드 해제

유지보수 모드를 비활성화하려면 `up` 명령어를 사용합니다.

```shell
php artisan up
```

> [!NOTE]
> 기본 유지보수 모드 템플릿은 `resources/views/errors/503.blade.php`에 직접 정의하여 커스터마이즈할 수 있습니다.

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 유지보수 모드일 때는 [큐 처리 작업](/docs/12.x/queues)이 수행되지 않습니다. 유지보수 모드를 해제하면 큐 작업은 다시 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 유지보수 모드의 대안

유지보수 모드는 필연적으로 몇 초간 애플리케이션의 다운타임이 발생합니다. 다운타임 없는(Zero-downtime) 배포가 필요하다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 완전 관리형 플랫폼에서 애플리케이션을 실행하는 것을 고려해 볼 수 있습니다.