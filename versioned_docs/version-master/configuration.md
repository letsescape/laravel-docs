# 설정 (Configuration)

- [소개](#introduction)
- [환경 설정](#environment-configuration)
    - [환경 변수 타입](#environment-variable-types)
    - [환경 설정 값 가져오기](#retrieving-environment-configuration)
    - [현재 환경 결정하기](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [설정 값 접근하기](#accessing-configuration-values)
- [설정 캐싱](#configuration-caching)
- [설정 퍼블리싱](#configuration-publishing)
- [디버그 모드](#debug-mode)
- [점검(메인터넌스) 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 프레임워크의 모든 설정 파일은 `config` 디렉터리에 저장됩니다. 각 옵션에는 문서가 포함되어 있으므로 파일을 살펴보고 사용 가능한 옵션에 익숙해지시기 바랍니다.

이 설정 파일들을 통해 데이터베이스 연결 정보, 메일 서버 정보, 그리고 애플리케이션 URL, 암호화 키 등 다양한 핵심 설정 값들을 구성할 수 있습니다.

<a name="the-about-command"></a>
#### `about` 명령어

Laravel은 `about` Artisan 명령어를 통해 애플리케이션의 설정, 드라이버 및 환경에 대한 개요를 표시할 수 있습니다.

```shell
php artisan about
```

애플리케이션 개요 출력에서 특정 섹션에만 관심이 있다면 `--only` 옵션을 사용해 해당 섹션만 필터링할 수 있습니다.

```shell
php artisan about --only=environment
```

또는, 특정 설정 파일의 값을 자세히 확인하고 싶다면 `config:show` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
## 환경 설정 (Environment Configuration)

애플리케이션이 실행되는 환경에 따라 서로 다른 설정 값을 사용하는 것이 유용할 때가 많습니다. 예를 들어, 운영 서버에서는 다른 캐시 드라이버를 사용하고, 로컬 개발 환경에서는 별도의 드라이버를 사용할 수 있습니다.

이를 간편하게 관리하기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. Laravel을 새로 설치하면, 애플리케이션의 루트 디렉터리에 `.env.example` 파일이 있으며, 이 파일에는 일반적으로 사용되는 여러 환경 변수가 정의되어 있습니다. 설치 과정에서 이 파일이 자동으로 `.env` 파일로 복사됩니다.

Laravel의 기본 `.env` 파일에는 애플리케이션이 로컬 환경 또는 운영 웹서버에서 실행되는지에 따라 달라질 수 있는 일반적인 설정 값들이 담겨 있습니다. 이 값들은 Laravel의 `env` 함수를 이용해 `config` 디렉터리 내의 설정 파일에서 읽어옵니다.

여러 명이 함께 개발하는 경우, `.env.example` 파일을 계속 애플리케이션에 포함하고 업데이트하는 것이 좋습니다. 예제 설정 파일에 플레이스홀더 값을 두면, 팀의 다른 개발자들도 애플리케이션 실행에 필요한 환경 변수가 무엇인지 명확하게 알 수 있습니다.

> [!NOTE]
> `.env` 파일의 모든 변수는 서버 또는 시스템 수준의 외부 환경 변수로 덮어쓸 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

각 개발자 또는 서버마다 환경 설정이 달라질 수 있으므로, `.env` 파일은 소스 컨트롤에 커밋하지 않아야 합니다. 또한, 누군가 소스 컨트롤 저장소에 접근할 경우, 민감한 자격 증명이 노출될 위험이 있으므로 보안상 문제가 발생할 수 있습니다.

하지만, Laravel의 내장 [환경 파일 암호화](#encrypting-environment-files) 기능을 사용하면 환경 파일을 암호화하여 소스 컨트롤에 안전하게 보관할 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 로드하기 전에 Laravel은 `APP_ENV` 환경 변수가 외부에서 제공되었는지 또는 `--env` CLI 인수가 지정되었는지 확인합니다. 그렇다면, 해당 환경에 맞는 `.env.[APP_ENV]` 파일이 있다면 우선적으로 로드합니다. 파일이 없으면 기본 `.env` 파일을 사용합니다.

<a name="environment-variable-types"></a>
### 환경 변수 타입 (Environment Variable Types)

`.env` 파일 내의 모든 변수는 기본적으로 문자열로 해석됩니다. 하지만 `env()` 함수에서 더 다양한 타입을 반환할 수 있도록 하기 위해 일부 예약 값을 사용할 수 있습니다:

<div class="overflow-auto">

| `.env` 값   | `env()` 값           |
| ----------- | -------------------- |
| true        | (bool) true          |
| (true)      | (bool) true          |
| false       | (bool) false         |
| (false)     | (bool) false         |
| empty       | (string) ''          |
| (empty)     | (string) ''          |
| null        | (null) null          |
| (null)      | (null) null          |

</div>

값에 공백이 포함된 환경 변수를 정의해야 한다면, 값을 큰따옴표로 감싸면 됩니다.

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
### 환경 설정 값 가져오기

`.env` 파일에 정의된 모든 변수는 애플리케이션이 요청을 받을 때 `$_ENV` PHP 슈퍼글로벌에 로드됩니다. 하지만, 설정 파일에서는 `env` 함수를 이용해 이 변수들의 값을 가져올 수 있습니다. 실제로 Laravel의 여러 설정 파일을 보면 많은 옵션들이 이 함수를 사용하고 있음을 확인할 수 있습니다.

```php
'debug' => (bool) env('APP_DEBUG', false),
```

`env` 함수의 두 번째 인자는 "기본 값"입니다. 해당 키에 대한 환경 변수가 없으면 이 기본 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 결정하기

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수를 통해 결정됩니다. 이 값은 `App` [파사드](/docs/master/facades)의 `environment` 메서드를 통해 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

또한, `environment` 메서드에 값을 전달하여 환경이 특정 값과 일치하는지 확인할 수도 있습니다. 환경이 전달한 값 중 하나와 일치하면 `true`를 반환합니다.

```php
if (App::environment('local')) {
    // 현재 환경이 local입니다.
}

if (App::environment(['local', 'staging'])) {
    // 현재 환경이 local 또는 staging입니다.
}
```

> [!NOTE]
> 애플리케이션 환경은 서버 수준의 `APP_ENV` 환경 변수로 덮어쓸 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화 (Encrypting Environment Files)

암호화되지 않은 환경 파일은 절대 소스 컨트롤에 저장하지 않아야 합니다. 하지만, Laravel은 환경 파일을 암호화하여 애플리케이션의 다른 파일들과 함께 안전하게 소스 컨트롤에 추가할 수 있도록 지원합니다.

<a name="encryption"></a>
#### 암호화 (Encryption)

환경 파일을 암호화하려면 `env:encrypt` 명령어를 사용할 수 있습니다.

```shell
php artisan env:encrypt
```

`env:encrypt` 명령어를 실행하면 `.env` 파일이 암호화되어 `.env.encrypted` 파일로 저장됩니다. 복호화 키는 명령어 실행 결과에 표시되며, 안전한 비밀번호 관리자에 저장해야 합니다. 직접 암호화 키를 지정하려면 `--key` 옵션을 사용합니다.

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 지정하는 키의 길이는 사용 중인 암호화 알고리즘이 요구하는 키 길이와 일치해야 합니다. 기본적으로 Laravel은 `AES-256-CBC` 알고리즘을 사용하며, 32자 키가 필요합니다. 명령어에 `--cipher` 옵션을 전달하여 Laravel의 [encrypter](/docs/master/encryption)가 지원하는 다른 알고리즘도 사용할 수 있습니다.

애플리케이션에 `.env`, `.env.staging` 등 여러 환경 파일이 있다면, `--env` 옵션을 사용해서 암호화할 환경 파일을 지정할 수 있습니다.

```shell
php artisan env:encrypt --env=staging
```

<a name="readable-variable-names"></a>
#### 가독성 있는 변수명 유지 (Readable Variable Names)

환경 파일을 암호화할 때, `--readable` 옵션을 사용하면 변수명을 유지하면서 값만 암호화할 수 있습니다.

```shell
php artisan env:encrypt --readable
```

이렇게 하면 아래와 같은 형식의 암호화된 파일이 생성됩니다:

```ini
APP_NAME=eyJpdiI6...
APP_ENV=eyJpdiI6...
APP_KEY=eyJpdiI6...
APP_DEBUG=eyJpdiI6...
APP_URL=eyJpdiI6...
```

이 가독성 있는 형식은 환경 변수명이 어떤 것인지 노출하지 않고도 알 수 있도록 하여, 민감한 데이터가 노출되지 않으면서도 버전 관리나 코드 리뷰 시 어떤 변수가 추가/삭제/변경되었는지 쉽게 알 수 있습니다.

환경 파일을 복호화할 때 Laravel은 암호화 포맷을 자동으로 감지하므로, `env:decrypt` 명령어에 별도의 옵션이 필요하지 않습니다.

> [!NOTE]
> `--readable` 옵션 사용 시, 원본 환경 파일의 주석이나 빈 줄은 암호화된 출력에 포함되지 않습니다.

<a name="decryption"></a>
#### 복호화 (Decryption)

환경 파일을 복호화하려면 `env:decrypt` 명령어를 사용하면 됩니다. 이 명령어는 복호화 키가 필요한데, 이는 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 가져옵니다.

```shell
php artisan env:decrypt
```

또는 키를 `--key` 옵션으로 명령어에 직접 전달할 수도 있습니다.

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

`env:decrypt` 명령어가 실행되면 `.env.encrypted` 파일의 내용을 복호화하여 `.env` 파일에 저장하게 됩니다.

사용자 지정 암호화 알고리즘을 사용하려면 `--cipher` 옵션을 함께 사용할 수 있습니다.

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

여러 환경 파일이 있는 경우, `--env` 옵션으로 복호화할 환경 파일을 지정할 수 있습니다.

```shell
php artisan env:decrypt --env=staging
```

기존 환경 파일을 덮어쓰려면 `--force` 옵션을 추가할 수 있습니다.

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
## 설정 값 접근하기 (Accessing Configuration Values)

애플리케이션 어디에서든 `Config` 파사드 또는 전역 `config` 함수를 이용해 손쉽게 설정 값을 불러올 수 있습니다. 설정 값은 "점(dot)" 표기법(파일 이름과 옵션 이름을 점으로 연결)으로 접근할 수 있습니다. 또한, 옵션이 존재하지 않는 경우 반환할 기본 값도 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// 설정 값이 없을 시 기본 값을 반환합니다...
$value = config('app.timezone', 'Asia/Seoul');
```

실행 중에 설정 값을 변경하려면 `Config` 파사드의 `set` 메서드를 사용하거나, 배열을 `config` 함수에 전달할 수 있습니다.

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

정적 분석 지원을 위해, `Config` 파사드는 타입이 지정된 설정 값 반환 메서드도 제공합니다. 반환된 값의 타입이 기대한 타입과 일치하지 않으면 예외가 발생합니다.

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
Config::collection('config-key');
```

<a name="configuration-caching"></a>
## 설정 캐싱 (Configuration Caching)

애플리케이션의 성능을 높이기 위해서는 `config:cache` Artisan 명령어를 사용하여 모든 설정 파일을 하나의 파일로 캐싱하는 것이 좋습니다. 이 명령어는 모든 설정 옵션을 하나의 파일로 병합해 프레임워크가 빠르게 불러올 수 있게 해줍니다.

보통 운영 환경 배포 과정의 일부로 `php artisan config:cache` 명령어를 실행해야 합니다. 개발 도중에는 설정 옵션을 자주 변경하게 되므로, 로컬 개발에서는 이 명령어를 실행하지 않는 것이 좋습니다.

한 번 설정이 캐싱되면, 프레임워크는 요청이나 Artisan 명령 실행 시 더 이상 `.env` 파일을 로드하지 않습니다. 따라서, `env` 함수는 외부 시스템 수준의 환경 변수만 반환합니다.

이런 이유로, 반드시 애플리케이션의 설정(`config`) 파일 내에서만 `env` 함수를 호출해야 합니다. Laravel의 기본 설정 파일을 보면 이를 쉽게 확인할 수 있습니다. 설정 값은 애플리케이션의 어디서든 [위에서 설명한](#accessing-configuration-values) `config` 함수를 사용해 접근할 수 있습니다.

설정 캐시를 정리하려면 `config:clear` 명령어를 사용할 수 있습니다.

```shell
php artisan config:clear
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행한다면, 반드시 설정 파일 내에서만 `env` 함수를 호출해야 합니다. 설정이 캐싱된 후에는 `.env` 파일이 더 이상 로드되지 않아, `env` 함수는 외부의 시스템 수준 환경 변수만 반환합니다.

<a name="configuration-publishing"></a>
## 설정 퍼블리싱 (Configuration Publishing)

Laravel의 대부분의 설정 파일은 이미 애플리케이션의 `config` 디렉터리에 퍼블리시되어 있습니다. 하지만, `cors.php`와 `view.php`와 같이 기본적으로 퍼블리시되지 않는 파일도 있습니다. 이는 대부분의 애플리케이션에서 해당 파일을 수정할 필요가 거의 없기 때문입니다.

필요한 경우, `config:publish` Artisan 명령어를 사용해 기본적으로 퍼블리시되지 않은 설정 파일도 퍼블리시할 수 있습니다.

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
## 디버그 모드 (Debug Mode)

`config/app.php` 설정 파일의 `debug` 옵션은 사용자에게 오류에 대한 정보가 얼마나 많이 표시될지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일의 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> 로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영 환경에서는 반드시 이 값을 `false`로 설정해야 합니다. 만약 운영 환경에서 이 변수가 `true`로 되어 있으면, 민감한 설정 값이 애플리케이션의 최종 사용자에게 노출될 위험이 있습니다.**

<a name="maintenance-mode"></a>
## 점검(메인터넌스) 모드 (Maintenance Mode)

애플리케이션이 점검(메인터넌스) 모드에 들어가면, 모든 요청에 대해 사용자 정의 뷰가 표시됩니다. 이를 통해 유지보수나 업데이트 작업 중에 애플리케이션을 "비활성화"하기가 쉬워집니다. 점검 모드 체크는 애플리케이션의 기본 미들웨어 스택에 포함되어 있습니다. 점검 모드에서는 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 503 상태 코드로 발생합니다.

점검 모드를 활성화하려면 `down` Artisan 명령어를 실행합니다.

```shell
php artisan down
```

점검 모드 응답에 `Refresh` HTTP 헤더를 포함하려면, `down` 명령어를 실행할 때 `refresh` 옵션을 사용할 수 있습니다. 이 헤더는 브라우저에 지정한 시간(초) 후 페이지를 자동으로 새로고침하라고 알려줍니다.

```shell
php artisan down --refresh=15
```

`retry` 옵션을 지정하면, `Retry-After` HTTP 헤더 값이 설정되지만, 대부분의 브라우저는 이 헤더를 무시합니다.

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
#### 점검 모드 우회

점검 모드 상태에서도 특정 토큰을 이용해 애플리케이션 접근을 허용하려면, `secret` 옵션으로 우회 토큰을 지정할 수 있습니다.

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

애플리케이션을 점검 모드로 전환한 후, 이 토큰에 해당하는 URL로 접속하면 Laravel이 브라우저에 점검 모드 우회 쿠키를 발급합니다.

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

Laravel이 비밀 토큰을 직접 생성하게 하려면, `with-secret` 옵션을 사용할 수 있습니다. 애플리케이션이 점검 모드에 들어가면 비밀 토큰이 화면에 표시됩니다.

```shell
php artisan down --with-secret
```

이 숨겨진 경로에 접근하면 애플리케이션의 `/` 경로로 리디렉션됩니다. 쿠키가 발급된 이후에는 애플리케이션이 점검 모드가 아닌 것처럼 정상적으로 이용할 수 있습니다.

> [!NOTE]
> 점검 모드 비밀 토큰은 보통 영문자, 숫자, 하이픈(-) 조합으로 구성해야 하며, URL에서 의미를 갖는 `?`나 `&` 등 특수문자는 피해야 합니다.

<a name="maintenance-mode-on-multiple-servers"></a>
#### 여러 서버에서의 점검 모드

기본적으로 Laravel은 파일 기반 시스템을 사용하여 애플리케이션의 점검 모드 여부를 판단합니다. 즉, 모든 서버에서 각각 `php artisan down` 명령어를 실행해야 합니다.

대신, Laravel은 캐시 기반 점검 모드도 지원합니다. 이 방식은 한 서버에서만 `php artisan down` 명령어를 실행하면 됩니다. 이를 사용하려면 애플리케이션의 `.env` 파일에서 점검 모드 관련 변수를 아래와 같이 수정합니다. 여러 서버에서 접근 가능한 캐시 `store`를 지정해야 모든 서버에서 점검 모드가 일관되게 유지됩니다.

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### 점검 모드 뷰 미리 렌더링하기

배포 시 `php artisan down` 명령을 사용한다면, Composer 의존성이나 기타 인프라가 업데이트되는 동안에도 사용자들이 간헐적으로 에러를 만날 수 있습니다. 이는 점검 모드 렌더링을 위해 Laravel의 많은 부분이 부팅되어야 하기 때문입니다.

이런 상황을 방지하기 위해, Laravel은 요청 처리의 시작 단계에서 즉시 반환될 점검 모드(메인터넌스 모드) 뷰를 미리 렌더링해 둘 수 있습니다. 의존성 로드 전에 이 뷰가 반환되므로 보다 안정적으로 점검 모드 화면을 제공합니다. 미리 렌더링할 Blade 템플릿을 지정하려면, `down` 명령의 `render` 옵션을 사용합니다.

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
#### 점검 모드 요청 리디렉션

점검 모드에서는 사용자가 접근하는 모든 애플리케이션 URL에 대해 점검 모드 뷰가 표시됩니다. 모든 요청을 특정 URL로 리디렉션하려면 `redirect` 옵션을 사용할 수 있습니다. 예를 들어, 모든 요청을 `/` URI로 리디렉션하고 싶다면 아래와 같이 하면 됩니다.

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
#### 점검 모드 해제

점검 모드를 해제하려면 `up` 명령어를 사용합니다.

```shell
php artisan up
```

> [!NOTE]
> 기본 점검 모드 템플릿은 `resources/views/errors/503.blade.php`에 위치한 파일로 직접 커스터마이징할 수 있습니다.

<a name="maintenance-mode-queues"></a>
#### 점검 모드와 큐(Queue)

애플리케이션이 점검 모드인 동안에는 [큐에 등록된 작업](/docs/master/queues)이 처리되지 않습니다. 점검 모드를 해제하면 다시 작업이 정상적으로 처리됩니다.

<a name="alternatives-to-maintenance-mode"></a>
#### 점검 모드의 대안

점검 모드는 애플리케이션이 몇 초 동안이라도 중단(다운타임)이 필요합니다. 무중단 배포를 원한다면 [Laravel Cloud](https://cloud.laravel.com)와 같은 완전 관리형 플랫폼에서 애플리케이션을 운영하는 것이 좋은 대안입니다.